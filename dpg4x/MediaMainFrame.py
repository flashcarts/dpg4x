#Boa:Frame:Frame2
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MediaMainFrame.py
# Purpose:      Frame with per-media settings.
#
# Author:       Marc P. Davignon
#
# Created:
# RCS-ID:       $Id: MediaMainFrame.py $
# Copyright:    (c) 2010 Marc P. Davignon
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import ConfigurationManager
import MediaVideoPanel
import MediaAudioPanel
import MediaSubtitlesPanel
import MediaOtherPanel

import wx
import os

def show_settings(file, parent):
    "Allows individual media settings which override global defaults"
    mediaMainFrame = Frame2(file, parent)
    mediaMainFrame.Show()
    Globals.mediaMainPanel = mediaMainFrame

[wxID_FRAME2, wxID_FRAME2NOTEBOOK1,
] = [wx.NewId() for _init_ctrls in range(2)]

class Frame2(wx.Frame):
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)


    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.notebook1, 1, border=0, flag=wx.EXPAND)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME2, name='', parent=prnt,
              style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                    wx.CLIP_CHILDREN,
              title=os.path.basename(self.file))

        self.notebook1 = wx.Toolbook(id=wxID_FRAME2NOTEBOOK1, name='notebook1',
              parent=self, style=wx.BK_TOP)

        self._init_sizers()

    def __init__(self, file, parent):
        # Disable the events on main frame
        Globals.mainPanel.Enable(False)

        self.file = file
        # Read options from the media specific config file (if one exists)
        # This allows media specific options to be saved between sessions
        ConfigurationManager.loadConfiguration(self.file)
        self._init_ctrls(parent)

        # Set the icons for the main window
        bundle = wx.IconBundle()
        icon_dir = os.getenv('DPG4X_ICONS')
        bundle.AddIconFromFile(icon_dir+'/dpg4x_64.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(icon_dir+'/dpg4x_48.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(icon_dir+'/dpg4x_32.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(icon_dir+'/dpg4x_22.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(icon_dir+'/dpg4x_16.png',
            wx.BITMAP_TYPE_PNG)
        self.SetIcons(bundle)

        # Set the icons for the menu
        imageList = wx.ImageList(32, 32)
        imageList.AddIcon(wx.Icon(icon_dir+'/files.png',
            wx.BITMAP_TYPE_PNG))
        imageList.AddIcon(wx.Icon(icon_dir+'/video.png',
            wx.BITMAP_TYPE_PNG))
        imageList.AddIcon(wx.Icon(icon_dir+'/audio.png',
            wx.BITMAP_TYPE_PNG))
        imageList.AddIcon(wx.Icon(icon_dir+'/subtitles.png',
            wx.BITMAP_TYPE_PNG))
        imageList.AddIcon(wx.Icon(icon_dir+'/other.png',
            wx.BITMAP_TYPE_PNG))
        self.notebook1.AssignImageList(imageList)

        # Panel with media video options
        mediaVideoPanel = MediaVideoPanel.MediaVideoPanel(self.notebook1)
        self.notebook1.AddPage(mediaVideoPanel,
            Globals.fillString(_(u'VIDEO'),10),imageId=1)
        Globals.mediaVideoPanel = mediaVideoPanel

        # Panel with media audio options
        mediaAudioPanel = MediaAudioPanel.MediaAudioPanel(self.notebook1)
        self.notebook1.AddPage(mediaAudioPanel,
            Globals.fillString(_(u'AUDIO'),10),imageId=2)
        Globals.mediaAudioPanel = mediaAudioPanel

        # Panel with media subtitle options
        mediaSubtitlesPanel = MediaSubtitlesPanel.MediaSubtitlesPanel(self.notebook1)
        self.notebook1.AddPage(mediaSubtitlesPanel,
            Globals.fillString(_(u'SUBTITLES'),10),imageId=3)
        Globals.mediaSubtitlesPanel = mediaSubtitlesPanel

        # Panel with aditional media options
        mediaOtherPanel = MediaOtherPanel.MediaOtherPanel(self.notebook1)
        self.notebook1.AddPage(mediaOtherPanel,
            Globals.fillString(_(u'MISC'),10),imageId=4)
        Globals.mediaOtherPanel = mediaOtherPanel

        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))

    def saveAndCloseFrame(self, event):
        "Save and close the media settings window"
        # Get the options from the panels
        Globals.mediaVideoPanel.loadOptions()
        Globals.mediaAudioPanel.loadOptions()
        Globals.mediaSubtitlesPanel.loadOptions()
        Globals.mediaOtherPanel.loadOptions(None)
        # Save options to the media specific config file
        ConfigurationManager.saveConfiguration(self.file)

        self.closeFrame(event)

    def closeFrame(self, event):
        "Do not save, just close the media settings window"
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
        self.Close()
