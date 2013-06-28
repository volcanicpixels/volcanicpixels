from flask import Flask
import os
import logging
from template_tests import is_development


app = Flask(__name__, template_folder='../application/templates/')
app.config.from_object('volcano.default_settings')
if is_development():
	app.config.from_object('volcano.development_settings')
	app.config.from_object('development_settings')
else:
	app.config.from_object('volcano.production_settings')
	app.config.from_object('production_settings')

if app.config['PROFILER_ENABLED']:
	from .profiler import GAEMiniProfiler
	GAEMiniProfiler(app)

import context_processors
import template_tests
import template_globals

"""
	import blueprints
"""

import blueprints
import views
import templates