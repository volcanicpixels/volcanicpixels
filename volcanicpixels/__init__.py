# encoding: utf-8
"""
    volcanicpixels
    ~~~~~~~~~~~~~~

    Volcanic Pixels application package
"""

import libs

from . import core
from . import www

WWW = www.create_app()
