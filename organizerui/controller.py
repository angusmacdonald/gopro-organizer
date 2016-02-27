import sys
sys.path.append('')
from organizercore import settings

import wx
from wx.lib.pubsub import pub
import view
import model

class OrganizerController:
	def __init__(self, app, appName):
		self.model = model.OrganizerModel() #Todo Make organizer class

		pub.subscribe(self.action_processed, "STATUS UPDATE")

		#set up the first frame which displays the current Model value
		self.view = view.OrganizerView(None, title=appName)
		self.view.btnStartOrganizing.Bind(wx.EVT_BUTTON, self.start_organizing)

		self.view.Show()

	def start_organizing(self, evt):
		pub.sendMessage("STATUS UPDATE", message="Beginning processing...")

		sett = settings.OrganizerSettings()

		sett.set_move_file(not self.view.chkCopyFiles.IsChecked())

		sett.set_include_meta(self.view.chkIncludeThmLrv.IsChecked())
		sett.set_store_by_date_taken(self.view.chkDateSubDirs.IsChecked())

		sett.set_use_custom_naming_format(self.view.chkChangeFileNameFormat.IsChecked())
		sett.set_custom_naming_format(self.view.fileNameFormat.GetValue())

		self.model.start_processing(self.view.inputPathText.GetValue(), 
			self.view.outputPathText.GetValue(), sett)
		pub.sendMessage("STATUS UPDATE", message="Finished processing...")
		
		
	def action_processed(self, message):
		self.view.AddMessage(message)


if __name__ == '__main__':
	appName = "GoPro Organizer"
	app = wx.App()
	app.SetAppName(appName) # Used in OSx app menu
	OrganizerController(app, appName)
	app.MainLoop()