#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Dpg2Avi.py
# Purpose:      Converts DPG videos into AVI videos.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Dpg2Avi.py $
# Copyright:    (c) 2010 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# This script performs direct conversion, with no video or audio encoding.

import Globals

import os
import sys
import gettext
import tempfile
import struct
import subprocess

# Check if a gettext resource is available for the current LANG
if not gettext.find('dpg4x', os.getenv('DPG4X_I18N')):
    gettext.install('dpg4x', os.getenv('DPG4X_I18N'), unicode=True)
else:
    gettext.translation('dpg4x', os.getenv('DPG4X_I18N')).install(unicode=True)

def Sysout(message):
    "Shows a message in the standart output"
    sys.stderr.write((message+"\n").encode(
        sys.getfilesystemencoding(),'replace'))

def Syserr(message):
    "Shows a message in the error output"
    sys.stderr.write((message+"\n").encode(
        sys.getfilesystemencoding(),'replace'))

# Main function
if __name__ == '__main__':
    
    try:
        
        # Variables used on error handling, they need to be declared
        fdInput = None
        fdAudio = None
        fdVideo = None
        
        # Check if mplayer is available
        if not Globals.which('mencoder'):
            message = _(u'%s not found in PATH. Please install it.') % 'mencoder'
            # Show an error in the console
            Syserr(_(u'ERROR') + ': ' + message)
            sys.exit(1)
        
        # Check the input parameters
        if len(sys.argv) != 3:
            Syserr(_(u'ERROR: Incorrect number of parameters'))
            Syserr(_(u'USAGE: dpg2avi input.dpg output.avi'))
            sys.exit(1)
            
        # Check the input file
        inputN = Globals.Decode(sys.argv[1])
        if not (os.path.isfile(inputN) and (os.access(inputN, os.R_OK))):
            Syserr(_(u'ERROR: The file %s can not be read') % inputN)
            sys.exit(1)

        # Check the output file and path
        outputN = Globals.Decode(sys.argv[2])
        outPath = os.path.dirname(outputN)
        outPath = os.path.abspath(outPath)
        if os.path.isfile(outputN):
            Syserr(_(u'ERROR: The file %s already exists') % outputN)
            sys.exit(1)
        if not os.access(outPath, os.W_OK):
            Syserr(_(u'ERROR: The folder %s can not be written') % outPath)
            sys.exit(1)
            
        # Open input file
        fdInput = open(inputN, 'rb')
        
        try:
            # Read the DPG version
            versionStr = fdInput.read(4)
            if versionStr[:3] != 'DPG':
                raise Exception()
            version = int(versionStr[3])
        
            # Read where the audio file starts
            fdInput.seek(20, os.SEEK_SET)
            audioStart = struct.unpack("<l", fdInput.read(4))[0]
            # Read the lenght of the audio file
            audioLenght = struct.unpack("<l", fdInput.read(4))[0]
            # Read where the video file starts
            videoStart = struct.unpack("<l", fdInput.read(4))[0]
            # Read the lenght of the video file
            videoLenght = struct.unpack("<l", fdInput.read(4))[0]
            
        # An exception in this code means the file is not DPG
        except Exception, e:
            print(e.message)
            isDPGFile = False
            raise Exception(_(u'%s is not a valid DPG file') % inputN)
                
        # Extract the audio data
        fdAudio = tempfile.NamedTemporaryFile(prefix='.dpg2avi', dir=outPath)
        fdInput.seek(audioStart, os.SEEK_SET)
        readed = 0
        while readed < audioLenght:
            # Max buffer lenght
            bufferLenght = 1024
            remain = audioLenght - readed
            # Adjut the buffer lenght
            if bufferLenght > remain:
                bufferLenght = remain
            buffer = fdInput.read(bufferLenght)
            fdAudio.write(buffer)
            readed += bufferLenght
        fdAudio.flush()
        
        # Extract the video data
        fdVideo = tempfile.NamedTemporaryFile(prefix='.dpg2avi', dir=outPath)
        fdInput.seek(videoStart, os.SEEK_SET)
        readed = 0
        while readed < videoLenght:
            # Max buffer lenght
            bufferLenght = 1024
            remain = videoLenght - readed
            # Adjut the buffer lenght
            if bufferLenght > remain:
                bufferLenght = remain
            buffer = fdInput.read(bufferLenght)
            fdVideo.write(buffer)
            readed += bufferLenght
        fdVideo.flush()

        # Join audio and video with mencoder
        mencoder_proc = subprocess.Popen(
            ['mencoder',fdVideo.name,'-audiofile',fdAudio.name,
            '-ovc','copy','-oac','copy','-o',outputN],
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT, 
            universal_newlines=True)
        mencoder_output = mencoder_proc.communicate()[0]
        # Check the return process
        if mencoder_proc.wait() != 0:
            raise Exception(_(u'Error on mencoder')+': '+mencoder_output)

        # Close the files
        if fdInput:
            fdInput.close()
        if fdAudio:
            fdAudio.close()
        if fdVideo:
            fdVideo.close()
            
    # Capture exceptions
    except Exception, e:
            Syserr(_(u'ERROR') + ': ' + e.message)
            # Close the files
            if fdInput:
                fdInput.close()
            if fdAudio:
                fdAudio.close()
            if fdVideo:
                fdVideo.close()
            sys.exit(1)
    
    # Clean exit
    sys.exit(0)
        
