"""
MacOS-optimized styles for Voice Studio
Modern UI with macOS Sonoma/Ventura design language
Supports Dark Mode, Vibrancy, and Accessibility
"""

import platform

def get_macos_stylesheet(dark_mode=False):
    """
    Trả về stylesheet tối ưu cho macOS với support Dark Mode
    
    Args:
        dark_mode (bool): Enable dark mode styling
    """
    
    # Color Schemes
    if dark_mode:
        colors = {
            'bg_primary': '#1c1c1e',
            'bg_secondary': '#2c2c2e', 
            'bg_tertiary': '#3a3a3c',
            'bg_card': '#2c2c2e',
            'text_primary': '#ffffff',
            'text_secondary': '#ebebf5',
            'text_tertiary': '#ebebf599',
            'accent': '#007AFF',
            'accent_hover': '#0056CC',
            'accent_pressed': '#004499',
            'border': '#38383a',
            'border_focus': '#007AFF',
            'success': '#32d74b',
            'warning': '#ff9f0a',
            'error': '#ff453a',
            'selection': '#007AFF33'
        }
    else:
        colors = {
            'bg_primary': '#f2f2f7',
            'bg_secondary': '#ffffff',
            'bg_tertiary': '#f9f9f9', 
            'bg_card': '#ffffff',
            'text_primary': '#000000',
            'text_secondary': '#3c3c43',
            'text_tertiary': '#3c3c4399',
            'accent': '#007AFF',
            'accent_hover': '#0056CC', 
            'accent_pressed': '#004499',
            'border': '#d1d1d6',
            'border_focus': '#007AFF',
            'success': '#34c759',
            'warning': '#ff9500',
            'error': '#ff3b30',
            'selection': '#007AFF33'
        }
    
    return f"""
        /* ============ MAIN WINDOW ============ */
        QMainWindow {{
            background-color: {colors['bg_primary']};
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
            font-size: 13px;
            color: {colors['text_primary']};
        }}
        
        /* ============ MODERN TABS ============ */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            background-color: {colors['bg_card']};
            border-radius: 12px;
            margin-top: 8px;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            padding: 12px 24px;
            margin-right: 4px;
            border-radius: 10px;
            font-weight: 500;
            font-size: 13px;
            min-width: 100px;
            color: {colors['text_secondary']};
            transition: all 0.2s ease;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['accent']};
            color: white;
            font-weight: 600;
            transform: scale(1.02);
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_primary']};
        }}
        
        /* ============ MODERN BUTTONS ============ */
        QPushButton {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 13px;
            min-height: 24px;
            transition: all 0.2s ease;
        }}
        
        QPushButton:hover {{
            background-color: {colors['accent_hover']};
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
        }}
        
        QPushButton:pressed {{
            background-color: {colors['accent_pressed']};
            transform: translateY(0px);
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
        }}
        
        QPushButton:disabled {{
            background-color: {colors['border']};
            color: {colors['text_tertiary']};
            transform: none;
            box-shadow: none;
        }}
        
        /* Secondary Button Style */
        QPushButton[class="secondary"] {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {colors['bg_secondary']};
            border-color: {colors['accent']};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        /* Success Button */
        QPushButton[class="success"] {{
            background-color: {colors['success']};
        }}
        
        QPushButton[class="success"]:hover {{
            background-color: #28cd47;
            box-shadow: 0 4px 12px rgba(52, 199, 89, 0.3);
        }}
        
        /* Warning Button */
        QPushButton[class="warning"] {{
            background-color: {colors['warning']};
        }}
        
        QPushButton[class="warning"]:hover {{
            background-color: #e6850e;
            box-shadow: 0 4px 12px rgba(255, 149, 0, 0.3);
        }}
        
        /* Danger Button */
        QPushButton[class="danger"] {{
            background-color: {colors['error']};
        }}
        
        QPushButton[class="danger"]:hover {{
            background-color: #d70015;
            box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3);
        }}
        
        /* ============ MODERN INPUT FIELDS ============ */
        QLineEdit, QTextEdit, QComboBox {{
            border: 1.5px solid {colors['border']};
            border-radius: 10px;
            padding: 12px 16px;
            background-color: {colors['bg_card']};
            font-size: 13px;
            color: {colors['text_primary']};
            selection-background-color: {colors['selection']};
            transition: all 0.2s ease;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border: 2px solid {colors['border_focus']};
            outline: none;
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        }}
        
        QTextEdit {{
            padding: 16px;
            line-height: 1.5;
        }}
        
        /* ============ ENHANCED COMBOBOX ============ */
        QComboBox::drop-down {{
            border: none;
            width: 24px;
            padding-right: 8px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid {colors['text_secondary']};
            margin-right: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 1px solid {colors['border']};
            border-radius: 12px;
            background-color: {colors['bg_card']};
            selection-background-color: {colors['accent']};
            selection-color: white;
            padding: 8px;
            outline: none;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 10px 16px;
            border-radius: 8px;
            margin: 2px 4px;
        }}
        
        /* ============ MODERN GROUP BOXES ============ */
        QGroupBox {{
            font-weight: 600;
            font-size: 15px;
            border: 2px solid {colors['border']};
            border-radius: 16px;
            margin-top: 16px;
            padding-top: 20px;
            background-color: {colors['bg_card']};
            color: {colors['text_primary']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 12px 0 12px;
            background-color: {colors['bg_card']};
            color: {colors['text_primary']};
            font-weight: 700;
        }}
        
        /* ============ TYPOGRAPHY ============ */
        QLabel {{
            color: {colors['text_primary']};
            font-size: 13px;
        }}
        
        QLabel[class="header"] {{
            font-size: 20px;
            font-weight: 700;
            color: {colors['text_primary']};
            letter-spacing: -0.5px;
        }}
        
        QLabel[class="subheader"] {{
            font-size: 16px;
            font-weight: 600;
            color: {colors['text_secondary']};
            letter-spacing: -0.2px;
        }}
        
        QLabel[class="caption"] {{
            font-size: 12px;
            font-weight: 500;
            color: {colors['text_tertiary']};
        }}
        
        /* ============ MODERN PROGRESS BAR ============ */
        QProgressBar {{
            border: none;
            border-radius: 12px;
            text-align: center;
            background-color: {colors['bg_tertiary']};
            height: 24px;
            font-weight: 600;
            color: {colors['text_primary']};
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                      stop: 0 {colors['accent']}, 
                                      stop: 1 #5AC8FA);
            border-radius: 12px;
            margin: 2px;
        }}
        
        /* ============ ENHANCED LIST WIDGET ============ */
        QListWidget {{
            border: 1px solid {colors['border']};
            border-radius: 12px;
            background-color: {colors['bg_card']};
            alternate-background-color: {colors['bg_tertiary']};
            selection-background-color: {colors['accent']};
            selection-color: white;
            padding: 8px;
            outline: none;
        }}
        
        QListWidget::item {{
            padding: 12px 16px;
            border-radius: 8px;
            margin: 2px 4px;
            transition: all 0.2s ease;
        }}
        
        QListWidget::item:hover {{
            background-color: {colors['bg_tertiary']};
            transform: translateX(4px);
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
            font-weight: 600;
        }}
        
        /* ============ MODERN SCROLLBARS ============ */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            border-radius: 4px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            border-radius: 4px;
            min-height: 24px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['text_tertiary']};
        }}
        
        QScrollBar:horizontal {{
            background-color: transparent;
            height: 8px;
            border-radius: 4px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['border']};
            border-radius: 4px;
            min-width: 24px;
            margin: 0;
        }}
        
        /* ============ ELEGANT SPLITTER ============ */
        QSplitter::handle {{
            background-color: {colors['border']};
            width: 2px;
            border-radius: 1px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {colors['accent']};
        }}
        
        /* ============ MODERN CHECKBOXES ============ */
        QCheckBox {{
            spacing: 12px;
            font-size: 13px;
            color: {colors['text_primary']};
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 6px;
            border: 2px solid {colors['border']};
            background-color: {colors['bg_card']};
            transition: all 0.2s ease;
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['accent']};
            border-color: {colors['accent']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTEiIHZpZXdCb3g9IjAgMCAxNCAxMSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEgNS41TDUuNSAxMEwxMyAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {colors['accent']};
            transform: scale(1.05);
        }}
        
        /* ============ ENHANCED SPIN BOX ============ */
        QSpinBox, QDoubleSpinBox {{
            border: 1.5px solid {colors['border']};
            border-radius: 10px;
            padding: 12px 16px;
            background-color: {colors['bg_card']};
            font-size: 13px;
            color: {colors['text_primary']};
            selection-background-color: {colors['selection']};
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {colors['border_focus']};
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        }}
        
        QSpinBox::up-button, QSpinBox::down-button,
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
            width: 20px;
            border: none;
            background-color: transparent;
            border-radius: 6px;
        }}
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover,
        QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {colors['bg_tertiary']};
        }}
        
        /* ============ MODERN TOOLTIPS ============ */
        QToolTip {{
            background-color: {colors['text_primary']};
            color: {colors['bg_primary']};
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 500;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }}
        
        /* ============ TABLE WIDGET ============ */
        QTableWidget {{
            border: 1px solid {colors['border']};
            border-radius: 12px;
            background-color: {colors['bg_card']};
            gridline-color: {colors['border']};
            selection-background-color: {colors['selection']};
            alternate-background-color: {colors['bg_tertiary']};
        }}
        
        QTableWidget::item {{
            padding: 8px 12px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_primary']};
            padding: 12px 16px;
            border: none;
            border-bottom: 1px solid {colors['border']};
            font-weight: 600;
        }}
        
        /* ============ MODERN SLIDER ============ */
        QSlider::groove:horizontal {{
            border: none;
            height: 6px;
            background-color: {colors['bg_tertiary']};
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {colors['accent']};
            border: none;
            width: 20px;
            height: 20px;
            border-radius: 10px;
            margin: -7px 0;
        }}
        
        QSlider::handle:horizontal:hover {{
            background-color: {colors['accent_hover']};
            transform: scale(1.1);
        }}
        
        QSlider::sub-page:horizontal {{
            background-color: {colors['accent']};
            border-radius: 3px;
        }}
    """

