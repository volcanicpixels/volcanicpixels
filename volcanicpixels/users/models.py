# -*- coding: utf-8 -*-
"""
    volcanicpixels.users.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from google.appengine.ext import ndb

from .errors import (
    EmailError, UserAuthenticationFailedError, UserNotFoundError)
from .helpers import validate_email, generate_hash, check_hash


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty(
        validator=lambda prop, email: validate_email(email))
    password = ndb.StringProperty(indexed=False)
    account_created = ndb.DateTimeProperty(auto_now_add=True)
    last_login = ndb.DateTimeProperty()
    stripe_id = ndb.StringProperty()

    @classmethod
    def get(cls, uid):
        if uid is None:
            raise UserNotFoundError()
        # First try and get a user by key (this is faster)
        user = ndb.Key("User", uid).get()
        if user:
            return user

        # Now try and match user email address. If they have changed
        # their email or are using a legacy oauth account then this is
        # needed.
        try:
            email = validate_email(uid)
        except EmailError:
            raise UserNotFoundError(uid)

        user = cls.query(cls.email == email).get()

        if user:
            return user
        else:
            raise UserNotFoundError(email)

    @classmethod
    def create(cls, email, password, **kwargs):
        """Creates a user

        Method for easily creating a user with a name, email and password.
        If not using this method then password hashing must be implemented.

        This does not put the new user.
        """
        password = generate_hash(password)
        return cls(email=email, password=password, **kwargs)

    @classmethod
    def authenticate(cls, uid, password):
        """Authenticates a user, if the credentials are correct it returns the
        user, otherwise raises an exception.
        """
        user = cls.get_user(uid)
        if user.verify_password(password):
            return user
        else:
            raise UserAuthenticationFailedError()

    def verify_password(self, password):
        """Checks whether the specified password matches this user."""

        # Some users may not have a password (third party oauth accounts) so
        # we need to make sure someone isn't trying to hyjack one of these
        # accounts by entering an empty password
        if self.password is None:
            return False
        return check_hash(password, self.password)

    def index_user(self):
        """
        Adds the current user to the volcanicpixels.search index.
        """
        pass
