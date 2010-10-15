#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         VideoPanel.py
# Purpose:      Panel with video options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: VideoPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals

import wx

[wxID_PANEL1, wxID_PANEL1CHECKBOX1, wxID_PANEL1CHECKBOX2, wxID_PANEL1CHOICE1, 
 wxID_PANEL1CHOICE2, wxID_PANEL1SPINCTRL1, wxID_PANEL1SPINCTRL2, 
 wxID_PANEL1SPINCTRL3, wxID_PANEL1STATICTEXT1, wxID_PANEL1STATICTEXT2, 
 wxID_PANEL1STATICTEXT3, wxID_PANEL1STATICTEXT4, wxID_PANEL1STATICTEXT5,
 wxID_PANEL1STATICTEXT6, wxID_PANEL1SPINCTRL4, wxID_PANEL1CHECKBOX3
] = [wx.NewId() for _init_ctrls in range(16)]

class VideoPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))
        parent.AddSpacer(wx.Size(150, 20), (0, 1), border=0, flag=0, span=(1, 2))
        parent.AddSpacer(wx.Size(40, 20), (0, 4), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText1, (1, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.spinCtrl1, (1, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText2, (3, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.spinCtrl2, (3, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox1, (3, 5), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText6, (6, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.spinCtrl4, (6, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox3, (6, 5), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText3, (9, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.spinCtrl3, (11, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.staticText4, (11, 1), border=0, 
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.AddWindow(self.choice1, (9, 3), border=0, flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox2, (11, 5), border=0, flag=0, span=(1, 1))
        
        # Too many objects here, pixel format hidden
        #parent.AddWindow(self.staticText5, (11, 1), border=0, 
        #      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        #parent.AddWindow(self.choice2, (11, 3), border=0, flag=0, span=(1, 1))

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
              label=_(u'Width')+' ', name='staticText1', parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL1, 
              initial=Globals.video_width,
              max=256, min=256, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.checkBox1 = wx.CheckBox(id=wxID_PANEL1CHECKBOX1, 
              label=_(u'Keep Aspect'),name='checkBox1', parent=self, style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_(u'Height')+' ', name='staticText2', parent=self, style=0)

        self.spinCtrl2 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL2, 
              initial=Globals.video_height,
              max=192, min=16, name='spinCtrl2', parent=self,
              style=wx.SP_ARROW_KEYS)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_(u'Video Bitrate')+' ', name='staticText3', parent=self, 
              style=0)

        self.spinCtrl3 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL3, 
              initial=Globals.video_fps,
              max=24, min=1, name='spinCtrl3', parent=self,
              style=wx.SP_ARROW_KEYS)

        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_(u'Frames Per Second')+' ', name='staticText4', 
              parent=self, style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)

        self.checkBox2 = wx.CheckBox(id=wxID_PANEL1CHECKBOX2, 
              label=_(u'Auto FPS'),name='checkBox2', parent=self, style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANEL1STATICTEXT5,
              label=_(u'Pixel Format')+' ', name='staticText5', parent=self, 
              style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)
              
        self.staticText6 = wx.StaticText(id=wxID_PANEL1STATICTEXT6,
              label=_(u'Video Track')+' ', name='staticText6', 
              parent=self, style=0)
              
        self.spinCtrl4 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL4, 
              initial=Globals.video_track,
              max=255, min=1, name='spinCtrl4', parent=self,
              style=wx.SP_ARROW_KEYS)
              
        self.checkBox3 = wx.CheckBox(id=wxID_PANEL1CHECKBOX3, 
              label=_(u'Auto Video Track'),name='checkBox3', parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Check the keep aspect if needed
        if Globals.video_keepaspect:
            self.checkBox1.SetValue(True)
        self.switchSize(None)
        
        # Init video bitrate choice
        self.choice1.Append(u'64',64)
        self.choice1.Append(u'80',80)
        self.choice1.Append(u'96',96)
        self.choice1.Append(u'112',112)
        self.choice1.Append(u'128',128)
        self.choice1.Append(u'144',144)
        self.choice1.Append(u'160',160)
        self.choice1.Append(u'176',176)
        self.choice1.Append(u'192',192)
        self.choice1.Append(u'208',208)
        self.choice1.Append(u'224',224)
        self.choice1.Append(u'240',240)
        self.choice1.Append(u'256',256)
        self.choice1.Append(u'272',272)
        self.choice1.Append(u'288',288)
        self.choice1.Append(u'304',304)
        self.choice1.Append(u'320',320)
        self.choice1.Append(u'336',336)
        self.choice1.Append(u'352',352)
        self.choice1.Append(u'368',368)
        self.choice1.Append(u'384',384)
        self.choice1.Append(u'400',400)
        self.choice1.Append(u'416',416)
        self.choice1.Append(u'432',432)
        self.choice1.Append(u'448',448)
        self.choice1.Append(u'464',464)
        self.choice1.SetStringSelection(str(Globals.video_bitrate))
        
        # Init the pixel format choice
        self.choice2.Append(u'RGB15',0)
        self.choice2.Append(u'RGB18',1)
        self.choice2.Append(u'RGB21',2)
        self.choice2.Append(u'RGB24',3)
        self.choice2.Select(Globals.video_pixel)
        
        # Pixel format other than RGB24 does not work for me
        # Maybe it works for others, but I'll better disable it for now
        self.choice2.Select(3)
        self.choice2.Enable(False)
        # Hidden also, there are too many options in the video panel
        self.staticText5.Show(False)
        self.choice2.Show(False)
        
        # Init the auto FPS check
        self.checkBox2.SetValue(Globals.video_autofps)
        self.switchAutoFPS(None)
        
        # Init the auto track check
        if Globals.video_autotrack:
            self.checkBox3.SetValue(True)
        self.switchAutoTrack(None)
        
        # Hack to detect when the spin buttons are pressed
        self.aux_flag_text = 0
        
        # Events
        wx.EVT_CHECKBOX(self.checkBox1, wxID_PANEL1CHECKBOX1, self.switchSize)
        wx.EVT_CHECKBOX(self.checkBox2, wxID_PANEL1CHECKBOX2, self.switchAutoFPS)
        wx.EVT_CHECKBOX(self.checkBox3, wxID_PANEL1CHECKBOX3, self.switchAutoTrack)
        wx.EVT_SPINCTRL(self.spinCtrl2, wxID_PANEL1SPINCTRL2, self.spinHeight)
        wx.EVT_TEXT(self.spinCtrl2, wxID_PANEL1SPINCTRL2, self.spinHeightText)

        
    def switchAutoTrack(self, event):
        "Enable or disable the track selector"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.spinCtrl4.Enable(not self.checkBox3.IsChecked())
              
    def switchSize(self, event):
        "Enable or disable the size controls"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        #self.spinCtrl1.Enable(not self.checkBox1.IsChecked())
        self.spinCtrl2.Enable(not self.checkBox1.IsChecked())
        
    def switchAutoFPS(self, event):
        "Enable or disable the FPS control"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.spinCtrl3.Enable(not self.checkBox2.IsChecked())
        
    def spinHeight(self, event):
        "Force video height to be an integer multiple of 16"
        # See track 3085578
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        newValue = self.spinCtrl2.GetValue()
        modNewValue = newValue % 16
        
        # Exit if the value is a multiple of 16
        if modNewValue == 0:
            # Reset the flag
            self.aux_flag_text = 0
            return
        
        # A spin button has been pressed
        if self.aux_flag_text < 2:
            # Round up
            if modNewValue == 1:
                self.spinCtrl2.SetValue(newValue + 16 - modNewValue)
            # Round down
            elif modNewValue == 15:
                self.spinCtrl2.SetValue(newValue - modNewValue)
            # Manage errors - ie. you select 192 and delete the 2
            # This is only one text event
            else:
                self.aux_flag_text = 2
        
        # The inner text control has been edited (or error on spin)
        if self.aux_flag_text >= 2:
            # Round up
            if modNewValue >= 8:
                self.spinCtrl2.SetValue(newValue + 16 - modNewValue)
            # Round down
            else:
                self.spinCtrl2.SetValue(newValue - modNewValue)
                
        # Reset the flag
        self.aux_flag_text = 0
            
    def spinHeightText(self, event):
        "Auxiliar funcion to detect when the spin button are (not) pressed"
        # This is a dirty hack... for the previous function
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.aux_flag_text += 1
        
    def loadOptions(self):
        "Load the video options as global variables"
        Globals.video_keepaspect = self.checkBox1.IsChecked()
        Globals.video_width = self.spinCtrl1.GetValue()
        Globals.video_height = self.spinCtrl2.GetValue()
        Globals.video_track = self.spinCtrl4.GetValue()
        Globals.video_autotrack = self.checkBox3.IsChecked()
        Globals.video_bitrate = self.choice1.GetClientData(
            self.choice1.GetSelection())
        Globals.video_autofps = self.checkBox2.IsChecked()
        Globals.video_fps = self.spinCtrl3.GetValue()
        Globals.video_pixel = self.choice2.GetClientData(
            self.choice2.GetSelection())
            
