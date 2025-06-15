# main.py

from PySide6.QtWidgets import QApplication
from ui.advanced_window import AdvancedMainWindow
import sys

# Entry point cho ứng dụng tạo video AI

def main():
    app = QApplication(sys.argv)
    window = AdvancedMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 