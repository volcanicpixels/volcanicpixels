# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import jsonify, request, render_template
from flask.ext.volcano import create_blueprint
from sslstore_api.methods import get_approver_emails as _get_approver_emails

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


@bp.route('/app-engine-ssl/get_approver_emails')
def get_approver_emails():
    """Get's the approver emails for a domain and returns an API response"""
    domain = request.args.get("domain", '')
    try:
        emails = _get_approver_emails(domain)
        return jsonify(status='SUCCESS', data=emails)
    except:
        msg = "An error occured whilst trying to retrieve the " + \
            "verification emails for %s" % domain
        return jsonify(status='ERROR', msg=msg)
