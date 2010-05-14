# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Previewer.py
# Purpose:      Allows advanced preview options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Previewer.py $
# Copyright:    (c) 2010 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Encoder

import subprocess
import os
import wx

def preview_files(file):
    "Encode a small chunk of the selected file and play it"
    busy = None
    # Create the temporary files
    Globals.createTemporary()
    # Disable the events on main frame
    Globals.mainPanel.Enable(False)
    try:
        # Set the busy cursor
        busy = wx.BusyCursor()
        
        filename = os.path.basename(file)

        # Start the audio encoding thread
        encode_audio = Encoder.EncodeAudioThread(file, file, preview=True)
        encode_audio.start()
        # Encode video
        Encoder.encode_video(file, file, preview=True)
        # Check the status of the thread
        encode_audio.join()
        threadError = encode_audio.getErrorMessage()
        if threadError:
            raise Exception(threadError)
        
        # Join audio and video with mencoder
        mencoder_proc = subprocess.Popen(
            ['mencoder',Globals.TMP_VIDEO,'-audiofile',Globals.TMP_AUDIO,
            '-ovc','copy','-oac','copy','-o',Globals.TMP_VIDEO+'.avi'],
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT, 
            universal_newlines=True)
        mencoder_output = mencoder_proc.communicate()[0]
        # Check the return process
        if mencoder_proc.wait() != 0:
            raise Exception(_(u'Error on mencoder')+': '+mencoder_output)
        
        # Sets the normal cursor again
        if busy is not None:
            del busy
        
        # Play the file with mplayer
        mplayer_proc = subprocess.Popen(
            ['mplayer',Globals.TMP_VIDEO+'.avi'], 
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT, 
            universal_newlines=True)
        mplayer_output = mplayer_proc.communicate()[0]
        # Check the return process
        if mplayer_proc.wait() != 0:
            raise Exception(_(u'Error on mplayer')+': '+mplayer_output)
        
        # Delete the temporary files
        os.remove(Globals.TMP_VIDEO+'.avi')
        Globals.clearTemporary()
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
    except Exception, e:
        # Sets the normal cursor again
        if busy is not None:
            del busy
        # Delete the temporary files
        Globals.clearTemporary()
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
        # Stop the audio encoding thread
        if encode_audio:
            encode_audio.stopThread()
        # Send the exception to the FilesPanel
        raise e
