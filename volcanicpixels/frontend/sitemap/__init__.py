# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.sitemap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template, request, url_for
from flask.ext.volcano import create_blueprint

bp = create_blueprint("sitemap", __name__,)


@bp.route('/sitemap.xml')
def render():
    url_root = request.url_root[:-1]
    pages = []
    endpoints = ['home', 'private-blog', 'ssl', 'ssl.buy', 'customers',
                 'security', 'terms-of-service', 'privacy-policy']

    for endpoint in endpoints:
        pages.append(url_for(endpoint))

    return render_template('sitemap', pages=pages, url_root=url_root)
