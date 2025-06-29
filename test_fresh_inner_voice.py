#!/usr/bin/env python3
"""
Fresh test cho Inner Voice Preview - No import cache
"""

import sys
import os

# Clear any existing module cache
modules_to_clear = [key for key in sys.modules.keys() if 'emotion_config_tab' in key or 'ui' in key]
for module in modules_to_clear:
    del sys.modules[module]
    print(f"🗑️ Cleared module: {module}")

sys.path.insert(0, 'src')

def fresh_test():
    """Fresh test inner voice với no cache"""
    
    print("🎭 FRESH Inner Voice Preview Test...")
    
    # Test constants first
    from tts.voice_generator import INNER_VOICE_AVAILABLE
    print(f"🎭 INNER_VOICE_AVAILABLE: {INNER_VOICE_AVAILABLE}")
    
    from ui.emotion_config_tab import PREVIEW_AVAILABLE
    print(f"🎵 PREVIEW_AVAILABLE: {PREVIEW_AVAILABLE}")
    
    from ui.emotion_config_tab import InnerVoicePreviewThread
    
    # Test parameters
    params = {
        'delay': 1900.0,
        'decay': 0.8,
        'gain': 0.6,
        'filter': 'volume=0.8,aecho=0.6:0.8:1900.0:0.8,lowpass=f=3000'
    }
    
    print(f"🔧 Constants check passed!")
    print(f"🔧 Parameters: {params}")
    
    # Create and run thread
    print("🚀 Creating fresh thread...")
    thread = InnerVoicePreviewThread("dreamy", params)
    
    print("🎭 Running thread directly...")
    thread.run()
    
    print("✅ Fresh test completed!")

if __name__ == "__main__":
    fresh_test() 