from configobj import ConfigObj

config = ConfigObj("default.conf", unrepr=True)

class OrganizerSettings:
	def __init__(self):
		self.moveFile = config['move']
		self.includeMeta = config['includeThmAndLrvFiles']
		self.storeByDateTaken = config['storeByDateTaken']
		self.fileNamingFormat = config['dateNamingFormat']
		self.useCustomNamingFormat = config['useCustomNamingFormat']

	def setMoveFile(self, move):
		self.moveFile = move

	def setIncludeMeta(self, includeMeta):
		self.includeMeta = includeMeta

	def setStoreByDateTaken(self, storeByDateTaken):
		self.storeByDateTaken = storeByDateTaken

	def setUseCustomNamingFormat(self, useCustomNamingFormat):
		self.useCustomNamingFormat = useCustomNamingFormat

	def setFileNamingFormat(self, fileNamingFormat):
		self.fileNamingFormat = fileNamingFormat