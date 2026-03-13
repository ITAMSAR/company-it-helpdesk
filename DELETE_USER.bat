@echo off
echo ========================================
echo Hapus User - IT Hub Internal
echo ========================================
echo.
echo PERINGATAN: Script ini akan menghapus user secara permanen!
echo.
pause

:input_username
echo.
set /p username="Masukkan username yang ingin dihapus: "
if "%username%"=="" (
    echo Username tidak boleh kosong!
    goto input_username
)

echo.
echo Memeriksa user...
python -c "import django; django.setup(); from django.contrib.auth.models import User; user = User.objects.get(username='%username%'); print('User ditemukan:'); print('Username:', user.username); print('Email:', user.email or '-'); print('Role:', 'Admin' if user.is_superuser else 'Staff' if user.is_staff else 'User')" 2>nul

if %errorLevel% neq 0 (
    echo.
    echo ERROR: User '%username%' tidak ditemukan!
    echo.
    pause
    exit /b 1
)

:confirm_delete
echo.
set /p confirm="Apakah Anda yakin ingin menghapus user '%username%'? (yes/no): "

if /i "%confirm%"=="yes" (
    goto do_delete
) else if /i "%confirm%"=="no" (
    echo.
    echo Penghapusan dibatalkan.
    echo.
    pause
    exit /b 0
) else (
    echo Jawaban tidak valid! Ketik 'yes' atau 'no'
    goto confirm_delete
)

:do_delete
echo.
echo ========================================
echo Menghapus user: %username%
echo ========================================
echo.

python -c "import django; django.setup(); from django.contrib.auth.models import User; user = User.objects.get(username='%username%'); user.delete(); print('User berhasil dihapus!')"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! User berhasil dihapus
    echo ========================================
    echo.
) else (
    echo.
    echo ERROR: Gagal menghapus user
    echo.
)

pause
