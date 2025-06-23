#!/usr/bin/env python3
"""
🎭 EMOTION CONFIGURATION TAB - TABLE FORMAT (IMPROVED)
====================================================

Tab quản lý cảm xúc với format bảng được cải thiện về UI/UX.

Features:
- Table format với row height phù hợp
- Preview âm thanh hoạt động tốt
- Action buttons gọn gàng
- Text formatting nhất quán
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QComboBox,
    QSlider, QLineEdit, QMessageBox, QFileDialog,
    QCheckBox, QScrollArea, QFormLayout, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox, QDoubleSpinBox, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont, QColor

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.emotion_config_manager import EmotionConfigManager, EmotionParameters

# Import TTS provider để preview âm thanh thật
try:
    from tts.real_chatterbox_provider import RealChatterboxProvider
    PREVIEW_AVAILABLE = True
except ImportError:
    PREVIEW_AVAILABLE = False
    print("⚠️ TTS provider not available - preview will be simulated")

import logging
logger = logging.getLogger(__name__)

class AudioPreviewThread(QThread):
    """Thread để generate preview âm thanh thật"""
    preview_completed = Signal(str, str, bool)  # emotion_name, audio_path, success
    preview_progress = Signal(str, int)  # emotion_name, progress_percent
    preview_error = Signal(str, str)  # emotion_name, error_message
    
    def __init__(self, emotion_name: str, parameters: dict):
        super().__init__()
        self.emotion_name = emotion_name
        self.parameters = parameters
        self.preview_text = f"Đây là preview của emotion {emotion_name}."
    
    def run(self):
        try:
            self.preview_progress.emit(self.emotion_name, 10)
            
            if PREVIEW_AVAILABLE:
                # Sử dụng TTS thật để generate audio
                try:
                    provider = RealChatterboxProvider()
                    self.preview_progress.emit(self.emotion_name, 30)
                    
                    # Tạo file preview
                    preview_dir = "test_audio_output"
                    os.makedirs(preview_dir, exist_ok=True)
                    audio_path = os.path.join(preview_dir, f"emotion_preview_{self.emotion_name}.wav")
                    
                    self.preview_progress.emit(self.emotion_name, 60)
                    
                    # Generate với parameters - sử dụng method chính xác
                    result = provider.generate_voice(
                        text=self.preview_text,
                        save_path=audio_path,
                        emotion_exaggeration=self.parameters.get('exaggeration', 1.0),
                        cfg_weight=self.parameters.get('cfg_weight', 0.5),
                        speed=self.parameters.get('speed', 1.0)
                    )
                    success = result.get('success', False)
                    
                    self.preview_progress.emit(self.emotion_name, 100)
                    
                    if success and os.path.exists(audio_path):
                        self.preview_completed.emit(self.emotion_name, audio_path, True)
                    else:
                        self.preview_error.emit(self.emotion_name, "TTS generation failed")
                        
                except Exception as e:
                    self.preview_error.emit(self.emotion_name, f"TTS error: {str(e)}")
            else:
                # Simulate preview cho demo
                time.sleep(1.5)
                self.preview_progress.emit(self.emotion_name, 50)
                time.sleep(1.0)
                self.preview_progress.emit(self.emotion_name, 100)
                
                self.preview_completed.emit(self.emotion_name, "simulated_preview.wav", False)
                
        except Exception as e:
            self.preview_error.emit(self.emotion_name, str(e))

class EmotionConfigTab(QWidget):
    """Emotion Configuration Tab với Table Format cải tiến"""
    
    def __init__(self):
        super().__init__()
        self.emotion_manager = EmotionConfigManager()
        self.preview_threads = {}  # Track active preview threads
        self.setup_ui()
        self.load_emotions_to_table()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🎭 Cấu hình Cảm xúc cho Voice Studio")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #007AFF; margin-bottom: 10px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_emotion_btn = QPushButton("➕ Thêm Emotion")
        self.add_emotion_btn.setStyleSheet("""
            QPushButton {
                background-color: #28CD41;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #25B83A;
            }
        """)
        self.add_emotion_btn.clicked.connect(self.add_custom_emotion)
        header_layout.addWidget(self.add_emotion_btn)
        
        self.export_btn = QPushButton("📤 Export")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        self.export_btn.clicked.connect(self.export_config)
        header_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton("📥 Import")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E6850E;
            }
        """)
        self.import_btn.clicked.connect(self.import_config)
        header_layout.addWidget(self.import_btn)
        
        layout.addLayout(header_layout)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("🔍 Lọc theo category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(["Tất cả", "neutral", "positive", "negative", "dramatic", "special"])
        self.category_filter.currentTextChanged.connect(self.filter_emotions)
        filter_layout.addWidget(self.category_filter)
        
        self.show_custom_only = QCheckBox("Chỉ hiện custom emotions")
        self.show_custom_only.toggled.connect(self.filter_emotions)
        filter_layout.addWidget(self.show_custom_only)
        
        filter_layout.addStretch()
        
        # Statistics
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #666; font-size: 12px;")
        filter_layout.addWidget(self.stats_label)
        
        layout.addLayout(filter_layout)
        
        # Main table với cải tiến + reset column
        self.emotions_table = QTableWidget()
        self.emotions_table.setColumnCount(10)  # Tăng thêm 1 cột cho reset
        
        headers = [
            "🎭 Emotion Name",      # 0
            "📝 Description",       # 1  
            "🏷️ Category",         # 2
            "🎯 Exaggeration",      # 3
            "⚖️ CFG Weight",       # 4
            "🌡️ Temperature",      # 5
            "⚡ Speed",            # 6
            "🔄 Reset",            # 7 - NEW reset column
            "🎵 Preview",          # 8
            "⚙️ Actions"          # 9
        ]
        
        self.emotions_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths với reset column
        header = self.emotions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Name
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Description
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # Category
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Exaggeration
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # CFG Weight
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Temperature
        header.setSectionResizeMode(6, QHeaderView.Fixed)  # Speed
        header.setSectionResizeMode(7, QHeaderView.Fixed)  # Reset
        header.setSectionResizeMode(8, QHeaderView.Fixed)  # Preview
        header.setSectionResizeMode(9, QHeaderView.Fixed)  # Actions
        
        # Set specific widths
        self.emotions_table.setColumnWidth(0, 150)  # Name
        self.emotions_table.setColumnWidth(2, 110)  # Category
        self.emotions_table.setColumnWidth(3, 120)  # Exaggeration
        self.emotions_table.setColumnWidth(4, 120)  # CFG Weight
        self.emotions_table.setColumnWidth(5, 120)  # Temperature
        self.emotions_table.setColumnWidth(6, 100)  # Speed
        self.emotions_table.setColumnWidth(7, 60)   # Reset
        self.emotions_table.setColumnWidth(8, 100)  # Preview
        self.emotions_table.setColumnWidth(9, 80)   # Actions
        
        # Cải thiện row height và table styling
        self.emotions_table.setAlternatingRowColors(True)
        self.emotions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.emotions_table.verticalHeader().setDefaultSectionSize(45)  # Tăng row height
        self.emotions_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #f1f3f4;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        layout.addWidget(self.emotions_table)
        
        # Status bar
        self.status_label = QLabel("✅ Sẵn sàng")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 6px 10px;
                border-radius: 4px;
                color: #28CD41;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
    
    def load_emotions_to_table(self):
        """Load tất cả emotions vào table với styling cải tiến"""
        all_emotions = self.emotion_manager.get_all_emotions()
        
        self.emotions_table.setRowCount(len(all_emotions))
        
        row = 0
        for emotion_name, emotion in all_emotions.items():
            is_custom = emotion_name in self.emotion_manager.custom_emotions
            
            # Column 0: Emotion Name - sửa font weight và màu chữ
            name_item = QTableWidgetItem(emotion_name)
            # Font thường không in đậm theo yêu cầu
            name_item.setFont(QFont("Arial", 10, QFont.Normal))
            if is_custom:
                name_item.setBackground(QColor("#E8F5E8"))  # Light green for custom
                name_item.setForeground(QColor("#000000"))  # Đen cho dễ đọc
            else:
                name_item.setBackground(QColor("#E3F2FD"))  # Light blue for default
                name_item.setForeground(QColor("#000000"))  # Đen cho dễ đọc
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Read-only
            self.emotions_table.setItem(row, 0, name_item)
            
            # Column 1: Description
            desc_item = QTableWidgetItem(emotion.description)
            desc_item.setFont(QFont("Arial", 9))  # Smaller font cho description
            if not is_custom:
                desc_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Read-only for default
            self.emotions_table.setItem(row, 1, desc_item)
            
            # Column 2: Category với sizing phù hợp
            category_combo = QComboBox()
            category_combo.addItems(["neutral", "positive", "negative", "dramatic", "special"])
            category_combo.setCurrentText(emotion.category)
            category_combo.setMinimumHeight(30)  # Đảm bảo height đủ
            category_combo.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 10px;
                }
                QComboBox::drop-down {
                    width: 20px;
                }
            """)
            if not is_custom:
                category_combo.setEnabled(False)  # Read-only for default
            else:
                category_combo.currentTextChanged.connect(
                    lambda text, name=emotion_name: self.update_emotion_parameter(name, 'category', text)
                )
            self.emotions_table.setCellWidget(row, 2, category_combo)
            
            # Column 3: Exaggeration
            exag_spinbox = QDoubleSpinBox()
            exag_spinbox.setRange(0.0, 2.5)
            exag_spinbox.setSingleStep(0.1)
            exag_spinbox.setDecimals(2)
            exag_spinbox.setValue(emotion.exaggeration)
            exag_spinbox.setMinimumHeight(28)
            exag_spinbox.setStyleSheet("font-size: 10px; padding: 2px;")
            exag_spinbox.valueChanged.connect(
                lambda value, name=emotion_name: self.update_emotion_parameter(name, 'exaggeration', value)
            )
            self.emotions_table.setCellWidget(row, 3, exag_spinbox)
            
            # Column 4: CFG Weight
            cfg_spinbox = QDoubleSpinBox()
            cfg_spinbox.setRange(0.0, 1.0)
            cfg_spinbox.setSingleStep(0.05)
            cfg_spinbox.setDecimals(2)
            cfg_spinbox.setValue(emotion.cfg_weight)
            cfg_spinbox.setMinimumHeight(28)
            cfg_spinbox.setStyleSheet("font-size: 10px; padding: 2px;")
            cfg_spinbox.valueChanged.connect(
                lambda value, name=emotion_name: self.update_emotion_parameter(name, 'cfg_weight', value)
            )
            self.emotions_table.setCellWidget(row, 4, cfg_spinbox)
            
            # Column 5: Temperature
            temp_spinbox = QDoubleSpinBox()
            temp_spinbox.setRange(0.1, 1.5)
            temp_spinbox.setSingleStep(0.1)
            temp_spinbox.setDecimals(2)
            temp_spinbox.setValue(emotion.temperature)
            temp_spinbox.setMinimumHeight(28)
            temp_spinbox.setStyleSheet("font-size: 10px; padding: 2px;")
            temp_spinbox.valueChanged.connect(
                lambda value, name=emotion_name: self.update_emotion_parameter(name, 'temperature', value)
            )
            self.emotions_table.setCellWidget(row, 5, temp_spinbox)
            
            # Column 6: Speed
            speed_spinbox = QDoubleSpinBox()
            speed_spinbox.setRange(0.5, 2.0)
            speed_spinbox.setSingleStep(0.1)
            speed_spinbox.setDecimals(1)
            speed_spinbox.setValue(emotion.speed)
            speed_spinbox.setMinimumHeight(28)
            speed_spinbox.setStyleSheet("font-size: 10px; padding: 2px;")
            speed_spinbox.valueChanged.connect(
                lambda value, name=emotion_name: self.update_emotion_parameter(name, 'speed', value)
            )
            self.emotions_table.setCellWidget(row, 6, speed_spinbox)
            
            # Column 7: Reset Button - reset về giá trị ban đầu
            reset_btn = QPushButton("🔄")
            reset_btn.setFixedSize(30, 30)  # Size gọn gàng
            reset_btn.setToolTip(f"Reset {emotion_name} về giá trị ban đầu")
            reset_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF6B35;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #E55A2B;
                }
                QPushButton:pressed {
                    background-color: #CC4C26;
                }
            """)
            reset_btn.clicked.connect(lambda: self.reset_emotion_to_default(emotion_name))
            self.emotions_table.setCellWidget(row, 7, reset_btn)
            
            # Column 8: Preview Button - compact và gọn gàng
            preview_btn = QPushButton("🎵")
            preview_btn.setFixedSize(35, 35)  # Size cố định gọn gàng
            preview_btn.setToolTip(f"Preview {emotion_name}")
            preview_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6366F1;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4F46E5;
                }
                QPushButton:pressed {
                    background-color: #3730A3;
                }
                QPushButton:disabled {
                    background-color: #D1D5DB;
                    color: #6B7280;
                }
            """)
            preview_btn.clicked.connect(lambda checked, name=emotion_name: self.preview_emotion(name))
            self.emotions_table.setCellWidget(row, 8, preview_btn)  # Cập nhật index từ 7 → 8
            
            # Column 9: Actions - chỉ icon gọn gàng
            if is_custom:
                delete_btn = QPushButton("🗑")
                delete_btn.setFixedSize(30, 30)  # Size nhỏ gọn
                delete_btn.setToolTip(f"Xóa {emotion_name}")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #EF4444;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #DC2626;
                    }
                    QPushButton:pressed {
                        background-color: #B91C1C;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, name=emotion_name: self.delete_emotion(name))
                self.emotions_table.setCellWidget(row, 9, delete_btn)  # Cập nhật index từ 8 → 9
            else:
                # Default emotions: show locked icon
                locked_label = QLabel("🔒")
                locked_label.setAlignment(Qt.AlignCenter)
                locked_label.setToolTip("Emotion mặc định - không thể xóa")
                locked_label.setStyleSheet("color: #9CA3AF; font-size: 14px;")
                self.emotions_table.setCellWidget(row, 9, locked_label)  # Cập nhật index từ 8 → 9
            
            row += 1
        
        self.update_statistics()
    
    def update_emotion_parameter(self, emotion_name: str, parameter: str, value):
        """Cập nhật parameter của emotion"""
        try:
            # Cập nhật trong emotion manager
            kwargs = {parameter: value}
            self.emotion_manager.modify_emotion(emotion_name, **kwargs)
            
            # Lưu custom emotions
            if emotion_name in self.emotion_manager.custom_emotions:
                self.emotion_manager.save_custom_emotions()
            
            self.update_status(f"✅ Cập nhật {emotion_name}: {parameter}={value}")
            
        except Exception as e:
            self.update_status(f"❌ Lỗi cập nhật {emotion_name}: {str(e)}")
    
    def preview_emotion(self, emotion_name: str):
        """Preview emotion với âm thanh thật - cải thiện error handling"""
        try:
            # Get current parameters
            emotion = self.emotion_manager.get_all_emotions()[emotion_name]
            parameters = {
                'exaggeration': emotion.exaggeration,
                'cfg_weight': emotion.cfg_weight,
                'temperature': emotion.temperature,
                'speed': emotion.speed
            }
            
            # Find preview button
            preview_btn = None
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    preview_btn = self.emotions_table.cellWidget(row, 8)  # Cập nhật từ 7 → 8
                    break
            
            if preview_btn:
                # Update button state
                preview_btn.setText("⏳")
                preview_btn.setEnabled(False)
                preview_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F59E0B;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                """)
                
                # Start preview thread
                self.preview_threads[emotion_name] = AudioPreviewThread(emotion_name, parameters)
                thread = self.preview_threads[emotion_name]
                
                thread.preview_completed.connect(lambda name, path, success: self.on_preview_completed(name, path, success))
                thread.preview_error.connect(lambda name, error: self.on_preview_error(name, error))
                
                thread.start()
                
                self.update_status(f"🎵 Đang tạo preview cho {emotion_name}...")
            
        except Exception as e:
            self.update_status(f"❌ Lỗi preview {emotion_name}: {str(e)}")
    
    def on_preview_completed(self, emotion_name: str, audio_path: str, is_real: bool):
        """Xử lý khi preview hoàn thành"""
        try:
            # Reset UI
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    preview_btn = self.emotions_table.cellWidget(row, 8)
                    if preview_btn:
                        preview_btn.setText("🎵")
                        preview_btn.setEnabled(True)
                        preview_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #6366F1;
                                color: white;
                                border: none;
                                border-radius: 6px;
                                font-size: 14px;
                                font-weight: bold;
                            }
                            QPushButton:hover {
                                background-color: #4F46E5;
                            }
                        """)
                    break
            
            # Play audio nếu có
            if is_real and os.path.exists(audio_path):
                # Mở file audio với default player
                import subprocess
                import platform
                
                try:
                    system = platform.system()
                    if system == "Windows":
                        os.startfile(audio_path)
                    elif system == "Darwin":  # macOS
                        subprocess.run(["open", audio_path])
                    else:  # Linux
                        subprocess.run(["xdg-open", audio_path])
                    
                    self.update_status(f"🎵 Preview {emotion_name} hoàn thành - đang phát âm thanh")
                except Exception as e:
                    self.update_status(f"❌ Không thể phát audio: {str(e)}")
                    
            else:
                # Simulated preview với thông tin chi tiết
                emotion_details = self.emotion_manager.get_all_emotions()[emotion_name]
                QMessageBox.information(
                    self,
                    f"🎵 Preview Simulation: {emotion_name}",
                    f"Preview simulation hoàn thành!\n\n"
                    f"🎭 Emotion: {emotion_name}\n"
                    f"📝 Description: {emotion_details.description}\n"
                    f"🏷️ Category: {emotion_details.category}\n"
                    f"🎯 Exaggeration: {emotion_details.exaggeration:.2f}\n"
                    f"⚖️ CFG Weight: {emotion_details.cfg_weight:.2f}\n"
                    f"🌡️ Temperature: {emotion_details.temperature:.2f}\n"
                    f"⚡ Speed: {emotion_details.speed:.1f}\n\n"
                    f"💡 Để nghe preview thật, cần TTS engine hoạt động."
                )
                
                self.update_status(f"✅ Preview simulation {emotion_name} hoàn thành")
            
            # Cleanup thread
            if emotion_name in self.preview_threads:
                del self.preview_threads[emotion_name]
                
        except Exception as e:
            self.update_status(f"❌ Lỗi xử lý preview {emotion_name}: {str(e)}")
    
    def on_preview_error(self, emotion_name: str, error: str):
        """Xử lý lỗi preview"""
        # Reset UI
        for row in range(self.emotions_table.rowCount()):
            name_item = self.emotions_table.item(row, 0)
            if name_item and name_item.text() == emotion_name:
                preview_btn = self.emotions_table.cellWidget(row, 8)
                if preview_btn:
                    preview_btn.setText("🎵")
                    preview_btn.setEnabled(True)
                    preview_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #6366F1;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            font-size: 14px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #4F46E5;
                        }
                    """)
                break
        
        # Cleanup thread
        if emotion_name in self.preview_threads:
            del self.preview_threads[emotion_name]
        
        # Show error with fallback simulation
        reply = QMessageBox.question(
            self, 
            "❌ Preview Error", 
            f"Lỗi tạo preview thật cho {emotion_name}:\n{error}\n\nBạn có muốn xem preview simulation không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Show simulation fallback
            emotion_details = self.emotion_manager.get_all_emotions()[emotion_name]
            QMessageBox.information(
                self,
                f"🎵 Preview Simulation: {emotion_name}",
                f"Preview simulation cho {emotion_name}:\n\n"
                f"🎭 Emotion: {emotion_name}\n"
                f"📝 Description: {emotion_details.description}\n"
                f"🎯 Exaggeration: {emotion_details.exaggeration:.2f}\n"
                f"⚖️ CFG Weight: {emotion_details.cfg_weight:.2f}\n"
                f"🌡️ Temperature: {emotion_details.temperature:.2f}\n"
                f"⚡ Speed: {emotion_details.speed:.1f}"
            )
        
        self.update_status(f"❌ Preview {emotion_name} thất bại - hiển thị simulation")
    
    def add_custom_emotion(self):
        """Thêm emotion tùy chỉnh mới"""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Thêm Emotion Mới")
        dialog.setModal(True)
        dialog.resize(400, 350)
        
        layout = QVBoxLayout(dialog)
        
        # Form inputs
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("tên_emotion_mới")
        form_layout.addRow("🎭 Tên Emotion:", name_input)
        
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Mô tả emotion này...")
        form_layout.addRow("📝 Mô tả:", desc_input)
        
        category_combo = QComboBox()
        category_combo.addItems(["neutral", "positive", "negative", "dramatic", "special"])
        form_layout.addRow("🏷️ Category:", category_combo)
        
        exag_spinbox = QDoubleSpinBox()
        exag_spinbox.setRange(0.0, 2.5)
        exag_spinbox.setSingleStep(0.1)
        exag_spinbox.setValue(1.0)
        form_layout.addRow("🎯 Exaggeration:", exag_spinbox)
        
        cfg_spinbox = QDoubleSpinBox()
        cfg_spinbox.setRange(0.0, 1.0)
        cfg_spinbox.setSingleStep(0.05)
        cfg_spinbox.setValue(0.5)
        form_layout.addRow("⚖️ CFG Weight:", cfg_spinbox)
        
        temp_spinbox = QDoubleSpinBox()
        temp_spinbox.setRange(0.1, 1.5)
        temp_spinbox.setSingleStep(0.1)
        temp_spinbox.setValue(0.7)
        form_layout.addRow("🌡️ Temperature:", temp_spinbox)
        
        speed_spinbox = QDoubleSpinBox()
        speed_spinbox.setRange(0.5, 2.0)
        speed_spinbox.setSingleStep(0.1)
        speed_spinbox.setValue(1.0)
        form_layout.addRow("⚡ Speed:", speed_spinbox)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        create_btn = QPushButton("✅ Tạo Emotion")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #28CD41;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        
        cancel_btn = QPushButton("❌ Hủy")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(create_btn)
        layout.addLayout(buttons_layout)
        
        def create_emotion():
            name = name_input.text().strip()
            description = desc_input.text().strip()
            
            if not name:
                QMessageBox.warning(dialog, "Thiếu thông tin", "Vui lòng nhập tên emotion!")
                return
            
            if name in self.emotion_manager.get_all_emotions():
                QMessageBox.warning(dialog, "Trùng tên", f"Emotion '{name}' đã tồn tại!")
                return
            
            try:
                self.emotion_manager.create_custom_emotion(
                    name=name,
                    description=description or f"Custom emotion: {name}",
                    category=category_combo.currentText(),
                    exaggeration=exag_spinbox.value(),
                    cfg_weight=cfg_spinbox.value(),
                    temperature=temp_spinbox.value(),
                    speed=speed_spinbox.value()
                )
                
                dialog.accept()
                self.load_emotions_to_table()  # Reload table
                self.update_status(f"✅ Đã tạo emotion '{name}'")
                
            except Exception as e:
                QMessageBox.critical(dialog, "Lỗi", f"Không thể tạo emotion: {str(e)}")
        
        create_btn.clicked.connect(create_emotion)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def delete_emotion(self, emotion_name: str):
        """Xóa custom emotion"""
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa emotion '{emotion_name}'?\n\nHành động này không thể hoàn tác.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if self.emotion_manager.delete_custom_emotion(emotion_name):
                    self.load_emotions_to_table()  # Reload table
                    self.update_status(f"✅ Đã xóa emotion '{emotion_name}'")
                else:
                    self.update_status(f"❌ Không thể xóa emotion '{emotion_name}'")
            except Exception as e:
                self.update_status(f"❌ Lỗi xóa emotion: {str(e)}")
    
    def filter_emotions(self):
        """Lọc emotions theo category và custom"""
        category_filter = self.category_filter.currentText()
        show_custom_only = self.show_custom_only.isChecked()
        
        for row in range(self.emotions_table.rowCount()):
            name_item = self.emotions_table.item(row, 0)
            if name_item:
                emotion_name = name_item.text()
                emotion = self.emotion_manager.get_all_emotions().get(emotion_name)
                
                if emotion:
                    # Category filter
                    category_match = (category_filter == "Tất cả" or emotion.category == category_filter)
                    
                    # Custom filter
                    is_custom = emotion_name in self.emotion_manager.custom_emotions
                    custom_match = (not show_custom_only or is_custom)
                    
                    # Show/hide row
                    show_row = category_match and custom_match
                    self.emotions_table.setRowHidden(row, not show_row)
    
    def export_config(self):
        """Export emotion configuration"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Emotion Config",
                f"emotion_config_{int(time.time())}.json",
                "JSON Files (*.json)"
            )
            
            if file_path:
                self.emotion_manager.export_emotion_config(file_path)
                self.update_status(f"✅ Đã export: {os.path.basename(file_path)}")
                
        except Exception as e:
            self.update_status(f"❌ Lỗi export: {str(e)}")
    
    def import_config(self):
        """Import emotion configuration"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import Emotion Config", "",
                "JSON Files (*.json)"
            )
            
            if file_path:
                if self.emotion_manager.import_emotion_config(file_path):
                    self.load_emotions_to_table()  # Reload table
                    self.update_status(f"✅ Đã import: {os.path.basename(file_path)}")
                else:
                    self.update_status("❌ Import thất bại")
                    
        except Exception as e:
            self.update_status(f"❌ Lỗi import: {str(e)}")
    
    def update_statistics(self):
        """Cập nhật thống kê emotions"""
        try:
            stats = self.emotion_manager.get_emotion_statistics()
            
            stats_text = (
                f"📊 Total: {stats['total_emotions']} | "
                f"🎭 Default: {stats['default_emotions']} | "
                f"✨ Custom: {stats['custom_emotions']} | "
                f"📦 Presets: {stats['total_presets']}"
            )
            
            self.stats_label.setText(stats_text)
            
        except Exception:
            self.stats_label.setText("❌ Lỗi thống kê")
    
    def update_status(self, message: str):
        """Cập nhật status message"""
        self.status_label.setText(message)
        QTimer.singleShot(3000, lambda: self.status_label.setText("✅ Sẵn sàng"))
    
    def connect_signals(self):
        """Kết nối signals"""
        # Filter signals already connected in setup_ui
        pass 

    def reset_emotion_to_default(self, emotion_name: str):
        """Reset emotion về giá trị gốc của cảm xúc đó cụ thể"""
        try:
            # Lấy giá trị gốc của emotion cụ thể từ default_emotions
            if emotion_name not in self.emotion_manager.default_emotions:
                QMessageBox.warning(
                    self, 
                    "Không thể Reset", 
                    f"Không tìm thấy giá trị gốc cho '{emotion_name}'.\n"
                    f"Emotion này có thể là custom emotion hoặc không có trong default emotions."
                )
                return
            
            # Lấy emotion gốc
            original_emotion = self.emotion_manager.default_emotions[emotion_name]
            default_values = {
                'exaggeration': original_emotion.exaggeration,
                'cfg_weight': original_emotion.cfg_weight,
                'temperature': original_emotion.temperature,
                'speed': original_emotion.speed
            }
            
            # DEBUG: In giá trị gốc ra console
            print(f"\n🔄 DEBUG RESET {emotion_name}:")
            print(f"   📝 Original Description: {original_emotion.description}")
            print(f"   🏷️ Original Category: {original_emotion.category}")
            print(f"   📊 Original Values:")
            print(f"      🎯 Exaggeration: {default_values['exaggeration']:.2f}")
            print(f"      ⚖️ CFG Weight: {default_values['cfg_weight']:.2f}")
            print(f"      🌡️ Temperature: {default_values['temperature']:.2f}")
            print(f"      ⚡ Speed: {default_values['speed']:.1f}")
            
            # Lấy giá trị hiện tại để so sánh
            current_emotion = self.emotion_manager.get_all_emotions()[emotion_name]
            print(f"   📈 Current Values:")
            print(f"      🎯 Exaggeration: {current_emotion.exaggeration:.2f}")
            print(f"      ⚖️ CFG Weight: {current_emotion.cfg_weight:.2f}")
            print(f"      🌡️ Temperature: {current_emotion.temperature:.2f}")
            print(f"      ⚡ Speed: {current_emotion.speed:.1f}")
            
            # Confirm dialog với giá trị gốc cụ thể
            dialog_text = (
                f"Bạn có chắc chắn muốn reset '{emotion_name}' về giá trị gốc?\n\n"
                f"📝 Emotion gốc: {original_emotion.description}\n"
                f"🏷️ Category: {original_emotion.category}\n\n"
                f"📊 Giá trị gốc sẽ được áp dụng:\n"
                f"🎯 Exaggeration: {default_values['exaggeration']:.2f}\n"
                f"⚖️ CFG Weight: {default_values['cfg_weight']:.2f}\n"
                f"🌡️ Temperature: {default_values['temperature']:.2f}\n"
                f"⚡ Speed: {default_values['speed']:.1f}\n\n"
                f"💡 Giá trị hiện tại:\n"
                f"🎯 Exaggeration: {current_emotion.exaggeration:.2f}\n"
                f"⚖️ CFG Weight: {current_emotion.cfg_weight:.2f}\n"
                f"🌡️ Temperature: {current_emotion.temperature:.2f}\n"
                f"⚡ Speed: {current_emotion.speed:.1f}"
            )
            
            reply = QMessageBox.question(
                self,
                "Reset Emotion về Gốc",
                dialog_text,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Update emotion parameters về giá trị gốc
                self.emotion_manager.modify_emotion(emotion_name, **default_values)
                
                # Save nếu là custom emotion (đã modify từ default)
                if emotion_name in self.emotion_manager.custom_emotions:
                    self.emotion_manager.save_custom_emotions()
                
                # Update UI trong table
                for row in range(self.emotions_table.rowCount()):
                    name_item = self.emotions_table.item(row, 0)
                    if name_item and name_item.text() == emotion_name:
                        # Update spinboxes với giá trị gốc cụ thể
                        exag_spinbox = self.emotions_table.cellWidget(row, 3)
                        if exag_spinbox:
                            exag_spinbox.setValue(default_values['exaggeration'])
                        
                        cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                        if cfg_spinbox:
                            cfg_spinbox.setValue(default_values['cfg_weight'])
                        
                        temp_spinbox = self.emotions_table.cellWidget(row, 5)
                        if temp_spinbox:
                            temp_spinbox.setValue(default_values['temperature'])
                        
                        speed_spinbox = self.emotions_table.cellWidget(row, 6)
                        if speed_spinbox:
                            speed_spinbox.setValue(default_values['speed'])
                        
                        break
                
                self.update_status(f"✅ Reset {emotion_name} về giá trị gốc: Exag={default_values['exaggeration']:.2f}, CFG={default_values['cfg_weight']:.2f}")
                
        except Exception as e:
            self.update_status(f"❌ Lỗi reset {emotion_name}: {str(e)}")
            QMessageBox.warning(self, "Lỗi Reset", f"Không thể reset {emotion_name} về giá trị gốc:\n{str(e)}") 