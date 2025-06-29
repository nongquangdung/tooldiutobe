#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
from ui.emotion_config_tab import InnerVoicePreviewThread

class DebugReceiver(QObject):
    @pyqtSlot(str, str, bool)
    def on_completed(self, inner_voice_type, audio_path, success):
        print(f"🎯 SIGNAL RECEIVED: type={inner_voice_type}, path={audio_path}, success={success}")
        
    @pyqtSlot(str, str)  
    def on_error(self, inner_voice_type, error):
        print(f"🚨 ERROR SIGNAL: type={inner_voice_type}, error={error}")

app = QApplication([])
receiver = DebugReceiver()

print("🔧 Testing thread signals...")

parameters = {
    'delay': 400.0, 
    'decay': 0.3, 
    'gain': 0.5, 
    'filter': 'aecho=0.5:0.3:400.0:0.3'
}

thread = InnerVoicePreviewThread('light', parameters)
thread.preview_completed.connect(receiver.on_completed)
thread.preview_error.connect(receiver.on_error)

print("⚡ Starting thread with signal receivers...")
thread.start()
thread.wait()  # Wait for completion

print("✅ Thread signals test completed!")
app.quit() 