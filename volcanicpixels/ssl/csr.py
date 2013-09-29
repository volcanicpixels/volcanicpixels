# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.csr
    ~~~~~~~~~~~~~~~~~~~~~~
"""
from base64 import b64encode
import binascii
import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher.PKCS1_v1_5 import PKCS115_Cipher
from pyasn1.codec.der import encoder, decoder
from pyasn1.type import univ, char
from .asn1 import (
    CertificationRequest as _CertificationRequest, CertificationRequestInfo,
    Name, Attributes2, Attributes, Attribute, AttributeType, AttributeValue,
    SubjectPublicKeyInfo, AlgorithmIdentifier, DigestInfo)
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
    request.set_subject_field('country', 'GB')
    request.set_subject_field('state', 'England')
    request.set_subject_field('locality', 'Ringwood')
    request.set_subject_field('organization', 'Platinum Mirror LTD')
    request.set_subject_field('organizational_unit', 'Digital Security')
    request.set_subject_field('common_name', 'www.volcanicpixels.com')
    request.set_subject_field('email', 'business@platinummirror.com')
    keypair = get_keypair(False)
    request.set_keypair(keypair)
    return request.encode()


class SubjectField():
    type = 'PrintableString'
    def __init__(self, value):
        self.value = value

    def get_attribute_value(self):
        return self.value

    def get_attribute(self):
        attribute = Attribute()
        attribute_type = AttributeType(self.identifier)
        attribute.setComponentByName('type', attribute_type)
        attribute_value = AttributeValue()
        value = self.get_attribute_value()
        attribute_value.setComponentByName(self.type, value)
        attribute.setComponentByName('value', attribute_value)
        return attribute

    def get_asn1(self):
        attributes = Attributes()
        attribute = self.get_attribute()
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
    type = 'IA5String'

class UnstructuredName(SubjectField):
    identifier = '1.2.840.113549.1.9.2'
    type = 'Set'

    def get_attribute_value(self):
        value = univ.Set()
        name = char.PrintableString(self.value)
        value.setComponentByPosition(0, name)
        return value


class CertificationRequest():
    version = 0

    def __init__(self, keypair=None, subject_fields=None, attributes=None):
        self.subject_fields = []
        self.attributes = {}
        self.keypair = None
        self.unstructuredName = None

        if subject_fields:
            self.set_subject_fields(subject_fields)

        if keypair:
            self.set_keypair(keypair)

    def set_keypair(self, keypair):
        """Keypair must already by an _rsaobj (i.e. been through importKey)"""
        self.keypair = keypair
        self.cipher = PKCS115_Cipher(self.keypair)

    def set_subject_fields(self, fields):
        for (field, value) in fields:
            self.set_subject_field(field, value)

    def set_subject_field(self, field, value):
        def set_field(cls):
            self.subject_fields.append(cls(value))

        if field == 'common_name':
            return set_field(CommonNameSubjectField)

        if field == 'country':
            return set_field(CountrySubjectField)

        if field == 'name':
            return set_field(NameSubjectField)

        if field == 'email':
            return set_field(EmailSubjectField)

        if field == 'organization':
            self.unstructuredName = value
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
        for field in self.subject_fields:
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

        attributes = Attributes2()
        if self.unstructuredName is not None:
            name = UnstructuredName(self.unstructuredName).get_attribute()
            attributes.setComponentByPosition(0, name)
        request_info.setComponentByName('attributes', attributes)

        return request_info

    def get_subject_publickey_info_asn1(self):
        publickey_info = SubjectPublicKeyInfo()

        algorithm_identifier = AlgorithmIdentifier()
        algorithm_identifier.setComponentByName(
            'algorithm', '1.2.840.113549.1.1.1')
        algorithm_identifier.setComponentByName('parameters', univ.Null())
        publickey_info.setComponentByName('algorithm', algorithm_identifier)

        if not self.keypair:
            raise KeyMissingError("No Key Provided")

        publickey = self.keypair.publickey()

        binary = publickey.exportKey('DER')
        tmp = decoder.decode(binary)

        publickey_info.setComponentByName('subjectPublicKey', tmp[0][1])
        return publickey_info

    def get_signature_algorithm_asn1(self):
        algorithm = AlgorithmIdentifier()
        algorithm.setComponentByName('algorithm', SHA1_CHECKSUM_WITH_RSA)
        algorithm.setComponentByName('parameters', univ.Null())
        return algorithm


    def get_signature(self, request_info, bits=2048):
        # See ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-1/pkcs-1v2-1.pdf (9.2)
        def hex2bin(hexdata):
            return bin(int(hexdata, 16))[2:].zfill(len(hexdata)*4)

        def tobits(s):
            result = "'"
            rv = []
            for c in s:
                bits = bin(ord(c))[2:]
                bits = '00000000'[len(bits):] + bits
                rv.extend([int(b) for b in bits])
            for bit in rv:
                result += str(bit)

            result += "'B"
            return result

        import logging
        digest = encoder.encode(request_info)
        data = digest
        digest_info = DigestInfo()
        algorithm = AlgorithmIdentifier()
        algorithm.setComponentByName('algorithm', '1.3.14.3.2.26')
        algorithm.setComponentByName('parameters', univ.Null())
        digest_info.setComponentByName('digestAlgorithm', algorithm)
        checksum = hashlib.sha1(data).digest()
        digest = univ.OctetString(checksum)
        logging.error(digest.prettyPrint())
        digest_info.setComponentByName('digest', digest)
        data = encoder.encode(digest_info)


        test = binascii.hexlify(data)
        binary_data = hex2bin(test)

        logging.error(len(binary_data))
        bits = bits - len(binary_data)
        bits = bits - 8 * 3
        pad_length = bits / 8
        
        padding = "0b" + "00000000" + "00000001" + "11111111" * pad_length
        padding = padding + "00000000"
        _data = padding + binary_data

        #data = long(_data, 0)
        #data = _data

        """
        data_ = bytes_to_long(data)
        data_ = bin(long)
        t_len = len(data)
        em_len = t_len + 11
        pad = em_len - t_len - 3
        # Now we need to pad it
        pre = "0x01" + "1" * pad + "0"
        data_ = univ.OctetString(pre + data_.prettyPrint()[2:])
        logging.error(pre)
        logging.error(data_.prettyPrint())
        data = pre + data
        """

        signature = self.cipher.encrypt(data)

        
        return tobits(signature)


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
        footer = "\n-----END CERTIFICATE REQUEST-----"
        asn1 = self.get_asn1()
        encoded = encoder.encode(asn1)
        encoded = b64encode(encoded)
        lines = []
        for i in xrange(0, len(encoded), 64):
            lines.append(encoded[i:i+64])
        encoded = '\n'.join(lines)
        encoded = header + encoded + footer
        return encoded






class KeyMissingError(Exception):
    pass
