# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages.customers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("customers", __name__)


@bp.route('/customers')
def render():
    return render_template('customers')
