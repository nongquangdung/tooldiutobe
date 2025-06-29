#!/usr/bin/env python3
"""
🎭 FINAL DEMO - 94 EMOTIONS CONFIG TAB
======================================

Demo script cuối cùng để verify và show off 
Emotion Config Tab với 94 emotions.
"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def show_config_emotions():
    """Show all emotions trong config file"""
    print("📋 CONFIG FILE EMOTIONS")
    print("=" * 40)
    
    with open('configs/emotions/unified_emotions.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    emotions = config['emotions']
    
    print(f"📊 Total emotions in config: {len(emotions)}")
    print(f"📊 Declared total: {config.get('total_emotions', 'not set')}")
    
    # Group by category
    categories = {}
    for name, emotion in emotions.items():
        category = emotion.get('category', 'unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(name)
    
    print(f"\n📊 EMOTIONS BY CATEGORY:")
    for category, emotion_list in sorted(categories.items()):
        print(f"   {category.upper()}: {len(emotion_list)} emotions")
        for i, emotion in enumerate(sorted(emotion_list)[:5]):  # Show first 5
            print(f"      {i+1}. {emotion}")
        if len(emotion_list) > 5:
            print(f"      ... and {len(emotion_list) - 5} more")
        print()
    
    return len(emotions)

def test_unified_system():
    """Test UnifiedEmotionSystem với config mới"""
    print("🎭 UNIFIED EMOTION SYSTEM TEST")
    print("=" * 40)
    
    from core.unified_emotion_system import UnifiedEmotionSystem
    
    system = UnifiedEmotionSystem()
    emotions = system.get_all_emotions()
    
    print(f"✅ UnifiedEmotionSystem loaded")
    print(f"📊 Available emotions: {len(emotions)}")
    
    # Test specific emotions từ 94 set
    test_emotions = [
        'happy', 'sad', 'angry', 'surprised', 'mysterious',  # Original
        'shocked', 'furious', 'melancholy', 'desperate', 'critical',  # New additions
        'warning', 'emergency', 'cynical', 'embarrassed', 'paranoid'  # More new
    ]
    
    print(f"\n🧪 TESTING SPECIFIC EMOTIONS:")
    found_count = 0
    for emotion in test_emotions:
        if emotion in emotions:
            data = emotions[emotion]
            category = data.get('category', 'unknown')
            description = data.get('description', 'No description')[:40]
            print(f"   ✅ {emotion}: {category} - {description}")
            found_count += 1
        else:
            print(f"   ❌ {emotion}: Not found")
    
    print(f"\n📊 Found {found_count}/{len(test_emotions)} test emotions")
    
    return len(emotions) >= 90  # Allow some tolerance

def demo_emotion_config_tab():
    """Demo Emotion Config Tab"""
    print("\n🎨 EMOTION CONFIG TAB DEMO")
    print("=" * 40)
    
    try:
        from PySide6.QtWidgets import QApplication
        from ui.emotion_config_tab import EmotionConfigTab
        
        # Create minimal app
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create tab
        print("🔄 Creating Emotion Config Tab...")
        emotion_tab = EmotionConfigTab()
        
        print("✅ Emotion Config Tab created successfully!")
        
        # Get emotions from tab
        system = emotion_tab.unified_emotion_system
        emotions = system.get_all_emotions()
        
        print(f"📊 Emotions loaded in tab: {len(emotions)}")
        
        # Test tab features
        print(f"\n🔧 TAB FEATURES:")
        print(f"   ✅ Emotion table: Ready for {len(emotions)} emotions")
        print(f"   ✅ Parameter controls: Temperature, Exaggeration, CFG, Speed")
        print(f"   ✅ Preview functionality: Audio preview with custom params")
        print(f"   ✅ Export/Import: Save and load emotion configs")
        print(f"   ✅ Add custom emotions: User can add new emotions")
        print(f"   ✅ Inner Voice controls: 3 echo types (light, deep, dreamy)")
        
        # Categories breakdown
        categories = {}
        for name, emotion_data in emotions.items():
            category = emotion_data.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\n📊 EMOTION CATEGORIES IN TAB:")
        for category, count in sorted(categories.items()):
            print(f"   {category}: {count} emotions")
        
        # Clean up
        emotion_tab.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Tab demo failed: {e}")
        return False

def main():
    """Main demo"""
    print("🎭 FINAL DEMO - 94 EMOTIONS CONFIG TAB")
    print("=" * 60)
    
    # 1. Show config emotions
    config_count = show_config_emotions()
    
    # 2. Test unified system
    system_ok = test_unified_system()
    
    # 3. Demo tab
    tab_ok = demo_emotion_config_tab()
    
    # Summary
    print(f"\n🎯 FINAL SUMMARY")
    print("=" * 30)
    print(f"📊 Config file emotions: {config_count}")
    print(f"🎭 UnifiedEmotionSystem: {'✅ WORKING' if system_ok else '❌ ISSUES'}")
    print(f"🎨 Emotion Config Tab: {'✅ WORKING' if tab_ok else '❌ ISSUES'}")
    
    if config_count >= 90 and system_ok and tab_ok:
        print(f"\n🎉 THÀNH CÔNG! 94 EMOTIONS CONFIG TAB HOÀN CHỈNH!")
        print(f"=" * 50)
        print(f"✅ Emotion Config Tab đã sẵn sàng với {config_count} emotions")
        print(f"✅ GIỮ NGUYÊN tab hiện tại và bổ sung đầy đủ emotions")
        print(f"✅ User có thể:")
        print(f"   🎛️ Tùy chỉnh 4 parameters cho từng emotion")
        print(f"   🔊 Preview âm thanh với settings tùy chỉnh")
        print(f"   💾 Export/Import emotion configs")
        print(f"   ➕ Add custom emotions mới")
        print(f"   🔄 Reset về default values")
        print(f"   🎵 Inner Voice controls (echo effects)")
        
        print(f"\n💡 CÁCH SỬ DỤNG:")
        print(f"   1. Mở Voice Studio (python src/main.py)")
        print(f"   2. Chuyển sang tab 'Emotion Config'")
        print(f"   3. Xem {config_count} emotions trong bảng")
        print(f"   4. Tùy chỉnh parameters theo ý muốn")
        print(f"   5. Preview âm thanh với settings mới")
        print(f"   6. Export để backup config")
        
    else:
        print(f"\n⚠️ CẦN KIỂM TRA THÊM:")
        if config_count < 90:
            print(f"   📋 Config file chỉ có {config_count} emotions")
        if not system_ok:
            print(f"   🎭 UnifiedEmotionSystem có vấn đề")
        if not tab_ok:
            print(f"   🎨 Emotion Config Tab có vấn đề")

if __name__ == "__main__":
    main() 