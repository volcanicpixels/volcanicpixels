# -*- coding: utf-8 -*-
"""
    volcanicpixels.legacy
    ~~~~~~~~~~~~~~~~~~~~~

    Normalises legacy stuff (redirects to new endpoint)
"""
from flask.ext.volcano import route, create_app as _create_app
from raven_appengine import register_sentry
from flask import request, redirect
import logging
import urllib


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = _create_app(__name__, __path__, settings_override)

    register_sentry(app)

    logging.info(app.config)

    return app

app = create_app()


@app.route('/api/1/<method>/')
def redirect_api(method):
    new_url = "http://legacy.volcanicpixels.com"
    new_url += request.path

    new_url += '?' + urllib.urlencode(request.args)

    return redirect(new_url)
