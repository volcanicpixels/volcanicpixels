# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from google.appengine.ext import ndb
from Crypto.PublicKey import RSA
from .errors import SSLCertificateNotFoundError


class SSLCertificate(ndb.Model):
    csr = ndb.TextProperty(required=True)
    keypair = ndb.TextProperty()
    domain = ndb.StringProperty()
    status = ndb.StringProperty()
    provider = ndb.StringProperty(indexed=False)
    cert_type = ndb.StringProperty(indexed=False)
    vendor_id = ndb.StringProperty()
    order_id = ndb.StringProperty()
    charge_id = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get(cls, order_id, user=None):
        if order_id is None:
            raise SSLCertificateNotFoundError()

        if user:
            cert = cls.query(
                cls.order_id == order_id, ancestor=user.key).get()
        else:
            cert = cls.query(cls.order_id == order_id).get()

        if cert:
            return cert
        else:
            raise SSLCertificateNotFoundError()

    @classmethod
    def create(cls, csr, **kwargs):
        """Creates a certificate object

        - Normalizes csr (exports it if object passed)
        - Normalizes keypair (exports it if object passed)
        """
        if hasattr(csr, 'export'):
            csr = csr.export()

        if 'keypair' in kwargs:
            if hasattr(kwargs['keypair'], 'export'):
                kwargs['keypair'] = kwargs['keypair'].export()
            if hasattr(kwargs['keypair'], 'exportKey'):
                kwargs['keypair'] = kwargs['keypair'].exportKey()

        return cls(csr=csr, **kwargs)


class KeyPair(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    bits = ndb.IntegerProperty(required=True)
    keypair = ndb.TextProperty(required=True)

    def publickey(self):
        return RSA.importKey(self.keypair).publickey()

    def export(self):
        return self.keypair
