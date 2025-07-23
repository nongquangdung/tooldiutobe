"""
Centralized style system for Voice Studio UI components.
Combines the best of both style systems and provides consistent styling across the application.
"""

# Color Palette
COLORS = {
    'primary': '#007AFF',
    'primary_hover': '#0056CC',
    'primary_pressed': '#004499',
    'success': '#28CD41',
    'success_hover': '#25B83A',
    'warning': '#FF9500',
    'warning_hover': '#E6850E',
    'danger': '#FF3B30',
    'danger_hover': '#D70015',
    'neutral': '#8E8E93',
    'text_primary': '#1d1d1f',
    'text_secondary': '#86868b',
    'border': '#d1d1d6',
    'background': '#ffffff',  # Đổi từ xám sang trắng
    'surface': '#ffffff',
    'group_background': '#f8f9fa',  # Màu nền nhẹ cho group
}

# Base Styles
BASE_STYLES = {
    'font_family': '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif',
    'border_radius': '8px',
    'padding': '8px 16px',
}

# Component Styles
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['surface']};
        color: {COLORS['primary']};
        border: 1px solid {COLORS['primary']};
        padding: {BASE_STYLES['padding']};
        border-radius: {BASE_STYLES['border_radius']};
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
    }}
    QPushButton:hover {{
        background-color: #F0F0FF;
        border-color: {COLORS['primary_hover']};
    }}
    QPushButton:pressed {{
        background-color: #E0E0FF;
        border-color: {COLORS['primary_pressed']};
    }}
    QPushButton:disabled {{
        background-color: #F8F9FA;
        color: {COLORS['neutral']};
        border-color: {COLORS['border']};
    }}
"""

PRIMARY_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['surface']};
        border: none;
        padding: {BASE_STYLES['padding']};
        border-radius: {BASE_STYLES['border_radius']};
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary_pressed']};
    }}
    QPushButton:disabled {{
        background-color: {COLORS['neutral']};
        color: {COLORS['surface']};
    }}
"""

SUCCESS_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['surface']};
        color: {COLORS['success']};
        border: 1px solid {COLORS['success']};
        padding: {BASE_STYLES['padding']};
        border-radius: {BASE_STYLES['border_radius']};
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
    }}
    QPushButton:hover {{
        background-color: #F0FFF4;
        border-color: {COLORS['success_hover']};
    }}
"""

DANGER_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['surface']};
        color: {COLORS['danger']};
        border: 1px solid {COLORS['danger']};
        padding: {BASE_STYLES['padding']};
        border-radius: {BASE_STYLES['border_radius']};
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
    }}
    QPushButton:hover {{
        background-color: #FFF5F5;
        border-color: {COLORS['danger_hover']};
    }}
"""

WARNING_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['surface']};
        color: {COLORS['warning']};
        border: 1px solid {COLORS['warning']};
        padding: {BASE_STYLES['padding']};
        border-radius: {BASE_STYLES['border_radius']};
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
    }}
    QPushButton:hover {{
        background-color: #FFF9F0;
        border-color: {COLORS['warning_hover']};
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 13px;
        font-family: {BASE_STYLES['font_family']};
        padding: 4px;
    }}
"""

HEADER_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 18px;
        font-weight: bold;
        font-family: {BASE_STYLES['font_family']};
        padding: 8px;
    }}
"""

STATUS_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        font-family: {BASE_STYLES['font_family']};
        padding: 4px;
    }}
"""

INPUT_STYLE = f"""
    QLineEdit, QTextEdit, QComboBox {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        font-family: {BASE_STYLES['font_family']};
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 2px solid {COLORS['primary']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_secondary']};
        margin-right: 5px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary']};
        selection-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
    }}
"""

TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {COLORS['surface']};
        alternate-background-color: #f8f9fa;
        gridline-color: {COLORS['border']};
        font-size: 12px;
        font-family: {BASE_STYLES['font_family']};
    }}
    QHeaderView::section {{
        background-color: #f1f3f4;
        padding: 8px;
        border: 1px solid {COLORS['border']};
        font-weight: bold;
        font-size: 12px;
    }}
    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {COLORS['border']};
    }}
"""

GROUP_BOX_STYLE = f"""
    QGroupBox {{
        font-weight: 600;
        font-size: 14px;
        border: 2px solid {COLORS['border']};
        border-radius: 12px;
        margin-top: 15px;
        padding-top: 15px;
        background-color: {COLORS['group_background']};
        font-family: {BASE_STYLES['font_family']};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 15px;
        padding: 4px 12px;
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }}
"""

SCROLL_AREA_STYLE = f"""
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    QScrollBar:vertical {{
        background-color: #f0f0f0;
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: #c0c0c0;
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: #a0a0a0;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

CHECKBOX_STYLE = f"""
    QCheckBox {{
        spacing: 8px;
        font-size: 13px;
        font-family: {BASE_STYLES['font_family']};
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid {COLORS['border']};
        background-color: {COLORS['surface']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
    }}
    QCheckBox::indicator:hover {{
        border-color: {COLORS['primary']};
    }}
"""

# Function to get complete stylesheet for a window/widget
def get_stylesheet():
    """Returns the complete stylesheet for the application"""
    return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {COLORS['background']};
            font-family: {BASE_STYLES['font_family']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {COLORS['border']};
            background-color: {COLORS['surface']};
            border-radius: {BASE_STYLES['border_radius']};
            margin-top: 4px;
        }}
        
        QTabBar::tab {{
            background-color: #e8e8e8;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: {BASE_STYLES['border_radius']};
            border-top-right-radius: {BASE_STYLES['border_radius']};
            font-weight: 500;
            min-width: 80px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {COLORS['surface']};
            border-bottom: 3px solid {COLORS['primary']};
            color: {COLORS['primary']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: #ddd;
        }}
        
        {BUTTON_STYLE}
        {LABEL_STYLE}
        {INPUT_STYLE}
        {TABLE_STYLE}
        {GROUP_BOX_STYLE}
        {SCROLL_AREA_STYLE}
        {CHECKBOX_STYLE}
    """