# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.terms-of-service
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from .. import route, create_blueprint

bp = create_blueprint('terms-of-service', __name__)


@route(bp, '/terms-of-service')
def index():
    return render_template('terms-of-service')
