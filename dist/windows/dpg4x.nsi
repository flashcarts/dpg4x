# NSIS definitions for dpg4

!define VERSION "3.0"
!define UMUI_VERSION "${VERSION}"
!define /date NOW "%Y-%m-%d"
!define UMUI_VERBUILD "3.0_${NOW}"

# Must contain four parts, used for internal comparisons of patch levels
!define  VIProduct_Ver "${VERSION}.1.0"

Name dpg4x
# Needed because $(^Name) sometimes does not seem to expand correctly
!define NAME dpg4x
!define PROGRAM_FILE dpg4x_main.exe

# Only tested on Win10 so far: Win7|Win8|Win8.1|Win10
ManifestSupportedOS "Win10"

# General Symbol Definitions
!define REGKEY "SOFTWARE\${Name}"
!define CLIENT_REGKEY "SOFTWARE\CLIENTS\MEDIA\${Name}"
!define COMPANY "Dpg4x Sourceforge project"
!define URL http://sourceforge.net/projects/dpg4x/

# Dependencies are not installed when updating
Var /GLOBAL Updating
Var /GLOBAL InstalledVersion

# Dependencies: Visual C libraries are installed
#!define DLLMSVC dependencies\vc_redist.x86.exe
#!define DLLMSVC dependencies\vc_redist.x64.exe
!define DLLMSVC dependencies\vc_redist.*.exe
# Seems to have changed in Win10 (not needed any longer, but older windowses needs this)
# install https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/
# copy all dlls from C:\Program Files (x86)\Windows Kits\10\Redist\10.0.19041.0\ucrt\DLLs\x86
# and/or C:\Program Files (x86)\Windows Kits\10\Redist\10.0.19041.0\ucrt\DLLs\x64 (or maybe arm...)

# Dependencies: mplayer and encoder are installed by downloading from the SourceForge
# project: MPlayer for Win32
#!define MPLAYER_REV 34401
#!define MPLAYER MPlayer-p3-svn-${MPLAYER_REV}
#!define MPLAYER7Z dependencies\${MPLAYER}.7z
#!define MPLAYER_URL "http://downloads.sourceforge.net/project/mplayer-win32/MPlayer%20and%20MEncoder/old/revision%20${MPLAYER_REV}/${MPLAYER}.7z"

# Dependencies: mplayer and encoder are installed by downloading from the SourceForge
# project: MPlayer for Win32 / Win64
!define MPLAYER_REV r38188%2Bg6e1903938b
!define MPLAYER MPlayer-x86_64-${MPLAYER_REV}
!define MPLAYER7Z dependencies\${MPLAYER}.7z
# Latest July 2020: http://downloads.sourceforge.net/project/mplayer-win32/MPlayer%20and%20MEncoder/r38188%2Bg6e1903938b/MPlayer-x86_64-r38188%2Bg6e1903938b.7z
#!define MPLAYER_URL "http://downloads.sourceforge.net/projects/mplayer-win32/files/MPlayer%20and%20MEncoder/${MPLAYER_REV}/${MPLAYER}.7z/download?use_mirror=autoselect"
  !define MPLAYER_URL "http://downloads.sourceforge.net/project/mplayer-win32/MPlayer%20and%20MEncoder/${MPLAYER_REV}/${MPLAYER}.7z"
# !define MPLAYER_URL "http://downloads.sourceforge.net/project/mplayer-win32/MPlayer%20and%20MEncoder/old/revision%20${MPLAYER_REV}/${MPLAYER}.7z"

# Installer attributes
OutFile "..\${NAME}-${VIProduct_Ver}_setup.exe"
Caption "${NAME} ${VIProduct_Ver}"
InstallDir $PROGRAMFILES\${NAME}
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion "${VIProduct_Ver}"
VIAddVersionKey ProductName "${Name}"
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey CompanyWebsite "${URL}"
VIAddVersionKey FileVersion "${VERSION}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
#InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show
# Vista+ XML manifest, does not affect older OSes
RequestExecutionLevel admin

# MultiUser Symbol Definitions
#!define MULTIUSER_EXECUTIONLEVEL Highest
#!define MULTIUSER_EXECUTIONLEVEL Standard
#!define MULTIUSER_MUI
#!define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_KEY "${REGKEY}"
#!define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_VALUENAME MultiUserInstallMode
#!define MULTIUSER_INSTALLMODE_COMMANDLINE
#!define MULTIUSER_INSTALLMODE_INSTDIR "${Name}"
#!define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_KEY "${REGKEY}"
#!define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_VALUE "Path"

