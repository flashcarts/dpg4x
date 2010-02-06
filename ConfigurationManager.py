# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         ConfigurationManager.py
# Purpose:      Manages the configuration variables.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: ConfigurationManager.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals

import ConfigParser
import os

# Private configuration manager
__cp = ConfigParser.SafeConfigParser()

###############
## FUNCTIONS ##
###############

def saveConfiguration():
    "Stores the configuration in disk"

    # General options
    if not __cp.has_section('GENERAL'):
        __cp.add_section('GENERAL')
    __cp.set('GENERAL','dpg_version',str(Globals.dpg_version))
    __cp.set('GENERAL','dpg_quality',Globals.Encode(Globals.dpg_quality))
    __cp.set('GENERAL','other_output',Globals.Encode(Globals.other_output))
    __cp.set('GENERAL','other_temporary',Globals.Encode(Globals.other_temporary))
    __cp.set('GENERAL','other_thumbnail',Globals.Encode(Globals.other_thumbnail))
    
    # Video options
    if not __cp.has_section('VIDEO'):
        __cp.add_section('VIDEO')
    __cp.set('VIDEO','video_keepaspect',str(Globals.video_keepaspect))
    __cp.set('VIDEO','video_width',str(Globals.video_width))
    __cp.set('VIDEO','video_height',str(Globals.video_height))
    __cp.set('VIDEO','video_bitrate',str(Globals.video_bitrate))
    __cp.set('VIDEO','video_fps',str(Globals.video_fps))
    __cp.set('VIDEO','video_autofps',str(Globals.video_autofps))
    __cp.set('VIDEO','video_pixel',str(Globals.video_pixel))
    
    # Audio options
    if not __cp.has_section('AUDIO'):
        __cp.add_section('AUDIO')
    __cp.set('AUDIO','audio_codec',Globals.Encode(Globals.audio_codec))
    __cp.set('AUDIO','audio_track',str(Globals.audio_track))
    __cp.set('AUDIO','audio_autotrack',str(Globals.audio_autotrack))
    __cp.set('AUDIO','audio_bitrate',str(Globals.audio_bitrate))
    __cp.set('AUDIO','audio_frequency',str(Globals.audio_frequency))
    __cp.set('AUDIO','audio_normalize',str(Globals.audio_normalize))
    __cp.set('AUDIO','audio_mono',str(Globals.audio_mono))
    
    # Subtitle options
    if not __cp.has_section('SUBTITLES'):
        __cp.add_section('SUBTITLES')
    __cp.set('SUBTITLES','subtitles_source',Globals.Encode(Globals.subtitles_source))
    __cp.set('SUBTITLES','subtitles_track',str(Globals.subtitles_track))
    __cp.set('SUBTITLES','subtitles_file',Globals.Encode(Globals.subtitles_file))
    __cp.set('SUBTITLES','subtitles_font',Globals.Encode(Globals.subtitles_font))
    __cp.set('SUBTITLES','subtitles_encoding',Globals.Encode(Globals.subtitles_encoding))
    
    try:
        Globals.CreateFolder(os.path.dirname(Globals.USERFILECONFIG))
        userConfig = open(Globals.USERFILECONFIG,'w')
        __cp.write(userConfig)
        userConfig.close()
    # If it fails, we only show a warning (no fatal)
    except Exception, e:
        Globals.debug(_(u'Can\'t save user configuration:') + ' ' \
            '' + unicode(e))

