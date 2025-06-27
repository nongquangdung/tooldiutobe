@echo off
echo =================================
echo  📥 AUTO INSTALL HEROKU CLI
echo =================================

echo 🔍 Checking if Heroku CLI already installed...
heroku --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Heroku CLI đã được cài đặt!
    heroku --version
    echo.
    echo 🚀 Bạn có thể chạy deploy ngay:
    echo .\quick_deploy_heroku.bat
    pause
    exit /b 0
)

echo ❌ Heroku CLI chưa được cài đặt
echo.

echo 📥 Downloading Heroku CLI...
echo URL: https://cli-assets.heroku.com/heroku-x64.exe

echo.
echo 🎯 Có 2 cách cài đặt:
echo.
echo 1️⃣  AUTO DOWNLOAD (PowerShell):
echo    powershell -Command "Invoke-WebRequest -Uri 'https://cli-assets.heroku.com/heroku-x64.exe' -OutFile 'heroku-installer.exe'; Start-Process 'heroku-installer.exe'"
echo.
echo 2️⃣  MANUAL DOWNLOAD (Browser):
echo    Vào: https://devcenter.heroku.com/articles/heroku-cli
echo    Download "64-bit Installer" và install
echo.

set /p choice="Chọn cách cài đặt (1 hoặc 2): "

if "%choice%"=="1" (
    echo 🚀 Auto downloading...
    powershell -Command "Invoke-WebRequest -Uri 'https://cli-assets.heroku.com/heroku-x64.exe' -OutFile 'heroku-installer.exe'"
    if exist heroku-installer.exe (
        echo ✅ Download thành công!
        echo 🛠️  Khởi chạy installer...
        start heroku-installer.exe
        echo.
        echo ⚠️  SAU KHI CÀI XONG:
        echo 1. Restart PowerShell 
        echo 2. Chạy: .\quick_deploy_heroku.bat
        pause
    ) else (
        echo ❌ Download failed, dùng cách 2 (manual)
    )
) else (
    echo 🌐 Opening browser...
    start https://devcenter.heroku.com/articles/heroku-cli
    echo.
    echo 📝 Instructions:
    echo 1. Download "64-bit Installer"
    echo 2. Install như bình thường
    echo 3. Restart PowerShell
    echo 4. Chạy: .\quick_deploy_heroku.bat
)

echo.
pause 