# encoding: utf-8
"""
    volcanicpixels
    ~~~~~~~~~~~~~~

    Volcanic Pixels application package
"""

import libs

from . import www

www_app = www.create_app()