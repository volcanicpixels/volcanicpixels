"""
	Decorators for URL handlers
"""
import os
from functools import wraps
from google.appengine.api import users, memcache
from flask import request, make_response
from . import app


def cached(func, timeout=None):
	if timeout is None:
		timeout = app.config.get('CACHE_TIMEOUT', 60*60)

	def cache_key():
		return request.path

	def cache_namespace():
		return os.environ['CURRENT_VERSION_ID']

	@wraps(func)
	def decorated_view(*args,**kwargs):
		if not app.config.get('CACHE_ENABLED'):
			return func(*args, **kwargs)
		if users.get_current_user(): # caching disabled for logged-in users
			return func(*args, **kwargs)

		response = memcache.get(cache_key(),namespace=cache_namespace())
		if response is None:
			response = make_response(func(*args, **kwargs))
			memcache.add(cache_key(),response, timeout, namespace=cache_namespace())
			response.headers.add('Added-To-Cache', cache_key() + '@' + cache_namespace())
		else:
			response.headers.add('From-Cache', cache_key() + '@' + cache_namespace())
		return response
	return decorated_view