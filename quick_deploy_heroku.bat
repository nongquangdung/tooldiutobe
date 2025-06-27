@echo off
echo =================================
echo  🚀 VOICE STUDIO HEROKU DEPLOY
echo =================================

echo Checking Heroku CLI...
heroku --version
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI chưa được cài đặt!
    echo Vui lòng cài từ: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo ✅ Heroku CLI OK!
echo.

echo Checking login...
heroku auth:whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔐 Đăng nhập Heroku...
    heroku login
    if %errorlevel% neq 0 (
        echo ❌ Login failed!
        pause
        exit /b 1
    )
)

echo ✅ Đã đăng nhập!
echo.

set /p APP_NAME="🎯 Nhập tên app (ví dụ: my-voice-studio): "
if "%APP_NAME%"=="" set APP_NAME=voice-studio-license

echo 📁 Chuyển vào thư mục license_server...
cd license_server

echo 🎯 Khởi tạo git repository...
git init

echo 📦 Add files...
git add .

echo 💾 Commit files...
git commit -m "Deploy Voice Studio License Server to Heroku"

echo 🚀 Tạo Heroku app: %APP_NAME%
heroku create %APP_NAME%
if %errorlevel% neq 0 (
    echo ⚠️  App name đã tồn tại, thử tên khác...
    set /p APP_NAME="Nhập tên app khác: "
    heroku create %APP_NAME%
)

echo 🌐 Deploy lên Heroku...
git push heroku main

echo 🎲 Tạo demo licenses...
heroku run "python admin.py demo"

echo 🌍 Mở app trong browser...
heroku open

echo.
echo =================================
echo  🎉 DEPLOY THÀNH CÔNG!
echo =================================

heroku apps:info --app %APP_NAME% | findstr "Web URL"

echo.
echo 📝 Next steps:
echo 1. Copy URL ở trên
echo 2. Chạy: python update_client_url.py [URL]
echo 3. Test: python simple_license_demo.py
echo 4. 💰 Start kiếm tiền!

cd ..
pause 