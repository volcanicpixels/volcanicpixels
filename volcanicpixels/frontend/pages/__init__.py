# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from functools import wraps

from flask import render_template

from .. import create_blueprint, route as _route

bp = create_blueprint('pages', __name__)


def route(*args, **kwargs):
    return _route(bp, *args, **kwargs)
