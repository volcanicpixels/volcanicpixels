# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages.terms-of-service
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .. import route, render_template


@route('/terms-of-service')
def render():
    return render_template('pages/terms-of-service')
