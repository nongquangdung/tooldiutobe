"""
MacOS-optimized styles for AI Video Generator
Tối ưu giao diện cho màn hình MacOS 13 inch
"""

def get_macos_stylesheet():
    """Trả về stylesheet tối ưu cho MacOS"""
    return """
        /* Main Window */
        QMainWindow {
            background-color: #f5f5f5;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #d0d0d0;
            background-color: white;
            border-radius: 8px;
            margin-top: 4px;
        }
        
        QTabBar::tab {
            background-color: #e8e8e8;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 3px solid #007AFF;
            color: #007AFF;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #ddd;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #007AFF;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 13px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #0056CC;
        }
        
        QPushButton:pressed {
            background-color: #004499;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
        
        /* Secondary buttons */
        QPushButton[class="secondary"] {
            background-color: #f0f0f0;
            color: #333;
            border: 1px solid #d0d0d0;
        }
        
        QPushButton[class="secondary"]:hover {
            background-color: #e0e0e0;
        }
        
        /* Danger buttons */
        QPushButton[class="danger"] {
            background-color: #FF3B30;
        }
        
        QPushButton[class="danger"]:hover {
            background-color: #D70015;
        }
        
        /* Input Fields */
        QLineEdit, QTextEdit, QComboBox {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            padding: 8px 12px;
            background-color: white;
            font-size: 13px;
            selection-background-color: #007AFF;
        }
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 2px solid #007AFF;
            outline: none;
        }
        
        QTextEdit {
            padding: 12px;
            line-height: 1.4;
        }
        
        /* ComboBox specific */
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #666;
            margin-right: 5px;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            background-color: white;
            selection-background-color: #007AFF;
            selection-color: white;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            border: 1px solid #d0d0d0;
            border-radius: 10px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            background-color: white;
            color: #333;
        }
        
        /* Labels */
        QLabel {
            color: #333;
            font-size: 13px;
        }
        
        QLabel[class="header"] {
            font-size: 16px;
            font-weight: 600;
            color: #000;
        }
        
        QLabel[class="subheader"] {
            font-size: 14px;
            font-weight: 500;
            color: #666;
        }
        
        /* Progress Bar */
        QProgressBar {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            text-align: center;
            background-color: #f0f0f0;
            height: 20px;
        }
        
        QProgressBar::chunk {
            background-color: #007AFF;
            border-radius: 7px;
            margin: 1px;
        }
        
        /* List Widget */
        QListWidget {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            background-color: white;
            alternate-background-color: #f9f9f9;
            selection-background-color: #007AFF;
            selection-color: white;
            padding: 4px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QListWidget::item:hover {
            background-color: #f0f0f0;
        }
        
        QListWidget::item:selected {
            background-color: #007AFF;
            color: white;
        }
        
        /* Scroll Areas */
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        /* Splitter */
        QSplitter::handle {
            background-color: #d0d0d0;
            width: 1px;
        }
        
        QSplitter::handle:hover {
            background-color: #007AFF;
        }
        
        /* Checkboxes */
        QCheckBox {
            spacing: 8px;
            font-size: 13px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #d0d0d0;
            background-color: white;
        }
        
        QCheckBox::indicator:checked {
            background-color: #007AFF;
            border-color: #007AFF;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }
        
        QCheckBox::indicator:hover {
            border-color: #007AFF;
        }
        
        /* Spin Box */
        QSpinBox {
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            padding: 8px 12px;
            background-color: white;
            font-size: 13px;
        }
        
        QSpinBox:focus {
            border: 2px solid #007AFF;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            width: 20px;
            border: none;
            background-color: transparent;
        }
        
        QSpinBox::up-arrow, QSpinBox::down-arrow {
            width: 8px;
            height: 8px;
        }
        
        /* Tooltips */
        QToolTip {
            background-color: #333;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 12px;
        }
    """

def get_compact_spacing():
    """Trả về các giá trị spacing tối ưu cho MacOS 13 inch"""
    return {
        'window_margin': 12,
        'group_spacing': 10,
        'item_spacing': 6,
        'button_padding': '8px 16px',
        'input_padding': '6px 10px',
        'group_margin_top': 8
    }

def get_macos_window_size():
    """Trả về kích thước cửa sổ tối ưu cho MacOS 13 inch"""
    return {
        'default_width': 1200,
        'default_height': 800,
        'min_width': 1000,
        'min_height': 700,
        'max_width': 1400,
        'max_height': 900
    } 