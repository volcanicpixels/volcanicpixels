# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl
    ~~~~~~~~~~~~~~~~~~

    The SSL Api.
"""
import stripe
from flask import session
from volcanicpixels.users import (
    get_current_user, get_user, authenticate_user, create_user,
    UserAuthenticationFailedError)
from .csr import CertificationRequest
from .helpers import get_keypair


def process_request(options):

    """
    Validate request info
    """

    credit_card = options.get('credit_card')

    def do_error(msg='An error occured'):
        raise Exception(msg)

    def is_token(value):
        """Determines whether the passed argument is a stripe token or not"""
        return (value[:3] == 'tok')

    """Normalize request

    At "END NORMALIZE" the user should be created and logged in, they
    should have a stripe id associated with them and if a token was passed
    as credit_card then it should be converted into a card object.

    TODO: update existing user if additional information is provided
    """

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

    if not user.stripe_id:
        # User doesn't have a stripe customer ID
        customer = stripe.Customer.create(
            description=name,
            email=email
        )

        user.stripe_id = customer.id
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

    """END NORMALIZE"""

    if 'csr' not in options:
        # We need to generate the CSR
        key = get_keypair(False)
        csr = CertificationRequest(keypair=key)

        # Set fields
        domain = options.get('domain')
        organization = options.get('organization')
        state = options.get('state')
        country = options.get('country')
        phone_number = options.get('phone_number')

        csr.set_subject_field('common_name', domain)
        csr.set_subject_field('organization', organization)
        csr.set_subject_field('state', state)
        csr.set_subject_field('country', country)
        csr.set_subject_field('telephone', phone_number)

    return 'test'
