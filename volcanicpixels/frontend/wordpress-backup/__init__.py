# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.wordpress-backup
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template

from flask.ext.volcano import create_blueprint

bp = create_blueprint("wordpress-backup", __name__)


@bp.route('/wordpress-backup/')
def render():
    return render_template('wordpress-backup')


@bp.route('/wordpress-backup/signup')
def signup():
    return render_template('wordpress-backup/signup')
