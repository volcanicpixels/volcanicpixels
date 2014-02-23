# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import render_template


def handle_404(e):
    return render_template('errors/404'), 404


def handle_500(e):
    return render_template('errors/500'), 500


def register_error_handlers(app):
    app.errorhandler(404)(handle_404)

    app.errorhandler(500)(handle_500)
