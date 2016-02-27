
import datetime
import os

def getDateTaken(file_name, outputFormat="%Y-%m-%d"):
	# Open image file for reading (binary mode)
	timestamp = os.path.getmtime(file_name)

	creationTime = datetime.datetime.fromtimestamp(timestamp)
	
	return datetime.date.strftime(creationTime, outputFormat)