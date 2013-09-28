# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from google.appengine.ext import ndb
from Crypto.PublicKey import RSA


class SSLCertificate(ndb.Model):
    pass


class KeyPair(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    bits = ndb.IntegerProperty(required=True)
    keypair = ndb.TextProperty(required=True)

    def publickey(self):
        return RSA.importKey(self.keypair).publickey()
