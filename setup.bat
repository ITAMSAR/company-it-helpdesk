@echo off
echo ========================================
echo IT Hub Internal - Setup Script
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python dari python.org
    pause
    exit /b 1
)
echo.

echo [2/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Gagal install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/5] Running migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Gagal membuat migrations!
    pause
    exit /b 1
)
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Gagal melakukan migrasi database!
    pause
    exit /b 1
)
echo.

echo [4/5] Creating superuser...
echo.
echo ========================================
echo PENTING: Saat input PASSWORD
echo - Password TIDAK AKAN TERLIHAT saat diketik
echo - Ini NORMAL untuk keamanan
echo - Ketik password Anda dan tekan ENTER
echo - Anda akan diminta ketik 2x untuk konfirmasi
echo ========================================
echo.
echo Silakan buat akun admin:
python manage.py createsuperuser
echo.

echo [5/5] Setup completed!
echo.
echo ========================================
echo Untuk menjalankan server:
echo   python manage.py runserver
echo.
echo Kemudian buka browser dan akses:
echo   http://127.0.0.1:8000
echo ========================================
pause
