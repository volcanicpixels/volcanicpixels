from . import app
from .template_tests import https
from flask import request
from gae_mini_profiler.templatetags import profiler_includes
import logging

@app.template_global()
def asset_domain(url=None):
	if https(url):
		return app.config.get('ASSET_DOMAIN')
	else:
		return app.config.get('SECURE_ASSET_DOMAIN')

@app.template_global()
def canonical_url():
	return request.url
