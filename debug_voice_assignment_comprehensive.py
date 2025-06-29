#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE VOICE ASSIGNMENT DEBUG TEST
==========================================

Test to debug exactly where voice assignment fails
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_chatterbox_voices_manager():
    """Test ChatterboxVoicesManager voice loading"""
    print("=" * 60)
    print("🧪 Testing ChatterboxVoicesManager...")
    
    try:
        from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
        
        manager = ChatterboxVoicesManager()
        voices = manager.get_available_voices()
        
        print(f"📋 ChatterboxVoicesManager loaded {len(voices)} voices:")
        
        test_voices = ['jeremiah', 'cora', 'eli', 'abigail']
        for voice_id in test_voices:
            if voice_id in voices:
                voice = voices[voice_id]
                print(f"  ✅ {voice_id} → {voice.name} ({voice.gender})")
                print(f"      📁 Expected file: voices/{voice.name}.wav")
                
                # Check if file exists
                expected_file = manager.voices_directory / f"{voice.name}.wav"
                if expected_file.exists():
                    print(f"      ✅ File exists: {expected_file}")
                else:
                    print(f"      ❌ File NOT found: {expected_file}")
            else:
                print(f"  ❌ {voice_id} NOT FOUND in ChatterboxVoicesManager")
                
    except Exception as e:
        print(f"❌ ChatterboxVoicesManager test failed: {e}")
        import traceback
        traceback.print_exc()

def test_real_chatterbox_provider():
    """Test RealChatterboxProvider voice loading"""
    print("=" * 60)
    print("🧪 Testing RealChatterboxProvider...")
    
    try:
        from src.tts.real_chatterbox_provider import RealChatterboxProvider
        
        provider = RealChatterboxProvider()
        voices = provider.get_available_voices()
        
        print(f"📋 RealChatterboxProvider loaded {len(voices)} voices:")
        
        test_voices = ['jeremiah', 'cora', 'eli', 'abigail']
        for voice_name in test_voices:
            # Test voice resolution
            resolved_voice = provider._resolve_voice_selection(voice_name)
            print(f"  🎯 {voice_name} → {resolved_voice}")
                
    except Exception as e:
        print(f"❌ RealChatterboxProvider test failed: {e}")
        import traceback
        traceback.print_exc()

def test_voice_files_case_sensitivity():
    """Test voice files case sensitivity issues"""
    print("=" * 60)
    print("🧪 Testing Voice Files Case Sensitivity...")
    
    voices_dir = Path("voices")
    if not voices_dir.exists():
        print(f"❌ Voices directory not found: {voices_dir}")
        return
    
    voice_files = list(voices_dir.glob("*.wav"))
    print(f"📁 Found {len(voice_files)} voice files:")
    
    test_voices = ['jeremiah', 'cora', 'eli', 'abigail']
    for voice_name in test_voices:
        print(f"\n🔍 Looking for variations of '{voice_name}':")
        
        variations = [
            voice_name.lower(),           # jeremiah
            voice_name.capitalize(),      # Jeremiah  
            voice_name.upper(),           # JEREMIAH
        ]
        
        for variation in variations:
            test_file = voices_dir / f"{variation}.wav"
            if test_file.exists():
                print(f"  ✅ Found: {test_file}")
            else:
                print(f"  ❌ Not found: {test_file}")

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE VOICE ASSIGNMENT DEBUG TEST")
    print("=" * 60)
    
    test_chatterbox_voices_manager()
    test_real_chatterbox_provider()
    test_voice_files_case_sensitivity()
    
    print("=" * 60)
    print("🧪 Voice assignment debug test completed!")

if __name__ == "__main__":
    from pathlib import Path
    main()
