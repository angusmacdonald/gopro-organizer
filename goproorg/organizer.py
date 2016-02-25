import sys
import os, shutil
import logging

from configobj import ConfigObj

import photoinfo
import file_matcher

config = ConfigObj("default.conf", unrepr=True)

VIDEOS = config['videos_dir']

def processGoProDirectory(inputDir, outputDir):

	absInputPath = os.path.abspath(inputDir)
	absOutputDir = os.path.abspath(outputDir)

	print absInputPath

	for item in os.listdir(absInputPath):

		if not os.path.isfile(item):
			_moveFilesInDir(os.path.join(inputDir, item), absOutputDir)
		else:
			continue

def _moveFilesInDir(inputDir, outputDir):
	for file in os.listdir(inputDir):
		_processFile(file, inputDir, outputDir)

def _processFile(fileName, inputDir, rootOutputDir):
	fullFilePath = os.path.join(inputDir, fileName)

	subDirectory = file_matcher.determineDestination(fileName, _getFileNamingPatterns())
	
	if subDirectory:
		# If we know where to move this file, move it
		logging.debug("Moving '{}' to '{}'".format(fileName, subDirectory))

		destDir = _getDestDirectory(fullFilePath, rootOutputDir, subDirectory)
		
		_moveToDir(destDir, fullFilePath)
	else:
		# This file type is not recognized so it is ignored
		logging.info("Filename format not recognized: {}".format(fileName))

def _getDestDirectory(fullFilePath, rootOutputDir, subDirectory):
	dateTaken = photoinfo.getDateTaken(fullFilePath)
	
	return os.path.join(rootOutputDir, dateTaken, subDirectory)

def _getFileNamingPatterns():
	patterns = file_matcher.defaultPatterns()
	
	if (config['includeThmAndLrvFiles']):
		patterns['GOPR\d\d\d\d\.[THM|LRV]'] = VIDEOS

	return patterns

def _moveToDir(destDir, filePath):

	if not os.path.exists(destDir):
		os.makedirs(destDir)

	fileName = os.path.basename(filePath)
	
	destFilePath = os.path.join(destDir, fileName)

	moveFile = config['move']

	logging.debug("Moving ({}) '{}'' to '{}'".format(moveFile, filePath, destFilePath))

	if moveFile:
		shutil.move(filePath, destFilePath)
	else:	
		shutil.copy2(filePath, destFilePath)

if __name__ == '__main__':
	inputDir = sys.argv[1]
	outputDir = sys.argv[2]
	iterateFolder(inputDir, outputDir)