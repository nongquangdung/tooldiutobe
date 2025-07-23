#!/usr/bin/env python3
"""
[THEATER] EMOTION CONFIGURATION TAB - TABLE FORMAT (IMPROVED)
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
    QSpinBox, QDoubleSpinBox, QProgressBar, QProgressDialog
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.unified_emotion_system import UnifiedEmotionSystem
from core.unified_emotion_helpers import get_emotion_parameters

# Import TTS provider để preview âm thanh thật
try:
    from tts.real_chatterbox_provider import RealChatterboxProvider
    PREVIEW_AVAILABLE = True
except ImportError:
    PREVIEW_AVAILABLE = False
    print("[WARNING] TTS provider not available - preview will be simulated")

import logging
logger = logging.getLogger(__name__)

class AudioPreviewThread(QThread):
    """Thread để generate preview âm thanh thật"""
    preview_completed = Signal(str, str, bool)  # emotion_name, audio_path, success
    preview_progress = Signal(str, int)  # emotion_name, progress_percent
    preview_error = Signal(str, str)  # emotion_name, error_message
    
    # High-quality emotion prompts for better preview
    EMOTION_PROMPTS = {
        "admiring": "Wow... I've never seen anything quite so beautiful. The way it moves, the colors, the elegance—it's absolutely breathtaking. I could stand here and watch it for hours.",
        "angry": "Don't talk to me like that again! I've had enough of your lies and your disrespect. If you cross the line one more time, I swear I won't hold back.",
        "anxious": "I... I don't know if this is going to work. Everything feels like it's falling apart and I can't catch a breath. What if I mess it up again?",
        "bewildered": "Wait, what just happened? I walked in and suddenly everyone was gone—it doesn't make any sense. Am I missing something obvious?",
        "calm": "Everything is going to be just fine. Let's take a deep breath and approach this with clarity. There's no need to rush.",
        "cheerful": "Good morning! Isn't it just a perfect day to start something new? I can't stop smiling, everything feels so full of energy and promise!",
        "cold": "I don't care what your excuse is. You made your decision, now deal with the consequences. Don't expect me to feel anything about it.",
        "commanding": "Stand back! I'm in control of this situation now. Do exactly as I say and no one will get hurt—this is not a request.",
        "confident": "I know exactly what I'm doing. I've prepared for this moment and I'm ready to show everyone what I'm capable of. There's no room for doubt.",
        "confused": "Wait, that doesn't add up. You said one thing yesterday and now it's completely different? I'm trying to understand but I'm lost here.",
        "contemplative": "Hm... It's strange how choices from years ago still echo today. I wonder what would have happened if I had chosen the other path.",
        "contemptuous": "Really? That's what you're proud of? It's laughable, honestly—I've seen better from someone half your age.",
        "disappointed": "I expected more from you. After everything we've been through, this is what it comes down to? It really hurts to see this.",
        "dramatic": "This is it—the final act, the climax of everything we've worked toward! Every decision has led to this moment of truth!",
        "encouraging": "You can do this—I believe in you! Even if it's hard, you're stronger than you think. Just take it step by step.",
        "excited": "Did you hear the news? This changes everything! I can barely sit still—I just want to jump up and celebrate!",
        "fearful": "No... please, don't go in there. Something feels wrong, like we're not alone. We should turn back while we still can.",
        "flirtatious": "Oh, you're such a tease. Every time you smile like that, it makes my heart skip a beat. You really know how to charm me.",
        "friendly": "Hey there! I'm so glad to see you again. Let's catch up—it's been way too long and I've missed this.",
        "happy": "I can't stop smiling—today's just perfect! Everything feels like it's going right, and I'm so grateful to be here.",
        "humorous": "So get this—he walks in wearing socks and sandals and says it's high fashion! I couldn't stop laughing for hours!",
        "innocent": "I didn't mean to cause any trouble... I was only trying to help. Please don't be mad, I really didn't know.",
        "mysterious": "They say if you follow the lantern light into the forest, you might never come back. But some say that's where secrets are revealed.",
        "neutral": "The report was submitted on time and everything is proceeding according to plan. Let me know if you need anything else.",
        "persuasive": "Look, I know you're hesitant, but just imagine the possibilities. This isn't just a good idea—it's the right one.",
        "playful": "Tag! You're it! Catch me if you can—but I bet you won't, I'm way too fast for you!",
        "pleading": "Please, just hear me out. I didn't mean for any of this to happen. I need you to understand—I'm begging you.",
        "romantic": "When I look into your eyes, everything else fades away. You make the world feel like it's standing still just for us.",
        "sad": "I tried everything... and yet here I am, alone again. It's like nothing I do ever makes a difference.",
        "sarcastic": "Oh, brilliant plan! What could possibly go wrong, right? Because that always works out *so well*.",
        "shy": "Um... hi. I didn't expect to run into you here. You look... nice. I mean, not that I've been looking—just... yeah.",
        "sleepy": "Mmm... just five more minutes. I stayed up too late again and now I can't keep my eyes open.",
        "soft": "Hey... you're okay now. Everything's going to be alright. Just rest, I've got you.",
        "surprised": "Whoa! That was totally unexpected. I had no idea that would happen—what a twist!",
        "suspenseful": "The lights flickered... then silence. Something—or someone—was out there, watching. Waiting.",
        "urgent": "Quick! There's no time to waste—we need to move now or it's going to be too late!",
        "whisper": "Shhh... keep your voice down. They might hear us. Every sound could give us away."
    }
    
    def __init__(self, emotion_name: str, parameters: dict):
        super().__init__()
        self.emotion_name = emotion_name
        self.parameters = parameters
        # Use high-quality prompt nếu có, fallback to generic
        self.preview_text = self.EMOTION_PROMPTS.get(
            emotion_name.lower(), 
            f"This is a preview of the {emotion_name} emotion with custom parameters."
        )
    
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
        self.unified_emotion_system = UnifiedEmotionSystem()
        self.preview_threads = {}  # Track active preview threads
        
        # Store original/default Inner Voice values for reset
        self.inner_voice_original_values = {}
        
        self.setup_ui()
        self.load_emotions_to_table()
        self.connect_signals()
        
        # Load emotions to table
        self.load_emotions_to_table()
        
        # Load inner voice config from file
        self.load_inner_voice_config_from_file()
        
        # Connect signals for auto-saving
        self.connect_inner_voice_signals()
        
        # Update statistics
        self.update_statistics()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title đã được xóa theo yêu cầu người dùng
        
        header_layout.addStretch()
        
        # Action buttons
        self.add_emotion_btn = QPushButton("[EMOJI] Thêm Emotion")
        self.add_emotion_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #28CD41;
                border: 1px solid #28CD41;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0FFF4;
                border-color: #25B83A;
            }
        """)
        self.add_emotion_btn.clicked.connect(self.add_custom_emotion)
        header_layout.addWidget(self.add_emotion_btn)
        
        self.export_btn = QPushButton("[EMOJI] Export")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #007AFF;
                border: 1px solid #007AFF;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
                border-color: #0056CC;
            }
        """)
        self.export_btn.clicked.connect(self.export_config)
        header_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton("[EMOJI] Import")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #FF9500;
                border: 1px solid #FF9500;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFF9F0;
                border-color: #E6850E;
            }
        """)
        self.import_btn.clicked.connect(self.import_config)
        header_layout.addWidget(self.import_btn)
        
        # Reset All button - đặt trước spacer
        self.reset_all_btn = QPushButton("[REFRESH] Reset All")
        self.reset_all_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #FF6B35;
                border: 1px solid #FF6B35;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFF5F5;
                border-color: #E55A2B;
            }
            QPushButton:pressed {
                background-color: #FED7CC;
                border-color: #CC4C26;
            }
        """)
        self.reset_all_btn.clicked.connect(self.reset_all_emotions_to_default)
        header_layout.addWidget(self.reset_all_btn)
        
        layout.addLayout(header_layout)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("[SEARCH] Lọc theo category:"))
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
            "[THEATER] Emotion Name",      # 0
            "[EDIT] Description",       # 1  
            "[EMOJI] Category",         # 2
            "[TARGET] Exaggeration",      # 3
            "[EMOJI] CFG Weight",       # 4
            "[EMOJI] Temperature",      # 5
            "[FAST] Speed",            # 6
            "[REFRESH] Reset",            # 7 - NEW reset column
            "[MUSIC] Preview",          # 8
            "[CONFIG] Actions"          # 9
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
        self.status_label = QLabel("[OK] Sẵn sàng")
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
        
        # === INNER VOICE CONFIG GROUP ===
        self.inner_voice_group = QGroupBox("Inner Voice (Thoại nội tâm)")
        self.inner_voice_group.setCheckable(True)
        self.inner_voice_group.setChecked(False)
        self.inner_voice_group.toggled.connect(self.on_inner_voice_toggle)
        inner_voice_layout = QVBoxLayout()

        # 3 type: light, deep, dreamy
        self.inner_voice_type_widgets = {}
        for type_name, label in [("light", "Nội tâm nhẹ (light)"), ("deep", "Nội tâm sâu (deep)"), ("dreamy", "Nội tâm cách âm (dreamy)")]:
            group = QGroupBox(label)
            group_layout = QHBoxLayout()
            # 4 thông số: delay, decay, gain, filter
            delay = QDoubleSpinBox(); delay.setRange(0, 2000); delay.setSuffix(" ms"); delay.setSingleStep(10)
            decay = QDoubleSpinBox(); decay.setRange(0, 1); decay.setSingleStep(0.01)
            gain = QDoubleSpinBox(); gain.setRange(0, 2); gain.setSingleStep(0.01)
            filter_edit = QLineEdit(); filter_edit.setPlaceholderText("FFmpeg filter string")
            group_layout.addWidget(QLabel("Delay:")); group_layout.addWidget(delay)
            group_layout.addWidget(QLabel("Decay:")); group_layout.addWidget(decay)
            group_layout.addWidget(QLabel("Gain:")); group_layout.addWidget(gain)
            group_layout.addWidget(QLabel("Filter:")); group_layout.addWidget(filter_edit)
            reset_btn = QPushButton("Reset mặc định"); reset_btn.clicked.connect(lambda _, t=type_name: self.reset_inner_voice_type(t))
            group_layout.addWidget(reset_btn)
<<<<<<< Updated upstream
=======
            preview_btn = QPushButton("[MUSIC] Preview")
            preview_btn.clicked.connect(lambda _, t=type_name: self.preview_inner_voice_type(t))
            group_layout.addWidget(preview_btn)
>>>>>>> Stashed changes
            group.setLayout(group_layout)
            inner_voice_layout.addWidget(group)
            self.inner_voice_type_widgets[type_name] = {
                "delay": delay, "decay": decay, "gain": gain, "filter": filter_edit, "reset": reset_btn, "group": group
            }
        
        self.inner_voice_group.setLayout(inner_voice_layout)
        layout.addWidget(self.inner_voice_group)
    
    def load_emotions_to_table(self):
        """Load tất cả emotions vào table với styling cải tiến"""
        all_emotions = self.unified_emotion_system.get_all_emotions()
        
        self.emotions_table.setRowCount(len(all_emotions))
        
        row = 0
        for emotion_name, emotion in all_emotions.items():
            # All emotions are editable in unified system
            is_custom = False
            
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
            
            # Column 7: Reset Button - reset về giá trị ban đầu (Center aligned)
            reset_btn = QPushButton("[REFRESH]")
            reset_btn.setFixedSize(30, 30)  # Size gọn gàng
            reset_btn.setToolTip(f"Reset {emotion_name} về giá trị ban đầu")
            reset_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #FF6B35;
                    border: 1px solid #FF6B35;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FFF5F5;
                    border-color: #E55A2B;
                }
                QPushButton:pressed {
                    background-color: #FED7CC;
                    border-color: #CC4C26;
                }
            """)
            reset_btn.clicked.connect(lambda checked, name=emotion_name: self.reset_emotion_to_default(name))
            
            # Tạo wrapper widget để center button
            reset_widget = QWidget()
            reset_layout = QHBoxLayout(reset_widget)
            reset_layout.setContentsMargins(0, 0, 0, 0)
            reset_layout.addStretch()
            reset_layout.addWidget(reset_btn)
            reset_layout.addStretch()
            self.emotions_table.setCellWidget(row, 7, reset_widget)
            
            # Column 8: Preview Button - compact và gọn gàng (Center aligned)
            preview_btn = QPushButton("[MUSIC]")
            preview_btn.setFixedSize(35, 35)  # Size cố định gọn gàng
            preview_btn.setToolTip(f"Preview {emotion_name}")
            preview_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #6366F1;
                    border: 1px solid #6366F1;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #F0F0FF;
                    border-color: #4F46E5;
                }
                QPushButton:pressed {
                    background-color: #E0E0FF;
                    border-color: #3730A3;
                }
                QPushButton:disabled {
                    background-color: #F8F9FA;
                    color: #6B7280;
                    border-color: #D1D5DB;
                }
            """)
            preview_btn.clicked.connect(lambda checked, name=emotion_name: self.preview_emotion(name))
            
            # Tạo wrapper widget để center button
            preview_widget = QWidget()
            preview_layout = QHBoxLayout(preview_widget)
            preview_layout.setContentsMargins(0, 0, 0, 0)
            preview_layout.addStretch()
            preview_layout.addWidget(preview_btn)
            preview_layout.addStretch()
            self.emotions_table.setCellWidget(row, 8, preview_widget)  # Cập nhật index từ 7 → 8
            
            # Column 9: Actions - chỉ icon gọn gàng (Center aligned)
            if is_custom:
                delete_btn = QPushButton("[EMOJI]")
                delete_btn.setFixedSize(30, 30)  # Size nhỏ gọn
                delete_btn.setToolTip(f"Xóa {emotion_name}")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #EF4444;
                        border: 1px solid #EF4444;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #FEF2F2;
                        border-color: #DC2626;
                    }
                    QPushButton:pressed {
                        background-color: #FEE2E2;
                        border-color: #B91C1C;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, name=emotion_name: self.delete_emotion(name))
                
                # Tạo wrapper widget để center button
                delete_widget = QWidget()
                delete_layout = QHBoxLayout(delete_widget)
                delete_layout.setContentsMargins(0, 0, 0, 0)
                delete_layout.addStretch()
                delete_layout.addWidget(delete_btn)
                delete_layout.addStretch()
                self.emotions_table.setCellWidget(row, 9, delete_widget)  # Cập nhật index từ 8 → 9
            else:
                # Default emotions: show locked icon (already centered)
                locked_label = QLabel("[EMOJI]")
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
            # Unified system handles parameter updates automatically
            pass
            
            self.update_status(f"[OK] Cập nhật {emotion_name}: {parameter}={value}")
            
        except Exception as e:
            self.update_status(f"[EMOJI] Error cập nhật {emotion_name}: {str(e)}")
    
    def preview_emotion(self, emotion_name: str):
        """Preview emotion với âm thanh thật - sử dụng real-time parameters từ UI"""
        try:
            # Get REAL-TIME parameters từ UI spinboxes, không phải từ unified system
            parameters = {}
            
            # Find row và lấy current values từ spinboxes
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    # Get real-time values từ UI widgets
                    exag_spinbox = self.emotions_table.cellWidget(row, 3)
                    cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                    temp_spinbox = self.emotions_table.cellWidget(row, 5)
                    speed_spinbox = self.emotions_table.cellWidget(row, 6)
                    
                    parameters = {
                        'exaggeration': exag_spinbox.value() if exag_spinbox else 1.0,
                        'cfg_weight': cfg_spinbox.value() if cfg_spinbox else 0.6,
                        'temperature': temp_spinbox.value() if temp_spinbox else 0.8,
                        'speed': speed_spinbox.value() if speed_spinbox else 1.0
                    }
                    
                    # Get preview text being used
                    preview_text = AudioPreviewThread.EMOTION_PROMPTS.get(
                        emotion_name.lower(), 
                        f"This is a preview of the {emotion_name} emotion with custom parameters."
                    )
                    
                    print(f"\n[MUSIC] PREVIEW {emotion_name} với REAL-TIME parameters:")
                    print(f"   [TARGET] Exaggeration: {parameters['exaggeration']:.2f} (từ UI)")
                    print(f"   [EMOJI] CFG Weight: {parameters['cfg_weight']:.2f} (từ UI)")
                    print(f"   [EMOJI] Temperature: {parameters['temperature']:.2f} (từ UI)")
                    print(f"   [FAST] Speed: {parameters['speed']:.1f} (từ UI)")
                    print(f"   [EDIT] Text: \"{preview_text[:50]}...\" ({len(preview_text)} chars)")
                    break
            
            # Fallback nếu không tìm thấy row
            if not parameters:
                emotion = self.unified_emotion_system.get_all_emotions()[emotion_name]
                parameters = {
                    'exaggeration': emotion.exaggeration,
                    'cfg_weight': emotion.cfg_weight,
                    'temperature': emotion.temperature,
                    'speed': emotion.speed
                }
            print(f"\n[WARNING] FALLBACK: Sử dụng default parameters cho {emotion_name}")
            
            # Find preview button từ wrapper widget
            preview_btn = None
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    preview_widget = self.emotions_table.cellWidget(row, 8)  # Cập nhật từ 7 → 8
                    if preview_widget:
                        # Lấy preview button từ layout
                        layout = preview_widget.layout()
                        if layout and layout.count() > 1:
                            preview_btn = layout.itemAt(1).widget()  # Button ở vị trí giữa
                    break
            
            if preview_btn:
                # Update button state
                preview_btn.setText("⏳")
                preview_btn.setEnabled(False)
                preview_btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #F59E0B;
                        border: 1px solid #F59E0B;
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
                
                self.update_status(f"[MUSIC] Đang tạo preview cho {emotion_name}...")
            
        except Exception as e:
            self.update_status(f"[EMOJI] Error preview {emotion_name}: {str(e)}")
    
    def on_preview_completed(self, emotion_name: str, audio_path: str, is_real: bool):
        """Xử lý khi preview hoàn thành"""
        try:
            # Reset UI - lấy preview button từ wrapper widget
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    preview_widget = self.emotions_table.cellWidget(row, 8)
                    if preview_widget:
                        # Lấy preview button từ layout
                        layout = preview_widget.layout()
                        if layout and layout.count() > 1:
                            preview_btn = layout.itemAt(1).widget()  # Button ở vị trí giữa
                    if preview_btn:
                        preview_btn.setText("[MUSIC]")
                        preview_btn.setEnabled(True)
                        preview_btn.setStyleSheet("""
                            QPushButton {
                                        background-color: white;
                                        color: #6366F1;
                                        border: 1px solid #6366F1;
                                border-radius: 6px;
                                font-size: 14px;
                                font-weight: bold;
                            }
                            QPushButton:hover {
                                        background-color: #F0F0FF;
                                        border-color: #4F46E5;
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
                    
                    self.update_status(f"[MUSIC] Preview {emotion_name} hoàn thành - đang phát âm thanh")
                except Exception as e:
                    self.update_status(f"[EMOJI] Không thể phát audio: {str(e)}")
                    
            else:
                # Simulated preview với REAL-TIME parameters từ UI
                # Get current UI values
                current_params = {}
                emotion_details = self.unified_emotion_system.get_all_emotions()[emotion_name]
                
                for row in range(self.emotions_table.rowCount()):
                    name_item = self.emotions_table.item(row, 0)
                    if name_item and name_item.text() == emotion_name:
                        exag_spinbox = self.emotions_table.cellWidget(row, 3)
                        cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                        temp_spinbox = self.emotions_table.cellWidget(row, 5)
                        speed_spinbox = self.emotions_table.cellWidget(row, 6)
                        
                        current_params = {
                            'exaggeration': exag_spinbox.value() if exag_spinbox else emotion_details.exaggeration,
                            'cfg_weight': cfg_spinbox.value() if cfg_spinbox else emotion_details.cfg_weight,
                            'temperature': temp_spinbox.value() if temp_spinbox else emotion_details.temperature,
                            'speed': speed_spinbox.value() if speed_spinbox else emotion_details.speed
                        }
                        break
                
                # Use current UI values hoặc fallback
                if not current_params:
                    current_params = {
                        'exaggeration': emotion_details.exaggeration,
                        'cfg_weight': emotion_details.cfg_weight,
                        'temperature': emotion_details.temperature,
                        'speed': emotion_details.speed
                    }
                
                QMessageBox.information(
                    self,
                    f"[MUSIC] Preview Simulation: {emotion_name}",
                    f"Preview simulation với REAL-TIME parameters!\n\n"
                    f"[THEATER] Emotion: {emotion_name}\n"
                    f"[EDIT] Description: {emotion_details.description}\n"
                    f"[EMOJI] Category: {emotion_details.category}\n\n"
                    f"[TARGET] Exaggeration: {current_params['exaggeration']:.2f} (real-time)\n"
                    f"[EMOJI] CFG Weight: {current_params['cfg_weight']:.2f} (real-time)\n"
                    f"[EMOJI] Temperature: {current_params['temperature']:.2f} (real-time)\n"
                    f"[FAST] Speed: {current_params['speed']:.1f} (real-time)\n\n"
                    f"[IDEA] Parameters được lấy từ UI spinboxes hiện tại!"
                )
                
                self.update_status(f"[OK] Preview simulation {emotion_name} hoàn thành")
            
            # Cleanup thread
            if emotion_name in self.preview_threads:
                del self.preview_threads[emotion_name]
                
        except Exception as e:
            self.update_status(f"[EMOJI] Error xử lý preview {emotion_name}: {str(e)}")
    
    def on_preview_error(self, emotion_name: str, error: str):
        """Xử lý lỗi preview"""
        # Reset UI - lấy preview button từ wrapper widget
        for row in range(self.emotions_table.rowCount()):
            name_item = self.emotions_table.item(row, 0)
            if name_item and name_item.text() == emotion_name:
                preview_widget = self.emotions_table.cellWidget(row, 8)
                if preview_widget:
                    # Lấy preview button từ layout
                    layout = preview_widget.layout()
                    if layout and layout.count() > 1:
                        preview_btn = layout.itemAt(1).widget()  # Button ở vị trí giữa
                    break
            
            if preview_btn:
                preview_btn.setText("[MUSIC]")
                preview_btn.setEnabled(True)
                preview_btn.setStyleSheet("""
                    QPushButton {
                                    background-color: white;
                                    color: #6366F1;
                                    border: 1px solid #6366F1;
                            border-radius: 6px;
                            font-size: 14px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                                    background-color: #F0F0FF;
                                    border-color: #4F46E5;
                        }
                    """)
            
            # Cleanup thread
            if emotion_name in self.preview_threads:
                del self.preview_threads[emotion_name]
        
        # Show error with fallback simulation
        reply = QMessageBox.question(
            self, 
            "[EMOJI] Preview Error", 
            f"Error tạo preview thật cho {emotion_name}:\n{error}\n\nBạn có muốn xem preview simulation không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Show simulation fallback với real-time parameters
            emotion_details = self.unified_emotion_system.get_all_emotions()[emotion_name]
            
            # Get real-time parameters từ UI
            current_params = {}
            for row in range(self.emotions_table.rowCount()):
                name_item = self.emotions_table.item(row, 0)
                if name_item and name_item.text() == emotion_name:
                    exag_spinbox = self.emotions_table.cellWidget(row, 3)
                    cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                    temp_spinbox = self.emotions_table.cellWidget(row, 5)
                    speed_spinbox = self.emotions_table.cellWidget(row, 6)
                    
                    current_params = {
                        'exaggeration': exag_spinbox.value() if exag_spinbox else emotion_details.exaggeration,
                        'cfg_weight': cfg_spinbox.value() if cfg_spinbox else emotion_details.cfg_weight,
                        'temperature': temp_spinbox.value() if temp_spinbox else emotion_details.temperature,
                        'speed': speed_spinbox.value() if speed_spinbox else emotion_details.speed
                    }
                    break
            
            # Fallback nếu không tìm thấy
            if not current_params:
                current_params = {
                    'exaggeration': emotion_details.exaggeration,
                    'cfg_weight': emotion_details.cfg_weight,
                    'temperature': emotion_details.temperature,
                    'speed': emotion_details.speed
                }
            
            QMessageBox.information(
                self,
                f"[MUSIC] Preview Simulation: {emotion_name}",
                f"Preview simulation cho {emotion_name} (fallback):\n\n"
                f"[THEATER] Emotion: {emotion_name}\n"
                f"[EDIT] Description: {emotion_details.description}\n\n"
                f"[TARGET] Exaggeration: {current_params['exaggeration']:.2f} (real-time)\n"
                f"[EMOJI] CFG Weight: {current_params['cfg_weight']:.2f} (real-time)\n"
                f"[EMOJI] Temperature: {current_params['temperature']:.2f} (real-time)\n"
                f"[FAST] Speed: {current_params['speed']:.1f} (real-time)\n\n"
                f"[IDEA] Sử dụng parameters từ UI spinboxes!"
            )
        
        self.update_status(f"[EMOJI] Preview {emotion_name} thất bại - hiển thị simulation")
    
    def add_custom_emotion(self):
        """Thêm emotion tùy chỉnh mới"""
        dialog = QDialog(self)
        dialog.setWindowTitle("[EMOJI] Thêm Emotion Mới")
        dialog.setModal(True)
        dialog.resize(400, 350)
        
        layout = QVBoxLayout(dialog)
        
        # Form inputs
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("tên_emotion_mới")
        form_layout.addRow("[THEATER] Tên Emotion:", name_input)
        
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Mô tả emotion này...")
        form_layout.addRow("[EDIT] Mô tả:", desc_input)
        
        category_combo = QComboBox()
        category_combo.addItems(["neutral", "positive", "negative", "dramatic", "special"])
        form_layout.addRow("[EMOJI] Category:", category_combo)
        
        exag_spinbox = QDoubleSpinBox()
        exag_spinbox.setRange(0.0, 2.5)
        exag_spinbox.setSingleStep(0.1)
        exag_spinbox.setValue(1.0)
        form_layout.addRow("[TARGET] Exaggeration:", exag_spinbox)
        
        cfg_spinbox = QDoubleSpinBox()
        cfg_spinbox.setRange(0.0, 1.0)
        cfg_spinbox.setSingleStep(0.05)
        cfg_spinbox.setValue(0.5)
        form_layout.addRow("[EMOJI] CFG Weight:", cfg_spinbox)
        
        temp_spinbox = QDoubleSpinBox()
        temp_spinbox.setRange(0.1, 1.5)
        temp_spinbox.setSingleStep(0.1)
        temp_spinbox.setValue(0.7)
        form_layout.addRow("[EMOJI] Temperature:", temp_spinbox)
        
        speed_spinbox = QDoubleSpinBox()
        speed_spinbox.setRange(0.5, 2.0)
        speed_spinbox.setSingleStep(0.1)
        speed_spinbox.setValue(1.0)
        form_layout.addRow("[FAST] Speed:", speed_spinbox)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        create_btn = QPushButton("[OK] Tạo Emotion")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #28CD41;
                border: 1px solid #28CD41;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)
        
        cancel_btn = QPushButton("[EMOJI] Hủy")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #FF3B30;
                border: 1px solid #FF3B30;
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
            
            if name.lower() in self.unified_emotion_system.get_all_emotions():
                QMessageBox.warning(dialog, "Trùng tên", f"Emotion '{name}' đã tồn tại!")
                return
            
            try:
                # Validate name format
                if not name.replace('_', '').isalnum():
                    QMessageBox.warning(dialog, "Tên không hợp lệ", 
                                      "Tên emotion chỉ được chứa chữ cái, số và dấu gạch dưới (_)")
                    return
                
                # Add custom emotion với default expert-compliant parameters
                success = self.unified_emotion_system.add_custom_emotion(
                    name=name,
                    description=description or f"Custom emotion: {name}",
                    category="neutral",
                    temperature=0.8,   # Expert compliant defaults
                    exaggeration=1.0,
                    cfg_weight=0.6,
                    speed=1.0,
                    aliases=[]
                )
                
                if success:
                    # Reload UI table to show new emotion
                    self.load_emotions_to_table()
                    self.update_statistics()
                    print(f"\n[THEATER] CUSTOM EMOTION ADDED:")
                    print(f"   [EDIT] Name: {name}")
                    print(f"   [BOOK] Description: {description or f'Custom emotion: {name}'}")
                    print(f"   [STATS] Parameters: T=0.8, E=1.0, C=0.6, S=1.0 (Expert Compliant)")
                    # Success dialog
                    QMessageBox.information(
                        dialog,
                        "Thành Công!",
                        f"[OK] Đã thêm custom emotion thành công!\n\n"
                        f"[EDIT] Tên: {name}\n"
                        f"[BOOK] Mô tả: {description or f'Custom emotion: {name}'}\n"
                        f"[EMOJI] Category: neutral\n"
                        f"[STATS] Parameters: Expert-compliant defaults\n\n"
                        f"[IDEA] Emotion đã được thêm vào bảng và bạn có thể tuỉnh chỉnh parameters!"
                    )
                    self.update_status(f"[OK] Đã thêm custom emotion: {name}")
                    dialog.accept()
                else:
                    QMessageBox.critical(dialog, "Error", "Không thể thêm emotion. Vui lòng thử lại.")
                
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Không thể tạo emotion:\n{str(e)}")
        
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
                if self.unified_emotion_system.delete_custom_emotion(emotion_name):
                    self.load_emotions_to_table()  # Reload table
                    self.update_status(f"[OK] Đã xóa emotion '{emotion_name}'")
                else:
                    self.update_status(f"[EMOJI] Không thể xóa emotion '{emotion_name}'")
            except Exception as e:
                self.update_status(f"[EMOJI] Error xóa emotion: {str(e)}")
    
    def filter_emotions(self):
        """Lọc emotions theo category và custom"""
        category_filter = self.category_filter.currentText()
        show_custom_only = self.show_custom_only.isChecked()
        
        for row in range(self.emotions_table.rowCount()):
            name_item = self.emotions_table.item(row, 0)
            if name_item:
                emotion_name = name_item.text()
                emotion = self.unified_emotion_system.get_all_emotions().get(emotion_name)
                
                if emotion:
                    # Category filter
                    category_match = (category_filter == "Tất cả" or emotion.category == category_filter)
                    
                    # Custom filter
                    is_custom = False  # No custom emotions in unified system
                    custom_match = (not show_custom_only or is_custom)
                    
                    # Show/hide row
                    show_row = category_match and custom_match
                    self.emotions_table.setRowHidden(row, not show_row)
    
    def export_config(self):
        """Export emotion configuration với current UI values"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Emotion Config",
                f"emotion_config_{int(time.time())}.json",
                "JSON Files (*.json)"
            )
            
            if file_path:
                # Collect current UI values cho export
                export_data = {
                    "export_info": {
                        "timestamp": int(time.time()),
                        "version": "unified_emotion_system_v1.0",
                        "source": "Voice Studio Emotion Config Tab",
                        "total_emotions": 0
                    },
                    "emotions": {}
                }
                
                # Loop qua table để lấy current UI values
                for row in range(self.emotions_table.rowCount()):
                    name_item = self.emotions_table.item(row, 0)
                    if name_item:
                        emotion_name = name_item.text()
                        
                        # Get current values từ UI widgets
                        exag_spinbox = self.emotions_table.cellWidget(row, 3)
                        cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                        temp_spinbox = self.emotions_table.cellWidget(row, 5)
                        speed_spinbox = self.emotions_table.cellWidget(row, 6)
                        
                        # Get description và category từ unified system
                        emotion_details = self.unified_emotion_system.get_all_emotions().get(emotion_name)
                        
                        if emotion_details:
                            export_data["emotions"][emotion_name] = {
                                "description": emotion_details.description,
                                "category": emotion_details.category,
                                "parameters": {
                                    "exaggeration": exag_spinbox.value() if exag_spinbox else emotion_details.exaggeration,
                                    "cfg_weight": cfg_spinbox.value() if cfg_spinbox else emotion_details.cfg_weight,
                                    "temperature": temp_spinbox.value() if temp_spinbox else emotion_details.temperature,
                                    "speed": speed_spinbox.value() if speed_spinbox else emotion_details.speed
                                },
                                "source": "unified_system"
                            }
                
                export_data["export_info"]["total_emotions"] = len(export_data["emotions"])
                
                # === THÊM INNER VOICE CONFIG VÀO EXPORT ===
                if hasattr(self, 'inner_voice_group'):
                    export_data["inner_voice_config"] = {
                        "enabled": self.inner_voice_group.isChecked(),
                        "presets": {}
                    }
                    
                    # Export thông số cho từng type
                    for type_name in ["light", "deep", "dreamy"]:
                        if type_name in self.inner_voice_type_widgets:
                            widgets = self.inner_voice_type_widgets[type_name]
                            export_data["inner_voice_config"]["presets"][type_name] = {
                                "delay": widgets["delay"].value(),
                                "decay": widgets["decay"].value(),
                                "gain": widgets["gain"].value(),
                                "filter": widgets["filter"].text()
                            }
                
                # Write to file
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                print(f"\n[EMOJI] EXPORT COMPLETED:")
                print(f"   [FOLDER] File: {file_path}")
                print(f"   [STATS] Emotions: {export_data['export_info']['total_emotions']}")
                
                self.update_status(f"[OK] Đã export {export_data['export_info']['total_emotions']} emotions: {os.path.basename(file_path)}")
                
                # Show success dialog
                QMessageBox.information(
                    self,
                    "Export Thành Công",
                    f"[OK] Đã export thành công!\n\n"
                    f"[FOLDER] File: {os.path.basename(file_path)}\n"
                    f"[STATS] Emotions: {export_data['export_info']['total_emotions']}\n"
                    f"[EMOJI] Size: {os.path.getsize(file_path):,} bytes\n\n"
                    f"[IDEA] File chứa current UI values của tất cả emotions!"
                )
                
        except Exception as e:
            self.update_status(f"[EMOJI] Error export: {str(e)}")
            QMessageBox.critical(self, "Error Export", f"Không thể export emotion config:\n{str(e)}")
    
    def import_config(self):
        """Import emotion configuration và apply vào UI"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import Emotion Config", "",
                "JSON Files (*.json)"
            )
            
            if file_path:
                # Read và validate file
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
                
                # Validate format
                if "emotions" not in import_data:
                    QMessageBox.warning(self, "Invalid Format", "File không có 'emotions' section!")
                    return
                
                imported_emotions = import_data["emotions"]
                total_import = len(imported_emotions)
                
                # Confirm import
                reply = QMessageBox.question(
                    self,
                    "Confirm Import",
                    f"[EMOJI] Import Emotion Configuration\n\n"
                    f"[FOLDER] File: {os.path.basename(file_path)}\n"
                    f"[STATS] Emotions to import: {total_import}\n\n"
                    f"[WARNING] Hành động này sẽ overwrite current UI values!\n"
                    f"[IDEA] Chỉ emotions có sẵn trong unified system sẽ được import.\n\n"
                    f"Bạn có muốn tiếp tục?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return
                
                # Process import với progress
                success_count = 0
                skip_count = 0
                failed_count = 0
                
                print(f"\n[EMOJI] STARTING IMPORT từ {os.path.basename(file_path)}")
                print("="*60)
                
                for emotion_name, emotion_config in imported_emotions.items():
                    try:
                        # Check nếu emotion tồn tại trong unified system
                        if emotion_name not in self.unified_emotion_system.get_all_emotions():
                            # Thêm custom emotion nếu không có trong unified system
                            description = emotion_config.get("description", "")
                            category = emotion_config.get("category", "neutral")
                            params = emotion_config.get("parameters", {})
                            temp = params.get("temperature", 0.8)
                            exag = params.get("exaggeration", 1.0)
                            cfg = params.get("cfg_weight", 0.6)
                            speed = params.get("speed", 1.0)
                            try:
                                self.unified_emotion_system.add_custom_emotion(
                                    name=emotion_name,
                                    description=description,
                                    category=category,
                                    temperature=temp,
                                    exaggeration=exag,
                                    cfg_weight=cfg,
                                    speed=speed,
                                    aliases=emotion_config.get("aliases", [])
                                )
                                print(f"➕ ADDED: {emotion_name} as custom emotion")
                                success_count += 1
                            except Exception as e:
                                print(f"❌ FAILED ADD: {emotion_name} - {str(e)}")
                                failed_count += 1
                            continue
                        
                        # Get parameters từ import file
                        if "parameters" not in emotion_config:
                            print(f"[EMOJI] FAILED: {emotion_name} (thiếu parameters)")
                            failed_count += 1
                            continue
                            
                        params = emotion_config["parameters"]
                        
                        # Find row trong table và update UI widgets
                        for row in range(self.emotions_table.rowCount()):
                            name_item = self.emotions_table.item(row, 0)
                            if name_item and name_item.text() == emotion_name:
                                # Update spinboxes với imported values
                                exag_spinbox = self.emotions_table.cellWidget(row, 3)
                                cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                                temp_spinbox = self.emotions_table.cellWidget(row, 5)
                                speed_spinbox = self.emotions_table.cellWidget(row, 6)
                                
                                if exag_spinbox and "exaggeration" in params:
                                    exag_spinbox.blockSignals(True)
                                    exag_spinbox.setValue(params["exaggeration"])
                                    exag_spinbox.blockSignals(False)
                                
                                if cfg_spinbox and "cfg_weight" in params:
                                    cfg_spinbox.blockSignals(True)
                                    cfg_spinbox.setValue(params["cfg_weight"])
                                    cfg_spinbox.blockSignals(False)
                                
                                if temp_spinbox and "temperature" in params:
                                    temp_spinbox.blockSignals(True)
                                    temp_spinbox.setValue(params["temperature"])
                                    temp_spinbox.blockSignals(False)
                                
                                if speed_spinbox and "speed" in params:
                                    speed_spinbox.blockSignals(True)
                                    speed_spinbox.setValue(params["speed"])
                                    speed_spinbox.blockSignals(False)
                                
                                print(f"[OK] IMPORTED: {emotion_name} - "
                                      f"Exag={params.get('exaggeration', 'N/A'):.2f}, "
                                      f"CFG={params.get('cfg_weight', 'N/A'):.2f}, "
                                      f"Temp={params.get('temperature', 'N/A'):.2f}, "
                                      f"Speed={params.get('speed', 'N/A'):.1f}")
                                success_count += 1
                                break
                        
                    except Exception as e:
                        print(f"[EMOJI] FAILED: {emotion_name} - {str(e)}")
                        failed_count += 1
                
                # Force UI refresh
                # Reload table to include newly added custom emotions
                self.load_emotions_to_table()
                self.emotions_table.viewport().update()
                self.emotions_table.repaint()
                self.update_statistics()
                
                # === IMPORT INNER VOICE CONFIG NẾU CÓ ===
                inner_voice_imported = False
                if "inner_voice_config" in import_data and hasattr(self, 'inner_voice_group'):
                    try:
                        inner_config = import_data["inner_voice_config"]
                        
                        # Apply enabled state
                        if "enabled" in inner_config:
                            self.inner_voice_group.setChecked(inner_config["enabled"])
                            self.on_inner_voice_toggle()
                        
                        # Apply presets cho từng type
                        if "presets" in inner_config:
                            for type_name, preset in inner_config["presets"].items():
                                if type_name in self.inner_voice_type_widgets:
                                    widgets = self.inner_voice_type_widgets[type_name]
                                    
                                    if "delay" in preset and "delay" in widgets:
                                        widgets["delay"].setValue(preset["delay"])
                                    if "decay" in preset and "decay" in widgets:
                                        widgets["decay"].setValue(preset["decay"])
                                    if "gain" in preset and "gain" in widgets:
                                        widgets["gain"].setValue(preset["gain"])
                                    if "filter" in preset and "filter" in widgets:
                                        widgets["filter"].setText(preset["filter"])
                        
                        inner_voice_imported = True
                        print(f"[OK] IMPORTED: Inner Voice Config - enabled={inner_config.get('enabled', False)}")
                        
                    except Exception as e:
                        print(f"[WARNING] WARNING: Không thể import inner voice config: {e}")
                
                print("="*60)
                
                print("="*60)
                print(f"[EMOJI] IMPORT COMPLETED!")
                print(f"[OK] Successfully imported: {success_count}")
                print(f"⏭ Skipped (not found): {skip_count}")
                print(f"[EMOJI] Failed: {failed_count}")
                print(f"[STATS] Total processed: {success_count + skip_count + failed_count}/{total_import}")
                if inner_voice_imported:
                    print(f"[THEATER] Inner Voice config imported successfully!")
                
                # Update status và show results
                self.update_status(f"[OK] Import completed: {success_count} success, {skip_count} skipped, {failed_count} failed")
                
                # Show completion dialog
                completion_msg = (
                    f"[EMOJI] Import emotion configuration completed!\n\n"
                    f"[OK] Successfully imported: {success_count} emotions\n"
                    f"⏭ Skipped (not found): {skip_count} emotions\n"
                    f"[EMOJI] Failed: {failed_count} emotions\n\n"
                    f"[STATS] Total: {success_count + skip_count + failed_count}/{total_import}\n"
                )
                
                if inner_voice_imported:
                    completion_msg += f"\n[THEATER] Inner Voice config cũng đã được import!\n"
                
<<<<<<< Updated upstream
                completion_msg += f"\n💡 UI đã được cập nhật với imported values!"
                
=======
                completion_msg += f"\n[IDEA] UI đã được cập nhật với imported values!"

                # Save imported emotions to disk so they persist on next app start
                self.unified_emotion_system.save_unified_config()

>>>>>>> Stashed changes
                QMessageBox.information(self, "Import Hoàn Thành", completion_msg)
                    
        except Exception as e:
            self.update_status(f"[EMOJI] Error import: {str(e)}")
            QMessageBox.critical(self, "Error Import", f"Không thể import emotion config:\n{str(e)}")
    
    def update_statistics(self):
        """Cập nhật thống kê emotions"""
        try:
            # Get statistics cho unified system
            all_emotions = self.unified_emotion_system.get_all_emotions()
            custom_emotions = self.unified_emotion_system.get_custom_emotions()
            
            stats = {
                'total_emotions': len(all_emotions),
                'default_emotions': len(all_emotions) - len(custom_emotions),
                'custom_emotions': len(custom_emotions),
                'total_presets': 0  # No presets in unified system
            }
            
            stats_text = (
                f"[STATS] Total: {stats['total_emotions']} | "
                f"[THEATER] Built-in: {stats['default_emotions']} | "
                f"[SPARKLE] Custom: {stats['custom_emotions']} | "
                f"[EMOJI] Presets: {stats['total_presets']}"
            )
            
            self.stats_label.setText(stats_text)
            
        except Exception:
            self.stats_label.setText("[EMOJI] Error thống kê")
    
    def update_status(self, message: str):
        """Cập nhật status message"""
        self.status_label.setText(message)
        QTimer.singleShot(3000, lambda: self.status_label.setText("[OK] Sẵn sàng"))
    
    def connect_signals(self):
        """Kết nối signals"""
        # Filter signals already connected in setup_ui
        pass 

    def reset_emotion_to_default(self, emotion_name: str):
        """Reset emotion về giá trị gốc của cảm xúc đó cụ thể"""
        try:
            # In unified system, all emotions can be reset to their original values
            if emotion_name not in self.unified_emotion_system.get_all_emotions():
                QMessageBox.warning(
                    self, 
                    "Không thể Reset", 
                    f"Không tìm thấy emotion '{emotion_name}' trong hệ thống."
                )
                return
            
            # Get original emotion from unified system
            original_emotion = self.unified_emotion_system.get_all_emotions()[emotion_name]
            default_values = {
                'exaggeration': original_emotion.exaggeration,
                'cfg_weight': original_emotion.cfg_weight,
                'temperature': original_emotion.temperature,
                'speed': original_emotion.speed
            }
            
            # DEBUG: In giá trị gốc ra console
            print(f"\n[REFRESH] DEBUG RESET {emotion_name}:")
            print(f"   [EDIT] Original Description: {original_emotion.description}")
            print(f"   [EMOJI] Original Category: {original_emotion.category}")
            print(f"   [STATS] Original Values:")
            print(f"      [TARGET] Exaggeration: {default_values['exaggeration']:.2f}")
            print(f"      [EMOJI] CFG Weight: {default_values['cfg_weight']:.2f}")
            print(f"      [EMOJI] Temperature: {default_values['temperature']:.2f}")
            print(f"      [FAST] Speed: {default_values['speed']:.1f}")
            
            # Lấy giá trị hiện tại để so sánh
            current_emotion = original_emotion  # In unified system, current = original
            print(f"   [METRICS] Current Values:")
            print(f"      [TARGET] Exaggeration: {current_emotion.exaggeration:.2f}")
            print(f"      [EMOJI] CFG Weight: {current_emotion.cfg_weight:.2f}")
            print(f"      [EMOJI] Temperature: {current_emotion.temperature:.2f}")
            print(f"      [FAST] Speed: {current_emotion.speed:.1f}")
            
            # Confirm dialog với giá trị gốc cụ thể
            dialog_text = (
                f"Bạn có chắc chắn muốn reset '{emotion_name}' về giá trị gốc?\n\n"
                f"[EDIT] Emotion gốc: {original_emotion.description}\n"
                f"[EMOJI] Category: {original_emotion.category}\n\n"
                f"[STATS] Giá trị gốc sẽ được áp dụng:\n"
                f"[TARGET] Exaggeration: {default_values['exaggeration']:.2f}\n"
                f"[EMOJI] CFG Weight: {default_values['cfg_weight']:.2f}\n"
                f"[EMOJI] Temperature: {default_values['temperature']:.2f}\n"
                f"[FAST] Speed: {default_values['speed']:.1f}\n\n"
                f"[IDEA] Giá trị hiện tại:\n"
                f"[TARGET] Exaggeration: {current_emotion.exaggeration:.2f}\n"
                f"[EMOJI] CFG Weight: {current_emotion.cfg_weight:.2f}\n"
                f"[EMOJI] Temperature: {current_emotion.temperature:.2f}\n"
                f"[FAST] Speed: {current_emotion.speed:.1f}"
            )
            
            reply = QMessageBox.question(
                self,
                "Reset Emotion về Gốc",
                dialog_text,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # For unified system, reload table to reset values
                # (The values are already in their default state)
                
                # [TARGET] UPDATE UI trong table với blocking signals để tránh recursive calls
                for row in range(self.emotions_table.rowCount()):
                    name_item = self.emotions_table.item(row, 0)
                    if name_item and name_item.text() == emotion_name:
                        print(f"   [REFRESH] Updating UI for row {row}")
                        
                        # Update spinboxes với giá trị gốc cụ thể - BLOCK SIGNALS
                        exag_spinbox = self.emotions_table.cellWidget(row, 3)
                        if exag_spinbox:
                            exag_spinbox.blockSignals(True)
                            exag_spinbox.setValue(default_values['exaggeration'])
                            exag_spinbox.blockSignals(False)
                            print(f"   [OK] Updated exaggeration: {default_values['exaggeration']:.2f}")
                        
                        cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                        if cfg_spinbox:
                            cfg_spinbox.blockSignals(True)
                            cfg_spinbox.setValue(default_values['cfg_weight'])
                            cfg_spinbox.blockSignals(False)
                            print(f"   [OK] Updated cfg_weight: {default_values['cfg_weight']:.2f}")
                        
                        temp_spinbox = self.emotions_table.cellWidget(row, 5)
                        if temp_spinbox:
                            temp_spinbox.blockSignals(True)
                            temp_spinbox.setValue(default_values['temperature'])
                            temp_spinbox.blockSignals(False)
                            print(f"   [OK] Updated temperature: {default_values['temperature']:.2f}")
                        
                        speed_spinbox = self.emotions_table.cellWidget(row, 6)
                        if speed_spinbox:
                            speed_spinbox.blockSignals(True)
                            speed_spinbox.setValue(default_values['speed'])
                            speed_spinbox.blockSignals(False)
                            print(f"   [OK] Updated speed: {default_values['speed']:.1f}")
                        
                        # Force table refresh và update statistics
                        self.emotions_table.viewport().update()
                        self.emotions_table.repaint()
                        self.update_statistics()  # Update emotion count statistics
                        
                        print(f"   [SUCCESS] UI update completed for {emotion_name}")
                        break
                
                self.update_status(f"[OK] Reset {emotion_name} về giá trị gốc: Exag={default_values['exaggeration']:.2f}, CFG={default_values['cfg_weight']:.2f}")
                
                # [REFRESH] ALTERNATIVE: Reload entire table to ensure consistency
                # Uncomment this line if individual widget updates don't work properly
                # self.load_emotions_to_table()
                
        except Exception as e:
            self.update_status(f"[EMOJI] Error reset {emotion_name}: {str(e)}")
            QMessageBox.warning(self, "Error Reset", f"Không thể reset {emotion_name} về giá trị gốc:\n{str(e)}") 

    def reset_all_emotions_to_default(self):
        """Reset tất cả emotions về giá trị gốc"""
        try:
            all_emotions = self.unified_emotion_system.get_all_emotions()
            total_emotions = len(all_emotions)
            
            # Confirm dialog với thông tin chi tiết
            dialog_text = (
                f"[WARNING] RESET TẤT CẢ EMOTIONS\n\n"
                f"Bạn có chắc chắn muốn reset TẤT CẢ {total_emotions} emotions "
                f"về giá trị gốc không?\n\n"
                f"[REFRESH] Hành động này sẽ:\n"
                f"• Reset tất cả parameters về expert-recommended values\n"
                f"• Phục hồi 100% compliance với expert recommendations\n"
                f"• Khôi phục toàn bộ hệ thống emotion về trạng thái tối ưu\n\n"
                f"[IDEA] Tất cả thay đổi hiện tại sẽ bị mất!\n"
                f"[STATS] Unified System sẽ được phục hồi hoàn toàn"
            )
            
            reply = QMessageBox.question(
                self,
                "Reset All Emotions",
                dialog_text,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Show progress dialog
                progress = QProgressDialog(
                    "Đang reset tất cả emotions...", 
                    "Hủy", 0, total_emotions, self
                )
                progress.setWindowTitle("Reset All Progress")
                progress.setWindowModality(Qt.WindowModal)
                progress.show()
                
                reset_count = 0
                failed_count = 0
                
                print(f"\n[REFRESH] STARTING RESET ALL {total_emotions} EMOTIONS")
                print("="*60)
                
                # Process tất cả emotions
                for idx, (emotion_name, emotion) in enumerate(all_emotions.items()):
                    progress.setValue(idx)
                    progress.setLabelText(f"Reset: {emotion_name}")
                    
                    if progress.wasCanceled():
                        break
                    
                    try:
                        # Get original values
                        default_values = {
                            'exaggeration': emotion.exaggeration,
                            'cfg_weight': emotion.cfg_weight,
                            'temperature': emotion.temperature,
                            'speed': emotion.speed
                        }
                        
                        print(f"[THEATER] {emotion_name}: Exag={default_values['exaggeration']:.2f}, "
                              f"CFG={default_values['cfg_weight']:.2f}, "
                              f"Temp={default_values['temperature']:.2f}, "
                              f"Speed={default_values['speed']:.1f}")
                        
                        # Update UI for this emotion
                        for row in range(self.emotions_table.rowCount()):
                            name_item = self.emotions_table.item(row, 0)
                            if name_item and name_item.text() == emotion_name:
                                # Update all spinboxes với blocking signals
                                exag_spinbox = self.emotions_table.cellWidget(row, 3)
                                if exag_spinbox:
                                    exag_spinbox.blockSignals(True)
                                    exag_spinbox.setValue(default_values['exaggeration'])
                                    exag_spinbox.blockSignals(False)
                                
                                cfg_spinbox = self.emotions_table.cellWidget(row, 4)
                                if cfg_spinbox:
                                    cfg_spinbox.blockSignals(True)
                                    cfg_spinbox.setValue(default_values['cfg_weight'])
                                    cfg_spinbox.blockSignals(False)
                                
                                temp_spinbox = self.emotions_table.cellWidget(row, 5)
                                if temp_spinbox:
                                    temp_spinbox.blockSignals(True)
                                    temp_spinbox.setValue(default_values['temperature'])
                                    temp_spinbox.blockSignals(False)
                                
                                speed_spinbox = self.emotions_table.cellWidget(row, 6)
                                if speed_spinbox:
                                    speed_spinbox.blockSignals(True)
                                    speed_spinbox.setValue(default_values['speed'])
                                    speed_spinbox.blockSignals(False)
                                
                                break
                        
                        reset_count += 1
                        
                    except Exception as e:
                        print(f"[EMOJI] Failed to reset {emotion_name}: {str(e)}")
                        failed_count += 1
                    
                    # Small delay để UI responsive
                    QApplication.processEvents()
                
                progress.setValue(total_emotions)
                progress.close()
                
                # Force table refresh
                self.emotions_table.viewport().update()
                self.emotions_table.repaint()
                self.update_statistics()
                
                print("="*60)
                print(f"[SUCCESS] RESET ALL COMPLETED!")
                print(f"[OK] Successfully reset: {reset_count} emotions")
                print(f"[EMOJI] Failed: {failed_count} emotions")
                print(f"[STATS] Total processed: {reset_count + failed_count}/{total_emotions}")
                
                # Success message
                if failed_count == 0:
                    self.update_status(f"[SUCCESS] Reset ALL {reset_count} emotions thành công! 100% Expert Compliance!")
                    QMessageBox.information(
                        self, 
                        "Reset All Hoàn Thành", 
                        f"[OK] Đã reset thành công {reset_count} emotions!\n\n"
                        f"[TARGET] Tất cả emotions giờ đã 100% expert compliance:\n"
                        f"• Temperature: 0.7-1.0 [OK]\n"
                        f"• Exaggeration: 0.8-1.2 [OK]\n"
                        f"• CFG Weight: 0.5-0.7 [OK]\n"
                        f"• Speed: 0.8-1.3 [OK]\n\n"
                        f"[REFRESH] Unified Emotion System restored!"
                    )
                else:
                    self.update_status(f"[WARNING] Reset ALL: {reset_count} thành công, {failed_count} thất bại")
                    QMessageBox.warning(
                        self, 
                        "Reset All Hoàn Thành Một Phần", 
                        f"[OK] Thành công: {reset_count} emotions\n"
                        f"[EMOJI] Thất bại: {failed_count} emotions\n\n"
                        f"Vui lòng kiểm tra console để biết chi tiết."
                    )
            
        except Exception as e:
            print(f"[EMOJI] CRITICAL ERROR in reset_all_emotions_to_default: {str(e)}")
            self.update_status(f"[EMOJI] Error reset all: {str(e)}")
            QMessageBox.critical(
                self, 
                "Error Reset All", 
                f"Không thể reset tất cả emotions:\n{str(e)}\n\n"
                f"Vui lòng thử lại hoặc reset từng emotion riêng lẻ."
            ) 

    def on_inner_voice_toggle(self):
        # Enable/disable các spinbox theo trạng thái bật/tắt
        enabled = self.inner_voice_group.isChecked()
        for w in self.inner_voice_type_widgets.values():
            for key in ["delay", "decay", "gain", "filter", "reset", "group"]:
                w[key].setEnabled(enabled)

    def reset_inner_voice_type(self, type_name: str):
        # Reset về thông số ORIGINAL (từ file hoặc user's settings)
        if type_name in self.inner_voice_original_values and type_name in self.inner_voice_type_widgets:
            original_vals = self.inner_voice_original_values[type_name]
            widgets = self.inner_voice_type_widgets[type_name]
            
            print(f"[REFRESH] RESETTING {type_name} to ORIGINAL values:")
            print(f"   delay: {original_vals['delay']}")
            print(f"   decay: {original_vals['decay']}")
            print(f"   gain: {original_vals['gain']}")
            print(f"   filter: '{original_vals['filter']}'")
            
            # Temporarily block signals để tránh trigger auto-save
            widgets["delay"].blockSignals(True)
            widgets["decay"].blockSignals(True)
            widgets["gain"].blockSignals(True)
            widgets["filter"].blockSignals(True)
            
            widgets["delay"].setValue(original_vals["delay"])
            widgets["decay"].setValue(original_vals["decay"])
            widgets["gain"].setValue(original_vals["gain"])
            widgets["filter"].setText(original_vals["filter"])
            
            # Unblock signals
            widgets["delay"].blockSignals(False)
            widgets["decay"].blockSignals(False)
            widgets["gain"].blockSignals(False)
            widgets["filter"].blockSignals(False)
            
            print(f"[OK] Reset completed for {type_name}")
            
            # Cập nhật InnerVoiceProcessor với thông số mới
            self.update_inner_voice_processor_preset(type_name)
            
            # Save config sau khi reset
            self.save_inner_voice_config_to_file()
        else:
            print(f"[EMOJI] Cannot reset {type_name}: No original values or widgets not found")
    
    def update_inner_voice_processor_preset(self, type_name: str):
        """Cập nhật preset InnerVoiceProcessor với thông số từ UI"""
        try:
            if type_name in self.inner_voice_type_widgets:
                widgets = self.inner_voice_type_widgets[type_name]
                
                # Thu thập thông số từ UI
                delay = widgets["delay"].value()
                decay = widgets["decay"].value()
                gain = widgets["gain"].value()
                
                # Auto-generate filter string từ current values
                auto_filter = self.generate_filter_string(type_name, delay, decay, gain)
                
                # Cập nhật filter text field để sync với values
                widgets["filter"].setText(auto_filter)
                
                custom_preset = {
                    "delay": delay,
                    "decay": decay, 
                    "gain": gain,
                    "filter": auto_filter
                }
                
                # Import và cập nhật InnerVoiceProcessor
                from core.inner_voice_processor import InnerVoiceProcessor
                processor = InnerVoiceProcessor()
                processor.set_custom_preset(type_name, custom_preset)
                
                print(f"[THEATER] Updated InnerVoiceProcessor preset for {type_name}: {custom_preset}")
                
        except Exception as e:
            print(f"[WARNING] Warning: Không thể cập nhật InnerVoiceProcessor preset: {e}")
    
    def generate_filter_string(self, type_name: str, delay: float, decay: float, gain: float) -> str:
        """Generate FFmpeg filter string từ UI parameters"""
        
        # Base aecho filter cho tất cả types
        base_filter = f"aecho={gain}:{decay}:{delay}:{decay}"
        
        # Type-specific enhancements
        if type_name == "light":
            # Light: simple echo
            return base_filter
            
        elif type_name == "deep":
            # Deep: dual echo với lowpass
            return f"{base_filter}|0.3,lowpass=f=3000"
            
        elif type_name == "dreamy":
            # Dreamy: volume + echo + lowpass
            return f"volume=0.8,{base_filter},lowpass=f=3000"
            
        else:
            # Fallback
            return base_filter
    
    def save_inner_voice_config_to_file(self):
        """Lưu cấu hình inner voice vào unified_emotions.json"""
        try:
            config_path = "configs/emotions/unified_emotions.json"
            
            print(f"[SEARCH] DEBUGGING SAVE: Starting save to {config_path}")
            
            # Đọc config hiện tại
            import json
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"[OK] Successfully read existing config file")
            else:
                config = {}
                print(f"[WARNING] Config file doesn't exist, creating new one")
            
            # Cập nhật inner voice config
            if hasattr(self, 'inner_voice_group') and hasattr(self, 'inner_voice_type_widgets'):
                print(f"[THEATER] Inner Voice enabled: {self.inner_voice_group.isChecked()}")
                
                config["inner_voice_config"] = {
                    "enabled": self.inner_voice_group.isChecked(),
                    "description": "Inner voice (thoại nội tâm) system configuration",
                    "presets": {}
                }
                
                # Lưu thông số từ UI
                for type_name in ["light", "deep", "dreamy"]:
                    if type_name in self.inner_voice_type_widgets:
                        widgets = self.inner_voice_type_widgets[type_name]
                        current_values = {
                            "delay": widgets["delay"].value(),
                            "decay": widgets["decay"].value(),
                            "gain": widgets["gain"].value(),
                            "filter": widgets["filter"].text(),
                            "description": f"Preset {type_name} - cài đặt từ UI"
                        }
                        config["inner_voice_config"]["presets"][type_name] = current_values
                        
                        print(f"[STATS] {type_name}: delay={current_values['delay']}, decay={current_values['decay']}, gain={current_values['gain']}, filter='{current_values['filter']}'")
                
                # Ghi lại file với error handling
                try:
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    
                    # Verify write
                    with open(config_path, 'r', encoding='utf-8') as f:
                        verify_config = json.load(f)
                    
                    if "inner_voice_config" in verify_config:
                        print(f"[OK] SAVE VERIFIED: File updated successfully")
                        
                        # Show current file values for debugging
                        saved_presets = verify_config["inner_voice_config"]["presets"]
                        for type_name, preset in saved_presets.items():
                            print(f"   [EDIT] Saved {type_name}: delay={preset['delay']}, filter='{preset['filter']}'")
                    else:
                        print(f"[EMOJI] SAVE FAILED: inner_voice_config not found in saved file")
                        
                except Exception as write_error:
                    print(f"[EMOJI] FILE WRITE ERROR: {write_error}")
                    raise write_error
                
                print(f"[EMOJI] SAVE COMPLETED: {config_path}")
                
            else:
                print(f"[EMOJI] SAVE FAILED: Missing inner_voice_group or inner_voice_type_widgets")
                
        except Exception as e:
            print(f"[EMOJI] CRITICAL SAVE ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    def load_inner_voice_config_from_file(self):
        """Load cấu hình inner voice từ unified_emotions.json khi khởi tạo"""
        try:
            config_path = "configs/emotions/unified_emotions.json"
            
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if "inner_voice_config" in config and hasattr(self, 'inner_voice_group'):
                    inner_config = config["inner_voice_config"]
                    
                    # Apply enabled state
                    if "enabled" in inner_config:
                        self.inner_voice_group.setChecked(inner_config["enabled"])
                        self.on_inner_voice_toggle()
                    
                    # Apply presets và lưu original values
                    if "presets" in inner_config:
                        for type_name, preset in inner_config["presets"].items():
                            if type_name in self.inner_voice_type_widgets:
                                widgets = self.inner_voice_type_widgets[type_name]
                                
                                # Lưu original values để reset về sau này
                                self.inner_voice_original_values[type_name] = {
                                    "delay": preset.get("delay", 500),
                                    "decay": preset.get("decay", 0.3),
                                    "gain": preset.get("gain", 0.5),
                                    "filter": preset.get("filter", "aecho=0.6:0.5:500:0.3")
                                }
                                
                                # Apply values to UI
                                widgets["delay"].setValue(preset.get("delay", 500))
                                widgets["decay"].setValue(preset.get("decay", 0.3))
                                widgets["gain"].setValue(preset.get("gain", 0.5))
                                widgets["filter"].setText(preset.get("filter", "aecho=0.6:0.5:500:0.3"))
                                
                                print(f"[EMOJI] Loaded {type_name}: delay={preset.get('delay')}, filter='{preset.get('filter')}'")
                    
                    print(f"[OK] Loaded inner voice config from {config_path}")
                else:
                    # Nếu không có config, set default original values
                    self.set_default_original_values()
                    
            else:
                # Nếu file không tồn tại, set defaults
                self.set_default_original_values()
                    
        except Exception as e:
            print(f"[WARNING] Warning: Không thể load inner voice config: {e}")
            self.set_default_original_values()
    
    def set_default_original_values(self):
        """Set default original values khi không có config file"""
        # Generate filter strings theo values mới
        light_filter = self.generate_filter_string("light", 50, 0.3, 0.5)
        deep_filter = self.generate_filter_string("deep", 150, 0.6, 0.7)
        dreamy_filter = self.generate_filter_string("dreamy", 300, 0.8, 0.6)
        
        self.inner_voice_original_values = {
            "light": {"delay": 50, "decay": 0.3, "gain": 0.5, "filter": light_filter},
            "deep": {"delay": 150, "decay": 0.6, "gain": 0.7, "filter": deep_filter},
            "dreamy": {"delay": 300, "decay": 0.8, "gain": 0.6, "filter": dreamy_filter}
        }
        
        print("[CLIPBOARD] Set default original values for Inner Voice:")
        for type_name, values in self.inner_voice_original_values.items():
            print(f"   [EMOJI] {type_name}: delay={values['delay']}, filter='{values['filter']}'")
        print("[CLIPBOARD] Set default original values for Inner Voice")
    
    def connect_inner_voice_signals(self):
        """Kết nối signals cho inner voice widgets để auto-save"""
        try:
            if hasattr(self, 'inner_voice_group') and hasattr(self, 'inner_voice_type_widgets'):
                # Kết nối signal cho checkbox chính
                self.inner_voice_group.toggled.connect(self.save_inner_voice_config_to_file)
                
                # Kết nối signals cho từng type widget
                for type_name, widgets in self.inner_voice_type_widgets.items():
                    # Kết nối spinbox value changes
                    if "delay" in widgets:
                        widgets["delay"].valueChanged.connect(lambda v, t=type_name: self.on_inner_voice_param_changed(t))
                    if "decay" in widgets:
                        widgets["decay"].valueChanged.connect(lambda v, t=type_name: self.on_inner_voice_param_changed(t))
                    if "gain" in widgets:
                        widgets["gain"].valueChanged.connect(lambda v, t=type_name: self.on_inner_voice_param_changed(t))
                    if "filter" in widgets:
                        widgets["filter"].textChanged.connect(lambda v, t=type_name: self.on_inner_voice_param_changed(t))
                
                print("[EMOJI] Connected inner voice signals for auto-save")
                
        except Exception as e:
            print(f"[WARNING] Warning: Không thể connect inner voice signals: {e}")
    
    def on_inner_voice_param_changed(self, type_name: str):
        """Xử lý khi user thay đổi thông số inner voice"""
        try:
            # Cập nhật processor với preset mới
            self.update_inner_voice_processor_preset(type_name)
            
            # Auto-save config
            self.save_inner_voice_config_to_file()
            
        except Exception as e:
            print(f"[WARNING] Warning: Error xử lý param change cho {type_name}: {e}")
    
