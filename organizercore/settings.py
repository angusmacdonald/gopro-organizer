from configobj import ConfigObj

config = ConfigObj("default.conf", unrepr=True)

class OrganizerSettings:
	def __init__(self):
		self.move_file = config['move']
		self.include_meta = config['include_thm_lrv_files']
		self.store_by_date_taken = config['store_by_date_taken']
		self.file_naming_format = config['date_naming_format']
		self.use_custom_naming_format = config['use_custom_naming_format']

	def set_move_file(self, move):
		self.move_file = move

	def set_include_meta(self, include_meta):
		self.include_meta = include_meta

	def set_store_by_date_taken(self, store_by_date_taken):
		self.store_by_date_taken = store_by_date_taken

	def set_use_custom_naming_format(self, use_custom_naming_format):
		self.use_custom_naming_format = use_custom_naming_format

	def set_custom_naming_format(self, file_naming_format):
		self.file_naming_format = file_naming_format