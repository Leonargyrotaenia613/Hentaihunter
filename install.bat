@echo off
:: HentaiHunter - Windows One-Line Installer
:: Run: curl -sSL https://raw.githubusercontent.com/sinkaroid/Hentaihunter/master/install.bat | cmd

title HentaiHunter Installer
color 0D

echo.
echo  ██╗  ██╗██╗  ██╗   HentaiHunter v2.0
echo  ██║  ██║██║  ██║   Doujinshi Downloader
echo  ███████║███████║   
echo  ╚══════╝╚══════╝   github.com/sinkaroid/Hentaihunter
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found. Installing via winget...
    winget install -e --id Python.Python.3.11 --silent
    if errorlevel 1 (
        echo [!] winget failed. Please install Python from https://python.org
        pause
        exit /b 1
    )
    echo [+] Python installed!
)

:: Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip not found, trying to fix...
    python -m ensurepip --upgrade
)

:: Clone or download
where git >nul 2>&1
if not errorlevel 1 (
    echo [*] Cloning repository...
    git clone https://github.com/sinkaroid/Hentaihunter.git
    cd Hentaihunter
) else (
    echo [*] Downloading via curl...
    curl -sSL https://github.com/sinkaroid/Hentaihunter/archive/refs/heads/master.zip -o hh.zip
    tar -xf hh.zip
    rename Hentaihunter-master Hentaihunter
    cd Hentaihunter
    del hh.zip
)

:: Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt --quiet

:: Create shortcut launcher
echo @echo off > "%~dp0hh.bat"
echo python "%~dp0Hentaihunter\hentaihunter.py" %%* >> "%~dp0hh.bat"

echo.
echo  [OK] HentaiHunter installed successfully!
echo.
echo  Usage:
echo    python hentaihunter.py https://nhentai.net/g/177013/
echo    python hentaihunter.py --list
echo    python hentaihunter.py URL -o C:\Downloads -t 8
echo.
pause
