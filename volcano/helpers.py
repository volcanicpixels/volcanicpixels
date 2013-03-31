import os
from flask import render_template as flask_render_template
import global_variables



"""
	Will look for the template in the specified folder otherwise will use application version.
"""
def select_template(template_name, folder=''):
	templates = [os.path.join(folder, template_name), template_name]
	return render_template(templates, **locals())

def render_template(template_name, **context):
	return flask_render_template(template_name, **context)

def variables_dict():
	return_object = {}
	for key in dir(global_variables):
		if key[0:2] != '__':
			return_object[key] = getattr(global_variables, key)
	return return_object