# MUI Symbol Definitions
!define MUI_ICON ${NAME}.ico
!define MUI_WELCOMEFINISHPAGE_BITMAP "installer_${NAME}.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "installer_${NAME}.bmp"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "SHCTX"
!define MUI_STARTMENUPAGE_REGISTRY_KEY ${REGKEY}
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${Name}"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall-colorful.ico"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE
!define MUI_LICENSEPAGE_RADIOBUTTONS

!define MUI_FINISHPAGE_NOAUTOCLOSE

#!define MUI_FINISHPAGE_LINK "${URL}"
#!define MUI_FINISHPAGE_LINK_LOCATION "${URL}"

;--------------------------------
;Included files
!include Sections.nsh
!include UMUI.nsh
!include LangFile.nsh
!include WordFunc.nsh
!include FileFunc.nsh


;--------------------------------
;Interface Settings

  !define UMUI_SKIN "blue"

  !define UMUI_USE_INSTALLOPTIONSEX

  !define MUI_ABORTWARNING
  !define MUI_UNABORTWARNING

  !define UMUI_PAGEBGIMAGE
  !define UMUI_UNPAGEBGIMAGE

  !define UMUI_USE_ALTERNATE_PAGE ; For Welcome finish abort pages
  !define UMUI_USE_UNALTERNATE_PAGE

  !define MUI_COMPONENTSPAGE_SMALLDESC

  !define UMUI_DEFAULT_SHELLVARCONTEXT all

  !define UMUI_ENABLE_DESCRIPTION_TEXT

;--------------------------------
;Registry Settings

  !define UMUI_PARAMS_REGISTRY_ROOT HKLM
  !define UMUI_PARAMS_REGISTRY_KEY "${REGKEY}"

  !define UMUI_LANGUAGE_REGISTRY_VALUENAME "UMUI_InstallerLanguage"
  !define UMUI_SHELLVARCONTEXT_REGISTRY_VALUENAME "UMUI_ShellVarContext"

  !define UMUI_UNINSTALLPATH_REGISTRY_VALUENAME "UMUI_UninstallPath"
  !define UMUI_UNINSTALL_FULLPATH "$INSTDIR\Uninstall.exe"
  !define UMUI_INSTALLERFULLPATH_REGISTRY_VALUENAME "UMUI_InstallPath"

  !define UMUI_VERSION_REGISTRY_VALUENAME "UMUI_Version"
  !define UMUI_VERBUILD_REGISTRY_VALUENAME "UMUI_VerBuild"

  !define UMUI_PREUNINSTALL_FUNCTION preuninstall_function

  InstallDirRegKey ${UMUI_PARAMS_REGISTRY_ROOT} "${UMUI_PARAMS_REGISTRY_KEY}" ""

;--------------------------------
;Reserve Files

  !insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

# Variables
Var StartMenuGroup

