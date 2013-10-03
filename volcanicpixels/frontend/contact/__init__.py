# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.contact
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("contact", __name__)


@bp.route('/contact-us/')
@bp.route('/contact')
def render():
    return render_template('contact')
