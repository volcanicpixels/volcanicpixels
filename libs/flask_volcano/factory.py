# -*- coding: utf-8 -*-
"""
    flask_volcano.factory
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Daniel Chatfield
"""

from flask import Flask, Blueprint
from flask.ext.modular_template_loader import register_loader

from .helpers import register_blueprints, url_build_handler


def create_app(package_name, package_path, config=None, **kwargs):
    """Returns a :class:`Flask` application instance configured with common
    extensions.
    """

    default_kwargs = {
        'instance_relative_config': True,
        'template_folder': package_path[0]
    }

    # Merge the kwargs with the defaults
    kwargs = dict(default_kwargs.items() + kwargs.items())

    app = Flask(package_name, **kwargs)

    app.config.from_object('volcanicpixels.settings')
    app.config.from_object('volcanicpixels.secret_keys')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(config)

    app.url_build_error_handlers.append(url_build_handler)

    register_blueprints(app, package_name, package_path)
    register_loader(app)

    return app


def create_blueprint(name, import_name, *args, **kwargs):
    return Blueprint(name, import_name, *args, **kwargs)
