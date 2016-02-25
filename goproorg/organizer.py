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
	def __init__(self, sett = settings.OrganizerSettings()):
		self.settings = sett

	def processGoProDirectory(self, inputDir, outputDir):
		absInputPath = os.path.abspath(inputDir)
		absOutputDir = os.path.abspath(outputDir)

		print absInputPath

		for item in os.listdir(absInputPath):

			if not os.path.isfile(item):
				self._moveFilesInDir(os.path.join(inputDir, item), absOutputDir)
			else:
				continue

	def _moveFilesInDir(self, inputDir, outputDir):
		for file in os.listdir(inputDir):
			self._processFile(file, inputDir, outputDir)

	def _processFile(self, fileName, inputDir, rootOutputDir):
		fullFilePath = os.path.join(inputDir, fileName)
			
		subDirectory = file_matcher.determineDestination(fileName, self._getFileNamingPatterns())
		
		if subDirectory:
			# If we know where to move this file, move it
			action = "Moving" if self.settings.moveFile else "Copying"
			logging.debug("{} '{}' to '{}'".format(action, fileName, subDirectory))
			pub.sendMessage("STATUS UPDATE", 
				message="{} '{}' to '{}'".format(action, fileName, subDirectory))
		
			destDir = self._getDestDirectory(fullFilePath, rootOutputDir, subDirectory)
			
			self._moveToDir(destDir, fullFilePath)
		else:
			# This file type is not recognized so it is ignored
			logging.info("Filename format not recognized: {}".format(fileName))
			pub.sendMessage("STATUS UPDATE", 
				message="Ignoring '{}'".format(fileName))

	def _getDestDirectory(self, fullFilePath, rootOutputDir, subDirectory):
		dateTaken = photoinfo.getDateTaken(fullFilePath)
		
		return os.path.join(rootOutputDir, dateTaken, subDirectory)

	def _getFileNamingPatterns(self):
		patterns = file_matcher.defaultPatterns()
		
		if (self.settings.includeMeta):
			patterns['GOPR\d\d\d\d\.[THM|LRV]'] = VIDEOS

		return patterns

	def _moveToDir(self, destDir, filePath):

		if not os.path.exists(destDir):
			os.makedirs(destDir)

		fileName = os.path.basename(filePath)
		
		destFilePath = os.path.join(destDir, fileName)

		moveFile = self.settings.moveFile

		logging.debug("Moving ({}) '{}'' to '{}'".format(moveFile, filePath, destFilePath))

		if moveFile:
			shutil.move(filePath, destFilePath)
		else:	
			shutil.copy2(filePath, destFilePath)

if __name__ == '__main__':
	inputDir = sys.argv[1]
	outputDir = sys.argv[2]
	iterateFolder(inputDir, outputDir)