# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Encoder.py
# Purpose:      Performs the encoding duties.
#
# Author:       Félix Medrano Sanz
#
# Created:
# RCS-ID:       $Id: Encoder.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# The following code is based on the dpgconv script.
# Thank you for all it's creators! See the README file for more details.

import Globals
import ConfigurationManager
import CustomProgressDialog
import Dpg2Avi
import DpgHeader
import DpgThumbnail

import re
import os
import stat
import subprocess
import struct
import wx
import shutil
import array
import signal
import sys
import tempfile
import threading

# Try to load the Python Image Library, if available
pilAvailable = True
try:
    from PIL import Image
except Exception:
    pilAvailable = False

def encode_video(file, filename, preview=False):
    "Encodes the video stream"

    global progress
    # Progress dialog disabled on preview
    if not preview:
        abort = progress.doProgress(1,
            filename + u' - ' + _(u'Starting encoding process'))
        # Abort the process if the user requests it
        if abort:
            raise Exception(_(u'Process aborted by user.'))

    # Prepare the input file to be usable by mplayer
    if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
        mpFile = file.split()
    else:
        mpFile = [ file ]

    # Get the aspect ratio if keepaspect selected
    if Globals.video_keepaspect:
        # RE to obtain the video aspect
        aspectRE = re.compile ("\nID_VIDEO_ASPECT=([0-9.]*)\n")
        # Get the video size from mplayer
        mplayer_proc = subprocess.Popen(
            Globals.ListUnicodeEncode(['mplayer','-frames','1','-vo','null','-ao','null','-identify']+mpFile),
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            # On Windows when running under py2exe it is
            # necessary to define stdin
            stdin=subprocess.PIPE,shell=Globals.shell(),
            universal_newlines=True)
        mplayer_output = mplayer_proc.communicate()[0]
        # Check the return process
        if mplayer_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)
        # In my tests, the video aspect can be shown more than once,
        # being the later the best one. So I'll use info[-1]
        info = aspectRE.findall(mplayer_output)
        if info:
            ratio = float(info[-1])
            # On MacOSX an older version of mplayer dev-CVS-060307-04:23-4.0.1
            # failed to return anything but 0.0000. MacOSX Fink mplayer
            # 1.0rc2-4.2.1 did not have this issue.
            # Worse, some files just refuse to return a ratio value
            # "ID_VIDEO_ASPECT=0.0000" and
            # "Movie-Aspect is undefined - no prescaling applied."
            # Tracker Bug 3306088 by Matt Kasdorf: float division by zero
            # To fix use WIDTH and HEIGHT instead.
            if ratio == 0:
                widthRE = re.compile ("\nID_VIDEO_WIDTH=([0-9.]*)\n")
                heightRE = re.compile ("\nID_VIDEO_HEIGHT=([0-9.]*)\n")
                ratio = round(float(widthRE.findall(mplayer_output)[-1])/float(heightRE.findall(mplayer_output)[-1]), 4)

            # Get the best size with the obtained ratio
            Globals.video_width = 256
            Globals.video_height = int(256.0/ratio)

    # The height must be between 16 and 192
    if Globals.video_height < 16:
        Globals.video_height = 16
    if Globals.video_height > 192:
        Globals.video_height = 192

    # Track 3085578 by Marc P. Davignon
    # Force video height to be an integer multiple of 16
    modVideo_height = Globals.video_height % 16
    # Round up
    if modVideo_height >= 8:
        Globals.video_height = Globals.video_height + 16 - modVideo_height
    # Round down
    elif modVideo_height > 0:
        Globals.video_height = Globals.video_height - modVideo_height

    # Calculate the FPS if auto FPS set
    if Globals.video_autofps:
        # This gives 15fps for 4x3 aspect and 20fps for panoramic
        Globals.video_fps = int(
            737280/(Globals.video_width*Globals.video_height))
        # With double pass FPS can't be lower than 24
        if Globals.dpg_quality == 'doublepass':
            if Globals.video_fps < 24:
                Globals.video_fps = 24
        # Don't allow values higher than 24
        if Globals.video_fps > 24:
            Globals.video_fps = 24

    # Prepare the pixel format string
    # Does this really work for anyone? Not for me!
    if Globals.video_pixel == 3:
        v_pixelformat = "format=rgb24"
    elif Globals.video_pixel == 2:
        v_pixelformat = "format=rgb21"
    elif Globals.video_pixel == 1:
        v_pixelformat = "format=rgb18"
    elif Globals.video_pixel == 0:
        v_pixelformat = "format=rgb15"

    # MacOSX mencoder 1.0rc2-4.2.1 segment faults when cmp=x:subcmp=x:precmp=x
    # is set above 0. Compared a couple videos created using Linux set to 6
    # and although the file sizes differed <1MB the video quality appeared to
    # be equal.
    defcmp='0'

    # Options to process with extra high quality (double pass)
    if Globals.dpg_quality == 'doublepass':
        if sys.platform != 'darwin':
            defcmp='6'
        v_cmd = mpFile+['-v','-ofps',str(Globals.video_fps),'-sws','9','-vf',
        v_pixelformat + ',' \
        'scale='+str(Globals.video_width)+':'+str(Globals.video_height)+':::3,harddup',
        '-nosound','-ovc','lavc','-lavcopts',
        'vcodec=mpeg1video:vstrict=-2:mbd=2:trell:cbp:mv0:vmax_b_frames=2:' \
        'cmp='+defcmp+':subcmp='+defcmp+':precmp='+defcmp+':dia=4:predia=4:bidir_refine=4:' \
        'mv0_threshold=0:last_pred=3:vbitrate='+str(Globals.video_bitrate),
        '-o',Globals.TMP_VIDEO,'-of','rawvideo']
        # Go to the directory where the divx2pass.log file will be stored
        current_path = os.getcwd()
        # Handle when Globals.createTemporary() has already been called and
        # the first file was not doublepass.
        if Globals.TMP_DIVX2PASS is None:
            Globals.TMP_DIVX2PASS = tempfile.mkdtemp(dir=Globals.other_temporary)
        # When encoding more than one doublepass file, make sure the path
        # exists to avoid error. See shutil.rmtree at the end of this function
        if not (os.path.exists(Globals.TMP_DIVX2PASS)):
            os.makedirs(Globals.TMP_DIVX2PASS)
        os.chdir(Globals.TMP_DIVX2PASS)

    # Options to process with high quality
    elif Globals.dpg_quality == 'high':
        if sys.platform != 'darwin':
            defcmp='6'
        v_cmd = mpFile+['-v','-ofps',str(Globals.video_fps),'-sws','9','-vf',
        v_pixelformat + ',' \
        'scale='+str(Globals.video_width)+':'+str(Globals.video_height)+':::3,harddup',
        '-nosound','-ovc','lavc','-lavcopts',
        'vcodec=mpeg1video:vstrict=-2:mbd=2:trell:cbp:mv0:keyint=15:cmp='+defcmp+':subcmp='+defcmp+':' \
        'precmp='+defcmp+':dia=3:predia=3:last_pred=3:vbitrate='+str(Globals.video_bitrate),
        '-o',Globals.TMP_VIDEO,'-of','rawvideo']
    # Options to process with low quality
    elif Globals.dpg_quality == 'low':
        v_cmd = mpFile+['-v','-ofps',str(Globals.video_fps),'-vf',
        v_pixelformat + ',' \
        'scale='+str(Globals.video_width)+':'+str(Globals.video_height)+',harddup',
        '-nosound','-ovc','lavc','-lavcopts',
        'vcodec=mpeg1video:vstrict=-2:keyint=15:vbitrate=' \
        ''+str(Globals.video_bitrate),'-o',Globals.TMP_VIDEO,'-of','rawvideo']
    # Options to process with normal quality
    else :
        if sys.platform != 'darwin':
            defcmp='2'
        v_cmd = mpFile+['-v','-ofps',str(Globals.video_fps),'-sws','9','-vf',
        v_pixelformat + ',' \
        'scale='+str(Globals.video_width)+':'+str(Globals.video_height)+':::3,harddup',
        '-nosound','-ovc','lavc','-lavcopts',
        'vcodec=mpeg1video:vstrict=-2:mbd=2:trell:cbp:mv0:keyint=15:cmp='+defcmp+':subcmp='+defcmp+':' \
        'precmp='+defcmp+':vbitrate='+str(Globals.video_bitrate),'-o',Globals.TMP_VIDEO,
        '-of','rawvideo']

    # Select the video track
    if not Globals.video_autotrack:
        v_cmd = v_cmd + ['-vid',str(Globals.video_track)]


    # Include the subtitles

    # Select subtitles track from video
    if Globals.subtitles_source == 'sid':
        v_cmd = ['-sid',str(Globals.subtitles_track)] + v_cmd
    # Select subtitles file
    elif Globals.subtitles_source == 'file':
        v_cmd = ['-sub',Globals.subtitles_file] + v_cmd
    # Disable the subtitles
    elif Globals.subtitles_source == 'disable':
        v_cmd = ['-sid','999'] + v_cmd

    # Set the encoding for subtitles
    if Globals.subtitles_encoding:
        v_cmd = ['-subcp',Globals.subtitles_encoding] + v_cmd
    # Set the font for subtitles
    if Globals.subtitles_font:
        v_cmd = ['-font',Globals.subtitles_font] + v_cmd

    # Encode only a small chunk on preview
    if preview:
        v_cmd = ['-endpos',str(Globals.other_previewsize)] + v_cmd

    # Prepare the double pass if extra high quality selected
    v_cmd = ['mencoder'] + v_cmd
    if Globals.dpg_quality == 'doublepass':
        # List size can vary, be sure option parameters follow the proper option
        lavc_opt_index = v_cmd.index('-lavcopts')
        lavc_opt_index += 1
        v_cmd_two = v_cmd[:]
        v_cmd[lavc_opt_index] += ':vpass=1:turbo:vb_strategy=2:vrc_maxrate=500:' \
            'vrc_minrate=0:vrc_buf_size=327:intra_matrix=8,9,12,22,26,27,29,' \
            '34,9,10,14,26,27,29,34,37,12,14,18,27,29,34,37,38,22,26,27,31,' \
            '36,37,38,40,26,27,29,36,39,38,40,48,27,29,34,37,38,40,48,58,29,' \
            '34,37,38,40,48,58,69,34,37,38,40,48,58,69,79:inter_matrix=16,18,' \
            '20,22,24,26,28,30,18,20,22,24,26,28,30,32,20,22,24,26,28,30,32,' \
            '34,22,24,26,30,32,32,34,36,24,26,28,32,34,34,36,38,26,28,30,32,' \
            '34,36,38,40,28,30,32,34,36,38,42,42,30,32,34,36,38,40,42,44'
        v_cmd_two[lavc_opt_index] += ':vpass=2:vrc_maxrate=500:vrc_minrate=0:' \
            'vrc_buf_size=327:keyint=15:intra_matrix=8,9,12,22,26,27,29,34,9,' \
            '10,14,26,27,29,34,37,12,14,18,27,29,34,37,38,22,26,27,31,36,37,' \
            '38,40,26,27,29,36,39,38,40,48,27,29,34,37,38,40,48,58,29,34,37,' \
            '38,40,48,58,69,34,37,38,40,48,58,69,79:inter_matrix=16,18,20,22,' \
            '24,26,28,30,18,20,22,24,26,28,30,32,20,22,24,26,28,30,32,34,22,' \
            '24,26,30,32,32,34,36,24,26,28,32,34,34,36,38,26,28,30,32,34,36,' \
            '38,40,28,30,32,34,36,38,42,42,30,32,34,36,38,40,42,44'

    # Execute mencoder
    Globals.debug('ENCODE VIDEO: ' + `v_cmd`)
    proc = subprocess.Popen(Globals.ListUnicodeEncode(v_cmd),stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,shell=Globals.shell(),
        stderr=subprocess.STDOUT, universal_newlines=True)
    # Show progress
    progRE = re.compile ("f \((.*)%\)")
    mencoder_output = ''
    localProgress = 1
    for line in proc.stdout:
        mencoder_output += line
        percent = progRE.search( line )
        if percent:
            # The size of the video progress will be 1X
            shownProgress = int(percent.group(1))
            diffProgress = int(percent.group(1)) - localProgress
            localProgress = int(percent.group(1))
            userProgress = str(shownProgress)
            # If we are in doublepass mode, we have encoded only the half
            if Globals.dpg_quality == 'doublepass':
                userProgress = str(shownProgress/2)
            # Progress dialog disabled on preview
            if not preview:
                abort = progress.doProgress(diffProgress,
                    filename + ' - ' + _(u'Encoding in progress') + ': ' +
                    userProgress + '%')
                # Abort the process if the user requests it
                if abort:
                    # os.kill() only works on Windows using Python 2.7 and
                    # greater. Not critical to creating DPG files so this
                    # could be left out.
                    if sys.platform == 'win32' and sys.version_info < (2, 7):
                        subprocess.Popen("taskkill /F /T /PID %i"%proc.pid , shell=Globals.shell())
                    else:
                        os.kill(proc.pid,signal.SIGTERM)
                    raise Exception(_(u'Process aborted by user.'))

    # Check the return process
    if proc.wait() != 0:
        raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)

    # Execute the second pass if necessary
    if Globals.dpg_quality == 'doublepass':
        Globals.debug('ENCODE VIDEO: ' + `v_cmd_two`)
        proc = subprocess.Popen(Globals.ListUnicodeEncode(v_cmd_two),stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,shell=Globals.shell(),
            stderr=subprocess.STDOUT, universal_newlines=True)
        # Show progress
        mencoder_output = ''
        localProgress = 1
        for line in proc.stdout:
            mencoder_output += line
            percent = progRE.search( line )
            if percent:
                # The size of the video progress will be 1X
                shownProgress = int(percent.group(1))
                diffProgress = int(percent.group(1)) - localProgress
                localProgress = int(percent.group(1))
                # Because we are in doublepass mode, we have encoded only the half
                # But add a 50% because the 1st pass is done
                userProgress = str(shownProgress/2 + 50)
                # Progress dialog disabled on preview
                if not preview:
                    abort = progress.doProgress(diffProgress,
                        filename + ' - ' + _(u'Encoding in progress') + ': ' +
                        userProgress + '%')
                    # Abort the process if the user requests it
                    if abort:
                        if sys.platform == 'win32' and sys.version_info < (2, 7):
                            subprocess.Popen("taskkill /F /T /PID %i"%proc.pid , shell=Globals.shell())
                        else:
                            os.kill(proc.pid,signal.SIGTERM)
                        raise Exception(_(u'Process aborted by user.'))

        # Check the return process
        if proc.wait() != 0:
            raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)
        # Delete the divx2pass.log temporary file
        os.chdir(current_path)
        shutil.rmtree(Globals.TMP_DIVX2PASS, ignore_errors = True)

