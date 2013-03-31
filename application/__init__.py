"""
Application Blueprint provides the code for main site
"""

from flask import Blueprint
import volcano

app = Blueprint('application', __name__, template_folder='templates')
from .views import *

volcano.app.register_blueprint(app)