#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         DpgImgInjector.py
# Purpose:      Insert supported wx.Image() file into an existing DPG file.
#
# Author:       Marc P. Davignon
#
# Created:
# RCS-ID:       $Id: DpgImgInjector.py $
# Copyright:    (c) 2011 Marc P. Davignon
# Licence:      GPL v3
#----------------------------------------------------------------------------

# This script performs binary injection, with no video or audio encoding.

import Globals
import Encoder

import os
import sys
import locale
import gettext
import shutil

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
    fdImage = None
    retval = 0

    try:

        # Check the input parameters
        if (len(sys.argv) < 3 or len(sys.argv) > 4):
            Syserr(_(u'ERROR: Incorrect number of parameters'))
            Syserr(_(u'USAGE: dpgimginjector input.dpg newimage.xxx [output.dpg]'))
            sys.exit(1)

        # Check the input file
        inputN = Globals.Decode(sys.argv[1])
        if not (os.path.isfile(inputN) and (os.access(inputN, os.R_OK))):
            Syserr(_(u'ERROR: The file %s can not be read') % inputN)
            sys.exit(1)

        # Check the image file
        imageN = Globals.Decode(sys.argv[2])
        if not (os.path.isfile(imageN) and (os.access(imageN, os.R_OK))):
            Syserr(_(u'ERROR: The file %s can not be read') % imageN)
            sys.exit(1)

        # Check the output file and path
        outputN = ''
        if len(sys.argv) == 4:
            outputN = Globals.Decode(sys.argv[3])
            outPath = os.path.dirname(outputN)
            outPath = os.path.abspath(outPath)
            if (os.path.isfile(outputN) and (not os.access(outputN, os.W_OK))):
                Syserr(_(u'ERROR: The file %s can not be written') % outputN)
                sys.exit(1)
            if not os.access(outPath, os.W_OK):
                Syserr(_(u'ERROR: The folder %s can not be written') % outPath)
                sys.exit(1)


        # Open input or output file
        if (outputN):
            shutil.copyfile(inputN, outputN)
            fdInput = open(outputN, 'r+b')
        else:
            fdInput = open(inputN, 'r+b')


        knownError = False
        try:
            # Read the DPG version
            versionStr = fdInput.read(4)
            if versionStr[:3] != 'DPG':
                raise Exception()
            # Use a specific message if DPG version < 4
            if int(versionStr[3]) < 4:
                knownError = True
                raise Exception(_(u'%(file)s is a DPG version %(version)s ' \
                    'file, but version 4 or better is required') % 
                    {"file": inputN, "version": versionStr[3]})

        # If the version cannot be readed, the file is not a valid DPG file
        except Exception, e:
            if knownError:
                raise e
            else:
                raise Exception(_(u'%s is not a valid DPG file') % inputN)


        # Create the temporary files
        Globals.createTemporary()

        Globals.other_thumbnail = imageN
        Encoder.conv_thumb(imageN, '', False)
        # Open the image file
        fdImage = open(Globals.TMP_THUMB, 'rb')

	# DPG0-3 Header size 36
	# DPG4 Header size 36 + 4 (THM0) = 40
	# DPG2-4 GOP Header +12 = 48 (DPG2-3) or 52 (DPG4)
	# Image Size is 98304
	# Audio start 52 + 98304 = 98356

        fdInput.seek(52, os.SEEK_SET)
        buffer = fdImage.read()
        fdInput.write(buffer)

        # Delete the temporary files
        Globals.clearTemporary()


    # Capture exceptions
    except Exception, e:
            Syserr(_(u'ERROR') + ': ' + unicode(e.args[0]))
            retval = 1
    finally:
    # Close all the files, delete temporary ones
        if fdInput:
            fdInput.close()
        if fdImage:
            fdImage.close()

    # Exit
    sys.exit(retval)
