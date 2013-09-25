# -*- coding: utf-8 -*-
"""
    volcanicpixels.users.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class UserError(Exception):
    """Base User Error"""


class EmailError(UserError):
    def __init__(self, email):
        self.msg = "%s is not a valid email address" % email


class UserNotFoundError(UserError):
    """Raised when User.get() is called for a user that does not exist"""
    def __init__(self, email=None):
        if email is not None:
            self.msg = "The user with email %s does not exist" % email
        else:
            self.msg = "User does not exist"


class UserSuspended(UserError):
    """Raised when User.auth() is called on a suspended user."""
    def __init__(self, msg="This user has been suspended."):
        self.msg = msg


class UserAuthenticationFailedError(UserError):
    """Raised when incorrect password is supplied to User.auth() """