;--------------------------------
;Pages

  !insertmacro UMUI_PAGE_MULTILANGUAGE

    !define UMUI_MAINTENANCEPAGE_MODIFY
    !define UMUI_MAINTENANCEPAGE_REPAIR
    !define UMUI_MAINTENANCEPAGE_REMOVE
    !define UMUI_MAINTENANCEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_PAGE_MAINTENANCE

    !define UMUI_UPDATEPAGE_REMOVE
    !define UMUI_UPDATEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_PAGE_UPDATE

    !define UMUI_WELCOMEPAGE_ALTERNATIVETEXT
  !insertmacro MUI_PAGE_WELCOME

    !define MUI_LICENSEPAGE_CHECKBOX
  !insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"

    #!define UMUI_INFORMATIONPAGE_USE_RICHTEXTFORMAT
  !insertmacro UMUI_PAGE_INFORMATION "..\..\README"

    !define UMUI_SETUPTYPEPAGE_STANDARD "$(UMUI_TEXT_SETUPTYPE_STANDARD_TITLE)"
    !define UMUI_SETUPTYPEPAGE_DEFAULTCHOICE ${UMUI_STANDARD}
    !define UMUI_SETUPTYPEPAGE_REGISTRY_VALUENAME "UMUI_SetupType"
  !insertmacro UMUI_PAGE_SETUPTYPE

    !define UMUI_COMPONENTSPAGE_INSTTYPE_REGISTRY_VALUENAME "UMUI_InstType"
    !define UMUI_COMPONENTSPAGE_REGISTRY_VALUENAME "UMUI_Components"
  !insertmacro MUI_PAGE_COMPONENTS

  !insertmacro MUI_PAGE_DIRECTORY

    !define UMUI_ADDITIONALTASKS_REGISTRY_VALUENAME "UMUI_Tasks"
  !insertmacro UMUI_PAGE_ADDITIONALTASKS addtasks_function

  !insertmacro UMUI_PAGE_ALTERNATIVESTARTMENU Application $StartMenuGroup

    !define UMUI_CONFIRMPAGE_TEXTBOX confirm_function
  !insertmacro UMUI_PAGE_CONFIRM

  !insertmacro MUI_PAGE_INSTFILES

    !define MUI_FINISHPAGE_SHOWREADME "..\..\README"
    !define MUI_FINISHPAGE_LINK "DPG4x Home Page"
    !define MUI_FINISHPAGE_LINK_LOCATION "${URL}"
  !insertmacro MUI_PAGE_FINISH

    !define UMUI_ABORTPAGE_LINK "DPG4x Home Page"
    !define UMUI_ABORTPAGE_LINK_LOCATION "${URL}"
  !insertmacro UMUI_PAGE_ABORT


  !insertmacro UMUI_UNPAGE_MULTILANGUAGE

    !define UMUI_MAINTENANCEPAGE_MODIFY
    !define UMUI_MAINTENANCEPAGE_REPAIR
    !define UMUI_MAINTENANCEPAGE_REMOVE
    !define UMUI_MAINTENANCEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_UNPAGE_MAINTENANCE

  !insertmacro MUI_UNPAGE_WELCOME

  !insertmacro MUI_UNPAGE_CONFIRM

  !insertmacro MUI_UNPAGE_INSTFILES

    !define MUI_FINISHPAGE_LINK "DPG4X Home Page"
    !define MUI_FINISHPAGE_LINK_LOCATION "${URL}"
  !insertmacro MUI_UNPAGE_FINISH

    !define UMUI_ABORTPAGE_LINK "DPG4x Home Page"
    !define UMUI_ABORTPAGE_LINK_LOCATION "${URL}"
  !insertmacro UMUI_UNPAGE_ABORT

;--------------------------------
;Languages

; first language is the default language if the system language is not in this list
  !insertmacro MUI_LANGUAGE "English"

  #!insertmacro LANGFILE_INCLUDE "EnglishExtra.nsh"  "nsis_translations\English.nsh"

  #!insertmacro MUI_LANGUAGE "Spanish"
  #!insertmacro MUI_LANGUAGE "Swedish"

#!include nsis_translations\translations.nsh
#!insertmacro LANGFILE_INCLUDE "nsis_translations\English.nsh" "nsis_translations\English.nsh"
#!insertmacro LANGFILE_INCLUDE_WITHDEFAULT "SwedishExtra.nsh" "nsis_translations\EnglishExtra.nsh" "nsis_translations\EnglishExtra.nsh" "nsis_translations\EnglishExtra.nsh"

;--------------------------------
;Installer Types

InstType "$(UMUI_TEXT_SETUPTYPE_STANDARD_TITLE)"

;--------------------------------
;Installer Sections

Section "Dpg4x core (required)" SECDpg4x

    SetDetailsPrint textonly
    DetailPrint "Installing DPG4x Core Files..."
    SetDetailsPrint listonly

	SectionIn 1 2 RO

    SetOutPath $INSTDIR
    SetOverwrite on
    File ..\..\dist\dpg4x_main.exe
	# Doc to consider later
    #File /r ..\dist\doc
    # icons, translations included in exe file by pyinstaller
	#File /r ..\dist\i18n
    #File /r ..\dist\icons
    SetOutPath $INSTDIR\dependencies
    File /r ${MPLAYER7Z}
    File /r ${DLLMSVC}
    File /r dependencies\README.txt
SectionEnd
        
