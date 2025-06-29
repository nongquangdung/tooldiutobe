#!/usr/bin/env python3
"""
Test Inner Voice Parameters - So sánh trước và sau cải tiến
Theo phân tích và gợi ý của user về thông số echo tối ưu
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.tts.voice_generator import VoiceGenerator
from src.core.inner_voice_simple import apply_inner_voice_effects

def test_improved_inner_voice():
    """Test inner voice với thông số cải tiến"""
    
    print("🎵 Testing Improved Inner Voice Parameters")
    print("=" * 50)
    
    # Test text
    test_text = "This is a test of our improved inner voice system with optimized echo parameters."
    
    # Create output directory
    output_dir = Path("test_improved_inner_voice")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize voice generator
    voice_gen = VoiceGenerator()
    
    # Test parameters - TRƯỚC KHI CẢI TIẾN
    old_params = {
        "light": {
            "delay": 50.0,
            "decay": 0.3, 
            "gain": 0.5,
            "filter": "aecho=0.5:0.3:50.0:0.3"
        },
        "deep": {
            "delay": 150.0,
            "decay": 0.6,
            "gain": 0.7,
            "filter": "aecho=0.7:0.6:150.0:0.6,lowpass=f=3000"
        },
        "dreamy": {
            "delay": 300.0,
            "decay": 0.8,
            "gain": 0.6,
            "filter": "volume=0.8,aecho=0.6:0.8:300.0:0.8,lowpass=f=3000"
        }
    }
    
    # Test parameters - SAU KHI CẢI TIẾN (theo gợi ý user)
    new_params = {
        "light": {
            "delay": 80.0,
            "decay": 0.35,
            "gain": 0.6,
            "filter": "aecho=0.6:0.4:80.0:0.35"
        },
        "deep": {
            "delay": 120.0,
            "decay": 0.7,
            "gain": 0.7,
            "filter": "aecho=0.7:0.7:120.0:0.7,lowpass=f=3000"
        },
        "dreamy": {
            "delay": 200.0,
            "decay": 0.8,
            "gain": 0.7,
            "filter": "volume=0.8,aecho=0.7:0.8:200.0:0.8,lowpass=f=3000"
        }
    }
    
    # 1. Generate base TTS first
    print("\n🎤 Generating base TTS audio...")
    base_file = output_dir / "base_audio.mp3"
    
    success = voice_gen.generate_voice(
        text=test_text,
        output_path=str(base_file),
        voice_name="Jordan",
        emotion_intensity=1.0,
        speed=1.0,
        cfg_weight=0.6
    )
    
    if not success or not base_file.exists():
        print("❌ Failed to generate base audio")
        return
    
    base_size = base_file.stat().st_size
    print(f"✅ Base audio generated: {base_size:,} bytes")
    
    # 2. Test old parameters
    print(f"\n🔸 Testing OLD parameters...")
    for voice_type, params in old_params.items():
        print(f"\n🟦 Testing OLD {voice_type}:")
        print(f"   📊 Delay: {params['delay']}ms, Decay: {params['decay']}, Gain: {params['gain']}")
        
        output_file = output_dir / f"old_{voice_type}.mp3"
        
        # Apply effects with custom parameters
        custom_params = {
            'delay': params['delay'],
            'decay': params['decay'], 
            'gain': params['gain']
        }
        
        success = apply_inner_voice_effects(
            input_file=str(base_file),
            output_file=str(output_file),
            voice_type=voice_type,
            custom_params=custom_params
        )
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            size_diff = file_size - base_size
            print(f"   ✅ Generated: {file_size:,} bytes ({size_diff:+,} vs base)")
        else:
            print(f"   ❌ Failed to generate {voice_type}")
    
    # 3. Test new parameters  
    print(f"\n🔹 Testing NEW parameters (User improved)...")
    for voice_type, params in new_params.items():
        print(f"\n🟦 Testing NEW {voice_type}:")
        print(f"   📊 Delay: {params['delay']}ms, Decay: {params['decay']}, Gain: {params['gain']}")
        print(f"   🎯 Expected: {get_voice_description(voice_type)}")
        
        output_file = output_dir / f"new_{voice_type}.mp3"
        
        # Apply effects with custom parameters
        custom_params = {
            'delay': params['delay'],
            'decay': params['decay'],
            'gain': params['gain']
        }
        
        success = apply_inner_voice_effects(
            input_file=str(base_file),
            output_file=str(output_file),
            voice_type=voice_type,
            custom_params=custom_params
        )
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            size_diff = file_size - base_size
            print(f"   ✅ Generated: {file_size:,} bytes ({size_diff:+,} vs base)")
        else:
            print(f"   ❌ Failed to generate {voice_type}")
    
    # 4. Test current config from file
    print(f"\n🔹 Testing CURRENT config from file...")
    for voice_type in ['light', 'deep', 'dreamy']:
        print(f"\n🟦 Testing CONFIG {voice_type}:")
        
        output_file = output_dir / f"config_{voice_type}.mp3"
        
        success = apply_inner_voice_effects(
            input_file=str(base_file),
            output_file=str(output_file),
            voice_type=voice_type,
            custom_params=None  # Use config file
        )
        
        if success and output_file.exists():
            file_size = output_file.stat().st_size
            size_diff = file_size - base_size
            print(f"   ✅ Generated: {file_size:,} bytes ({size_diff:+,} vs base)")
        else:
            print(f"   ❌ Failed to generate {voice_type}")
    
    # 5. Summary
    print(f"\n🎉 Test completed! Results in: {output_dir}")
    print(f"\n📂 Generated files:")
    
    categories = [
        ("Base Audio", "base_*.mp3"),
        ("OLD Parameters", "old_*.mp3"), 
        ("NEW Parameters", "new_*.mp3"),
        ("Config File", "config_*.mp3")
    ]
    
    for category, pattern in categories:
        print(f"\n📁 {category}:")
        files = sorted(output_dir.glob(pattern))
        for file in files:
            size = file.stat().st_size
            print(f"   📄 {file.name} ({size:,} bytes)")
    
    print(f"\n🎧 Comparison Guide:")
    print(f"   🔸 OLD vs NEW: Compare same voice types to hear improvements")
    print(f"   🔹 CONFIG: Should match NEW parameters (latest config)")
    print(f"   🎯 Listen for: Echo clarity, depth, and naturalness")

def get_voice_description(voice_type):
    """Get expected description for voice type"""
    descriptions = {
        "light": "Thì thầm nội tâm, bóng âm mờ nhạt, tự nhiên hơn",
        "deep": "Vọng trong tâm trí, ấm trầm, echo dày hơn", 
        "dreamy": "Phi thực, như trong giấc mơ, delay rõ ràng hơn"
    }
    return descriptions.get(voice_type, "Unknown")

if __name__ == "__main__":
    test_improved_inner_voice() 