#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         FilesPanel.py
# Purpose:      Panel with files to be encoded.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: FilesPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Encoder
import ConfigurationManager
import Previewer
import AddVcdDialog
import AddDvdDialog

import wx
import os

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, wxID_PANEL1BUTTON3, 
 wxID_PANEL1CHOICE1, wxID_PANEL1LISTCTRL1, wxID_PANEL1STATICTEXT1, 
 wxID_PANEL1STATICTEXT2, wxID_PANEL1BUTTON4, wxID_PANEL1CHOICE2,
 wxID_PANEL1BUTTON5, wxID_PANEL1BUTTON6, wxID_PANEL1BUTTON7, 
 wxID_PANEL1BUTTON8, wxID_PANEL1BUTTON9
] = [wx.NewId() for _init_ctrls in range(15)]

class FilesPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.listCtrl1, (1, 1), border=0, flag=wx.EXPAND,
              span=(5, 6))
        parent.AddWindow(self.button1, (1, 8), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button2, (2, 8), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button8, (3, 8), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button4, (4, 8), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.staticText1, (7, 5), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.AddWindow(self.staticText2, (7, 2), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.AddWindow(self.button3, (9, 1), border=0, flag=wx.EXPAND,
              span=(1, 6))
        parent.AddWindow(self.choice1, (7, 6), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.choice2, (7, 3), border=0, flag=0, span=(1, 1))
        parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(565, 300))

        self.listCtrl1 = wx.ListCtrl(id=wxID_PANEL1LISTCTRL1, name='listCtrl1',
              parent=self, style=wx.LC_REPORT, size=(350, 130))

        self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=_(u'Add Media'),
              name='button1', parent=self, style=0, size=(130, 35))

        self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=_(u'Delete Media'),
              name='button2', parent=self, style=0, size=(130, 35))
              
        self.button4 = wx.Button(id=wxID_PANEL1BUTTON4, label=_(u'Preview'),
              name='button4', parent=self, style=0, size=(130, 35))

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_(u'Quality')+' ', name='staticText1', parent=self, style=0)
              
        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_(u'DPG Version')+' ', name='staticText2', parent=self, 
              style=0)

        self.button3 = wx.Button(id=wxID_PANEL1BUTTON3, 
              label=_(u'Start Encoding'), name='button3', parent=self, 
              size=(350, 50), style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)
              
        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)
              
        self.button5 = wx.Button(id=wxID_PANEL1BUTTON5, label=_(u'Add File'),
              name='button5', parent=self, style=0, size=(130, 35))
              
        self.button6 = wx.Button(id=wxID_PANEL1BUTTON6, label=_(u'Add DVD'),
              name='button6', parent=self, style=0, size=(130, 35))
              
        self.button7 = wx.Button(id=wxID_PANEL1BUTTON7, label=_(u'Add VCD'),
              name='button7', parent=self, style=0, size=(130, 35))
              
        self.button8 = wx.Button(id=wxID_PANEL1BUTTON8, label=_(u'Play Media'),
              name='button8', parent=self, style=0, size=(130, 35))
              
        self.button9 = wx.Button(id=wxID_PANEL1BUTTON9, label=_(u'Cancel'),
              name='button9', parent=self, style=0, size=(130, 35))

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Path for the last added file
        self.lastFilePath = ''
        
        # Init version choice
        self.choice2.Append(u'0',0)
        self.choice2.Append(u'1',1)
        self.choice2.Append(u'2',2)
        self.choice2.Append(u'3',3)
        self.choice2.Append(u'4',4)
        self.choice2.Select(Globals.dpg_version)
        
        # Init quality choice
        self.choice1.Append(_(u'Low'),'low')
        self.choice1.Append(_(u'Normal'),'normal')
        self.choice1.Append(_(u'High'),'high')
        self.choice1.Append(_(u'Extra High'),'doublepass')
        if Globals.dpg_quality == 'low':
            self.choice1.Select(0)
        elif Globals.dpg_quality == 'normal':
            self.choice1.Select(1)
        elif Globals.dpg_quality == 'high':
            self.choice1.Select(2)
        elif Globals.dpg_quality == 'doublepass':
            self.choice1.Select(3)
        
        # Init list control
        self.listCtrl1.InsertColumn(0,_(u'Media sources to encode'))
        self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        
        # Hide the add-media buttons (will be shown later)
        self.button5.Show(False)
        self.button6.Show(False)
        self.button7.Show(False)
        self.button9.Show(False)
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_PANEL1BUTTON1, self.addMedia)
        wx.EVT_BUTTON(self.button2, wxID_PANEL1BUTTON2, self.deleteMedia)
        wx.EVT_BUTTON(self.button4, wxID_PANEL1BUTTON4, self.previewMedia)
        wx.EVT_BUTTON(self.button3, wxID_PANEL1BUTTON3, self.startEncoding)
        wx.EVT_CHOICE(self.choice2, wxID_PANEL1CHOICE2, self.changeDPGLevel)
        wx.EVT_CHOICE(self.choice1, wxID_PANEL1CHOICE1, self.changeQuality)
        wx.EVT_BUTTON(self.button5, wxID_PANEL1BUTTON5, self.addFile)
        wx.EVT_BUTTON(self.button6, wxID_PANEL1BUTTON6, self.addDvd)
        wx.EVT_BUTTON(self.button7, wxID_PANEL1BUTTON7, self.addVcd)
        wx.EVT_BUTTON(self.button8, wxID_PANEL1BUTTON8, self.playMedia)
        wx.EVT_BUTTON(self.button9, wxID_PANEL1BUTTON9, self.restoreMenu)
        
        # Drop files
        class FileDropTarget(wx.FileDropTarget):
            def setFilesPanel(self, filesPanel):
                self.filesPanel = filesPanel
            def OnDropFiles(self, x, y, filenames):
                return self.filesPanel.dropFiles(filenames)
        fileDropTarget = FileDropTarget()
        fileDropTarget.setFilesPanel(self)
        self.listCtrl1.SetDropTarget(fileDropTarget)
        
    def addMedia(self, event):
        "Enable the buttons to add files, dvd and vcd"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Hide the main buttons
        self.button1.Show(False)
        self.button2.Show(False)
        self.button4.Show(False)
        self.button8.Show(False)
        # Show the add-media buttons
        self.button5.Show(True)
        self.button6.Show(True)
        self.button7.Show(True)
        self.button9.Show(True)
        # Replace the buttons in the layout
        self.gridBagSizer1.Replace(self.button1, self.button5)
        self.gridBagSizer1.Replace(self.button2, self.button6)
        self.gridBagSizer1.Replace(self.button4, self.button9)
        self.gridBagSizer1.Replace(self.button8, self.button7)
        self.gridBagSizer1.Layout()
        
    def restoreMenu(self, event):
        "Restores the changes made by the addMedia button"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Hide the add-media buttons
        self.button5.Show(False)
        self.button6.Show(False)
        self.button7.Show(False)
        self.button9.Show(False)
        # Show the main buttons
        self.button1.Show(True)
        self.button2.Show(True)
        self.button4.Show(True)
        self.button8.Show(True)
        # Replace the buttons in the layout
        self.gridBagSizer1.Replace(self.button5, self.button1)
        self.gridBagSizer1.Replace(self.button6, self.button2)
        self.gridBagSizer1.Replace(self.button9, self.button4)
        self.gridBagSizer1.Replace(self.button7, self.button8)
        self.gridBagSizer1.Layout()

    def addFile(self, event):
        "Add a file (or more) to the input media list"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Open a file dialog
        fileDialog = wx.FileDialog(self, _(u'Select the files to be encoded'), 
            defaultDir=self.lastFilePath, 
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | 
                  wx.FD_MULTIPLE | wx.FD_PREVIEW)
        if fileDialog.ShowModal() == wx.ID_OK:
            # Add the selected files to the list
            files = fileDialog.GetPaths()
            for file in files:
                # Avoid duplicated items
                if self.listCtrl1.FindItem(-1, file) == -1:
                    index = self.listCtrl1.GetItemCount()
                    self.listCtrl1.InsertStringItem(index, file)
                    self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)
                # Remember the last path
                self.lastFilePath = os.path.dirname(file)
        fileDialog.Destroy()
        # Restore the menu
        self.restoreMenu(None)
        
    def addDvd(self, event):
        "Add a Dvd to the input media list"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Show the Vcd Dialog
        dialog = AddDvdDialog.AddDvdDialog(self)
        value = dialog.ShowModal()
        if value == wx.ID_OK:
            device = dialog.getDevice()
            track = dialog.getTrack()
            chapter = dialog.getChapter()
            if chapter:
                url = 'dvd://' + track + ' -chapter ' + chapter + ' -dvd-device ' + device
            else:
                url = 'dvd://' + track + ' -dvd-device ' + device
            # Add the media source to the list
            # Avoid duplicated items
            if self.listCtrl1.FindItem(-1, url) == -1:
                index = self.listCtrl1.GetItemCount()
                self.listCtrl1.InsertStringItem(index, url)
                self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        dialog.Destroy()
        # Restore the menu
        self.restoreMenu(None)
        
    def addVcd(self, event):
        "Add a Vcd to the input media list"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Show the Vcd Dialog
        dialog = AddVcdDialog.AddVcdDialog(self)
        value = dialog.ShowModal()
        if value == wx.ID_OK:
            device = dialog.getDevice()
            track = dialog.getTrack()
            url = 'vcd://' + track + ' -cdrom-device ' + device
            # Add the media source to the list
            # Avoid duplicated items
            if self.listCtrl1.FindItem(-1, url) == -1:
                index = self.listCtrl1.GetItemCount()
                self.listCtrl1.InsertStringItem(index, url)
                self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        dialog.Destroy()
        # Restore the menu
        self.restoreMenu(None)
        
    def deleteMedia(self, event):
        "Delete the selected media sources from the list"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Check if there are media sources selected
        if self.listCtrl1.GetSelectedItemCount() == 0:
            message = _(u'No media sources selected.')
            dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                style=wx.ICON_ERROR)
            dialog.ShowModal()
            return
        # Get the selected items
        selItems = []
        item = self.listCtrl1.GetFirstSelected()
        while item >= 0:
            selItems.append(item)
            item = self.listCtrl1.GetNextSelected(item)
        # Delete them in reverse order
        selItems.reverse()
        for item in selItems:
            self.listCtrl1.DeleteItem(item)
            
    def playMedia(self, event):
        "Just play the selected media source"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        try:
            # Allow only one file
            if self.listCtrl1.GetSelectedItemCount() != 1:
                message = _(u'Select one media source.')
                dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                    style=wx.ICON_ERROR)
                dialog.ShowModal()
                return
            # Play the file
            item = self.listCtrl1.GetItemText(self.listCtrl1.GetFirstSelected())
            Previewer.play_files(item)       
        # On error, warn the user
        except Exception, e:
            message = e.message
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                style=wx.ICON_ERROR)
            dialog.ShowModal()
            
    def previewMedia(self, event):
        "Encode and play a preview of the selected media"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        try:
            # Allow only one file
            if self.listCtrl1.GetSelectedItemCount() != 1:
                message = _(u'Select one media source.')
                dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                    style=wx.ICON_ERROR)
                dialog.ShowModal()
                return
            # Get the options from the panels
            Globals.videoPanel.loadOptions()
            Globals.audioPanel.loadOptions()
            Globals.subtitlesPanel.loadOptions()
            Globals.otherPanel.loadOptions(None)
            # Save the options to the config file
            ConfigurationManager.saveConfiguration()
            # Preview the file
            item = self.listCtrl1.GetItemText(self.listCtrl1.GetFirstSelected())
            Previewer.preview_files(item)       
        # On error, warn the user
        except Exception, e:
            message = e.message
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                style=wx.ICON_ERROR)
            dialog.ShowModal()
        
    def changeDPGLevel(self, event):
        "Update the GUI when the dpg level changes"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        version = event.GetClientData()
        
        # Only mono audio for DPG0
        if (version == 0):
            Globals.audioPanel.checkBox2.Enable(False)
        else:
            Globals.audioPanel.checkBox2.Enable(True)
        
        # Only DPG4 uses thumbnails
        if (version == 4):
            Globals.otherPanel.textCtrl3.Enable(True)
            Globals.otherPanel.button3.Enable(True)
        else:
            Globals.otherPanel.textCtrl3.Enable(False)
            Globals.otherPanel.button3.Enable(False)
            
        # OGG can be used only with DPG3 or better
        oldSelection = Globals.audioPanel.choice1.GetSelection()
        if version>2 and Globals.audioPanel.choice1.GetCount()<3:
            Globals.audioPanel.choice1.Append(u'OGG','vorbis')
        elif version<3 and Globals.audioPanel.choice1.GetCount()>2:
            Globals.audioPanel.choice1.Delete(2)
            if oldSelection < 2:
                Globals.audioPanel.choice1.SetSelection(oldSelection)
            else:
                Globals.audioPanel.choice1.SetSelection(1)
        
    def changeQuality(self, event):
        "Update the GUI when the quality level changes"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        quality = event.GetClientData()
        # Mencoder won't work with double pass and fps < 24
        currFPS = Globals.videoPanel.spinCtrl3.GetValue()
        autoFPS = Globals.videoPanel.checkBox2.IsChecked()
        if quality == 'doublepass':
            if (not autoFPS) and (currFPS < 24):
                message = _(u'With extra high quality, the video FPS can ' \
                    u'not be lower than 24. Raising video FPS to 24.')
                Globals.debug(_(u'WARNING') + ': ' + message)
                # Show a dialog to the user
                dialog = wx.MessageDialog(self, message, _(u'WARNING'), 
                    style=wx.ICON_EXCLAMATION)
                dialog.ShowModal()
            # Set the min FPS to 24
            Globals.videoPanel.spinCtrl3.SetRange(24,
                Globals.videoPanel.spinCtrl3.GetMax())
        # With other qualities, we can user lower FPS
        else:
            Globals.videoPanel.spinCtrl3.SetRange(1,
                Globals.videoPanel.spinCtrl3.GetMax())
            # With autoFPS set it back to 15 (default) again
            if autoFPS:
                Globals.videoPanel.spinCtrl3.SetValue(15)
            
    def startEncoding(self, event):
        "Start encoding the selected files"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        try:
            # Check that we have files and we can read them
            files = []
            item = self.listCtrl1.GetNextItem(-1)
            while item >= 0:
                file = self.listCtrl1.GetItemText(item)
                # Can't check DVD and VCD sources
                if not ((file[:6] == 'vcd://') or (file[:6] == 'dvd://')):
                    if os.path.isfile(file) and os.access(file, os.W_OK):
                        files.append(file)
                    # If can not be readed, show error message and exit
                    else:
                        raise Exception(_(u'Can not read file %s.') % file)
                # Always append DVD and VCD
                else:
                    files.append(file)
                item = self.listCtrl1.GetNextItem(item)
            # Show a dialog to the user
            if len(files) < 1:
                raise Exception(_(u'There are no media sources to process.'))
            # Get the options from the files panel
            Globals.dpg_version = self.choice2.GetClientData(
                self.choice2.GetSelection())
            Globals.dpg_quality = self.choice1.GetClientData(
                self.choice1.GetSelection())
            # Get the options from the panels
            Globals.videoPanel.loadOptions()
            Globals.audioPanel.loadOptions()
            Globals.subtitlesPanel.loadOptions()
            Globals.otherPanel.loadOptions(files)
            # Save the options to the config file
            ConfigurationManager.saveConfiguration()
            # Start encoding the files
            Encoder.encode_files(files)
        # On error, warn the user
        except Exception, e:
            message = e.message
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                style=wx.ICON_ERROR)
            dialog.ShowModal()
        
    def dropFiles(self, filenames):
        "One or more files are drop over the file list"
        for file in filenames: 
            # Avoid duplicated items
            if self.listCtrl1.FindItem(-1, file) == -1:
                index = self.listCtrl1.GetItemCount()
                self.listCtrl1.InsertStringItem(index, file)
                self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)

       