Section "Download and install mplayer" SECMplayer
	SectionIn 1

    # Download and install mplayer
	# Mplayer download functions are based on, incl reusing code, the NSIS installer
    # in the SourceForge project: SMPlayer  (Written by redxii, thanks)
    retry_mplayer:

    DetailPrint $(MPLAYER_IS_DOWNLOADING)
	DetailPrint ${MPLAYER_URL}
    DetailPrint '/timeout 30000 /resume "" /MODERNPOPUP SourceForge \
	          /caption $(MPLAYER_IS_DOWNLOADING) /banner ${MPLAYER7Z} \
	          ${MPLAYER_URL}  \
			  $INSTDIR\${MPLAYER7Z} /end'
    inetc::get /timeout 30000 /resume "" \
	          /caption $(MPLAYER_IS_DOWNLOADING) /banner "${MPLAYER7Z}" \
	          ${MPLAYER_URL}  \
			  $INSTDIR\${MPLAYER7Z} /end

    Pop $R0
    StrCmp $R0 OK 0 check_mplayer

    DetailPrint "Extracting files..."

    SetOutPath $INSTDIR
    # the File command expects the file to be there when building the installer.
    # Solved by including an empty file that is replaced by the download above
    File "${MPLAYER7Z}"
    Nsis7z::Extract ${MPLAYER7Z}
    # Delete ${MPLAYER7Z}

    check_mplayer:
    ;This label does not necessarily mean there was a download error, so check first
    ${If} $R0 != "OK"
      DetailPrint $(MPLAYER_DL_FAILED)
    ${EndIf}

    IfFileExists "$INSTDIR\${MPLAYER}\mplayer.exe" mplayerInstSuccess mplayerInstFailed
      mplayerInstSuccess:
        WriteRegDWORD SHCTX "${REGKEY}" Installed_MPlayer 0x1
        Goto done
      mplayerInstFailed:
        MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION $(MPLAYER_DL_RETRY) /SD IDCANCEL IDRETRY retry_mplayer
        WriteRegDWORD SHCTX "${REGKEY}" Installed_MPlayer 0x0
        # Allow to continue without this and install mplayer manually later
        # Abort $(MPLAYER_INST_FAILED)
        MessageBox MB_OK  "$(MPLAYER_INST_FAILED)"
    done:
SectionEnd

Section "Install MS Visual C libraries" SECVisualClibs
	SectionIn 1

    # Silent install of visual C libraries:
    # If you would like to install the VC runtime packages in unattended mode (which will 
    # show a small progress bar but not require any user interaction), you can change the 
    # /qn switch below to /qb.  If you would like the progress bar to not show a cancel button, 
    # then you can change the /qn switch to /qb!
    ExecWait '"$INSTDIR\${DLLMSVC}" /q:a /c:"VCREDI~1.EXE /q:a /c:""msiexec /i vcredist.msi /qb!"" "'  
    WriteRegStr SHCTX "${REGKEY}\Components" Main 1
SectionEnd

Section -post SEC0001
    WriteRegStr SHCTX "${REGKEY}" Path $INSTDIR
    WriteRegStr SHCTX "${REGKEY}" Version "${VIProduct_Ver}"

    # Default Programs, Vista and later: (possibly more things to explore here...)
    # http://msdn.microsoft.com/en-us/library/cc144154%28v=vs.85%29.aspx
    WriteRegStr SHCTX  "${CLIENT_REGKEY}\Capabilities\FileAssociations" ".dpg" "DPG Video"
    WriteRegStr SHCTX  "${CLIENT_REGKEY}\Capabilities\FileAssociations" ".avi" "DPG Video"
    WriteRegStr SHCTX "${CLIENT_REGKEY}\Capabilities" "ApplicationDescription" $(APPLICATION_DESCRIPTION)
    WriteRegStr SHCTX "${CLIENT_REGKEY}\Capabilities" "ApplicationName" "${Name}"
    WriteRegStr SHCTX "Software\RegisteredApplications" "${Name}" "${CLIENT_REGKEY}\Capabilities"

    SetOutPath $INSTDIR
    WriteUninstaller $INSTDIR\uninstall.exe

	;create desktop shortcut
	!insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED DESKTOP
	    CreateShortCut "$DESKTOP\${Name}.lnk" "$INSTDIR\${PROGRAM_FILE}" ""
    !insertmacro UMUI_ADDITIONALTASKS_ENDIF

    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    CreateShortCut "$SMPROGRAMS\$StartMenuGroup\${Name} ${VERSION}.lnk" "$INSTDIR\${PROGRAM_FILE}" "" "$INSTDIR\${PROGRAM_FILE}"
    StrCmp "$Updating" "Yes" 0 +2
      Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\${Name} $InstalledVersion.lnk"
    WriteINIStr    "$SMPROGRAMS\$StartMenuGroup\$(WebLink).url" "InternetShortcut" "URL" "${URL}"
    !insertmacro MUI_STARTMENU_WRITE_END

	# From https://nsis.sourceforge.io/Add_uninstall_information_to_Add/Remove_Programs
	!define UNINST_KEY "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${Name}"
    WriteRegStr SHCTX "${UNINST_KEY}" DisplayName "${Name}"
    WriteRegStr SHCTX "${UNINST_KEY}" DisplayVersion "${VIProduct_Ver}"
    WriteRegStr SHCTX "${UNINST_KEY}" Publisher "${COMPANY}"
    WriteRegStr SHCTX "${UNINST_KEY}" URLInfoAbout "${URL}"
    WriteRegStr SHCTX "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\uninstall.exe"
    WriteRegStr SHCTX "${UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
	WriteRegStr SHCTX "${UNINST_KEY}" \
                 "QuietUninstallString" "$INSTDIR\uninstall.exe /S"
    WriteRegDWORD SHCTX "${UNINST_KEY}" NoModify 1
    WriteRegDWORD SHCTX "${UNINST_KEY}" NoRepair 1

    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD SHCTX "${UNINST_KEY}" "EstimatedSize" "$0"

