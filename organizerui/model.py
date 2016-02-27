import sys
sys.path.append('')

from organizercore import organizer

class OrganizerModel:

    def start_processing(self, input_dir, output_dir, settings):
        organizer.Organizer(settings).process_gopro_dir(input_dir, output_dir)
