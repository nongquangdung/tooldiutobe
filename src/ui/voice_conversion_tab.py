#!/usr/bin/env python3
"""
[EMOJI] VOICE CONVERSION TAB - PHASE 3 FEATURE
=========================================

Voice Conversion tab implementation dựa trên original Chatterbox Extended.
Feature cho phép convert voice từ source audio sang target voice style.

Features:
- Voice-to-Voice conversion
- Batch conversion support  
- Quality control settings
- Real-time preview
- Progress tracking
"""

import os
import json
import time
import tempfile
from typing import Dict, List, Optional, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QComboBox,
    QSlider, QLineEdit, QMessageBox, QFileDialog,
    QCheckBox, QScrollArea, QFormLayout, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox, QDoubleSpinBox, QProgressBar, QProgressDialog,
    QFrame, QSizePolicy, QTextEdit, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer, QSize
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QPen, QBrush, QPalette

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
logger = logging.getLogger(__name__)

class VoiceConversionWorker(QThread):
    """Background worker for voice conversion"""
    progress_updated = Signal(int, str)
    conversion_completed = Signal(dict)
    error_occurred = Signal(str)
    
    def __init__(self, conversion_config):
        super().__init__()
        self.conversion_config = conversion_config
    
    def run(self):
        """Run voice conversion process"""
        try:
            self.progress_updated.emit(10, "[REFRESH] Khởi tạo chuyển đổi giọng nói...")
            
            # Simulate conversion process (replace with actual Chatterbox logic)
            import time
            time.sleep(1)
            
            self.progress_updated.emit(30, "[MUSIC] Đang tải audio nguồn...")
            time.sleep(1)
            
            self.progress_updated.emit(50, "[THEATER] Phân tích phong cách giọng nói đích...")
            time.sleep(1)
            
            self.progress_updated.emit(70, "[FAST] Đang chuyển đổi giọng nói...")
            time.sleep(2)
            
            self.progress_updated.emit(90, "[EMOJI] Lưu audio đã chuyển đổi...")
            time.sleep(1)
            
            # Mock result
            result = {
                'success': True,
                'output_path': self.conversion_config.get('output_path', './output/converted.wav'),
                'conversion_time': 5.2,
                'quality_score': 0.92
            }
            
            self.progress_updated.emit(100, "[OK] Hoàn thành chuyển đổi giọng nói!")
            self.conversion_completed.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class VoiceConversionTab(QWidget):
    """Voice Conversion Tab - Phase 3 Feature"""
    
    def __init__(self):
        super().__init__()
        self.conversion_queue = []
        self.current_conversion = None
        self.setup_ui()
        self.load_voice_models()
    
    def setup_ui(self):
        """Setup Voice Conversion UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("[EMOJI] STUDIO CHUYỂN ĐỔI GIỌNG NÓI")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("[ON] Sẵn sàng")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        main_layout.addLayout(header_layout)
        
        # === INPUT SECTION ===
        input_group = QGroupBox("[EMOJI] Cấu hình đầu vào")
        input_layout = QVBoxLayout()
        
        # Source audio selection
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Audio nguồn:"))
        
        self.source_audio_input = QLineEdit()
        self.source_audio_input.setPlaceholderText("Chọn file audio nguồn để chuyển đổi...")
        source_layout.addWidget(self.source_audio_input)
        
        self.browse_source_btn = QPushButton("[FOLDER] Duyệt")
        self.browse_source_btn.clicked.connect(self.browse_source_audio)
        source_layout.addWidget(self.browse_source_btn)
        
        self.play_source_btn = QPushButton("[PLAY]")
        self.play_source_btn.setMaximumWidth(40)
        self.play_source_btn.clicked.connect(self.play_source_audio)
        self.play_source_btn.setEnabled(False)
        source_layout.addWidget(self.play_source_btn)
        
        input_layout.addLayout(source_layout)
        
        # Target voice selection
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Phong cách giọng đích:"))
        
        self.target_voice_combo = QComboBox()
        self.target_voice_combo.setMinimumWidth(200)
        target_layout.addWidget(self.target_voice_combo)
        
        self.browse_target_btn = QPushButton("[FOLDER] Giọng tùy chỉnh")
        self.browse_target_btn.clicked.connect(self.browse_custom_target)
        target_layout.addWidget(self.browse_target_btn)
        
        self.preview_target_btn = QPushButton("[EMOJI]")
        self.preview_target_btn.setMaximumWidth(40)
        self.preview_target_btn.clicked.connect(self.preview_target_voice)
        target_layout.addWidget(self.preview_target_btn)
        
        target_layout.addStretch()
        input_layout.addLayout(target_layout)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # === CONVERSION SETTINGS ===
        settings_group = QGroupBox("[CONFIG] Cài đặt chuyển đổi")
        settings_layout = QGridLayout()
        
        # Conversion strength
        settings_layout.addWidget(QLabel("Cường độ chuyển đổi:"), 0, 0)
        self.conversion_strength = QSlider(Qt.Horizontal)
        self.conversion_strength.setRange(1, 100)
        self.conversion_strength.setValue(75)
        self.conversion_strength.valueChanged.connect(self.update_strength_label)
        settings_layout.addWidget(self.conversion_strength, 0, 1)
        
        self.strength_label = QLabel("75%")
        self.strength_label.setMinimumWidth(40)
        settings_layout.addWidget(self.strength_label, 0, 2)
        
        # Pitch preservation
        settings_layout.addWidget(QLabel("Giữ nguyên cao độ:"), 1, 0)
        self.pitch_preservation = QSlider(Qt.Horizontal)
        self.pitch_preservation.setRange(0, 100)
        self.pitch_preservation.setValue(50)
        self.pitch_preservation.valueChanged.connect(self.update_pitch_label)
        settings_layout.addWidget(self.pitch_preservation, 1, 1)
        
        self.pitch_label = QLabel("50%")
        self.pitch_label.setMinimumWidth(40)
        settings_layout.addWidget(self.pitch_label, 1, 2)
        
        # Quality settings
        settings_layout.addWidget(QLabel("Chế độ chất lượng:"), 2, 0)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Nháp (Nhanh, 22kHz)",
            "Tiêu chuẩn (Cân bằng, 44kHz)",
            "Chất lượng cao (Chậm, 48kHz)",
            "Siêu cao (Chậm nhất, 96kHz)"
        ])
        self.quality_combo.setCurrentIndex(1)  # Standard
        settings_layout.addWidget(self.quality_combo, 2, 1, 1, 2)
        
        # Advanced options
        settings_layout.addWidget(QLabel("Advanced Options:"), 3, 0)
        advanced_layout = QHBoxLayout()
        
        self.preserve_emotion_checkbox = QCheckBox("Preserve Emotion")
        self.preserve_emotion_checkbox.setChecked(True)
        advanced_layout.addWidget(self.preserve_emotion_checkbox)
        
        self.noise_reduction_checkbox = QCheckBox("Noise Reduction")
        self.noise_reduction_checkbox.setChecked(True)
        advanced_layout.addWidget(self.noise_reduction_checkbox)
        
        self.normalize_volume_checkbox = QCheckBox("Normalize Volume")
        self.normalize_volume_checkbox.setChecked(True)
        advanced_layout.addWidget(self.normalize_volume_checkbox)
        
        settings_layout.addLayout(advanced_layout, 3, 1, 1, 2)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # === OUTPUT SECTION ===
        output_group = QGroupBox("[EMOJI] Output Configuration")
        output_layout = QVBoxLayout()
        
        # Output path
        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel("Output Folder:"))
        
        self.output_path_input = QLineEdit()
        self.output_path_input.setText("./voice_studio_output/converted/")
        output_path_layout.addWidget(self.output_path_input)
        
        self.browse_output_btn = QPushButton("[FOLDER]")
        self.browse_output_btn.setMaximumWidth(40)
        self.browse_output_btn.clicked.connect(self.browse_output_folder)
        output_path_layout.addWidget(self.browse_output_btn)
        
        output_layout.addLayout(output_path_layout)
        
        # Output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["WAV (Uncompressed)", "MP3 (320kbps)", "FLAC (Lossless)"])
        format_layout.addWidget(self.output_format_combo)
        
        format_layout.addStretch()
        output_layout.addLayout(format_layout)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # === CONVERSION CONTROL ===
        control_group = QGroupBox("[EMOJI] Conversion Control")
        control_layout = QVBoxLayout()
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.preview_conversion_btn = QPushButton("[EMOJI] Preview Conversion")
        self.preview_conversion_btn.clicked.connect(self.preview_conversion)
        self.preview_conversion_btn.setEnabled(False)
        button_layout.addWidget(self.preview_conversion_btn)
        
        self.start_conversion_btn = QPushButton("[ROCKET] Start Conversion")
        self.start_conversion_btn.clicked.connect(self.start_conversion)
        self.start_conversion_btn.setEnabled(False)
        self.start_conversion_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        button_layout.addWidget(self.start_conversion_btn)
        
        self.batch_conversion_btn = QPushButton("[FOLDER] Batch Convert")
        self.batch_conversion_btn.clicked.connect(self.start_batch_conversion)
        button_layout.addWidget(self.batch_conversion_btn)
        
        control_layout.addLayout(button_layout)
        
        # Progress section
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        control_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #7F8C8D; font-style: italic;")
        self.progress_label.setVisible(False)
        control_layout.addWidget(self.progress_label)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # === RESULTS SECTION ===
        results_group = QGroupBox("[STATS] Conversion Results")
        results_layout = QVBoxLayout()
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.setMaximumHeight(150)
        results_layout.addWidget(self.results_list)
        
        # Results actions
        results_actions_layout = QHBoxLayout()
        
        self.play_result_btn = QPushButton("[PLAY] Play Selected")
        self.play_result_btn.clicked.connect(self.play_selected_result)
        self.play_result_btn.setEnabled(False)
        results_actions_layout.addWidget(self.play_result_btn)
        
        self.open_result_folder_btn = QPushButton("[FOLDER] Open Folder")
        self.open_result_folder_btn.clicked.connect(self.open_results_folder)
        results_actions_layout.addWidget(self.open_result_folder_btn)
        
        self.clear_results_btn = QPushButton("[DELETE] Clear Results")
        self.clear_results_btn.clicked.connect(self.clear_results)
        results_actions_layout.addWidget(self.clear_results_btn)
        
        results_actions_layout.addStretch()
        results_layout.addLayout(results_actions_layout)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        # Connect signals
        self.source_audio_input.textChanged.connect(self.update_ui_state)
        self.target_voice_combo.currentTextChanged.connect(self.update_ui_state)
        self.results_list.itemSelectionChanged.connect(self.on_result_selection_changed)
    
    def load_voice_models(self):
        """Load available voice models for conversion"""
        # Predefined voice styles
        voice_models = [
            "[THEATER] Narrator - Professional",
            "[EMOJI] Male - Young Adult",
            "[EMOJI] Female - Young Adult", 
            "[EMOJI] Male - Elder",
            "[EMOJI] Female - Elder",
            "[BOT] Robot - Synthetic",
            "[CIRCUS] Cartoon - Animated",
            "[EMOJI] Radio - Broadcaster",
            "[ACTION] Movie - Dramatic",
            "[MUSIC] Singer - Melodic"
        ]
        
        self.target_voice_combo.addItems(voice_models)
    
    def browse_source_audio(self):
        """Browse for source audio file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Source Audio",
            "",
            "Audio files (*.wav *.mp3 *.flac *.m4a);;All files (*.*)"
        )
        
        if file_path:
            self.source_audio_input.setText(file_path)
            self.play_source_btn.setEnabled(True)
    
    def browse_custom_target(self):
        """Browse for custom target voice"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Target Voice Sample",
            "",
            "Audio files (*.wav *.mp3 *.flac);;All files (*.*)"
        )
        
        if file_path:
            # Add custom voice to combo
            custom_name = f"[TARGET] Custom: {os.path.basename(file_path)}"
            self.target_voice_combo.addItem(custom_name)
            self.target_voice_combo.setCurrentText(custom_name)
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )
        
        if folder_path:
            self.output_path_input.setText(folder_path + "/")
    
    def update_strength_label(self, value):
        """Update conversion strength label"""
        self.strength_label.setText(f"{value}%")
    
    def update_pitch_label(self, value):
        """Update pitch preservation label"""
        self.pitch_label.setText(f"{value}%")
    
    def update_ui_state(self):
        """Update UI state based on inputs"""
        has_source = bool(self.source_audio_input.text().strip())
        has_target = bool(self.target_voice_combo.currentText())
        
        self.preview_conversion_btn.setEnabled(has_source and has_target)
        self.start_conversion_btn.setEnabled(has_source and has_target)
    
    def on_result_selection_changed(self):
        """Handle result selection change"""
        has_selection = bool(self.results_list.currentItem())
        self.play_result_btn.setEnabled(has_selection)
    
    def play_source_audio(self):
        """Play source audio"""
        source_path = self.source_audio_input.text()
        if source_path and os.path.exists(source_path):
            self.status_label.setText("[SOUND] Playing source audio...")
            # TODO: Implement audio playback
            QMessageBox.information(self, "Audio Player", f"Playing: {os.path.basename(source_path)}")
            self.status_label.setText("[ON] Ready")
    
    def preview_target_voice(self):
        """Preview target voice"""
        target_voice = self.target_voice_combo.currentText()
        if target_voice:
            self.status_label.setText("[EMOJI] Previewing target voice...")
            # TODO: Implement voice preview
            QMessageBox.information(self, "Voice Preview", f"Preview: {target_voice}")
            self.status_label.setText("[ON] Ready")
    
    def preview_conversion(self):
        """Preview conversion result (first 10 seconds)"""
        self.status_label.setText("[EMOJI] Generating preview...")
        
        # TODO: Implement preview conversion
        QMessageBox.information(
            self, 
            "Preview", 
            "Preview conversion would generate first 10 seconds with current settings"
        )
        
        self.status_label.setText("[ON] Ready")
    
    def start_conversion(self):
        """Start voice conversion"""
        # Validate inputs
        source_path = self.source_audio_input.text()
        if not source_path or not os.path.exists(source_path):
            QMessageBox.warning(self, "Error", "Please select a valid source audio file")
            return
        
        # Prepare conversion config
        output_dir = self.output_path_input.text() or "./voice_studio_output/converted/"
        os.makedirs(output_dir, exist_ok=True)
        
        output_filename = f"converted_{int(time.time())}.wav"
        output_path = os.path.join(output_dir, output_filename)
        
        conversion_config = {
            'source_path': source_path,
            'target_voice': self.target_voice_combo.currentText(),
            'output_path': output_path,
            'conversion_strength': self.conversion_strength.value(),
            'pitch_preservation': self.pitch_preservation.value(),
            'quality_mode': self.quality_combo.currentText(),
            'preserve_emotion': self.preserve_emotion_checkbox.isChecked(),
            'noise_reduction': self.noise_reduction_checkbox.isChecked(),
            'normalize_volume': self.normalize_volume_checkbox.isChecked(),
            'output_format': self.output_format_combo.currentText()
        }
        
        # Start conversion worker
        self.current_conversion = VoiceConversionWorker(conversion_config)
        self.current_conversion.progress_updated.connect(self.on_conversion_progress)
        self.current_conversion.conversion_completed.connect(self.on_conversion_completed)
        self.current_conversion.error_occurred.connect(self.on_conversion_error)
        
        # Update UI
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.start_conversion_btn.setEnabled(False)
        self.status_label.setText("[ROCKET] Converting...")
        
        self.current_conversion.start()
    
    def start_batch_conversion(self):
        """Start batch conversion"""
        QMessageBox.information(
            self,
            "Batch Conversion",
            "Batch conversion feature will allow you to convert multiple files at once.\n\nComing in next update!"
        )
    
    def on_conversion_progress(self, progress, message):
        """Handle conversion progress updates"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)
    
    def on_conversion_completed(self, result):
        """Handle conversion completion"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.start_conversion_btn.setEnabled(True)
        self.status_label.setText("[ON] Ready")
        
        if result['success']:
            # Add to results list
            result_item = QListWidgetItem(f"[OK] {os.path.basename(result['output_path'])} (Quality: {result['quality_score']:.1%})")
            result_item.setData(Qt.UserRole, result['output_path'])
            self.results_list.addItem(result_item)
            
            QMessageBox.information(
                self,
                "Conversion Complete",
                f"Voice conversion completed successfully!\n\n"
                f"Output: {result['output_path']}\n"
                f"Time: {result['conversion_time']:.1f}s\n"
                f"Quality Score: {result['quality_score']:.1%}"
            )
        else:
            QMessageBox.critical(self, "Conversion Failed", "Voice conversion failed. Please check settings and try again.")
    
    def on_conversion_error(self, error_message):
        """Handle conversion errors"""
        self.progress_bar.setVisible(False) 
        self.progress_label.setVisible(False)
        self.start_conversion_btn.setEnabled(True)
        self.status_label.setText("[EMOJI] Error")
        
        QMessageBox.critical(self, "Conversion Error", f"An error occurred during conversion:\n\n{error_message}")
    
    def play_selected_result(self):
        """Play selected conversion result"""
        current_item = self.results_list.currentItem()
        if current_item:
            file_path = current_item.data(Qt.UserRole)
            if file_path and os.path.exists(file_path):
                self.status_label.setText("[SOUND] Playing result...")
                # TODO: Implement audio playback
                QMessageBox.information(self, "Audio Player", f"Playing: {os.path.basename(file_path)}")
                self.status_label.setText("[ON] Ready")
    
    def open_results_folder(self):
        """Open results folder"""
        output_dir = self.output_path_input.text() or "./voice_studio_output/converted/"
        if os.path.exists(output_dir):
            os.startfile(output_dir) if os.name == 'nt' else os.system(f'open "{output_dir}"')
        else:
            QMessageBox.information(self, "Folder", "No results folder found yet.")
    
    def clear_results(self):
        """Clear results list"""
        reply = QMessageBox.question(
            self,
            "Clear Results",
            "Are you sure you want to clear all conversion results?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.results_list.clear()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    window = VoiceConversionTab()
    window.show()
    
    sys.exit(app.exec()) 