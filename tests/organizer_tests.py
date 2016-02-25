from nose.tools import *

from goproorg import organizer
import shutil, tempfile, os

from configobj import ConfigObj

config = ConfigObj("default.conf", unrepr=True)

PHOTOS = config['photos_dir']
VIDEOS = config['videos_dir']
TIMELAPSES = config['timelapses_dir']


class TestOrganizer:
	def setUp(self):
		self.input_dir = tempfile.mkdtemp()
		self.output_dir = tempfile.mkdtemp()

		photos = ("GOPR9962.JPG", "GOPR9963.JPG", "GOPR9964.JPG")
		movies = ("GOPR9961.MP4", "GOPR9990.MP4")
		utils = ("GOPR9990.THM", "GOPR9990.LRV")
		timeLapses = ("G0098818.JPG", "G0098819.JPG", "G0098820.JPG", "G0108821.JPG")
		
		self.files = ()

		for photo in (photos + movies + utils + timeLapses):
			containingDir = os.path.join(self.input_dir, "DCIM1")

			if not os.path.exists(containingDir):
				os.makedirs(containingDir)

			fileName = os.path.join(containingDir, photo)
			self.files = self.files + (createFileWithName(fileName), )

	def tearDown(self):
		shutil.rmtree(self.input_dir)
	
	def test_files_created(self):
		assert len(self.files) > 0
		for file in self.files:
			print "Check if exists: {}".format(file.name)
			assert os.path.exists(file.name)

	def test_files_organized(self):
		organizer.processGoProDirectory(self.input_dir, self.output_dir)

		assert len(os.listdir(self.output_dir)) == 1

		dateDir = os.path.join(self.output_dir, os.listdir(self.output_dir)[0])

		assert len(os.listdir(dateDir)) == 3

		valid_names = ['photos', 'videos', 'timelapses']

		for name in os.listdir(dateDir):
			assert any(name in s for s in valid_names)
		
		assert len(os.listdir(os.path.join(dateDir, PHOTOS))) == 3
		assert len(os.listdir(os.path.join(dateDir, VIDEOS))) == 2
		assert len(os.listdir(os.path.join(dateDir, TIMELAPSES))) == 2

		assert len(os.listdir(os.path.join(dateDir, TIMELAPSES, '009'))) == 3
		assert len(os.listdir(os.path.join(dateDir, TIMELAPSES, '010'))) == 1

		


def createFileWithName(name):
	return open(name, 'w+')