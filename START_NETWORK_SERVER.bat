@echo off
color 0A
echo ========================================
echo    IT HUB INTERNAL - NETWORK MODE
echo ========================================
echo.
echo 🌐 Server akan berjalan di: 192.168.1.11:8000
echo 📱 QR Code akan berfungsi untuk HP
echo.
echo PASTIKAN:
echo ✅ HP dan komputer di WiFi yang sama
echo ✅ Firewall Windows mengizinkan Python
echo.
echo 🚀 Starting server...
echo ========================================
echo.
python manage.py runserver 0.0.0.0:8000
echo.
echo Server stopped. Press any key to exit...
pause > nul