class SoxThread(threading.Thread):
    "Thread to execute the sox process"
    # This is neccesary because if we execute mplayer and sox at the same
    # time and use a pipe, we don't need aditional temporary space and
    # the process may be faster

    def __init__(self, params):
        "Constructor for SoxThread"
        threading.Thread.__init__(self)
        self.params = params
        self.errorMessage = None
        self.stop = False

    def stopThread(self):
        "Stop the run function"
        self.stop = True

    def getErrorMessage(self):
        "Returns the error message"
        return self.errorMessage

    def run(self):
        "Running code for the tread"

        try:
            proc_sox = subprocess.Popen(Globals.ListUnicodeEncode(self.params), stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,shell=Globals.shell(),
                stderr=subprocess.STDOUT, universal_newlines=True)
            # Monitor execution
            sox_output = ''
            for line in proc_sox.stdout:
                sox_output += line
                # Check if the encoding must continue
                if self.stop:
                    proc_sox.terminate()
                    raise Exception(_(u'Audio encoding stopped'))
            # Check the return process
            if proc_sox.wait() != 0:
                raise Exception(_(u'ERROR ON SOX')+'\n\n'+sox_output)
        # Manage posible exceptions on the thread
        except Exception, e:
            self.errorMessage = unicode(e.args[0])

