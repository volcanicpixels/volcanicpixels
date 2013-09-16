# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.paegs.customers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from .. import route, render_template


@route('/customers')
def render():
    return render_template('pages/customers')
