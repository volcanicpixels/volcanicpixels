# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.private-blog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("private-blog", __name__)


# trailing slash is for legacy purposes - do not remove
@bp.route('/password-protect-wordpress-plugin/')
def render():
    return render_template('private-blog')
