@echo off
cls
echo ========================================
echo UPDATE TICKET STATUS - Add Notes Field
echo ========================================
echo.
echo Perubahan:
echo 1. Status "Diproses" -> "Sedang Dikerjakan"
echo 2. Status "Ditolak" -> "Tidak Selesai"
echo 3. Tambah field "Catatan" untuk notes
echo.
echo PENTING: 
echo 1. TUTUP SERVER DJANGO (tekan Ctrl+C)
echo 2. Data tiket akan tetap aman
echo.
pause

echo.
echo Step 1: Stop proses Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

echo.
echo Step 2: Backup database...
if exist db.sqlite3 (
    copy db.sqlite3 db.sqlite3.backup
    echo Backup berhasil: db.sqlite3.backup
)

echo.
echo Step 3: Buat migration...
python manage.py makemigrations tickets
echo.

echo Step 4: Apply migration...
python manage.py migrate
echo.

if %errorlevel% neq 0 (
    echo ERROR: Migration gagal!
    echo Restore backup: copy db.sqlite3.backup db.sqlite3
    pause
    exit /b 1
)

echo.
echo ========================================
echo SELESAI!
echo ========================================
echo.
echo Perubahan berhasil diterapkan!
echo Data tiket lama tetap aman.
echo.
echo Fitur baru:
echo - Status: Baru, Sedang Dikerjakan, Selesai, Tidak Selesai
echo - Field catatan untuk notes saat update status
echo.
echo Sekarang jalankan: run.bat
echo.
pause
