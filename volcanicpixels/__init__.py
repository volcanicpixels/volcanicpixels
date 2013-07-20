# encoding: utf-8
"""
    volcanicpixels
    ~~~~~~~~~~~~~~

    Volcanic Pixels application package
"""

import libs

from .www import create_app as create_www_app

www = create_www_app()

