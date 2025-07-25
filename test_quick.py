"""
Quick test cho Modern Voice Studio UI
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication, QMainWindow
from src.ui.modern_voice_studio_tab import ModernVoiceStudioTab

class QuickTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Studio - Quick Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Trực tiếp add modern Voice Studio tab
        voice_studio_tab = ModernVoiceStudioTab()
        self.setCentralWidget(voice_studio_tab)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QuickTestWindow()
    window.show()
    
    print("UI đã khởi động. Nhấn Ctrl+C để thoát.")
    sys.exit(app.exec())