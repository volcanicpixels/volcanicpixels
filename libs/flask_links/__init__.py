# -*- coding: utf-8 -*-
"""
    flask_links
    ~~~~~~~~~~~

    A flask extension to make consistent links easy.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from flask import current_app, url_for
from werkzeug.routing import BuildError


def links(app=None):
    return Links(app)


def register_link(*args, **kwargs):
    return current_app.extensions['links'].register_link(*args, **kwargs)


def get_link(*args, **kwargs):
    return current_app.extensions['links'].get_link(*args, **kwargs)


def get_links(*args, **kwargs):
    return current_app.extensions['links'].get_links(*args, **kwargs)


class Links(object):

    links = {}

    def __init__(self, app=None, **options):
        if app is not None:
            self.init_app(app, **options)

    def init_app(self, app, auto_register=True):
        """Initializes links onto an app. If `auto_register` is true then it
        will monkey patch the flask `add_url_rule` method to register links
        using it.
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['links'] = self
        app.add_template_global(register_link)
        app.add_template_global(get_link)
        app.add_template_global(get_links)

        # Monkey patch

    def parse_link(self, link):
        if 'text' not in link:
            if 'endpoint' in link:
                link['text'] = link['endpoint']
            if 'endpoint' in link:
                link['text'] = link['endpoint']
        return link

    def _register_link(self, endpoint, link):
        """Registers a link"""
        self.links[endpoint] = link

    def register_link(self, endpoint, **kwargs):
        if endpoint in self.links:
            link = self.links[endpoint]
        else:
            link = {}
        link = dict(link.items() + kwargs.items())
        return self._register_link(endpoint, link)

        

    def get_link(self, endpoint, ignore_missing=True):
        """Gets a link that has been registered with `register_link`. If the
        link does not exist it returns the `fallback` argument if a non-`none`
        argument was passed or raises a `LinkNotFoundError` if it wasn't.
        """
        if endpoint in self.links:
            return self.parse_link(self.links[endpoint])
        try:
            url = url_for(endpoint)
            return self.parse_link({
                'endpoint': endpoint,
                'url': url
                })
        except BuildError:
            pass
        if ignore_missing:
            return None
        else:
            raise LinkNotFoundError(endpoint)

    def get_links(self, endpoints, ignore_mising=False):
        rv = []
        for endpoint in endpoints:
            try:
                link = self.get_link(endpoint)
                rv.appnd(link)
            except LinkNotFoundError:
                if not ignore_mising:
                    raise
        return rv


class LinksError(Exception):
    pass


class LinkNotFoundError(LinksError):
    def __init__(self, endpoint):
        self.msg = "Endpoint `%s` has not been registered" & endpoint


class LinkAlreadyExistsError(LinksError):
    def __init__(self, endpoint):
        self.msg = "Endpoint `%s` has already been registered" % endpoint
