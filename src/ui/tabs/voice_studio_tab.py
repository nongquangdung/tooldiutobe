from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QLineEdit, QScrollArea,
    QFrame, QCheckBox, QProgressBar, QTextEdit,
    QStackedWidget, QHeaderView, QSplitter, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont, QTextCursor
import sys
import os
from ..modern_styles import (
    ModernStyles, ModernColors, ModernSpacing, 
    ModernTypography, ModernEffects, apply_modern_theme
)
import json

class VoiceGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, script_data, voice_mapping, output_dir, emotion_configs=None):
        super().__init__()
        self.script_data = script_data
        self.voice_mapping = voice_mapping
        self.output_dir = output_dir
        self.emotion_configs = emotion_configs or {}
        
    def run(self):
        try:
            # No need for direct VoiceGenerator - using Chatterbox Extended instead
            
            def progress_callback(current, total, message):
                progress = int((current / total) * 100)
                self.progress_updated.emit(progress, message)
            
            # Use Chatterbox Extended for proper preprocessing/postprocessing flow
            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration
            chatterbox_extended = ChatterboxExtendedIntegration()
            
            result = chatterbox_extended.generate_audio_from_script_data(
                script_data=self.script_data,
                voice_mapping=self.voice_mapping,
                output_directory=self.output_dir,
                emotion_configs=self.emotion_configs,
                progress_callback=progress_callback
            )
            
            if result.get("success"):
                self.finished.emit({"success": True, "message": "Voice generation completed"})
            else:
                self.finished.emit({"success": False, "error": result.get("error", "Unknown error")})
            
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})