class EncodeAudioThread(threading.Thread):
    "Thread to encode the audio stream"

    def __init__(self, file, filename, preview=False):
        "Constructor for EncodeAudioThread"
        threading.Thread.__init__(self)
        self.file = file
        self.errorMessage = None
        self.stop = False
        self.preview = preview

    def getErrorMessage(self):
        "Returns the error message"
        return self.errorMessage

    def stopThread(self):
        "Stop the run function"
        self.stop = True

    def run(self):
        "Running code for the tread"

        try:
            sox_thread = None
            file = self.file

            # Prepare the input file to be usable by mplayer
            if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
                mpFile = file.split()
            else:
                mpFile = [ file ]

            # Check if the encoding must continue
            if self.stop:
                raise Exception(_(u'Audio encoding stopped'))

            # When mp2 audio codec is selected, we use mencoder to perform
            # all the process
            a_cmd = ['mencoder']+mpFile+['-v','-of','rawaudio','-oac',
                'lavc','-ovc','copy','-lavcopts',
                'acodec=mp2:abitrate='+str(Globals.audio_bitrate_mp2),
                '-o',Globals.TMP_AUDIO]

            # When gms or ogg is selected, we use mplayer+sox
            m_cmd = ['mplayer']+mpFile+['-v','-vo','null','-ao',
                'pcm:fast:file='+Globals.TMP_FIFO]
            s_cmd = ['sox','-V3','-S',Globals.TMP_FIFO]

            # Option to normalize the volume
            normalize = ''
            if Globals.audio_normalize:
                normalize = ',volnorm'
                s_cmd = s_cmd + ['--norm']

            # Get the number of audio channels for video source
            mplayer_proc = subprocess.Popen(
                Globals.ListUnicodeEncode(['mplayer','-frames','0','-vo','null','-ao','null','-identify']+mpFile),
                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,shell=Globals.shell(),
                universal_newlines=True)
            mplayer_output = mplayer_proc.communicate()[0]
            # Check the return process
            if mplayer_proc.wait() != 0:
                raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)
            # Identify the info by searchinb the ID_AUDIO_NCH tag
            nchanRE = re.compile ("\nID_AUDIO_NCH=([0-9]*)\n")
            nchanSE = nchanRE.search(mplayer_output)
            if nchanSE:
                nchan = nchanSE.group(1)

                # Use the same number of channels for input and output
                # But do not use more than 2 channels
                # DPGV0 only supports mono audio
                if (not Globals.audio_mono) and (Globals.dpg_version > 0):
                    if nchan > 2:
                        a_cmd = a_cmd + ['-srate',str(Globals.audio_frequency),'-af',
                            'channels=2,lavcresample='+str(Globals.audio_frequency)+normalize]
                        s_cmd = s_cmd + ['-c','2','-r',str(Globals.audio_frequency)]
                    else:
                        a_cmd = a_cmd + ['-srate',str(Globals.audio_frequency),'-af',
                            'lavcresample='+str(Globals.audio_frequency)+normalize]
                        s_cmd = s_cmd + ['-r',str(Globals.audio_frequency)]
                    # Update the audio_mono variable for the header process
                    if nchan == 1:
                        Globals.audio_mono = True
                # If the force mono option is set (or DPG0), use only one
                else:
                    a_cmd = a_cmd + ['-srate',str(Globals.audio_frequency),'-af',
                        'channels=1,lavcresample='+str(Globals.audio_frequency)+normalize]
                    s_cmd = s_cmd + ['-c','1','-r',str(Globals.audio_frequency)]

            # When error, include the output in the exception
            else:
                raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)

            # Select the audio track
            if not Globals.audio_autotrack:
                a_cmd = a_cmd + ['-aid',str(Globals.audio_track)]
                m_cmd = m_cmd + ['-aid',str(Globals.audio_track)]

            # Encode only a small chunk on preview
            if self.preview:
                a_cmd = a_cmd + ['-endpos',str(Globals.other_previewsize)]
                m_cmd = m_cmd + ['-endpos',str(Globals.other_previewsize)]

            # If mp2 codec is selected, execute mencoder
            if Globals.audio_codec == 'mp2':
                Globals.debug('ENCODE AUDIO: ' + `a_cmd`)
                proc = subprocess.Popen(Globals.ListUnicodeEncode(a_cmd), stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,shell=Globals.shell(),
                    stderr=subprocess.STDOUT, universal_newlines=True)
                # Monitor execution
                mencoder_output = ''
                for line in proc.stdout:
                    mencoder_output += line
                    # Check if the encoding must continue
                    if self.stop:
                        raise Exception(_(u'Audio encoding stopped'))
                # Check the return process
                if proc.wait() != 0:
                    raise Exception(_(u'ERROR ON MENCODER')+'\n\n'+mencoder_output)

            # If gsm or ogg is selected, execute mplayer and sox
            else:

                # SOX
                # Add the format options
                if Globals.audio_codec == 'vorbis':
                    format = ['-t','ogg','-C']
                    if Globals.audio_bitrate_vorbis == 45:
                        format = format + ['-1']
                    if Globals.audio_bitrate_vorbis == 64:
                        format = format + ['0']
                    if Globals.audio_bitrate_vorbis == 80:
                        format = format + ['1']
                    if Globals.audio_bitrate_vorbis == 96:
                        format = format + ['2']
                    if Globals.audio_bitrate_vorbis == 112:
                        format = format + ['3']
                    if Globals.audio_bitrate_vorbis == 128:
                        format = format + ['4']
                    if Globals.audio_bitrate_vorbis == 160:
                        format = format + ['5']
                    if Globals.audio_bitrate_vorbis == 192:
                        format = format + ['6']
                    if Globals.audio_bitrate_vorbis == 224:
                        format = format + ['7']
                    if Globals.audio_bitrate_vorbis == 256:
                        format = format + ['8']
                    if Globals.audio_bitrate_vorbis == 320:
                        format = format + ['9']
                    if Globals.audio_bitrate_vorbis == 500:
                        format = format + ['10']
                else:
                    format = ['-t','wav','-e','gsm-full-rate']
                s_cmd = s_cmd + format + [Globals.TMP_AUDIO]
                # Execute sox through a trhead
                Globals.debug('ENCODE AUDIO: ' + `s_cmd`)
                sox_thread = SoxThread(s_cmd)
                sox_thread.start()

                # MPLAYER
                Globals.debug('ENCODE AUDIO: ' + `m_cmd`)
                proc = subprocess.Popen(Globals.ListUnicodeEncode(m_cmd), stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,shell=Globals.shell(),
                    stderr=subprocess.STDOUT, universal_newlines=True)
                # Monitor execution
                mplayer_output = ''
                for line in proc.stdout:
                    mplayer_output += line
                    # Check if the encoding must continue
                    if self.stop:
                        proc.terminate()
                        raise Exception(_(u'Audio encoding stopped'))
                # Check the return process
                if proc.wait() != 0:
                    raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)

                # Check for errors in SOX
                sox_thread.join()
                threadError = sox_thread.getErrorMessage()
                if threadError:
                    raise Exception(threadError)

        # Manage posible exceptions on the thread
        except Exception, e:
            self.errorMessage = unicode(e.args[0])
            # Stop the sox thread
            if sox_thread:
                sox_thread.stopThread()

