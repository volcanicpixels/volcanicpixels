# -*- coding: utf-8 -*-
"""
    volcanicpixels.helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""

import importlib
import logging
import pkgutil
import os

from flask import Blueprint
from raven.contrib.flask import Sentry
from raven_appengine import register_transport


def load_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask
    application found in all child modules for the specified package.

    :param app: the Flask application
    :param package_name:
    :param package_path:

    """

    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


def is_dev_server():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


def should_start_sentry(app):
    """Determines whether to initialize sentry for the given app."""
    if is_dev_server():
        return False
    else:
        return True


def load_sentry(app, dsn=None):
    """Loads `sentry` onto the given flask app."""
    try:
        register_transport()
        Sentry(app=app, dsn=dsn)
    except:
        logging.exception("Failed to load sentry")
    return app
