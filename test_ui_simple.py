import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from src.ui.advanced_window import AdvancedMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("Creating window...")
    window = AdvancedMainWindow()
    print("Showing window...")
    window.show()
    
    # Print tab info without emoji
    print(f"Total tabs: {window.tabs.count()}")
    for i in range(window.tabs.count()):
        try:
            tab_name = window.tabs.tabText(i)
            # Remove emojis for safe printing
            safe_name = ''.join(c for c in tab_name if ord(c) < 128)
            print(f"Tab {i}: {safe_name}")
        except:
            print(f"Tab {i}: <error reading name>")
    
    sys.exit(app.exec())