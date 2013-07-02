# -*- coding: utf-8 -*-
""" Removes all dependencies
"""

import os
import shutil
from subprocess import Popen

libs_module_init = """# -*- coding: utf-8 -*-
\"""
	libs
    ~~~~

    Fixes python path so packages in /libs/ can be imported.
\"""

import os, sys

sys.path.insert(0, os.path.dirname(__file__))"""

def main():
	base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	libs_dir = os.path.join(base_dir, 'libs')

	print libs_dir
	if os.path.exists(libs_dir):
		shutil.rmtree(libs_dir)
	os.mkdir(libs_dir)

	with open(os.path.join(libs_dir, '__init__.py'), 'wb') as f:
		f.write(libs_module_init)
		f.close()

	Popen('pip install -r requirements.txt --target=libs', cwd=base_dir)




if __name__ == "__main__":
    main()