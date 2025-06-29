#!/usr/bin/env python3
"""
Test script để kiểm tra inner voice preview UI components
"""

import sys
import os
sys.path.insert(0, 'src')

def test_inner_voice_preview_ui():
    """Test inner voice preview UI components"""
    
    print("🎛️ TESTING INNER VOICE PREVIEW UI")
    print("=" * 50)
    
    try:
        # Test import InnerVoicePreviewThread
        from ui.emotion_config_tab import InnerVoicePreviewThread
        print("✅ InnerVoicePreviewThread imported successfully")
        
        # Create QApplication first
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication([])
        
        # Test UI components
        from ui.emotion_config_tab import EmotionConfigTab
        tab = EmotionConfigTab()
        print("✅ EmotionConfigTab created")
        
        # Check preview method
        if hasattr(tab, 'preview_inner_voice'):
            print("✅ preview_inner_voice method exists")
        else:
            print("❌ preview_inner_voice method missing")
            return False
        
        # Check widgets
        if hasattr(tab, 'inner_voice_type_widgets'):
            widgets = tab.inner_voice_type_widgets
            print(f"✅ inner_voice_type_widgets: {list(widgets.keys())}")
            
            for voice_type, controls in widgets.items():
                if 'preview' in controls:
                    print(f"   ✅ {voice_type}: has preview button")
                else:
                    print(f"   ❌ {voice_type}: missing preview button")
                    return False
        else:
            print("❌ inner_voice_type_widgets missing")
            return False
        
        # Check signal handlers
        handlers = ['on_inner_voice_preview_completed', 'on_inner_voice_preview_error', 'on_inner_voice_preview_progress']
        for handler in handlers:
            if hasattr(tab, handler):
                print(f"✅ {handler} method exists")
            else:
                print(f"❌ {handler} method missing")
                return False
        
        # Check thread tracking
        if hasattr(tab, 'inner_voice_preview_threads'):
            print("✅ inner_voice_preview_threads tracking exists")
        else:
            print("❌ inner_voice_preview_threads missing")
            return False
        
        print("\n🎉 INNER VOICE PREVIEW UI: ALL COMPONENTS READY!")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_inner_voice_preview_ui()
    print(f"\n{'='*50}")
    if success:
        print("🎉 Inner Voice Preview UI Test: SUCCESS")
        print("💡 Bây giờ bạn có thể bấm nút '🎵 Preview' trong Inner Voice section!")
        print("🎯 Các nút preview sẽ xuất hiện trong:")
        print("   - Inner Voice → Nội tâm nhẹ (light) → 🎵 Preview")
        print("   - Inner Voice → Nội tâm sâu (deep) → 🎵 Preview") 
        print("   - Inner Voice → Nội tâm cách âm (dreamy) → 🎵 Preview")
    else:
        print("💥 Inner Voice Preview UI Test: FAILED")
    print(f"{'='*50}") 