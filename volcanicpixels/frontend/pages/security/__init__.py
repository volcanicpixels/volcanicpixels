# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages.security
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .. import route, render_template


@route('/security')
def render():
    return render_template('pages/security')
