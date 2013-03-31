from flask import render_template, abort
from jinja2 import TemplateNotFound
from . import app
from .decorators import cached
import logging
import volcano


@app.route('/')
@app.route('/<page_id>/')
def test(page_id='home'):
	try:
		return render_template('%s.page' % page_id)
	except TemplateNotFound:
		abort(404)