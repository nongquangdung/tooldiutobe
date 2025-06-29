#!/usr/bin/env python3
"""
Debug script - test inner voice preview trực tiếp
"""

import sys
import os
import importlib
sys.path.insert(0, 'src')

def test_inner_voice_direct():
    """Test inner voice preview trực tiếp"""
    
    print("🎭 Testing Inner Voice Preview Direct...")
    
    # Force reload module để get latest code
    if 'ui.emotion_config_tab' in sys.modules:
        importlib.reload(sys.modules['ui.emotion_config_tab'])
        print("🔄 Reloaded emotion_config_tab module")
    
    # Mock parameters từ UI
    test_parameters = {
        'delay': 1900.0,
        'decay': 0.8,
        'gain': 0.6,
        'filter': 'volume=0.8,aecho=0.6:0.8:1900.0:0.8,lowpass=f=3000'
    }
    
    print(f"🔧 Test parameters: {test_parameters}")
    
    # Import InnerVoicePreviewThread
    from ui.emotion_config_tab import InnerVoicePreviewThread
    
    # Create thread
    thread = InnerVoicePreviewThread("dreamy", test_parameters)
    
    # Run synchronously
    print("🚀 Starting thread.run()...")
    thread.run()  # Run directly instead of .start()
    
    print("✅ Thread completed!")

if __name__ == "__main__":
    test_inner_voice_direct() 