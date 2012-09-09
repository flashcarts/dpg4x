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

import os.path
import sys
import tempfile
import struct
import subprocess

def Dpg2Avi(inputN, outputN = None):
    # Variables used on error handling, they need to be declared
    fdInput = None
    fdAudio = None
    fdVideo = None
    fdAudio_name = ""
    fdVideo_name = ""
    retval = 0

    if not outputN:
        # Check if the file already exists and choose another
        # We'll add a ~number at the end.
        version = 1
        outputN = inputN[:-4] + '.avi'
        while os.path.exists(outputN):
            if version == 1:
                outputN = outputN[:-4] + '~' + str(version) + '.avi'
            else:
                outputN = outputN[:outputN.rfind('~')+1] + str(version) + '.avi'
            version += 1       

    try:      
        if not (os.path.isfile(inputN) and (os.access(inputN, os.R_OK))):
            Globals.debug(_(u'ERROR: The file %s can not be read') % inputN)
            sys.exit(1)

        # Check the output file and path
        outPath = os.path.dirname(outputN)
        outPath = os.path.abspath(outPath)
        if os.path.isfile(outputN):
            Globals.debug(_(u'ERROR: The file %s already exists') % outputN)
            sys.exit(1)
        if not os.access(outPath, os.W_OK):
            Globals.debug(_(u'ERROR: The folder %s can not be written') % outPath)
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
            # print(unicode(e.args[0]))
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
            Globals.ListUnicodeEncode(['mencoder',fdVideo_name,'-audiofile',fdAudio_name,
            '-ffourcc','mpg1','-ovc','copy','-oac','copy','-o',outputN]),
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT, 
            universal_newlines=True)
        mencoder_output = mencoder_proc.communicate()[0]
        # Check the return process
        if mencoder_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)
            
    # Capture exceptions
    except Exception, e:
            Globals.debug(_(u'ERROR') + ': ' + unicode(e.args[0]))
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
    return retval
