# -*- coding: utf-8 -*-
"""
    sslstore_api
    ~~~~~~~~~~~~

    A python module for interacting with the sslstore API.

    TODO:
     - implement response caching to database
     - implement health check and automatic 5 minute request block after 2
       failed health checks

    :copyright: (c) 2013 by Daniel Chatfield
"""

from .client import Client


def flask_init(app):
    partner_code = app.config.get('SSLSTORE_PARTNER_CODE')
    auth_token = app.config.get('SSLSTORE_AUTH_TOKEN')
    sandbox = app.config.get('SSLSTORE_SANDBOX', True)
    app.extensions['sslstore'] = Client(partner_code, auth_token, sandbox)
