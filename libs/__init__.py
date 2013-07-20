# -*- coding: utf-8 -*-
"""
    libs
    ~~~~

    Fixes python path so packages in /libs/ can be imported.
"""

import os, sys

sys.path.insert(0, os.path.dirname(__file__))