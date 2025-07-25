"""
Modern UI Styles for Voice Studio
Áp dụng Material Design 3 và Minimalist Design principles
"""

from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ModernColors:
    """Modern color palette theo Material Design 3 và Minimalist principles"""
    
    # Primary colors - Xanh dương theo Material Design
    PRIMARY = "#0d6efd"
    PRIMARY_HOVER = "#0b5ed7" 
    PRIMARY_PRESSED = "#004085"
    PRIMARY_LIGHT = "#9ac3fe"
    
    # Surface colors - Minimalist approach
    SURFACE = "#ffffff"
    SURFACE_SECONDARY = "#f8f9fa"
    SURFACE_TERTIARY = "#f0f0f0"
    
    # Text colors với độ tương phản WCAG compliant
    TEXT_PRIMARY = "#0f1925"  # Tỷ lệ tương phản > 4.5:1
    TEXT_SECONDARY = "#464d55"
    TEXT_TERTIARY = "#767e89"
    TEXT_PLACEHOLDER = "#767e89"
    
    # Border colors
    BORDER_DEFAULT = "#e0e4e7"
    BORDER_FOCUS = "#d0e3ff"
    BORDER_DISABLED = "#f0f0f0"
    
    # Status colors
    SUCCESS = "#2ecc71"  # Flat Design Green
    WARNING = "#f1c40f"  # Flat Design Yellow
    ERROR = "#e74c3c"    # Flat Design Red
    INFO = "#3498db"     # Flat Design Blue
    
    # Disabled states
    DISABLED_BG = "#f0f0f0"
    DISABLED_TEXT = "#808080"

class ModernSpacing:
    """Spacing system theo Material Design 8dp grid"""
    
    # Base spacing unit (8dp)
    UNIT = 8
    
    # Margins - 16px theo khuyến nghị
    MARGIN_SMALL = UNIT     # 8px
    MARGIN_DEFAULT = UNIT * 2  # 16px
    MARGIN_LARGE = UNIT * 3    # 24px
    
    # Padding - 8px theo khuyến nghị
    PADDING_SMALL = UNIT // 2   # 4px
    PADDING_DEFAULT = UNIT      # 8px
    PADDING_LARGE = UNIT * 2    # 16px
    
    # Layout spacing
    LAYOUT_SPACING = UNIT * 2   # 16px
    SECTION_SPACING = UNIT * 3  # 24px
    
    # Border radius
    BORDER_RADIUS_SMALL = 4
    BORDER_RADIUS_DEFAULT = 8
    BORDER_RADIUS_LARGE = 12

class ModernTypography:
    """Typography system với hierarchy rõ ràng"""
    
    # Font family - System fonts
    FONT_FAMILY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    
    # Font sizes - GIẢM SIZE CHO COMPACT HỢN
    FONT_H1 = 18  # Tiêu đề chính (giảm từ 24)
    FONT_H2 = 16  # Tiêu đề phụ (giảm từ 20)
    FONT_H3 = 14  # Tiêu đề nhóm (giảm từ 18)
    FONT_BODY = 13  # Văn bản chính (giảm từ 16)
    FONT_SMALL = 12  # Văn bản nhỏ (giảm từ 14)
    FONT_CAPTION = 11  # Chú thích (giảm từ 12)
    
    # Font weights
    WEIGHT_LIGHT = 300
    WEIGHT_NORMAL = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700

