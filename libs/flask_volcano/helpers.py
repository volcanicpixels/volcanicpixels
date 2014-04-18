# -*- coding: utf-8 -*-
"""
    flask_volcano.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Daniel Chatfield
"""

import importlib
import logging
import pkgutil
import os
import sys
from urlparse import urljoin
from functools import wraps

from google.appengine.api.app_identity import get_application_id
from google.appengine.api import users

from flask import Blueprint, url_for, request, current_app, redirect
from werkzeug.routing import BuildError


def route(app, *args, **kwargs):

    def decorator(f):
        @app.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator


def register_blueprints(app, package_name, package_path):
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
                app.register_blueprint(item)
                logging.info("Registered `%s` blueprint onto `%s` app" %
                             (item.name, app.import_name))
            rv.append(item)
    return rv


def register_views(app, package_name, package_path=None):
    if package_path is None:
        package_path = find_package_path(package_name)

    for _, name, _ in pkgutil.iter_modules(package_path):
        # ignore private modules
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
    return (os.environ.get('SERVER_SOFTWARE', '').startswith('Development') or
            get_application_id().endswith('staging'))


def is_beta_server():
    return os.environ.get('CURRENT_VERSION_ID', '').startswith('beta')


def server_info():
    if is_dev_server():
        return "[DEV]"
    elif is_beta_server():
        return "[BETA]"
    return ""


def url_build_handler(error, endpoint, values):
    if endpoint.split('.')[-1] not in ['render', 'index']:
        for item in ['render', 'index']:
            try:
                return url_for(endpoint + '.' + item)
            except BuildError:
                continue


def make_external(url, root=None):
    if root is None:
        root = request.url_root
    return urljoin(root, url)


def canonical_url(url):
    return make_external(url, current_app.config.get('CANONICAL_URL_ROOT'))


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(401)  # Unauthorized
            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view