def loadConfiguration():

    # Read the configuration file
    __cp.read(Globals.FILECONFIG)
        
    # General options
    if not __cp.has_section('GENERAL'):
        __cp.add_section('GENERAL')
    if __cp.has_option('GENERAL', 'dpg_version'):
        Globals.dpg_version = __cp.getint('GENERAL','dpg_version') 
    if __cp.has_option('GENERAL', 'dpg_quality'):
        Globals.dpg_quality = Globals.Decode(__cp.get('GENERAL','dpg_quality')) 
    if __cp.has_option('GENERAL', 'other_output'):
        Globals.other_output = Globals.Decode(__cp.get('GENERAL','other_output'))
    if __cp.has_option('GENERAL', 'other_temporary'):
        Globals.other_temporary = Globals.Decode(__cp.get('GENERAL','other_temporary'))
    if __cp.has_option('GENERAL', 'other_thumbnail'):
        Globals.other_thumbnail = Globals.Decode(__cp.get('GENERAL','other_thumbnail'))

    # Video options
    if not __cp.has_section('VIDEO'):
        __cp.add_section('VIDEO')
    if __cp.has_option('VIDEO', 'video_keepaspect'):
        Globals.video_keepaspect = __cp.getboolean('VIDEO','video_keepaspect')
    if __cp.has_option('VIDEO', 'video_width'):
        Globals.video_width = __cp.getint('VIDEO','video_width')
    if __cp.has_option('VIDEO', 'video_height'):
        Globals.video_height = __cp.getint('VIDEO','video_height')
    if __cp.has_option('VIDEO', 'video_bitrate'):
        Globals.video_bitrate = __cp.getint('VIDEO','video_bitrate')
    if __cp.has_option('VIDEO', 'video_fps'):
        Globals.video_fps = __cp.getint('VIDEO','video_fps')
    if __cp.has_option('VIDEO', 'video_autofps'):
        Globals.video_autofps = __cp.getboolean('VIDEO','video_autofps')
    if __cp.has_option('VIDEO', 'video_pixel'):
        Globals.video_pixel = __cp.getint('VIDEO','video_pixel')

    # Audio options
    if not __cp.has_section('AUDIO'):
        __cp.add_section('AUDIO') 
    if __cp.has_option('AUDIO', 'audio_codec'):
        Globals.audio_codec = Globals.Decode(__cp.get('AUDIO','audio_codec'))
    if __cp.has_option('AUDIO', 'audio_track'):
        Globals.audio_track = __cp.getint('AUDIO','audio_track')
    if __cp.has_option('AUDIO', 'audio_autotrack'):
        Globals.audio_autotrack = __cp.getboolean('AUDIO','audio_autotrack')
    if __cp.has_option('AUDIO', 'audio_bitrate'):
        Globals.audio_bitrate = __cp.getint('AUDIO','audio_bitrate')  
    if __cp.has_option('AUDIO', 'audio_frequency'):
        Globals.audio_frequency = __cp.getint('AUDIO','audio_frequency')
    if __cp.has_option('AUDIO', 'audio_normalize'):
        Globals.audio_normalize = __cp.getboolean('AUDIO','audio_normalize')
    if __cp.has_option('AUDIO', 'audio_mono'):
        Globals.audio_mono = __cp.getboolean('AUDIO','audio_mono')
        
    # Subtitle options
    if not __cp.has_section('SUBTITLES'):
        __cp.add_section('SUBTITLES')
    if __cp.has_option('SUBTITLES', 'subtitles_source'):
        Globals.subtitles_source = Globals.Decode(__cp.get('SUBTITLES','subtitles_source'))     
    if __cp.has_option('SUBTITLES', 'subtitles_track'):
        Globals.subtitles_track = __cp.getint('SUBTITLES','subtitles_track')
    if __cp.has_option('SUBTITLES', 'subtitles_file'):
        Globals.subtitles_file = Globals.Decode(__cp.get('SUBTITLES','subtitles_file'))
    if __cp.has_option('SUBTITLES', 'subtitles_font'):
        Globals.subtitles_font = Globals.Decode(__cp.get('SUBTITLES','subtitles_font'))
    if __cp.has_option('SUBTITLES', 'subtitles_encoding'):
        Globals.subtitles_encoding = Globals.Decode(__cp.get('SUBTITLES','subtitles_encoding'))