class VoiceStudioTab(QWidget):
    """Modern Voice Studio Tab với full functionality từ old tab + modern design"""
    
    # Signals
    script_data_updated = Signal(dict)
    character_settings_changed = Signal(str, dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        # Using Chatterbox Extended instead of direct VoiceGenerator - REAL FUNCTIONALITY
        self.script_data = None
        self.voice_mapping = {}
        self.character_configs = {}  # Store emotion parameters per character
        self.output_directory = "./voice_studio_output"
        self.emotions_config = self.load_emotions_config()
        self.current_mode = "none"  # "simple", "complex", or "none"
        self.single_emotion_config = {'emotion': 'neutral', 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.0, 'temperature': 0.8}
        
        self.setup_ui()
        self.setup_connections()
        
        # Initialize with real status - MODERN LOGGING
        self.add_log("[SYSTEM] Voice Studio initialized with full functionality")
        self.add_log("[INFO] Ready to import script and generate voices")
        self.add_log(f"[CONFIG] Loaded {len(self.emotions_config.get('emotions', {}))} emotion presets")
        print(f"[DEBUG] Emotions config loaded: {len(self.emotions_config.get('emotions', {}))} emotions")
    
    def setup_ui(self):
        """Setup modern UI layout với 3-column design"""
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
        
        # COLUMN 2: Main content panel (expandable) - OLD LEFT PANEL
        main_content_panel = self.create_left_panel()
        content_splitter.addWidget(main_content_panel)
        
        # COLUMN 3: Progress & Logs panel (fixed ratio) - OLD RIGHT PANEL + LOGS
        logs_panel = self.create_right_panel()
        content_splitter.addWidget(logs_panel)
        
        # Set splitter sizes: 75% main content, 25% logs
        content_splitter.setSizes([750, 250])
        content_splitter.setStretchFactor(0, 3)  # Main content gets 3x stretch
        content_splitter.setStretchFactor(1, 1)  # Logs panel gets 1x stretch
        
        main_layout.addWidget(content_splitter)
    
    def create_left_panel(self):
        """Create main content panel với modern styling"""
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
        
        # Voice Configuration Section (Main feature) - CHARACTER TABLE
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
        """Create right panel với progress & results logs"""
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
    
    def create_tab_header_panel(self):
        \"\"\"Tạo professional sidebar - Column 1\"\"\"
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(200)  # Slightly wider for better proportions
        sidebar_widget.setStyleSheet(f\"\"\"
            QWidget {{
                background-color: {ModernColors.SURFACE};
                border-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
            }}
        \"\"\")
        
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
        \"\"\"Tạo brand section ở top sidebar\"\"\"
        brand_widget = QWidget()
        brand_widget.setFixedHeight(60)
        brand_widget.setStyleSheet(f\"\"\"
            QWidget {{
                background-color: transparent;
            }}
        \"\"\")
        
        brand_layout = QHBoxLayout(brand_widget)
        brand_layout.setContentsMargins(16, 12, 16, 12)
        brand_layout.setSpacing(12)
        
        # App icon
        icon_label = QLabel(\"🎵\")
        icon_label.setFixedSize(32, 32)
        icon_label.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 24px;
                qproperty-alignment: AlignCenter;
                background-color: {ModernColors.PRIMARY};
                border-radius: 16px;
            }}
        \"\"\")
        brand_layout.addWidget(icon_label)
        
        # App name
        app_name = QLabel(\"Voice Studio\")
        app_name.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {ModernColors.TEXT_PRIMARY};
            }}
        \"\"\")
        brand_layout.addWidget(app_name)
        
        brand_layout.addStretch()
        
        return brand_widget
    
    def create_navigation_section(self):
        \"\"\"Tạo navigation tabs section\"\"\"
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(8, 16, 8, 16)
        nav_layout.setSpacing(4)
        
        # Section title
        section_title = QLabel(\"WORKSPACE\")
        section_title.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 10px;
                font-weight: 600;
                color: {ModernColors.TEXT_SECONDARY};
                padding: 8px 12px;
                letter-spacing: 1px;
            }}
        \"\"\")
        nav_layout.addWidget(section_title)
        
        # Navigation items
        nav_items = [
            (\"🎤\", \"Voice Studio\", \"\", True),
            (\"🎞️\", \"Video Studio\", \"Create AI videos\", False),
            (\"🔧\", \"Tools\", \"Utilities & settings\", False),
            (\"📊\", \"Analytics\", \"Usage & statistics\", False),
        ]
        
        for icon, title, subtitle, is_active in nav_items:
            nav_item = self.create_nav_item(icon, title, subtitle, is_active)
            nav_layout.addWidget(nav_item)
        
        return nav_widget
    
    def create_nav_item(self, icon, title, subtitle, is_active=False):
        \"\"\"Tạo professional navigation item\"\"\"
        nav_item = QWidget()
        nav_item.setFixedHeight(56)
        
        # Style based on active state
        if is_active:
            bg_color = ModernColors.PRIMARY_LIGHT
            text_color = ModernColors.TEXT_PRIMARY
            subtitle_color = ModernColors.TEXT_SECONDARY
            left_accent = f\"\"\"
                border-left: 3px solid {ModernColors.PRIMARY};
            \"\"\"
        else:
            bg_color = \"transparent\"
            text_color = ModernColors.TEXT_SECONDARY
            subtitle_color = ModernColors.TEXT_TERTIARY
            left_accent = \"\"
        
        nav_item.setStyleSheet(f\"\"\"
            QWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                margin: 0px 4px;
                {left_accent}
            }}
            QWidget:hover {{
                background-color: {ModernColors.SURFACE_SECONDARY};
            }}
        \"\"\")
        
        nav_layout = QHBoxLayout(nav_item)
        nav_layout.setContentsMargins(16, 8, 16, 8)
        nav_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(24, 24)
        icon_label.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 18px;
                color: {text_color};
                qproperty-alignment: AlignCenter;
            }}
        \"\"\")
        nav_layout.addWidget(icon_label)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 13px;
                font-weight: 500;
                color: {text_color};
                margin: 0;
                padding: 0;
            }}
        \"\"\")
        text_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 10px;
                color: {subtitle_color};
                margin: 0;
                padding: 0;
            }}
        \"\"\")
        text_layout.addWidget(subtitle_label)
        
        nav_layout.addLayout(text_layout)
        nav_layout.addStretch()
        
        return nav_item
    
    def create_status_section(self):
        \"\"\"Tạo status section ở bottom sidebar\"\"\"
        status_widget = QWidget()
        status_widget.setFixedHeight(50)
        status_widget.setStyleSheet(f\"\"\"
            QWidget {{
                background-color: transparent;
            }}
        \"\"\")
        
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(16, 12, 16, 12)
        status_layout.setSpacing(8)
        
        # Status indicator
        status_dot = QLabel(\"●\")
        status_dot.setFixedSize(12, 12)
        status_dot.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 10px;
                color: #a3f73e;
                qproperty-alignment: AlignCenter;
            }}
        \"\"\")
        status_layout.addWidget(status_dot)
        
        # Status text
        status_text = QLabel(\"Ready\")
        status_text.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 11px;
                font-weight: 500;
                color: {ModernColors.TEXT_PRIMARY};
            }}
        \"\"\")
        status_layout.addWidget(status_text)
        
        status_layout.addStretch()
        
        # Settings icon
        settings_icon = QLabel(\"⚙️\")
        settings_icon.setFixedSize(16, 16)
        settings_icon.setStyleSheet(f\"\"\"
            QLabel {{
                font-size: 12px;
                color: {ModernColors.TEXT_SECONDARY};
                qproperty-alignment: AlignCenter;
            }}
        \"\"\")
        status_layout.addWidget(settings_icon)
        
        return status_widget
    
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
        
        # Initialize with empty table
        self.adjust_table_height()
        
        return config_group
    
    def create_character_settings_table(self):
        \"\"\"T\u1ea1o b\u1ea3ng c\u1ea5u h\u00ecnh chi ti\u1ebft 11 c\u1ed9t v\u1edbi modern styling\"\"\"
        self.character_settings_table = QTableWidget()
        self.character_settings_table.verticalHeader().setVisible(False)
        self.character_settings_table.setColumnCount(11)
        self.character_settings_table.setHorizontalHeaderLabels([
            \"Character\", \"Emotion\", \"Exaggeration\", \"Speed\", 
            \"CFG Weight\", \"Temperature\", \"Mode\", \"Voice/Clone\", 
            \"Whisper Voice\", \"Status\", \"Preview\"
        ])
        
        # Apply modern table styling v\u1edbi proper clipping
        self.character_settings_table.setStyleSheet(f\"\"\"
            {ModernStyles.get_table_style()}
            
            /* Ensure proper border radius clipping */
            QTableWidget {{
                border-collapse: separate;
                border-spacing: 0;
            }}
            
            /* Fix corner cells \u0111\u1ec3 match border radius */
            QTableWidget QTableCornerButton::section {{
                background-color: {ModernColors.SURFACE_TERTIARY};
                border: none;
                border-top-left-radius: {ModernSpacing.BORDER_RADIUS_LARGE}px;
            }}
        \"\"\")\n        
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
        header.setMinimumSectionSize(50)  # Reduce minimum \u0111\u1ec3 preview column c\u00f3 th\u1ec3 nh\u1ecf h\u01a1n
        self.character_settings_table.setColumnWidth(0, 120)  # Character
        self.character_settings_table.setColumnWidth(6, 130)  # Mode
        self.character_settings_table.setColumnWidth(8, 150)  # Whisper Voice
        self.character_settings_table.setColumnWidth(10, 40)  # Preview - compact width
        
        # Enable alternating row colors v\u00e0 selection
        self.character_settings_table.setAlternatingRowColors(True)
        self.character_settings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.character_settings_table.verticalHeader().setDefaultSectionSize(40)  # Compact row height
    
    def create_centered_widget(self, widget):
        \"\"\"T\u1ea1o container widget \u0111\u1ec3 c\u0103n gi\u1eefa widget trong table cell\"\"\"
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget)
        layout.setAlignment(Qt.AlignCenter)
        return container
    
    def adjust_table_height(self):
        \"\"\"T\u1ef1 \u0111\u1ed9ng adjust height c\u1ee7a table theo s\u1ed1 rows\"\"\"
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
    
    def create_tts_configuration_section(self):
        """③ TTS Configuration Section"""
        group = QGroupBox("③ Cấu hình TTS (Chatterbox)")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['primary']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Voice selection
        voice_layout = QFormLayout()
        self.voice_combo = QComboBox()
        self.update_voice_list()
        self.voice_combo.setStyleSheet(INPUT_STYLE)
        voice_layout.addRow("Giọng nói chính:", self.voice_combo)
        
        layout.addLayout(voice_layout)
        
        # Configuration checkboxes
        self.auto_emotion_cb = QCheckBox("[THEATER] Tự điều chỉnh cảm xúc")
        self.auto_emotion_cb.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
        self.auto_emotion_cb.setChecked(True)
        layout.addWidget(self.auto_emotion_cb)
        
        self.detailed_config_cb = QCheckBox("[CONFIG] Cấu hình chi tiết")
        self.detailed_config_cb.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
        layout.addWidget(self.detailed_config_cb)
        
        # Advanced controls (initially hidden)
        self.advanced_controls = QWidget()
        advanced_layout = QGridLayout(self.advanced_controls)
        
        # Speed control
        advanced_layout.addWidget(QLabel("Tốc độ:"), 0, 0)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        advanced_layout.addWidget(self.speed_slider, 0, 1)
        self.speed_label = QLabel("1.0x")
        self.speed_label.setStyleSheet(LABEL_STYLE)
        advanced_layout.addWidget(self.speed_label, 0, 2)
        
        # Emotion intensity
        advanced_layout.addWidget(QLabel("Cường độ cảm xúc:"), 1, 0)
        self.emotion_slider = QSlider(Qt.Horizontal)
        self.emotion_slider.setRange(0, 200)
        self.emotion_slider.setValue(100)
        advanced_layout.addWidget(self.emotion_slider, 1, 1)
        self.emotion_label = QLabel("1.0x")
        self.emotion_label.setStyleSheet(LABEL_STYLE)
        advanced_layout.addWidget(self.emotion_label, 1, 2)
        
        self.advanced_controls.setVisible(False)
        layout.addWidget(self.advanced_controls)
        
        return group
    
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
        
        actions_layout.addLayout(buttons_layout)
        
        return actions_group
    
    def create_character_config_section(self):
        """④ Character Configuration Section"""
        group = QGroupBox("④ Cấu hình Nhân vật & Emotion")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['warning']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Character configuration table  
        self.character_table = QTableWidget()
        self.character_table.setColumnCount(5)  # Character, Emotion, Exaggeration, CFG, Speed
        self.character_table.setHorizontalHeaderLabels([
            "Nhân vật", "Emotion", "Exaggeration", "CFG", "Speed"
        ])
        
        # Set table properties
        header = self.character_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setDefaultSectionSize(100)
        self.character_table.setAlternatingRowColors(True)
        self.character_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.character_table.setMaximumHeight(200)
        
        # Style the table
        self.character_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['background']};
                alternate-background-color: {COLORS['surface']};
                selection-background-color: {COLORS['primary']};
                gridline-color: {COLORS['border']};
                border: 1px solid {COLORS['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QHeaderView::section {{
                background-color: {COLORS['surface']};
                color: {COLORS['text_primary']};
                padding: 8px;
                border: 1px solid {COLORS['border']};
                font-weight: bold;
            }}
        """)
        
        layout.addWidget(self.character_table)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.auto_fill_btn = QPushButton("[REFRESH] Tự động điền")
        self.auto_fill_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        button_layout.addWidget(self.auto_fill_btn)
        
        self.reset_emotions_btn = QPushButton("[CONFIG] Reset Emotions")
        self.reset_emotions_btn.setStyleSheet(BUTTON_STYLE)
        button_layout.addWidget(self.reset_emotions_btn)
        
        layout.addLayout(button_layout)
        
        return group
    
    def create_simple_emotion_section(self):
        """Single emotion configuration for Simple mode"""
        group = QGroupBox("④ Emotion Configuration (Single Voice)")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['success']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # Single emotion dropdown
        self.single_emotion_combo = QComboBox()
        # Ensure emotions_config is loaded
        if self.emotions_config and 'emotions' in self.emotions_config:
            emotions = ['neutral'] + sorted(self.emotions_config.get('emotions', {}).keys())
        else:
            emotions = ['neutral', 'happy', 'sad', 'angry']  # Fallback
        self.single_emotion_combo.addItems(emotions)
        self.single_emotion_combo.setCurrentText('neutral')
        self.single_emotion_combo.setStyleSheet(INPUT_STYLE)
        self.single_emotion_combo.currentTextChanged.connect(self.on_single_emotion_changed)
        layout.addRow("Emotion:", self.single_emotion_combo)
        
        # Parameters (editable)
        self.single_exag_spin = QSpinBox()
        self.single_exag_spin.setRange(50, 200)  # 0.5 to 2.0 (scaled by 100)
        self.single_exag_spin.setValue(100)  # Default 1.0
        self.single_exag_spin.setSuffix("%")
        self.single_exag_spin.setStyleSheet(INPUT_STYLE)
        layout.addRow("Exaggeration:", self.single_exag_spin)
        
        self.single_cfg_spin = QSpinBox()
        self.single_cfg_spin.setRange(10, 100)  # 0.1 to 1.0 (scaled by 100)
        self.single_cfg_spin.setValue(60)  # Default 0.6
        self.single_cfg_spin.setSuffix("%")
        self.single_cfg_spin.setStyleSheet(INPUT_STYLE)
        layout.addRow("CFG Weight:", self.single_cfg_spin)
        
        self.single_speed_spin = QSpinBox()
        self.single_speed_spin.setRange(50, 200)  # 0.5 to 2.0 (scaled by 100)
        self.single_speed_spin.setValue(100)  # Default 1.0
        self.single_speed_spin.setSuffix("%")
        self.single_speed_spin.setStyleSheet(INPUT_STYLE)
        layout.addRow("Speed:", self.single_speed_spin)
        
        # Connect spin boxes to update config
        self.single_exag_spin.valueChanged.connect(self.update_single_emotion_config)
        self.single_cfg_spin.valueChanged.connect(self.update_single_emotion_config)
        self.single_speed_spin.valueChanged.connect(self.update_single_emotion_config)
        
        return group
    
    def create_script_overview_section(self):
        """⑥ Script Overview Section"""
        group = QGroupBox("⑤ Tổng Quan Script")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['primary']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(6)
        
        # Overview labels
        self.segments_label = QLabel("0")
        self.segments_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold;")
        layout.addRow("Số đoạn:", self.segments_label)
        
        self.characters_label = QLabel("0")
        self.characters_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold;")
        layout.addRow("Nhân vật:", self.characters_label)
        
        self.dialogues_label = QLabel("0")
        self.dialogues_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold;")
        layout.addRow("Tổng dialogue:", self.dialogues_label)
        
        self.status_label = QLabel("Chưa có script")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-style: italic;")
        layout.addRow("Trạng thái:", self.status_label)
        
        return group
    
    def create_token_stats_section(self):
        """⑥ Token Statistics Section"""
        group = QGroupBox("⑥ Thống kê Token")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['success']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Token savings display
        savings_layout = QHBoxLayout()
        savings_layout.addWidget(QLabel("[EMOJI] Token tiết kiệm:"))
        self.savings_label = QLabel("0 tokens")
        self.savings_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        savings_layout.addWidget(self.savings_label)
        savings_layout.addStretch()
        layout.addLayout(savings_layout)
        
        # Request form button
        self.request_form_btn = QPushButton("[EDIT] Tạo AI Request Form")
        self.request_form_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        layout.addWidget(self.request_form_btn)
        
        return group
    
    def create_progress_section(self):
        """Tạo section progress cho right panel"""
        progress_group = QGroupBox("📈 Progress")
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
        \"\"\"T\u1ea1o section logs cho right panel\"\"\"
        logs_group = QGroupBox(\"\ud83d\udcdd Application Logs\")
        logs_group.setStyleSheet(ModernStyles.get_groupbox_style())
        
        logs_layout = QVBoxLayout(logs_group) 
        logs_layout.setSpacing(ModernSpacing.LAYOUT_SPACING)
        
        # Logs text area - takes up most of right panel space
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlaceholderText(\"Application logs will appear here...\")
        self.logs_text.setStyleSheet(f\"\"\"
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
        \"\"\")
        logs_layout.addWidget(self.logs_text)
        
        # Logs control buttons - compact
        logs_controls = QHBoxLayout()
        
        self.clear_logs_btn = QPushButton(\"\ud83d\uddd1\ufe0f\")
        self.clear_logs_btn.setMaximumWidth(30)
        self.clear_logs_btn.setToolTip(\"Clear logs\")
        self.clear_logs_btn.setStyleSheet(f\"\"\"
            QPushButton {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 4px;
                padding: 4px;
                font-size: {ModernTypography.FONT_CAPTION}px;
            }}
        \"\"\")
        self.clear_logs_btn.clicked.connect(self.clear_logs)
        logs_controls.addWidget(self.clear_logs_btn)
        
        self.save_logs_btn = QPushButton(\"\ud83d\udcbe\")
        self.save_logs_btn.setMaximumWidth(30)
        self.save_logs_btn.setToolTip(\"Save logs to file\")
        self.save_logs_btn.setStyleSheet(f\"\"\"
            QPushButton {{
                background-color: {ModernColors.SURFACE_SECONDARY};
                border: 1px solid {ModernColors.BORDER_DEFAULT};
                border-radius: 4px;
                padding: 4px;
                font-size: {ModernTypography.FONT_CAPTION}px;
            }}
        \"\"\")
        self.save_logs_btn.clicked.connect(self.save_logs)
        logs_controls.addWidget(self.save_logs_btn)
        
        logs_controls.addStretch()
        logs_layout.addLayout(logs_controls)
        
        return logs_group
    
    def create_results_section(self):
        """⑧ Results & Actions Section"""
        group = QGroupBox("⑧ Kết quả & Thao tác")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {COLORS['surface']};
            }}
            QGroupBox::title {{
                color: {COLORS['primary']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Results info
        self.results_label = QLabel("Chưa có kết quả")
        self.results_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(self.results_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("[DELETE] Clear")
        self.clear_btn.setStyleSheet(BUTTON_STYLE)
        button_layout.addWidget(self.clear_btn)
        
        self.delete_btn = QPushButton("[EMOJI] Delete")
        self.delete_btn.setStyleSheet(DANGER_BUTTON_STYLE)
        button_layout.addWidget(self.delete_btn)
        
        self.merge_btn = QPushButton("[EMOJI] Merge")
        self.merge_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        button_layout.addWidget(self.merge_btn)
        
        layout.addLayout(button_layout)
        
        # Open output folder button
        self.open_folder_btn = QPushButton("[FOLDER] Mở thư mục kết quả")
        self.open_folder_btn.setStyleSheet(BUTTON_STYLE)
        layout.addWidget(self.open_folder_btn)
        
        return group
    
    def load_emotions_config(self):
        """Load emotions config file"""
        try:
            # Try to load from the same location as original tab
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'emotions', 'unified_emotions.json')
            if os.path.exists(config_path):
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
    
    def setup_connections(self):
        """Setup signal connections - Real functionality"""
        # Import buttons
        self.import_json_btn.clicked.connect(self.import_script_file)  # Real import
        self.import_srt_btn.clicked.connect(self.import_srt_file)  # Keep placeholder for now
        self.from_video_tab_btn.clicked.connect(self.load_from_video_tab)
        self.manual_json_btn.clicked.connect(self.show_manual_input_dialog)  # Real dialog
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
    
    def update_voice_list(self):
        """Update voice list from available voices"""
        try:
            voices = self.voice_generator.get_available_voices("chatterbox")
            self.voice_combo.clear()
            
            for voice_id, voice_info in voices.items():
                display_name = f"{voice_info['name']} ({voice_info['gender']})"
                self.voice_combo.addItem(display_name, voice_id)
                
            if not voices:
                self.voice_combo.addItem("Không có giọng nói", None)
                
        except Exception as e:
            print(f"Error updating voice list: {e}")
            self.voice_combo.addItem("Error tải giọng nói", None)
    
    def toggle_advanced_controls(self, checked):
        """Toggle advanced controls visibility"""
        self.advanced_controls.setVisible(checked)
    
    def import_script_file(self):
        """Import script from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file script JSON", "", "JSON files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.script_data = json.load(f)
                
                # Detect if this is a complex script (multiple characters)
                characters = set()
                for segment in self.script_data.get('segments', []):
                    for dialogue in segment.get('dialogues', []):
                        characters.add(dialogue['speaker'])
                
                if len(characters) > 1:
                    self.switch_to_mode("complex")
                else:
                    self.switch_to_mode("simple")
                
                self.update_script_overview()
                self.script_preview.setText(f"[OK] Đã tải script từ: {file_path}")
                self.status_label.setText(f"Script đã sẵn sàng - {self.current_mode.title()} mode")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Không thể đọc file: {str(e)}")
    
    def show_manual_input_dialog(self):
        """Show manual script input dialog - switches to Simple mode"""
        # Store current emotion settings before switching
        current_emotion_settings = None
        if hasattr(self, 'single_emotion_combo') and hasattr(self, 'single_exag_spin'):
            current_emotion_settings = {
                'emotion': self.single_emotion_combo.currentText(),
                'exag': self.single_exag_spin.value(),
                'cfg': self.single_cfg_spin.value(),
                'speed': self.single_speed_spin.value()
            }
            print(f"[DEBUG] Storing current emotion settings: {current_emotion_settings}")
        
        # Switch to simple mode for manual text input
        self.switch_to_mode("simple")
        
        # Restore emotion settings if they existed
        if current_emotion_settings and hasattr(self, 'single_emotion_combo'):
            self.single_emotion_combo.setCurrentText(current_emotion_settings['emotion'])
            self.single_exag_spin.setValue(current_emotion_settings['exag'])
            self.single_cfg_spin.setValue(current_emotion_settings['cfg'])
            self.single_speed_spin.setValue(current_emotion_settings['speed'])
            print(f"[DEBUG] Restored emotion settings: {current_emotion_settings}")
        
        # Clear any existing script data
        self.script_data = None
        self.script_preview.setText("[INFO] Chế độ nhập thủ công - Sử dụng 1 emotion cho toàn bộ text")
        self.status_label.setText("Chế độ Simple - Ready")
        
        # Update overview for simple mode
        self.segments_label.setText("1")
        self.characters_label.setText("1")
        self.dialogues_label.setText("1")
        
        QMessageBox.information(self, "Simple Mode", "Chế độ Simple đã được kích hoạt.\n\nCấu hình emotion ở bên dưới, sau đó click Generate Voice.")
    
    def update_script_overview(self):
        """Update script overview information"""
        if not self.script_data:
            return
        
        segments = self.script_data.get('segments', [])
        characters = self.script_data.get('characters', [])
        
        total_dialogues = sum(len(seg.get('dialogues', [])) for seg in segments)
        
        self.segments_label.setText(str(len(segments)))
        self.characters_label.setText(str(len(characters)))
        self.dialogues_label.setText(str(total_dialogues))
        
        # Calculate estimated tokens saved
        estimated_tokens = len(segments) * 50  # Rough estimate
        self.savings_label.setText(f"{estimated_tokens} tokens")
        
        # Update character table when script changes (only in complex mode)
        if self.current_mode == "complex":
            self.update_character_table()
    
    def start_voice_generation(self):
        """Start voice generation process"""
        if not self.script_data:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng import script trước")
            return
        
        # Prepare voice mapping
        default_voice = self.voice_combo.currentData()
        if not default_voice:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn giọng nói")
            return
        
        # Extract actual speaker names from script dialogues
        speakers_in_script = set()
        for segment in self.script_data.get('segments', []):
            for dialogue in segment.get('dialogues', []):
                speakers_in_script.add(dialogue['speaker'])
        
        # Create voice mapping for actual speakers (all using selected voice for now)
        self.voice_mapping = {speaker: default_voice for speaker in speakers_in_script}
        print(f"[VOICE STUDIO DEBUG] Created voice_mapping from actual speakers: {self.voice_mapping}")
        
        # Pass emotion configurations based on current mode
        if self.current_mode == "simple":
            # For simple mode, use single emotion config
            emotion_configs = {'default': self.single_emotion_config}
            print(f"[SIMPLE MODE CONFIGS] {emotion_configs}")
        else:
            # For complex mode, use character table configs
            emotion_configs = self.get_character_emotion_configs()
            print(f"[COMPLEX MODE CONFIGS] {emotion_configs}")
        
        # Start generation thread with emotion configs
        self.generation_thread = VoiceGenerationThread(
            self.script_data, self.voice_mapping, self.output_directory, emotion_configs
        )
        self.generation_thread.progress_updated.connect(self.update_progress)
        self.generation_thread.finished.connect(self.generation_finished)
        
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("[REFRESH] Đang tạo...")
        self.generation_thread.start()
    
    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.progress_status.setText(message)
    
    def generation_finished(self, result):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("[MIC] Tạo Voice")
        
        if result.get('success'):
            self.progress_status.setText("[OK] Hoàn thành")
            self.results_label.setText("Voice generation thành công!")
            QMessageBox.information(self, "Thành công", "Tạo voice hoàn tất!")
        else:
            self.progress_status.setText("[EMOJI] Error")
            error_msg = result.get('error', 'Unknown error')
            QMessageBox.critical(self, "Error", f"Tạo voice thất bại:\n{error_msg}")
    
    def preview_voice(self):
        """Preview voice with current settings"""
        QMessageBox.information(self, "Preview", "Tính năng preview sẽ được triển khai")
    
    def show_voice_settings(self):
        """Show voice settings dialog"""
        QMessageBox.information(self, "Cài đặt", "Dialog cài đặt voice sẽ được triển khai")
    
    def generate_ai_request_form(self):
        """Generate AI request form"""
        QMessageBox.information(self, "AI Request", "Tính năng tạo AI request form sẽ được triển khai")
    
    def clear_results(self):
        """Clear results display"""
        self.results_label.setText("Đã xóa kết quả")
        self.progress_bar.setValue(0)
        self.progress_status.setText("Sẵn sàng")
    
    def delete_output_files(self):
        """Delete output files"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa tất cả file output?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Thông báo", "Tính năng xóa file sẽ được triển khai")
    
    def merge_audio_files(self):
        """Merge generated audio files"""
        QMessageBox.information(self, "Merge", "Tính năng merge audio sẽ được triển khai")
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        import subprocess
        import platform
        
        try:
        def update_character_table(self):
        """Update character table based on script data"""
        if not self.script_data:
            self.character_table.setRowCount(0)
            return
        
        # Extract unique speakers from script
        speakers = set()
        for segment in self.script_data.get('segments', []):
            for dialogue in segment.get('dialogues', []):
                speakers.add(dialogue['speaker'])
        
        # Setup table rows
        self.character_table.setRowCount(len(speakers))
        
        emotions = list(self.emotions_config.get('emotions', {}).keys())
        
        for row, speaker in enumerate(sorted(speakers)):
            # Character name (read-only)
            char_item = QTableWidgetItem(speaker)
            char_item.setFlags(char_item.flags() & ~Qt.ItemIsEditable)
            self.character_table.setItem(row, 0, char_item)
            
            # Emotion dropdown
            emotion_combo = QComboBox()
            emotion_combo.addItems(['neutral'] + sorted(emotions))
            emotion_combo.setCurrentText('neutral')
            emotion_combo.currentTextChanged.connect(lambda emotion, r=row: self.on_emotion_changed(r, emotion))
            self.character_table.setCellWidget(row, 1, emotion_combo)
            
            # Default neutral parameters
            default_emotion = self.emotions_config.get('emotions', {}).get('neutral', {})
            
            # Exaggeration (editable)
            exag_item = QTableWidgetItem(str(default_emotion.get('exaggeration', 1.0)))
            self.character_table.setItem(row, 2, exag_item)
            
            # CFG (editable)
            cfg_item = QTableWidgetItem(str(default_emotion.get('cfg_weight', 0.6)))
            self.character_table.setItem(row, 3, cfg_item)
            
            # Speed (editable)
            speed_item = QTableWidgetItem(str(default_emotion.get('speed', 1.0)))
            self.character_table.setItem(row, 4, speed_item)
            
            # Store config for this character
            self.character_configs[speaker] = {
                'emotion': 'neutral',
                'exaggeration': default_emotion.get('exaggeration', 1.0),
                'cfg_weight': default_emotion.get('cfg_weight', 0.6),
                'speed': default_emotion.get('speed', 1.0),
                'temperature': default_emotion.get('temperature', 0.8)
            }
    
    def on_emotion_changed(self, row, emotion_name):
        """Handle emotion selection change - auto-fill parameters"""
        if emotion_name not in self.emotions_config.get('emotions', {}):
            return
        
        emotion_config = self.emotions_config['emotions'][emotion_name]
        
        # Get character name
        char_item = self.character_table.item(row, 0)
        if not char_item:
            return
        character = char_item.text()
        
        # Update table cells with emotion parameters
        self.character_table.item(row, 2).setText(str(emotion_config.get('exaggeration', 1.0)))
        self.character_table.item(row, 3).setText(str(emotion_config.get('cfg_weight', 0.6)))
        self.character_table.item(row, 4).setText(str(emotion_config.get('speed', 1.0)))
        
        # Update character config storage
        self.character_configs[character] = {
            'emotion': emotion_name,
            'exaggeration': emotion_config.get('exaggeration', 1.0),
            'cfg_weight': emotion_config.get('cfg_weight', 0.6),
            'speed': emotion_config.get('speed', 1.0),
            'temperature': emotion_config.get('temperature', 0.8)
        }
        
        print(f"[EMOTION AUTO-FILL] {character}: {emotion_name} -> exag={emotion_config.get('exaggeration')}, cfg={emotion_config.get('cfg_weight')}, speed={emotion_config.get('speed')}")
    
    def on_cell_changed(self, row, column):
        """Handle manual cell editing - update character config"""
        if column < 2:  # Skip character name and emotion dropdown
            return
            
        char_item = self.character_table.item(row, 0)
        if not char_item:
            return
        character = char_item.text()
        
        if character not in self.character_configs:
            self.character_configs[character] = {}
        
        try:
            value = float(self.character_table.item(row, column).text())
            
            if column == 2:  # Exaggeration
                self.character_configs[character]['exaggeration'] = value
            elif column == 3:  # CFG
                self.character_configs[character]['cfg_weight'] = value
            elif column == 4:  # Speed
                self.character_configs[character]['speed'] = value
                
            print(f"[MANUAL EDIT] {character}: column {column} = {value}")
        except ValueError:
            # Reset to previous valid value if invalid input
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number")
    
    def auto_fill_character_table(self):
        """Auto-fill all characters with recommended emotion settings"""
        if not self.script_data:
            QMessageBox.information(self, "No Script", "Please import a script first")
            return
        
        # Simple auto-assignment logic
        emotion_suggestions = {
            'narrator': 'neutral',
            'character1': 'friendly', 
            'character2': 'confident',
            'character3': 'cheerful'
        }
        
        for row in range(self.character_table.rowCount()):
            char_item = self.character_table.item(row, 0)
            if not char_item:
                continue
                
            character = char_item.text().lower()
            suggested_emotion = emotion_suggestions.get(character, 'happy')
            
            # Set emotion in dropdown
            emotion_combo = self.character_table.cellWidget(row, 1)
            if emotion_combo and suggested_emotion in [emotion_combo.itemText(i) for i in range(emotion_combo.count())]:
                emotion_combo.setCurrentText(suggested_emotion)
        
        QMessageBox.information(self, "Auto-fill Complete", "Đã tự động điền emotion cho các nhân vật")
    
    def reset_all_emotions_to_neutral(self):
        """Reset all character emotions to neutral"""
        for row in range(self.character_table.rowCount()):
            emotion_combo = self.character_table.cellWidget(row, 1)
            if emotion_combo:
                emotion_combo.setCurrentText('neutral')
        
        QMessageBox.information(self, "Reset Complete", "Đã reset tất cả emotion về neutral")
    
    def get_character_emotion_configs(self):
        """Get current emotion configurations for all characters"""
        configs = {}
        
        for row in range(self.character_table.rowCount()):
            char_item = self.character_table.item(row, 0)
            if not char_item:
                continue
                
            character = char_item.text()
            emotion_combo = self.character_table.cellWidget(row, 1)
            
            if emotion_combo:
                emotion = emotion_combo.currentText()
                exag_item = self.character_table.item(row, 2)
                cfg_item = self.character_table.item(row, 3)
                speed_item = self.character_table.item(row, 4)
                
                try:
                    configs[character] = {
                        'emotion': emotion,
                        'exaggeration': float(exag_item.text()) if exag_item else 1.0,
                        'cfg_weight': float(cfg_item.text()) if cfg_item else 0.6,
                        'speed': float(speed_item.text()) if speed_item else 1.0,
                        'temperature': self.character_configs.get(character, {}).get('temperature', 0.8)
                    }
                except (ValueError, AttributeError):
                    # Fallback to neutral if parsing fails
                    configs[character] = {
                        'emotion': 'neutral',
                        'exaggeration': 1.0,
                        'cfg_weight': 0.6,
                        'speed': 1.0,
                        'temperature': 0.8
                    }
        
        return configs
    
    def populate_available_voices(self):
        """Load available voices for the main voice dropdown"""
        try:
            # This would normally load from voice library
            # For now, using common voice names
            voices = [
                ('abigail', 'Abigail'),
                ('alexander', 'Alexander'), 
                ('anna', 'Anna'),
                ('brian', 'Brian'),
                ('emma', 'Emma')
            ]
            
            self.voice_combo.clear()
            for voice_id, voice_name in voices:
                self.voice_combo.addItem(voice_name, voice_id)
                
        except Exception as e:
            print(f"[VOICE LOADING ERROR] {e}")
    
    def switch_to_mode(self, mode):
        """Switch between Simple and Complex modes"""
        self.current_mode = mode
        
        if mode == "simple":
            # Show simple emotion config, hide character table
            self.simple_emotion_group.setVisible(True)
            self.character_group.setVisible(False)
            print("[MODE] Switched to Simple mode - single emotion config")
            
            # Only trigger initial emotion load if spin boxes are at default values
            if hasattr(self, 'single_emotion_combo') and hasattr(self, 'single_exag_spin'):
                # Check if values are still at default (user hasn't customized)
                is_default_values = (
                    self.single_exag_spin.value() == 100 and
                    self.single_cfg_spin.value() == 60 and
                    self.single_speed_spin.value() == 100
                )
                
                if is_default_values:
                    current_emotion = self.single_emotion_combo.currentText()
                    print(f"[MODE] Triggering emotion load for: {current_emotion} (default values)")
                    self.on_single_emotion_changed(current_emotion)
                else:
                    print(f"[MODE] Skipping emotion load - user has customized values")
            
        elif mode == "complex":
            # Show character table, hide simple emotion config
            self.simple_emotion_group.setVisible(False)
            self.character_group.setVisible(True)
            print("[MODE] Switched to Complex mode - multiple character configs")
            
        else:  # mode == "none"
            # Hide both until user chooses input
            self.simple_emotion_group.setVisible(False)
            self.character_group.setVisible(False)
            print("[MODE] No mode selected")
    
    def on_single_emotion_changed(self, emotion_name):
        """Handle emotion change in Simple mode"""
        print(f"[DEBUG] on_single_emotion_changed called with: {emotion_name}")
        
        if not self.emotions_config or 'emotions' not in self.emotions_config:
            print(f"[DEBUG] emotions_config not loaded yet")
            return
            
        if emotion_name not in self.emotions_config.get('emotions', {}):
            print(f"[DEBUG] {emotion_name} not found in emotions config")
            return
            
        emotion_config = self.emotions_config['emotions'][emotion_name]
        print(f"[DEBUG] Found emotion config: {emotion_config}")
        
        # Temporarily block signals to avoid recursive calls
        self.single_exag_spin.blockSignals(True)
        self.single_cfg_spin.blockSignals(True)
        self.single_speed_spin.blockSignals(True)
        
        # Auto-fill spin boxes with emotion parameters
        exag_value = int(emotion_config.get('exaggeration', 1.0) * 100)
        cfg_value = int(emotion_config.get('cfg_weight', 0.6) * 100)
        speed_value = int(emotion_config.get('speed', 1.0) * 100)
        
        print(f"[DEBUG] Setting values: exag={exag_value}, cfg={cfg_value}, speed={speed_value}")
        
        self.single_exag_spin.setValue(exag_value)
        self.single_cfg_spin.setValue(cfg_value)
        self.single_speed_spin.setValue(speed_value)
        
        # Re-enable signals
        self.single_exag_spin.blockSignals(False)
        self.single_cfg_spin.blockSignals(False)
        self.single_speed_spin.blockSignals(False)
        
        # Update single emotion config
        self.update_single_emotion_config()
        
        print(f"[SINGLE EMOTION] {emotion_name} -> exag={emotion_config.get('exaggeration')}, cfg={emotion_config.get('cfg_weight')}, speed={emotion_config.get('speed')}")
    
    def update_single_emotion_config(self):
        """Update single emotion configuration from UI values"""
        self.single_emotion_config = {
            'emotion': self.single_emotion_combo.currentText(),
            'exaggeration': self.single_exag_spin.value() / 100.0,
            'cfg_weight': self.single_cfg_spin.value() / 100.0,
            'speed': self.single_speed_spin.value() / 100.0,
            'temperature': self.emotions_config.get('emotions', {}).get(
                self.single_emotion_combo.currentText(), {}
            ).get('temperature', 0.8)
        }
        print(f"[SINGLE CONFIG UPDATE] {self.single_emotion_config}")
        
        if platform.system() == "Windows":
                subprocess.run(["explorer", self.output_directory])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.output_directory])
            else:  # Linux
                subprocess.run(["xdg-open", self.output_directory])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Không thể mở thư mục: {str(e)}")
    
    def add_log(self, message):
        \"\"\"Add message to logs với timestamp\"\"\"
        from datetime import datetime
        
        timestamp = datetime.now().strftime(\"%H:%M:%S\")
        log_entry = f\"[{timestamp}] {message}\"
        
        # Add to logs text area
        if hasattr(self, 'logs_text'):
            self.logs_text.append(log_entry)
            # Auto scroll to bottom
            cursor = self.logs_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.logs_text.setTextCursor(cursor)
    
    def clear_logs(self):
        \"\"\"Clear all logs\"\"\"
        if hasattr(self, 'logs_text'):
            self.logs_text.clear()
            self.add_log(\"[SYSTEM] Logs cleared\")
    
    def save_logs(self):
        \"\"\"Save logs to file\"\"\"
        from datetime import datetime
        
        if not hasattr(self, 'logs_text'):
            return
            
        # Get save location
        timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")
        default_filename = f\"voice_studio_logs_{timestamp}.txt\"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            \"Save Logs\", 
            default_filename,
            \"Text Files (*.txt);;All Files (*)\"\n        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.logs_text.toPlainText())
                self.add_log(f\"[SYSTEM] Logs saved to {file_path}\")
            except Exception as e:
                self.add_log(f\"[ERROR] Failed to save logs: {str(e)}\")
    
    def toggle_emotion_mapping_mode(self, enabled):
        \"\"\"Toggle emotion mapping mode - disable/enable manual emotion controls\"\"\"
        # When auto emotion mapping is enabled, disable 5 emotion control columns
        for row in range(self.character_settings_table.rowCount()):
            # Columns: 1=Emotion, 2=Exaggeration, 3=Speed, 4=CFG Weight, 5=Temperature
            for col in [1, 2, 3, 4, 5]:
                container_widget = self.character_settings_table.cellWidget(row, col)
                if container_widget:
                    # Get the actual widget inside the container
                    actual_widget = container_widget.layout().itemAt(0).widget()
                    if actual_widget:
                        if enabled:
                            # Auto mode: disable + change style to indicate disabled
                            actual_widget.setEnabled(False)
                            if hasattr(actual_widget, 'setStyleSheet'):
                                actual_widget.setStyleSheet(f\"\"\"
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
                                \"\"\")\n                        else:\n                            # Manual mode: enable + restore normal style\n                            actual_widget.setEnabled(True)\n                            actual_widget.setStyleSheet(ModernStyles.get_table_cell_widget_style())\n        \n        # Update progress text\n        mode = \"Auto Emotion Mapping\" if enabled else \"Manual Configuration\"\n        self.progress_text.setText(f\"Mode: {mode}\")\n        \n        # Log the mode change\n        self.add_log(f\"[MODE] Switched to {mode}\")\n    \n    def generate_voice_real(self):\n        \"\"\"Real voice generation using Chatterbox Extended\"\"\"\n        if not self.script_data:\n            self.add_log(\"[ERROR] No script data loaded. Please import a script first.\")\n            return\n            \n        self.add_log(\"[GENERATION] Starting real voice generation...\")\n        self.progress_text.setText(\"Initializing voice generation...\")\n        self.progress_bar.setVisible(True)\n        self.progress_bar.setValue(0)\n        \n        try:\n            # Import real voice generation\n            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration\n            \n            def progress_callback(current, total, message):\n                progress = int((current / total) * 100)\n                self.progress_bar.setValue(progress)\n                self.progress_text.setText(message)\n                self.add_log(f\"[PROGRESS] {message} ({current}/{total})\")\n            \n            # Initialize Chatterbox Extended\n            chatterbox_extended = ChatterboxExtendedIntegration()\n            \n            # Start generation\n            result = chatterbox_extended.generate_audio_from_script_data(\n                script_data=self.script_data,\n                voice_mapping=self.voice_mapping,\n                output_directory=self.output_directory,\n                emotion_configs=self.character_configs,\n                progress_callback=progress_callback\n            )\n            \n            if result.get(\"success\"):\n                self.add_log(\"[SUCCESS] Voice generation completed successfully!\")\n                self.progress_text.setText(\"Voice generation completed!\")\n                if os.path.exists(self.output_directory):\n                    self.add_log(f\"[OUTPUT] Files saved to: {self.output_directory}\")\n            else:\n                self.add_log(f\"[ERROR] Voice generation failed: {result.get('error', 'Unknown error')}\")\n                \n        except Exception as e:\n            self.add_log(f\"[ERROR] Voice generation failed: {str(e)}\")\n            self.progress_text.setText(\"Generation failed\")\n    \n    def open_output_folder_real(self):\n        \"\"\"Open output folder in file manager - Real implementation\"\"\"\n        try:\n            import subprocess\n            import platform\n            \n            if not os.path.exists(self.output_directory):\n                os.makedirs(self.output_directory, exist_ok=True)\n                self.add_log(f\"[SYSTEM] Created output directory: {self.output_directory}\")\n            \n            if platform.system() == \"Windows\":\n                subprocess.run([\"explorer\", self.output_directory])\n            elif platform.system() == \"Darwin\":  # macOS\n                subprocess.run([\"open\", self.output_directory])\n            else:  # Linux\n                subprocess.run([\"xdg-open\", self.output_directory])\n                \n            self.add_log(f\"[ACTION] Opened output folder: {self.output_directory}\")\n            \n        except Exception as e:\n            self.add_log(f\"[ERROR] Failed to open output folder: {str(e)}\")\n    \n    def load_from_video_tab(self):\n        \"\"\"Load script data from video tab\"\"\"\n        self.progress_text.setText(\"Loading from video tab...\")\n        self.add_log(\"[ACTION] Loading script data from video tab\")\n        \n    def show_manual_input_dialog(self):\n        \"\"\"Show manual script input dialog\"\"\"\n        self.manual_input_area.setVisible(True)\n        self.add_log(\"[ACTION] Opening manual script input dialog\")\n        \n    def parse_manual_json(self):\n        \"\"\"Parse manual JSON input\"\"\"\n        json_text = self.manual_script_input.toPlainText().strip()\n        if json_text:\n            try:\n                self.script_data = json.loads(json_text)\n                self.update_script_overview()\n                self.populate_character_table()\n                self.add_log(\"[SUCCESS] JSON parsed and loaded successfully\")\n                self.progress_text.setText(\"Script loaded from manual input\")\n                self.manual_input_area.setVisible(False)\n            except json.JSONDecodeError as e:\n                self.add_log(f\"[ERROR] Invalid JSON format: {str(e)}\")\n                self.progress_text.setText(\"Invalid JSON format\")\n        else:\n            self.progress_text.setText(\"Please enter JSON data first\")\n            self.add_log(\"[WARNING] No JSON data provided for parsing\")\n            \n    def browse_output_folder(self):\n        \"\"\"Browse for output folder\"\"\"\n        folder = QFileDialog.getExistingDirectory(self, \"Select Output Directory\")\n        if folder:\n            self.output_directory = folder\n            self.output_path_input.setText(folder)\n            self.add_log(f\"[FOLDER] Output directory changed to: {folder}\")\n        \n    def import_srt_file(self):\n        \"\"\"Import script from SRT file - Placeholder for now\"\"\"\n        QMessageBox.information(self, \"SRT Import\", \"SRT import feature will be implemented soon!\")\n        self.add_log(\"[INFO] SRT import feature not yet implemented\")\n    \n    def clear_results(self):\n        \"\"\"Clear results and reset progress\"\"\"\n        self.progress_text.setText(\"Ready to generate voices\")\n        self.progress_bar.setVisible(False)\n        self.progress_bar.setValue(0)\n        self.add_log(\"[SYSTEM] Results cleared, ready for new generation\")\n    \n    def update_script_overview(self):\n        \"\"\"Update script overview with real data\"\"\"\n        if not self.script_data:\n            return\n            \n        segments = self.script_data.get('segments', [])\n        characters = set()\n        total_dialogues = 0\n        \n        for segment in segments:\n            for dialogue in segment.get('dialogues', []):\n                characters.add(dialogue['speaker'])\n                total_dialogues += 1\n        \n        # Update status display\n        self.characters_label.setText(f\"👥 Characters: {len(characters)}\")\n        self.segments_label.setText(f\"📑 Segments: {len(segments)}\")\n        \n        self.add_log(f\"[OVERVIEW] {len(segments)} segments, {len(characters)} characters, {total_dialogues} dialogues\")"