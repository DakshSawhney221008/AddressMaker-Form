# Get Tunnel URLs script
Write-Host "Checking localtunnel URLs..." -ForegroundColor Cyan

# First check if the command exists
if (Get-Command lt -ErrorAction SilentlyContinue) {
    Write-Host "Localtunnel is installed." -ForegroundColor Green
    
    # Start backend tunnel temporarily just to get URL
    $backendProcess = Start-Process -PassThru -NoNewWindow powershell -ArgumentList "-ExecutionPolicy Bypass -Command `"lt --port 5000 --print-url`""
    Start-Sleep -Seconds 5
    Write-Host "Backend API URL should appear in a separate window." -ForegroundColor Yellow
    
    # Start frontend tunnel temporarily just to get URL
    $frontendProcess = Start-Process -PassThru -NoNewWindow powershell -ArgumentList "-ExecutionPolicy Bypass -Command `"lt --port 8000 --print-url`""
    Start-Sleep -Seconds 5
    Write-Host "Frontend URL should appear in a separate window." -ForegroundColor Yellow
    
    Write-Host "`nAfter noting the URLs, you can update your code:" -ForegroundColor Green
    Write-Host "1. In submit.js, update the fetch URLs" -ForegroundColor Yellow
    Write-Host "2. In index.html, update the fetch URL in the form submission code" -ForegroundColor Yellow
    
    Write-Host "`nPress Enter to close the temporary processes..." -ForegroundColor Cyan
    Read-Host
    
    # Cleanup
    if ($backendProcess) { Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue }
    if ($frontendProcess) { Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue }
} else {
    Write-Host "Localtunnel (lt) is not available in your PATH. Please make sure it's installed correctly." -ForegroundColor Red
}

Write-Host "`nDon't forget to run these commands in separate windows to keep your tunnels active:" -ForegroundColor Green
Write-Host "powershell -ExecutionPolicy Bypass -Command `"lt --port 5000`"" -ForegroundColor Yellow
Write-Host "powershell -ExecutionPolicy Bypass -Command `"lt --port 8000`"" -ForegroundColor Yellow 