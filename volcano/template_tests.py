from flask import request
from . import app
import os

@app.template_test()
def https(url=None):
	if url == None:
		url = request.url
	return 'https://' == url[0:8]

@app.template_test()
def is_development():
	return 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev')