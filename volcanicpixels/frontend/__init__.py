# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application module
"""

from functools import wraps

from .. import factory


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = factory.create_app(__name__, __path__, settings_override)

    return app


def create_blueprint(*args, **kwargs):
    return factory.create_blueprint(*args, **kwargs)


def route(bp, *args, **kwargs):

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator

app = create_app()
