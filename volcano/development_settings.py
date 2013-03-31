import os

DEBUG = True
TESTING = True

if 'LOCAL_SERVER_NAME' in os.environ:
	SERVER_NAME = os.environ['LOCAL_SERVER_NAME']

cache_enabled = False
profiler_enabled = True