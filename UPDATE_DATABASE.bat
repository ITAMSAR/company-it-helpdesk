@echo off
cls
echo ========================================
echo UPDATE DATABASE - Fitur Baru
echo ========================================
echo.
echo Fitur baru yang ditambahkan:
echo 1. Manajemen Email Karyawan (CRUD)
echo 2. Kategori Dinamis untuk Inventaris
echo 3. Filter by Kategori dan Status
echo.
echo PENTING: Backup database dulu jika ada data penting!
echo.
pause

echo.
echo ========================================
echo LANGKAH 1: Membuat Migration Files
echo ========================================
echo.
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Gagal membuat migrations!
    pause
    exit /b 1
)
echo.
pause

echo.
echo ========================================
echo LANGKAH 2: Menerapkan Migrasi
echo ========================================
echo.
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Gagal apply migrations!
    pause
    exit /b 1
)
echo.
pause

echo.
echo ========================================
echo SELESAI!
echo ========================================
echo.
echo Langkah selanjutnya:
echo 1. Tambah kategori default di Admin Panel
echo    - Login ke: http://127.0.0.1:8000/admin
echo    - Klik "Kategori Peralatan"
echo    - Tambah: Laptop, Monitor, Mouse, dll
echo.
echo 2. Test fitur baru:
echo    - Menu "Email Karyawan" (sidebar)
echo    - Tombol "Kelola Kategori" (di Inventaris)
echo    - Filter by kategori dan status
echo.
echo 3. Baca UPDATE_FEATURES.md untuk detail lengkap
echo.
pause
