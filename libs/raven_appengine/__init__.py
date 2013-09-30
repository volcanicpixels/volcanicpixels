# -*- coding: utf-8 -*-
"""
    raven_appengine
    ~~~~~~~~~~~~~~~

    A raven transport that uses the appengine deferred library. This transport
    does not verify that the message was sent successfully.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from libs import fix_path

fix_path()

# hack to let the deferred library work
from libs.raven_appengine.fix import *
