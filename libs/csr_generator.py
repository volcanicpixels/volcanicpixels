# -*- coding: utf-8 -*-
"""
    csr_generator
    ~~~~~~~~~~~~~

    A pure python module for generating SSL certificate signing requests.

    A certification request consists of a distinguished name (the domain to
    sign), a public key, and an optional set of attributes (although most
    certification authorities require at least some of the attributes).

    This module has been written to conform to the spec at:
    http://tools.ietf.org/html/rfc2986

    :copyright: (c) 2013 by Daniel Chatfield.
    :license: MIT, see LICENSE for more details.
"""

from Crypto.PublicKey import RSA

def generate_pkey(bits=2048):
    key = RSA.generate(2048)
    return RSA.exportKey('PEM')


def generate_csr(pkey, digest="md5", **fields):
    """Create a certificate signing request

    Arguments: pkey     - The private key to associate with this request
               digest   - Digestion method to use for signing, default is md5
               **fields - The fields to add the the request. Possible 
                          arguments are:
                            country
                            state
                            locality
                            org
                            org_unit
                            common_name
                            email_address


    """
