# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template, request

from flask.ext.volcano import create_blueprint

from .data import COUNTRIES, REGIONS

bp = create_blueprint("app-engine-ssl", __name__)


@bp.route('/app-engine-ssl/')
def render():
    return render_template('app-engine-ssl')


@bp.route('/app-engine-ssl/buy')
def buy():
    defaults = {}
    country = request.headers.get('X-Appengine-Country', '').upper()
    region = request.headers.get('X-AppEngine-Region', '').upper()

    # When App Engine is running locally or cannot determine country it
    # returns ZZ as the country code.
    if country == 'ZZ':
        country = 'GB'

    if country is not None:
        defaults['country'] = country
    else:
        defaults['country'] = 'US'

    if country in REGIONS and region in REGIONS[country]:
        defaults['state'] = REGIONS[country][region]

    return render_template('app-engine-ssl/buy',
                           countries=COUNTRIES, **defaults)