def mpeg_stat(filename):
    "Generate file with GOP offsets and calculate frames"

    # Increase progress
    global progress
    abort = progress.doProgress(1,
        filename + ' - ' + _(u'Generating GOP offsets'))
    # Abort the process if the user requests it
    if abort:
        raise Exception(_(u'Process aborted by user.'))

    # RE to obtain the number of frames
    framesRE = re.compile ("frames: ([0-9]*)\.")
    # Execute the mpeg_stat process
    stat_proc = subprocess.Popen(
        Globals.ListUnicodeEncode(['mpeg_stat','-offset',Globals.TMP_STAT,Globals.TMP_VIDEO]),
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,shell=Globals.shell(),
        universal_newlines=True)
    stat_output = stat_proc.communicate()[0]
    # Check the return process
    if stat_proc.wait() != 0:
        raise Exception(_(u'ERROR ON MPEG_STAT')+'\n\n'+stat_output)
    # Gather the frames information
    info = framesRE.search(stat_output)
    if info:
        frames = info.group(1)
        gopSize = 0
        # Generate GOP offsets
        # Only needed if dpg version >= 2
        if Globals.dpg_version >= 2:
            gop=open(Globals.TMP_GOP, 'wb')
            stat=open(Globals.TMP_STAT, 'rb')
            frame = 0
            # Process every line generated by mpeg_stat
            for line in stat:
                sline = line.split()
                if sline[0] == "picture" :
                    frame += 1
                elif sline[0] == "sequence":
                    gopSize += 1
                    gop.write (struct.pack ( "<l" , frame ))
                    # mpeg_stat shows bit offsets
                    gop.write (struct.pack ( "<l" , int(sline[1])/8 ))
            # Close files
            gop.close()
            stat.close()
    # When error, include the output in the exception
    else:
        raise Exception(_(u'ERROR ON MPEG_STAT')+'\n\n'+stat_output)
    return (int(frames), gopSize*8)

