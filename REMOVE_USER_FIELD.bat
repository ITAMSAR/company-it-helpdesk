@echo off
cls
echo ========================================
echo REMOVE USER FIELD FROM EMAIL
echo ========================================
echo.
echo Menghapus field 'user' dari EmployeeEmail model
echo.
echo PENTING: 
echo 1. TUTUP SERVER DJANGO (tekan Ctrl+C)
echo 2. Semua data email akan hilang
echo.
pause

echo.
echo Step 1: Stop proses Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

echo.
echo Step 2: Hapus database lama...
del db.sqlite3 2>nul
if exist db.sqlite3 (
    echo ERROR: Gagal hapus database! Tutup server dulu.
    pause
    exit /b 1
)
echo Database dihapus!

echo.
echo Step 3: Hapus semua migration files...
del apps\users\migrations\0*.py 2>nul
del apps\inventory\migrations\0*.py 2>nul
del apps\tickets\migrations\0*.py 2>nul
del apps\reminder\migrations\0*.py 2>nul
echo Migration files dihapus!

echo.
echo Step 4: Buat migration baru...
python manage.py makemigrations
echo.

echo Step 5: Apply migrations...
python manage.py migrate
echo.

echo Step 6: Buat superuser...
echo INGAT: Password tidak terlihat saat diketik (ini normal)
echo.
python manage.py createsuperuser
echo.

echo.
echo ========================================
echo SELESAI!
echo ========================================
echo.
echo Perubahan:
echo - Field 'user' dihapus dari Email Karyawan
echo - Form lebih simple, hanya data email karyawan
echo.
echo Sekarang jalankan: run.bat
echo.
pause
