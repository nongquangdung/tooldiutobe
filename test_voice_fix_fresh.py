#!/usr/bin/env python3
"""
🧪 TEST VOICE FIX WITH FRESH INSTANCE
=====================================

Test voice selection với fresh instance để đảm bảo fix đã hoạt động
"""

import sys
import os
sys.path.append('src')

# Force clear any existing instances
if 'src.tts.real_chatterbox_provider' in sys.modules:
    del sys.modules['src.tts.real_chatterbox_provider']

from src.tts.real_chatterbox_provider import RealChatterboxProvider

def test_voice_fix():
    """Test voice fix với fresh instance"""
    print("🧪 TESTING VOICE FIX WITH FRESH INSTANCE")
    print("=" * 50)
    
    # Force create new instance (bỏ qua Singleton cache)
    try:
        # Clear singleton instance nếu có
        if hasattr(RealChatterboxProvider, '_instance'):
            RealChatterboxProvider._instance = None
            print("🗑️ Cleared existing Singleton instance")
        
        # Tạo instance mới
        provider = RealChatterboxProvider()
        print("✅ Created fresh RealChatterboxProvider instance")
        
        # Test voice resolution
        test_voices = ["austin", "connor", "jordan", "abigail"]
        
        print(f"\n🎯 Testing voice resolution:")
        print("-" * 30)
        
        for voice_name in test_voices:
            print(f"\n🔍 Testing voice: '{voice_name}'")
            resolved = provider._resolve_voice_selection(voice_name)
            
            print(f"  Result: ID='{resolved['id']}' | Name='{resolved['name']}' | Gender={resolved['gender']}")
            if 'file_path' in resolved:
                print(f"  File: {resolved['file_path']}")
                # Check if file exists
                if os.path.exists(resolved['file_path']):
                    print(f"  ✅ File exists")
                else:
                    print(f"  ❌ File NOT found")
            else:
                print(f"  ⚠️ No file_path in result")
                
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voice_fix() 