from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QScrollArea, QSlider, QSpinBox,
    QTextEdit, QLineEdit, QCheckBox, QProgressBar, QFileDialog,
    QSplitter, QFormLayout, QGridLayout, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont, QPixmap, QIcon
import sys
import os
# Remove problematic sys.path manipulation
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# VoiceGenerator import removed - using Chatterbox Extended instead
from ui.styles import (
    BUTTON_STYLE, PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, DANGER_BUTTON_STYLE,
    LABEL_STYLE, HEADER_LABEL_STYLE, INPUT_STYLE, COLORS
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
    def __init__(self, parent=None):
        super().__init__(parent)
        # Using Chatterbox Extended instead of direct VoiceGenerator
        self.script_data = None
        self.voice_mapping = {}
        self.character_configs = {}  # Store emotion parameters per character
        self.output_directory = "./voice_studio_output"
        self.emotions_config = self.load_emotions_config()
        self.current_mode = "none"  # "simple", "complex", or "none"
        self.single_emotion_config = {'emotion': 'neutral', 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.0, 'temperature': 0.8}
        print(f"[DEBUG] Emotions config loaded: {len(self.emotions_config.get('emotions', {}))} emotions")
        self.setup_ui()
        self.setup_connections()
        self.populate_available_voices()  # Load voices for existing dropdown
    
    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # LEFT PANEL (60%) - Input & Configuration
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # RIGHT PANEL (40%) - Overview & Progress
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([600, 400])  # 60% - 40%
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
    
    def create_left_panel(self):
        """Create left panel with input and configuration"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(12)
        
        # ① Script Input Section
        script_group = self.create_script_input_section()
        left_layout.addWidget(script_group)
        
        # ② Template Mode Section
        template_group = self.create_template_mode_section()
        left_layout.addWidget(template_group)
        
        # ③ TTS Configuration Section
        tts_group = self.create_tts_configuration_section()
        left_layout.addWidget(tts_group)
        
        # ④ Character Configuration Section (Complex mode)
        self.character_group = self.create_character_config_section()
        left_layout.addWidget(self.character_group)
        
        # ④ Simple Emotion Section (Simple mode) - Initially hidden
        self.simple_emotion_group = self.create_simple_emotion_section()
        self.simple_emotion_group.setVisible(False)
        left_layout.addWidget(self.simple_emotion_group)
        
        # ⑤ Actions Section
        actions_group = self.create_actions_section()
        left_layout.addWidget(actions_group)
        
        # Add stretch to push everything up
        left_layout.addStretch()
        
        return left_widget
    
    def create_right_panel(self):
        """Create right panel with overview and progress"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(12)
        
        # ⑥ Script Overview Section
        overview_group = self.create_script_overview_section()
        right_layout.addWidget(overview_group)
        
        # ⑦ Token Statistics Section
        stats_group = self.create_token_stats_section()
        right_layout.addWidget(stats_group)
        
        # ⑧ Progress Section
        progress_group = self.create_progress_section()
        right_layout.addWidget(progress_group)
        
        # ⑨ Results & Actions Section
        results_group = self.create_results_section()
        right_layout.addWidget(results_group)
        
        # Add stretch to push everything up
        right_layout.addStretch()
        
        return right_widget
    
    def create_script_input_section(self):
        """① Script Input Section"""
        group = QGroupBox("① Nhập Script")
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
        
        # Script import buttons
        import_layout = QHBoxLayout()
        
        self.import_file_btn = QPushButton("[FOLDER] Import từ file")
        self.import_file_btn.setStyleSheet(BUTTON_STYLE)
        import_layout.addWidget(self.import_file_btn)
        
        self.manual_input_btn = QPushButton("[EDIT] Nhập thủ công")
        self.manual_input_btn.setStyleSheet(BUTTON_STYLE)
        import_layout.addWidget(self.manual_input_btn)
        
        layout.addLayout(import_layout)
        
        # Data source selection
        source_layout = QFormLayout()
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems([
            "Script JSON chuẩn",
            "AI Generated Script", 
            "Video Tab Output",
            "Custom Format"
        ])
        self.data_source_combo.setStyleSheet(INPUT_STYLE)
        source_layout.addRow("Nguồn dữ liệu:", self.data_source_combo)
        
        layout.addLayout(source_layout)
        
        # Script preview
        self.script_preview = QTextEdit()
        self.script_preview.setMaximumHeight(100)
        self.script_preview.setPlaceholderText("Script preview sẽ hiển thị ở đây...")
        self.script_preview.setStyleSheet(INPUT_STYLE)
        self.script_preview.setReadOnly(True)
        layout.addWidget(self.script_preview)
        
        return group
    
    def create_template_mode_section(self):
        """② Template Mode Section"""
        group = QGroupBox("② Chế độ Template")
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
        layout.setSpacing(8)
        
        # Template mode selection
        self.template_mode_combo = QComboBox()
        self.template_mode_combo.addItems([
            "Standard - Cân bằng (400 tokens)",
            "Balanced - Tối ưu (250 tokens)",
            "Rapid - Nhanh (150 tokens)",
            "Custom - Tùy chỉnh"
        ])
        self.template_mode_combo.setStyleSheet(INPUT_STYLE)
        layout.addRow("Chế độ:", self.template_mode_combo)
        
        return group
    
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
        """④ Actions Section"""
        group = QGroupBox("④ Hành động")
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
        
        # Primary action button
        self.generate_btn = QPushButton("[MIC] Tạo Voice")
        self.generate_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.generate_btn.setMinimumHeight(40)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.generate_btn.setFont(font)
        layout.addWidget(self.generate_btn)
        
        # Secondary actions
        secondary_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("[EMOJI] Preview")
        self.preview_btn.setStyleSheet(BUTTON_STYLE)
        secondary_layout.addWidget(self.preview_btn)
        
        self.settings_btn = QPushButton("[CONFIG] Cài đặt")
        self.settings_btn.setStyleSheet(BUTTON_STYLE)
        secondary_layout.addWidget(self.settings_btn)
        
        layout.addLayout(secondary_layout)
        
        return group
    
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
        """⑦ Progress Section"""
        group = QGroupBox("⑦ Tiến trình sinh Voice")
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
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 5px;
                background-color: {COLORS['background']};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.progress_status = QLabel("Sẵn sàng")
        self.progress_status.setStyleSheet(LABEL_STYLE)
        layout.addWidget(self.progress_status)
        
        # Output directory
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("[FOLDER] Output:"))
        self.output_path_label = QLabel(self.output_directory)
        self.output_path_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        output_layout.addWidget(self.output_path_label)
        output_layout.addStretch()
        layout.addLayout(output_layout)
        
        return group
    
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
        """Load emotions configuration from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'emotions', 'unified_emotions.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[EMOTION CONFIG ERROR] {e}")
            return {"emotions": {}}
    
    def setup_connections(self):
        """Setup signal connections"""
        # File operations
        self.import_file_btn.clicked.connect(self.import_script_file)
        self.manual_input_btn.clicked.connect(self.show_manual_input_dialog)
        
        # Configuration
        self.detailed_config_cb.toggled.connect(self.toggle_advanced_controls)
        self.speed_slider.valueChanged.connect(lambda v: self.speed_label.setText(f"{v/100:.1f}x"))
        self.emotion_slider.valueChanged.connect(lambda v: self.emotion_label.setText(f"{v/100:.1f}x"))
        
        # Actions
        self.generate_btn.clicked.connect(self.start_voice_generation)
        self.preview_btn.clicked.connect(self.preview_voice)
        self.settings_btn.clicked.connect(self.show_voice_settings)
        self.request_form_btn.clicked.connect(self.generate_ai_request_form)
        
        # Character config connections
        self.auto_fill_btn.clicked.connect(self.auto_fill_character_table)
        self.reset_emotions_btn.clicked.connect(self.reset_all_emotions_to_neutral)
        self.character_table.cellChanged.connect(self.on_cell_changed)
        
        # Results actions
        self.clear_btn.clicked.connect(self.clear_results)
        self.delete_btn.clicked.connect(self.delete_output_files)
        self.merge_btn.clicked.connect(self.merge_audio_files)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
    
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