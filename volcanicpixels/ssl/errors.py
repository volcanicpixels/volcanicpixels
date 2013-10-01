# -*- coding: utf-8 -*-
"""
    volcanicpixels.ssl.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The SSL Api.
"""


class UserNotProvidedError(Exception):
    pass


class CVCCheckFailedError(Exception):
    pass


class SSLCertificateNotFoundError(Exception):
    pass
