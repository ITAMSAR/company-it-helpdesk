@echo off
echo ========================================
echo Daftar User - IT Hub Internal
echo ========================================
echo.
echo Menampilkan semua user yang terdaftar...
echo.

python -c "import django; django.setup(); from django.contrib.auth.models import User; users = User.objects.all(); print('Total user:', users.count()); print('\n' + '='*60); [print(f'\nUsername: {u.username}\nEmail: {u.email or \"-\"}\nRole: {\"Admin\" if u.is_superuser else \"Staff\" if u.is_staff else \"User\"}\nAktif: {\"Ya\" if u.is_active else \"Tidak\"}\nTerakhir login: {u.last_login or \"Belum pernah\"}\n' + '-'*60) for u in users]"

echo.
echo ========================================
echo.
echo Untuk mengelola user:
echo - Buat user baru: CREATE_USER.bat
echo - Ganti password: CHANGE_PASSWORD.bat
echo - Hapus user: DELETE_USER.bat
echo.
pause
