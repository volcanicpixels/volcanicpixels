# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.privacy-policy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from .. import route, create_blueprint

bp = create_blueprint('privacy-policy', __name__)


@route(bp, '/privacy-policy')
def render():
    return render_template('privacy-policy')
