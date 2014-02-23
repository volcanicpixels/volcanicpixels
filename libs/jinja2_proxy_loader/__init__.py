# -*- coding: utf-8 -*-
"""
    jinja2_proxy_loader
    ~~~~~~~~~~~~~~~~~~~

    A jinja2 loader that transforms template names.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from jinja2 import BaseLoader, TemplateNotFound


def create_extension_proxy(loader, extension):
    """Creates a proxy loader that adds the given extensionto the template
    name.
    """
    return ExtensionProxyLoader(loader, extension)


class ProxyLoader(BaseLoader):
    def __init__(self, loader):
        self.loader = loader

    def get_source(self, environment, template):
        return self.loader.get_source(environment, template)

    def load(self, environment, name, globals=None):
        return self.loader.load(environment, name, globals)

    def list_templates(self):
        return self.loader.list_templates()


class ExtensionProxyLoader(ProxyLoader):
    """Jinja loader that adds the specified extension on to template names."""

    def __init__(self, loader, extension=".html"):
        super(ExtensionProxyLoader, self).__init__(loader)
        self.extension = extension

    def get_source(self, environment, template):
        return self.loader.get_source(environment, template + self.extension)


class IOErrorProxyLoader(ProxyLoader):
    """A proxy loader that catches IOError exceptions and raises a
    `TemplateNotFound` exception.
    """

    def get_source(self, environment, template):
        try:
            return self.loader.get_source(environment, template)
        except IOError:
            raise TemplateNotFound(template)


class LoaderMissingError(Exception):
    """Error class raised when called on an app with no existing `jinja_loader`
    property.
    """
    def __init__(self, msg=""):
        self.msg = msg
