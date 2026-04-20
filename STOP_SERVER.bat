@echo off
title Stop IT Dashboard Server
color 0C
echo.
echo ========================================
echo    STOP IT DASHBOARD SERVER
echo ========================================
echo.
echo Mencari dan menghentikan server Django...
echo.

REM Kill semua proses Python yang menjalankan manage.py
taskkill /f /im python.exe /fi "WINDOWTITLE eq *runserver*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *manage.py*" 2>nul

echo Server Django telah dihentikan.
echo.
pause