@echo off
echo Installing psutil into venv_clean...

REM Activate venv_clean and install psutil
call .\venv_clean\Scripts\activate.bat
pip install psutil==5.9.8
echo.
echo psutil installation completed!
pause 