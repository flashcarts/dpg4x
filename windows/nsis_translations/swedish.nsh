# Language: English (1033)
# English language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE "Swedish" "Svenska"

# Update checks
${LangFileString} ALREADY_INSTALLED "${Name} �r redan installerad"

# Start menu entries
${LangFileString} UninstallLink "Avinstallera ${Name}"
${LangFileString} WebLink "${Name} websida"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "Laddar ned MPlayer..."
${LangFileString} MPLAYER_DL_RETRY "MPlayer kunde inte installeras, nytt f�rs�k?"
${LangFileString} MPLAYER_DL_FAILED "Kunde ej ladda ned MPlayer: '$R0'."
${LangFileString} MPLAYER_INST_FAILED "Kunde ej installera MPlayer som beh�vs f�r konvertering. Du beh�ver installera MPlayer separat."

# Vista & Later Default Programs Registration
${LangFileString} APPLICATION_DESCRIPTION "Kodar om video till DPG - ett format som spelas av Nintendo DS mediaspelare moonshell"