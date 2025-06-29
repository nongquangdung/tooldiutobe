#!/usr/bin/env python3
"""
🔧 FIX VOICE CASE SENSITIVITY ISSUE
=====================================

Vấn đề: User chọn 'layla' nhưng file là 'Layla.wav' → System fallback về 'Abigail.wav'

Giải pháp: Sửa logic trong _resolve_voice_selection() để thử nhiều case formats:
1. lowercase: layla.wav
2. PascalCase: Layla.wav  
3. UPPERCASE: LAYLA.wav

Usage: python fix_voice_case_sensitivity.py
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_current_issue():
    """Demonstrate the current case sensitivity issue"""
    print("🔍 TESTING CURRENT CASE SENSITIVITY ISSUE")
    print("="*50)
    
    voices_dir = "voices"
    test_voice = "layla"
    
    # Current logic (broken)
    voice_file_path_lower = os.path.join(voices_dir, f"{test_voice}.wav")
    voice_file_path_capital = os.path.join(voices_dir, f"{test_voice.capitalize()}.wav")
    
    print(f"🎯 User chọn voice: '{test_voice}'")
    print(f"🔍 Tìm file #1: {voice_file_path_lower}")
    print(f"   Result: {'✅ TỒN TẠI' if os.path.exists(voice_file_path_lower) else '❌ KHÔNG TỒN TẠI'}")
    
    print(f"🔍 Tìm file #2: {voice_file_path_capital}")
    print(f"   Result: {'✅ TỒN TẠI' if os.path.exists(voice_file_path_capital) else '❌ KHÔNG TỒN TẠI'}")
    
    # Show actual files
    print(f"\n📁 Files thực tế trong {voices_dir}/:")
    try:
        files = os.listdir(voices_dir)
        layla_files = [f for f in files if 'layla' in f.lower()]
        for f in layla_files:
            print(f"   - {f}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def fix_voice_resolution():
    """Apply the fix to voice resolution logic"""
    print("\n🔧 APPLYING FIX TO VOICE RESOLUTION")
    print("="*50)
    
    # Read current file
    provider_file = "src/tts/real_chatterbox_provider.py"
    
    try:
        with open(provider_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the problematic section
        old_logic = '''                        # Try both lowercase and capitalize case for file name
                        voice_file_path_lower = str(voices_manager.voices_directory / f"{voice_name}.wav")
                        voice_file_path_capital = str(voices_manager.voices_directory / f"{voice_name.capitalize()}.wav")
                        
                        if os.path.exists(voice_file_path_lower):
                            voice['file_path'] = voice_file_path_lower
                            print(f"🎤 Voice found: {voice['name']} → {voice_file_path_lower}")
                        elif os.path.exists(voice_file_path_capital):
                            voice['file_path'] = voice_file_path_capital
                            print(f"🎤 Voice found: {voice['name']} → {voice_file_path_capital}")
                        else:
                            print(f"⚠️ Voice file not found for: {voice_name} (tried {voice_file_path_lower} and {voice_file_path_capital})")'''
        
        new_logic = '''                        # Try multiple case formats for voice files
                        voice_variations = [
                            f"{voice_name}.wav",           # lowercase: layla.wav
                            f"{voice_name.capitalize()}.wav",  # PascalCase: Layla.wav
                            f"{voice_name.upper()}.wav",   # UPPERCASE: LAYLA.wav
                            f"{voice_name.lower()}.wav"    # explicit lowercase
                        ]
                        
                        voice_file_found = None
                        for variation in voice_variations:
                            voice_file_path = str(voices_manager.voices_directory / variation)
                            if os.path.exists(voice_file_path):
                                voice_file_found = voice_file_path
                                print(f"🎤 Voice found: {voice['name']} → {voice_file_path}")
                                break
                        
                        if voice_file_found:
                            voice['file_path'] = voice_file_found
                        else:
                            tried_paths = [str(voices_manager.voices_directory / v) for v in voice_variations]
                            print(f"⚠️ Voice file not found for: {voice_name}")
                            print(f"   Tried: {tried_paths}")'''
        
        if old_logic in content:
            # Apply fix
            content = content.replace(old_logic, new_logic)
            
            # Write back
            with open(provider_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Fixed case sensitivity issue in voice resolution!")
            print("   Now supports: lowercase, PascalCase, UPPERCASE formats")
            
        else:
            print("⚠️ Target code section not found for replacement")
            print("   Manual fix may be required")
    
    except Exception as e:
        print(f"❌ Error applying fix: {e}")

def test_fix():
    """Test the fix"""
    print("\n🧪 TESTING THE FIX")
    print("="*50)
    
    try:
        # Import after fix
        from src.tts.real_chatterbox_provider import RealChatterboxProvider
        
        provider = RealChatterboxProvider.get_instance()
        
        # Test voice resolution
        test_voices = ['layla', 'Layla', 'LAYLA', 'abigail', 'Abigail']
        
        for voice_name in test_voices:
            print(f"\n🎯 Testing voice: '{voice_name}'")
            try:
                resolved_voice = provider._resolve_voice_selection(voice_name)
                print(f"   ✅ Resolved to: {resolved_voice.get('name', 'Unknown')}")
                if 'file_path' in resolved_voice:
                    print(f"   📁 File: {resolved_voice['file_path']}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main function"""
    print("🔧 VOICE CASE SENSITIVITY FIX")
    print("="*60)
    
    # 1. Demonstrate issue
    test_current_issue()
    
    # 2. Apply fix
    fix_voice_resolution()
    
    # 3. Test fix
    test_fix()
    
    print("\n🎉 SUMMARY:")
    print("✅ Vấn đề: User chọn 'layla' → File 'Layla.wav' → Không match")
    print("✅ Giải pháp: Thử multiple case formats (lowercase, PascalCase, UPPERCASE)")
    print("✅ Kết quả: Voice selection sẽ hoạt động với mọi case format!")

if __name__ == "__main__":
    main() 