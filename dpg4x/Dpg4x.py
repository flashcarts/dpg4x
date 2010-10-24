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

import wxversion
wxversion.select('2.8')
import wx

import os
import sys
import gettext

import MainFrame
import Globals

# Check if a gettext resource is available for the current LANG
if not gettext.find('dpg4x', os.getenv('DPG4X_I18N')):
    Globals.debug(u'WARNING: dpg4x is not available in your languaje, ' \
                u'please help us to translate it.')
    gettext.install('dpg4x', os.getenv('DPG4X_I18N'), unicode=True)
else:
    gettext.translation('dpg4x', os.getenv('DPG4X_I18N')).install(unicode=True)

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
            dialog = wx.MessageDialog(None, message, _(u'ERROR'), style=wx.ICON_ERROR)
            dialog.ShowModal()
            sys.exit(1)

# Main function
if __name__ == '__main__':
    application = wx.App(redirect=False,clearSigInt=False)
    checkDependencies()
    mainFrame = MainFrame.create(None)
    mainFrame.Show()
    Globals.mainPanel = mainFrame
    application.SetTopWindow(mainFrame)
    application.MainLoop()
    sys.exit(0)
        
