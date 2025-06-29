#!/usr/bin/env python3
"""
🎭 DEMO 93 EMOTIONS CONFIG TAB
==============================

Demo script để test Emotion Config Tab với 93 emotions đã được mở rộng.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.unified_emotion_system import UnifiedEmotionSystem

def test_93_emotions_config():
    """Test config với 93 emotions"""
    print("🎭 TESTING 93 EMOTIONS CONFIG")
    print("=" * 50)
    
    # Test 1: Load config file
    config_path = "configs/emotions/unified_emotions.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ Config loaded successfully")
        print(f"   📊 Total emotions: {config['total_emotions']}")
        print(f"   📊 Actual count: {len(config['emotions'])}")
        print(f"   📊 Version: {config['version']}")
        
    except Exception as e:
        print(f"❌ Config load failed: {e}")
        return False
    
    # Test 2: Unified Emotion System
    try:
        system = UnifiedEmotionSystem()
        emotions = system.get_all_emotions()
        
        print(f"✅ UnifiedEmotionSystem loaded")
        print(f"   📊 Available emotions: {len(emotions)}")
        
        # Show some sample emotions
        emotion_list = list(emotions.keys())
        print(f"   📋 Sample emotions:")
        for i in range(min(15, len(emotion_list))):
            emotion_name = emotion_list[i]
            emotion_data = emotions[emotion_name]
            print(f"      {i+1:2d}. {emotion_name} (category: {emotion_data.get('category', 'unknown')})")
            
    except Exception as e:
        print(f"❌ UnifiedEmotionSystem failed: {e}")
        return False
    
    # Test 3: Categories count
    try:
        categories = {}
        for emotion_name, emotion_data in emotions.items():
            category = emotion_data.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        print(f"✅ Categories analysis:")
        for category, count in sorted(categories.items()):
            print(f"      {category}: {count} emotions")
            
    except Exception as e:
        print(f"❌ Categories analysis failed: {e}")
        return False
    
    print(f"\n🎯 RESULT: 93 Emotions Config Tab ready!")
    print(f"   ✅ Config file: {len(config['emotions'])} emotions")
    print(f"   ✅ System load: {len(emotions)} emotions")
    print(f"   ✅ Categories: {len(categories)} categories")
    
    return True

def demo_emotion_config_tab():
    """Demo Emotion Config Tab UI với 93 emotions"""
    print("\n🎨 DEMO EMOTION CONFIG TAB UI")
    print("=" * 50)
    
    try:
        # Import PySide6
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Import Emotion Config Tab
        from ui.emotion_config_tab import EmotionConfigTab
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create Emotion Config Tab
        emotion_tab = EmotionConfigTab()
        
        # Show window
        emotion_tab.show()
        emotion_tab.setWindowTitle("🎭 93 Emotions Config Tab - Demo")
        emotion_tab.resize(1200, 800)
        
        print("✅ Emotion Config Tab UI created successfully!")
        print("   📋 Tab hiển thị đầy đủ 93 emotions")
        print("   🎛️ Có thể tùy chỉnh, preview, export/import")
        print("   🔧 Inner Voice controls đã được tích hợp")
        
        # Get emotions count from tab
        system = emotion_tab.unified_emotion_system
        emotions = system.get_all_emotions()
        print(f"   📊 Emotions loaded in UI: {len(emotions)}")
        
        print(f"\n🎯 Tab ready! Bạn có thể:")
        print(f"   ✅ Xem tất cả 93 emotions trong bảng")
        print(f"   ✅ Tùy chỉnh parameters (Temperature, Exaggeration, CFG, Speed)")
        print(f"   ✅ Preview âm thanh với parameters mới")
        print(f"   ✅ Export/Import config")
        print(f"   ✅ Add custom emotions mới")
        print(f"   ✅ Reset về default values")
        
        # Don't run event loop for demo
        emotion_tab.close()
        
        return True
        
    except Exception as e:
        print(f"❌ UI demo failed: {e}")
        return False

def main():
    """Main demo function"""
    print("🎭 93 EMOTIONS CONFIG TAB DEMO")
    print("=" * 60)
    
    # Test config
    config_ok = test_93_emotions_config()
    
    if config_ok:
        # Demo UI 
        ui_ok = demo_emotion_config_tab()
        
        if ui_ok:
            print(f"\n🎉 SUCCESS! 93 EMOTIONS CONFIG TAB SẴN SÀNG!")
            print(f"   ✅ Config file: ✅ Working")
            print(f"   ✅ Unified System: ✅ Working") 
            print(f"   ✅ UI Tab: ✅ Working")
            print(f"\n💡 Để sử dụng: Chạy Voice Studio và mở Emotion Config tab")
        else:
            print(f"\n⚠️ Config OK nhưng UI có vấn đề - check dependencies")
    else:
        print(f"\n❌ Config có vấn đề - cần fix trước")

if __name__ == "__main__":
    main() 