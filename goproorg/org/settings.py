from configobj import ConfigObj

config = ConfigObj("default.conf", unrepr=True)

class OrganizerSettings:
	def __init__(self):
		self.moveFile = config['move']
		self.includeMeta = config['includeThmAndLrvFiles']

	def setMoveFile(self, move):
		self.moveFile = move

	def setIncludeMeta(self, includeMeta):
		self.includeMeta = includeMeta