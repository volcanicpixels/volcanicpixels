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


class NonAcademicEmailError(Exception):
    pass


class DomainCouponMismatchError(Exception):
    def __init__(self, coupon, domain):
        self.message = "%s entered, but coupon only valid for %s" \
            % (coupon, domain)
