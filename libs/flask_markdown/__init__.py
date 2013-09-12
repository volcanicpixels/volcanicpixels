# -*- coding: utf-8 -*-
"""
    flask_markdown
    ~~~~~~~~~~~~~~

    A flask extension to add markdown support.

    :copyright: (c) 2013 by Daniel Chatfield
"""

from jinja2_markdown_extension import MarkdownExtension

def markdown(app):
    app.jinja_env.add_extension(MarkdownExtension)
