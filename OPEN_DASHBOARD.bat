@echo off
title Open IT Dashboard
color 0B
echo.
echo ========================================
echo    MEMBUKA IT DASHBOARD
echo ========================================
echo.

echo Mengecek server...
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 3 -UseBasicParsing | Out-Null; Write-Host '✅ Server aktif!' -ForegroundColor Green } catch { Write-Host '❌ Server tidak aktif! Jalankan START_SERVER.bat dulu.' -ForegroundColor Red; pause; exit }"

echo.
echo Membuka dashboard di browser...
start http://192.168.1.11:8000

echo.
echo Dashboard terbuka di browser default Anda.
timeout /t 3 /nobreak >nul