# -*- coding: utf-8 -*-
"""
    volcanicpixels.helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""

import importlib
import logging
import pkgutil
import os
import sys

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

    logging.info(package_path)

    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        import_name = '%s.%s' % (package_name, name)
        m = importlib.import_module(import_name)
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                load_routes(import_name, m.__path__)
                app.register_blueprint(item)
                logging.info("Regisered `%s` blueprint onto `%s` app" %
                             (item.name, app.import_name))
            rv.append(item)
    return rv


def load_routes(package_name, package_path=None):
    """Loads all sub modules of a package"""

    logging.info(package_path)

    if package_path is None:
        package_path = find_package_path(package_name)

    for _, name, _ in pkgutil.iter_modules(package_path):
        if name[:1] != '_':
            importlib.import_module('%s.%s' % (package_name, name))


def find_package_path(import_name):
    """Attempts to work out the package path from the import name."""
    # Module already imported?
    mod = sys.modules.get(import_name)
    if mod is not None and hasattr(mod, '__path__'):
        return mod.__path__

    # Check the loader.
    loader = pkgutil.get_loader(import_name)

    if loader is None or import_name == '__main__':
        return os.getcwd()

    if hasattr(loader, 'get_filename'):
        filepath = loader.get_filename(import_name)
        return [os.path.dirname(os.path.abspath(filepath))]
    else:
        __import__(import_name)
        return sys.modules[import_name].__path__


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
