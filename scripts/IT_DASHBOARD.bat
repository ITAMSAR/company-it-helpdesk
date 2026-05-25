@echo off
cd /d "%~dp0.."
title IT Hub Internal Tools
color 0A
set "PYTHON_CMD=python"
set "PIP_CMD=python -m pip"
if exist venv\Scripts\python.exe (
    set "PYTHON_CMD=venv\Scripts\python.exe"
    set "PIP_CMD=venv\Scripts\python.exe -m pip"
)

:menu
cls
echo ========================================
echo        IT HUB INTERNAL - TOOLS
echo ========================================
echo Project: %CD%
echo.
echo  1. Start server localhost
echo  2. Start server network / LAN
echo  3. Start server with venv
echo  4. Open dashboard
echo  5. Check server status
echo.
echo  6. Setup first install
echo  7. Update database / migrate
echo  8. Create admin/staff user
echo  9. Change user password
echo 10. List users
echo 11. Delete user
echo.
echo 12. Setup firewall port 8000
echo 13. Stop Python/Django server
echo 14. Reset fresh database
echo  0. Exit
echo.
set /p choice="Choose option: "

if "%choice%"=="1" goto start_local
if "%choice%"=="2" goto start_network
if "%choice%"=="3" goto start_venv
if "%choice%"=="4" goto open_dashboard
if "%choice%"=="5" goto check_server
if "%choice%"=="6" goto setup
if "%choice%"=="7" goto migrate
if "%choice%"=="8" goto create_user
if "%choice%"=="9" goto change_password
if "%choice%"=="10" goto list_users
if "%choice%"=="11" goto delete_user
if "%choice%"=="12" goto firewall
if "%choice%"=="13" goto stop_server
if "%choice%"=="14" goto reset_fresh
if "%choice%"=="0" exit /b 0
goto menu

:start_local
cls
call :ensure_django || goto django_error
echo Starting server at http://127.0.0.1:8000
echo Press Ctrl+C to stop.
echo.
"%PYTHON_CMD%" manage.py runserver
pause
goto menu

:start_network
cls
call :ensure_django || goto django_error
echo Starting server at http://0.0.0.0:8000
echo Use your PC LAN IP from another device, for example:
echo http://192.168.1.11:8000
echo Press Ctrl+C to stop.
echo.
"%PYTHON_CMD%" manage.py runserver 0.0.0.0:8000
pause
goto menu

:start_venv
cls
if not exist venv\Scripts\activate.bat (
    echo venv not found. Run option 6 first.
    pause
    goto menu
)
call venv\Scripts\activate.bat
set "PYTHON_CMD=venv\Scripts\python.exe"
call :ensure_django || goto django_error
echo Starting server with venv at http://0.0.0.0:8000
echo Press Ctrl+C to stop.
echo.
"%PYTHON_CMD%" manage.py runserver 0.0.0.0:8000
pause
goto menu

:open_dashboard
cls
echo Opening dashboard...
start http://127.0.0.1:8000
timeout /t 2 /nobreak >nul
goto menu

:check_server
cls
echo Checking http://localhost:8000 ...
echo.
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 3 -UseBasicParsing; Write-Host 'Server ACTIVE - Status:' $response.StatusCode -ForegroundColor Green } catch { Write-Host 'Server NOT ACTIVE' -ForegroundColor Red }"
echo.
pause
goto menu

:setup
cls
echo [1/5] Checking Python...
python --version
if errorlevel 1 goto python_error
echo.
echo [2/5] Creating virtual environment if needed...
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo Existing venv looks broken.
        set /p recreate_venv="Recreate venv folder? (y/n): "
        if /i "%recreate_venv%"=="y" (
            rmdir /s /q venv
        ) else (
            goto command_error
        )
    )
)
if not exist venv\Scripts\python.exe (
    python -m venv venv
    if errorlevel 1 goto command_error
)
set "PYTHON_CMD=venv\Scripts\python.exe"
set "PIP_CMD=venv\Scripts\python.exe -m pip"
echo.
echo [3/5] Installing dependencies...
"%PIP_CMD%" install -r requirements.txt
if errorlevel 1 goto command_error
echo.
echo [4/5] Running migrations...
"%PYTHON_CMD%" manage.py makemigrations
"%PYTHON_CMD%" manage.py migrate
if errorlevel 1 goto command_error
echo.
echo [5/5] Creating admin user...
"%PYTHON_CMD%" manage.py createsuperuser
echo.
echo Setup complete.
pause
goto menu

:migrate
cls
call :ensure_django || goto django_error
echo This will migrate database without deleting data.
echo A local backup will be created as db.sqlite3.backup-local.
echo.
pause
if exist db.sqlite3 copy db.sqlite3 db.sqlite3.backup-local
"%PYTHON_CMD%" manage.py makemigrations
"%PYTHON_CMD%" manage.py migrate
if errorlevel 1 goto command_error
echo.
echo Migration complete.
pause
goto menu

:create_user
cls
call :ensure_django || goto django_error
"%PYTHON_CMD%" manage.py createsuperuser
pause
goto menu

:change_password
cls
call :ensure_django || goto django_error
set /p username="Username to change password: "
if "%username%"=="" goto menu
"%PYTHON_CMD%" manage.py changepassword %username%
pause
goto menu

:list_users
cls
call :ensure_django || goto django_error
"%PYTHON_CMD%" manage.py shell -c "from django.contrib.auth.models import User; users=User.objects.all(); print('Total user:', users.count()); [print(u.username, '|', u.email or '-', '|', 'Admin' if u.is_superuser else 'Staff' if u.is_staff else 'User', '| Active:', u.is_active) for u in users]"
pause
goto menu

:delete_user
cls
call :ensure_django || goto django_error
set /p username="Username to delete: "
if "%username%"=="" goto menu
echo.
set /p confirm="Delete user '%username%'? Type YES: "
if /i not "%confirm%"=="YES" goto menu
"%PYTHON_CMD%" manage.py shell -c "from django.contrib.auth.models import User; User.objects.get(username='%username%').delete(); print('Deleted: %username%')"
pause
goto menu

:firewall
cls
echo This option must be run as Administrator.
echo.
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Please right-click this file and choose Run as administrator.
    pause
    goto menu
)
netsh advfirewall firewall delete rule name="Django IT Hub - Port 8000" >nul 2>&1
netsh advfirewall firewall add rule name="Django IT Hub - Port 8000" dir=in action=allow protocol=TCP localport=8000
pause
goto menu

:stop_server
cls
echo Stopping Python/Django processes...
taskkill /f /im python.exe /fi "WINDOWTITLE eq *runserver*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *manage.py*" 2>nul
echo Done.
pause
goto menu

:reset_fresh
cls
call :ensure_django || goto django_error
echo WARNING: This will delete db.sqlite3 and all local data.
set /p confirm="Type RESET to continue: "
if /i not "%confirm%"=="RESET" goto menu
taskkill /F /IM python.exe 2>nul
if exist db.sqlite3 del db.sqlite3
"%PYTHON_CMD%" manage.py migrate
"%PYTHON_CMD%" manage.py createsuperuser
pause
goto menu

:ensure_django
"%PYTHON_CMD%" -c "import django" >nul 2>&1
exit /b %errorlevel%

:python_error
echo.
echo ERROR: Python not found.
pause
goto menu

:command_error
echo.
echo ERROR: Command failed. Check the message above.
pause
goto menu

:django_error
echo.
echo ERROR: Django is not installed for this Python:
echo %PYTHON_CMD%
echo.
echo Choose option 6 to setup/install dependencies first.
echo If venv is broken, delete the venv folder and run option 6 again.
pause
goto menu
