@ECHO off
REM This file build an installer file for Windows, to be run from the the windows directory
REM Please install everything listed in README_dpg4x_win.txt before running this file
cd /d %~dp0\..
python windows\setup.py py2exe
cd windows
"c:\Program Files\NSIS\makensis.exe" dpg4x.nsi
Echo "Successfully built new installer" 