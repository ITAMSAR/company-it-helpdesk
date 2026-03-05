@echo off
echo ========================================
echo Starting IT Hub Internal (Network Mode)
echo ========================================
echo.
echo Server akan berjalan di:
echo - PC ini: http://127.0.0.1:8000
echo - Dari laptop: http://192.168.1.4:8000
echo.
echo PENTING:
echo 1. Pastikan firewall Windows mengizinkan port 8000
echo 2. PC dan laptop harus di jaringan yang sama
echo 3. Gunakan IP address di atas untuk akses dari laptop
echo.
echo Tekan Ctrl+C untuk stop server
echo ========================================
echo.
python manage.py runserver 0.0.0.0:8000
pause
