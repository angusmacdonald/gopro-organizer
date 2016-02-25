import organizer

class OrganizerModel:

    def startProcessing(self, inputDir, outputDir):
        organizer.processGoProDirectory(inputDir, outputDir)
