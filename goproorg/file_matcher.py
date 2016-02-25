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
default_patterns = { 'GOPR\d\d\d\d\.MP4': VIDEOS,
			 'GOPR\d\d\d\d\.JPG': PHOTOS,
			 'GP(\d\d)\d\d\d\d\.MP4': CHAPTERED,
			 'G(\d\d\d)\d\d\d\d\.JPG': TIMELAPSES,
			 '3D_[LR]\d\d\d\d\.MP4': THREE_D }

def defaultPatterns():
	return default_patterns

def getType(fileName, patterns=defaultPatterns()):
	for pattern, dirName in default_patterns.iteritems():
		m = re.search(pattern, fileName)
		
		if m:
			return processMatch(m, pattern, dirName)
	
	return None

def processMatch(m, pattern, name):
	numGroups = len(m.groups())

	if numGroups > 0:
		logging.debug(os.path.join(name, m.groups()[0]))
		return os.path.join(name, m.groups()[0])
	else:
		return name

#Single Video
#GOPRxxxx.mp4
#GOPRxxxx.jpg

#Chaptered Video
#GPzzxxxx.mp4

# Burst / timelapse
# Gyyyxxxx.jpg
# 

# 3D Recording
# 3D_Lxxxx.mp4 (left camera)
# 3D_Rxxxx.mp4 (right camera)