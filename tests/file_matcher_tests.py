from nose.tools import *
import os

from goproorg import file_matcher
from configobj import ConfigObj

config = ConfigObj("default.conf", unrepr=True)

PHOTOS = config['photos_dir']
VIDEOS = config['videos_dir']
TIMELAPSES = config['timelapses_dir']
CHAPTERED = config['chaptered_dir']
THREE_D = config['three_d_dir']

class TestFileMatcher:
	
	def test_photo(self):
		assert PHOTOS == file_matcher.determineDestination("GOPR0023.JPG")
	def test_video(self):
		assert VIDEOS == file_matcher.determineDestination("GOPR0023.MP4")
	def test_timelapse(self):
		print os.path.join(TIMELAPSES, "009") == file_matcher.determineDestination("G0090023.JPG")
		assert os.path.join(TIMELAPSES, "009") == file_matcher.determineDestination("G0090023.JPG")
	def test_chaptered(self):
		assert os.path.join(CHAPTERED, "09") == file_matcher.determineDestination("GP090023.MP4")
	def test_3d(self):
		assert THREE_D == file_matcher.determineDestination("3D_L0023.MP4")
		assert THREE_D == file_matcher.determineDestination("3D_R0023.MP4")
	def test_unknown(self):
		assert not file_matcher.determineDestination("blah.JPG")