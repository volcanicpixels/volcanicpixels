# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.asn
    ~~~~~~~~~~~~~~~~~~~~~~

    EVERY OTHER WEBSITE JUST USES OPENSSL, BUT WE CAN'T BECAUSE GOOGLE DOESN'T
    LIKE C MODULES.

    MY LIFE FOR THE PAST FEW DAYS HAS CONSISTED OF:

    HOW THE FUCK DO I MAKE A CERTIFICATE SIGNING REQUEST?
        (FINDS A SPEC)
    WTF IS ASN.1? (FROM INTRODUCTION PART OF CSR SPEC)
        (FINDS AND READS THE STUPIDLY LONG ASN SPEC)
    GOES BACK TO READING CSR SPEC
    ALSO READS (AS THEY ARE REQUIRED):
    - X509 SPEC
    - X501 SPEC
    ALMOST COMMIT SUICIDE (IF I HADN'T ALREADY DEVELOPED A PRETTY INTERFACE
        I WOULD PROBABLY KNOCK THE PROJECT ON THE HEAD NOW)
    STARTS IMPLEMENTING THE SPEC IN PYTHON
"""
from pyasn1.type import namedtype, univ, tag, char
from Crypto.Util.number import long_to_bytes, bytes_to_long
from StringIO import StringIO as BytesIO



class AlgorithmIdentifier(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', univ.ObjectIdentifier()),
        namedtype.OptionalNamedType('parameters', univ.Any())
    )


class DigestInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('digestAlgorithm', AlgorithmIdentifier()),
        namedtype.NamedType('digest', univ.OctetString())
    )


class AttributeType(univ.ObjectIdentifier):
    pass


class AttributeValue(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('IA5String', char.IA5String()),
        namedtype.NamedType('UTF8String', char.UTF8String()),
        namedtype.NamedType('PrintableString', char.PrintableString()),
        namedtype.NamedType('Set', univ.Set())
    )


class Attribute(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('type', AttributeType()),
        namedtype.NamedType('value', AttributeValue())
    )


class Attributes(univ.Set):
    componentType = Attribute()


class Attributes2(Attributes):
    tagSet = Attributes.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
    )


class Name(univ.SequenceOf):
    componentType = Attributes()


class SubjectPublicKeyInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', AlgorithmIdentifier()),
        namedtype.NamedType('subjectPublicKey', univ.BitString())
    )


class CertificationRequestInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer()),
        namedtype.NamedType('subject', Name()),
        namedtype.NamedType('subjectPKInfo', SubjectPublicKeyInfo()),
        namedtype.NamedType('attributes', Attributes2())
    )


class CertificationRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('certificationRequestInfo',
                            CertificationRequestInfo()),
        namedtype.NamedType('signatureAlgorithm', AlgorithmIdentifier()),
        namedtype.NamedType('signature', univ.BitString())
    )
