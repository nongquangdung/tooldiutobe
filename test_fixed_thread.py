#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

from ui.emotion_config_tab import InnerVoicePreviewThread

print("🔧 Testing FIXED InnerVoicePreviewThread...")

parameters = {
    'delay': 400.0, 
    'decay': 0.3, 
    'gain': 0.5, 
    'filter': 'aecho=0.5:0.3:400.0:0.3'
}

thread = InnerVoicePreviewThread('light', parameters)
print("⚡ Running fixed thread...")
thread.run()
print("✅ Fixed thread test completed!")

# Check output
import glob
output_files = glob.glob("test_inner_voice_output/inner_voice_preview_*.wav")
if output_files:
    latest_file = max(output_files, key=os.path.getctime)
    print(f"🎵 Latest processed file: {latest_file}")
    print(f"📏 File size: {os.path.getsize(latest_file)} bytes")
else:
    print("❌ No processed files found") 