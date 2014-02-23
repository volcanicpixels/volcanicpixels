# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.security
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("security", __name__)


@bp.route('/security')
def render():
    return render_template('security')
