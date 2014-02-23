# -*- coding: utf-8 -*-
"""
    flask_modular_template_loader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A jinja2 loader that loads templates arranged in a modular way.

    `template` will resolve to:
     - {template}
     - {template}index.html
     - {template}/index.html

    :copyright: (c) 2013 by Daniel Chatfield
"""

from jinja2 import ChoiceLoader

from jinja2_proxy_loader import (
    create_extension_proxy, LoaderMissingError, IOErrorProxyLoader)


def load_loader(app):
    return register_loader(app)


def register_loader(app):

    original_loader = app.jinja_loader
    loaders = []

    if original_loader is None:
        raise LoaderMissingError()

    loaders.append(IOErrorProxyLoader(original_loader))
    loaders.append(create_extension_proxy(original_loader, '.html'))
    loaders.append(create_extension_proxy(original_loader, 'index.html'))
    loaders.append(create_extension_proxy(original_loader, '/index.html'))

    app.jinja_loader = ChoiceLoader(loaders)
