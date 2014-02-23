# -*- coding: utf-8 -*-
"""
    volcanicpixels.users
    ~~~~~~~~~~~~~~~~~~~~

    Normalizes API for different user providers (Google, internal etc.)
"""

import datetime

from flask import session

from .errors import UserNotFoundError, UserAuthenticationFailedError
from .models import User


def get_current_user():
    """Gets the currently logged in user or returns None"""
    user = session.get('user', None)
    try:
        user = User.get(user)
        return user
    except UserNotFoundError:
        return None


def get_user(uid):
    try:
        return User.get(uid)
    except UserNotFoundError:
        return None


def create_user(email, password, **kwargs):
    return User.create(email, password, **kwargs)


def authenticate_user(uid, password):
    """Authenticates a user with email and password

    Checks a users credentials and adds them to the session if they are
    correct. This function doesn't catch exceptions to allow the callee to
    be able to distinguish between a user not found and an incorrect password.
    """

    user = User.authenticate(uid, password)
    user.last_login = datetime.datetime.now()
    user.put()
    session['user'] = user.key.id()
    return user


def logout_user():
    session['user'] = None


def inject_user():
    return dict(user=get_current_user())
