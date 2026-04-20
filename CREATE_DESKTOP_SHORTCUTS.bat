@echo off
title Create Desktop Shortcuts
echo.
echo ========================================
echo    MEMBUAT SHORTCUT DI DESKTOP
echo ========================================
echo.

set "PROJECT_PATH=%CD%"
set "DESKTOP=%USERPROFILE%\Desktop"

echo Membuat shortcut di desktop...
echo.

REM Create shortcut untuk START_SERVER
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🚀 Start IT Dashboard Server.lnk'); $Shortcut.TargetPath = '%PROJECT_PATH%\START_SERVER.bat'; $Shortcut.WorkingDirectory = '%PROJECT_PATH%'; $Shortcut.IconLocation = 'shell32.dll,25'; $Shortcut.Save()"

REM Create shortcut untuk CHECK_SERVER
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🔍 Check Server Status.lnk'); $Shortcut.TargetPath = '%PROJECT_PATH%\CHECK_SERVER.bat'; $Shortcut.WorkingDirectory = '%PROJECT_PATH%'; $Shortcut.IconLocation = 'shell32.dll,23'; $Shortcut.Save()"

REM Create shortcut untuk STOP_SERVER
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\🛑 Stop IT Dashboard Server.lnk'); $Shortcut.TargetPath = '%PROJECT_PATH%\STOP_SERVER.bat'; $Shortcut.WorkingDirectory = '%PROJECT_PATH%'; $Shortcut.IconLocation = 'shell32.dll,27'; $Shortcut.Save()"

echo ✅ Shortcut berhasil dibuat di desktop!
echo.
echo Shortcut yang dibuat:
echo - 🚀 Start IT Dashboard Server
echo - 🔍 Check Server Status  
echo - 🛑 Stop IT Dashboard Server
echo.
echo Sekarang Anda bisa nyalain server langsung dari desktop!
echo.
pause