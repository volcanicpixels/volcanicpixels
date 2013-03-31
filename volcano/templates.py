from flask import Blueprint, render_template
from . import app

bp = Blueprint('templates',__name__,template_folder='templates/volcano')
app.register_blueprint(bp)

bp = Blueprint('templates_namespaced',__name__,template_folder='templates')
app.register_blueprint(bp)