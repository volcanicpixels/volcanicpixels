# -*- coding: utf-8 -*-
"""
    volcanicpixels.dev_keys
    ~~~~~~~~~~~~~~~

"""

from flask.ext.volcano import is_dev_server


if not is_dev_server():
    raise Exception("dev_keys.py cannot be used in production")

SECRET_KEY = "NOTSOSECRETDEVKEY"

CANONICAL_URL_ROOT = "https://www.volcanicpixels.com"

SSLSTORE_SANDBOX = True
SSLSTORE_PARTNER_CODE = '82912397'
SSLSTORE_AUTH_TOKEN = '25B1889E4E52AE9DF42DCDEDC4F7A9CB'

STRIPE_KEY = "sk_test_RggHJuTyiebN6DiJdgE826q8"
STRIPE_PUB_KEY = "pk_test_NgVxcRzPcljLftdwhuJAMMpX"
