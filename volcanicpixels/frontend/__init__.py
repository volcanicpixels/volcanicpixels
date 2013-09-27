# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application module
"""
from flask.ext.links import links
from flask.ext.markdown import markdown
from flask.ext.volcano import route, create_app as _create_app
from sslstore_api import flask_init
import stripe


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = _create_app(__name__, __path__, settings_override)

    markdown(app)
    links(app)
    flask_init(app)

    return app

app = create_app()
stripe_key = app.config.get('STRIPE_KEY')

if stripe_key:
    stripe.stripe_key = stripe_key
