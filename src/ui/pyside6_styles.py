"""
Centralized style system for Voice Studio UI components.
Optimized for PySide6.
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
    'background': '#f5f5f7',
    'surface': '#ffffff',
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
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: {BASE_STYLES['border_radius']};
        padding: {BASE_STYLES['padding']};
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
    }}
"""

INPUT_STYLE = f"""
    QComboBox, QLineEdit, QTextEdit {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: {BASE_STYLES['border_radius']};
        padding: 6px 12px;
        font-family: {BASE_STYLES['font_family']};
    }}
    QComboBox:hover, QLineEdit:hover, QTextEdit:hover {{
        border-color: {COLORS['primary']};
    }}
    QComboBox:focus, QLineEdit:focus, QTextEdit:focus {{
        border-color: {COLORS['primary']};
        border-width: 2px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
        padding-right: 4px;
    }}
    QComboBox::down-arrow {{
        image: url(resources/icons/chevron-down.svg);
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary']};
        selection-color: white;
        border: 1px solid {COLORS['border']};
        border-radius: {BASE_STYLES['border_radius']};
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-family: {BASE_STYLES['font_family']};
    }}
"""

TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: {BASE_STYLES['border_radius']};
        gridline-color: {COLORS['border']};
        font-family: {BASE_STYLES['font_family']};
    }}
    QTableWidget::item {{
        padding: 4px;
    }}
    QTableWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    QHeaderView::section {{
        background-color: {COLORS['background']};
        color: {COLORS['text_primary']};
        padding: 6px;
        border: none;
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        font-weight: bold;
    }}
"""

GROUP_BOX_STYLE = f"""
    QGroupBox {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: {BASE_STYLES['border_radius']};
        margin-top: 1em;
        padding-top: 1em;
        font-family: {BASE_STYLES['font_family']};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 8px;
        padding: 0 3px;
        color: {COLORS['text_primary']};
        font-weight: bold;
    }}
"""

SCROLL_AREA_STYLE = f"""
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    QScrollBar:vertical {{
        border: none;
        background-color: {COLORS['background']};
        width: 12px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: {COLORS['neutral']};
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
        background: none;
    }}
    QScrollBar:horizontal {{
        border: none;
        background-color: {COLORS['background']};
        height: 12px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {COLORS['neutral']};
        border-radius: 6px;
        min-width: 20px;
        margin: 2px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
        background: none;
    }}
"""

CHECKBOX_STYLE = f"""
    QCheckBox {{
        color: {COLORS['text_primary']};
        font-family: {BASE_STYLES['font_family']};
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
    QCheckBox::indicator:unchecked {{
        background-color: {COLORS['surface']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
        image: url(resources/icons/check.svg);
    }}
    QCheckBox::indicator:hover {{
        border-color: {COLORS['primary']};
    }}
"""

def get_stylesheet():
    """Returns the complete stylesheet for the application."""
    return f"""
        /* Global Styles */
        * {{
            font-family: {BASE_STYLES['font_family']};
        }}
        
        /* Button Styles */
        {BUTTON_STYLE}
        
        /* Input Styles */
        {INPUT_STYLE}
        
        /* Label Styles */
        {LABEL_STYLE}
        
        /* Table Styles */
        {TABLE_STYLE}
        
        /* Group Box Styles */
        {GROUP_BOX_STYLE}
        
        /* Scroll Area Styles */
        {SCROLL_AREA_STYLE}
        
        /* Checkbox Styles */
        {CHECKBOX_STYLE}
    """ 