def get_dark_mode_enabled():
    """Detect if system is in dark mode (macOS only)"""
    if platform.system() == "Darwin":
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'Dark'
        except:
            return False
    return False

def get_modern_spacing():
    """Modern spacing values for macOS design"""
    return {
        'window_margin': 20,
        'section_spacing': 24,
        'group_spacing': 16,
        'item_spacing': 8,
        'button_padding': '12px 20px',
        'input_padding': '12px 16px',
        'group_margin_top': 16,
        'card_padding': '20px',
        'border_radius': '12px'
    }

def get_macos_window_size():
    """Optimized window sizes for modern macOS"""
    return {
        'default_width': 1400,
        'default_height': 900,
        'min_width': 1200,
        'min_height': 800,
        'max_width': 1800,
        'max_height': 1200,
        'compact_width': 1000,
        'compact_height': 700
    }

def apply_macos_vibrancy(widget):
    """Apply macOS vibrancy effect to widget (if supported)"""
    if platform.system() == "Darwin":
        try:
            # This would require PyObjC for native vibrancy
            # For now, we'll use a visual approximation
            widget.setStyleSheet(widget.styleSheet() + """
                background-color: rgba(248, 248, 248, 0.8);
                backdrop-filter: blur(20px);
            """)
        except:
            pass

def get_accent_color():
    """Get system accent color (macOS)"""
    if platform.system() == "Darwin":
        try:
            import subprocess
            # Try to get system accent color
            result = subprocess.run(['defaults', 'read', '-g', 'AppleAccentColor'], 
                                  capture_output=True, text=True)
            accent_map = {
                '0': '#FF3B30',  # Red
                '1': '#FF9500',  # Orange  
                '2': '#FFCC00',  # Yellow
                '3': '#34C759',  # Green
                '4': '#007AFF',  # Blue (default)
                '5': '#5856D6',  # Purple
                '6': '#FF2D92',  # Pink
            }
            accent_id = result.stdout.strip()
            return accent_map.get(accent_id, '#007AFF')
        except:
            return '#007AFF'
    return '#007AFF' 