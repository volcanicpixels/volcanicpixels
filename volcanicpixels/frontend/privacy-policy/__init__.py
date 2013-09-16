# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.privacy-policy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("privacy-policy", __name__)


@bp.route('/privacy-policy')
def render():
    return render_template('privacy-policy')
