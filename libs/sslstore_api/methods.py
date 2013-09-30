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


def check_csr(*args, **kwargs):
    return current_app.extensions['sslstore'].check_csr(*args, **kwargs)


def create_dv_ssl_order(*args, **kwargs):
    return current_app.extensions['sslstore'].create_dv_ssl_order(
        *args, **kwargs)


def get_order_status(*args, **kwargs):
    return current_app.extensions['sslstore'].get_order_status(
        *args, **kwargs)


def get_certificates(*args, **kwargs):
    return current_app.extensions['sslstore'].get_certificates(
        *args, **kwargs)


def resend_email(*args, **kwargs):
    return current_app.extensions['sslstore'].resend_email(
        *args, **kwargs)
