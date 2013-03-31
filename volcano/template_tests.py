from flask import request
from . import app

@app.template_test()
def https(url=None):
	if url == None:
		url = request.url
	return 'https://' == url[0:8]