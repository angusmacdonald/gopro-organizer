
import datetime
import os

def getDateTaken(fileName, outputFormat="%Y-%m-%d"):
	# Open image file for reading (binary mode)
	timestamp = os.path.getmtime(fileName)

	creationTime = datetime.datetime.fromtimestamp(timestamp)
	
	return datetime.date.strftime(creationTime, outputFormat)