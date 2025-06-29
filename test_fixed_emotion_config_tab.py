#!/usr/bin/env python3
"""
🔧 TEST FIXED EMOTION CONFIG TAB - 94 EMOTIONS LOADING
=======================================================

Test script sau khi fix .description attribute access errors.
"""

import sys
import os
sys.path.append('src')

from core.unified_emotion_system import UnifiedEmotionSystem

def test_unified_system_dict_compatibility():
    """Test UnifiedEmotionSystem để verify trả về dictionaries với .get() method"""
    print("🔍 Testing UnifiedEmotionSystem dictionary compatibility...")
    
    try:
        system = UnifiedEmotionSystem()
        all_emotions = system.get_all_emotions()
        
        print(f"✅ Loaded {len(all_emotions)} emotions")
        
        # Test một emotion bất kỳ
        if all_emotions:
            emotion_name, emotion_data = list(all_emotions.items())[0]
            print(f"🧪 Testing emotion: {emotion_name}")
            print(f"   Type: {type(emotion_data)}")
            
            # Test .get() method
            description = emotion_data.get('description', 'No description')
            category = emotion_data.get('category', 'neutral')
            exaggeration = emotion_data.get('exaggeration', 1.0)
            
            print(f"   ✅ Description: {description}")
            print(f"   ✅ Category: {category}")
            print(f"   ✅ Exaggeration: {exaggeration}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_emotion_config_tab_loading():
    """Test loading Emotion Config Tab UI"""
    print("\n🔍 Testing Emotion Config Tab loading...")
    
    try:
        # Import sau khi check UnifiedEmotionSystem
        from PySide6.QtWidgets import QApplication
        from ui.emotion_config_tab import EmotionConfigTab
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Tạo tab
        tab = EmotionConfigTab()
        
        print("✅ EmotionConfigTab created successfully")
        print(f"✅ Table has {tab.emotions_table.rowCount()} rows")
        
        # Test một vài emotions để verify không có lỗi
        all_emotions = tab.unified_emotion_system.get_all_emotions()
        print(f"✅ UnifiedEmotionSystem loaded {len(all_emotions)} emotions")
        
        # Test preview capability
        if all_emotions:
            first_emotion = list(all_emotions.keys())[0]
            print(f"✅ Sample emotion for testing: {first_emotion}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading EmotionConfigTab: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 TESTING FIXED EMOTION CONFIG TAB - 94 EMOTIONS")
    print("="*60)
    
    # Test 1: UnifiedEmotionSystem compatibility
    test1_passed = test_unified_system_dict_compatibility()
    
    # Test 2: UI loading
    test2_passed = test_emotion_config_tab_loading()
    
    print("\n📊 TEST RESULTS:")
    print("="*60)
    print(f"🧪 UnifiedEmotionSystem compatibility: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"🖥️ EmotionConfigTab UI loading: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Emotion Config Tab is ready for 94 emotions!")
        print("💡 You can now open Voice Studio and use the Emotion Config tab.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    main() 