#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AudioPanel.py
# Purpose:      Panel with audio options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AudioPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals

import wx

[wxID_PANEL1, wxID_PANEL1CHECKBOX1, wxID_PANEL1CHECKBOX2, wxID_PANEL1CHOICE1, 
 wxID_PANEL1CHOICE2, wxID_PANEL1CHOICE3, wxID_PANEL1SPINCTRL1, 
 wxID_PANEL1STATICTEXT1, wxID_PANEL1STATICTEXT2, wxID_PANEL1STATICTEXT3, 
 wxID_PANEL1STATICTEXT4, wxID_PANEL1CHECKBOX3
] = [wx.NewId() for _init_ctrls in range(12)]

class AudioPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))
        parent.AddSpacer(wx.Size(150, 20), (0, 1), border=0, flag=0, span=(1,2))
        parent.AddSpacer(wx.Size(40, 20), (0, 4), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText1, (1, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.AddWindow(self.choice1, (1, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText2, (4, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.AddWindow(self.spinCtrl1, (4, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox3, (4, 5), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox1, (7, 5), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText3, (7, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,
              2))
        parent.AddWindow(self.choice2, (7, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText4, (9, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,
              2))
        parent.AddWindow(self.choice3, (9, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox2, (9, 5), border=0, flag=0, span=(1, 1))

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

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_(u'Audio Codec')+' ', name='staticText1', parent=self, 
              style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_(u'Select Audio Track')+' ', name='staticText2', 
              parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL1, 
              initial=Globals.audio_track,
              max=14, min=0, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.checkBox1 = wx.CheckBox(id=wxID_PANEL1CHECKBOX1, 
              label=_(u'Normalize Volume'), name='checkBox1', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_(u'Audio Bitrate')+' ', name='staticText3', 
              parent=self, style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_(u'Audio Frequency')+' ', name='staticText4', parent=self, 
              style=0)

        self.choice3 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE3,
              name='choice3', parent=self, style=0)

        self.checkBox2 = wx.CheckBox(id=wxID_PANEL1CHECKBOX2, 
              label=_(u'Force Mono Channel'), name='checkBox2', 
              parent=self, style=0)
              
        self.checkBox3 = wx.CheckBox(id=wxID_PANEL1CHECKBOX3, 
              label=_(u'Auto Audio Track'), name='checkBox3', 
              parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Init the audio codec choice
        self.choice1.Append(u'GSM','libgsm')
        self.choice1.Append(u'MP2','mp2')
        # OGG can be used only with DPG3 or better
        if Globals.dpg_version >= 3:
            self.choice1.Append(u'OGG','vorbis')
        # Load the stored selection
        if Globals.audio_codec == 'libgsm':
            self.choice1.Select(0)
        elif Globals.audio_codec == 'mp2':
            self.choice1.Select(1)
        elif Globals.audio_codec == 'vorbis':
            self.choice1.Select(2)
            
        # We are having lots of problems with the way mencoder manages
        # gms and ogg, so it'll be disabled until a solution is found
        # I think adding more dependencies is not worth it
        self.choice1.Select(1)
        self.choice1.Enable(False)
            
        # Init the audio bitrate choice
        self.choice2.Append(u'32',32)
        self.choice2.Append(u'48',48)
        self.choice2.Append(u'64',64)
        self.choice2.Append(u'80',80)
        self.choice2.Append(u'96',96)
        self.choice2.Append(u'112',112)
        self.choice2.Append(u'128',128)
        self.choice2.Append(u'144',144)
        self.choice2.Append(u'160',160)
        self.choice2.Append(u'176',176)
        self.choice2.Append(u'192',192)
        self.choice2.Append(u'208',208)
        self.choice2.Append(u'224',224)
        self.choice2.Append(u'240',240)
        self.choice2.Append(u'256',256)
        self.choice2.SetStringSelection(str(Globals.audio_bitrate))
        
        # Init the audio frequency choice
        self.choice3.Append(u'22050',22050)
        self.choice3.Append(u'32000',32000)
        self.choice3.Append(u'44100',44100)
        self.choice3.SetStringSelection(str(Globals.audio_frequency))
        
        # Only audio at 32000 works with current versions. Disabled.
        self.choice3.SetSelection(1)
        self.choice3.Enable(False)
        
        # Init the auto track check
        if Globals.audio_autotrack:
            self.checkBox3.SetValue(True)
        self.switchAutoTrack(None)
        
        # Check normalize if needed
        if Globals.audio_normalize:
            self.checkBox1.SetValue(True)
            
        # Check mono if needed
        if Globals.audio_mono:
            self.checkBox2.SetValue(True)
        
        # Events
        wx.EVT_CHECKBOX(self.checkBox3, wxID_PANEL1CHECKBOX3, self.switchAutoTrack)
        
    def switchAutoTrack(self, event):
        "Enable or disable the track selector"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.spinCtrl1.Enable(not self.checkBox3.IsChecked())
        
    def loadOptions(self):
        "Load the audio options as global variables"
        Globals.audio_codec = self.choice1.GetClientData(
            self.choice1.GetSelection())
        Globals.audio_track = self.spinCtrl1.GetValue()
        Globals.audio_autotrack = self.checkBox3.IsChecked() 
        Globals.audio_bitrate = self.choice2.GetClientData(
            self.choice2.GetSelection())
        Globals.audio_frequency = self.choice3.GetClientData(
            self.choice3.GetSelection())
        Globals.audio_normalize = self.checkBox1.IsChecked()
        Globals.audio_mono = self.checkBox2.IsChecked()

