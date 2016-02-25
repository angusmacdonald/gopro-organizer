import wx
import ui

class App(wx.App):
   def OnInit(self):
		self.SetAppName("Test_Tip")

		frame = OrganizerUi(None, -1, "Test show tip at start up")
		frame.Show(True)
		self.SetTopWindow(frame)

		if os.path.exists("tips.txt"):
			wx.CallAfter(frame.show_tip)

		return True