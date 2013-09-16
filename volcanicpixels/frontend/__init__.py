# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend
    ~~~~~~~~~~~~~~~~~~~~~~~

    Volcanic Pixels frontend application module
"""
from flask.ext.links import links
from flask.ext.markdown import markdown
from flask.ext.volcano import route, create_app as _create_app


def create_app(settings_override=None):
    """ Returns the Volcanic Pixels Flask application. """

    app = _create_app(__name__, __path__, settings_override)

    markdown(app)
    links(app)

    return app

app = create_app()
