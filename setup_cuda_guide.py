#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CUDA Setup Guide - Hướng dẫn cài đặt GPU support cho ChatterboxTTS
"""

import sys
import os
import subprocess
import platform

def check_gpu_hardware():
    """Kiểm tra hardware GPU"""
    print("🖥️ GPU HARDWARE DETECTION")
    print("=" * 50)
    
    try:
        # Try nvidia-smi command
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ NVIDIA GPU detected!")
            lines = result.stdout.split('\n')
            for line in lines:
                if 'NVIDIA' in line or 'GeForce' in line or 'RTX' in line or 'GTX' in line:
                    print(f"   🎮 {line.strip()}")
            return True
        else:
            print("❌ nvidia-smi failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ nvidia-smi not found - No NVIDIA GPU or drivers not installed")
        return False

def check_current_pytorch():
    """Kiểm tra PyTorch hiện tại"""
    print("\n🔥 PYTORCH CURRENT STATUS")
    print("=" * 50)
    
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
        
        if '+cpu' in torch.__version__:
            print("⚠️ CPU-only version detected!")
            print("   This is why ChatterboxTTS is using CPU")
        elif '+cu' in torch.__version__:
            cuda_version = torch.__version__.split('+cu')[1]
            print(f"✅ CUDA version: {cuda_version}")
        
        print(f"🎯 CUDA Available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"   🎮 GPU Count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                print(f"   🖥️ GPU {i}: {props.name}")
        else:
            print("   ❌ No CUDA support in current PyTorch")
            
        return torch.cuda.is_available()
        
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def generate_cuda_install_commands():
    """Tạo commands để cài đặt CUDA PyTorch"""
    print("\n🚀 CUDA INSTALLATION GUIDE")
    print("=" * 50)
    
    print("📋 Step 1: Check NVIDIA Driver")
    print("   Run this command: nvidia-smi")
    print("   If it fails, install NVIDIA drivers first from:")
    print("   https://www.nvidia.com/Download/index.aspx")
    
    print("\n📋 Step 2: Install CUDA Toolkit (Optional but recommended)")
    print("   Download from: https://developer.nvidia.com/cuda-downloads")
    print("   Choose your OS and follow instructions")
    
    print("\n📋 Step 3: Install PyTorch with CUDA")
    print("   🔥 MOST IMPORTANT: Replace CPU PyTorch with CUDA version")
    print()
    
    # Get latest PyTorch CUDA commands
    print("   Option A: CUDA 11.8 (Recommended for compatibility)")
    print("   pip uninstall torch torchvision torchaudio")
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print()
    
    print("   Option B: CUDA 12.1 (Latest)")
    print("   pip uninstall torch torchvision torchaudio") 
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print()
    
    print("   Option C: Auto-detect (Recommended)")
    print("   Go to: https://pytorch.org/get-started/locally/")
    print("   Select your configuration and copy the command")

def test_performance_difference():
    """So sánh performance CPU vs GPU nếu có"""
    print("\n⚡ PERFORMANCE COMPARISON")
    print("=" * 50)
    
    try:
        import torch
        import time
        
        # Test tensor operations
        size = 1000
        cpu_tensor = torch.randn(size, size)
        
        # CPU test
        start_time = time.time()
        for _ in range(10):
            result = torch.mm(cpu_tensor, cpu_tensor)
        cpu_time = time.time() - start_time
        print(f"📱 CPU Performance: {cpu_time:.3f}s for 10 matrix multiplications")
        
        if torch.cuda.is_available():
            # GPU test
            gpu_tensor = cpu_tensor.cuda()
            torch.cuda.synchronize()
            
            start_time = time.time()
            for _ in range(10):
                result = torch.mm(gpu_tensor, gpu_tensor)
            torch.cuda.synchronize()
            gpu_time = time.time() - start_time
            
            speedup = cpu_time / gpu_time
            print(f"🎮 GPU Performance: {gpu_time:.3f}s for 10 matrix multiplications")
            print(f"🚀 GPU Speedup: {speedup:.1f}x faster than CPU")
            
            if speedup > 2:
                print("✅ Significant GPU advantage - CUDA worth installing!")
            else:
                print("⚠️ Minor GPU advantage - CPU may be sufficient")
        else:
            print("❌ No GPU available for comparison")
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")

def create_install_script():
    """Tạo script tự động cài đặt"""
    print("\n📝 AUTO INSTALL SCRIPT")
    print("=" * 50)
    
    script_content = """@echo off
echo Installing PyTorch with CUDA support...
echo.

echo Step 1: Uninstalling CPU-only PyTorch...
pip uninstall torch torchvision torchaudio -y

echo.
echo Step 2: Installing CUDA PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo Step 3: Testing installation...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

echo.
if torch.cuda.is_available():
    echo ✅ SUCCESS! CUDA PyTorch installed correctly
else:
    echo ❌ FAILED! CUDA not available - check NVIDIA drivers
endif

pause
"""
    
    with open("install_pytorch_cuda.bat", "w") as f:
        f.write(script_content)
    
    print("✅ Created install_pytorch_cuda.bat")
    print("   Run this script as Administrator to auto-install CUDA PyTorch")

def main():
    """Main diagnostic and setup guide"""
    print("🎮 CUDA SETUP DIAGNOSTIC & GUIDE")
    print("Setting up GPU acceleration for ChatterboxTTS")
    print("=" * 60)
    
    # Check system
    print(f"💻 System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Run checks
    has_gpu = check_gpu_hardware()
    has_cuda_pytorch = check_current_pytorch()
    
    # Analysis and recommendations
    print("\n" + "=" * 60)
    print("🎯 ANALYSIS & RECOMMENDATIONS")
    
    if not has_gpu:
        print("❌ ISSUE: No NVIDIA GPU detected")
        print("💡 SOLUTION: ")
        print("   1. Install NVIDIA GPU drivers")
        print("   2. Or continue using CPU (slower but works)")
        
    elif not has_cuda_pytorch:
        print("❌ ISSUE: NVIDIA GPU available but PyTorch is CPU-only")
        print("💡 SOLUTION: Install CUDA-enabled PyTorch")
        print("   This is why ChatterboxTTS is using CPU instead of GPU!")
        
        generate_cuda_install_commands()
        create_install_script()
        
        print("\n🚀 QUICK FIX:")
        print("   1. Run: pip uninstall torch torchvision torchaudio")
        print("   2. Run: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        print("   3. Restart your application")
        print("   4. ChatterboxTTS will automatically use GPU!")
        
    else:
        print("✅ ALL GOOD: GPU available and PyTorch has CUDA support")
        test_performance_difference()
    
    print("\n📚 Additional Resources:")
    print("   - PyTorch Installation: https://pytorch.org/get-started/locally/")
    print("   - CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
    print("   - NVIDIA Drivers: https://www.nvidia.com/Download/index.aspx")

if __name__ == "__main__":
    main() 