SectionEnd

# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 SHCTX "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

# Uninstaller sections
Section /o -un.Main UNSEC0000
    # Delete directories recursively except for main directory
    # Do not recursively delete $INSTDIR
    # RmDir /r /REBOOTOK $INSTDIR\doc
    # RmDir /r /REBOOTOK $INSTDIR\i18n
    # RmDir /r /REBOOTOK $INSTDIR\icons
    RmDir /r /REBOOTOK $INSTDIR\dependencies    
    Delete /REBOOTOK $INSTDIR\*.dll
    Delete /REBOOTOK $INSTDIR\library.zip
    Delete /REBOOTOK $INSTDIR\*.exe
    Delete /REBOOTOK $INSTDIR\*.pyd
    Delete /REBOOTOK $INSTDIR\*.7z
    Delete /REBOOTOK $INSTDIR\*.log    

    RmDir /r /REBOOTOK $INSTDIR\${MPLAYER}

    RmDir /REBOOTOK $INSTDIR
    DeleteRegValue SHCTX "${REGKEY}\Components" Main
SectionEnd

Section -un.post UNSEC0001
    DeleteRegKey SHCTX "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${Name}"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\${Name} ${VERSION}.lnk"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\$(WebLink).url" 
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue SHCTX "${REGKEY}" StartMenuGroup
    DeleteRegKey /IfEmpty SHCTX "${REGKEY}\Components"
    DeleteRegKey /IfEmpty SHCTX "${REGKEY}"
    DeleteRegValue SHCTX "Software\RegisteredApplications" "${Name}"
    DeleteRegKey SHCTX "${REGKEY}"
    DeleteRegKey SHCTX "${CLIENT_REGKEY}"
    Delete "$DESKTOP\${Name}.lnk"
    RmDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RmDir /REBOOTOK $INSTDIR
    Push $R0
    StrCpy $R0 $StartMenuGroup 1
    StrCmp $R0 ">" no_smgroup
no_smgroup:
    Pop $R0
SectionEnd

!insertmacro UMUI_DECLARECOMPONENTS_BEGIN
  !insertmacro UMUI_COMPONENT SECDpg4x
  !insertmacro UMUI_COMPONENT SECMplayer
  !insertmacro UMUI_COMPONENT SECVisualClibs
!insertmacro UMUI_DECLARECOMPONENTS_END

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDpg4x} "The core files required to use dpg4x (UI, dpg encoder)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SECMplayer} "Download and install mplayer and mencoder which converts video and audio streams"
  !insertmacro MUI_DESCRIPTION_TEXT ${SECVisualClibs} "Install Visual C redistributable libraries (vc_redist)"
!insertmacro MUI_FUNCTION_DESCRIPTION_END


Function .onGUIEnd
    # empty
FunctionEnd

