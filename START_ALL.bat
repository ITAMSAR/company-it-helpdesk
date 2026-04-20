@echo off
title IT Dashboard - Start All
color 0A
echo.
echo ========================================
echo    IT DASHBOARD - START ALL
echo ========================================
echo.
echo 1. Starting Django server...
echo.

REM Masuk ke directory project
cd /d "D:\Project Coding\company-it-helpdesk"

REM Start server di background
start "IT Dashboard Server" cmd /k "python manage.py runserver 0.0.0.0:8000"

echo 2. Waiting for server to start...
timeout /t 5 /nobreak >nul

echo 3. Testing server connection...
powershell -Command "for($i=1; $i -le 10; $i++) { try { Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 2 -UseBasicParsing | Out-Null; Write-Host '✅ Server ready!' -ForegroundColor Green; break } catch { Write-Host 'Waiting...' $i '/10' -ForegroundColor Yellow; Start-Sleep 2 } }"

echo.
echo 4. Opening dashboard in browser...
start http://192.168.1.11:8000

echo.
echo ✅ IT Dashboard siap digunakan!
echo.
echo PENTING: Jangan tutup window "IT Dashboard Server"
echo         Window itu adalah server yang harus tetap jalan.
echo.
timeout /t 3 /nobreak >nul