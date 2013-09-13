# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.customers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from .. import route, create_blueprint

bp = create_blueprint('customers', __name__)


@route(bp, '/customers')
def index():
    return render_template('customers')
