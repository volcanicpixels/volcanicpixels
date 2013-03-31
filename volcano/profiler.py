import os
from flask.helpers import send_from_directory
from flask import request, jsonify
from .gae_mini_profiler import profiler, templatetags
from jinja2 import Environment, FileSystemLoader

import logging

def replace_insensitive(string, target, replacement):
	"""Similar to string.replace() but is case insensitive
	Code borrowed from: http://forums.devshed.com/python-programming-11/
	case-insensitive-string-replace-490921.html
	"""

	no_case = string.lower()
	index = no_case.rfind(target.lower())
	if index >= 0:
		return string[:index] + replacement + string[index + len(target):]
	else:
		return string


class GAEMiniProfilerWSGIMiddleware(profiler.ProfilerWSGIMiddleware):

	def __init__(self, flask_app, *args, **kwargs):
		self.flask_app = flask_app
		profiler.ProfilerWSGIMiddleware.__init__(self, *args, **kwargs)

	def should_profile(self, environ):
		from google.appengine.api import users

		if environ["PATH_INFO"].startswith("/gae_mini_profiler/"):
			return False

		if self.flask_app.config['GAEMINIPROFILER_PROFILER_ADMINS'] and \
		   users.is_current_user_admin():
			return True

		user = users.get_current_user()

		return user and user.email() in \
				self.flask_app.config['GAEMINIPROFILER_PROFILER_EMAILS']


class GAEMiniProfiler(object):

	PROFILER_URL_PREFIX = "/_gae_mini_profiler/"

	def __init__(self, app, *args, **kwargs):
		self.app = app

		# Apply the middleware
		app.wsgi_app = GAEMiniProfilerWSGIMiddleware(app, app.wsgi_app)

		# Set up config defaults
		self.app.config.setdefault('GAEMINIPROFILER_PROFILER_EMAILS', [
			'test@example.com'
		])
		self.app.config.setdefault('GAEMINIPROFILER_PROFILER_ADMINS', True)

		# Build the static path based on our current directory
		base_dir = os.path.dirname(__file__)
		self._static_dir = os.path.join(base_dir, 'gae_mini_profiler/static')

		# Configure jinja for internal templates
		logging.error(os.path.join(base_dir, 'gae_mini_profiler/templates'))
		self.jinja_env = Environment(
			autoescape=True,
			extensions=['jinja2.ext.i18n'],
			loader=FileSystemLoader(
				os.path.join(base_dir, 'gae_mini_profiler/templates')
			)
		)

		# Install the response hook
		app.after_request(self._process_response)

		app.add_url_rule(self.PROFILER_URL_PREFIX + "static/<path:filename>",
						 'gae_mini_profiler.static', self._send_static_file)
		app.add_url_rule(self.PROFILER_URL_PREFIX + "request",
						 'gae_mini_profiler.request', self._request_view)
		app.add_url_rule(self.PROFILER_URL_PREFIX + "shared",
						 'gae_mini_profiler.share', self._share_view)

	def _send_static_file(self, filename):
		"""Send an internal static file."""

		return send_from_directory(self._static_dir, filename)

	def _process_response(self, response):
		"""Process response and append the profiler code if appropriate."""

		if response.status_code != 200 or not response.is_sequence:
			return response

		response_html = response.data.decode(response.charset)
		profiler_html = templatetags.profiler_includes()

		# Inject the profiler HTML snippet right before the </body>
		response.response = [
			replace_insensitive(
				response_html,
				'</body>',
				profiler_html + '</body>'
			)
		]

		return response

	def _render_profiler(self):
		context = self._get_render_context()
		context['request_id'] = profiler.CurrentRequestId.get()
		return self._render("includes.html", context)

	def _get_render_context(self):
		return {
			'js_path': "/gae_mini_profiler/static/js/profiler.js?",
			'css_path': "/gae_mini_profiler/static/css/profiler.css"
		}

	def _render(self, template_name, context):
		"""Render a jinja2 template within the application's environment."""

		template = self.jinja_env.get_template(template_name)
		return template.render(**context)

	def _request_view(self):
		"""Renders the request stats."""

		request_id = request.args['request_id']
		stats = profiler.RequestStats.get(request_id)

		if not stats:
			return u''

		dict_request_stats = {}
		for property in profiler.RequestStats.serialized_properties:
			dict_request_stats[property] = \
					stats.__getattribute__(property)

		return jsonify(dict_request_stats)

	def _share_view(self):
		"""Renders the shared stats view."""

		request_id = request.args['request_id']

		if not profiler.RequestStats.get(request_id):
			return u"Profiler stats no longer available."

		context = self._get_render_context()
		context['request_id'] = request_id
		return self._render("shared.html", context)