def alternative_mpeg_stat(filename):
    "Alternate way to generate file with GOP offsets and calculate frames"
    # The mpeg_stat method has been more tested and is faster

    # Increase progress
    global progress
    abort = progress.doProgress(1,
        filename + ' - ' + _(u'Generating GOP offsets'))
    # Abort the process if the user requests it
    if abort:
        raise Exception(_(u'Process aborted by user.'))

    # These are the start codes used in the mpeg format
    PICTURE_START_CODE = array.array('c','\x00\x00\x01\x00')
    SEQ_START_CODE = array.array('c','\x00\x00\x01\xb3')
    # Open the files
    mpgFile = open(Globals.TMP_VIDEO, 'rb')
    # Only needed if dpg version >= 2
    if Globals.dpg_version >= 2:
        gopFile = open(Globals.TMP_GOP, 'wb')
    # Init variables
    numFrames = 0
    gopSize = 0
    tmpBytes = array.array('c')

    try:
        # Get the first 4 bytes
        tmpBytes.fromfile(mpgFile, 4)
        # Process the file until EOF reached
        while True:
            # If picture start found, increase the number of frames
            if tmpBytes == PICTURE_START_CODE:
                numFrames += 1
                # Get the next 4 bytes and continue
                tmpBytes = array.array('c')
                tmpBytes.fromfile(mpgFile, 4)
            # If sequence start found, write to the GOP file
            elif tmpBytes == SEQ_START_CODE:
                # This is only needed for dpg version >= 2
                if Globals.dpg_version >= 2:
                    gopSize += 1
                    offset = mpgFile.tell() - 4
                    gopFile.write (struct.pack ( "<l" , numFrames))
                    gopFile.write (struct.pack ( "<l" , offset))
                # Get the next 4 bytes and continue
                tmpBytes = array.array('c')
                tmpBytes.fromfile(mpgFile, 4)
            # If nothing found, get another byte and continue
            else:
                tmpBytes.pop(0)
                tmpBytes.fromfile(mpgFile, 1)
    # No problem, we just found the EOF
    except EOFError:
        pass

    # Close files and exit
    mpgFile.close()
    # Only needed if dpg version >= 2
    if Globals.dpg_version >= 2:
        gopFile.close()
    # mpeg_stat always gets one frame less than me
    return ((numFrames-1), (gopSize*8))

