#!/usr/bin/env python3
"""
🎭 DEMO TABLE FORMAT EMOTION CONFIG UI
=====================================

Demo UI emotion configuration với format bảng giống character settings.

Hiển thị:
- Table format dễ nhìn và chỉnh sửa
- Preview âm thanh thật 
- Thêm/xóa custom emotions
- Tùy chỉnh parameters trực tiếp trong bảng
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ui.emotion_config_tab import EmotionConfigTab

class DemoWindow(QMainWindow):
    """Window demo cho table emotion config"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎭 Voice Studio - Demo Table Emotion Config")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Add emotion config tab
        emotion_tab = EmotionConfigTab()
        tab_widget.addTab(emotion_tab, "🎭 Emotion Configuration")
        
        self.setCentralWidget(tab_widget)
        
        # Style the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007AFF;
            }
        """)

def main():
    """Run demo"""
    print("🎭 Starting Table Format Emotion Config Demo...")
    
    app = QApplication(sys.argv)
    
    # Create and show demo window
    window = DemoWindow()
    window.show()
    
    print("✅ Demo UI loaded successfully!")
    print("📝 Features:")
    print("   - Table format giống character settings")
    print("   - Preview âm thanh thật (có TTS) hoặc simulation")
    print("   - Thêm/xóa custom emotions")
    print("   - Tùy chỉnh parameters trực tiếp")
    print("   - Filter theo category")
    print("   - Export/import configs")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 