@echo off
echo ========================================
echo  Installing PyTorch with CUDA support
echo  for ChatterboxTTS GPU acceleration
echo ========================================
echo.

echo Step 1: Uninstalling CPU-only PyTorch...
pip uninstall torch torchvision torchaudio -y

echo.
echo Step 2: Installing CUDA PyTorch + torchaudio (CUDA 11.8)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo Step 3: Testing CUDA installation...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"

echo.
echo Step 4: Testing ChatterboxTTS device detection...
python -c "import sys; sys.path.append('src'); from tts.real_chatterbox_provider import RealChatterboxProvider; provider = RealChatterboxProvider(); print('ChatterboxTTS device:', provider.device_name)"

echo.
echo ========================================
echo Installation completed!
echo ChatterboxTTS should now use GPU instead of CPU
echo ========================================
pause
