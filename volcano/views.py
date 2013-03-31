"""
Defines default handlers
"""

from .helpers import render_template
from . import app
from flask import request, redirect, flash, abort, url_for
from google.appengine.api import users
import logging

@app.route('/login/')
def login():
	redirect_to = request.args.get('redirect_to', '/')
	user = users.get_current_user()
	if user:
		flash('Already logged in as user %s' % user.nickname())
		return redirect(redirect_to)
	else:
		return redirect(users.create_login_url(redirect_to))


@app.route('/logout/')
def logout():
	redirect_to = request.args.get('redirect_to', '/')
	return redirect(users.create_logout_url(redirect_to))


"""
	Error pages
"""

@app.errorhandler(404)
def page_not_found(e):
	return render_template('/errors/not_found.page'), 404

@app.errorhandler(500)
def internal_error(e):
	return render_template('/errors/internal_error.page'), 500


# Handle 405 errors
@app.errorhandler(405)
def server_error(e):
	return render_template('/errors/method_not_allowed.page'), 405

"""
	System views
"""

@app.route('/_ah/warmup')
def warmup():
	return ''