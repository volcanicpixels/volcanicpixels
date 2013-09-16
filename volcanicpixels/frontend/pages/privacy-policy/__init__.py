# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages.privacy-policy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .. import route, render_template


@route('/privacy-policy')
def render():
    return render_template('pages/privacy-policy')
