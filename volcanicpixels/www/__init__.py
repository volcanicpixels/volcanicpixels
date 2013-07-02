# -*- coding: utf-8 -*-
"""
    volcanicpixels.www
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application package
"""

from functools import wraps

from .. import factory

def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = factory.create_app(__name__, __path__, settings_override)

    return app


def route(bp, *args, **kwargs):

	def decorator(f):
		@bp.route(*args, **kwargs)
		@wraps(f)
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs)
		return f

	return decorator

