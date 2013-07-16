# -*- coding: utf-8 -*-
"""
    volcanicpixels.settings
    ~~~~~~~~~~~~~~~

    Volcanic Pixels settings module
"""

try:
	from .secret_keys import SENTRY_DSN
except ImportError:
	pass


DEBUG = True
SECRET_KEY = 'super-secret-key'