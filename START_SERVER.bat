@echo off
title IT Dashboard Server
color 0A
echo.
echo ========================================
echo    IT DASHBOARD SERVER STARTER
echo ========================================
echo.
echo Starting Django server...
echo Server akan berjalan di: http://192.168.1.11:8000
echo.
echo Untuk stop server: tekan Ctrl+C
echo Untuk tutup window ini: ketik 'exit' lalu Enter
echo.
echo ========================================
echo.

REM Masuk ke directory project
cd /d "D:\Project Coding\company-it-helpdesk"

REM Jalankan server Django
python manage.py runserver 0.0.0.0:8000

echo.
echo Server telah berhenti.
pause