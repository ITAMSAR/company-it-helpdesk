param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 9000
)

$ErrorActionPreference = "Stop"

Write-Host "Checking Python 3.11..."
py -3.11 --version

Write-Host "Installing/updating dependencies..."
py -3.11 -m pip install -r requirements.txt

Write-Host "Applying database migrations..."
py -3.11 manage.py migrate

Write-Host "Starting IT Hub Dashboard at http://$HostAddress`:$Port"
py -3.11 manage.py runserver "$HostAddress`:$Port"
