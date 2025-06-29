#!/usr/bin/env python3
"""
🔄 FORCE VOICE FIX RESTART
==========================

Script để force restart và clear cache cho voice fix
"""

import sys
import os
import gc
sys.path.append('src')

def force_restart_voice_system():
    """Force restart voice system và clear cache"""
    print("🔄 FORCING VOICE SYSTEM RESTART")
    print("=" * 50)
    
    # 1. Clear tất cả imports liên quan đến voice
    voice_modules = [mod for mod in sys.modules.keys() if 'voice' in mod.lower() or 'chatterbox' in mod.lower() or 'tts' in mod.lower()]
    
    print(f"🗑️ Clearing {len(voice_modules)} voice-related modules:")
    for module in voice_modules:
        if module in sys.modules:
            print(f"   - {module}")
            del sys.modules[module]
    
    # 2. Force garbage collection
    gc.collect()
    print("🧹 Garbage collection completed")
    
    # 3. Re-import với fresh state
    print("\n🔄 Re-importing with fresh state...")
    
    try:
        from src.tts.real_chatterbox_provider import RealChatterboxProvider
        
        # Force clear singleton
        if hasattr(RealChatterboxProvider, '_instance'):
            RealChatterboxProvider._instance = None
            print("✅ Singleton instance cleared")
        
        # Create new instance
        provider = RealChatterboxProvider()
        print("✅ Fresh RealChatterboxProvider created")
        
        # Test voice resolution nhanh
        test_result = provider._resolve_voice_selection("austin")
        if test_result['name'] == 'Austin' and 'file_path' in test_result:
            print(f"✅ Voice fix confirmed: austin → {test_result['name']} ({test_result['file_path']})")
            return True
        else:
            print(f"❌ Voice fix failed: {test_result}")
            return False
            
    except Exception as e:
        print(f"❌ Error during restart: {e}")
        return False

def generate_test_audio():
    """Generate test audio để verify fix"""
    print(f"\n🎧 GENERATING TEST AUDIO")
    print("-" * 30)
    
    try:
        from src.tts.real_chatterbox_provider import RealChatterboxProvider
        provider = RealChatterboxProvider()
        
        test_voices = ["austin", "connor", "jordan"]
        
        for voice in test_voices:
            print(f"\n🎤 Testing voice: {voice}")
            
            result = provider.generate_voice(
                text=f"Hello, this is {voice} speaking. Voice selection test.",
                save_path=f"test_voice_fix_{voice}.mp3",
                voice_name=voice,
                emotion_exaggeration=1.0,
                speed=1.0,
                cfg_weight=0.6
            )
            
            if result.get('success'):
                voice_used = result.get('voice_name', 'Unknown')
                print(f"✅ Generated audio for {voice} → using voice: {voice_used}")
            else:
                print(f"❌ Failed to generate audio for {voice}")
                
    except Exception as e:
        print(f"❌ Error generating test audio: {e}")

if __name__ == "__main__":
    # Step 1: Force restart
    restart_success = force_restart_voice_system()
    
    if restart_success:
        print(f"\n✅ Voice system restart successful!")
        print(f"💡 User có thể test lại bây giờ với voices sẽ hoạt động đúng")
        
        # Step 2: Generate test audio
        generate_test_audio()
        
        print(f"\n🎯 SOLUTION FOR USER:")
        print(f"=" * 50)
        print(f"1. ✅ Voice fix đã được applied")
        print(f"2. 🔄 Restart lại main application để clear Singleton cache")
        print(f"3. 🎭 Hoặc chạy script này trước khi sử dụng voice")
        print(f"4. 🎧 Test voices: austin, connor, jordan sẽ ra voices khác nhau")
        
    else:
        print(f"\n❌ Voice system restart failed!")
        print(f"💡 User có thể cần restart lại main application manually") 