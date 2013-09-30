# -*- coding: utf-8 -*-
"""
    volcanicpixels.frontend.app-engine-ssl.data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from os import path
import logging

from flask import json

BASE_DIR = path.dirname(__file__)

COUNTRIES_FILE = path.join(BASE_DIR, "countries.json")
try:
    COUNTRIES = json.load(open(COUNTRIES_FILE))
except:
    logging.exception("Failed to load countries.json")
    COUNTRIES = {}
COUNTRIES_BY_NAME = {}

for country in COUNTRIES:
    COUNTRIES_BY_NAME[country['name']] = country
REGIONS_FILE = path.join(BASE_DIR, "regions.json")
try:
    REGIONS = json.load(open(REGIONS_FILE))
except:
    logging.exception("Failed to load regions.json")
