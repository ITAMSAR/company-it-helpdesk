@echo off
title Check IT Dashboard Server Status
color 0B
echo.
echo ========================================
echo    CHECK SERVER STATUS
echo ========================================
echo.

REM Cek apakah server berjalan
echo Mengecek status server...
echo.

REM Test koneksi ke server
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 3 -UseBasicParsing; Write-Host '✅ Server AKTIF - Status:' $response.StatusCode -ForegroundColor Green } catch { Write-Host '❌ Server TIDAK AKTIF' -ForegroundColor Red }"

echo.
echo Test akses inventory:
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/inventory/' -TimeoutSec 3 -UseBasicParsing; Write-Host '✅ Inventory page OK - Status:' $response.StatusCode -ForegroundColor Green } catch { Write-Host '❌ Inventory page tidak bisa diakses' -ForegroundColor Red }"

echo.
echo Test QR scanning:
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/inventory/test-mobile/' -TimeoutSec 3 -UseBasicParsing; Write-Host '✅ QR system OK - Status:' $response.StatusCode -ForegroundColor Green } catch { Write-Host '❌ QR system tidak bisa diakses' -ForegroundColor Red }"

echo.
echo ========================================
echo Jika server TIDAK AKTIF, jalankan START_SERVER.bat
echo ========================================
echo.
pause