# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.domain_changer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("domain-changer", __name__)


# trailing slash is for legacy purposes - do not remove

@bp.route('/wordpress-domain-changer-plugin')
def render():
    return render_template('domain-changer')