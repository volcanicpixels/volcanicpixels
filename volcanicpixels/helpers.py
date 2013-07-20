# -*- coding: utf-8 -*-
"""
    volcanicpixels.helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""

import pkgutil
import importlib

from flask import Blueprint


def register_blueprints(app, package_name, package_path):
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


def should_start_sentry(app):
    """ Determines whether to initialize sentry for the given app. """
    return True
