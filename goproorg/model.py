import organizer

class OrganizerModel:

    def startProcessing(self, inputDir, outputDir, settings):
        organizer.Organizer(settings).processGoProDirectory(inputDir, outputDir)