def conv_thumb(filename, frames, updateprogress=True):
    "Generate a video thumbnail"

    if updateprogress:
        # Increase progress
        global progress
        abort = progress.doProgress(1,
            filename + ' - ' + _(u'Generating thumbnail'))
        # Abort the process if the user requests it
        if abort:
            raise Exception(_(u'Process aborted by user.'))

    # Takes a PNG screenshot if no file given.
    if not Globals.other_thumbnail:
        # png:outdir= is pretty new, the latest Windows (1.0rc2-4.2.1) and
        # Mac Fink (1.0rc2-4.2.1) binaries do not include this option.
        # While Fedora 13 (SVN-r32421-snapshot-4.4.4) does. Best to avoid it
        # for now.
        current_path = os.getcwd()
        os.chdir(Globals.TMP_SHOT)

        # The 00000001.png is choosed by mplayer
        shot_file = os.path.join(Globals.TMP_SHOT ,'00000001.png')
        s_cmd = ['mplayer',Globals.TMP_VIDEO,'-nosound','-vo',
            'png','-frames','1','-ss',
            # Skip 10% of the frames
            str(int((int(frames)/Globals.video_fps)/10))]
        # Execute mplayer to generate the shot
        mplayer_proc = subprocess.Popen(Globals.ListUnicodeEncode(s_cmd), stdout=subprocess.PIPE,
          stdin=subprocess.PIPE,shell=Globals.shell(),
          stderr=subprocess.STDOUT, universal_newlines=True)
        mplayer_output = mplayer_proc.communicate()[0]
        # Check the return process
        if mplayer_proc.wait() != 0:
            raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)

        # Some low quality encoded videos, have problems with the 10% skip
        if not os.path.isfile(shot_file):
            # Try again without ss
            s_cmd = ['mplayer',Globals.TMP_VIDEO,'-nosound','-vo',
            'png','-frames','1']
            # Execute mplayer
            mplayer_proc = subprocess.Popen(Globals.ListUnicodeEncode(s_cmd), stdout=subprocess.PIPE,
              stdin=subprocess.PIPE,shell=Globals.shell(),
              stderr=subprocess.STDOUT, universal_newlines=True)
            mplayer_output = mplayer_proc.communicate()[0]
            # Check the return process
            if mplayer_proc.wait() != 0:
                raise Exception(_(u'ERROR ON MPLAYER')+'\n\n'+mplayer_output)

        thumbfile = shot_file
        os.chdir(current_path)
    # If a file given, use it
    else:
        thumbfile = Globals.other_thumbnail

    # Tomas 20120917: moved code below to DpgThumbnail class
    thumbnail = DpgThumbnail.DpgThumbnail(thumbfile)
    thumb_data = thumbnail.getThumbData()

    # Write the data to a temporary file
    thumb_file = open(Globals.TMP_THUMB, 'wb')
    thumb_file.write(thumb_data)
    thumb_file.close()

    # Remove shot temporary file
    if not Globals.other_thumbnail:
        os.remove(shot_file)

