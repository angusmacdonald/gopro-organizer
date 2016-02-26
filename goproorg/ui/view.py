import wx
from os.path import expanduser
import logging


class OrganizerView(wx.Frame):
  
	def __init__(self, parent, title):
		super(OrganizerView, self).__init__(parent, title=title, 
			size=(390, 590))
			
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
  		fontItalic = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
  		fontItalic = fontItalic.MakeItalic()
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Input

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

		explainer1 = self.createExplainerLine(panel, fontItalic, 
			'\tThe path to the directory containing DCIM sub-directories.')
		vbox.Add(explainer1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=3)

		vbox.Add((-1, 10))

		# Output


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
		
		explainer2 = self.createExplainerLine(panel, fontItalic, 
			'\tWhere files will be copied. This directory will contain date sub-dirs.')
	
		vbox.Add(explainer2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=3)


		vbox.Add((-1, 10))

		# Options

		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkIncludeThmLrv = wx.CheckBox(panel, label='Include THM and LRV Files. They are ignored if unchecked.')
		self.chkIncludeThmLrv.SetFont(font)
		self.chkIncludeThmLrv.SetValue(True)
		hbox4.Add(self.chkIncludeThmLrv)

		vbox.Add(hbox4, flag=wx.LEFT, border=10)

		hbox45 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkCopyFiles = wx.CheckBox(panel, 
			label='Copy, leaving existing files untouched. They are deleted if unchecked.')
		self.chkCopyFiles.SetFont(font)
		self.chkCopyFiles.SetValue(True)
		hbox45.Add(self.chkCopyFiles, flag=wx.LEFT, border=10)
		
		vbox.Add(hbox45, flag=wx.LEFT, border=10)



		hbox46 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkDateSubDirs = wx.CheckBox(panel, 
			label='Store items in sub-directories by date taken.')
		self.chkDateSubDirs.SetFont(font)
		self.chkDateSubDirs.SetValue(True)
		hbox46.Add(self.chkDateSubDirs, flag=wx.LEFT, border=10)
		
		vbox.Add(hbox46, flag=wx.LEFT, border=10)



		vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		self.btnStartOrganizing = wx.Button(panel, label='Start Organizing', size=(400, 30))
		hbox5.Add(self.btnStartOrganizing)
		vbox.Add(hbox5, flag=wx.EXPAND, border=1)



		# Status Box

		hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		self.statusUpdates = wx.TextCtrl(panel, -1,"Waiting for input...\n", 
			size=(400, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)
		hbox6.Add(self.statusUpdates)
		vbox.Add(hbox6, flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT|wx.EXPAND, border=1)


		panel.SetSizer(vbox)

		
		btnInputDir.Bind(wx.EVT_BUTTON, self.OnInputPathDir)
		btnOutputDir.Bind(wx.EVT_BUTTON, self.OnOutputPathDir)

	def createExplainerLine(self, panel, font, label_text):
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		
		self.inputDescriptionLabel = wx.StaticText(panel, label=label_text)
		self.inputDescriptionLabel.SetFont(font)
		
		hbox.Add(self.inputDescriptionLabel, flag=wx.RIGHT|wx.EXPAND, border=8)
		
		return hbox
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

	def AddMessage(self, message):
		logging.debug("Incoming message: {}".format(message))

		newStatus = "{}\n".format(message)

		self.statusUpdates.AppendText(newStatus)
		self.statusUpdates.Refresh()


	def OnClose(self, event):
		self.Close()

if __name__ == '__main__':
	appName = "GoPro Organizer"
	app = wx.App()
	app.SetAppName(appName) # Used in OSx app menu
	OrganizerView(None, title=appName)
	app.MainLoop()