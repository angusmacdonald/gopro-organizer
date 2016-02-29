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
	""" Main class, finds and moves/copies photos as specified in settings.

		The class is initialized with settings that define how the move will
		take place, and the process_gopro_dir() starts the action on a
		specified set of input and output directories.
	"""

	def __init__(self, sett = settings.OrganizerSettings()):
		"""
			Arguments:
				sett (settings): Config settings related to the processing
					of the directory.
		"""
		
		self.settings = sett

	def process_gopro_dir(self, input_dir, output_dir):
		"""
			Find all the appropriate files in the input directory and
			move/copy them to the output directory.

			Arguments:
				input_dir (str): path to the directory containing GoPro DCIM dirs.
				output_dir (str): path to the directory where results will be stored.

			Returns: The number of files successfully processed.
		"""

		if in_directory(output_dir, input_dir):
			pub.sendMessage("STATUS UPDATE", 
				message="ERROR: The output directory cannot be a sub-directory of the input directory.")			
			return 0

		if not os.path.exists(input_dir):
			pub.sendMessage("STATUS UPDATE", 
				message="ERROR: The input directory does not exist.")			
			return 0

		abs_input_path = os.path.abspath(input_dir)
		abs_output_dir = os.path.abspath(output_dir)

		return self._process_files(abs_input_path, abs_output_dir)

	def _process_files(self, input_dir, output_dir):
		files_processed = 0

		for root, directories, filenames in os.walk(input_dir):
			for filename in filenames: 
				full_file_path = os.path.join(root,filename) 
				files_processed += self._process_single_file(filename, full_file_path, output_dir)

		return files_processed

	def _process_single_file(self, filename, full_file_path, root_output_dir):
		"""
			Analyze the specified file to determine if it matches a pattern that
			should be moved, and move the file if so.

			Returns: 1 if the file was moved, 0 if it was not.
		"""

		sub_directory = file_matcher.determine_destination(filename, self._get_file_naming_patterns())
		
		if sub_directory:
			# If we know where to move this file, move it
			action = "Moving" if self.settings.move_file else "Copying"
			logging.debug("{} '{}' to '{}'".format(action, filename, sub_directory))
			pub.sendMessage("STATUS UPDATE", 
				message="{} '{}' to '{}'".format(action, filename, sub_directory))
		
			dest_dir = self._get_dest_path(full_file_path, root_output_dir, sub_directory)
			
			newFileName = self._get_new_filename(full_file_path, dest_dir)

			self._move_file_to_dir(dest_dir, full_file_path, newFileName)
			return 1
		else:
			# This file type is not recognized so it is ignored
			logging.info("Filename format not recognized: {}".format(filename))
			pub.sendMessage("STATUS UPDATE", 
				message="Ignoring '{}'".format(filename))
			return 0

	def _get_dest_path(self, full_file_path, root_output_dir, sub_directory):
		date_taken = photoinfo.getDateTaken(full_file_path)
		
		if self.settings.store_by_date_taken:
			return os.path.join(root_output_dir, date_taken, sub_directory)
		else :
			return os.path.join(root_output_dir, sub_directory)

	def _get_new_filename(self, full_file_path, dest_dir):
		if self.settings.use_custom_naming_format:
			customFormat = self.settings.file_naming_format
			filename, file_extension = os.path.splitext(full_file_path)
			
			date_taken = photoinfo.getDateTaken(full_file_path, customFormat)
			new_file_path = "{}{}".format(date_taken, file_extension)

			# Ensure file name is unique (add number to end to make unique if not):
			count = 1
			while True:
				fullPathOfNewFile = abs_input_path = os.path.join(dest_dir, new_file_path)
				logging.debug("Checking if file exists: {}".format(fullPathOfNewFile))
				
				if not os.path.isfile(fullPathOfNewFile):
					logging.debug("File does not exist: {}".format(fullPathOfNewFile))
					break

				new_file_path = "{}_{}{}".format(date_taken, count, file_extension)
				count += 1

			return new_file_path
		else:
			return os.path.basename(full_file_path)



	def _get_file_naming_patterns(self):
		patterns = file_matcher.default_patterns()
		
		if (self.settings.include_meta):
			patterns['GOPR\d\d\d\d\.[THM|LRV]'] = VIDEOS

		return patterns

	def _move_file_to_dir(self, dest_dir, src_file, file_name):

		if not os.path.exists(dest_dir):
			os.makedirs(dest_dir)
		
		dest_file_path = os.path.join(dest_dir, file_name)

		move_file = self.settings.move_file

		logging.debug("Moving ({}) '{}'' to '{}'".format(move_file, dest_file_path, dest_file_path))

		if move_file:
			shutil.move(src_file, dest_file_path)
		else:	
			shutil.copy2(src_file, dest_file_path)


def in_directory(file, directory):
    # http://stackoverflow.com/q/3812849
    directory = os.path.join(os.path.realpath(directory), '')
    file = os.path.realpath(file)

    #return true, if the common prefix of both is equal to directory
    #e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
    return os.path.commonprefix([file, directory]) == directory

if __name__ == '__main__':
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	iterateFolder(input_dir, output_dir)