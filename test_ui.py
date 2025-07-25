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
    
    # Print tab info
    print(f"Total tabs: {window.tabs.count()}")
    for i in range(window.tabs.count()):
        tab_name = window.tabs.tabText(i)
        print(f"Tab {i}: {tab_name}")
    
    sys.exit(app.exec())