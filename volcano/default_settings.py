DEBUG = False
TESTING = False


"""
	Application settings
"""

try:
	from .secret_keys import SECRET_KEY, SESSION_KEY
except ImportError:
	import logging
	from flask import abort
	logging.error('No secret keys defined - run /config/generate_keys.py to generate them (make sure to remove them from source control)')
	# secret keys must be defined
	abort(500)

CACHE_TIMEOUT = 60*60*24
CACHE_ENABLED = True
PROFILER_ENABLED = True
SECURE_ASSET_DOMAIN = ASSET_DOMAIN = '//commondatastorage.googleapis.com/assets.volcanicpixels.com'