# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Globals.py
# Purpose:      Source file with global variables and functions.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Globals.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import ConfigurationManager

import os
import sys
import string
import tempfile
import shutil

###############
## VARIABLES ##
###############

# Configuration files
FILECONFIG = [os.path.expanduser("~/.config/dpg4x/config.ini")]
# User config file
USERFILECONFIG = FILECONFIG[0]

# Temporary files
TMP_AUDIO = None
TMP_FIFO = None
TMP_VIDEO = None
TMP_HEADER = None
TMP_GOP = None
TMP_STAT = None
TMP_THUMB = None
TMP_SHOT = None
TMP_DIVX2PASS = None
	
# Option panels
mainPanel = None
filesPanel = None
videoPanel = None
audioPanel = None
subtitlesPanel = None
otherPanel = None

# General options
dpg_version = 4
dpg_quality = 'normal'
# Used to remember the last DVD/VCD device used
dpg_vcddevice = '/dev/cdrom'
dpg_dvddevice = '/dev/dvd'

# Video options
video_keepaspect = False
video_width = 256
video_height = 192
video_track = 0
video_autotrack = True
video_bitrate = 288
video_fps = 15
video_autofps = True
video_pixel = 3
# 0 RGB15
# 1 RGB18
# 2 RGB21
# 3 RGB24 

# Audio options
audio_codec = 'mp2'
audio_track = 0
audio_autotrack = True
audio_bitrate_mp2 = 128
audio_bitrate_vorbis = 128
audio_frequency = 32000
audio_normalize = False
audio_mono = False

# Subtitle options
subtitles_source = 'auto'
subtitles_track = 0
subtitles_file = ''
subtitles_font = 'Sans'
subtitles_encoding = sys.getfilesystemencoding()

# Other output
other_output = ''
other_temporary = '/tmp'
other_thumbnail = ''
other_previewsize = 10


###############
## FUNCTIONS ##
###############

def debug(message):
    "Shows a message in the error output"
    sys.stderr.write((message+"\n").encode(
        sys.getfilesystemencoding(),'replace'))

def Encode(text):
    "Encode text to be system-encoding compatible"
    return text.encode(sys.getfilesystemencoding(),'replace')

def Decode(text):
    "Decode text to be system-encoding compatible"
    return text.decode(sys.getfilesystemencoding(),'replace')
        
def CreateFolder(dir):
    "Create a folder with full path"
    if not os.path.isdir(dir):
        chunks = dir.split("/")
        subchunk = "/"
        for chunk in chunks:
            subchunk = os.path.join(subchunk, chunk)
            if not os.path.isdir(subchunk):
                #os.mkdir(subchunk, stat.S_IRWXU) UMASK?
                os.mkdir(subchunk)

# Stolen from Noah Spurrier's pexpect. Thank you Noah!
# Pexpect it's a great library and I use it often. 
# But now, I just need this function, so I'll try to save on dependencies...
def which (filename):

    """This takes a given filename; tries to find it in the environment path;
    then checks if it is executable. This returns the full path to the filename
    if found and executable. Otherwise this returns None."""

    # Special case where filename already contains a path.
    if os.path.dirname(filename) != '':
        if os.access (filename, os.X_OK):
            return filename

    if not os.environ.has_key('PATH') or os.environ['PATH'] == '':
        p = os.defpath
    else:
        p = os.environ['PATH']

    # Oddly enough this was the one line that made Pexpect
    # incompatible with Python 1.5.2.
    #pathlist = p.split (os.pathsep)
    pathlist = string.split (p, os.pathsep)

    for path in pathlist:
        f = os.path.join(path, filename)
        if os.access(f, os.X_OK):
            return f
    return None

def concat(out,*files):
    "Concatenate a list of files"
    outfile = open(out,'w')
    for name in files:
        outfile.write( open(name).read() )
    outfile.close()
    
def fillString(string, length):
    "Fills a string with spaces until length is reached"
    stringAux = string
    while len(stringAux) < length:
        stringAux = ' ' + stringAux
        if len(stringAux) < length:
            stringAux = stringAux + ' '
    return stringAux
    
def createTemporary():
    "Create the temporary files needed to encode"
    
    # Folder for the temporary files
    global other_temporary
    tmpDir = other_temporary
    
    # Audio temporary file
    global TMP_AUDIO
    fd,TMP_AUDIO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Audio temporary fifo - maybe there is a better way to do it...
    global TMP_FIFO
    fd,TMP_FIFO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    os.remove(TMP_FIFO)
    os.mkfifo(TMP_FIFO,0600)
	# Video temporary file
    global TMP_VIDEO
    fd,TMP_VIDEO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
	# Header temporary file
    global TMP_HEADER
    fd,TMP_HEADER = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
	# GOP offsets temporaries
	# Only needed with dpg_version >= 2
    global dpg_version
    global TMP_GOP
    global TMP_STAT
    if dpg_version >= 2:
        fd,TMP_GOP = tempfile.mkstemp(dir=tmpDir)
        os.close(fd)
    # TMP_STAT always needed for frames calculation
    fd,TMP_STAT = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Thumbnail temporary files
    global other_thumbnail
    global TMP_THUMB
    global TMP_SHOT
    fd,TMP_THUMB = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Only needed on autogenerate
    if not other_thumbnail:
        TMP_SHOT = tempfile.mkdtemp(dir=tmpDir)
    # Divx 2-pass log file
    # Only needed for very high quality encode
    global TMP_DIVX2PASS
    if dpg_quality == 'doublepass':
        TMP_DIVX2PASS = tempfile.mkdtemp(dir=tmpDir)
        
def clearTemporary():
    "Delete the temporary files"
    return
    try:
        # Audio temporary file
        global TMP_AUDIO
        if TMP_AUDIO and os.path.isfile(TMP_AUDIO):
            os.remove(TMP_AUDIO)
        # Audio temporary fifo
        global TMP_FIFO
        if TMP_FIFO and os.path.exists(TMP_FIFO):
            os.remove(TMP_FIFO)
        # Video temporary file
        global TMP_VIDEO
        if TMP_VIDEO and os.path.isfile(TMP_VIDEO):
            os.remove(TMP_VIDEO)
        # Header temporary file
        global TMP_HEADER
        if TMP_HEADER and os.path.isfile(TMP_HEADER):
            os.remove(TMP_HEADER)
        # GOP offsets temporaries
        global TMP_GOP
        global TMP_STAT
        if TMP_GOP and os.path.isfile(TMP_GOP):
            os.remove(TMP_GOP)
        if TMP_STAT and os.path.isfile(TMP_STAT):
            os.remove(TMP_STAT)
        # Thumbnail temporary files
        global TMP_THUMB
        global TMP_SHOT
        if TMP_THUMB and os.path.isfile(TMP_THUMB):
            os.remove(TMP_THUMB)
        # Note that TMP_SHOT is a folder, not a file
        if TMP_SHOT and os.path.isdir(TMP_SHOT):
            shutil.rmtree(TMP_SHOT, ignore_errors = True)
        # Same with TMP_DIVX2PASS
        global TMP_DIVX2PASS
        if TMP_DIVX2PASS and os.path.isdir(TMP_DIVX2PASS):
            shutil.rmtree(TMP_DIVX2PASS, ignore_errors = True)
            
    # Warn if there is a problem when deleting files
    except Exception, e:
        debug(_(u'WARNING: Temporary files were not properly deleted:') + '' \
            u' ' + str(e.args[0]))
            
            
# Load the configuration file
ConfigurationManager.loadConfiguration()