def write_header(filename, frames):
    "Generate the DPG header"

    # Increase progress
    global progress
    abort = progress.doProgress(1,
        filename + ' - ' + _(u'Generating header'))
    # Abort the process if the user requests it
    if abort:
        raise Exception(_(u'Process aborted by user.'))

    # Tomas 20120909: moved code below to DpgHeader class
    dpg = DpgHeader.DpgHeader()
    dpg.setAudio(Globals.audio_codec, Globals.audio_frequency)
    dpg.setVideo(frames, Globals.video_fps, Globals.video_pixel)
    dpg.setSizes(Globals.dpg_version, 
                 os.stat(Globals.TMP_VIDEO)[stat.ST_SIZE], 
                 os.stat(Globals.TMP_AUDIO)[stat.ST_SIZE], 
                 os.stat(Globals.TMP_GOP)[stat.ST_SIZE])
    # print dpg
    dpg.toFile(Globals.TMP_HEADER)


def gui_encode_files(files):
    "Handle GUI logic with progress window"
    # Init the progress dialog
    busy = None
    progress = CustomProgressDialog.CustomProgressDialog(
        Globals.mainPanel, len(files), total_progress())
    progress.Show()
    # Disable the events on main frame
    Globals.mainPanel.Enable(False)
    try:
        # Set the busy cursor
        busy = wx.BusyCursor()
        encode_files(files, progress)
    finally:
        # Sets the normal cursor again
        if busy is not None:
            del busy
        # End the progress dialog
        if progress:
            progress.Destroy()
        # Enable the events on main frame
        Globals.mainPanel.Enable(True)
  
def total_progress():
    # Calculate the length of the encoding process
    # 100 video + 1 GOP + 1 Header + 1 to join everything
    totalProgress = 103
    # Add another 100 if we'll use double pass for video
    if Globals.dpg_quality == 'doublepass':
        totalProgress += 100
    # Add one more if a video thumbnail will be generated
    if Globals.dpg_version >= 4:
        totalProgress += 1
    return totalProgress


