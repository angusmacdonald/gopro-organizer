import re
import os
import logging

from configobj import ConfigObj
config = ConfigObj("default.conf", unrepr=True)

PHOTOS = config['photos_dir']
VIDEOS = config['videos_dir']
TIMELAPSES = config['timelapses_dir']
CHAPTERED = config['chaptered_dir']
THREE_D = config['three_d_dir']

# Via http://gopro.com/support/articles/hero3-and-hero3-file-naming-convention
def default_patterns():
	""" Returns a dictionary mapping file regex patterns to the name of the directory
		where these files should be stored when matched
	"""

	return { 'GOPR\d\d\d\d\.MP4': VIDEOS,
			 'GOPR\d\d\d\d\.JPG': PHOTOS,
			 'GP(\d\d)\d\d\d\d\.MP4': CHAPTERED,
			 'G(\d\d\d)\d\d\d\d\.JPG': TIMELAPSES,
			 '3D_[LR]\d\d\d\d\.MP4': THREE_D }

def determine_destination(file_name, patterns=default_patterns()):
	""" Given a filename, return the directory where this file should be stored.

		'None' is returned if the file is not recognized amongst the provided patterns.

		Arguments:
			file_name (str): Name of the file being checked.
			patterns (dict): regex dict of the form described in 'default_patterns()'

		Returns: The relative path to the directory where the file should be stored, or
			None if the file is not recognized.
	"""

	for pattern, dirName in patterns.iteritems():
		m = re.search(pattern, file_name)
		
		if m:
			return _process_match(m, pattern, dirName)
	
	return None

def _process_match(m, pattern, name):
	numGroups = len(m.groups())

	if numGroups > 0:
		logging.debug(os.path.join(name, m.groups()[0]))
		return os.path.join(name, m.groups()[0])
	else:
		return name