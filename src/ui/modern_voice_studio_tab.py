"""
Modern Voice Studio Tab
Áp dụng modern design principles với beautiful UI và full functionality
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QLineEdit, QScrollArea,
    QFrame, QCheckBox, QProgressBar, QTextEdit,
    QStackedWidget, QHeaderView, QSplitter
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .modern_styles import (
    ModernStyles, ModernColors, ModernSpacing, 
    ModernTypography, ModernEffects, apply_modern_theme
)

class ModernVoiceStudioTab(QWidget):
    """Modern Voice Studio Tab với beautiful design và full functionality"""
    
    # Signals
    script_data_updated = Signal(dict)
    character_settings_changed = Signal(str, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Real Voice Studio data - không còn demo
        self.script_data = None
        self.voice_mapping = {}
        self.character_configs = {}  # Store emotion parameters per character
        self.output_directory = "./voice_studio_output"
        self.emotions_config = self.load_emotions_config()
        self.current_mode = "none"  # "simple", "complex", or "none"
        self.single_emotion_config = {'emotion': 'neutral', 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.0, 'temperature': 0.8}
        
        self.setup_ui()
        self.setup_connections()
        
        # Initialize with real status
        self.add_log("[SYSTEM] Voice Studio initialized with real functionality")
        self.add_log("[INFO] Ready to import script and generate voices")
        self.add_log(f"[CONFIG] Loaded {len(self.emotions_config.get('emotions', {}))} emotion presets")
        
    def setup_ui(self):
        """Setup modern UI layout"""
        # Apply modern theme
        apply_modern_theme(self)
        
        # Main layout - horizontal 3-column
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)  # No spacing between columns
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        
        # COLUMN 1: Tab Header/Title (Fixed width - compact)
        tab_header_panel = self.create_tab_header_panel()
        main_layout.addWidget(tab_header_panel)
        
        # COLUMN 2 & 3: Create horizontal splitter cho main content
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {ModernColors.BORDER_DEFAULT};
                width: 2px;
            }}
        """)
        
        # COLUMN 2: Main content panel (expandable)
        main_content_panel = self.create_main_content_panel()
        content_splitter.addWidget(main_content_panel)
        
        # COLUMN 3: Progress & Logs panel (fixed ratio)  
        logs_panel = self.create_logs_panel()
        content_splitter.addWidget(logs_panel)
        
        # Set splitter sizes: 75% main content, 25% logs
        content_splitter.setSizes([750, 250])
        content_splitter.setStretchFactor(0, 3)  # Main content gets 3x stretch
        content_splitter.setStretchFactor(1, 1)  # Logs panel gets 1x stretch
        
        main_layout.addWidget(content_splitter)
    
    def create_tab_header_panel(self):
        """Tạo professional sidebar - Column 1"""
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(200)  # Slightly wider for better proportions
        sidebar_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {ModernColors.SURFACE};
                border-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App Logo/Brand Section
        brand_section = self.create_brand_section()
        sidebar_layout.addWidget(brand_section)
        
        # Navigation Tabs
        nav_section = self.create_navigation_section()
        sidebar_layout.addWidget(nav_section)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Bottom Status Section
        status_section = self.create_status_section()
        sidebar_layout.addWidget(status_section)
        
        return sidebar_widget
    
    def create_brand_section(self):
        """Tạo brand section ở top sidebar"""
        brand_widget = QWidget()
        brand_widget.setFixedHeight(60)
        brand_widget.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
            }}
        """)
        
        brand_layout = QHBoxLayout(brand_widget)
        brand_layout.setContentsMargins(16, 12, 16, 12)
        brand_layout.setSpacing(12)
        
        # App icon
        icon_label = QLabel("🎵")
        icon_label.setFixedSize(32, 32)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                qproperty-alignment: AlignCenter;
                background-color: {ModernColors.PRIMARY};
                border-radius: 16px;
            }}
        """)
        brand_layout.addWidget(icon_label)
        
        # App name
        app_name = QLabel("Voice Studio")
        app_name.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {ModernColors.TEXT_PRIMARY};
            }}
        """)
        brand_layout.addWidget(app_name)
        
        brand_layout.addStretch()
        
        return brand_widget
    
    def create_navigation_section(self):
        """Tạo navigation tabs section"""
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(8, 16, 8, 16)
        nav_layout.setSpacing(4)
        
        # Section title
        section_title = QLabel("WORKSPACE")
        section_title.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                font-weight: 600;
                color: {ModernColors.TEXT_SECONDARY};
                padding: 8px 12px;
                letter-spacing: 1px;
            }}
        """)
        nav_layout.addWidget(section_title)
        
        # Navigation items
        nav_items = [
            ("🎤", "Voice Studio", "", True),
            ("🎞️", "Video Studio", "Create AI videos", False),
            ("🔧", "Tools", "Utilities & settings", False),
            ("📊", "Analytics", "Usage & statistics", False),
        ]
        
        for icon, title, subtitle, is_active in nav_items:
            nav_item = self.create_nav_item(icon, title, subtitle, is_active)
            nav_layout.addWidget(nav_item)
        
        return nav_widget
    
    def create_nav_item(self, icon, title, subtitle, is_active=False):
        """Tạo professional navigation item"""
        nav_item = QWidget()
        nav_item.setFixedHeight(56)
        
        # Style based on active state
        if is_active:
            bg_color = ModernColors.PRIMARY_LIGHT
            text_color = ModernColors.TEXT_PRIMARY
            subtitle_color = ModernColors.TEXT_SECONDARY
            left_accent = f"""
                border-left: 3px solid {ModernColors.PRIMARY};
            """
        else:
            bg_color = "transparent"
            text_color = ModernColors.TEXT_SECONDARY
            subtitle_color = ModernColors.TEXT_TERTIARY
            left_accent = ""
        
        nav_item.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                margin: 0px 4px;
                {left_accent}
            }}
            QWidget:hover {{
                background-color: {ModernColors.SURFACE_SECONDARY};
            }}
        """)
        
        nav_layout = QHBoxLayout(nav_item)
        nav_layout.setContentsMargins(16, 8, 16, 8)
        nav_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(24, 24)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                color: {text_color};
                qproperty-alignment: AlignCenter;
            }}
        """)
        nav_layout.addWidget(icon_label)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: 500;
                color: {text_color};
                margin: 0;
                padding: 0;
            }}
        """)
        text_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: {subtitle_color};
                margin: 0;
                padding: 0;
            }}
        """)
        text_layout.addWidget(subtitle_label)
        
        nav_layout.addLayout(text_layout)
        nav_layout.addStretch()
        
        # Bỏ active indicator dot
        
        return nav_item
    
    def create_status_section(self):
        """Tạo status section ở bottom sidebar"""
        status_widget = QWidget()
        status_widget.setFixedHeight(50)
        status_widget.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
            }}
        """)
        
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(16, 12, 16, 12)
        status_layout.setSpacing(8)
        
        # Status indicator
        status_dot = QLabel("●")
        status_dot.setFixedSize(12, 12)
        status_dot.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: #a3f73e;
                qproperty-alignment: AlignCenter;
            }}
        """)
        status_layout.addWidget(status_dot)
        
        # Status text
        status_text = QLabel("Ready")
        status_text.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: 500;
                color: {ModernColors.TEXT_PRIMARY};
            }}
        """)
        status_layout.addWidget(status_text)
        
        status_layout.addStretch()
        
        # Settings icon
        settings_icon = QLabel("⚙️")
        settings_icon.setFixedSize(16, 16)
        settings_icon.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {ModernColors.TEXT_SECONDARY};
                qproperty-alignment: AlignCenter;
            }}
        """)
        status_layout.addWidget(settings_icon)
        
        return status_widget
    
    
    def create_main_content_panel(self):
        """Tạo main content panel - Column 2 (Expandable)"""
        # Đây chính là left_panel cũ
        return self.create_left_panel()
    
    def create_logs_panel(self):
        """Tạo logs panel - Column 3 (Fixed ratio)"""
        # Đây chính là right_panel cũ
        return self.create_right_panel()
    
    def create_left_panel(self):
        """Tạo left panel với main content"""
        # Scroll area for left content với border radius
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {ModernColors.SURFACE};
                border: none;
                border-radius: 0px;
            }}
        """)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(ModernSpacing.SECTION_SPACING)
        content_layout.setContentsMargins(0, 0, ModernSpacing.MARGIN_DEFAULT, 0)  # Right margin for splitter
        
        # Script Import Section (với overview gộp vào)
        import_section = self.create_import_section()
        content_layout.addWidget(import_section)
        
        # Voice Configuration Section (Main feature)
        config_section = self.create_voice_config_section()
        content_layout.addWidget(config_section)
        
        # Actions Section
        actions_section = self.create_actions_section()
        content_layout.addWidget(actions_section)
        
        # Add stretch to push content to top
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        return scroll_area
    
    def create_right_panel(self):
        """Tạo right panel với progress & results logs"""
        right_widget = QWidget()
        right_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {ModernColors.SURFACE};
                border-top-right-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
                border-bottom-right-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
            }}
        """)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        right_layout.setContentsMargins(ModernSpacing.MARGIN_DEFAULT, 0, 0, 0)  # Left margin for splitter
        
        # Progress Section
        progress_section = self.create_progress_section()
        right_layout.addWidget(progress_section)
        
        # Enhanced Results/Logs Section
        logs_section = self.create_logs_section()
        right_layout.addWidget(logs_section)
        
        return right_widget
        
    def create_import_section(self):
        """Tạo section import script data"""
        import_group = QGroupBox("📝 Import Script Data")
        import_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        import_layout = QVBoxLayout(import_group)
        import_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Import methods
        methods_layout = QHBoxLayout()
        
        # File import buttons
        self.import_json_btn = QPushButton("📁 Import JSON")
        self.import_json_btn.setStyleSheet(ModernStyles.get_button_style("success"))
        self.import_json_btn.setToolTip("Import script from JSON file")
        
        self.import_srt_btn = QPushButton("📄 Import SRT") 
        self.import_srt_btn.setStyleSheet(ModernStyles.get_button_style("secondary"))
        self.import_srt_btn.setToolTip("Import script from SRT subtitle file")
        
        self.from_video_tab_btn = QPushButton("📹 From Video Tab")
        self.from_video_tab_btn.setStyleSheet(ModernStyles.get_button_style("primary"))
        
        self.manual_json_btn = QPushButton("✏️ Manual Input")  
        self.manual_json_btn.setStyleSheet(ModernStyles.get_button_style("secondary"))
        
        methods_layout.addWidget(self.import_json_btn)
        methods_layout.addWidget(self.import_srt_btn)
        methods_layout.addWidget(self.from_video_tab_btn)
        methods_layout.addWidget(self.manual_json_btn)
        methods_layout.addStretch()
        
        import_layout.addLayout(methods_layout)
        
        # Manual input area (initially hidden)
        self.manual_input_area = QWidget()
        manual_input_layout = QVBoxLayout(self.manual_input_area)
        
        self.manual_script_input = QTextEdit()
        self.manual_script_input.setPlaceholderText("Paste your JSON script here...")
        self.manual_script_input.setMaximumHeight(80)  # Compact input area
        self.manual_script_input.setStyleSheet(ModernStyles.get_input_style())
        
        self.parse_json_btn = QPushButton("✅ Parse JSON")
        self.parse_json_btn.setStyleSheet(ModernStyles.get_button_style("success"))
        
        manual_input_layout.addWidget(self.manual_script_input)
        manual_input_layout.addWidget(self.parse_json_btn)
        
        self.manual_input_area.setVisible(False)
        import_layout.addWidget(self.manual_input_area)
        
        # Compact status info - CHỈ 2 THÔNG SỐ QUAN TRỌNG
        status_layout = QHBoxLayout()
        
        # Characters info - professional
        chars_info = QLabel("👥 Characters: No data")
        chars_info.setObjectName("characters_info")
        chars_info.setStyleSheet(f"""
            QLabel {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                font-size: {ModernTypography.FONT_SMALL}px;
                font-weight: {ModernTypography.WEIGHT_MEDIUM};
            }}
        """)
        self.characters_label = chars_info  # Keep reference
        
        # Segments info - professional
        segments_info = QLabel("📑 Segments: 0")
        segments_info.setObjectName("segments_info")
        segments_info.setStyleSheet(f"""
            QLabel {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 6px;
                padding: {ModernSpacing.PADDING_DEFAULT}px;
                font-size: {ModernTypography.FONT_SMALL}px;
                font-weight: {ModernTypography.WEIGHT_MEDIUM};
            }}
        """)
        self.segments_label = segments_info  # Keep reference
        
        # BỎ status "Ready" - không cần thiết
        
        status_layout.addWidget(chars_info)
        status_layout.addWidget(segments_info)
        status_layout.addStretch()
        
        import_layout.addLayout(status_layout)
        
        return import_group
    
    def create_voice_config_section(self):
        """Tạo section cấu hình giọng nói chi tiết - MAIN FEATURE"""
        config_group = QGroupBox("🎭 Voice Configuration (Advanced)")
        config_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Enable manual configuration
        enable_layout = QHBoxLayout()
        
        self.enable_manual_config = QCheckBox("Enable Manual Configuration")
        self.enable_manual_config.setChecked(True)  # Enabled by default
        self.enable_manual_config.setStyleSheet(f"""
            QCheckBox {{
                font-size: {ModernTypography.FONT_BODY}px;
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
            }}
        """)
        
        self.auto_emotion_mapping = QCheckBox("🎭 Auto Emotion Mapping")
        self.auto_emotion_mapping.setChecked(True)
        
        enable_layout.addWidget(self.enable_manual_config)
        enable_layout.addWidget(self.auto_emotion_mapping)
        enable_layout.addStretch()
        
        config_layout.addLayout(enable_layout)
        
        # Character settings table - BEAUTIFUL & FUNCTIONAL
        self.create_character_settings_table()
        config_layout.addWidget(self.character_settings_table)
        
        # Populate với sample data
        self.populate_sample_character_data()
        
        # Auto-adjust table height theo số rows
        self.adjust_table_height()
        
        return config_group
    
    def create_centered_widget(self, widget):
        """Tạo container widget để căn giữa widget trong table cell"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget)
        layout.setAlignment(Qt.AlignCenter)
        return container
    
    def create_character_settings_table(self):
        """Tạo bảng cấu hình chi tiết 11 cột với modern styling"""
        self.character_settings_table = QTableWidget()
        self.character_settings_table.verticalHeader().setVisible(False)
        self.character_settings_table.setColumnCount(11)
        self.character_settings_table.setHorizontalHeaderLabels([
            "Character", "Emotion", "Exaggeration", "Speed", 
            "CFG Weight", "Temperature", "Mode", "Voice/Clone", 
            "Whisper Voice", "Status", "Preview"
        ])
        # Không set fixed height - để table tự co theo số rows
        
        # Apply modern table styling với proper clipping
        self.character_settings_table.setStyleSheet(f"""
            {ModernStyles.get_table_style()}
            
            /* Ensure proper border radius clipping */
            QTableWidget {{
                border-collapse: separate;
                border-spacing: 0;
            }}
            
            /* Fix corner cells để match border radius */
            QTableWidget QTableCornerButton::section {{
                background-color: {ModernColors.SURFACE_TERTIARY};
                border: none;
                border-top-left-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
            }}
        """)
        
        # Configure column sizes
        header = self.character_settings_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Character
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Emotion
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Exaggeration
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Speed
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # CFG Weight
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Temperature
        header.setSectionResizeMode(6, QHeaderView.Interactive)  # Mode
        header.setSectionResizeMode(7, QHeaderView.Stretch)  # Voice/Clone
        header.setSectionResizeMode(8, QHeaderView.Interactive)  # Whisper Voice
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Status  
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)  # Preview
        
        # Set minimum widths
        header.setMinimumSectionSize(50)  # Reduce minimum để preview column có thể nhỏ hơn
        self.character_settings_table.setColumnWidth(0, 120)  # Character
        self.character_settings_table.setColumnWidth(6, 130)  # Mode
        self.character_settings_table.setColumnWidth(8, 150)  # Whisper Voice
        self.character_settings_table.setColumnWidth(10, 40)  # Preview - compact width
        
        # Enable alternating row colors và selection
        self.character_settings_table.setAlternatingRowColors(True)
        self.character_settings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.character_settings_table.verticalHeader().setDefaultSectionSize(40)  # Compact row height
    
    def populate_sample_character_data(self):
        """Populate bảng với dữ liệu mẫu để demo"""
        self.add_log("[DATA] Loading sample character configurations")
        sample_characters = [
            {
                "name": "Narrator", 
                "emotion": "😌 Calm",
                "exag": "1.0",
                "speed": "1.0", 
                "cfg": "0.6",
                "temp": "0.8",
                "status": "🟢 Ready"
            },
            {
                "name": "Character 1",
                "emotion": "😊 Happy", 
                "exag": "1.2",
                "speed": "1.1",
                "cfg": "0.7",
                "temp": "0.9",
                "status": "🟡 Pending"
            },
            {
                "name": "Character 2",
                "emotion": "🤔 Thoughtful",
                "exag": "0.8", 
                "speed": "0.9",
                "cfg": "0.5",
                "temp": "0.7",
                "status": "🟢 Ready"
            }
        ]
        
        self.character_settings_table.setRowCount(len(sample_characters))
        
        for i, char in enumerate(sample_characters):
            # Character name
            name_item = QTableWidgetItem(char["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.character_settings_table.setItem(i, 0, name_item)
            
            # Emotion dropdown - căn giữa trong cell
            emotion_combo = QComboBox()
            emotion_combo.addItems([
                "😊 Happy", "😢 Sad", "😠 Angry", "😌 Calm", "😰 Fearful",
                "😮 Surprised", "💝 Romantic", "🤔 Thoughtful", "🎭 Dramatic"
            ])
            emotion_combo.setCurrentText(char["emotion"])
            emotion_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 1, self.create_centered_widget(emotion_combo))
            
            # Numeric inputs với modern styling - căn giữa trong cell
            for col, key in [(2, "exag"), (3, "speed"), (4, "cfg"), (5, "temp")]:
                input_field = QLineEdit(char[key])
                input_field.setAlignment(Qt.AlignCenter)
                input_field.setStyleSheet(ModernStyles.get_table_cell_widget_style())
                self.character_settings_table.setCellWidget(i, col, self.create_centered_widget(input_field))
            
            # Mode selector - căn giữa trong cell
            mode_combo = QComboBox()
            mode_combo.addItems(["🎭 Voice Selection", "🎤 Voice Clone"])
            mode_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 6, self.create_centered_widget(mode_combo))
            
            # Voice/Clone dropdown - thay thế label bằng dropdown - căn giữa trong cell
            voice_combo = QComboBox()
            voice_combo.addItems([
                "Young Female", "Young Male", "Mature Female", "Mature Male", 
                "Child Voice", "Narrator", "Deep Male", "Gentle Female"
            ])
            voice_combo.setCurrentText("Young Female")
            voice_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 7, self.create_centered_widget(voice_combo))
            
            # Whisper voice dropdown - thay thế label bằng dropdown - căn giữa trong cell
            whisper_combo = QComboBox()
            whisper_combo.addItems([
                "Auto Detect", "English", "Vietnamese", "Chinese", "Japanese", "Korean"
            ])
            whisper_combo.setCurrentText("Auto Detect")
            whisper_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 8, self.create_centered_widget(whisper_combo))
            
            # Status - với styling đặc biệt cho status badge - căn giữa trong cell
            status_label = QLabel(char["status"])
            status_label.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 9, self.create_centered_widget(status_label))
            
            # Preview button - COMPACT SIZE - căn giữa trong cell
            preview_btn = QPushButton("▶")
            preview_btn.setFixedSize(24, 24)  # Fixed size để không tràn ra ngoài
            preview_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ModernColors.PRIMARY};
                    color: {ModernColors.SURFACE};
                    border: none;
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: bold;
                    margin: 0px;
                    padding: 0px;
                }}
                QPushButton:pressed {{
                    background-color: {ModernColors.PRIMARY_PRESSED};
                }}
            """)
            self.character_settings_table.setCellWidget(i, 10, self.create_centered_widget(preview_btn))
        
        # Adjust table height và log completion
        self.adjust_table_height()
        self.add_log(f"[DATA] Populated {len(sample_characters)} character configurations successfully")
    
    def adjust_table_height(self):
        """Tự động adjust height của table theo số rows"""
        row_count = self.character_settings_table.rowCount()
        if row_count == 0:
            self.character_settings_table.setMaximumHeight(120)  # Minimum height
            return
        
        # Calculate optimal height: header + rows + padding
        header_height = 35  # Header row height
        row_height = 40     # Each data row height  
        padding = 20        # Extra padding
        
        optimal_height = header_height + (row_count * row_height) + padding
        
        # Set reasonable limits
        min_height = 120
        max_height = 400
        
        final_height = max(min_height, min(optimal_height, max_height))
        self.character_settings_table.setMaximumHeight(final_height)
        self.character_settings_table.setMinimumHeight(final_height)
    
    def create_actions_section(self):
        """Tạo section actions - compact với tất cả buttons trong 1 hàng"""
        actions_group = QGroupBox("🚀 Actions")
        actions_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Output folder
        output_layout = QHBoxLayout()
        output_label = QLabel("📁 Output:")
        output_label.setStyleSheet(ModernStyles.get_label_style("body"))
        output_label.setMinimumWidth(60)
        
        self.output_path_input = QLineEdit("./voice_studio_output/")
        self.output_path_input.setReadOnly(True)
        self.output_path_input.setStyleSheet(ModernStyles.get_input_style())
        
        self.browse_output_btn = QPushButton("📂")
        self.browse_output_btn.setMaximumWidth(40)
        self.browse_output_btn.setStyleSheet(ModernStyles.get_button_style("secondary"))
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(self.browse_output_btn)
        
        actions_layout.addLayout(output_layout)
        
        # Tất cả buttons trong 1 hàng - DÀN ĐỀU TOÀN BỘ CHIỀU RỘNG
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        self.generate_selected_btn = QPushButton("🎤 Generate Selected")
        self.generate_selected_btn.setStyleSheet(ModernStyles.get_button_style("warning"))
        
        self.generate_all_btn = QPushButton("🎭 Generate All")
        self.generate_all_btn.setStyleSheet(ModernStyles.get_button_style("success"))
        
        self.open_output_btn = QPushButton("📂 Open Output")
        self.open_output_btn.setStyleSheet(ModernStyles.get_button_style("secondary"))
        
        self.clear_results_btn = QPushButton("🗑️ Clear Results")
        self.clear_results_btn.setStyleSheet(ModernStyles.get_button_style("error"))
        
        # Thêm buttons với equal stretch để dàn đều
        buttons_layout.addWidget(self.generate_selected_btn, 1)  # stretch = 1
        buttons_layout.addWidget(self.generate_all_btn, 1)       # stretch = 1  
        buttons_layout.addWidget(self.open_output_btn, 1)        # stretch = 1
        buttons_layout.addWidget(self.clear_results_btn, 1)      # stretch = 1
        
        # KHÔNG addStretch() ở cuối để buttons chiếm hết width
        
        actions_layout.addLayout(buttons_layout)
        
        return actions_group
    
    def create_progress_section(self):
        """Tạo section progress cho right panel"""
        progress_group = QGroupBox("📊 Progress")
        progress_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                background-color: {ModernColors.SURFACE_TERTIARY};
                height: 18px;
                text-align: center;
                font-weight: {ModernTypography.WEIGHT_SEMIBOLD};
                font-size: {ModernTypography.FONT_CAPTION}px;
            }}
            
            QProgressBar::chunk {{
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                background-color: {ModernColors.PRIMARY};
            }}
        """)
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Status text - compact cho right panel
        self.progress_text = QLabel("Ready to generate voices")
        self.progress_text.setStyleSheet(f"""
            QLabel {{
                font-size: {ModernTypography.FONT_CAPTION}px;
                color: {ModernColors.TEXT_SECONDARY};
                padding: 4px;
                background-color: {ModernColors.SURFACE_SECONDARY};
                border-radius: 4px;
            }}
        """)
        self.progress_text.setWordWrap(True)
        progress_layout.addWidget(self.progress_text)
        
        return progress_group
    
    def create_logs_section(self):
        """Tạo section logs cho right panel"""
        logs_group = QGroupBox("📝 Application Logs")
        logs_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        logs_layout = QVBoxLayout(logs_group)
        logs_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Logs text area - takes up most of right panel space
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlaceholderText("Application logs will appear here...")
        self.logs_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernColors.SURFACE};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: {ModernSpacing.BORDER_RADIUS_DEFAULT}px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: {ModernTypography.FONT_CAPTION}px;
                color: {ModernColors.TEXT_PRIMARY};
                padding: 8px;
                selection-background-color: {ModernColors.PRIMARY_LIGHT};
            }}
        """)
        logs_layout.addWidget(self.logs_text)
        
        # Logs control buttons - compact
        logs_controls = QHBoxLayout()
        
        self.clear_logs_btn = QPushButton("🗑️")
        self.clear_logs_btn.setMaximumWidth(30)
        self.clear_logs_btn.setToolTip("Clear logs")
        self.clear_logs_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 4px;
                padding: 4px;
                font-size: {ModernTypography.FONT_CAPTION}px;
            }}
        """)
        self.clear_logs_btn.clicked.connect(self.clear_logs)
        logs_controls.addWidget(self.clear_logs_btn)
        
        self.save_logs_btn = QPushButton("💾")
        self.save_logs_btn.setMaximumWidth(30)
        self.save_logs_btn.setToolTip("Save logs to file")
        self.save_logs_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 4px;
                padding: 4px;
                font-size: {ModernTypography.FONT_CAPTION}px;
            }}
        """)
        self.save_logs_btn.clicked.connect(self.save_logs)
        logs_controls.addWidget(self.save_logs_btn)
        
        logs_controls.addStretch()
        logs_layout.addLayout(logs_controls)
        
        return logs_group
    
    def setup_connections(self):
        """Setup signal connections - Real functionality"""
        # Import buttons
        self.import_json_btn.clicked.connect(self.import_script_file)  # Real import
        self.import_srt_btn.clicked.connect(self.import_srt_file)  # Keep placeholder for now
        self.from_video_tab_btn.clicked.connect(self.load_from_video_tab)
        self.manual_json_btn.clicked.connect(self.show_manual_input_dialog)  # Real dialog
        # self.manual_table_btn removed from UI
        self.parse_json_btn.clicked.connect(self.parse_manual_json)
        
        # Output settings
        self.browse_output_btn.clicked.connect(self.browse_output_folder)
        
        # Generation buttons  
        self.generate_selected_btn.clicked.connect(self.generate_voice_real)  # Real generation
        self.generate_all_btn.clicked.connect(self.generate_voice_real)       # Real generation
        
        # Results buttons
        self.open_output_btn.clicked.connect(self.open_output_folder_real)    # Real folder open
        self.clear_results_btn.clicked.connect(self.clear_results)
        
        # Configuration
        self.auto_emotion_mapping.toggled.connect(self.toggle_emotion_mapping_mode)
        
    # Placeholder methods - implement actual functionality
    def load_from_video_tab(self):
        """Load script data from video tab"""
        self.progress_text.setText("Loading from video tab...")
        self.add_log("[ACTION] Loading script data from video tab")
        
    def show_manual_json_input(self):
        """Show manual JSON input area"""
        self.manual_input_area.setVisible(True)
        self.add_log("[UI] Manual JSON input area opened")
        
    def show_manual_table_input(self):
        """Show manual table input"""
        self.progress_text.setText("Manual table input not implemented yet")
        self.add_log("[INFO] Manual table input feature not implemented")
        
    def parse_manual_json(self):
        """Parse manual JSON input"""
        json_text = self.manual_script_input.toPlainText().strip()
        if json_text:
            self.progress_text.setText("Parsing JSON...")
            self.add_log(f"[JSON] Parsing {len(json_text)} characters of JSON data")
        else:
            self.progress_text.setText("Please enter JSON data first")
            self.add_log("[WARNING] No JSON data provided for parsing")
            
    def browse_output_folder(self):
        """Browse for output folder"""
        self.progress_text.setText("Browse output folder...")
        self.add_log("[ACTION] Opening folder browser dialog")
        
    def generate_selected_voice(self):
        """Generate voice for selected character"""
        self.progress_text.setText("Generating selected voice...")
        self.progress_bar.setVisible(True)
        self.add_log("[GENERATE] Starting voice generation for selected character")
        
    def generate_all_voices(self):
        """Generate all voices với progress simulation"""
        self.progress_text.setText("Initializing voice generation...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.add_log("[GENERATE] Starting voice generation for all characters")
        
        # Simulate generation progress với QTimer
        from PySide6.QtCore import QTimer
        
        self.generation_progress = 0
        self.generation_timer = QTimer()
        self.generation_timer.timeout.connect(self.simulate_generation_progress)
        self.generation_timer.start(500)  # Update every 500ms
    
    def simulate_generation_progress(self):
        """Simulate voice generation progress với detailed logs"""
        self.generation_progress += 10
        
        # Progress stages với realistic logs
        if self.generation_progress == 10:
            self.progress_text.setText("Loading character configurations...")
            self.add_log("[PROCESS] Loading character emotion settings")
        elif self.generation_progress == 20:
            self.progress_text.setText("Preprocessing script data...")
            self.add_log("[PROCESS] Analyzing script segments and dialogue distribution")
        elif self.generation_progress == 30:
            self.progress_text.setText("Initializing TTS engine...")
            self.add_log("[ENGINE] Starting Chatterbox TTS engine")
        elif self.generation_progress == 40:
            self.progress_text.setText("Processing Narrator voice...")
            self.add_log("[VOICE] Generating audio for Narrator - 15 segments")
        elif self.generation_progress == 60:
            self.progress_text.setText("Processing Character 1 voice...")
            self.add_log("[VOICE] Generating audio for Character 1 - 8 segments")
        elif self.generation_progress == 80:
            self.progress_text.setText("Processing Character 2 voice...")
            self.add_log("[VOICE] Generating audio for Character 2 - 5 segments")
        elif self.generation_progress == 90:
            self.progress_text.setText("Merging audio segments...")
            self.add_log("[POST] Combining individual segments into final audio")
        elif self.generation_progress >= 100:
            # Generation complete
            self.generation_timer.stop()
            self.progress_bar.setValue(100)
            self.progress_text.setText("Voice generation completed!")
            self.add_log("[SUCCESS] Voice generation completed successfully")
            self.add_log("[OUTPUT] Files saved to ./voice_studio_output/")
            self.add_log("[STATS] Total processing time: 4.2 seconds")
            return
        
        self.progress_bar.setValue(self.generation_progress)
        
    def open_output_folder(self):
        """Open output folder in file manager"""
        self.progress_text.setText("Opening output folder...")
        self.add_log("[ACTION] Opening output folder in file manager")
        
    def clear_results(self):
        """Clear results and reset progress"""
        self.progress_text.setText("Ready to generate voices")
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.add_log("[SYSTEM] Results cleared, ready for new generation")
    
    def toggle_emotion_mapping_mode(self, enabled):
        """Toggle emotion mapping mode - disable/enable manual emotion controls"""
        # Khi auto emotion mapping được bật, disable 5 cột emotion controls
        for row in range(self.character_settings_table.rowCount()):
            # Columns: 1=Emotion, 2=Exaggeration, 3=Speed, 4=CFG Weight, 5=Temperature
            for col in [1, 2, 3, 4, 5]:
                container_widget = self.character_settings_table.cellWidget(row, col)
                if container_widget:
                    # Get the actual widget inside the container
                    actual_widget = container_widget.layout().itemAt(0).widget()
                    if actual_widget:
                        if enabled:
                            # Auto mode: disable + change style để indicate disabled
                            actual_widget.setEnabled(False)
                            if hasattr(actual_widget, 'setStyleSheet'):
                                actual_widget.setStyleSheet(f"""
                                    QComboBox, QLineEdit {{
                                        background-color: #f5f5f5;
                                        border: 1px solid #d0d0d0;
                                        border-radius: 6px;
                                        padding: 4px 8px;
                                        font-size: {ModernTypography.FONT_SMALL}px;
                                        height: 28px;
                                        color: #888888;
                                        margin: 0px;
                                    }}
                                """)
                        else:
                            # Manual mode: enable + restore normal style
                            actual_widget.setEnabled(True)
                            actual_widget.setStyleSheet(ModernStyles.get_table_cell_widget_style())
        
        # Update progress text
        mode = "Auto Emotion Mapping" if enabled else "Manual Configuration"
        self.progress_text.setText(f"Mode: {mode}")
        
        # Log the mode change
        self.add_log(f"[MODE] Switched to {mode}")
    
    # === REAL VOICE STUDIO FUNCTIONALITY ===
    
    def load_emotions_config(self):
        """Load emotions config file"""
        try:
            # Try to load from the same location as original tab
            import os
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'emotions.json')
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default emotions if file not found
                return {
                    "emotions": {
                        "neutral": {"exaggeration": 1.0, "cfg_weight": 0.6, "speed": 1.0, "temperature": 0.8},
                        "happy": {"exaggeration": 1.3, "cfg_weight": 0.7, "speed": 1.1, "temperature": 0.9},
                        "sad": {"exaggeration": 0.8, "cfg_weight": 0.5, "speed": 0.9, "temperature": 0.7},
                        "angry": {"exaggeration": 1.5, "cfg_weight": 0.8, "speed": 1.2, "temperature": 1.0},
                        "excited": {"exaggeration": 1.4, "cfg_weight": 0.75, "speed": 1.15, "temperature": 0.95}
                    }
                }
        except Exception as e:
            print(f"[ERROR] Failed to load emotions config: {e}")
            return {"emotions": {}}
    
    def import_script_file(self):
        """Import script from JSON file - Real functionality"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file script JSON", "", "JSON files (*.json)"
        )
        
        if file_path:
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.script_data = json.load(f)
                
                # Detect if this is a complex script (multiple characters)
                characters = set()
                for segment in self.script_data.get('segments', []):
                    for dialogue in segment.get('dialogues', []):
                        characters.add(dialogue['speaker'])
                
                if len(characters) > 1:
                    self.current_mode = "complex"
                    self.add_log(f"[IMPORT] Complex script loaded - {len(characters)} characters detected")
                else:
                    self.current_mode = "simple"
                    self.add_log(f"[IMPORT] Simple script loaded - single character")
                
                self.update_script_overview()
                self.populate_character_table()
                self.add_log(f"[SUCCESS] Script imported from: {file_path}")
                self.progress_text.setText(f"Script ready - {self.current_mode.title()} mode")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Không thể đọc file: {str(e)}")
                self.add_log(f"[ERROR] Failed to import script: {str(e)}")
    
    def update_script_overview(self):
        """Update script overview with real data"""
        if not self.script_data:
            return
            
        segments = self.script_data.get('segments', [])
        characters = set()
        total_dialogues = 0
        
        for segment in segments:
            for dialogue in segment.get('dialogues', []):
                characters.add(dialogue['speaker'])
                total_dialogues += 1
        
        # Update status display (simplified for now)
        self.add_log(f"[OVERVIEW] {len(segments)} segments, {len(characters)} characters, {total_dialogues} dialogues")
    
    def populate_character_table(self):
        """Populate character table with real script data"""
        if not self.script_data:
            return
            
        # Extract characters from script
        characters = set()
        for segment in self.script_data.get('segments', []):
            for dialogue in segment.get('dialogues', []):
                characters.add(dialogue['speaker'])
        
        characters = list(characters)
        
        # Clear existing table
        self.character_settings_table.setRowCount(0)
        
        # Add rows for each character
        for i, character in enumerate(characters):
            self.character_settings_table.insertRow(i)
            
            # Character name
            char_label = QLabel(character)
            char_label.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 0, self.create_centered_widget(char_label))
            
            # Default emotion controls
            emotion_combo = QComboBox()
            emotion_combo.addItems(list(self.emotions_config.get('emotions', {}).keys()))
            emotion_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 1, self.create_centered_widget(emotion_combo))
            
            # Exaggeration
            exag_input = QLineEdit("1.0")
            exag_input.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 2, self.create_centered_widget(exag_input))
            
            # Speed
            speed_input = QLineEdit("1.0")
            speed_input.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 3, self.create_centered_widget(speed_input))
            
            # CFG Weight
            cfg_input = QLineEdit("0.6")
            cfg_input.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 4, self.create_centered_widget(cfg_input))
            
            # Temperature
            temp_input = QLineEdit("0.8")
            temp_input.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 5, self.create_centered_widget(temp_input))
            
            # Voice/Clone dropdown
            voice_combo = QComboBox()
            voice_combo.addItems(["Select Voice", "Voice 1", "Voice 2", "Voice 3"])
            voice_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 6, self.create_centered_widget(voice_combo))
            
            # Whisper Voice dropdown  
            whisper_combo = QComboBox()
            whisper_combo.addItems(["Auto", "Whisper 1", "Whisper 2"])
            whisper_combo.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 7, self.create_centered_widget(whisper_combo))
            
            # Audio Length
            length_label = QLabel("0:00")
            length_label.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 8, self.create_centered_widget(length_label))
            
            # Status
            status_label = QLabel("Ready")
            status_label.setStyleSheet(ModernStyles.get_table_cell_widget_style())
            self.character_settings_table.setCellWidget(i, 9, self.create_centered_widget(status_label))
            
            # Preview button
            preview_btn = QPushButton("▶")
            preview_btn.setMaximumWidth(30)
            preview_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ModernColors.PRIMARY};
                    color: {ModernColors.SURFACE};
                    border: none;
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: bold;
                    margin: 0px;
                    padding: 0px;
                }}
                QPushButton:pressed {{
                    background-color: {ModernColors.PRIMARY_PRESSED};
                }}
            """)
            self.character_settings_table.setCellWidget(i, 10, self.create_centered_widget(preview_btn))
        
        # Adjust table height
        self.adjust_table_height()
        self.add_log(f"[DATA] Populated {len(characters)} character configurations")
    
    def generate_voice_real(self):
        """Real voice generation using Chatterbox Extended"""
        if not self.script_data:
            self.add_log("[ERROR] No script data loaded. Please import a script first.")
            return
            
        self.add_log("[GENERATION] Starting real voice generation...")
        self.progress_text.setText("Initializing voice generation...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        try:
            # Import real voice generation
            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration
            
            def progress_callback(current, total, message):
                progress = int((current / total) * 100)
                self.progress_bar.setValue(progress)
                self.progress_text.setText(message)
                self.add_log(f"[PROGRESS] {message} ({current}/{total})")
            
            # Initialize Chatterbox Extended
            chatterbox_extended = ChatterboxExtendedIntegration()
            
            # Start generation
            result = chatterbox_extended.generate_audio_from_script_data(
                script_data=self.script_data,
                voice_mapping=self.voice_mapping,
                output_directory=self.output_directory,
                emotion_configs=self.character_configs,
                progress_callback=progress_callback
            )
            
            if result.get("success"):
                self.add_log("[SUCCESS] Voice generation completed successfully!")
                self.progress_text.setText("Voice generation completed!")
                import os
                if os.path.exists(self.output_directory):
                    self.add_log(f"[OUTPUT] Files saved to: {self.output_directory}")
            else:
                self.add_log(f"[ERROR] Voice generation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.add_log(f"[ERROR] Voice generation failed: {str(e)}")
            self.progress_text.setText("Generation failed")
    
    def show_manual_input_dialog(self):
        """Show manual script input dialog"""
        self.add_log("[ACTION] Opening manual script input dialog")
        # For now, just show a placeholder message
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Manual Input", "Manual script input feature coming soon!")
    
    def open_output_folder_real(self):
        """Open output folder in file manager - Real implementation"""
        try:
            import subprocess
            import platform
            import os
            
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory, exist_ok=True)
                self.add_log(f"[SYSTEM] Created output directory: {self.output_directory}")
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", self.output_directory])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.output_directory])
            else:  # Linux
                subprocess.run(["xdg-open", self.output_directory])
                
            self.add_log(f"[ACTION] Opened output folder: {self.output_directory}")
            
        except Exception as e:
            self.add_log(f"[ERROR] Failed to open output folder: {str(e)}")
    
    def import_srt_file(self):
        """Import script from SRT file - Placeholder for now"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "SRT Import", "SRT import feature will be implemented soon!")
        self.add_log("[INFO] SRT import feature not yet implemented")
    
    def add_log(self, message):
        """Add message to logs với timestamp"""
        from datetime import datetime
        from PySide6.QtGui import QTextCursor
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Add to logs text area
        if hasattr(self, 'logs_text'):
            self.logs_text.append(log_entry)
            # Auto scroll to bottom
            cursor = self.logs_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.logs_text.setTextCursor(cursor)
    
    def clear_logs(self):
        """Clear all logs"""
        if hasattr(self, 'logs_text'):
            self.logs_text.clear()
            self.add_log("[SYSTEM] Logs cleared")
    
    def save_logs(self):
        """Save logs to file"""
        from PySide6.QtWidgets import QFileDialog
        from datetime import datetime
        
        if not hasattr(self, 'logs_text'):
            return
            
        # Get save location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"voice_studio_logs_{timestamp}.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Logs", 
            default_filename,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.logs_text.toPlainText())
                self.add_log(f"[SYSTEM] Logs saved to {file_path}")
            except Exception as e:
                self.add_log(f"[ERROR] Failed to save logs: {str(e)}")