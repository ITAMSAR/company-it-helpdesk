@echo off
cls
echo ========================================
echo UPDATE DATABASE - Safe Migration
echo ========================================
echo.
echo Script ini untuk update database TANPA hapus data
echo Gunakan saat ada perubahan model (tambah field, dll)
echo.
echo PENTING: 
echo 1. TUTUP SERVER DJANGO (tekan Ctrl+C)
echo 2. BACKUP database dulu (copy db.sqlite3)
echo.
pause

echo.
echo ========================================
echo Step 1: Backup Database
echo ========================================
echo.
if exist db.sqlite3 (
    copy db.sqlite3 db.sqlite3.backup
    echo Backup berhasil: db.sqlite3.backup
) else (
    echo Database tidak ditemukan, skip backup
)
echo.
pause

echo.
echo ========================================
echo Step 2: Buat Migration Files
echo ========================================
echo.
python manage.py makemigrations
echo.
pause

echo.
echo ========================================
echo Step 3: Lihat SQL yang Akan Dijalankan (Opsional)
echo ========================================
echo.
echo Mau lihat SQL query yang akan dijalankan? (y/n)
set /p show_sql=
if /i "%show_sql%"=="y" (
    python manage.py sqlmigrate inventory 0001
    echo.
    pause
)

echo.
echo ========================================
echo Step 4: Apply Migrations
echo ========================================
echo.
python manage.py migrate
echo.

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Migration Gagal!
    echo ========================================
    echo.
    echo Kemungkinan penyebab:
    echo 1. Ada constraint yang dilanggar
    echo 2. Field baru tidak punya default value
    echo 3. Data lama tidak kompatibel
    echo.
    echo Solusi:
    echo 1. Restore backup: copy db.sqlite3.backup db.sqlite3
    echo 2. Perbaiki model (tambah default value, null=True, dll)
    echo 3. Atau buat data migration manual
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SELESAI!
echo ========================================
echo.
echo Database berhasil diupdate!
echo Data lama tetap aman.
echo.
echo File backup: db.sqlite3.backup
echo Hapus backup jika sudah yakin: del db.sqlite3.backup
echo.
pause
