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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from tts.voice_generator import VoiceGenerator
from ..styles import (
    BUTTON_STYLE, PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, DANGER_BUTTON_STYLE,
    LABEL_STYLE, HEADER_LABEL_STYLE, INPUT_STYLE, COLORS
)
import json

class VoiceGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, script_data, voice_mapping, output_dir):
        super().__init__()
        self.script_data = script_data
        self.voice_mapping = voice_mapping
        self.output_dir = output_dir
        
    def run(self):
        try:
            voice_gen = VoiceGenerator()
            
            def progress_callback(current, total, message):
                progress = int((current / total) * 100)
                self.progress_updated.emit(progress, message)
            
            # Mock progress for now - integrate with real generation
            total_dialogues = sum(len(seg.get('dialogues', [])) for seg in self.script_data.get('segments', []))
            
            for i in range(total_dialogues):
                progress_callback(i + 1, total_dialogues, f"Generating voice {i+1}/{total_dialogues}")
                self.msleep(500)  # Simulate processing time
            
            self.finished.emit({"success": True, "message": "Voice generation completed"})
            
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})

class VoiceStudioTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.voice_generator = VoiceGenerator()
        self.script_data = None
        self.voice_mapping = {}
        self.output_directory = "./voice_studio_output"
        self.setup_ui()
        self.setup_connections()
    
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
        
        # ④ Actions Section
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
        
        # ⑤ Script Overview Section
        overview_group = self.create_script_overview_section()
        right_layout.addWidget(overview_group)
        
        # ⑥ Token Statistics Section
        stats_group = self.create_token_stats_section()
        right_layout.addWidget(stats_group)
        
        # ⑦ Progress Section
        progress_group = self.create_progress_section()
        right_layout.addWidget(progress_group)
        
        # ⑧ Results & Actions Section
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
        
        self.import_file_btn = QPushButton("📁 Import từ file")
        self.import_file_btn.setStyleSheet(BUTTON_STYLE)
        import_layout.addWidget(self.import_file_btn)
        
        self.manual_input_btn = QPushButton("✏️ Nhập thủ công")
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
        self.auto_emotion_cb = QCheckBox("🎭 Tự điều chỉnh cảm xúc")
        self.auto_emotion_cb.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
        self.auto_emotion_cb.setChecked(True)
        layout.addWidget(self.auto_emotion_cb)
        
        self.detailed_config_cb = QCheckBox("⚙️ Cấu hình chi tiết")
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
        self.generate_btn = QPushButton("🎙️ Tạo Voice")
        self.generate_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.generate_btn.setMinimumHeight(40)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.generate_btn.setFont(font)
        layout.addWidget(self.generate_btn)
        
        # Secondary actions
        secondary_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("👂 Preview")
        self.preview_btn.setStyleSheet(BUTTON_STYLE)
        secondary_layout.addWidget(self.preview_btn)
        
        self.settings_btn = QPushButton("⚙️ Cài đặt")
        self.settings_btn.setStyleSheet(BUTTON_STYLE)
        secondary_layout.addWidget(self.settings_btn)
        
        layout.addLayout(secondary_layout)
        
        return group
    
    def create_script_overview_section(self):
        """⑤ Script Overview Section"""
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
        savings_layout.addWidget(QLabel("💰 Token tiết kiệm:"))
        self.savings_label = QLabel("0 tokens")
        self.savings_label.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        savings_layout.addWidget(self.savings_label)
        savings_layout.addStretch()
        layout.addLayout(savings_layout)
        
        # Request form button
        self.request_form_btn = QPushButton("📝 Tạo AI Request Form")
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
        output_layout.addWidget(QLabel("📁 Output:"))
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
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setStyleSheet(BUTTON_STYLE)
        button_layout.addWidget(self.clear_btn)
        
        self.delete_btn = QPushButton("❌ Delete")
        self.delete_btn.setStyleSheet(DANGER_BUTTON_STYLE)
        button_layout.addWidget(self.delete_btn)
        
        self.merge_btn = QPushButton("🔗 Merge")
        self.merge_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        button_layout.addWidget(self.merge_btn)
        
        layout.addLayout(button_layout)
        
        # Open output folder button
        self.open_folder_btn = QPushButton("📂 Mở thư mục kết quả")
        self.open_folder_btn.setStyleSheet(BUTTON_STYLE)
        layout.addWidget(self.open_folder_btn)
        
        return group
    
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
            self.voice_combo.addItem("Lỗi tải giọng nói", None)
    
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
                
                self.update_script_overview()
                self.script_preview.setText(f"✅ Đã tải script từ: {file_path}")
                self.status_label.setText("Script đã sẵn sàng")
                
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Không thể đọc file: {str(e)}")
    
    def show_manual_input_dialog(self):
        """Show manual script input dialog"""
        # This would open a dialog for manual script input
        QMessageBox.information(self, "Thông báo", "Tính năng nhập thủ công sẽ được triển khai")
    
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
        
        # Create basic voice mapping for all characters
        characters = self.script_data.get('characters', [])
        self.voice_mapping = {char['id']: default_voice for char in characters}
        
        # Start generation thread
        self.generation_thread = VoiceGenerationThread(
            self.script_data, self.voice_mapping, self.output_directory
        )
        self.generation_thread.progress_updated.connect(self.update_progress)
        self.generation_thread.finished.connect(self.generation_finished)
        
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("🔄 Đang tạo...")
        self.generation_thread.start()
    
    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.progress_status.setText(message)
    
    def generation_finished(self, result):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🎙️ Tạo Voice")
        
        if result.get('success'):
            self.progress_status.setText("✅ Hoàn thành")
            self.results_label.setText("Voice generation thành công!")
            QMessageBox.information(self, "Thành công", "Tạo voice hoàn tất!")
        else:
            self.progress_status.setText("❌ Lỗi")
            error_msg = result.get('error', 'Unknown error')
            QMessageBox.critical(self, "Lỗi", f"Tạo voice thất bại:\n{error_msg}")
    
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
            if platform.system() == "Windows":
                subprocess.run(["explorer", self.output_directory])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.output_directory])
            else:  # Linux
                subprocess.run(["xdg-open", self.output_directory])
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể mở thư mục: {str(e)}")