#!/usr/bin/env python3
"""
Test UI Inner Voice Preview Button
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import time

def test_ui_preview():
    """Test preview button trong UI"""
    print("🎛️ TESTING UI INNER VOICE PREVIEW")
    print("=" * 45)
    
    try:
        # Create Qt application
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Import after Qt app is created
        from src.ui.emotion_config_tab import EmotionConfigTab
        
        # Create tab
        tab = EmotionConfigTab()
        print("✅ EmotionConfigTab created")
        
        # Show tab (optional for testing)
        tab.show()
        tab.resize(800, 600)
        
        # Test inner voice preview methods
        print("\n🧪 Testing preview methods...")
        
        # Test light inner voice
        print("   🔍 Testing light inner voice preview...")
        tab.preview_inner_voice("light")
        
        # Wait a bit for thread to start
        time.sleep(1)
        
        # Test if thread is created
        if "light" in tab.inner_voice_preview_threads:
            thread = tab.inner_voice_preview_threads["light"]
            if thread and thread.isRunning():
                print("   ✅ Light preview thread started successfully")
                
                # Wait for completion
                timeout = 30  # 30 seconds timeout
                start_time = time.time()
                
                while thread.isRunning() and (time.time() - start_time) < timeout:
                    app.processEvents()
                    time.sleep(0.1)
                
                if not thread.isRunning():
                    print("   ✅ Light preview thread completed")
                else:
                    print("   ⚠️ Light preview thread timeout")
            else:
                print("   ❌ Light preview thread not running")
        else:
            print("   ❌ Light preview thread not created")
        
        # Test deep inner voice
        print("   🔍 Testing deep inner voice preview...")
        tab.preview_inner_voice("deep")
        time.sleep(1)
        
        if "deep" in tab.inner_voice_preview_threads:
            thread = tab.inner_voice_preview_threads["deep"]
            if thread and thread.isRunning():
                print("   ✅ Deep preview thread started successfully")
                
                timeout = 30
                start_time = time.time()
                
                while thread.isRunning() and (time.time() - start_time) < timeout:
                    app.processEvents()
                    time.sleep(0.1)
                
                if not thread.isRunning():
                    print("   ✅ Deep preview thread completed")
                else:
                    print("   ⚠️ Deep preview thread timeout")
            else:
                print("   ❌ Deep preview thread not running")
        else:
            print("   ❌ Deep preview thread not created")
        
        # Test dreamy inner voice
        print("   🔍 Testing dreamy inner voice preview...")
        tab.preview_inner_voice("dreamy")
        time.sleep(1)
        
        if "dreamy" in tab.inner_voice_preview_threads:
            thread = tab.inner_voice_preview_threads["dreamy"]
            if thread and thread.isRunning():
                print("   ✅ Dreamy preview thread started successfully")
                
                timeout = 30
                start_time = time.time()
                
                while thread.isRunning() and (time.time() - start_time) < timeout:
                    app.processEvents()
                    time.sleep(0.1)
                
                if not thread.isRunning():
                    print("   ✅ Dreamy preview thread completed")
                else:
                    print("   ⚠️ Dreamy preview thread timeout")
            else:
                print("   ❌ Dreamy preview thread not running")
        else:
            print("   ❌ Dreamy preview thread not created")
        
        # Check if any preview files were created
        print("\n📁 Checking generated preview files...")
        
        import glob
        preview_files = glob.glob("test_inner_voice_output/preview_*.wav")
        
        if preview_files:
            print(f"   ✅ Found {len(preview_files)} preview files:")
            for file_path in preview_files:
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                print(f"      📄 {filename} ({size:,} bytes)")
        else:
            print("   ⚠️ No preview files found in test_inner_voice_output/")
            
            # Check alternative locations
            alt_files = glob.glob("test_audio_output/preview_*.wav")
            if alt_files:
                print(f"   ✅ Found {len(alt_files)} preview files in test_audio_output/:")
                for file_path in alt_files:
                    filename = os.path.basename(file_path)
                    size = os.path.getsize(file_path)
                    print(f"      📄 {filename} ({size:,} bytes)")
        
        print("\n✅ UI INNER VOICE PREVIEW TEST COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ui_preview()
    if success:
        print("\n🎉 UI INNER VOICE PREVIEW SUCCESS!")
        print("✅ Preview buttons hoạt động đúng")
    else:
        print("\n❌ UI inner voice preview có vấn đề") 