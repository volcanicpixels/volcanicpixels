# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl.countries
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from os import path

from flask import json

BASE_DIR = path.dirname(__file__)

COUNTRIES_FILE = path.join(BASE_DIR, "countries.json")
COUNTRIES = json.load(open(COUNTRIES_FILE))


REGIONS_FILE = path.join(BASE_DIR, "regions.json")
REGIONS = json.load(open(REGIONS_FILE))

BLOCKED_COUNTRIES = ["AO", "CU", "LY", "KP", "IR", "SY", "SL", "SD", "YU"]
