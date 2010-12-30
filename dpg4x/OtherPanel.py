#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         OtherPanel.py
# Purpose:      Panel with aditional options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: OtherPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# NOTE: "OTHER" is not longer used, now we call it "MISC".

import Globals
import ConfigurationManager

import wx
import os

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, wxID_PANEL1BUTTON3, 
 wxID_PANEL1STATICTEXT1, wxID_PANEL1STATICTEXT2, wxID_PANEL1STATICTEXT3, 
 wxID_PANEL1TEXTCTRL1, wxID_PANEL1TEXTCTRL2, wxID_PANEL1TEXTCTRL3, 
 wxID_PANEL1STATICTEXT4, wxID_PANEL1STATICTEXT5, wxID_PANEL1STATICTEXT6,
 wxID_DIALOG1SPINCTRL1, wxID_PANEL1BUTTON4, wxID_PANEL2
] = [wx.NewId() for _init_ctrls in range(16)]

class OtherPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))
        parent.AddSpacer(wx.Size(100, 8), (0, 1), border=0, flag=0, span=(1, 2))
        parent.AddSpacer(wx.Size(280, 8), (0, 3), border=0, flag=0, span=(1, 3))
        parent.AddWindow(self.staticText1, (1, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.textCtrl1, (1, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.AddWindow(self.button1, (1, 6), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText4, (2, 1), border=0, 
              flag=wx.ALIGN_CENTER, span=(1,7))
        parent.AddWindow(self.staticText2, (4, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.AddWindow(self.textCtrl2, (4, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.AddWindow(self.button2, (4, 6), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText3, (6, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.textCtrl3, (6, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.AddWindow(self.button3, (6, 6), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText5, (7, 1), border=0, 
              flag=wx.ALIGN_CENTER, span=(1, 7))    
        parent.AddWindow(self.staticText6, (9, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 3))
        parent.AddWindow(self.spinCtrl1, (9, 4), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.panel2, (11, 1), border=0, flag=wx.EXPAND,
              span=(1, 7))
              
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit
        
        parent.Add(self.button4, 1, border=0, flag=wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)
        self.boxSizer1 = wx.BoxSizer(wx.VERTICAL)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)
        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.gridBagSizer1)
        self.panel2.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)
              
        self.panel2 = wx.Panel(id=wxID_PANEL2, name='', parent=self)

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_(u'Output Folder')+' ', name='staticText1', 
              parent=self, style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.other_output)

        self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=_(u'Examine'),
              name='button1', parent=self, style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_(u'Temporary Folder')+' ', name='staticText2', 
              parent=self, style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL2, name='textCtrl2',
              parent=self, style=0, value=Globals.other_temporary)

        self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=_(u'Examine'),
              name='button2', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_(u'Select Thumbnail')+' ', name='staticText3', 
              parent=self, style=0)

        self.textCtrl3 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL3, name='textCtrl3',
              parent=self, style=0, value=Globals.other_thumbnail)

        self.button3 = wx.Button(id=wxID_PANEL1BUTTON3, label=_(u'Examine'),
              name='button3', parent=self, style=0)
              
        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_(u'The input folder will be used by default'), 
              name='staticText4', parent=self, style=0)
              
        self.staticText5 = wx.StaticText(id=wxID_PANEL1STATICTEXT5,
              label=_(u'Thumbnails are autogenerated by default (DPG4 only)'), 
              name='staticText5', parent=self, style=0)
              
        self.staticText6 = wx.StaticText(id=wxID_PANEL1STATICTEXT6,
              label=_(u'Preview size (seconds)'), 
              name='staticText6', parent=self, style=0)
              
        self.spinCtrl1 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL1, 
              value=str(Globals.other_previewsize), max=9999, min=1,
              name='spinCtrl1', parent=self, style=wx.SP_ARROW_KEYS)
              
        self.button4 = wx.Button(id=wxID_PANEL1BUTTON4, 
              label=_(u'Reset all the configuration to the default values'),
              name='button4', parent=self.panel2, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Thumbnails only available for DPG version 4
        if Globals.dpg_version < 4:
            self.textCtrl3.Enable(False)
            self.button3.Enable(False)
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_PANEL1BUTTON1, self.selectOuputDir)
        wx.EVT_BUTTON(self.button2, wxID_PANEL1BUTTON2, self.selectTemporaryDir)
        wx.EVT_BUTTON(self.button3, wxID_PANEL1BUTTON3, self.selectThumbnail)
        wx.EVT_BUTTON(self.button4, wxID_PANEL1BUTTON4, self.resetConfiguration)
        
    def selectOuputDir(self, event):
        "Dialog to select the output folder"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.DirDialog(self, _(u'Select the ouput folder'), 
            style=wx.DD_DEFAULT_STYLE, 
            defaultPath=os.path.dirname(self.textCtrl1.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl1.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def selectTemporaryDir(self, event):
        "Dialog to select the output folder"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.DirDialog(self, _(u'Select the temporary folder'), 
            style=wx.DD_DEFAULT_STYLE, 
            defaultPath=os.path.dirname(self.textCtrl2.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl2.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def selectThumbnail(self, event):
        "Dialog to select a subtitles file"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.FileDialog(self, _(u'Select a thumbnail file'), style=wx.OPEN, 
            defaultDir=os.path.dirname(self.textCtrl3.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl3.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def loadOptions(self, files):
        "Load the other options as global variables"
        Globals.other_output = self.textCtrl1.GetValue()
        # Check the output folder exists and is writable
        if Globals.other_output:
            if not (os.path.isdir(Globals.other_output) and os.access(
                Globals.other_output, os.W_OK)):
                raise Exception(_(u'The output folder can not be written.' \
                    u' Please select another one.'))
        # If no output folder given, check the input folders
        elif files is not None:
            for file in files:
                # Check for DVD and VCD sources
                if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
                    raise Exception(_(u'If you want to encode from DVD or VCD' \
                        u' you need to select an output folder in "MISC".'))
                # Check for normal files
                else:
                    outDir = os.path.dirname(file)
                    if not (os.path.isdir(outDir) and os.access(outDir, os.W_OK)):
                        raise Exception(_(u'The folder %s can not be written.' \
                            u' Please select an output folder in "MISC".') % outDir)
            
        Globals.other_temporary = self.textCtrl2.GetValue()
        # Check the temporary folder exists and is writable
        if not (os.path.isdir(Globals.other_temporary) and os.access(
            Globals.other_temporary, os.W_OK)):
            raise Exception(_(u'The temporary folder can not be written.' \
                u' Please select another one.'))
                
        Globals.other_thumbnail = self.textCtrl3.GetValue()
        # Check the thumbnail file can be readed
        if Globals.other_thumbnail:
            if not (os.path.isfile(Globals.other_thumbnail) and os.access(
                Globals.other_thumbnail, os.R_OK)):
                raise Exception(_(u'The thumbnail file can not be readed.'))
            # Check the thumbnail file can be processed by wx.Image
            imageAux = wx.Image(Globals.other_thumbnail)
            if not imageAux.IsOk():
                raise Exception(_(u'The thumbnail file has an unknown format.'))
            
        Globals.other_previewsize = self.spinCtrl1.GetValue()
        
    def resetConfiguration(self, event):
        "Deletes the configuation files and restarts the program"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Ask for confirmation
        dialog = wx.MessageDialog(self, 
            _(u'The configuration files will be deleted and dpg4x will be ' \
            'restarted using the default settings. Do you want to continue?'),
            _(u'QUESTION'), style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        confirmation = dialog.ShowModal()
        if confirmation == wx.ID_YES:
            # Delete the configuration files
            ConfigurationManager.resetAllConfiguration()
            # Restart the program
            Globals.restart = True
            Globals.mainPanel.Close()
      
