@echo off
echo ========================================
echo Setup Firewall untuk IT Hub Internal
echo ========================================
echo.
echo Script ini akan membuka port 8000 di Windows Firewall
echo Agar laptop bisa akses server Django dari PC ini
echo.
echo CATATAN: Perlu Run as Administrator!
echo.
pause

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: Script ini harus dijalankan sebagai Administrator!
    echo Klik kanan file ini dan pilih "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo Membuka port 8000 di Windows Firewall...
echo.

REM Delete existing rule if exists
netsh advfirewall firewall delete rule name="Django IT Hub - Port 8000" >nul 2>&1

REM Add new firewall rule
netsh advfirewall firewall add rule name="Django IT Hub - Port 8000" dir=in action=allow protocol=TCP localport=8000

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Firewall rule berhasil dibuat
    echo ========================================
    echo.
    echo Port 8000 sekarang terbuka untuk koneksi dari jaringan lokal
    echo.
    echo Langkah selanjutnya:
    echo 1. Jalankan: run_network.bat
    echo 2. Dari laptop, buka: http://192.168.1.4:8000
    echo.
) else (
    echo.
    echo ERROR: Gagal membuat firewall rule
    echo Pastikan script dijalankan sebagai Administrator
    echo.
)

pause
