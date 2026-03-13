@echo off
echo ========================================
echo Buat User Baru - IT Hub Internal
echo ========================================
echo.
echo Script ini akan membuat user baru (admin atau staff)
echo.
pause

:input_username
echo.
set /p username="Masukkan username baru: "
if "%username%"=="" (
    echo Username tidak boleh kosong!
    goto input_username
)

:input_email
echo.
set /p email="Masukkan email (opsional, tekan Enter untuk skip): "

:input_role
echo.
echo Pilih role user:
echo 1. Superuser/Admin (akses penuh)
echo 2. Staff (akses terbatas)
echo.
set /p role="Pilih (1/2): "

if "%role%"=="1" (
    set role_name=Superuser/Admin
    goto create_superuser
) else if "%role%"=="2" (
    set role_name=Staff
    goto create_staff
) else (
    echo Pilihan tidak valid!
    goto input_role
)

:create_superuser
echo.
echo ========================================
echo Membuat Superuser: %username%
echo ========================================
echo.
echo PENTING: Password tidak akan terlihat saat diketik
echo.
if "%email%"=="" (
    python manage.py createsuperuser --username %username%
) else (
    python manage.py createsuperuser --username %username% --email %email%
)
goto end

:create_staff
echo.
echo ========================================
echo Membuat Staff User: %username%
echo ========================================
echo.
echo PENTING: Password tidak akan terlihat saat diketik
echo.
if "%email%"=="" (
    python manage.py createsuperuser --username %username%
) else (
    python manage.py createsuperuser --username %username% --email %email%
)
if %errorLevel% equ 0 (
    echo.
    echo Mengubah ke staff user...
    python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='%username%'); u.is_superuser = False; u.save(); print('User berhasil diubah ke staff')"
)

:end
if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! User berhasil dibuat
    echo ========================================
    echo.
    echo Username: %username%
    echo Role: %role_name%
    echo.
) else (
    echo.
    echo ERROR: Gagal membuat user
    echo Kemungkinan username sudah digunakan
    echo.
)

pause
