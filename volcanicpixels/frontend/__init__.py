# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application module
"""
from flask.ext.links import links
from flask.ext.markdown import markdown
from flask.ext.volcano import route, create_app as _create_app, canonical_url
from volcanicpixels.users import inject_user
from raven_appengine import register_sentry
from sslstore_api import flask_init
from .errors import register_error_handlers
import stripe
import logging


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = _create_app(__name__, __path__, settings_override)

    markdown(app)
    links(app)
    register_sentry(app)
    flask_init(app)

    logging.info(app.config)

    app.context_processor(inject_user)
    app.add_template_global(canonical_url)

    register_error_handlers(app)

    return app

app = create_app()
stripe_key = app.config.get('STRIPE_KEY')


if stripe_key:
    logging.info('Stripe configured')
    stripe.api_key = stripe_key
