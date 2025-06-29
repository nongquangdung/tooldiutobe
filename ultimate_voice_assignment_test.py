#!/usr/bin/env python3
"""
🧪 ULTIMATE VOICE ASSIGNMENT TEST
===============================

Test toàn diện voice assignment sau khi fix fallback issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_voice_assignment_flow():
    """Test complete voice assignment flow"""
    print("🧪 ULTIMATE VOICE ASSIGNMENT TEST")
    print("=" * 60)
    
    # Test 1: ChatterboxVoicesManager
    print("\n1. 🎙️ Testing ChatterboxVoicesManager...")
    try:
        from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
        
        manager = ChatterboxVoicesManager()
        voices = manager.get_available_voices()
        
        print(f"   ✅ Loaded {len(voices)} voices")
        
        # Test specific voices from log
        test_voices = ['austin', 'elena', 'jeremiah', 'cora', 'eli']
        for voice_id in test_voices:
            if voice_id in voices:
                voice = voices[voice_id]
                print(f"   ✅ {voice_id} → {voice.name} ({voice.gender})")
            else:
                print(f"   ❌ {voice_id} NOT FOUND")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: RealChatterboxProvider integration  
    print("\n2. 🤖 Testing RealChatterboxProvider...")
    try:
        from src.tts.real_chatterbox_provider import RealChatterboxProvider
        
        provider = RealChatterboxProvider()
        available_voices = provider.get_available_voices()
        
        print(f"   ✅ Provider loaded {len(available_voices)} voices")
        
        # Test voice resolution
        test_voices = ['austin', 'elena', 'jeremiah', 'cora', 'eli']
        for voice_name in test_voices:
            resolved = provider._resolve_voice_selection(voice_name)
            print(f"   🎯 {voice_name} → {resolved['name']} (ID: {resolved['id']})")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Voice files existence
    print("\n3. 📁 Testing Voice Files...")
    voices_dir = Path("voices")
    if voices_dir.exists():
        voice_files = list(voices_dir.glob("*.wav"))
        print(f"   ✅ Found {len(voice_files)} voice files")
        
        # Check specific voices
        test_voices = ['austin', 'elena', 'jeremiah', 'cora', 'eli']
        for voice_name in test_voices:
            # Try different case variations
            file_variations = [
                f"{voice_name}.wav",
                f"{voice_name.capitalize()}.wav",
                f"{voice_name.upper()}.wav"
            ]
            
            found = False
            for file_var in file_variations:
                file_path = voices_dir / file_var
                if file_path.exists():
                    print(f"   ✅ {voice_name} → {file_var}")
                    found = True
                    break
            
            if not found:
                print(f"   ❌ {voice_name} file NOT FOUND")
    else:
        print(f"   ❌ Voices directory not found: {voices_dir}")
    
    print("\n" + "=" * 60)
    print("🎯 Test completed! Check results above.")

if __name__ == "__main__":
    test_voice_assignment_flow()
