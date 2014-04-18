# -*- coding: utf-8 -*-
"""
    volcanicpixels.settings
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels settings module
"""

from datetime import timedelta

DEBUG = True
TESTING = True

# This key should be overridden in secret_keys.py. In the future I will
# implement some clever encryption scheme so that the secret_keys can safely
# be added to github but until then you MUST NOT push code into production
# unless the secret_keys.py file is present otherwise you will invalidate all
# current sessions and new sessions will be signed with 'super-secret-key'
# which is neither super nor secret.

SESSION_COOKIE_NAME = "SESSION_AUTH"
PERMANENT_SESSION_LIFETIME = timedelta(days=31)
