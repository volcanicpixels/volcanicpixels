# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl
    ~~~~~~~~~~~~~~~~~~

    The SSL Api.
"""
from google.appengine.ext import ndb
from google.appengine.ext import deferred
import stripe
from Crypto.PublicKey import RSA
from flask import session
from volcanicpixels.users import (
    get_current_user, get_user, authenticate_user, create_user,
    UserAuthenticationFailedError)
from .models import KeyPair


def generate_keypair(bits=2048):
    """Generates a public/private key pair"""
    return RSA.generate(2048)


def make_keypair():
    """Generates and adds a new pkey to the datastore"""

    ancestor = ndb.Key("KeyStore", "CSR_BUFFER")

    keypair = generate_keypair().exportKey('PEM')
    keypair = KeyPair(parent=ancestor, bits=2048, keypair=keypair)
    keypair.put()


@ndb.transactional
def get_keypair(encode=True):
    """Returns a key pair from the datastore or generates one if the store is
    empty.
    """

    # Use deferred to add a new key
    deferred.defer(make_keypair)

    ancestor = ndb.Key("KeyStore", "CSR_BUFFER")

    key = KeyPair.query(KeyPair.bits == 2048, ancestor=ancestor).get()

    if key:
        keypair = key.keypair
        key.key.delete()
        if encode:
            return keypair
        else:
            return RSA.importKey(keypair)
    else:
        # key store is empty, let's add a few more keys

        deferred.defer(make_keypair)
        deferred.defer(make_keypair)
        deferred.defer(make_keypair)
        deferred.defer(make_keypair)
        deferred.defer(make_keypair)

        if encode:
            return generate_keypair().exportKey('PEM')
        else:
            return generate_keypair()


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
            session['user'] = user.id()

    if not user.stripe_id:
        # User doesn't have a stripe customer ID
        customer = stripe.Customers.create(
            name=name,
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
        key = get_keypair()
