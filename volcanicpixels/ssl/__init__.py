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
    key =  "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAuzx7DKpcgJln2Ou04vhaY/oCxtL+QdDKq1ayIGczRLkStHC7\nlyeCCbTBHoRCCwrsu//bFJ5bBc1Qa1XpDz5LOaw7QtTuAFwVLTDSd4VsOj3V6VMN\nHp/y+Ci08o5WU3I3UayTlLlCXwTJbHZ5uU0cX7yX7BirdDhbrHyzZDLDst1Zogkh\n9hImdacEDFJW5UCPj9Ue14S0e6gDlQDoNniReFKsO/9FYR/c9/YFncSopgY6RyCK\nQky06fUA0pSgtjX4s0gz9y2mbIXBByx0b38F2ORmhRI4RydalJN/GrQ9rIWNYohe\nRylPiSpdDnKB5AeVv/X6EltfcPu1geBn3qas5wIDAQABAoIBADE6aqPe2ulY7Cvl\ndS7D24gzwK0j5oPJcK/x4G2SlLE588gLZ9cLJS6GHsx2O6MJoUqgr6pRJF93JvDB\nqsA+QasNNJuSvmzLySmTj5KrOtRpU6fAFU/6//ftQ/4OHHZeLltEA51zxBaVfJwO\n3lwxAQfO3ybNKa8p7jiApO3wRvHsuzhCJkE7zLKYuKzqZ6RlOmB79oQwraTawAvR\n4G3IJkp/RpRVYetSn7PDEIZsMBbG3wvNBPdG35qqcdHLy3wzFsizvin47Eu3+rgv\ncnW4wFYiQ0o0bZ868VC0Bg6wdwieABmL+UpJdJEX2CZAXpFcHSLA7nk9YHeVsVCQ\nd66YJPECgYEA8DJlP4iA8QsvuUME0fWWYFU9xlzghetNWHm07P3kcrtW45NbEfr6\nJRNQx411ZIE1o1cjHUX30aclXUaOUQF9rCq152TOfWAoFhD3fc8zFxxOvFxET1/1\nAGW7eMHVTE5Cc4OI0JdElaW1/vW5GYsfunQjM5I95HiEWMtyLEWrlnkCgYEAx44T\nmeA3qrht0wAMqRI9I02SxQlW4jiS0HLR+PAoQfCHWUwCSTpuHahQnO7Ti3j3Elvl\nG75WAPeD7335yGOT3rbMaBdPc9u8KpSYI4V2OrtMS3gZm8Vb6fV55Q6X3xAwONrD\nT5xj2/KDbcyHtryOUkH44UzBxdXVFM0bA/FLBl8CgYEAwKV6xTkjSbDSJwGUlR0m\n7b6QXE9TmLU/hK2gqc98cXTF3KLsEQC9rgzO5i4TsHddYNNbi3f5qkIn2qbjMB9E\n/1gGKz+TycTcgc474cDUVj3S/In4E71/kEEH2nOEMr4119XwXnRkgq20yXelbNJD\nsVTCgvNRBrSOWXVa7h024OkCgYBZqSZ5btrUJAWEVnNZy84YfJRDX4zgG9crPUvG\nc/FCn1XQ82vbhxtOy/9cY5o9Al7QquVn778otA1dn9aJCOS5npx88GxMfCAxaY5p\n919FyD3hctbevHAt0JOyLTpjiRyBjxlOPdBIVNBklw8rNdEkeGvgnuI5h3gz3mwS\n+2lgNQKBgBu4dCXR6dE1I7l0XkvunFOZuzoxTxY86B1lOEWWQf3fDPddnofhVeQt\nNc9/pdjtYWev+AaGoxCBpg/352B7X6kNjjoXQfvmdkrrewV2hxct/yijukuCEr4Z\n3pcWYydL1O5hCHRmKefQnRxXgj9+RmT9O0G65jQhFfqDPkOO84Kh\n-----END RSA PRIVATE KEY-----"

    if encode:
        return key
    else:
        return RSA.importKey(key)

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
