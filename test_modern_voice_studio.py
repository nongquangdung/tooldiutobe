"""
Test Modern Voice Studio Tab
Demo beautiful UI với full functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from src.ui.modern_voice_studio_tab import ModernVoiceStudioTab

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Voice Studio - UI Demo")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add modern Voice Studio tab
        voice_studio_tab = ModernVoiceStudioTab()
        tabs.addTab(voice_studio_tab, "🎤 Modern Voice Studio")
        
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')  # Modern look
    
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())