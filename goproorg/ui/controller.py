import sys
sys.path.append('goproorg')
from org import settings

import wx
from wx.lib.pubsub import pub
import view
import model

class OrganizerController:
	def __init__(self, app, appName):
		self.model = model.OrganizerModel() #Todo Make organizer class

		pub.subscribe(self.ActionProcessed, "STATUS UPDATE")

		#set up the first frame which displays the current Model value
		self.view = view.OrganizerView(None, title=appName)
		self.view.btnStartOrganizing.Bind(wx.EVT_BUTTON, self.StartOrganizing)

		self.view.Show()

	def StartOrganizing(self, evt):
		pub.sendMessage("STATUS UPDATE", message="Beginning processing...")

		sett = settings.OrganizerSettings()

		sett.setMoveFile(not self.view.chkCopyFiles.IsChecked())

		sett.setIncludeMeta(self.view.chkIncludeThmLrv.IsChecked())
		sett.setStoreByDateTaken(self.view.chkDateSubDirs.IsChecked())

		self.model.startProcessing(self.view.inputPathText.GetValue(), 
			self.view.outputPathText.GetValue(), sett)
		pub.sendMessage("STATUS UPDATE", message="Finished processing...")
		
		
	def ActionProcessed(self, message):
		self.view.AddMessage(message)


if __name__ == '__main__':
	appName = "GoPro Organizer"
	app = wx.App()
	app.SetAppName(appName) # Used in OSx app menu
	OrganizerController(app, appName)
	app.MainLoop()