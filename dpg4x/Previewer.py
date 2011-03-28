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
from moreControls.OutputTextDialog import OutputTextDialog

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
        
        # PATCH: Mplayer can't play audio bitrate higher than 256
        old_audio_bitrate = Globals.audio_bitrate_mp2
        if Globals.audio_bitrate_mp2 > 256:
            Globals.audio_bitrate_mp2 = 256
        
        # Start the audio encoding thread
        encode_audio = Encoder.EncodeAudioThread(file, file, preview=True)
        encode_audio.start()
        # Encode video
        Encoder.encode_video(file, file, preview=True)
        # Check the status of the thread
        encode_audio.join()
        # Restore the audio bitrate (previous patch)
        Globals.audio_bitrate_mp2 = old_audio_bitrate
        threadError = encode_audio.getErrorMessage()
        if threadError:
            raise Exception(threadError)
        
        # Join audio and video with mencoder
        mencoder_proc = subprocess.Popen(
            Globals.ListUnicodeEncode(['mencoder',Globals.TMP_VIDEO,'-audiofile',Globals.TMP_AUDIO,
            '-ffourcc','mpg1','-ovc','copy','-oac','copy','-o',
            Globals.TMP_VIDEO+'.avi']),
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            # On Windows when running under py2exe it is 
            # necessary to define stdin
            stdin=subprocess.PIPE,shell=Globals.shell(), 
            universal_newlines=True)
        mencoder_output = mencoder_proc.communicate()[0]
        # Check the return process
        if mencoder_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)
        
        # Sets the normal cursor again
        if busy is not None:
            del busy
        
        # Play the file with mplayer
        mplayer_proc = subprocess.Popen(
            Globals.ListUnicodeEncode(['mplayer',Globals.TMP_VIDEO+'.avi']), 
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            # On Windows when running under py2exe it is 
            # necessary to define stdin
            stdin=subprocess.PIPE,shell=Globals.shell(),
            universal_newlines=True)
        mplayer_output = mplayer_proc.communicate()[0]
        # Check the return process
        if mplayer_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)
        
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
    
def play_files(file):
    "Play the selected file without encoding it"
    # Disable the events on main frame
    Globals.mainPanel.Enable(False)
    try:
        # Prepare the input file to be usable by mplayer
        if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
            mpFile = file.split()
        else:
            mpFile = [ file ]
        
        # Play the file with mplayer
        mplayer_proc = subprocess.Popen(
            Globals.ListUnicodeEncode(['mplayer']+mpFile), 
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            # On Windows when running under py2exe it is 
            # necessary to define stdin
            stdin=subprocess.PIPE,shell=Globals.shell(),
            universal_newlines=True)
        mplayer_output = mplayer_proc.communicate()[0]
        # Check the return process
        if mplayer_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)
        
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
    except Exception, e:
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
        # Send the exception to the FilesPanel
        raise e
    
def show_information(file, parent):
    "Displays information about a media source"
    
    # Prepare the input file to be usable by mplayer
    if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
        mpFile = file.split()
    else:
        mpFile = [ file ]
            
    # Get the media information from mplayer
    mplayer_proc = subprocess.Popen(
        Globals.ListUnicodeEncode(['mplayer','-frames','0','-vo','null','-ao','null','-identify']+mpFile),
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        # On Windows when running under py2exe it is 
            # necessary to define stdin
            stdin=subprocess.PIPE,shell=Globals.shell(),
        universal_newlines=True)
    mplayer_output = mplayer_proc.communicate()[0]
    # Check the return process
    if mplayer_proc.wait() != 0:
        raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)
    
    # Show a dialog to the user
    dialog = OutputTextDialog(parent, mplayer_output, 
        _(u'Information about %s') % os.path.basename(file))
    dialog.ShowModal()
