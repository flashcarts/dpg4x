#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:App:BoaApp

#----------------------------------------------------------------------------
# Name:         Dpg4x.py
# Purpose:      A dpg encoder for Linux (and maybe others).
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Dpg4x.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import sys
import os

# On Windows wxPython 2.9.1.1 works better than 2.8.11.0.
# In particuliar OutputTextDialog() is unreadable and unusable. You can only
# see the first couple of letters of the text and the close button is missing.

# wxPython running from py2exe fails with wxversion.select()
# See: http://www.wxpython.org/docs/api/wxversion-module.html
if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.select(['2.8','2.9'])
import wx


import MainFrame
import Globals
import DpgImgInjector
import Dpg2Avi
import Encoder

modules ={u'AddDvdDialog': [0,
                   u'A dialog to add Dvd media sources.',
                   u'AddDvdDialog.py'],
 u'AddVcdDialog': [0,
                   u'A dialog to add Vcd media sources.',
                   u'AddVcdDialog.py'],
 u'AudioPanel': [0, u'Panel with audio options.', u'AudioPanel.py'],
 u'ConfigurationManager': [0,
                           u'Manages the configuration variables.',
                           u'ConfigurationManager.py'],
 u'CustomFontSelector': [0,
                         u'Dialog to select fonts (only faces).',
                         u'CustomFontSelector.py'],
 u'CustomProgressDialog': [0,
                           u'Dialog to show the progress of the encoding.',
                           u'CustomProgressDialog.py'],
 u'Dpg2Avi': [0, u'Converts DPG videos into AVI videos.', u'Dpg2Avi.py'],
 u'DpgImgInjector': [0,
                     u'Insert supported wx.Image() file into an existing DPG file.',
                     u'DpgImgInjector.py'],
 u'Encoder': [0, u'Performs the encoding duties.', u'Encoder.py'],
 u'FilesPanel': [0, u'Panel with files to be encoded.', u'FilesPanel.py'],
 u'Globals': [0,
              u'Source file with global variables and functions.',
              u'Globals.py'],
 u'MainFrame': [1, u'Main frame of Application.', u'MainFrame.py'],
 u'MediaAudioPanel': [0,
                      u'Panel with per-media audio options.',
                      u'MediaAudioPanel.py'],
 u'MediaMainFrame': [0,
                     u'Frame with per-media settings.',
                     u'MediaMainFrame.py'],
 u'MediaOtherPanel': [0,
                      u'Panel with per-media aditional options.',
                      u'MediaOtherPanel.py'],
 u'MediaSubtitlesPanel': [0,
                          u'Panel with per-media subtitle options.',
                          u'MediaSubtitlesPanel.py'],
 u'MediaVideoPanel': [0,
                      u'Panel with per-media video options.',
                      u'MediaVideoPanel.py'],
 u'OtherPanel': [0, u'Panel with aditional options.', u'OtherPanel.py'],
 u'OutputTextDialog': [0,
                       u"Dialog with a TextCtrl to show program's output.",
                       u'moreControls/OutputTextDialog.py'],
 u'Previewer': [0, u'Allows advanced preview options.', u'Previewer.py'],
 u'SubtitlesPanel': [0, u'Panel with subtitle options.', u'SubtitlesPanel.py'],
 u'TreeCtrlComboPopup': [0,
                         u'Popup control containing a TreeCtrl.',
                         u'TreeCtrlComboPopup.py'],
 u'VideoPanel': [0, u'Panel with video options.', u'VideoPanel.py']}
    
def checkDependencies():
    "Check that the mandatory dependecies are present"
    # Mandatory programs
    mandatory = ['mplayer','mencoder']
    # Check that all of them are present
    for program in mandatory:
        if not Globals.which(program):
            message = _(u'%s not found in PATH. Please install it.') % program
            # Show an error in the console
            Globals.debug(_(u'ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(None, message, _(u'ERROR'), style=wx.OK|wx.ICON_ERROR)
            dialog.ShowModal()
            sys.exit(1)

def checkArgs():
    # optparse is deprecated in 2.7, but we might run on older Python versions
    from optparse import OptionParser

    usage = u'usage: %prog [options] file1 file2...   (starts GUI if no options)'
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--image", dest="image",
                  help=u'image file to inject into DPG files', metavar="FILE",)
    parser.add_option("", "--dpg",
                  action="store_true", dest="dpg", default=False,
                  help=u'convert files to DPG')
    parser.add_option("", "--avi",
                  action="store_true", dest="avi", default=False,
                  help=u'convert DPG files to AVI, no transformation')

    (options, args) = parser.parse_args()
    if len(args)>0:
        if options.image:
            for a in args:
                a = Globals.Decode(a)
                Globals.debug(a)
                DpgImgInjector.DpgInject(a,options.image,a)
            return False
        elif options.avi:
            for a in args:
                a = Globals.Decode(a)
                Globals.debug(a)
                Dpg2Avi.Dpg2Avi(a)
            return False
        elif options.dpg:
            for a in args:
                a = Globals.Decode(a)
                Globals.debug(a)
                Encoder.encode_files([a])
            return False
    return True


# Main function
if __name__ == '__main__':
    Globals.SetupTranslation()
    checkDependencies()
    firstExec = checkArgs() 
    application = wx.App(redirect=False,clearSigInt=False)
    while firstExec or Globals.restart:
        # Reload the Globals module on restart
        if Globals.restart:
            reload(Globals)
        firstExec = False
        mainFrame = MainFrame.create(None, Globals.getIconDir())
        mainFrame.Show()
        Globals.mainPanel = mainFrame
        application.SetTopWindow(mainFrame)
        application.MainLoop()
    sys.exit(0)
