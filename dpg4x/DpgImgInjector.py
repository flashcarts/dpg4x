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
import shutil

def DpgInject(inputN, imageN, outputN):
    # Variables used on error handling, they need to be declared
    fdOutput = None
    fdImage = None

    try:
        if not (os.path.isfile(inputN) and (os.access(inputN, os.R_OK))):
            Globals.debug(_(u'ERROR: The file %s cannot be read') % inputN)
            return 1

        if not (os.path.isfile(imageN) and (os.access(imageN, os.R_OK))):
            Globals.debug(_(u'ERROR: The file %s cannot be read') % imageN)
            return 1

        outPath = os.path.dirname(outputN)
        outPath = os.path.abspath(outPath)
        if (os.path.isfile(outputN) and (not os.access(outputN, os.W_OK))):
            Globals.debug(_(u'ERROR: The file %s cannot be written') % outputN)
            return 1
        if not os.access(outPath, os.W_OK):
            Globals.debug(_(u'ERROR: The folder %s cannot be written') % outPath)
            return 1

        # Copy file if not modifying input
        if (outputN != inputN):
            shutil.copyfile(inputN, outputN)

        fdOutput = open(outputN, 'r+b')

        knownError = False
        try:
            # Read the DPG version
            versionStr = fdOutput.read(4)
            if versionStr[:3] != 'DPG':
                raise Exception()
            # Use a specific message if DPG version < 4
            if int(versionStr[3]) < 4:
                knownError = True
                raise Exception(_(u'%(file)s is a DPG version %(version)s ' \
                    'file, but version 4 or better is required') % 
                    {"file": inputN, "version": versionStr[3]})

        # If the version cannot be read, the file is not a valid DPG file
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

        fdOutput.seek(52, os.SEEK_SET)
        buffer = fdImage.read()
        fdOutput.write(buffer)

    # Capture exceptions
    except Exception, e:
            Globals.debug(_(u'ERROR') + ': ' + unicode(e.args[0]))
            retval = 1
    finally:
    # Close all the files, delete temporary ones
        if fdOutput:
            fdOutput.close()
        if fdImage:
            fdImage.close()
        Globals.clearTemporary()
    return 0
