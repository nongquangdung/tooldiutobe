#!/usr/bin/env python3
"""
TEST ONLY NEW SIMPLE INNER VOICE
NO OLD PROCESSOR IMPORTS
"""

import sys
import os
import tempfile

# Setup paths
sys.path.insert(0, os.path.abspath('.'))

# Only import the new simple processor
from src.core.inner_voice_simple import apply_inner_voice_effects

def test_all_types():
    """Test all inner voice types with a dummy file"""
    
    print("🎵 TESTING ONLY NEW SIMPLE INNER VOICE")
    print("=" * 50)
    
    # Create a dummy audio file for testing
    dummy_input = "test_audio_output/dummy_input.wav"
    os.makedirs("test_audio_output", exist_ok=True)
    os.makedirs("test_inner_voice_output", exist_ok=True)
    
    # Create a minimal WAV file (silence)
    import wave
    import struct
    
    with wave.open(dummy_input, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        
        # 1 second of silence
        duration = 1.0
        frames = int(duration * 24000)
        
        for i in range(frames):
            wav_file.writeframes(struct.pack('<h', 0))
    
    print(f"✅ Created dummy input: {dummy_input}")
    
    # Test all types
    types = ['light', 'deep', 'dreamy']
    results = {}
    
    for voice_type in types:
        print(f"\n🎭 Testing {voice_type}...")
        
        output_file = f"test_inner_voice_output/test_{voice_type}.wav"
        
        success = apply_inner_voice_effects(
            input_file=dummy_input,
            output_file=output_file,
            voice_type=voice_type
        )
        
        if success and os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"✅ {voice_type}: Success! ({size} bytes)")
            results[voice_type] = True
        else:
            print(f"❌ {voice_type}: Failed!")
            results[voice_type] = False
    
    # Test custom params
    print(f"\n🔧 Testing custom parameters...")
    
    custom_params = {
        'delay': 500.0,
        'decay': 0.4,
        'gain': 0.6
    }
    
    custom_output = "test_inner_voice_output/test_custom.wav"
    
    success = apply_inner_voice_effects(
        input_file=dummy_input,
        output_file=custom_output,
        voice_type='light',
        custom_params=custom_params
    )
    
    if success and os.path.exists(custom_output):
        size = os.path.getsize(custom_output)
        print(f"✅ Custom: Success! ({size} bytes)")
        results['custom'] = True
    else:
        print(f"❌ Custom: Failed!")
        results['custom'] = False
    
    # Summary
    print(f"\n📊 RESULTS:")
    success_count = sum(1 for r in results.values() if r)
    total_count = len(results)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {name}")
    
    print(f"\n🎯 Success rate: {success_count}/{total_count} ({success_count/total_count*100:.0f}%)")
    
    # Cleanup
    try:
        os.remove(dummy_input)
    except:
        pass
    
    return success_count == total_count

if __name__ == "__main__":
    success = test_all_types()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n💥 SOME TESTS FAILED!")
        sys.exit(1) 