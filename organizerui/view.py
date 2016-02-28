import wx
from os.path import expanduser
import logging

from configobj import ConfigObj
config = ConfigObj("default.conf", unrepr=True)

class OrganizerView(wx.Frame):
  
	def __init__(self, parent, title):
		super(OrganizerView, self).__init__(parent, title=title, 
			size=(400, 530))
			
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
  		self.fontHeading = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
  		self.fontHeading.SetPointSize(20)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Heading 1
		heading1 = self.createHeading(panel, 'Media Location')
		vbox.Add(heading1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		

		# Input

		self.inputPathLabel = wx.StaticText(panel, label='Input Directory    ')
		self.inputPathLabel.SetToolTip(
			wx.ToolTip('All GoPro photos in this directory and all sub-directories will be copied.'))
		self.inputPathLabel.SetFont(font)
		self.inputPathText = wx.TextCtrl(panel)
		self.inputPathText.SetValue(expanduser("~"))
		btnInputDir = wx.Button(panel, label='...', size=(40, 20))
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		
		hbox1.Add(self.inputPathLabel, flag=wx.RIGHT, border=8)
		hbox1.Add(self.inputPathText, proportion=1, border=8)
		hbox1.Add(btnInputDir, flag=wx.LEFT|wx.RIGHT, border=10)

		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		# Output

		self.outputPath = wx.StaticText(panel, label='Output Directory')
		self.outputPath.SetFont(font)
		self.outputPath.SetToolTip(
			wx.ToolTip('Where all GoPro photos will be moved/copied.'))
		
		self.outputPathText = wx.TextCtrl(panel)
		self.outputPathText.SetValue(expanduser("~"))
		btnOutputDir = wx.Button(panel, label='...', size=(40, 20))
		
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2.Add(self.outputPath, flag=wx.RIGHT, border=8)
		hbox2.Add(self.outputPathText, proportion=1, flag=wx.RIGHT)
		
		hbox2.Add(btnOutputDir,flag=wx.LEFT|wx.RIGHT, border=10)

		vbox.Add(hbox2, flag=wx.LEFT | wx.TOP | wx.RIGHT | wx.EXPAND, border=10)
		

		# Start button
		
		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		self.btnStartOrganizing = wx.Button(panel, label='Start Organizing', size=(400, 30))
		hbox5.Add(self.btnStartOrganizing)
		vbox.Add(hbox5, flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)

		
		# Options
		vbox.Add(self.createHeading(panel, 'Settings'), 
			flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)
		
		# Include THM and LRV files
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkIncludeThmLrv = wx.CheckBox(panel, label='Include THM and LRV Files.')
		self.chkIncludeThmLrv.SetFont(font)
		self.chkIncludeThmLrv.SetValue(True)
		hbox4.Add(self.chkIncludeThmLrv)

		vbox.Add(hbox4, flag=wx.LEFT, border=10)

		# Copy or move?
		hbox45 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkCopyFiles = wx.CheckBox(panel, 
			label='Copy files (move files if unchecked).')
		self.chkCopyFiles.SetFont(font)
		self.chkCopyFiles.SetValue(True)
		hbox45.Add(self.chkCopyFiles)
		
		vbox.Add(hbox45, flag=wx.LEFT, border=10)

		# Store in date sub-directory option:
		hbox46 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkDateSubDirs = wx.CheckBox(panel, 
			label='Store items in sub-directories named by date taken.')
		self.chkDateSubDirs.SetFont(font)
		self.chkDateSubDirs.SetValue(True)
		hbox46.Add(self.chkDateSubDirs)
		
		vbox.Add(hbox46, flag=wx.LEFT, border=10)

		# Rename files option:
		hbox47 = wx.BoxSizer(wx.HORIZONTAL)
		self.chkChangeFileNameFormat = wx.CheckBox(panel, 
			label='Rename files to the following date format:')
		self.chkChangeFileNameFormat.SetToolTip(
			wx.ToolTip('The format of this pattern is described in the supplied documentation.'))
		self.chkChangeFileNameFormat.SetFont(font)
		self.chkChangeFileNameFormat.SetValue(False)
		hbox47.Add(self.chkChangeFileNameFormat)
		
		vbox.Add(hbox47, flag=wx.LEFT, border=10)

		# Date regex for file naming:
		hbox48 = wx.BoxSizer(wx.HORIZONTAL)
		self.fileNameFormat = wx.TextCtrl(panel)
		self.fileNameFormat.Enable(False)
		self.fileNameFormat.SetValue(config['date_naming_format'])
		hbox48.Add(self.fileNameFormat, proportion=1, border=8)
		
		vbox.Add(hbox48, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=30)



		# Status Box
		vbox.Add(self.createHeading(panel, 'Status'), 
			flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		
		hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		self.statusUpdates = wx.TextCtrl(panel, -1,"Waiting for input...\n", 
			size=(400, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)
		hbox6.Add(self.statusUpdates)
		vbox.Add(hbox6, flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT|wx.EXPAND, border=10)


		panel.SetSizer(vbox)

		self.chkCopyFiles.Bind(wx.EVT_CHECKBOX, self.OnChkCopyFile)
		self.chkChangeFileNameFormat.Bind(wx.EVT_CHECKBOX, self.OnChkFileNameFormat)
		btnInputDir.Bind(wx.EVT_BUTTON, self.OnInputPathDir)
		btnOutputDir.Bind(wx.EVT_BUTTON, self.OnOutputPathDir)

	def createHeading(self, panel, headingText):
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		pathHeading = wx.StaticText(panel, label=headingText)
		pathHeading.SetFont(self.fontHeading)
		hbox.Add(pathHeading, flag=wx.RIGHT|wx.EXPAND, border=0)

		return hbox

	def createExplainerLine(self, panel, font, label_text):
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		
		self.inputDescriptionLabel = wx.StaticText(panel, label=label_text)
		self.inputDescriptionLabel.SetFont(font)
		
		hbox.Add(self.inputDescriptionLabel, flag=wx.RIGHT|wx.EXPAND, border=8)
		
		return hbox


	def OnChkCopyFile(self, event):
		if not event.IsChecked():
			dial = wx.MessageDialog(None, 
				'Are you sure? Disabling copy means that files are removed from their source location.', 'Disable copy?', 
				wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
			retCode = dial.ShowModal()

			if (retCode != wx.ID_YES):
				self.chkCopyFiles.SetValue(True)
			
			dial.Destroy()

	def OnChkFileNameFormat(self, event):
		self.fileNameFormat.Enable(event.IsChecked())

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