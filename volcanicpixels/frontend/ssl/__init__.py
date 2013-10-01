# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import logging
import sys
from StringIO import StringIO
import zipfile
import stripe
from flask import (
    jsonify, request, render_template, url_for, redirect, make_response)
from flask.ext.volcano import create_blueprint
from sslstore_api.methods import (
    get_approver_emails as _get_approver_emails, get_order_status,
    get_certificates, resend_email as _resend_email, check_csr)
from sslstore_api.errors import WildCardCSRError
from volcanicpixels.ssl import (
    normalize_request, process_request, get_user_certificates,
    get_certificate)
from volcanicpixels.users import (
    get_user, UserAuthenticationFailedError, get_current_user, User)

from volcanicpixels.ssl.data import COUNTRIES_BY_NAME, REGIONS
from .helpers import fix_unicode

bp = create_blueprint("ssl", __name__, url_prefix="/ssl")


@bp.route('/')
def render():
    return buy(template="ssl")


@bp.route('/buy')
def buy(defaults=None, template="ssl/buy"):
    if defaults is None:
        defaults = {}
    country = request.headers.get('X-Appengine-Country', '').upper()
    region = request.headers.get('X-AppEngine-Region', '').upper()

    if 'country' not in defaults:
        # When App Engine is running locally or cannot determine country it
        # returns ZZ as the country code.
        if country == 'ZZ':
            country = 'GB'

        if country is not None:
            defaults['country'] = country
        else:
            defaults['country'] = 'US'

    if 'state' not in defaults:
        if country in REGIONS and region in REGIONS[country]:
            defaults['state'] = REGIONS[country][region]

    return render_template(template, countries=COUNTRIES_BY_NAME, **defaults)


@bp.route('/upload-csr')
def upload_csr(defaults=None, template="ssl/buy"):
    if defaults is None:
        defaults = {}

    return render_template(
        template, countries=COUNTRIES_BY_NAME, upload_csr=True, **defaults)


@bp.route('/buy', methods=['POST'])
def process_order():
    options = {}
    for key in request.form:
        options[key] = request.form[key]
    try:
        options = normalize_request(options)
        cert = process_request(options)
    except WildCardCSRError:
        options['error'] = "Wildcard domain not allowed"
    except:
        logging.exception("Uncaught exception while processing order")
        options['error'] = "An error occured, we have emailed an admin."
    finally:
        return buy(options)

    return redirect(url_for('.complete_order', order_id=cert.order_id))


@bp.route('/complete')
def complete_order():
    """
    Complete order page, either takes a SSLCertificate ID as an arg or get's
    the users most recent SSL certificate.
    """
    user = get_current_user()

    if not user:
        # TODO: fix redirect path to include args
        return redirect(url_for('auth.login', redirect=request.path))

    order_id = request.args.get('order_id', None)

    if order_id is None:
        # Fetch User's last certificate
        certs = get_user_certificates(limit=1)

        if len(certs) == 0:
            # Not sure how they got here, best log an error
            logging.error("User has no certificates")
            raise Exception("Certificate not found")

        cert = certs[0]
    else:
        cert = get_certificate(order_id, user)
        if cert is None:
            logging.error('Certificate not found')
            raise Exception("Certificate not found")

    #if cert.status != 'pending':
        # TODO: redirect to dashboard
        #return "Already setup"

    return render_template('ssl/complete', certificate=cert)


@bp.route('/download')
def download():
    """
    Prepares the certificates for download (TODO: redirect to GS)
    """
    user = get_current_user()

    if not user:
        # TODO: fix redirect path to include args
        return redirect(url_for('auth.login', redirect=request.path))

    order_id = request.args.get('order_id', None)
    download_type = request.args.get('type', "appengine")
    force = request.args.get('force', None)

    if order_id is None:
        # Fetch User's last certificate
        certs = get_user_certificates(limit=1)

        if len(certs) == 0:
            # Not sure how they got here, best log an error
            logging.error("User has no certificates")
            raise Exception("Certificate not found")

        cert = certs[0]
    else:
        cert = get_certificate(order_id, user)
        if cert is None:
            logging.error('Certificate not found')
            raise Exception("Certificate not found")

    cert_modified = False

    if cert.certs is None or force:
        certificates = get_certificates(order_id)
        cert.certs = certificates['Certificates']
        cert_modified = True

    if cert.appengine_cert is None or force:
        appengine_cert = ''
        top = middle = bottom = None
        for _cert in cert.certs:
            logging.info(_cert)
            if _cert['FileName'] == 'PositiveSSLCA2.crt':
                middle = _cert['FileContent']
            if _cert['FileName'] == 'AddTrustExternalCARoot.crt':
                bottom = _cert['FileContent']
            else:
                top = _cert['FileContent']

        if top is not None and middle is not None and bottom is not None:
            appengine_cert = top + middle + bottom
        else:
            logging.error("Predefined ssl merging rules failed")
            for _cert in cert.certs:
                appengine_cert += _cert['FileContent']
        cert.appengine_cert = appengine_cert
        cert_modified = True

    if cert_modified:
        cert.put()

    output = StringIO()
    z = zipfile.ZipFile(output, 'w')

    if download_type == 'appengine':
        z.writestr("certificate.crt", fix_unicode(cert.appengine_cert))

    if download_type == 'unformatted':
        for _cert in cert.certs:
            z.writestr(
                fix_unicode(_cert['FileName']),
                fix_unicode(_cert['FileContent'])
            )

    if cert.keypair is not None:
        z.writestr("privatekey.key", fix_unicode(cert.keypair))

    z.close()
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "multipart/x-zip"
    response.headers['Content-Disposition'] = "attachment; " + \
                                              "filename=ssl_bundle.zip"
    return response


