param(
    [string]$HostAddress = "0.0.0.0",
    [int]$Port = 9000
)

$ErrorActionPreference = "Stop"

Write-Host "Checking Python 3.11..."
py -3.11 --version

Write-Host "Installing/updating dependencies..."
py -3.11 -m pip install -r requirements.txt

Write-Host "Applying database migrations..."
py -3.11 manage.py migrate

Write-Host "Starting IT Hub Dashboard on all network interfaces."
Write-Host "From this laptop: http://127.0.0.1`:$Port"
Write-Host "From another PC on the same network, use this laptop's LAN IP, for example: http://192.168.100.32`:$Port"
py -3.11 manage.py runserver "$HostAddress`:$Port"
