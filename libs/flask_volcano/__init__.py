# -*- coding: utf-8 -*-
"""
    flask_volcano
    ~~~~~~~~~~~~~

    An opinionated way of structuring a flask app.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from .helpers import (
    route, register_blueprints, register_views, is_dev_server, make_external,
    canonical_url, server_info, admin_required)
from .factory import create_app, create_blueprint
