import sys
import os, shutil
import logging

from configobj import ConfigObj

import photoinfo
import file_matcher

config = ConfigObj("default.conf", unrepr=True)

VIDEOS = config['videos_dir']

def iterateFolder(inputDir, outputDir):

	absInputPath = os.path.abspath(inputDir)
	absOutputDir = os.path.abspath(outputDir)

	print absInputPath

	for item in os.listdir(absInputPath):

		if not os.path.isfile(item):
			moveFilesInDir(os.path.join(inputDir, item), absOutputDir)
		else:
			continue

def moveFilesInDir(inputDir, outputDir):
	for file in os.listdir(inputDir):

		fullFilePath = os.path.join(inputDir, file)

		patterns = file_matcher.defaultPatterns()
		
		if (config['includeThmAndLrvFiles']):
			patterns['GOPR\d\d\d\d\.[THM|LRV]'] = VIDEOS

		subDirectory = file_matcher.getType(file, patterns)
		
		if subDirectory:
			logging.debug("Moving '{}' to '{}'".format(file, subDirectory))

			dateTaken = photoinfo.getDateTaken(fullFilePath)
			moveToDir(dateTaken, subDirectory, fullFilePath, outputDir)
		else:
			logging.info("Filename format not recognized: {}".format(file))

def moveToDir(dateDir, subDir, filePath, outputDir):

	dateDirPath = os.path.join(outputDir, dateDir)

	subDirPath =  os.path.join(dateDirPath, subDir)

	if not os.path.exists(subDirPath):
		os.makedirs(subDirPath)

	fileName = os.path.basename(filePath)
	destLocation = os.path.join(subDirPath, fileName)

	if config['move'] == 'True':
		logging.debug("Moving {} to {}".format(filePath, destLocation))
		shutil.move(filePath, destLocation)
	else:	
		logging.debug("Copying {} to {}".format(filePath, destLocation))
		shutil.copy2(filePath, destLocation)

if __name__ == '__main__':
	inputDir = sys.argv[1]
	outputDir = sys.argv[2]
	iterateFolder(inputDir, outputDir)