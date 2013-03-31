from . import app
from .helpers import variables_dict


@app.context_processor
def add_globals():
	return variables_dict()