Function .onInit
    InitPluginsDir
    #!insertmacro MUI_LANGDLL_DISPLAY
	!insertmacro UMUI_MULTILANG_GET
    #!insertmacro MULTIUSER_INIT  
	; Change default InstallDir to C:\ProgramData on Windows Vista and more
	ClearErrors
    IfFileExists $INSTDIR endCheckVersion 0
      ReadRegStr $0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
      IfErrors endCheckVersion 0 ; If not WinNT
        IntCmp $0 6 0 endCheckVersion 0 ; If version >= 6
          SetShellVarContext all
          StrCpy $INSTDIR "$APPDATA\${NAME}"
  endCheckVersion:

FunctionEnd

# Uninstaller functions
Function un.onInit
	!insertmacro UMUI_MULTILANG_GET
	!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuGroup
    # !insertmacro MULTIUSER_UNINIT
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd

;--------------------------------
; Pages functions

Function addtasks_function
  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LABEL "$(UMUI_TEXT_ADDITIONALTASKS_ADDITIONAL_ICONS)"
  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK DESKTOP 1 "$(UMUI_TEXT_ADDITIONALTASKS_CREATE_DESKTOP_ICON)"

  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LINE

  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LABEL "$(UMUI_TEXT_SHELL_VAR_CONTEXT)"

  UserInfo::GetAccountType
  Pop $R0
  StrCmp $R0 "Guest" 0 notLimited
    !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO CURRENT 1 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
    Goto endShellVarContext
  notLimited:
    !insertmacro UMUI_GETSHELLVARCONTEXT
    Pop $R0
    StrCmp $R0 "current" 0 allShellVarContext
      !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO ALL 0 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_FOR_ALL_USERS)"
      !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO CURRENT 1 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
      Goto endShellVarContext
    allShellVarContext:
      !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO ALL 1 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_FOR_ALL_USERS)"
      !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO CURRENT 0 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
  endShellVarContext:
  ClearErrors

FunctionEnd

!macro confirm_addline section

  SectionGetFlags ${Sec${section}} $1
  IntOp $1 $1 & ${SF_SELECTED}
  IntCmp $1 ${SF_SELECTED} 0 n${section} n${section}
    SectionGetText ${Sec${section}} $1
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "    - $1"
  n${section}:

!macroend


Function confirm_function
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_DESTINATION_LOCATION)"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $INSTDIR"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""
  
  ;Only if StartMenu Folder is selected
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_START_MENU_FOLDER)"
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $STARTMENU_FOLDER"

    ;ShellVarContext
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_SHELL_VAR_CONTEXT)"
    !insertmacro UMUI_GETSHELLVARCONTEXT
    Pop $1
    StrCmp $1 "all" 0 current
      !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_SHELL_VAR_CONTEXT_FOR_ALL_USERS)"
      Goto endsvc
    current:
      !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
    endsvc:
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""

  !insertmacro MUI_STARTMENU_WRITE_END

  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_COMPNENTS)"

  !insertmacro confirm_addline Dpg4x
  !insertmacro confirm_addline Mplayer
  !insertmacro confirm_addline VisualClibs
  
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_ADDITIONALTASKS_TITLE):"
  ;Only if one at least of additional icon check is checked  
  !insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED DESKTOP
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_ADDITIONALTASKS_ADDITIONAL_ICONS)"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "            $(UMUI_TEXT_ADDITIONALTASKS_CREATE_DESKTOP_ICON)"
  !insertmacro UMUI_ADDITIONALTASKS_ENDIF
  ;ShellVarContext
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_SHELL_VAR_CONTEXT)"
  ; only if for all user radio is selected
  !insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED ALL
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "            $(UMUI_TEXT_SHELL_VAR_CONTEXT_FOR_ALL_USERS)"
  !insertmacro UMUI_ADDITIONALTASKS_ENDIF
  ; only if for current user is selected
  !insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED CURRENT
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "            $(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
  !insertmacro UMUI_ADDITIONALTASKS_ENDIF 

FunctionEnd

Function preuninstall_function

  IfFileExists $INSTDIR\${PROGRAM_FILE} dpg4x_installed
    MessageBox MB_YESNO "It does not appear that NSIS is installed in the directory '$INSTDIR'.$\r$\nContinue anyway (not recommended)?" IDYES dpg4x_installed
    Abort "Install aborted by user"
  dpg4x_installed:
  # consider adding more here...
FunctionEnd