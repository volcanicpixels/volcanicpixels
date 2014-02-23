# -*- coding: utf-8 -*-
"""
    volcanicpixels.legacy
    ~~~~~~~~~~~~~~~~~~~~~

    Normalises legacy stuff (redirects to new endpoint)
"""
from flask.ext.volcano import create_app as _create_app
from flask import request, redirect
import logging


def fix_unicode(text):
    text = text.decode("utf-8")

    text = text.replace(u"\xa0", u" ")
    text = text.encode("utf-8")

    return text


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = _create_app(__name__, __path__, settings_override)

    logging.info(app.config)

    return app

app = create_app()


@app.route('/api/1/<method>/')
def redirect_api(method):
    new_url = "http://legacy.volcanicpixels.com"
    new_url += request.path
    new_url += '?'
    for arg in request.args:
        new_url += arg + "=" + request.args[arg] + "&"

    return redirect(new_url[:-1])
