#!/usr/bin/env python3
"""
Test script cho Emotion Configuration UI
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ui.emotion_config_tab import EmotionConfigTab

def test_emotion_ui():
    """Test emotion configuration UI"""
    app = QApplication(sys.argv)
    
    # Create emotion config tab
    emotion_tab = EmotionConfigTab()
    emotion_tab.show()
    emotion_tab.setWindowTitle("🎭 Test Emotion Configuration")
    emotion_tab.resize(1000, 700)
    
    print("✅ Emotion Configuration UI loaded successfully!")
    
    # Get all emotions
    all_emotions = emotion_tab.emotion_manager.get_all_emotions()
    print(f"📊 Loaded {len(all_emotions)} emotions")
    
    # Print emotion names by category
    categories = {}
    for emotion_name, emotion in all_emotions.items():
        category = emotion.category
        if category not in categories:
            categories[category] = []
        categories[category].append(emotion_name)
    
    for category, emotion_names in categories.items():
        print(f"\n🏷️ {category.upper()}: {len(emotion_names)} emotions")
        for emotion_name in emotion_names:
            print(f"  - {emotion_name}")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_emotion_ui() 