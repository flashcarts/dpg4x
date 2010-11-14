@ECHO off

REM This file configures the paths used by dpg4x.
REM You can modify to suit your needs.
REM Read the INSTALL file for more details.

REM Get the folder for default installation
set OLD_DIR=%CD%
cd /d %~dp0
set DPG4X_BASE=%CD%
cd %OLD_DIR%

REM Path to the source files
set DPG4X_SOURCE=%DPG4X_BASE%

REM Path to the icon files
set DPG4X_ICONS=%DPG4X_BASE%\icons

REM Path to the gettext resources
set DPG4X_I18N=%DPG4X_BASE%\i18n

REM Execute the python interpreter
python "%DPG4X_SOURCE%\Dpg4x.py" "%*"
