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
import MediaMainFrame
import AddVcdDialog
import AddDvdDialog
from moreControls.OutputTextDialog import OutputTextDialog

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import os

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, wxID_PANEL1BUTTON3, 
 wxID_PANEL1CHOICE1, wxID_PANEL1LISTCTRL1, wxID_PANEL1STATICTEXT1, 
 wxID_PANEL1STATICTEXT2, wxID_PANEL1BUTTON4, wxID_PANEL1CHOICE2,
 wxID_PANEL1BUTTON5, wxID_PANEL1BUTTON6, wxID_PANEL1BUTTON7, 
 wxID_PANEL1BUTTON8, wxID_PANEL1BUTTON9, wxID_PANEL1BUTTON10,
 wxID_PANEL1BUTTON11, wxID_PANEL1BUTTON12, wxID_PANEL2,
 wxID_PANEL1STATICTEXT3
] = [wx.NewId() for _init_ctrls in range(20)]

class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
        ListCtrlAutoWidthMixin.__init__(self)

class FilesPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(20, 1), (0, 0), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.listCtrl1, (1, 1), border=0, flag=wx.EXPAND,
              span=(6, 6))
        parent.AddWindow(self.panel2, (0, 8), border=0, flag=wx.EXPAND, 
              span=(11, 1))
        parent.AddWindow(self.staticText1, (8, 4), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.AddWindow(self.staticText2, (8, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.AddWindow(self.button3, (10, 1), border=0, flag=0,
              span=(1, 6))
        parent.AddWindow(self.choice1, (8, 5), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.choice2, (8, 2), border=0, flag=0, span=(1, 1))
        
    def _init_coll_gridBagSizer2_Items(self, parent):
        # generated method, don't edit
        
        parent.AddWindow(self.button1, (1, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button2, (2, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button10, (3, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        
        parent.AddWindow(self.button8, (5, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button4, (6, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        
        parent.AddWindow(self.staticText3, (8, 1), border=0, 
              flag=wx.ALIGN_CENTER, span=(1, 1))
        parent.AddSpacer(wx.Size(5, 5), (9, 1), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.button11, (10, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        parent.AddWindow(self.button12, (11, 1), border=0, flag=wx.EXPAND, span=(1, 1))
        

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)
        self.gridBagSizer2 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)
        self._init_coll_gridBagSizer2_Items(self.gridBagSizer2)

        self.SetSizer(self.gridBagSizer1)
        self.panel2.SetSizer(self.gridBagSizer2)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)
        
        self.panel2 = wx.Panel(id=wxID_PANEL2, name='', parent=self)

        self.listCtrl1 = CustomListCtrl(id=wxID_PANEL1LISTCTRL1, 
              style= wx.LC_REPORT|wx.BORDER_NONE|wx.LC_HRULES|wx.LC_VRULES,
              parent=self, size=(380, 150))

        self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=_(u'Add Media'),
              name='button1', parent=self.panel2, style=0)

        self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=_(u'Delete Media'),
              name='button2', parent=self.panel2, style=0)
              
        self.button4 = wx.Button(id=wxID_PANEL1BUTTON4, label=_(u'DPG Preview'),
              name='button4', parent=self.panel2, style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_(u'Quality')+' ', name='staticText1', parent=self, style=0)
              
        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_(u'DPG Version')+' ', name='staticText2', parent=self, 
              style=0)
              
        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_(u'Individual Settings'), name='staticText3', 
              parent=self.panel2, style=0)

        self.button3 = wx.Button(id=wxID_PANEL1BUTTON3, 
              label=_(u'Start Encoding'), name='button3', parent=self, 
              size=(350, 50), style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)
              
        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)
              
        self.button5 = wx.Button(id=wxID_PANEL1BUTTON5, label=_(u'Add File'),
              name='button5', parent=self.panel2, style=0)
              
        self.button6 = wx.Button(id=wxID_PANEL1BUTTON6, label=_(u'Add DVD'),
              name='button6', parent=self.panel2, style=0)
              
        self.button7 = wx.Button(id=wxID_PANEL1BUTTON7, label=_(u'Add VCD'),
              name='button7', parent=self.panel2, style=0)
              
        self.button8 = wx.Button(id=wxID_PANEL1BUTTON8, label=_(u'Play Media'),
              name='button8', parent=self.panel2, style=0)
              
        self.button9 = wx.Button(id=wxID_PANEL1BUTTON9, label=_(u'Cancel'),
              name='button9', parent=self.panel2, style=0)
              
        self.button10 = wx.Button(id=wxID_PANEL1BUTTON10, label=_(u'Media Info'),
              name='button10', parent=self.panel2, style=0)
              
        self.button11 = wx.Button(id=wxID_PANEL1BUTTON11, label=_(u'Set'),
              name='button11', parent=self.panel2, style=0)
              
        self.button12 = wx.Button(id=wxID_PANEL1BUTTON12, label=_(u'Delete'),
              name='button12', parent=self.panel2, style=0)

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
        self.listCtrl1.InsertColumn(1,_(u'Indv Settings'), wx.LIST_FORMAT_CENTRE)
        self.listCtrl1.SetColumnWidth(0,300)
        # wx.LIST_AUTOSIZE_USEHEADER defaults to 80 pixels on all platforms
        # but Win32, better to be explicit. setResizeColumn() actually breaks
        # manual resizing on Windows.
        self.listCtrl1.SetColumnWidth(1,80)
        
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
        wx.EVT_BUTTON(self.button10, wxID_PANEL1BUTTON10, self.showMediaInfo)
        wx.EVT_BUTTON(self.button11, wxID_PANEL1BUTTON11, self.showMediaSettings)
        wx.EVT_BUTTON(self.button12, wxID_PANEL1BUTTON12, self.deleteMediaSettings)
        
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
        self.button10.Show(False)
        self.button11.Show(False)
        self.button12.Show(False)
        self.staticText3.Show(False)
        # Show the add-media buttons
        self.button5.Show(True)
        self.button6.Show(True)
        self.button7.Show(True)
        self.button9.Show(True)
        # Replace the buttons in the layout
        self.gridBagSizer2.Replace(self.button1, self.button5)
        self.gridBagSizer2.Replace(self.button2, self.button6)
        self.gridBagSizer2.Replace(self.button10, self.button7)
        self.gridBagSizer2.Replace(self.button8, self.button9)
        # Do not layout the full window to avoid resize
        self.gridBagSizer2.Layout()
        
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
        self.button10.Show(True)
        self.button11.Show(True)
        self.button12.Show(True)
        self.staticText3.Show(True)
        # Replace the buttons in the layout
        self.gridBagSizer2.Replace(self.button5, self.button1)
        self.gridBagSizer2.Replace(self.button6, self.button2)
        self.gridBagSizer2.Replace(self.button7, self.button10)
        self.gridBagSizer2.Replace(self.button9, self.button8)
        self.Layout()

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
                    # Check if a media configuration exists for the file
                    configfile = ConfigurationManager.getMediaConfiguration(file)
                    if os.path.isfile(configfile):
                        self.listCtrl1.SetStringItem(index, 1, _("YES"))
                    else:
                        self.listCtrl1.SetStringItem(index, 1, _("NO"))
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
                # Check if a media configuration exists for the file
                configfile = ConfigurationManager.getMediaConfiguration(url)
                if os.path.isfile(configfile):
                    self.listCtrl1.SetStringItem(index, 1, _("YES"))
                else:
                    self.listCtrl1.SetStringItem(index, 1, _("NO"))
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
                # Check if a media configuration exists for the file
                configfile = ConfigurationManager.getMediaConfiguration(url)
                if os.path.isfile(configfile):
                    self.listCtrl1.SetStringItem(index, 1, _("YES"))
                else:
                    self.listCtrl1.SetStringItem(index, 1, _("NO"))
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
                style=wx.OK|wx.ICON_ERROR)
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
                    style=wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
                return
            # Play the file
            item = self.listCtrl1.GetItemText(self.listCtrl1.GetFirstSelected())
            Previewer.play_files(item)       
        # On error, warn the user
        except Exception, e:
            message = str(e.args[0])
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            #dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
            #    style=wx.OK|wx.ICON_ERROR)
            dialog = OutputTextDialog(self, message, _(u'ERROR'))
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
                    style=wx.OK|wx.ICON_ERROR)
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
            
            # Read options from the media specific config file (if one exists)
            # This allows media specific options to be saved between sessions
            ConfigurationManager.loadConfiguration(item)
            
            Previewer.preview_files(item)       
        # On error, warn the user
        except Exception, e:
            message = str(e.args[0])
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            #dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
            #    style=wx.OK|wx.ICON_ERROR)
            dialog = OutputTextDialog(self, message, _(u'ERROR'))
            dialog.ShowModal()
            
    def showMediaInfo(self, event):
        "Displays information about a media source"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        try:
            # Allow only one file
            if self.listCtrl1.GetSelectedItemCount() != 1:
                message = _(u'Select one media source.')
                dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                    style=wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
                return
            # Preview the file
            item = self.listCtrl1.GetItemText(self.listCtrl1.GetFirstSelected())
            Previewer.show_information(item, self)       
        # On error, warn the user
        except Exception, e:
            message = str(e.args[0])
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            #dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
            #    style=wx.OK|wx.ICON_ERROR)
            dialog = OutputTextDialog(self, message, _(u'ERROR'))
            dialog.ShowModal()
            
    def showMediaSettings(self, event):
        "Allows individual media settings which override global defaults"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        try:
            # Allow only one file
            if self.listCtrl1.GetSelectedItemCount() != 1:
                message = _(u'Select one media source.')
                dialog = wx.MessageDialog(self, message, _(u'ERROR'),
                    style=wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
                return
            # Show file settings
            item = self.listCtrl1.GetFirstSelected()
            name = self.listCtrl1.GetItemText(item)
            MediaMainFrame.show_settings(name, self)
            # Check if a media configuration exists for the file
            configfile = ConfigurationManager.getMediaConfiguration(name)
            if os.path.isfile(configfile):
                self.listCtrl1.SetStringItem(item, 1, _("YES"))
            else:
                self.listCtrl1.SetStringItem(item, 1, _("NO"))
        # On error, warn the user
        except Exception, e:
            message = str(e.args[0])
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(self, message, _(u'ERROR'),
                style=wx.OK|wx.ICON_ERROR)
                
    def deleteMediaSettings(self, event):
        "Delete the individual settings for a media file"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Check if there are media sources selected
        if self.listCtrl1.GetSelectedItemCount() == 0:
            message = _(u'No media sources selected.')
            dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                style=wx.OK|wx.ICON_ERROR)
            dialog.ShowModal()
            return
        # Get the selected items
        selItems = []
        item = self.listCtrl1.GetFirstSelected()
        while item >= 0:
            selItems.append(item)
            item = self.listCtrl1.GetNextSelected(item)
        # Delete the configuration files
        for item in selItems:
            filename = self.listCtrl1.GetItemText(item)
            ConfigurationManager.deleteConfiguration(filename)
            self.listCtrl1.SetStringItem(item, 1, _("NO"))
            
        
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
        Globals.audioPanel.changeAudioCodec(None)
        
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
                    if os.path.isfile(file) and os.access(file, os.R_OK):
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
            message = str(e.args[0])
            Globals.debug(_(u'ENCODING ERROR') + ': ' + message)
            # Show a dialog to the user
            #dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
            #    style=wx.OK|wx.ICON_ERROR)
            dialog = OutputTextDialog(self, message, _(u'ERROR'))
            dialog.ShowModal()
        
    def dropFiles(self, filenames):
        "One or more files are drop over the file list"
        for file in filenames: 
            # Avoid duplicated items
            if self.listCtrl1.FindItem(-1, file) == -1:
                index = self.listCtrl1.GetItemCount()
                self.listCtrl1.InsertStringItem(index, file)
                self.listCtrl1.SetColumnWidth(0, wx.LIST_AUTOSIZE)
