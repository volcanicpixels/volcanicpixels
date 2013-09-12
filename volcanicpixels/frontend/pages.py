# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.pages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import Blueprint, render_template

from . import route

bp = Blueprint('pages', __name__)


@route(bp, '/')
def home():
    return render_template('home.html')
