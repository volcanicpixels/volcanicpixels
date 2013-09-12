# -*- coding: utf-8 -*-
"""
    volcanicpixels.factory
    ~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import Flask, Blueprint
from flask.ext.modular_template_loader import load_loader

from .helpers import load_blueprints, should_start_sentry, load_sentry


def create_app(package_name, package_path, config=None, **kwargs):
    """Returns a :class:`Flask` application instance configured with
    common extensions.
    """

    default_kwargs = {
        'instance_relative_config': True,
        'template_folder': package_path[0]
    }

    # Merge the kwargs with the defaults
    kwargs = dict(default_kwargs.items() + kwargs.items())

    app = Flask(package_name, **kwargs)

    app.config.from_object('volcanicpixels.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(config)

    load_blueprints(app, package_name, package_path)

    if should_start_sentry(app):
        load_sentry(app)

    load_loader(app)

    return app


def create_blueprint(*args, **kwargs):
    return Blueprint(*args, **kwargs)
