# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from google.appengine.ext import ndb
from google.appengine.ext import deferred
from Crypto.PublicKey import RSA
from .models import KeyPair


def is_academic(email):
    if email is None:
        return False
    import logging
    logging.info(email[-9:])
    return email[-6:] == ".ac.uk" or email[-4:] == ".edu"


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