@bp.route('/resend_email')
def resend_email():
    order_id = request.args.get('order_id', None)
    try:
        _resend_email(order_id)
        return jsonify(status='SUCCESS', data="SUCCESS")
    except:
        msg = "Could not resend email, contact support"
        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)


@bp.route('/order_status')
def order_status():
    """Checks the status of an order and returns a filtered object"""
    order_id = request.args.get("order_id")
    user = get_current_user()

    """Security:

    Here we are fetching the certificate entity attached to this order_id
    from the database, if this fails then either the order_id is wrong, in
    which case the subsequent API call would fail, or it belongs to another
    user. Without this an authenticated user could access other people's
    order statuses.
    """
    cert = get_certificate(order_id, user)
    if not cert:
        msg = "Order %s does not exist or belongs to another user." % order_id
        return jsonify(status='ERROR', msg=msg)
    if cert.status == 'active':
        return jsonify(status='SUCCESS', data={'status': 'active'})
    try:
        result = get_order_status(order_id)
        data = {}
        status = result['OrderStatus']['MajorStatus']
        if status == 'Pending':
            data['status'] = 'pending'
        elif status == 'Active':
            cert.status = 'active'
            cert.put()
            data['status'] = 'active'
        else:
            logging.error("Unknown status %s" % status)

        data['approver_email'] = result['ApproverEmail']

        return jsonify(status='SUCCESS', data=data)

    except:
        logging.exception("Error checking order status")
        return jsonify(
            status='ERROR',
            msg="An error occured checking the order status"
        )


@bp.route('/get_approver_emails')
def get_approver_emails():
    """Get's the approver emails for a domain and returns an API response"""
    domain = request.args.get("domain", '')
    try:
        emails = _get_approver_emails(domain)
        return jsonify(status='SUCCESS', data=emails)
    except:
        msg = "An error occured whilst trying to retrieve the " + \
            "verification emails for %s" % domain
        return jsonify(status='ERROR', msg=msg)


@bp.route('/verify_csr')
def verify_csr():
    csr = request.args.get("csr", '')
    if csr == '':
        return jsonify(status='ERROR', msg="You haven't entered anything")
    try:
        result = check_csr(csr)
        if result['isWildcardCSR']:
            return jsonify(
                status='ERROR',
                msg="This CSR is for a wildcard certificate"
            )
        if 'DominName' in result:
            domain = result['DominName']
        else:
            domain = result['DomainName']
        emails = _get_approver_emails(domain)
        data = {'emails': emails, 'domain': domain}
        return jsonify(status='SUCCESS', data=data)
    except:
        logging.exception("Uncaught CSR Error")
        msg = "This isn't a valid CSR. If you are sure it is " + \
              "then contact support."
        return jsonify(status='ERROR', msg=msg)


@bp.route('/check_email')
def check_email():
    """Checks whether an email belongs to an account or not."""
    email = request.args.get("email")
    try:
        user = get_user(email)
        if user:
            return jsonify(status='SUCCESS', data='existing')
        else:
            return jsonify(status='SUCCESS', data='new')
    except:
        msg = "An error occured whilst trying to check if this email is " + \
            "associated with an existing user."

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)


@bp.route('/check_password')
def check_password():
    """Checks whether the submitted password is correct."""
    email = request.args.get("email")
    password = request.args.get("password")
    msg = None
    try:
        User.authenticate(email, password)
        msg = "An error occured whilst retrieving your details from stripe"
        return jsonify(
            status='SUCCESS', data={'user': 'correct'})
    except UserAuthenticationFailedError:
        return jsonify(
            status='SUCCESS', data={'user': 'incorrect'})
    except:
        if msg is None:
            msg = "An error occured whilst trying to check login credentials"

            msg += "\n\n" + sys.exc_info()[0]

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)


@bp.route('/get_cards')
def get_cards():
    msg = None
    try:
        user = get_current_user()
        if not user:
            email = request.args.get('email')
            password = request.args.get('password')
            user = User.authenticate(email, password)
        cards = []
        if user.stripe_id:
            customer = stripe.Customer.retrieve(user.stripe_id)
            for _card in customer.cards.data:
                card = {
                    "name": "**** **** **** " + _card.last4,
                    "id": _card.id
                }

                if _card.id == customer.default_card:
                    card['default'] = True
                cards.append(card)

        return jsonify(
            status='SUCCESS', data={'cards': cards})
    except:
        if msg is None:
            msg = "An error occured whilst retrieving your details from stripe"

            msg += "\n\n" + sys.exc_info()[0]

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)
