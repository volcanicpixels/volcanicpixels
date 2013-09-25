# -*- coding: utf-8 -*-
"""
    volcanicpixels.users.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import re

from pbkdf2 import crypt
from flask import session

from .errors import EmailError, UserNotFoundError
from .models import User


EMAIL_REGEX = re.compile('[^@]+@[^@]+\.[^@]+')


def get_current_user():
    """Gets the currently logged in user or returns None"""
    user = session['user']
    try:
        user = User.get(user)
        return user
    except UserNotFoundError:
        return None


def authenticate_user(uid, password):
    """Authenticates a user with email and password

    Checks a users credentials and adds them to the session if they are
    correct. This function doesn't catch exceptions to allow the callee to
    be able to distinguish between a user not found and an incorrect password.
    """

    user = User.authenticate(uid, password)
    session['user'] = user.id()


def validate_email(prop, value):
    value = value.lower()
    if EMAIL_REGEX.match(value):
        raise EmailError(value)
    else:
        return value


def generate_hash(password, salt=None, iterations=None):
    return crypt(password, salt, iterations)


def check_hash(password, hash):
    """Validate a given password

    This function is used to check whether password matches the given hash.
    The salt and iteration count are stored as part of the hash as per the
    pbkdf2 spec.
    """
    return (crypt(password, hash) == hash)
