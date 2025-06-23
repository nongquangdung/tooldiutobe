#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, 'src')

from src.tts.real_chatterbox_provider import RealChatterboxProvider

def test_voice_resolution():
    print("🧪 Testing voice file resolution...")
    
    # Get provider instance
    provider = RealChatterboxProvider.get_instance()
    
    # Test voices to resolve
    test_voices = ['olivia', 'gabriel', 'thomas', 'abigail']
    
    for voice_name in test_voices:
        print(f"\n🔍 Testing voice: {voice_name}")
        
        # Resolve voice
        voice = provider._resolve_voice_selection(voice_name)
        print(f"   Voice resolved: {voice['name']} ({voice['id']})")
        
        # Check if file path exists
        if 'file_path' in voice:
            if os.path.exists(voice['file_path']):
                print(f"   ✅ Voice file exists: {voice['file_path']}")
            else:
                print(f"   ❌ Voice file not found: {voice['file_path']}")
        else:
            print(f"   ❌ No file_path set in voice object")

if __name__ == "__main__":
    test_voice_resolution() 