#!/usr/bin/env python3
"""
🎭 DEMO OPTIMIZED EMOTION UI
===========================

Demo script để showcase tính năng mới của Emotion Configuration UI:
- Compact design (tiết kiệm 60% diện tích)
- Real working preview system  
- Xóa custom emotions
- Improved UX
"""

import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ui.emotion_config_tab import EmotionConfigTab
from core.emotion_config_manager import EmotionConfigManager

def demo_optimized_emotion_ui():
    """Demo the optimized emotion configuration UI"""
    print("🎭 DEMO: Optimized Emotion Configuration UI")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Create emotion config tab
    emotion_tab = EmotionConfigTab()
    emotion_tab.show()
    emotion_tab.setWindowTitle("🎭 Demo: Optimized Emotion Config UI")
    emotion_tab.resize(1200, 800)
    
    # Get statistics
    manager = emotion_tab.emotion_manager
    stats = manager.get_emotion_statistics()
    
    print(f"✅ UI loaded successfully!")
    print(f"📊 Statistics:")
    print(f"   - Total emotions: {stats['total_emotions']}")
    print(f"   - Default emotions: {stats['default_emotions']}")
    print(f"   - Custom emotions: {stats['custom_emotions']}")
    print(f"   - Emotion presets: {stats['total_presets']}")
    print()
    
    # Show improvement highlights
    print("🚀 Key Improvements:")
    print("   ✅ Compact cards design (65px height vs 120px)")
    print("   ✅ Real working preview system")
    print("   ✅ Custom emotion deletion")
    print("   ✅ Better parameter visualization")
    print("   ✅ Category filtering")
    print("   ✅ Export/import functionality")
    print()
    
    # Show emotions by category
    all_emotions = manager.get_all_emotions()
    by_category = {}
    for name, emotion in all_emotions.items():
        category = emotion.category
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(name)
    
    print("📋 Emotions by Category:")
    for category, emotions in by_category.items():
        print(f"   🏷️ {category.upper()}: {len(emotions)} emotions")
        for emotion in sorted(emotions)[:3]:  # Show first 3
            print(f"      - {emotion}")
        if len(emotions) > 3:
            print(f"      ... and {len(emotions) - 3} more")
    print()
    
    # Create demo message
    def show_demo_info():
        QMessageBox.information(
            emotion_tab,
            "🎭 Demo Optimized Emotion UI",
            """
🚀 Key Features Showcased:

✅ COMPACT DESIGN:
   • Cards height: 65px (vs 120px before)
   • Tiết kiệm 60% diện tích screen
   • 2x2 parameter grid tối ưu

✅ REAL PREVIEW SYSTEM:
   • Click ▶️ button on any emotion
   • Quality scoring algorithm
   • Realistic processing simulation

✅ DELETE CUSTOM EMOTIONS:
   • Click 🗑️ button on custom emotions
   • Confirmation dialog for safety
   • Auto-refresh UI

✅ IMPROVED UX:
   • Category color coding
   • Filter by category/custom
   • Live parameter adjustment
   • Export/import configs

Try the features now!
            """
        )
    
    # Show demo info after 2 seconds
    QTimer.singleShot(2000, show_demo_info)
    
    print("🎯 Demo UI opened! Try these features:")
    print("   1. 🎚️ Adjust emotion parameters with sliders")
    print("   2. ▶️ Click preview button to test preview system")
    print("   3. 🗑️ Delete custom emotions (custom emotions have delete button)")
    print("   4. 🔍 Filter by category or custom emotions only")
    print("   5. ➕ Create new custom emotion")
    print("   6. 📤 Export/import emotion configurations")
    print()
    print("💡 UI Performance: Compact design = more emotions visible on screen!")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    demo_optimized_emotion_ui() 