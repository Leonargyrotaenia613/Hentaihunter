# HentaiHunter - PowerShell Installer
# Run: irm https://raw.githubusercontent.com/sinkaroid/Hentaihunter/master/install.ps1 | iex

$ErrorActionPreference = "Stop"
$repo = "https://github.com/sinkaroid/Hentaihunter"
$raw  = "https://raw.githubusercontent.com/sinkaroid/Hentaihunter/master"

Write-Host ""
Write-Host " HentaiHunter v2.0 - Installer" -ForegroundColor Magenta
Write-Host " github.com/sinkaroid/Hentaihunter" -ForegroundColor DarkGray
Write-Host ""

# Check Python
try {
    $pyver = python --version 2>&1
    Write-Host "[+] Found: $pyver" -ForegroundColor Green
} catch {
    Write-Host "[*] Python not found. Installing..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --silent
}

# Download files
$files = @("hentaihunter.py", "requirements.txt")
$dest  = "$env:USERPROFILE\HentaiHunter"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

foreach ($f in $files) {
    Write-Host "[*] Downloading $f..." -ForegroundColor Cyan
    Invoke-WebRequest "$raw/$f" -OutFile "$dest\$f"
}

# Install deps
Write-Host "[*] Installing dependencies..." -ForegroundColor Cyan
pip install -r "$dest\requirements.txt" --quiet

# Create launcher in PATH
$launcher = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\hh.cmd"
@"
@echo off
python "$dest\hentaihunter.py" %*
"@ | Set-Content $launcher

Write-Host ""
Write-Host " [OK] Done! HentaiHunter is ready." -ForegroundColor Green
Write-Host ""
Write-Host " Usage:" -ForegroundColor White
Write-Host "   hh https://nhentai.net/g/177013/" -ForegroundColor Cyan
Write-Host "   hh --list" -ForegroundColor Cyan
Write-Host "   hh URL -o D:\Downloads -t 8" -ForegroundColor Cyan
Write-Host ""
