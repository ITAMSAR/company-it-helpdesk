@echo off
cd /d "%~dp0.."
echo ========================================
echo IT DASHBOARD SERVER STARTER (VENV)
echo ========================================
echo Starting Django server with virtual environment...
echo Server akan berjalan di: http://192.168.1.11:8000
echo Untuk stop server: tekan Ctrl+C
echo Untuk tutup window ini: ketik 'exit' lalu Enter
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Django is available
python manage.py check >nul 2>&1
if errorlevel 1 (
    echo ERROR: Django tidak ditemukan atau ada masalah konfigurasi!
    echo Mencoba install dependencies...
    pip install -r requirements.txt
    echo.
    echo Coba jalankan server lagi...
    echo.
)

REM Run Django server
python manage.py runserver 0.0.0.0:8000

REM If server stops
echo.
echo Server telah berhenti.
pause