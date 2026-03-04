@echo off
cls
echo ========================================
echo RESTART FRESH - Complete Reset
echo ========================================
echo.
echo Script ini akan:
echo 1. Stop semua proses Python
echo 2. Hapus database lama
echo 3. Buat database baru
echo 4. Buat superuser
echo 5. Jalankan server
echo.
echo PENTING: Semua data akan hilang!
echo.
pause

echo.
echo ========================================
echo Step 1: Stop Proses Python
echo ========================================
echo.
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo Proses Python berhasil di-stop!
) else (
    echo Tidak ada proses Python yang running.
)
timeout /t 2 >nul

echo.
echo ========================================
echo Step 2: Hapus Database Lama
echo ========================================
echo.
if exist db.sqlite3 (
    del db.sqlite3
    if exist db.sqlite3 (
        echo ERROR: Gagal hapus database!
        echo Tutup semua aplikasi yang menggunakan database.
        pause
        exit /b 1
    ) else (
        echo Database lama berhasil dihapus!
    )
) else (
    echo Database tidak ditemukan (sudah bersih).
)

echo.
echo ========================================
echo Step 3: Buat Database Baru
echo ========================================
echo.
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Gagal membuat database!
    pause
    exit /b 1
)
echo Database baru berhasil dibuat!

echo.
echo ========================================
echo Step 4: Buat Superuser
echo ========================================
echo.
echo INGAT: Password tidak terlihat saat diketik (ini normal)
echo.
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo ERROR: Gagal membuat superuser!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 5: Jalankan Server
echo ========================================
echo.
echo Server akan dijalankan di: http://127.0.0.1:8000
echo.
echo Untuk stop server: Tekan Ctrl+C
echo.
pause

echo Starting server...
python manage.py runserver
