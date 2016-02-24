
import sys
import os
import shutil

from configobj import ConfigObj

import photoinfo

config = ConfigObj("default.conf", unrepr=True)

PHOTOS = config['photos_dir']
VIDEOS = config['videos_dir']
TIMELAPSES = config['timelapses_dir']

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

		acceptedVideoFormats = ('.MP4')

		if (config['includeLrvFile']):
			acceptedVideoFormats + ('.LRV')
		if (config['includeThmFile']):
			acceptedVideoFormats + ('.THM')


		if file.endswith(('.JPG')) and file.startswith('GOPR'):
			# This is a regular photo
			print "Moving photo {}".format(file)
			moveToDir(photoinfo.getDateTaken(fullFilePath), PHOTOS, fullFilePath, outputDir)
		elif file.endswith(('.JPG')):
			# This is a time lapse photo
			print "Moving timelapse photo {}".format(file)
			timeLapseNum = file[1:4]
			print "Time lapse number {}".format(timeLapseNum)
			outputSubDir = "{}/{}".format(TIMELAPSES, timeLapseNum)
			moveToDir(photoinfo.getDateTaken(fullFilePath), outputSubDir, fullFilePath, outputDir)
		elif file.endswith(acceptedVideoFormats):	
			print "Moving video {}".format(file)
			moveToDir(photoinfo.getDateTaken(fullFilePath), VIDEOS, fullFilePath, outputDir)

def moveToDir(dateDir, subDir, filePath, outputDir):

	dateDirPath = os.path.join(outputDir, dateDir)

	subDirPath =  os.path.join(dateDirPath, subDir)

	if not os.path.exists(subDirPath):
		os.makedirs(subDirPath)

	fileName = os.path.basename(filePath)
	destLocation = os.path.join(subDirPath, fileName)

	if config['move'] == 'True':
		print "Moving {} to {}".format(filePath, destLocation)
		shutil.move(filePath, destLocation)
	else:	
		print "Copying {} to {}".format(filePath, destLocation)
		shutil.copy2(filePath, destLocation)

if __name__ == '__main__':
	inputDir = sys.argv[1]
	outputDir = sys.argv[2]
	iterateFolder(inputDir, outputDir)