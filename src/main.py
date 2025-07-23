# main.py

from PySide6.QtWidgets import QApplication
from ui.advanced_window import AdvancedMainWindow
import sys
import os

# Entry point cho ứng dụng tạo video AI

def setup_ffmpeg_path():
    """Auto-detect and add local ffmpeg to PATH"""
    local_ffmpeg_path = os.path.join(os.getcwd(), "tools", "ffmpeg")
    if os.path.exists(local_ffmpeg_path):
        current_path = os.environ.get("PATH", "")
        if local_ffmpeg_path not in current_path:
            os.environ["PATH"] = local_ffmpeg_path + os.pathsep + current_path
            print(f"[OK] Added local ffmpeg to PATH: {local_ffmpeg_path}")
    else:
        print("[WARNING] Local ffmpeg not found - run install_dependencies.bat")

def main():
    # Setup environment
    setup_ffmpeg_path()
    
    app = QApplication(sys.argv)
    window = AdvancedMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 