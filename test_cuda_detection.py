#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CUDA Detection - Kiểm tra GPU availability cho ChatterboxTTS
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_torch_cuda():
    """Test PyTorch CUDA availability"""
    print("🔍 PYTORCH CUDA DETECTION")
    print("=" * 50)
    
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
        
        # CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"🎯 CUDA Available: {cuda_available}")
        
        if cuda_available:
            print(f"   🏷️ CUDA Version: {torch.version.cuda}")
            print(f"   🎮 GPU Count: {torch.cuda.device_count()}")
            
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                memory_gb = props.total_memory / (1024**3)
                print(f"   🖥️ GPU {i}: {props.name}")
                print(f"      💾 Memory: {memory_gb:.1f}GB")
                print(f"      ⚡ Compute: {props.major}.{props.minor}")
        else:
            print("   ❌ No CUDA devices found")
            
        # Test device creation
        print(f"\n🧪 Device Test:")
        if cuda_available:
            device = torch.device("cuda:0")
            print(f"   ✅ CUDA device created: {device}")
            
            # Test memory
            print(f"   💾 Memory allocated: {torch.cuda.memory_allocated(0) / (1024**2):.1f}MB")
            print(f"   💾 Memory cached: {torch.cuda.memory_reserved(0) / (1024**2):.1f}MB")
        else:
            device = torch.device("cpu")
            print(f"   📱 CPU device: {device}")
            
    except ImportError as e:
        print(f"❌ PyTorch not available: {e}")
        return False
    except Exception as e:
        print(f"❌ CUDA test failed: {e}")
        return False
    
    return cuda_available

def test_chatterbox_device():
    """Test ChatterboxTTS device detection"""
    print("\n🎤 CHATTERBOX DEVICE DETECTION")
    print("=" * 50)
    
    try:
        from tts.real_chatterbox_provider import RealChatterboxProvider
        
        provider = RealChatterboxProvider()
        device_info = provider.get_device_info()
        
        print(f"📊 Device Info:")
        for key, value in device_info.items():
            print(f"   {key}: {value}")
            
        return device_info.get('device') == 'cuda'
        
    except Exception as e:
        print(f"❌ ChatterboxTTS device detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chatterbox_cuda_force():
    """Test force CUDA device trong ChatterboxTTS"""
    print("\n🚀 CHATTERBOX CUDA FORCE TEST")
    print("=" * 50)
    
    try:
        # Add chatterbox path
        chatterbox_path = r"D:\LearnCusor\BOTAY.COM\chatterbox\src"
        if chatterbox_path not in sys.path:
            sys.path.insert(0, chatterbox_path)
        
        from chatterbox.tts import ChatterboxTTS
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available, cannot force CUDA device")
            return False
        
        print("🔧 Forcing CUDA device...")
        
        # Force CUDA device
        device = "cuda"
        model = ChatterboxTTS.from_pretrained(device=device)
        
        print(f"✅ ChatterboxTTS loaded on: {device}")
        print(f"   📱 Model device: {next(model.parameters()).device}")
        
        # Test generation
        print("🧪 Testing generation...")
        text = "Hello, this is a CUDA test"
        result = model.generate(text)
        
        print(f"✅ Generation successful!")
        print(f"   📊 Result type: {type(result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ CUDA force test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """Test CUDA environment variables"""
    print("\n🌍 ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    cuda_vars = [
        'CUDA_HOME',
        'CUDA_PATH', 
        'CUDA_ROOT',
        'CUDA_TOOLKIT_ROOT_DIR',
        'LD_LIBRARY_PATH',
        'PATH'
    ]
    
    for var in cuda_vars:
        value = os.environ.get(var)
        if value:
            if 'PATH' in var and 'cuda' in value.lower():
                print(f"✅ {var}: {value[:100]}...")
            elif 'PATH' not in var:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def main():
    """Run all CUDA detection tests"""
    print("🎮 CUDA DETECTION TEST SUITE")
    print("Testing GPU availability for ChatterboxTTS")
    print("=" * 60)
    
    try:
        # Test 1: PyTorch CUDA
        torch_cuda = test_torch_cuda()
        
        # Test 2: Environment
        test_environment_variables()
        
        # Test 3: ChatterboxTTS device
        chatterbox_cuda = test_chatterbox_device()
        
        # Test 4: Force CUDA
        force_cuda = test_chatterbox_cuda_force()
        
        print("\n" + "=" * 60)
        print("📋 SUMMARY")
        print(f"✅ PyTorch CUDA: {torch_cuda}")
        print(f"✅ ChatterboxTTS CUDA: {chatterbox_cuda}")
        print(f"✅ Force CUDA: {force_cuda}")
        
        if torch_cuda and not chatterbox_cuda:
            print("\n⚠️ ISSUE DETECTED:")
            print("   PyTorch has CUDA but ChatterboxTTS using CPU")
            print("   💡 Possible fixes:")
            print("   1. Check ChatterboxTTS initialization")
            print("   2. Force device='cuda' in from_pretrained()")
            print("   3. Check GPU memory availability")
        elif torch_cuda and chatterbox_cuda:
            print("\n🎉 ALL GOOD!")
            print("   Both PyTorch and ChatterboxTTS using CUDA")
        else:
            print("\n📱 CPU MODE")
            print("   CUDA not available, using CPU")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 