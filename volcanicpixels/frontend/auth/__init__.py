# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import logging

from flask import render_template, url_for, request, redirect

from flask.ext.volcano import create_blueprint
from volcanicpixels.users import (
    authenticate_user, UserNotFoundError, UserAuthenticationFailedError,
    logout_user)

bp = create_blueprint("auth", __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page"""
    if request.method == 'GET':
        return render_template('auth/login')

    email = request.form.get('email')
    password = request.form.get('password')
    redirect_url = request.args.get('redirect', None)
    if redirect_url is None:
        redirect_url = url_for('home')

    try:
        authenticate_user(email, password)
    except UserNotFoundError:
        logging.info('User not found')
        return render_template('auth/login', error="That user doesn't exist")
    except UserAuthenticationFailedError:
        return render_template(
            'auth/login', error="Incorrect Password", email=email)
        logging.info('Wrong password')
    return redirect(redirect_url)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
