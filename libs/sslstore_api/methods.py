# -*- coding: utf-8 -*-
"""
    sslstore_api.methods
    ~~~~~~~~~~~~~~~~~~~~

    Methods that use the current app for the sslstore_api Client instance.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from flask import current_app


def get_approver_emails(*args, **kwargs):
    return current_app.extensions['sslstore'].get_approver_emails(
        *args, **kwargs)
