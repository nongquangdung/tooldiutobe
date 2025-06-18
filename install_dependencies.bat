@echo off
echo ========================================
echo  Installing ALL Dependencies
echo  for ChatterboxTTS & AI Video Generator
echo ========================================
echo.

echo Step 1: Check current PyTorch version...
python -c "import torch; print('Current PyTorch:', torch.__version__)"
echo.

echo Step 2: Installing missing Python packages...
pip install torchaudio
pip install pydub
pip install ffmpeg-python
echo.

echo Step 3: Installing ffmpeg (for audio processing)...
echo Downloading ffmpeg...
powershell -Command "& { Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip' }"

echo Extracting ffmpeg...
powershell -Command "& { Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg-temp' -Force }"

echo Moving ffmpeg to tools directory...
if not exist "tools" mkdir tools
if not exist "tools\ffmpeg" mkdir tools\ffmpeg
xcopy "ffmpeg-temp\ffmpeg-master-latest-win64-gpl\bin\*" "tools\ffmpeg\" /Y

echo Cleaning up...
rmdir /s /q ffmpeg-temp
del ffmpeg.zip

echo.
echo Step 4: Adding ffmpeg to PATH (current session)...
set PATH=%CD%\tools\ffmpeg;%PATH%

echo.
echo Step 5: Testing installations...
echo Testing PyTorch + torchaudio...
python -c "import torch, torchaudio; print('✅ PyTorch + torchaudio OK')"

echo Testing ffmpeg...
tools\ffmpeg\ffmpeg.exe -version | findstr /C:"ffmpeg version"

echo Testing pydub...
python -c "import pydub; print('✅ pydub OK')"

echo.
echo Step 6: Testing ChatterboxTTS import...
python -c "import sys; sys.path.append('src'); from tts.real_chatterbox_provider import RealChatterboxProvider; provider = RealChatterboxProvider(); print('ChatterboxTTS status:', provider.available)"

echo.
echo ========================================
echo Installation completed!
echo.
echo IMPORTANT: 
echo 1. ffmpeg is installed in tools\ffmpeg\
echo 2. Add to your permanent PATH: %CD%\tools\ffmpeg
echo 3. Or restart app to use local ffmpeg
echo ========================================
pause 