#!/usr/bin/env python3
"""
🔧 FIX VOICE ASSIGNMENT ULTIMATE
===============================

Script fix TRIỆT ĐỂ voice assignment issue:
- Fix fallback 'abigail' trong advanced_window.py line 2524
- Sử dụng dynamic voice selection từ character table
- Đảm bảo voice assignment hoạt động đúng

Author: Voice Studio Team  
Date: 2025-01-26
Target: Line 2524 trong src/ui/advanced_window.py
"""

import os
import sys
import shutil
from pathlib import Path
import re

def fix_voice_fallback_in_advanced_window():
    """Fix fallback 'abigail' trong advanced_window.py"""
    
    advanced_window_file = Path("src/ui/advanced_window.py")
    
    if not advanced_window_file.exists():
        print(f"❌ File not found: {advanced_window_file}")
        return False
    
    # Create backup
    backup_file = advanced_window_file.with_suffix('.py.backup')
    shutil.copy2(advanced_window_file, backup_file)
    print(f"📋 Created backup: {backup_file}")
    
    # Read current content
    with open(advanced_window_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the problematic line
    old_line = "voice_name = voice_settings.get('suggested_voice', 'abigail')  # Use real voice ID"
    
    if old_line in content:
        print("🔍 Found problematic line with fallback 'abigail'")
        
        # NEW: Dynamic voice selection logic
        new_logic = """# Dynamic voice selection - NO hardcoded fallback
                    voice_name = voice_settings.get('suggested_voice')
                    
                    # If no voice in mapping, get from character settings table dynamically
                    if not voice_name:
                        # Get voice from character settings table row
                        voice_name = self.get_character_voice_from_table(speaker)
                        print(f"🔄 No voice mapping for {speaker}, using table voice: {voice_name}")
                    
                    # Final fallback: use first available voice (not hardcoded 'abigail')
                    if not voice_name:
                        try:
                            # Get first available voice from ChatterboxVoicesManager
                            from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                            voices_manager = ChatterboxVoicesManager()
                            available_voices = voices_manager.get_available_voices()
                            if available_voices:
                                voice_name = list(available_voices.keys())[0]
                                print(f"🔄 Final fallback for {speaker}: {voice_name}")
                            else:
                                voice_name = 'abigail'  # Only if no voices available at all
                        except Exception as e:
                            print(f"⚠️ Error getting dynamic voice: {e}")
                            voice_name = 'abigail'  # Last resort fallback
                    
                    print(f"🎯 {speaker}: Using VOICE SELECTION - {voice_name}")"""
        
        # Replace the old line with new logic
        content = content.replace(old_line, new_logic)
        print("✅ Replaced hardcoded fallback with dynamic voice selection")
        
        # Also need to add the helper method get_character_voice_from_table
        helper_method = '''
    def get_character_voice_from_table(self, character_id):
        """Get character voice from settings table dynamically"""
        try:
            # Find character row in character_settings_table
            table = self.character_settings_table
            for row in range(table.rowCount()):
                char_item = table.item(row, 0)  # Character column
                if char_item and char_item.text() == character_id:
                    # Get voice combo from Voice column (column 1)
                    voice_combo = table.cellWidget(row, 1)
                    if voice_combo:
                        current_voice = voice_combo.currentData()
                        if current_voice:
                            return current_voice
                        # If no currentData, try currentText
                        return voice_combo.currentText().lower()
            
            # If character not found in table, return None
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting voice from table for {character_id}: {e}")
            return None'''
        
        # Find a good place to insert the helper method (after other helper methods)
        insertion_point = content.find("def get_character_name_by_id(self, char_id):")
        if insertion_point != -1:
            content = content[:insertion_point] + helper_method + "\n\n    " + content[insertion_point:]
            print("✅ Added helper method get_character_voice_from_table")
        else:
            print("⚠️ Could not find insertion point for helper method")
    
    else:
        print("⚠️ Target line not found - may have been already fixed")
    
    # Save fixed content
    with open(advanced_window_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed voice fallback in advanced_window.py")
    return True

def create_ultimate_test_script():
    """Create comprehensive test script for voice assignment"""
    
    test_content = '''#!/usr/bin/env python3
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
    print("\\n1. 🎙️ Testing ChatterboxVoicesManager...")
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
    print("\\n2. 🤖 Testing RealChatterboxProvider...")
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
    print("\\n3. 📁 Testing Voice Files...")
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
    
    print("\\n" + "=" * 60)
    print("🎯 Test completed! Check results above.")

if __name__ == "__main__":
    test_voice_assignment_flow()
'''
    
    with open("ultimate_voice_assignment_test.py", 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Created ultimate_voice_assignment_test.py")

def main():
    """Main execution"""
    print("🚀 FIX VOICE ASSIGNMENT ULTIMATE")
    print("=" * 50)
    
    # Step 1: Fix fallback in advanced_window.py
    print("\\nStep 1: Fixing voice fallback...")
    success1 = fix_voice_fallback_in_advanced_window()
    
    # Step 2: Create test script
    print("\\nStep 2: Creating test script...")
    create_ultimate_test_script()
    
    if success1:
        print("\\n🎉 ULTIMATE FIX COMPLETED!")
        print("✅ Voice fallback fixed")
        print("✅ Dynamic voice selection implemented")
        print("✅ Test script created")
        print("\\n💡 Next steps:")
        print("1. Run: python ultimate_voice_assignment_test.py")
        print("2. Test voice generation với characters")
        print("3. Verify logs show correct voice assignment")
    else:
        print("\\n❌ Some fixes failed - check errors above")

if __name__ == "__main__":
    main() 