class ModernStyles:
    """Modern style definitions cho các widget"""
    
    @staticmethod
    def get_button_style(variant="primary"):
        """
        QPushButton styles với các variant khác nhau
        Kích thước vùng chạm 48x48dp theo Material Design
        """
        base_style = f"""
            QPushButton {{
                font-family: {ModernTypography.FONT_FAMILY};
                font-size: {ModernTypography.FONT_BODY}px;
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                padding: {ModernSpacing.PADDING_DEFAULT}px {ModernSpacing.PADDING_LARGE}px;
                min-height: 20px;  /* Compact button size */
                border: none;
            }}
        """
        
        if variant == "primary":
            return base_style + f"""
                QPushButton {{
                    background-color: {ModernColors.PRIMARY};
                    color: {ModernColors.SURFACE};
                }}
                QPushButton:hover {{
                    background-color: {ModernColors.PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {ModernColors.PRIMARY_PRESSED};
                }}
                QPushButton:disabled {{
                    background-color: {ModernColors.DISABLED_BG};
                    color: {ModernColors.DISABLED_TEXT};
                }}
            """
        elif variant == "secondary":
            return base_style + f"""
                QPushButton {{
                    background-color: {ModernColors.SURFACE};
                    color: {ModernColors.PRIMARY};
                    border: 1px solid {ModernColors.PRIMARY};
                }}
                QPushButton:hover {{
                    background-color: {ModernColors.PRIMARY_LIGHT};
                    border-color: {ModernColors.PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {ModernColors.PRIMARY_PRESSED};
                    color: {ModernColors.SURFACE};
                }}
            """
        elif variant == "success":
            return base_style + f"""
                QPushButton {{
                    background-color: {ModernColors.SUCCESS};
                    color: {ModernColors.SURFACE};
                }}
                QPushButton:hover {{
                    background-color: #25a866;
                }}
            """
        elif variant == "warning":
            return base_style + f"""
                QPushButton {{
                    background-color: {ModernColors.WARNING};
                    color: {ModernColors.TEXT_PRIMARY};
                }}
                QPushButton:hover {{
                    background-color: #e6b800;
                }}
            """
        elif variant == "error":
            return base_style + f"""
                QPushButton {{
                    background-color: {ModernColors.ERROR};
                    color: {ModernColors.SURFACE};
                }}
                QPushButton:hover {{
                    background-color: #c0392b;
                }}
            """
    
    @staticmethod
    def get_input_style():
        """QLineEdit và QTextEdit styles"""
        return f"""
            QLineEdit, QTextEdit {{
                font-family: {ModernTypography.FONT_FAMILY};
                font-size: {ModernTypography.FONT_BODY}px;
                color: {ModernColors.TEXT_PRIMARY};
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                selection-background-color: {ModernColors.PRIMARY_LIGHT};
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {ModernColors.BORDER_FOCUS};
            }}
            
            QLineEdit:disabled, QTextEdit:disabled {{
                background-color: {ModernColors.DISABLED_BG};
                color: {ModernColors.DISABLED_TEXT};
                border-color: {ModernColors.BORDER_DISABLED};
            }}
            
            QLineEdit::placeholder, QTextEdit::placeholder {{
                color: {ModernColors.TEXT_PLACEHOLDER};
            }}
        """
    
    @staticmethod
    def get_combobox_style():
        """QComboBox styles với custom dropdown arrow"""
        return f"""
            QComboBox {{
                font-family: {ModernTypography.FONT_FAMILY};
                font-size: {ModernTypography.FONT_BODY}px;
                color: {ModernColors.TEXT_PRIMARY};
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                padding-right: 30px;  /* Space for arrow */
                min-width: 120px;
            }}
            
            QComboBox:focus {{
                border: 2px solid {ModernColors.BORDER_FOCUS};
            }}
            
            QComboBox:disabled {{
                background-color: {ModernColors.DISABLED_BG};
                color: {ModernColors.DISABLED_TEXT};
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
            }}
            
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
                border-left: 2px solid {ModernColors.TEXT_SECONDARY};
                border-bottom: 2px solid {ModernColors.TEXT_SECONDARY};
                transform: rotate(-45deg);
                margin-top: -6px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                selection-background-color: {ModernColors.PRIMARY_LIGHT};
                selection-color: {ModernColors.TEXT_PRIMARY};
                padding: {ModernSpacing.PADDING_SMALL}px;
            }}
            
            QComboBox QAbstractItemView::item {{
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                border-radius: {ModernSpacing.BORDER_RADIUS_SMALL}px;
                margin: 1px;
            }}
        """
    
    @staticmethod
    def get_table_style():
        """QTableWidget styles với proper border-radius và clear cell visibility"""
        return f"""
            QTableWidget {{
                font-family: {ModernTypography.FONT_FAMILY};
                font-size: {ModernTypography.FONT_SMALL}px;
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
                gridline-color: transparent;
                selection-background-color: {ModernColors.PRIMARY_LIGHT};
                alternate-background-color: {ModernColors.SURFACE_SECONDARY};
                outline: none;
            }}
            
            QTableWidget::item {{
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                border: none;
                background-color: transparent;
                border-bottom: 1px solid {ModernColors.SURFACE_SECONDARY};
                text-align: center;
                vertical-align: middle;
            }}
            
            QTableWidget::item:selected {{
                background-color: {ModernColors.PRIMARY_LIGHT};
                color: {ModernColors.TEXT_PRIMARY};
                border-radius: 4px;
            }}
            
            QHeaderView {{
                background-color: transparent;
            }}
            
            QHeaderView::section {{
                background-color: {ModernColors.SURFACE_TERTIARY};
                color: {ModernColors.TEXT_SECONDARY};
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                border: none;
                border-bottom: 2px solid {ModernColors.BORDER_DEFAULT};
                border-right: 1px solid {ModernColors.BORDER_DEFAULT};
            }}
            
            QHeaderView::section:first {{
                border-top-left-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
                border-left: none;
            }}
            
            QHeaderView::section:last {{
                border-top-right-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
                border-right: none;
            }}
        """
    
    @staticmethod
    def get_table_cell_widget_style():
        """Styling cho widgets bên trong table cells - ComboBox, LineEdit, etc với vertical alignment"""
        return f"""
            /* ComboBox trong table cells - căn giữa theo chiều dọc */
            QComboBox {{
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: {ModernTypography.FONT_SMALL}px;
                height: 28px;
                margin: 0px;
            }}
            
            QComboBox:focus {{
                border: 2px solid {ModernColors.PRIMARY_LIGHT};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 16px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                selection-background-color: {ModernColors.PRIMARY_LIGHT};
            }}
            
            /* LineEdit trong table cells - căn giữa theo chiều dọc */
            QLineEdit {{
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: {ModernTypography.FONT_SMALL}px;
                height: 28px;
                margin: 0px;
                text-align: center;
            }}
            
            QLineEdit:focus {{
                border: 2px solid {ModernColors.PRIMARY_LIGHT};
            }}
            
            /* Labels trong table cells - căn giữa theo chiều dọc */
            QLabel {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: {ModernTypography.FONT_SMALL}px;
                height: 28px;
                margin: 0px;
                qproperty-alignment: AlignCenter;
            }}
            
            /* QPushButton trong table cells - căn giữa theo chiều dọc */
            QPushButton {{
                background-color: {ModernColors.PRIMARY};
                color: {ModernColors.SURFACE};
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: {ModernTypography.FONT_CAPTION}px;
                height: 28px;
                margin: 0px;
            }}
            
            QPushButton:hover {{
                background-color: {ModernColors.PRIMARY_HOVER};
            }}
        """
    
    @staticmethod
    def get_groupbox_style():
        """QGroupBox styles với modern title styling"""
        return f"""
            QGroupBox {{
                font-family: {ModernTypography.FONT_FAMILY};
                font-size: {ModernTypography.FONT_H3}px;
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                color: {ModernColors.TEXT_PRIMARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
                margin-top: {ModernSpacing.MARGIN_LARGE}px;
                padding-top: {ModernSpacing.PADDING_LARGE}px;
                background-color: {ModernColors.SURFACE};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: {ModernSpacing.PADDING_DEFAULT}px {ModernSpacing.PADDING_LARGE}px;
                background-color: {ModernColors.PRIMARY};
                color: {ModernColors.SURFACE};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                margin-left: {ModernSpacing.MARGIN_DEFAULT}px;
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
            }}
        """
    
    @staticmethod
    def get_label_style(variant="body"):
        """QLabel styles với typography hierarchy"""
        base_style = f"""
            QLabel {{
                font-family: {ModernTypography.FONT_FAMILY};
                color: {ModernColors.TEXT_PRIMARY};
            }}
        """
        
        if variant == "h1":
            return base_style + f"""
                QLabel {{
                    font-size: {ModernTypography.FONT_H1}px;
                    font-weight: {ModernTypography.WEIGHT_BOLD};
                    margin-bottom: {ModernSpacing.MARGIN_DEFAULT}px;
                }}
            """
        elif variant == "h2":
            return base_style + f"""
                QLabel {{
                    font-size: {ModernTypography.FONT_H2}px;
                    font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                    margin-bottom: {ModernSpacing.MARGIN_SMALL}px;
                }}
            """
        elif variant == "h3":
            return base_style + f"""
                QLabel {{
                    font-size: {ModernTypography.FONT_H3}px;
                    font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                    color: {ModernColors.TEXT_SECONDARY};
                }}
            """
        elif variant == "caption":
            return base_style + f"""
                QLabel {{
                    font-size: {ModernTypography.FONT_CAPTION}px;
                    color: {ModernColors.TEXT_TERTIARY};
                }}
            """
        else:  # body
            return base_style + f"""
                QLabel {{
                    font-size: {ModernTypography.FONT_BODY}px;
                }}
            """

class ModernEffects:
    """Modern visual effects như shadows"""
    
    @staticmethod
    def create_card_shadow():
        """Tạo bóng đổ cho card theo Material Design elevation 2dp"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 20))  # Màu đen với opacity 20/255
        shadow.setOffset(0, 2)  # Offset Y = 2px
        shadow.setBlurRadius(4)  # Blur radius 4px
        return shadow
    
    @staticmethod
    def create_button_shadow():
        """Tạo bóng đổ cho button khi hover"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(8)
        return shadow
    
    @staticmethod
    def create_dialog_shadow():
        """Tạo bóng đổ cho dialog theo Material Design elevation 24dp"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 12)
        shadow.setBlurRadius(24)
        return shadow

def apply_modern_theme(widget):
    """Áp dụng modern theme cho một widget"""
    # Áp dụng font family cho toàn bộ widget
    widget.setStyleSheet(f"""
        * {{
            font-family: {ModernTypography.FONT_FAMILY};
        }}
        
        {ModernStyles.get_button_style("primary")}
        {ModernStyles.get_input_style()}
        {ModernStyles.get_combobox_style()}
        {ModernStyles.get_table_style()}
        {ModernStyles.get_groupbox_style()}
        {ModernStyles.get_label_style("body")}
    """)