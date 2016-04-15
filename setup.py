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

import glob

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
 sys.argv.append('py2exe')
 sys.path.append("C:\\Microsoft.VC90.CRT")


 import py2exe

 extra_options = dict(
	options = {
		'py2exe': {
			'optimize': 2, 
			"packages": ['wx.lib.pubsub'],
			}
		},
    windows = [
    	{
    		'script': mainscript,
    		'icon_resources': [(1, "assets/icon.ico")]
    	}
    	],
    zipfile = None,
    data_files = [
    	('', ["default.conf"]),
    	("Microsoft.VC90.CRT", ['C:\\redist\\msvcm90.dll', 
    		'C:\\redist\\msvcp90.dll', 
    		'C:\\redist\\msvcr90.dll'])
    	]
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





