#!/usr/bin/env python3
"""
Chatterbox TTS Installation Script
Compatible với Python 3.9 và Apple M2/CUDA/CPU
"""
import subprocess
import sys
import platform
import os

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def detect_system():
    """Detect system and available hardware"""
    system = platform.system()
    arch = platform.machine()
    
    print(f"🖥️ System: {system} ({arch})")
    
    # Check for Apple Silicon
    if system == "Darwin" and arch == "arm64":
        return "apple_m2"
    
    # Check for CUDA on Linux/Windows
    elif system in ["Linux", "Windows"]:
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
        except ImportError:
            pass
    
    return "cpu"

def install_pytorch_for_system(hardware_type):
    """Install PyTorch appropriate for the system"""
    if hardware_type == "apple_m2":
        # Apple Silicon - use MPS optimized PyTorch
        command = "pip3 install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu"
        return run_command(command, "Installing PyTorch for Apple Silicon (MPS)")
    
    elif hardware_type == "cuda":
        # CUDA GPU - install CUDA-enabled PyTorch
        command = "pip3 install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118"
        return run_command(command, "Installing PyTorch with CUDA support")
    
    else:
        # CPU fallback
        command = "pip3 install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu"
        return run_command(command, "Installing PyTorch (CPU only)")

def install_compatible_dependencies():
    """Install compatible versions of dependencies"""
    dependencies = [
        ("numpy==1.24.3", "Installing compatible NumPy"),
        ("transformers==4.30.2", "Installing compatible Transformers"),
        ("librosa==0.10.1", "Installing compatible Librosa"),
        ("soundfile", "Installing SoundFile"),
        ("scipy<1.11.0", "Installing compatible SciPy"),
        ("einops==0.6.1", "Installing compatible Einops")
    ]
    
    success_count = 0
    for package, description in dependencies:
        if run_command(f"pip3 install {package}", description):
            success_count += 1
    
    return success_count == len(dependencies)

def install_chatterbox_alternative():
    """Install alternative TTS solution if Chatterbox fails"""
    print("🔄 Installing fallback TTS solutions...")
    
    alternatives = [
        ("pyttsx3", "Installing pyttsx3 (offline TTS)"),
        ("edge-tts", "Installing Edge TTS (Microsoft)"),
        ("TTS", "Installing Coqui TTS")
    ]
    
    for package, description in alternatives:
        run_command(f"pip3 install {package}", description)

def test_installation():
    """Test if installation works"""
    print("🧪 Testing installation...")
    
    test_script = """
import sys
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
    
    if torch.cuda.is_available():
        print(f"🎯 CUDA available: {torch.cuda.get_device_name(0)}")
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        print("🍎 Apple MPS available")
    else:
        print("💻 CPU mode")
    
    try:
        from chatterbox import ChatterboxTTS
        print("✅ Chatterbox TTS imported successfully")
        
        # Quick test
        tts = ChatterboxTTS()
        print("✅ Chatterbox TTS initialized")
        
    except Exception as e:
        print(f"⚠️ Chatterbox TTS not available: {e}")
        print("🔄 Fallback TTS will be used")
        
except Exception as e:
    print(f"❌ Installation test failed: {e}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e.stderr}")
        return False

def main():
    """Main installation flow"""
    print("🤖 Chatterbox TTS Installation for AI Video Generator")
    print("=" * 60)
    
    # Detect system
    hardware_type = detect_system()
    print(f"🎯 Detected hardware: {hardware_type}")
    
    # Install PyTorch
    if not install_pytorch_for_system(hardware_type):
        print("❌ PyTorch installation failed")
        return False
    
    # Install compatible dependencies
    if not install_compatible_dependencies():
        print("⚠️ Some dependencies failed to install")
    
    # Try to install Chatterbox TTS
    print("🔄 Installing Chatterbox TTS...")
    if not run_command("pip3 install git+https://github.com/resemble-ai/chatterbox.git", 
                      "Installing Chatterbox TTS from GitHub"):
        print("⚠️ Chatterbox TTS installation failed, installing alternatives...")
        install_chatterbox_alternative()
    
    # Test installation
    if test_installation():
        print("\n🎉 Installation completed successfully!")
        print("📱 Your device support:")
        
        if hardware_type == "apple_m2":
            print("   🍎 Apple M2 chip with MPS acceleration")
        elif hardware_type == "cuda":
            print("   🎯 NVIDIA GPU with CUDA acceleration")
        else:
            print("   💻 CPU processing")
        
        print("\n🚀 You can now use Chatterbox TTS in the AI Video Generator!")
        print("   • Go to Settings tab")
        print("   • Click '📱 Kiểm tra Device' to see your setup")
        print("   • Use '🧹 Xóa Cache' to clear memory if needed")
        
    else:
        print("\n⚠️ Installation completed with warnings")
        print("App will use fallback TTS providers (Google TTS, etc.)")
    
    return True

if __name__ == "__main__":
    main() 