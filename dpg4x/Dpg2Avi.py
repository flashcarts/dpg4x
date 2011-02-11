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
import locale
import gettext
import tempfile
import struct
import subprocess

# Check if a gettext resource is available for the current LANG
# If no env variable defined, assume that i18n files are located below the top directory
i18n_dir = os.getenv('DPG4X_I18N')
if not(i18n_dir):
    i18n_dir = os.path.join(os.path.dirname(sys.argv[0]), "i18n")
# gettext will search in default directories if no other path given
if not os.path.isdir(i18n_dir):
    i18n_dir = None
                    
if not gettext.find('dpg4x', i18n_dir) and sys.platform == 'win32':
    os.environ['LANG']=locale.getdefaultlocale()[0]
if not gettext.find('dpg4x', i18n_dir):
    gettext.install('dpg4x', i18n_dir, unicode=True)
else:
    gettext.translation('dpg4x', i18n_dir).install(unicode=True)


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
    
    # Variables used on error handling, they need to be declared
    fdInput = None
    fdAudio = None
    fdVideo = None
    fdAudio_name = ""
    fdVideo_name = ""
    retval = 0

    try:
        
        
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
            print(str(e.args[0]))
            isDPGFile = False
            raise Exception(_(u'%s is not a valid DPG file') % inputN)
                
        # Extract the audio data
        fdAudio = tempfile.NamedTemporaryFile(prefix='.dpg2avi', dir=outPath, delete=False)
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
		# Windows won't let mencoder open the file twice -> close it
        fdAudio_name = fdAudio.name
        fdAudio.close()

        # Extract the video data
        fdVideo = tempfile.NamedTemporaryFile(prefix='.dpg2avi', dir=outPath, delete=False)
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
		# Windows won't let mencoder open the file twice -> close it
        fdVideo_name = fdVideo.name
        fdVideo.close()
 
	    # Join audio and video with mencoder
        mencoder_proc = subprocess.Popen(
            ['mencoder',fdVideo_name,'-audiofile',fdAudio_name,
            '-ffourcc','mpg1','-ovc','copy','-oac','copy','-o',outputN],
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT, 
            universal_newlines=True)
        mencoder_output = mencoder_proc.communicate()[0]
        # Check the return process
        if mencoder_proc.wait() != 0:
			raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)
            
    # Capture exceptions
    except Exception, e:
            Syserr(_(u'ERROR') + ': ' + str(e.args[0]))
            retval = 1
    finally:
    # Close all the files, delete temporary ones
        if fdInput:
            fdInput.close()
        if fdAudio:
            fdAudio.close()
        if os.path.exists(fdAudio_name):
            os.unlink(fdAudio_name)
        if fdVideo:
            fdVideo.close()
        if os.path.exists(fdVideo_name):
            os.unlink(fdVideo_name)
    
    # Exit
    sys.exit(retval)
