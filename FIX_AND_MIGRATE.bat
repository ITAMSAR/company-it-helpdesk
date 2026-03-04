@echo off
cls
echo ========================================
echo FIX AND MIGRATE - Smart Migration
echo ========================================
echo.
echo Script ini akan:
echo 1. Rollback migration yang error
echo 2. Jalankan migration baru yang pintar
echo 3. Convert data lama otomatis
echo.
pause

echo.
echo ========================================
echo LANGKAH 1: Rollback Migration
echo ========================================
echo.
python manage.py migrate inventory 0001
if errorlevel 1 (
    echo WARNING: Rollback gagal atau tidak perlu
)
echo.
pause

echo.
echo ========================================
echo LANGKAH 2: Hapus Migration Lama
echo ========================================
echo.
del "apps\inventory\migrations\0002_equipmentcategory_alter_equipment_category.py" 2>nul
echo Migration lama dihapus (jika ada)
echo.
pause

echo.
echo ========================================
echo LANGKAH 3: Jalankan Migration Baru
echo ========================================
echo.
echo Migration baru akan:
echo - Buat tabel kategori
echo - Buat kategori default (Laptop, Monitor, dll)
echo - Convert data lama otomatis
echo.
python manage.py migrate
if errorlevel 1 (
    echo.
    echo ERROR: Migration gagal!
    echo.
    echo Kemungkinan penyebab:
    echo 1. Database corrupt
    echo 2. Ada data yang tidak valid
    echo.
    echo Solusi: Jalankan FIX_MIGRATION.bat untuk fresh start
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
echo Migration berhasil!
echo Data lama sudah diconvert ke format baru.
echo.
echo Langkah selanjutnya:
echo 1. Jalankan server: run.bat
echo 2. Test fitur baru
echo 3. Tambah kategori lain jika perlu
echo.
pause
