# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages.home
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask.ext.links import get_link

from .. import route, render_template


@route('/', text="Home")
def render():
    """Renders the homepage"""
    projects = [
        {
            "name": "Private Blog WordPress Plugin",
            "teaser": "This plugin makes it easy to make all or part of your "
                      "WordPress blog private.",
            "icon": "li_key"
        },
        {
            "name": "WordPress Backup Service",
            "teaser": "Keeping your data backed-up can be an arduous task. "
                      "Our plugin makes the task completely painless. Packed "
                      "full of features and at an incredible price you'd be "
                      "mad not to!",
            "icon": "li_data"
        },
        {
            "name": "WordPress plugin Update Service",
            "teaser": "The easiest way to distribute updates to your plugin "
                      "via Github.",
            "icon": "li_cloud"
        }
    ]
    return render_template('pages/home', projects=projects)
