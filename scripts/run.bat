@echo off
cd /d "%~dp0.."
echo Starting IT Hub Internal...
python manage.py runserver
pause
