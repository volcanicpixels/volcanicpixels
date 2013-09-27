# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import logging

from csr_generator import generate_pkey
from flask import (
    jsonify, redirect, request, render_template, session, url_for)
from flask.ext.volcano import create_blueprint
from sslstore_api.methods import get_approver_emails as _get_approver_emails
import stripe

from volcanicpixels.users import (
    get_user, authenticate_user, get_current_user, create_user,
    UserAuthenticationFailedError)

from .data import COUNTRIES, REGIONS

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
                           countries=COUNTRIES, **defaults)


@bp.route('/ssl/test')
def process_order():
    return generate_pkey()


@bp.route('/ssl/process_order', methods=['GET', 'POST'])
def process_order():
    if request.method == 'GET':
        return redirect(url_for('.buy'))

    return _process_order(request.form)


def _process_order(options):

    """
    Validate request info
    """

    credit_card = options.get('credit_card')

    def do_error(msg='An error occured'):
        options['error_msg'] = msg
        options['credit_card'] = credit_card
        return buy(options)

    def is_token(value):
        """Determines whether the passed argument is a stripe token or not"""
        return (value[:3] == 'tok')

    """Normalize request

    At "END NORMALIZE" the user should be created and logged in, they
    should have a stripe id associated with them and if a token was passed
    as credit_card then it should be converted into a card object.

    TODO: update existing user if additional information is provided
    """

    user = get_current_user()
    if not user:
        # user is not logged in, let's see if the email is attached to an
        # account
        email = options.get('email')
        password = options.get('password')
        user = get_user(email)

        if user:
            # account exists - try to authenticate
            try:
                authenticate_user(email, password)
            except UserAuthenticationFailedError:
                return do_error('Password is incorrect')
        else:
            # this is a new account
            user = create_user(email, password, name=name)
            session['user'] = user.id()

    if not user.stripe_id:
        # User doesn't have a stripe customer ID
        customer = stripe.Customers.create(
            name=name,
            email=email
        )

        user.stripe_id = customer.id
        card = customer.cards.create(card=credit_card)
        credit_card = card.id
    else:
        # User has a stripe ID
        customer = stripe.Customer.retrieve(user.stripe_id)
        if is_token(credit_card):
            # this is a new card
            card = customer.cards.create(card=credit_card)
            credit_card = card.id

    user.put()

    """END NORMALIZE"""

    if 'csr' not in options:
        # We need to generate the CSR
        pass


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
    try:
        authenticate_user(email, password)
        return jsonify(
            status='SUCCESS', data={'user': 'correct', 'cards': []})
    except UserAuthenticationFailedError:
        return jsonify(
            status='SUCCESS', data={'user': 'incorrect', 'cards': []})
    except:
        msg = "An error occured whilst trying to check login credentials"

        logging.exception(msg)
        return jsonify(status='ERROR', msg=msg)
