# -*- coding: utf-8 -*-
"""
    volcanicpixels.factory
    ~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import Flask

from .core import sentry
from .helpers import register_blueprints, should_start_sentry


def create_app(package_name, package_path, settings_override=None):
    """Returns a :class:`Flask` application instance configured with
    common extensions.

    :param package_name: application package name
    :param package_path:
    :param settings_override:

    """

    app = Flask(package_name, instance_relative_config=True)

    if should_start_sentry(app):
        sentry.init_app(app)

    app.config.from_object('volcanicpixels.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)

    return app
