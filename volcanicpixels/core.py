# -*- coding: utf-8 -*-
"""
	volcanicpixels.core
	~~~~~~~~~~~~~~~~~~~
"""


from raven.contrib.flask import Sentry

from .secret_keys import SENTRY_DSN

sentry = Sentry(dsn=SENTRY_DSN)

class VolcanicPixelsException(Exception):
	""" Base application error class."""
	pass

