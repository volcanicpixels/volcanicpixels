import os

DEBUG = True
TESTING = True

if 'SERVER_NAME' in os.environ:
	SERVER_NAME = os.environ['SERVER_NAME']


cache_enabled = True
profiler_enabled = False
