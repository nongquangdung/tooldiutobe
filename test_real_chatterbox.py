#!/usr/bin/env python3
"""
Test script cho Real Chatterbox TTS Provider
"""
import sys
import os
sys.path.append('src')

print("🚀 Starting Real Chatterbox TTS Test...")

try:
    from tts.real_chatterbox_provider import RealChatterboxProvider
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_real_chatterbox():
    print("🧪 Testing Real Chatterbox TTS Provider...")
    
    # Initialize provider
    provider = RealChatterboxProvider()
    
    # Print device info
    info = provider.get_device_info()
    print(f"📱 Device Info:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    if not provider.available:
        print("❌ Real Chatterbox TTS not available")
        return False
    
    # Test text generation
    test_text = "Xin chào, đây là test giọng nói từ Chatterbox TTS."
    output_path = "test_audio_output/test_chatterbox_real.wav"
    
    print(f"\n🎤 Testing voice generation...")
    print(f"   Text: {test_text}")
    print(f"   Output: {output_path}")
    
    result = provider.generate_voice(
        text=test_text,
        save_path=output_path,
        emotion_exaggeration=1.2,
        speed=1.0,
        cfg_weight=0.7
    )
    
    if result.get('success'):
        print("✅ Voice generation successful!")
        if os.path.exists(output_path):
            print(f"   File saved: {output_path}")
            file_size = os.path.getsize(output_path)
            print(f"   File size: {file_size} bytes")
        else:
            print("❌ Audio file not found")
    else:
        print(f"❌ Voice generation failed: {result.get('error', 'Unknown error')}")
    
    return result.get('success', False)

if __name__ == "__main__":
    success = test_real_chatterbox()
    print(f"\n🏁 Test {'PASSED' if success else 'FAILED'}") 