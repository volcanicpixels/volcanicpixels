# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import logging
import sys
import stripe
from flask import jsonify, redirect, request, render_template, url_for
from flask.ext.volcano import create_blueprint
from sslstore_api.methods import get_approver_emails as _get_approver_emails

from volcanicpixels.ssl import process_request
from volcanicpixels.users import (
    get_user, authenticate_user, UserAuthenticationFailedError,
    get_current_user, User)

from .data import COUNTRIES_BY_NAME, REGIONS

bp = create_blueprint("ssl", __name__)


@bp.route('/app-engine-ssl')
def render():
    return render_template('ssl')


@bp.route('/ssl/buy')
def buy(defaults=None):
    if defaults is None:
        defaults = {}
    country = request.headers.get('X-Appengine-Country', '').upper()
    region = request.headers.get('X-AppEngine-Region', '').upper()

    if 'country' not in defaults:
        # When App Engine is running locally or cannot determine country it
        # returns ZZ as the country code.
        if country == 'ZZ':
            country = 'GB'

        if country is not None:
            defaults['country'] = country
        else:
            defaults['country'] = 'US'

    if 'state' not in defaults:
        if country in REGIONS and region in REGIONS[country]:
            defaults['state'] = REGIONS[country][region]

    return render_template('ssl/buy',
                           countries=COUNTRIES_BY_NAME, **defaults)


@bp.route('/ssl/test2')
def test2():
    from volcanicpixels.ssl.csr import test_csr
    return test_csr()


@bp.route('/ssl/buy', methods=['POST'])
def process_order():
    if request.method == 'GET':
        return redirect(url_for('.buy'))

    options = request.form

    state = options.get('state')
    country = options.get('country')

    if country in REGIONS and state in REGIONS[country]:
        options['state'] = REGIONS[country][state]

    return process_request(options)


@bp.route('/ssl/get_approver_emails')
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


@bp.route('/ssl/check_email')
def check_email():
    """Checks whether an email belongs to an account or not."""
    email = request.args.get("email")
    try:
        user = get_user(email)
        if user:
            return jsonify(status='SUCCESS', data='existing')
        else:
            return jsonify(status='SUCCESS', data='new')
    except:
        msg = "An error occured whilst trying to check if this email is " + \
            "associated with an existing user."

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)


@bp.route('/ssl/check_password')
def check_password():
    """Checks whether the submitted password is correct."""
    email = request.args.get("email")
    password = request.args.get("password")
    msg = None
    try:
        User.authenticate(email, password)
        msg = "An error occured whilst retrieving your details from stripe"
        return jsonify(
            status='SUCCESS', data={'user': 'correct'})
    except UserAuthenticationFailedError:
        return jsonify(
            status='SUCCESS', data={'user': 'incorrect'})
    except:
        if msg is None:
            msg = "An error occured whilst trying to check login credentials"

            msg += "\n\n" + sys.exc_info()[0]

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)


@bp.route('/ssl/get_cards')
def get_cards():
    msg = None
    try:
        user = get_current_user()
        if not user:
            email = request.args.get('email')
            password = request.args.get('password')
            user = User.authenticate(email, password)
        cards = []
        if user.stripe_id:
            customer = stripe.Customer.retrieve(user.stripe_id)
            for _card in customer.cards.data:
                card = {
                    "name": "**** **** **** " + _card.last4,
                    "id": _card.id
                }

                if _card.id == customer.default_card:
                    card['default'] = True
                cards.append(card)

        return jsonify(
            status='SUCCESS', data={'cards': cards})
    except:
        if msg is None:
            msg = "An error occured whilst retrieving your details from stripe"

            msg += "\n\n" + sys.exc_info()[0]

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)
