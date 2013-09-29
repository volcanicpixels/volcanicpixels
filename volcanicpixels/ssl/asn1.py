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


def _isInt(x, onlyNonNegative=False):
    test = 0
    try:
        test += x
    except TypeError:
        return False
    return not onlyNonNegative or (x >= 0)


def b(s):
    return s


def bchr(s):
        return chr(s)


def bstr(s):
        return str(s)


def bord(s):
        return ord(s)


class BytesIO_EOF(BytesIO):
    """This class differs from BytesIO in that an EOFError exception is
    raised whenever EOF is reached."""

    def __init__(self, *params):
        BytesIO.__init__(self, *params)
        self.setRecord(False)

    def setRecord(self, record):
        self._record = record
        self._recording = b("")

    def read(self, length):
        s = BytesIO.read(self, length)
        if len(s) < length:
            raise EOFError
        if self._record:
            self._recording += s
        return s

    def read_byte(self):
        return self.read(1)[0]


class NoDerElementError(EOFError):
    pass


class DerObject(object):
    def __init__(self, asn1Id=None, payload=b(''), implicit=None,
                 constructed=False):

        if asn1Id is None:
            self._idOctet = None
            return
        asn1Id = self._convertTag(asn1Id)
        self._implicit = implicit
        if implicit:
            # In a BER/DER identifier octet:
            # * bits 4-0 contain the tag value
            # * bit 5 is set if the type is 'construted'
            #   and unset if 'primitive'
            # * bits 7-6 depend on the encoding class
            #
            # Class    | Bit 7, Bit 6
            # universal    |   0      0
            # application  |   0      1
            # context-spec |   1      0 (default for IMPLICIT)
            # private      |   1      1
            #
            self._idOctet = 0x80 | self._convertTag(implicit)
        else:
            self._idOctet = asn1Id
        if constructed:
            self._idOctet |= 0x20
        self.payload = payload

    def _convertTag(self, tag):
        """Check if *tag* is a real DER tag.
        Convert it from a character to number if necessary.
        """
        if not _isInt(tag):
            if len(tag) == 1:
                tag = bord(tag[0])
        # Ensure that tag is a low tag
        if not (_isInt(tag) and 0 <= tag < 0x1F):
            raise ValueError("Wrong DER tag")
        return tag

    def _lengthOctets(self):
        """Build length octets according to the current object's
        payload.

        Return a byte string that encodes the payload length (in
        bytes) in a format suitable for DER length octets (L).
        """
        payloadLen = len(self.payload)
        if payloadLen > 127:
            encoding = long_to_bytes(payloadLen)
            return bchr(len(encoding)+128) + encoding
        return bchr(payloadLen)

    def encode(self):
        """Return this DER element, fully encoded as a binary byte
        string."""
        # Concatenate identifier octets, length octets,
        # and contents octets
        return bchr(self._idOctet) + self._lengthOctets() + self.payload

    def _decodeLen(self, s):
        """Decode DER length octets from a file."""

        length = bord(s.read_byte())
        if length <= 127:
            return length
        payloadLength = bytes_to_long(s.read(length & 0x7F))
        # According to DER (but not BER) the long form is used
        # only when the length doesn't fit into 7 bits.
        if payloadLength <= 127:
            raise ValueError("Not a DER length tag (but still valid BER).")
        return payloadLength

    def decode(self, derEle):
        """Decode a complete DER element, and re-initializes this
        object with it.

        :Parameters:
          derEle : byte string
            A complete DER element.

        :Raise ValueError:
          In case of parsing errors.
        :Raise EOFError:
          If the DER element is too short.
        """

        s = BytesIO_EOF(derEle)
        self._decodeFromStream(s)
        # There shouldn't be other bytes left
        try:
            b = s.read_byte()
            raise ValueError("Unexpected extra data after the DER structure")
        except EOFError:
            pass

    def _decodeFromStream(self, s):
        """Decode a complete DER element from a file."""

        try:
            idOctet = bord(s.read_byte())
        except EOFError:
            raise NoDerElementError
        if self._idOctet is not None:
            if idOctet != self._idOctet:
                raise ValueError("Unexpected DER tag")
        else:
            self._idOctet = idOctet
        length = self._decodeLen(s)
        self.payload = s.read(length)


class DerBitString(DerObject):
    def __init__(self, value=b(''), implicit=None):
        """Initialize the DER object as a BIT STRING.

        :Parameters:
          value : byte string
            The initial, packed bit string.
            If not specified, the bit string is empty.
          implicit : integer
            The IMPLICIT tag to use for the encoded object.
            It overrides the universal tag for OCTET STRING (3).
        """
        DerObject.__init__(self, 0x03, b(''), implicit, False)
        self.value = value

    def encode(self):
        """Return the DER BIT STRING, fully encoded as a
        binary string."""

        # Add padding count byte
        self.payload = b('\x00') + self.value
        return DerObject.encode(self)

    def decode(self, derEle):
        """Decode a complete DER BIT STRING, and re-initializes this
        object with it.

        :Parameters:
            derEle : byte string
                A complete DER BIT STRING.

        :Raise ValueError:
            In case of parsing errors.
        :Raise EOFError:
            If the DER element is too short.
        """

        DerObject.decode(self, derEle)

    def _decodeFromStream(self, s):
        """Decode a complete DER BIT STRING DER from a file."""

        # Fill-up self.payload
        DerObject._decodeFromStream(self, s)

        if self.payload and bord(self.payload[0]) != 0:
            raise ValueError("Not a valid BIT STRING")

        # Fill-up self.value
        self.value = b('')
        # Remove padding count byte
        if self.payload:
            self.value = self.payload[1:]
