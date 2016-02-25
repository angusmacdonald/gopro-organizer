import wx
from os.path import expanduser

import organizer

class OrganizerUi(wx.Frame):
  
	def __init__(self, parent, title):
		super(OrganizerUi, self).__init__(parent, title=title, 
			size=(390, 190))
			
		self.InitUI()
		self.Centre()
		self.Show()     
		
	def InitUI(self):
	
		panel = wx.Panel(self)

		# Menu
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		self.SetMenuBar(menubar)
		
		self.Bind(wx.EVT_MENU, self.OnClose, fitem)

		# Main Body

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
  
		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.inputPathLabel = wx.StaticText(panel, label='Path to GoPro Files')
		self.inputPathLabel.SetFont(font)
		hbox1.Add(self.inputPathLabel, flag=wx.RIGHT|wx.EXPAND, border=8)
		self.inputPathText = wx.TextCtrl(panel)
		self.inputPathText.SetValue(expanduser("~"))
		hbox1.Add(self.inputPathText, proportion=1, border=8)
		
		btnInputDir = wx.Button(panel, label='...', size=(40, 20))
		hbox1.Add(btnInputDir, border=8)

		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.outputPath = wx.StaticText(panel, label='Output Path')
		self.outputPath.SetFont(font)
		hbox2.Add(self.outputPath, flag=wx.RIGHT, border=8)
		self.outputPathText = wx.TextCtrl(panel)
		self.outputPathText.SetValue(expanduser("~"))
		hbox2.Add(self.outputPathText, proportion=1)
		
		btnOutputDir = wx.Button(panel, label='...', size=(40, 20))
		hbox2.Add(btnOutputDir)

		vbox.Add(hbox2, flag=wx.LEFT | wx.TOP | wx.RIGHT | wx.EXPAND, border=10)
		
		vbox.Add((-1, 10))


		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkIncludeThmLrv = wx.CheckBox(panel, label='Include THM and LRV Files')
		self.chkIncludeThmLrv.SetFont(font)
		self.chkIncludeThmLrv.SetValue(True)
		hbox4.Add(self.chkIncludeThmLrv)
		self.chkCopyFiles = wx.CheckBox(panel, label='Copy')
		self.chkCopyFiles.SetFont(font)
		self.chkCopyFiles.SetValue(True)
		hbox4.Add(self.chkCopyFiles, flag=wx.LEFT, border=10)
		self.chkRenameToDate = wx.CheckBox(panel, label='Rename to Date Taken')
		self.chkRenameToDate.SetFont(font)
		hbox4.Add(self.chkRenameToDate, flag=wx.LEFT, border=10)
		vbox.Add(hbox4, flag=wx.LEFT, border=10)

		vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		btnStartOrganizing = wx.Button(panel, label='Start Organizing', size=(170, 30))
		hbox5.Add(btnStartOrganizing)
		btnClose = wx.Button(panel, label='Close', size=(70, 30))
		hbox5.Add(btnClose, flag=wx.LEFT|wx.BOTTOM, border=5)
		vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=1)

		panel.SetSizer(vbox)

		btnStartOrganizing.Bind(wx.EVT_BUTTON, self.OnStartOrganizing)
		btnClose.Bind(wx.EVT_BUTTON, self.OnClose)
		btnInputDir.Bind(wx.EVT_BUTTON, self.OnInputPathDir)
		btnOutputDir.Bind(wx.EVT_BUTTON, self.OnOutputPathDir)

	def OnInputPathDir(self, event):
		text = "Choose the directory containing DCIM files:"
		dir = self.chooseDirectory(text)

		self.inputPathText.SetValue(dir)

	def OnOutputPathDir(self, event):
		text = "Choose the directory where your organized photos will be stored:"
		dir = self.chooseDirectory(text)

		self.outputPathText.SetValue(dir)

		
	def chooseDirectory(self, text):
		response = ""

		dialog = wx.DirDialog(None, text,style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
		if dialog.ShowModal() == wx.ID_OK:
			response = dialog.GetPath()
		dialog.Destroy()

		return response

	def OnStartOrganizing(self,event):
		print self.inputPathText.GetValue()
		print self.outputPathText.GetValue()
		print self.chkIncludeThmLrv.IsChecked()
		print self.chkCopyFiles.IsChecked()
		print self.chkRenameToDate.IsChecked()

		organizer.iterateFolder(self.inputPathText.GetValue(), self.outputPathText.GetValue())

	def OnClose(self, event):
		self.Close()

if __name__ == '__main__':
  	appName = "GoPro Organizer"
	app = wx.App()
	app.SetAppName(appName) # Used in OSx app menu
	OrganizerUi(None, title=appName)
	app.MainLoop()