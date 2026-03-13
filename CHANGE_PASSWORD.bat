@echo off
echo ========================================
echo Ganti Password User - IT Hub Internal
echo ========================================
echo.
echo Script ini akan mengubah password user yang sudah ada
echo.
pause

:input_username
echo.
set /p username="Masukkan username yang ingin diganti passwordnya: "
if "%username%"=="" (
    echo Username tidak boleh kosong!
    goto input_username
)

echo.
echo ========================================
echo Mengubah password untuk: %username%
echo ========================================
echo.
echo PENTING: Password tidak akan terlihat saat diketik
echo.

python manage.py changepassword %username%

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Password berhasil diubah
    echo ========================================
    echo.
) else (
    echo.
    echo ERROR: Gagal mengubah password
    echo User mungkin tidak ditemukan
    echo.
)

pause