def encode_files(files, iprogress = None):
    "Encode the given list of files"
    encode_audio = None 
    global progress
    
    if iprogress: 
        progress = iprogress
    else:
        progress = CustomProgressDialog.TextProgress(None, len(files), total_progress())

    # Create the temporary files
    Globals.createTemporary()
    try:
        # Process the list of files
        for file in files:

            # Tomas: If it's a DPG file, just run dpg2avi
            # Would it be better to have this check directly in the FilesPanel code?            
            v = DpgHeader.getDpgVersion(file)
            if v:
                Dpg2Avi.Dpg2Avi(file)
                continue
            
            # Read options from the media specific config file (if one exists)
            ConfigurationManager.loadConfiguration(file)

            # Don't try to get the filename of a dvd or vcd source
            if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
                filename = file
            else:
                filename = os.path.basename(file)

            # Start the audio encoding thread
            encode_audio = EncodeAudioThread(file, filename)
            encode_audio.start()

            # Encode video
            encode_video(file, filename)

            # Wait for the audio encoding thread to finish
            # But if it hasn't finished yet... something goes wrong
            abort = progress.doProgress(1,
                filename + ' - ' + _(u'Finishing encoding process'))
            # Abort the process if the user requests it
            if abort:
                raise Exception(_(u'Process aborted by user.'))
            # Check the status of the thread
            encode_audio.join()
            threadError = encode_audio.getErrorMessage()
            if threadError:
                raise Exception(threadError)

            # Check the progress status
            # It's neccesary to fix it when filtering by chapters
            calculatedProg = 100
            if Globals.dpg_quality == 'doublepass':
                calculatedProg += 100
            realProg = progress.getCurrentProgress()
            # Increase progress when neccesary
            if realProg < calculatedProg:
                diffProgress = calculatedProg-realProg
                abort = progress.doProgress(diffProgress,
                        filename + ' - ' + _(u'Encoding in progress') + ': 100%')
                # Abort the process if the user requests it
                if abort:
                    raise Exception(_(u'Process aborted by user.'))

            # Generate GOP offsets
            if Globals.which('mpeg_stat'):
                frames, gopSize = mpeg_stat(filename)
            # If mpeg_stat not available, we'll try an alternate way
            else:
                # Warning disabled - mpeg_stat seems to be dead
                #Globals.debug(_(u'WARNING: mpeg_stat not found. The extraction' \
                #    u' of header offsets will be slower.'))
                frames, gopSize = alternative_mpeg_stat(filename)
            # With dpg version >= 4, we can use thumbnails
            if Globals.dpg_version >= 4:
                conv_thumb(filename, frames)
            # Write the DPG header
            write_header(filename, frames)
            # Get the output folder
            outputDir = Globals.other_output
            # Use the same as input by default
            # It won't be allowed when VCD or DVD sources are selected
            if not outputDir:
                outputDir = os.path.dirname(file)
            # Get the ouput full path
            if (file[:6] == 'vcd://'):
                dpgnameBase = file.split()[0].replace('://','_') + '_' \
                '' + file.split()[-1].replace('/','') + '.dpg'
            elif (file[:6] == 'dvd://'):
                # Filter by chapter
                if len(file.split()) == 5:
                    dpgnameBase = file.split()[0].replace('://','_') + '_' \
                        '' + file.split()[2] + '_' + file.split()[-1].replace('/','') + '.dpg'
                # Don't filter by chapter
                else:
                    dpgnameBase = file.split()[0].replace('://','_') + '_' \
                        '' + file.split()[-1].replace('/','') + '.dpg'
            else:
                dpgnameBase = os.path.basename (os.path.splitext(file)[0]) + '.dpg'
            dpgName = os.path.join(outputDir, dpgnameBase)
            # Check if the file already exists and choose another
            # We'll add a ~number at the end.
            version = 1
            while os.path.exists(dpgName):
                if version == 1:
                    dpgName = dpgName[:-4] + '~' + str(version) + '.dpg'
                else:
                    dpgName = dpgName[:dpgName.rfind('~')+1] + str(version) + '.dpg'
                version += 1

            # Concatenate the video parts

            # Increase progress
            abort = progress.doProgress(1,
                filename + ' - ' + _(u'Writing video file'))
            # Abort the process if the user requests it
            if abort:
                raise Exception(_(u'Process aborted by user.'))

            # For dpg version 4
            if Globals.dpg_version == 4:
                Globals.concat(dpgName,Globals.TMP_HEADER,Globals.TMP_THUMB,
                    Globals.TMP_AUDIO,Globals.TMP_VIDEO,Globals.TMP_GOP)
            # For dpg version 2 and 3
            elif (Globals.dpg_version == 2) | (Globals.dpg_version == 3):
                Globals.concat(dpgName,Globals.TMP_HEADER,Globals.TMP_AUDIO,
                    Globals.TMP_VIDEO,Globals.TMP_GOP)
            # For dpg version 0 and 1
            else:
                Globals.concat(dpgName,Globals.TMP_HEADER,Globals.TMP_AUDIO,
                    Globals.TMP_VIDEO)
        # Delete the temporary files
        Globals.clearTemporary()

    except Exception, e:
        # Delete the temporary files
        Globals.clearTemporary()
        # Stop the audio encoding thread
        if encode_audio:
            encode_audio.stopThread()
        # Send the exception to the FilesPanel
        raise e
        