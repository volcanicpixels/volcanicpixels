# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.terms-of-service
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("terms-of-service", __name__)


@bp.route('/terms-of-service')
def render():
    return render_template('terms-of-service')
