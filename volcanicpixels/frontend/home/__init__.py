# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.home
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template, url_for

from flask.ext.volcano import create_blueprint

bp = create_blueprint("home", __name__)


@bp.route('/_ah/warmup')
@bp.route('/')
def render():
    """Renders the homepage"""
    projects = [
        {
            "name": "Private Blog WordPress Plugin",
            "teaser": "This plugin makes it easy to make all or part of your "
                      "WordPress blog private.",
            "icon": "li_key",
            "url": url_for('private-blog')
        },
        {
            "name": "Google App Engine SSL Certificates",
            "teaser": "The quickest and easiest way to get SSL certificates "
                      "for use with Google App Engine. No messing around "
                      "with the terminal or chaining certificates.",
            "icon": "li_key",
            "url": url_for('ssl')
        }
    ]
    """
        {
            "name": "WordPress Backup Service",
            "teaser": "Keeping your data backed-up can be an arduous task. "
                      "Our plugin makes the task completely painless. Packed "
                      "full of features and at an incredible price you'd be "
                      "mad not to!",
            "icon": "li_data",
            "url": url_for('wordpress-backup')
        },
    """
    return render_template('home', projects=projects)
