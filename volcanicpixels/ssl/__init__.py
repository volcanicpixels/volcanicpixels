# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl
    ~~~~~~~~~~~~~~~~~~

    The SSL Api.
"""
import stripe
import logging
from itsdangerous import URLSafeSerializer, BadPayload, BadSignature
from flask import session, request, current_app
from volcanicpixels.users import (
    get_current_user, get_user, authenticate_user, create_user,
    UserAuthenticationFailedError)
from sslstore_api.methods import check_csr, create_dv_ssl_order
from sslstore_api.errors import WildCardCSRError
from .csr import CertificationRequest
from .data import REGIONS
from .helpers import get_keypair, is_academic
from .errors import (
    CVCCheckFailedError, SSLCertificateNotFoundError,
    UserNotProvidedError, NonAcademicEmailError, DomainCouponMismatchError)
from .models import SSLCertificate


def create_certificate(csr, **kwargs):
    return SSLCertificate.create(csr, **kwargs)


def get_certificate(order_id, user=None):
    """Gets a certificate by order_id, this should ideally called with the
    user argument to ensure consistency (ancestorless datastore queries can
    return stale results)
    """
    try:
        return SSLCertificate.get(order_id, user)
    except SSLCertificateNotFoundError:
        return None


def get_user_certificates(user=None, limit=20):
    if user is None:
        user = get_current_user()
    if user is None:
        # No user was provided to the function and a user it not loggedin
        raise UserNotProvidedError()

    return SSLCertificate.query(
        ancestor=user.key
    ).order(
        -SSLCertificate.created_at
    ).fetch(limit)


def do_error(msg='An error occured'):
    raise Exception(msg)


def check_request(options):
    """
    Do as many preliminary checks as possible
    """

    promotion = options.get('promotion', None)
    email = options.get('email')
    domain = options.get('domain', '')
    approver_email = options.get('approver_email', None)

    if 'user' in options:
        user = options['user']
    else:
        user = get_current_user()

    if user is not None:
        email = user.email

    if 'csr' not in options:

        # check that a domain name has been submitted
        if len(domain) == 0:
            do_error("You haven't submitted a domain")

    # check for academic status
    if promotion == 'academic':
        if not is_academic(email):
            raise NonAcademicEmailError(
                'The email address %s is not an accepted academic email'
                % email)

    # Check that approver email has been selected
    if approver_email is None:
        do_error('No approver email has been selected')

    return options


def normalize_request(options):
    """Normalize request

    After this, the user should be created and logged in, they
    should have a stripe id associated with them and if a token was passed
    as credit_card then it should be converted into a stripe card id.

    TODO: update existing user if additional information is provided
    """

    credit_card = options.get('credit_card')
    country = options.get('country')
    state = options.get('state')
    coupon_code = options.get('coupon_code')
    domain = options.get('domain')

    options['amount'] = 35

    if coupon_code is not None:
        s = URLSafeSerializer(
            current_app.config.get('SECRET_KEY'), salt='SSL_COUPON')
        # Load the coupon
        try:
            options['coupon'] = coupon = s.loads(coupon_code)
            # coupon should contain price, domain

            if 'domain' in coupon and coupon['domain'] != '':
                if domain is not None and domain != coupon['domain']:
                    raise DomainCouponMismatchError(coupon['domain'], domain)

            if 'price' in coupon:
                options['amount'] = coupon['price']

            options['coupon_message'] = 'Coupon applied'
        except BadPayload, e:
            options['coupon_code'] = None
            options['error'] = 'The coupon entered is not valid'
        except BadSignature, e:
            options['coupon_code'] = None
            options['error'] = 'This coupon has been tampered with'

    if country in REGIONS and state in REGIONS[country]:
        options['state'] = REGIONS[country][state]

    def is_token(value):
        """Determines whether the passed argument is a stripe token or not"""
        if value is None:
            return False
        return (value[:3] == 'tok')

    if 'user' in options:
        user = options['user']
    else:
        user = get_current_user()

    if not user:
        # user is not logged in, let's see if the email is attached to an
        # account
        email = options.get('email')
        password = options.get('password')
        name = options.get('name')
        user = get_user(email)

        if user:
            # account exists - try to authenticate
            try:
                authenticate_user(email, password)
            except UserAuthenticationFailedError:
                return do_error('Password is incorrect')
        else:
            # this is a new account
            user = create_user(email, password, name=name)
            session['user'] = user.key.id()

    if not user.name:
        name = options.get('name')
        user.name = name

    if not user.stripe_id:
        # User doesn't have a stripe customer ID
        customer = stripe.Customer.create(
            description=name,
            email=email
        )

        user.stripe_id = customer.id
        if is_token(credit_card):
            card = customer.cards.create(card=credit_card)
            credit_card = card.id
    else:
        # User has a stripe ID
        customer = stripe.Customer.retrieve(user.stripe_id)
        if is_token(credit_card):
            # this is a new card
            card = customer.cards.create(card=credit_card)
            credit_card = card.id

    user.put()

    if 'csr' not in options:
        # We need to generate the CSR
        keypair = get_keypair(False)
        csr = CertificationRequest(keypair=keypair)

        # Set fields
        domain = options.get('domain')
        organization = options.get('organization')
        state = options.get('state')
        country = options.get('country')
        phone_number = options.get('phone_number')
        email = user.email

        csr.set_subject_field('common_name', domain)
        csr.set_subject_field('organization', organization)
        csr.set_subject_field('state', state)
        csr.set_subject_field('country', country)
        csr.set_subject_field('telephone', phone_number)
        csr.set_subject_field('email_address', email)

        options['csr'] = csr.export()
        options['keypair'] = keypair.exportKey()

    options['credit_card'] = credit_card
    options['user'] = user

    if request.args.get('promotion') == 'academic':
        options['academic'] = True

    if options.get('promotion', '') == 'academic':
        options['academic'] = True

    return options


def process_request(options):
    keypair = options.get('keypair', None)
    csr = options.get('csr', 'NO_CSR')
    user = options.get('user', None)
    domain = options.get('domain', None)
    approver_email = options.get('approver_email', None)
    price = options.get('price')
    coupon = options.get('coupon')

    # TODO: Consume nonce and regurgitate on exception

    try:
        result = check_csr(csr)
        if result['isWildcardCSR']:
            raise WildCardCSRError()
    except:
        raise

    # Now let's authorise a stripe payment

    card = options.get('credit_card', None)
    customer = user.stripe_id
    amount = options.get('amount', 35)
    description = "SSL certificate for %s" % domain

    if options.get('promotion') == 'academic':
        amount = 15

    amount = int(amount)
    price = int(price)

    if amount != price:
        do_error('Price sanity check failed, expected %s but got %s'
                 % (str(amount), str(price)))

    # TODO: BQ and datastore

    logging.info('Checks passed')
    logging.info('Amount: %s' % amount)

    if amount == 0:
        charge_id = None
    else:
        try:
            charge = stripe.Charge.create(
                amount=amount * 100,
                currency="gbp",
                card=card,
                customer=customer,
                description=description,
                capture=False
            )
        except:
            raise

        if charge.card.cvc_check == "fail":
            raise CVCCheckFailedError()

        charge_id = charge.id

    # Payment authorised, now let's get this certificate!

    ssl_certificate = create_certificate(
        parent=user.key,
        csr=csr,
        keypair=keypair,
        domain=domain,
        charge_id=charge_id,
        provider="sslstore",
        status="created"
    )

    ssl_certificate.put()

    result = create_dv_ssl_order(
        csr,
        domain,
        approver_email
    )

    ssl_certificate.order_id = result['TheSSLStoreOrderID']
    ssl_certificate.status = "pending"

    if 'VendorOrderID' in result:
        ssl_certificate.vendor_id = result['VendorOrderID']

    ssl_certificate.put()

    # Now actually charge the credit card
    # TODO: If this fails (which it should never do since the bank has issued
    # an authorization which is essentially a promise that it can do the
    # payment then we should automatically lock the SSL certificate)
    #
    # Also this can be wrapped in a deferred to benefit from automatic
    # retrying.

    if amount != 0:
        charge.capture()

    return ssl_certificate
