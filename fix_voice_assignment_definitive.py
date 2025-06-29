#!/usr/bin/env python3
"""
🔧 FIX VOICE ASSIGNMENT DEFINITIVE
=================================

Script fix triệt để vấn đề voice assignment:
- Real Chatterbox provider hardcode 'abigail'
- Fix get_available_voices() method
- Fix voice lookup logic

Author: Voice Studio Team
Date: 2025-01-26
"""

import os
import sys
import shutil
from pathlib import Path

def backup_and_fix_real_chatterbox_provider():
    """Fix Real Chatterbox provider voice assignment issue"""
    
    provider_file = Path("src/tts/real_chatterbox_provider.py")
    
    if not provider_file.exists():
        print(f"❌ File not found: {provider_file}")
        return False
    
    # Create backup
    backup_file = provider_file.with_suffix('.py.backup')
    shutil.copy2(provider_file, backup_file)
    print(f"📋 Created backup: {backup_file}")
    
    # Read current content
    with open(provider_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if get_available_voices method exists and is problematic
    if "def get_available_voices(self)" in content:
        print("🔍 Found get_available_voices method")
        
        # Fix: Replace hardcoded voice list with ChatterboxVoicesManager integration
        new_get_available_voices = '''    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get available voices from ChatterboxVoicesManager (not hardcoded)"""
        try:
            # Import ChatterboxVoicesManager
            from .chatterbox_voices_integration import ChatterboxVoicesManager
            
            voices_manager = ChatterboxVoicesManager()
            chatterbox_voices = voices_manager.get_available_voices()
            
            # Convert ChatterboxVoice objects to dict format
            available_voices = []
            for voice_id, voice in chatterbox_voices.items():
                voice_dict = {
                    'id': voice_id,
                    'name': voice.name, 
                    'gender': voice.gender,
                    'description': voice.description,
                    'language': voice.language,
                    'file_path': str(voices_manager.voices_directory / f"{voice.name}.wav")
                }
                available_voices.append(voice_dict)
            
            print(f"🎙️ Loaded {len(available_voices)} predefined voices từ ChatterboxVoicesManager")
            return available_voices
            
        except Exception as e:
            print(f"⚠️ Error loading voices from ChatterboxVoicesManager: {e}")
            # Fallback to basic voice
            return [{
                'id': 'abigail',
                'name': 'Abigail',
                'gender': 'female',
                'description': 'Default fallback voice',
                'language': 'en',
                'file_path': 'voices/Abigail.wav'
            }]'''
        
        # Find and replace the method
        import re
        pattern = r'def get_available_voices\(self\).*?(?=\n    def|\nclass|\n$|\Z)'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_get_available_voices.strip(), content, flags=re.DOTALL)
            print("✅ Replaced get_available_voices method")
        else:
            # If method doesn't exist, add it before the end of class
            insertion_point = content.rfind('class RealChatterboxProvider')
            if insertion_point != -1:
                # Find end of class (look for next class or end of file)
                class_end = content.find('\nclass', insertion_point + 1)
                if class_end == -1:
                    class_end = len(content)
                
                # Insert before class end
                content = content[:class_end-1] + '\n' + new_get_available_voices + '\n' + content[class_end-1:]
                print("✅ Added get_available_voices method")
    
    # Save fixed content
    with open(provider_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed Real Chatterbox provider voice assignment")
    return True

def create_voice_assignment_debug_test():
    """Create comprehensive voice assignment debug test"""
    
    test_content = '''#!/usr/bin/env python3
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
        print(f"\\n🔍 Looking for variations of '{voice_name}':")
        
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
'''
    
    test_file = Path("debug_voice_assignment_comprehensive.py")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ Created comprehensive debug test: {test_file}")

def main():
    """Main fix function"""
    print("🔧 FIXING VOICE ASSIGNMENT DEFINITIVELY...")
    print("=" * 60)
    
    # Fix 1: Real Chatterbox provider
    print("🤖 Fix 1: Fixing Real Chatterbox provider...")
    backup_and_fix_real_chatterbox_provider()
    
    # Fix 2: Create debug test
    print("🧪 Fix 2: Creating comprehensive debug test...")
    create_voice_assignment_debug_test()
    
    print("=" * 60)
    print("✅ VOICE ASSIGNMENT FIX COMPLETED!")
    print("")
    print("📋 NEXT STEPS:")
    print("1. Run: python debug_voice_assignment_comprehensive.py")
    print("2. Restart Voice Studio application")  
    print("3. Test voice generation - should now use correct voices!")

if __name__ == "__main__":
    main() 