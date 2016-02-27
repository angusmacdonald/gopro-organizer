import sys
import os, shutil
import logging

from configobj import ConfigObj
from wx.lib.pubsub import pub

import photoinfo
import file_matcher
import settings

config = ConfigObj("default.conf", unrepr=True)

VIDEOS = config['videos_dir']

class Organizer:
	""" Main class, finds and moves/copies photos as specified in settings.

		The class is initialized with settings that define how the move will
		take place, and the processGoProDirectory() starts the action on a
		specified set of input and output directories.
	"""

	def __init__(self, sett = settings.OrganizerSettings()):
		"""
			Arguments:
				sett (settings): Config settings related to the processing
					of the directory.
		"""
		
		self.settings = sett

	def processGoProDirectory(self, inputDir, outputDir):
		"""
			Find all the appropriate files in the input directory and
			move/copy them to the output directory.

			Arguments:
				inputDir (str): path to the directory containing GoPro DCIM dirs.
				outputDir (str): path to the directory where results will be stored.
		"""

		absInputPath = os.path.abspath(inputDir)
		absOutputDir = os.path.abspath(outputDir)

		self._moveFilesInDir(absInputPath, absOutputDir)

	def _moveFilesInDir(self, inputDir, outputDir):

		for root, directories, filenames in os.walk(inputDir):
			for filename in filenames: 
				fullFilePath = os.path.join(root,filename) 
				self._processFile(filename, fullFilePath, outputDir)

	def _processFile(self, filename, fullFilePath, rootOutputDir):

		subDirectory = file_matcher.determineDestination(filename, self._getFileNamingPatterns())
		
		if subDirectory:
			# If we know where to move this file, move it
			action = "Moving" if self.settings.moveFile else "Copying"
			logging.debug("{} '{}' to '{}'".format(action, filename, subDirectory))
			pub.sendMessage("STATUS UPDATE", 
				message="{} '{}' to '{}'".format(action, filename, subDirectory))
		
			destDir = self._getDestPath(fullFilePath, rootOutputDir, subDirectory)
			
			newFileName = self._getNewFileName(fullFilePath, destDir)

			self._moveToDir(destDir, fullFilePath, newFileName)
		else:
			# This file type is not recognized so it is ignored
			logging.info("Filename format not recognized: {}".format(filename))
			pub.sendMessage("STATUS UPDATE", 
				message="Ignoring '{}'".format(filename))

	def _getDestPath(self, fullFilePath, rootOutputDir, subDirectory):
		dateTaken = photoinfo.getDateTaken(fullFilePath)
		
		if self.settings.storeByDateTaken:
			return os.path.join(rootOutputDir, dateTaken, subDirectory)
		else :
			return os.path.join(rootOutputDir, subDirectory)

	def _getNewFileName(self, fullFilePath, destDir):
		if self.settings.useCustomNamingFormat:
			customFormat = self.settings.fileNamingFormat
			filename, file_extension = os.path.splitext(fullFilePath)
			
			dateTaken = photoinfo.getDateTaken(fullFilePath, customFormat)
			newFilePath = "{}{}".format(dateTaken, file_extension)

			# Ensure file name is unique (add number to end to make unique if not):
			count = 1
			while True:
				fullPathOfNewFile = absInputPath = os.path.join(destDir, newFilePath)
				logging.debug("Checking if file exists: {}".format(fullPathOfNewFile))
				
				if not os.path.isfile(fullPathOfNewFile):
					logging.debug("File does not exist: {}".format(fullPathOfNewFile))
					break

				newFilePath = "{}_{}{}".format(dateTaken, count, file_extension)
				count += 1

			return newFilePath
		else:
			return os.path.basename(fullFilePath)



	def _getFileNamingPatterns(self):
		patterns = file_matcher.defaultPatterns()
		
		if (self.settings.includeMeta):
			patterns['GOPR\d\d\d\d\.[THM|LRV]'] = VIDEOS

		return patterns

	def _moveToDir(self, destDir, srcFile, fileName):

		if not os.path.exists(destDir):
			os.makedirs(destDir)
		
		destFilePath = os.path.join(destDir, fileName)

		moveFile = self.settings.moveFile

		logging.debug("Moving ({}) '{}'' to '{}'".format(moveFile, destFilePath, destFilePath))

		if moveFile:
			shutil.move(srcFile, destFilePath)
		else:	
			shutil.copy2(srcFile, destFilePath)


if __name__ == '__main__':
	inputDir = sys.argv[1]
	outputDir = sys.argv[2]
	iterateFolder(inputDir, outputDir)