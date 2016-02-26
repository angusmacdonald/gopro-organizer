
import datetime
import os

def getDateTaken(fileName):
	# Open image file for reading (binary mode)
	timestamp = os.path.getmtime(fileName)

	creationTime = datetime.date.fromtimestamp(timestamp)
	
	return datetime.date.strftime(creationTime, "%Y-%m-%d")