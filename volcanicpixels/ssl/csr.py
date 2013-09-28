# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.csr
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import logging
from base64 import encodestring
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from Crypto.Util.number import long_to_bytes
from pyasn1.codec.der import encoder, decoder
from pyasn1.codec.ber import encoder as ber_encoder
from .asn1 import (
    CertificationRequest as _CertificationRequest, CertificationRequestInfo,
    Name, Attributes, Attribute, AttributeType, AttributeValue,
    SubjectPublicKeyInfo, AlgorithmIdentifier, DerBitString, bchr)
from . import get_keypair

"""
Define the ObjectIdentifier constants
"""

SHA1_CHECKSUM_WITH_RSA = "1.2.840.113549.1.1.5"


def generate_csr(pkey, domain, **fields):
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
                            email_address
    """


def test_csr():
    request = CertificationRequest()
    request.set_subject_field('common_name', 'www.volcanicpixels.com')
    request.set_subject_field('country', 'GB')
    request.set_subject_field('state', 'England')
    request.set_subject_field('locality', 'Ringwood')
    request.set_subject_field('organization', 'Platinum Mirror LTD')
    request.set_subject_field('organizational_unit', 'Digital Security')
    keypair = get_keypair(False)
    request.set_keypair(keypair)
    return request.encode()


class SubjectField():
    def __init__(self, value):
        self.value = value

    def get_asn1(self):
        attributes = Attributes()
        attribute = Attribute()
        attribute_type = AttributeType(self.identifier)
        attribute.setComponentByName('type', attribute_type)
        attribute_value = AttributeValue(self.value)
        attribute.setComponentByName('value', attribute_value)
        attributes.setComponentByPosition(0, attribute)
        return attributes


class CommonNameSubjectField(SubjectField):
    identifier = '2.5.4.3'


class CountrySubjectField(SubjectField):
    identifier = '2.5.4.6'


class NameSubjectField(SubjectField):
    identifier = '2.5.4.41'


class OrganizationSubjectField(SubjectField):
    identifier = '2.5.4.10'


class OrganizationalUnitSubjectField(SubjectField):
    identifier = '2.5.4.11'


class TelephoneSubjectField(SubjectField):
    identifier = '2.5.4.20'


class StreetAddressSubjectField(SubjectField):
    identifier = '2.5.4.9'


class LocalitySubjectField(SubjectField):
    identifier = '2.5.4.7'

class StateSubjectField(SubjectField):
    identifier = '2.5.4.8'


class EmailSubjectField(SubjectField):
    identifier = '1.2.840.113549.1.9.1'


class CertificationRequest():
    version = 0

    def __init__(self, keypair=None, subject_fields=None, attributes=None):
        self.subject_fields = {}
        self.attributes = {}
        self.keypair = None

        if subject_fields:
            self.set_subject_fields(subject_fields)

        if keypair:
            self.set_keypair(keypair)

    def set_keypair(self, keypair):
        """Keypair must already by an _rsaobj (i.e. been through importKey)"""
        self.keypair = keypair

    def set_subject_fields(self, fields):
        for (field, value) in fields:
            self.set_subject_field(field, value)

    def set_subject_field(self, field, value):
        def set_field(cls):
            self.subject_fields[field] = cls(value)

        if field == 'common_name':
            return set_field(CommonNameSubjectField)

        if field == 'country':
            return set_field(CountrySubjectField)

        if field == 'name':
            return set_field(NameSubjectField)

        if field == 'email':
            return set_field(EmailSubjectField)

        if field == 'organization':
            return set_field(OrganizationSubjectField)

        if field == 'organizational_unit':
            return set_field(OrganizationalUnitSubjectField)

        if field == 'state':
            return set_field(StateSubjectField)

        if field == 'telephone':
            return set_field(TelephoneSubjectField)

        if field == 'street_address':
            return set_field(StreetAddressSubjectField)

        if field == 'locality':
            return set_field(LocalitySubjectField)

        raise NotImplementedError("The %s field is not implemented" % field)

    def get_subject_asn1(self):


        subject = Name()
        i = 0
        for field in self.subject_fields.itervalues():
            subject.setComponentByPosition(i, field.get_asn1())
            i += 1
        return subject

    def get_certification_request_info_asn1(self):
        request_info = CertificationRequestInfo()
        request_info.setComponentByName('version', 0)

        subject = self.get_subject_asn1()
        request_info.setComponentByName('subject', subject)

        subject_pk_info = self.get_subject_publickey_info_asn1()
        request_info.setComponentByName('subjectPKInfo', subject_pk_info)

        return request_info

    def get_subject_publickey_info_asn1(self):
        publickey_info = SubjectPublicKeyInfo()

        algorithm_identifier = AlgorithmIdentifier()
        algorithm_identifier.setComponentByName(
            'algorithm', '1.2.840.113549.1.1.1')
        publickey_info.setComponentByName('algorithm', algorithm_identifier)

        if not self.keypair:
            raise KeyMissingError("No Key Provided")

        publickey = self.keypair.publickey()
        binary = DerBitString(
            DerSequence([publickey.n, publickey.e]).encode()
        ).encode()

        binary = publickey.exportKey('DER')
        tmp = decoder.decode(binary)

        publickey_info.setComponentByName('subjectPublicKey', tmp[0][1])
        return publickey_info

    def get_signature_algorithm_asn1(self):
        algorithm = AlgorithmIdentifier()
        algorithm.setComponentByName('algorithm', SHA1_CHECKSUM_WITH_RSA)
        return algorithm


    def get_signature(self, request_info):
        data = encoder.encode(request_info)
        checksum = hashlib.sha1(data).digest()
        return "'" + "{0:b}".format(self.keypair.sign(checksum, 1)[0]) + "'B"


    def get_asn1(self):
        """Get's the ASN1 object for the certifcation request"""
        request = _CertificationRequest()

        request_info = self.get_certification_request_info_asn1()
        request.setComponentByName('certificationRequestInfo', request_info)

        signature_algorithm = self.get_signature_algorithm_asn1()
        request.setComponentByName('signatureAlgorithm', signature_algorithm)

        signature = self.get_signature(request_info)
        request.setComponentByName('signature', signature)

        return request

    def encode(self):
        header = "-----BEGIN CERTIFICATE REQUEST-----\n"
        footer = "-----END CERTIFICATE REQUEST-----"
        asn1 = self.get_asn1()
        encoded = encoder.encode(asn1)
        encoded = encodestring(encoded)
        encoded = header + encoded + footer
        return encoded






class KeyMissingError(Exception):
    pass
