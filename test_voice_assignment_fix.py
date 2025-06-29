#!/usr/bin/env python3
"""
🧪 VOICE ASSIGNMENT TEST
======================

Test script để verify voice assignment hoạt động đúng
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager

def test_voice_assignment():
    print("🧪 Testing Voice Assignment...")
    
    manager = ChatterboxVoicesManager()
    voices = manager.get_available_voices()
    
    print(f"📋 Available voices: {len(voices)}")
    
    test_voices = ['jeremiah', 'cora', 'eli', 'abigail']
    
    for voice_id in test_voices:
        if voice_id in voices:
            voice = voices[voice_id]
            print(f"  ✅ {voice_id} → {voice.name} ({voice.gender})")
        else:
            print(f"  ❌ {voice_id} NOT FOUND")
    
    print("🧪 Voice assignment test completed!")

if __name__ == "__main__":
    test_voice_assignment()
