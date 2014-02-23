# -*- coding: utf-8 -*-
"""
    volcanicpixels.users.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import re

from pbkdf2 import crypt

from .errors import EmailError


EMAIL_REGEX = re.compile('[^@]+@[^@]+\.[^@]+')


def validate_email(email):
    email = email.lower()
    if EMAIL_REGEX.match(email):
        return email
    else:
        raise EmailError(email)


def generate_hash(password, salt=None, iterations=None):
    return crypt(password, salt, iterations)


def check_hash(password, hash):
    """Validate a given password

    This function is used to check whether password matches the given hash.
    The salt and iteration count are stored as part of the hash as per the
    pbkdf2 spec.
    """
    return (crypt(password, hash) == hash)
