#!/usr/bin/env python3

import sys
import os
import tempfile
sys.path.insert(0, 'src')

from src.tts.real_chatterbox_provider import RealChatterboxProvider

def test_voice_preview():
    print("🎧 Testing voice preview functionality...")
    
    # Get provider instance
    provider = RealChatterboxProvider.get_instance()
    
    # Test preview generation
    test_cases = [
        {"voice_name": "olivia", "text": "Hello, I am Olivia. This is my voice preview."},
        {"voice_name": "gabriel", "text": "Greetings, this is Gabriel speaking with confidence."},
        {"voice_name": "thomas", "text": "Good day, this is Thomas with a narrative voice."}
    ]
    
    # Create temp directory for previews
    temp_dir = tempfile.mkdtemp()
    print(f"💾 Preview files will be saved to: {temp_dir}")
    
    for i, case in enumerate(test_cases, 1):
        voice_name = case["voice_name"]
        text = case["text"]
        
        print(f"\n🎤 Test {i}: {voice_name}")
        print(f"   📝 Text: '{text}'")
        
        # Generate preview
        save_path = os.path.join(temp_dir, f"preview_{voice_name}.wav")
        
        result = provider.generate_voice(
            text=text,
            save_path=save_path,
            voice_name=voice_name,
            emotion_exaggeration=1.35,
            speed=1.0,
            cfg_weight=0.5
        )
        
        if result.get('success'):
            file_size = os.path.getsize(result['path']) if os.path.exists(result['path']) else 0
            print(f"   ✅ Success! Generated: {result['path']}")
            print(f"   📊 Voice: {result.get('voice_name', 'Unknown')} ({result.get('voice_gender', 'Unknown')})")
            print(f"   🔄 Voice cloned: {'Yes' if result.get('voice_cloned') else 'No'}")
            print(f"   📏 File size: {file_size} bytes")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n🎯 Voice preview test completed!")
    print(f"💡 Check the generated files in: {temp_dir}")

if __name__ == "__main__":
    test_voice_preview() 