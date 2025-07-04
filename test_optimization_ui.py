#!/usr/bin/env python3
"""
Test script for TTS Optimization UI
Launch just the optimization tab for development/testing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    
    # Test window
    window = QMainWindow()
    window.setWindowTitle("🚀 TTS Optimization Settings - Test")
    window.setGeometry(100, 100, 1200, 800)
    
    try:
        # Import and create optimization tab
        from src.ui.tabs.tts_optimization_tab import TtsOptimizationTab
        
        # Create central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add optimization tab
        optimization_tab = TtsOptimizationTab()
        layout.addWidget(optimization_tab)
        
        window.setCentralWidget(central_widget)
        
        # Connect signals for testing
        def on_settings_changed(settings):
            print(f"🔧 Settings changed: {settings}")
        
        optimization_tab.optimization_changed.connect(on_settings_changed)
        
        print("✅ TTS Optimization UI loaded successfully!")
        print("🎯 GPU auto-detection and optimization controls are available")
        
    except Exception as e:
        print(f"❌ Error loading TTS Optimization UI: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 