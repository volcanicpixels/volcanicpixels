# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application module
"""

from functools import wraps

from flask.ext.markdown import markdown
from flask.ext.links import links, register_link

from .. import factory
from ..factory import create_blueprint


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = factory.create_app(__name__, __path__, settings_override)

    markdown(app)
    links(app)

    return app


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator

app = create_app()
