"""
raven.contrib.transports.appengine.raven_appengine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details
:license: BSD, see LICENSE for more details
"""
from __future__ import absolute_import

from raven.transport import AsyncTransport, HTTPTransport

try:
    from google.appengine.ext import deferred
except:
    raise ImportError("AppEngineTransport requires the deferred "
                      "library. Enable it in app.yaml.")

class AppEngineTransport(AsyncTransport, HTTPTransport):
    """
    This provides a transport that uses the appengine deferred library.

    This transport does not verify that the message was successful.
    """
    scheme = ['appengine+http', 'appengine+https']

    def __init__(self, parsed_url):
        

        super(AppEngineTransport, self).__init__(parsed_url)

        # Remove the 'appengine+' from the protocol
        self._url = self._url.split('+', 1)[-1]

    def async_send(self, data, headers, success_cb, failure_cb):
        deferred.defer(self.send, data, headers)
        success_cb()

def register_transport():
    from raven import Client
    Client.register_scheme('appengine+http', AppEngineTransport)