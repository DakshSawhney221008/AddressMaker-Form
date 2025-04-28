# Tunnel script for Real Estate form
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"

Write-Host "Starting tunnels for Real Estate Form app..." -ForegroundColor Green
Write-Host "API Server (port 5000)" -ForegroundColor Cyan

# Start Backend tunnel
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c node $env:APPDATA\npm\node_modules\localtunnel\bin\lt.js --port 5000"

Write-Host "Frontend Server (port 8000)" -ForegroundColor Cyan

# Start Frontend tunnel
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c node $env:APPDATA\npm\node_modules\localtunnel\bin\lt.js --port 8000"

Write-Host "Tunnels should be active now. Check the console output for URLs." -ForegroundColor Green
Write-Host "Press any key to stop the tunnels..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 