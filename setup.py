"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
	 python setup.py py2app

 Usage (Windows):
	 python setup.py py2exe
 """

import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'organizerui/controller.py'

if sys.platform == 'darwin':
 extra_options = dict(
	 setup_requires=['py2app'],
	 app=[mainscript],
	 # Cross-platform applications generally expect sys.argv to
	 # be used for opening files.
	 options=dict(py2app=dict(
	 	argv_emulation=False, 
	 	resources=["default.conf"], 
	 	iconfile="assets/icon.icns")
	 ),
 )
elif sys.platform == 'win32':
 extra_options = dict(
	 setup_requires=['py2exe'],
	 app=[mainscript],
 )
else:
	extra_options = {
		'description': 'GoPro photo organizer, separating photos, videos, etc.',
		'author': 'Angus Macdonald',
		'url': 'https://github.com/angusmacdonald/gopro-organizer',
		'download_url': 'http://github.com/angusmacdonald/gopro-organizer',
		'author_email': 'angus.d.macdonald AT gmail.com',
		'version': '0.1',
		'install_requires': ['nose', 'configobj'],
		'packages': ['goproorg'],
		'scripts': []
	}

setup(
	name="GoPro Organizer",
	**extra_options
)
