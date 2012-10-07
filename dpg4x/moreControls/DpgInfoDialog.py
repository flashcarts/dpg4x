# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         DpgInfoDialog.py
# Purpose:      Dialog with a thumbail image and TextCtrls to show DPG info,
#               includes a button to replace the thumbnail
#
# Author:       Tomas Aronsson
# Created:      Sep 2012
# Copyright:    (c) 2012 Tomas Aronsson
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx
import os
import DpgHeader
import DpgThumbnail

[wxID_DIALOG1, wxID_DIALOG1PANEL1, wxID_DIALOG1TEXTCTRL1,
 wxID_DIALOG1TIMER1
] = [wx.NewId() for _init_ctrls in range(4)]

class DpgInfoDialog(wx.Dialog):
 
    def _init_sizers(self):
        self.boxSizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxSizer1.Add(self.textCtrl1, 1, border=0, flag=wx.EXPAND)
        self.boxSizer1.Add(self.bmp, 1, border=0, flag=wx.EXPAND)
        self.dpg_panel.SetSizer(self.boxSizer1)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxSizer2.Add(self.button1, 0, border=0, flag=wx.ALIGN_RIGHT)
        self.boxSizer2.Add(self.button2, 0, border=0, flag=wx.ALIGN_RIGHT)
        self.panelb.SetSizer(self.boxSizer2)

        self.boxSizer3 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer3.Add(self.dpg_panel, 1, border=0, flag=wx.EXPAND)
        self.boxSizer3.Add(self.textCtrl2, 1, border=0, flag=wx.EXPAND)
        self.boxSizer3.Add(self.panelb, 0, border=1, flag=wx.ALIGN_RIGHT)
        self.main_panel.SetSizer(self.boxSizer3)


    def _init_ctrls(self, prnt, titl=''):
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(271, 143), size=wx.Size(683, 445),
              style=wx.CAPTION | wx.RESIZE_BORDER, title=titl)
        self.SetClientSize(wx.Size(683, 445))

        self.main_panel = wx.Panel(id=wxID_DIALOG1PANEL1, name='main_panel',
              parent=self, style=wx.TAB_TRAVERSAL)

        # DPG info panel
        self.dpg_panel = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self.main_panel, style=wx.TAB_TRAVERSAL)

        self.bmp = wx.StaticBitmap(self.dpg_panel, wx.ID_ANY, wx.EmptyBitmap(256, 192))

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self.dpg_panel,
              style=wx.TE_MULTILINE | wx.TE_READONLY, value='')

        # Mencoder output
        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl2',
              parent=self.main_panel,
              style=wx.TE_MULTILINE | wx.TE_READONLY, value='')

        # Buttons
        self.panelb = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel2',
              parent=self.main_panel, style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wx.ID_CLOSE, label=_(u'Close'),
              parent=self.panelb, style=0)

        self.button2 = wx.Button(id=wx.ID_OPEN, label=_(u'Select Thumbnail'),
              parent=self.panelb, style=0)

        self._init_sizers()

    def __init__(self, parent, filename, text='', title=''):
        self.filename = filename
        self._init_ctrls(parent, title)
        # Show the text
        dpg = DpgHeader.DpgHeader(filename)
        if dpg.version > 3:
            thumb = DpgThumbnail.DpgThumbnail(filename)
            self.textCtrl1.AppendText(unicode(dpg))
            self.textCtrl1.ShowPosition(0)
            self.bmp.SetBitmap(thumb.getImage().ConvertToBitmap())
        else:
            self.textCtrl1.AppendText(unicode(dpg))
            
        self.textCtrl2.AppendText(text)
        self.textCtrl2.ShowPosition(0)
        # Events
        wx.EVT_BUTTON(self.button1, wx.ID_CLOSE, self.OnClose)
        # Only allow to replace thumbnail if DPG 4
        if dpg.version > 3:
            wx.EVT_BUTTON(self.button2, wx.ID_OPEN, self.OnReplaceThumb)
        else:
            self.button2.Disable()
        
    def OnClose(self, event):
        "Close the dialog"
        self.EndModal(wx.ID_OK)

    def OnReplaceThumb(self, event):
        "Replace thumbnail"
        image_file = None
        dialog = wx.FileDialog(self, _(u'Select a thumbnail file'), style=wx.OPEN,
            defaultDir=os.path.dirname(self.filename))
        if dialog.ShowModal() == wx.ID_OK:
            image_file = dialog.GetPath()
        dialog.Destroy()

        if image_file is not None: 
            try:       
                DpgThumbnail.DpgInject(self.filename,image_file,self.filename)
                thumb = DpgThumbnail.DpgThumbnail(image_file)
                self.bmp.SetBitmap(thumb.getImage().ConvertToBitmap())
            except Exception, e:
                message = unicode(e.args[0])
                dialog = wx.MessageDialog(self, message, _(u'ERROR'), 
                                          style=wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
                            