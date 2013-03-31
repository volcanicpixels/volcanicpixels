"""
Application Blueprint provides the admin pages
"""

from flask import Blueprint
import volcano

app = Blueprint('admin',__name__)
volcano.app.register_blueprint(app)

import views