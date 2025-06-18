#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test All Dependencies - Kiểm tra tất cả packages và tools cần thiết
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_python_packages():
    """Test các Python packages cần thiết"""
    print("🐍 PYTHON PACKAGES TEST")
    print("=" * 50)
    
    packages = [
        ("torch", "PyTorch for AI models"),
        ("torchaudio", "Audio processing for ChatterboxTTS"),
        ("pydub", "Audio manipulation"),
        ("PySide6", "Qt GUI framework"),
        ("requests", "HTTP requests"),
    ]
    
    results = {}
    
    for package, description in packages:
        try:
            if package == "torch":
                import torch
                print(f"✅ {package}: {torch.__version__} ({description})")
                print(f"   CUDA Available: {torch.cuda.is_available()}")
                results[package] = True
            elif package == "torchaudio":
                import torchaudio
                print(f"✅ {package}: {torchaudio.__version__} ({description})")
                results[package] = True
            elif package == "pydub":
                import pydub
                print(f"✅ {package}: Available ({description})")
                results[package] = True
            elif package == "PySide6":
                import PySide6
                print(f"✅ {package}: {PySide6.__version__} ({description})")
                results[package] = True
            elif package == "requests":
                import requests
                print(f"✅ {package}: {requests.__version__} ({description})")
                results[package] = True
            else:
                __import__(package)
                print(f"✅ {package}: Available ({description})")
                results[package] = True
                
        except ImportError as e:
            print(f"❌ {package}: Not available - {e}")
            results[package] = False
        except Exception as e:
            print(f"⚠️ {package}: Error - {e}")
            results[package] = False
    
    return results

def test_ffmpeg():
    """Test ffmpeg availability"""
    print("\n🎵 FFMPEG TEST")
    print("=" * 50)
    
    import subprocess
    
    # Test system ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ System ffmpeg: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ System ffmpeg: Not found")
    
    # Test local ffmpeg
    local_ffmpeg = os.path.join("tools", "ffmpeg", "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        try:
            result = subprocess.run([local_ffmpeg, '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ Local ffmpeg: {version_line}")
                return True
        except:
            print("❌ Local ffmpeg: Found but not working")
    else:
        print("❌ Local ffmpeg: Not found in tools/ffmpeg/")
        print("   Run install_dependencies.bat to download")
    
    return False

def test_chatterbox_integration():
    """Test ChatterboxTTS integration"""
    print("\n🎤 CHATTERBOX INTEGRATION TEST")
    print("=" * 50)
    
    try:
        from tts.real_chatterbox_provider import RealChatterboxProvider
        
        provider = RealChatterboxProvider()
        device_info = provider.get_device_info()
        
        print("📊 ChatterboxTTS Status:")
        for key, value in device_info.items():
            status = "✅" if value else "❌"
            if key == "device_name" and value != "Unknown":
                status = "✅"
            print(f"   {key}: {status} {value}")
        
        # Test model loading
        if provider.available and provider.is_initialized:
            print("✅ ChatterboxTTS ready for use!")
            return True
        else:
            print("❌ ChatterboxTTS not ready")
            if not device_info.get("torch_available"):
                print("   Fix: Install PyTorch + torchaudio")
            if not device_info.get("chatterbox_available"):
                print("   Fix: Check chatterbox installation")
            return False
            
    except Exception as e:
        print(f"❌ ChatterboxTTS integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive dependency test"""
    print("🔍 COMPREHENSIVE DEPENDENCY TEST")
    print("Testing all requirements for ChatterboxTTS AI Video Generator")
    print("=" * 70)
    
    # Run all tests
    package_results = test_python_packages()
    ffmpeg_ok = test_ffmpeg()
    chatterbox_ok = test_chatterbox_integration()
    
    # Combine results
    all_results = {
        **package_results,
        "ffmpeg": ffmpeg_ok,
        "chatterbox": chatterbox_ok
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    total_tests = len(all_results)
    passed_tests = sum(all_results.values())
    
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 PERFECT! All dependencies ready!")
    elif passed_tests >= total_tests * 0.8:
        print("✅ GOOD! Minor issues need fixing")
    else:
        print("⚠️ ISSUES! Several dependencies need attention")
    
    # Installation guide
    print("\n📋 QUICK FIXES:")
    if not all(package_results.values()):
        print("1. Install missing packages: ./install_dependencies.bat")
    if not ffmpeg_ok:
        print("2. Install ffmpeg: included in install_dependencies.bat")
    if not chatterbox_ok:
        print("3. Fix ChatterboxTTS: Check local clone or install package")

if __name__ == "__main__":
    main() 