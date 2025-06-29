#!/usr/bin/env python3
"""
🐛 DEBUG VOICE MATCHING ISSUE
=============================

Script to debug why all voices fallback to Abigail instead of using correct voice
"""

import sys
import os
sys.path.append('src')

from src.tts.real_chatterbox_provider import RealChatterboxProvider
from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager

def debug_voice_matching():
    """Debug voice matching logic"""
    print("🐛 DEBUGGING VOICE MATCHING ISSUE")
    print("=" * 50)
    
    # Test voices from log
    test_voices = ["austin", "connor", "jordan"]
    
    print("\n1. 🎙️ ChatterboxVoicesManager Test:")
    print("-" * 30)
    try:
        voices_manager = ChatterboxVoicesManager()
        chatterbox_voices = voices_manager.get_available_voices()
        
        print(f"Total voices loaded: {len(chatterbox_voices)}")
        print("\nFirst 10 voices:")
        for i, (voice_id, voice_data) in enumerate(list(chatterbox_voices.items())[:10]):
            print(f"  [{i+1}] ID: '{voice_id}' | Name: '{voice_data.name}' | Gender: {voice_data.gender}")
            
        print(f"\nLooking for test voices: {test_voices}")
        for test_voice in test_voices:
            if test_voice in chatterbox_voices:
                voice_data = chatterbox_voices[test_voice]
                print(f"  ✅ '{test_voice}' found: {voice_data.name} ({voice_data.gender})")
            else:
                print(f"  ❌ '{test_voice}' NOT found")
                
    except Exception as e:
        print(f"❌ Error with ChatterboxVoicesManager: {e}")
    
    print("\n2. 🤖 RealChatterboxProvider Test:")
    print("-" * 30)
    try:
        provider = RealChatterboxProvider.get_instance()
        available_voices = provider.get_available_voices()
        
        print(f"Total available voices: {len(available_voices)}")
        print("\nFirst 10 available voices:")
        for i, voice in enumerate(available_voices[:10]):
            print(f"  [{i+1}] ID: '{voice['id']}' | Name: '{voice['name']}' | Gender: {voice['gender']}")
            
        print(f"\nTesting voice resolution for: {test_voices}")
        for test_voice in test_voices:
            print(f"\n🔍 Testing voice: '{test_voice}'")
            resolved_voice = provider._resolve_voice_selection(test_voice)
            print(f"  Result: ID='{resolved_voice['id']}' | Name='{resolved_voice['name']}' | Gender={resolved_voice['gender']}")
            if 'file_path' in resolved_voice:
                print(f"  File: {resolved_voice['file_path']}")
            else:
                print(f"  File: NOT FOUND")
                
    except Exception as e:
        print(f"❌ Error with RealChatterboxProvider: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n3. 📁 Voice Files Check:")
    print("-" * 30)
    try:
        voices_dir = "voices"
        if os.path.exists(voices_dir):
            voice_files = [f for f in os.listdir(voices_dir) if f.endswith('.wav')]
            print(f"Voice files found ({len(voice_files)}):")
            for i, file in enumerate(voice_files[:10]):
                file_stem = file.replace('.wav', '').lower()
                print(f"  [{i+1}] {file} → stem: '{file_stem}'")
                
            print(f"\nChecking test voices in files:")
            for test_voice in test_voices:
                matching_files = [f for f in voice_files if test_voice.lower() in f.lower()]
                if matching_files:
                    print(f"  ✅ '{test_voice}' matches: {matching_files}")
                else:
                    print(f"  ❌ '{test_voice}' no matches found")
        else:
            print(f"❌ Voices directory not found: {voices_dir}")
            
    except Exception as e:
        print(f"❌ Error checking voice files: {e}")

if __name__ == "__main__":
    debug_voice_matching() 