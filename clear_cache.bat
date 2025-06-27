@echo off
echo 🧹 Clearing Python cache for Voice Studio...
echo.

REM Xóa cache trong thư mục gốc
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ Cleared root __pycache__
)

REM Xóa cache trong src
if exist "src\__pycache__" (
    rmdir /s /q "src\__pycache__"
    echo ✅ Cleared src __pycache__
)

REM Xóa cache trong ui
if exist "src\ui\__pycache__" (
    rmdir /s /q "src\ui\__pycache__"
    echo ✅ Cleared ui __pycache__
)

REM Xóa cache trong core
if exist "src\core\__pycache__" (
    rmdir /s /q "src\core\__pycache__"
    echo ✅ Cleared core __pycache__
)

REM Xóa cache trong tts
if exist "src\tts\__pycache__" (
    rmdir /s /q "src\tts\__pycache__"
    echo ✅ Cleared tts __pycache__
)

REM Xóa cache trong ai
if exist "src\ai\__pycache__" (
    rmdir /s /q "src\ai\__pycache__"
    echo ✅ Cleared ai __pycache__
)

REM Xóa cache trong project
if exist "src\project\__pycache__" (
    rmdir /s /q "src\project\__pycache__"
    echo ✅ Cleared project __pycache__
)

REM Xóa cache trong video
if exist "src\video\__pycache__" (
    rmdir /s /q "src\video\__pycache__"
    echo ✅ Cleared video __pycache__
)

REM Xóa cache trong image
if exist "src\image\__pycache__" (
    rmdir /s /q "src\image\__pycache__"
    echo ✅ Cleared image __pycache__
)

echo.
echo 🎉 All Python cache cleared successfully!
echo 💡 You can now run Voice Studio without cache issues.
echo.
pause 