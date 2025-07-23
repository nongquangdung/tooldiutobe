<<<<<<< Updated upstream
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QLineEdit, QGroupBox,
                               QGridLayout, QMessageBox, QTextEdit, QCheckBox,
                               QScrollArea, QSplitter, QTabWidget, QWidget,
                               QInputDialog, QFrame, QSlider, QSpinBox,
                               QFileDialog, QProgressBar)
from PySide6.QtCore import Qt, QSize, QTimer
import os
import tempfile
import platform

class ManualVoiceSetupDialog(QDialog):
    def __init__(self, voice_generator, parent=None):
        super().__init__(parent)
        self.voice_generator = voice_generator
        self.voice_mapping = {}
        self.character_configs = []
        self.preview_files = []
        self._closing = False  # Prevent recursion
        
        self.setWindowTitle("🎭 Cấu hình giọng đọc theo nhân vật")
        self.setModal(True)
        
        # Responsive sizing based on platform
        if platform.system() == "Darwin":  # macOS
            self.resize(1000, 700)
            self.setMinimumSize(900, 600)
        else:  # Windows/Linux
            self.resize(1100, 750)
            self.setMinimumSize(950, 650)
        
        self.setup_ui()
        self.setup_default_characters()
        self.apply_responsive_styles()
    
    def setup_ui(self):
        """Thiết lập UI responsive"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # Header với title và instructions
        self.create_header(main_layout)
        
        # Main content với splitter layout
        self.create_main_content(main_layout)
        
        # Bottom action buttons
        self.create_action_buttons(main_layout)
    
    def create_header(self, parent_layout):
        """Tạo header responsive"""
        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_frame.setLayout(header_layout)
        
        # Title
        title = QLabel("🎭 Cấu hình giọng đọc theo nhân vật")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "💡 Thiết lập tối đa 6 nhân vật với giọng đọc riêng biệt. "
            "Chỉ nhân vật được tích ✅ sẽ được sử dụng để tạo audio."
        )
        instructions.setObjectName("instructions")
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(instructions)
        
        parent_layout.addWidget(header_frame)
    
    def create_main_content(self, parent_layout):
        """Tạo main content với responsive layout"""
        # Sử dụng horizontal splitter cho responsive layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Character configurations
        left_panel = self.create_characters_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Voice info và controls
        right_panel = self.create_info_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter ratio (70% - 30%)
        splitter.setSizes([700, 300])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        
        parent_layout.addWidget(splitter)
    
    def create_characters_panel(self):
        """Tạo panel cấu hình nhân vật với scroll"""
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel.setLayout(panel_layout)
        
        # Header
        chars_header = QLabel("👥 Cấu hình nhân vật (tối đa 6)")
        chars_header.setObjectName("section_header")
        panel_layout.addWidget(chars_header)
        
        # Scroll area cho characters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(12)
        scroll_content.setLayout(scroll_layout)
        
        # Tạo 6 character widgets với layout responsive
        self.character_widgets = []
        for i in range(6):
            char_widget = self.create_character_widget_responsive(i + 1)
            self.character_widgets.append(char_widget)
            scroll_layout.addWidget(char_widget)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        panel_layout.addWidget(scroll)
        
        return panel
    
    def create_character_widget_responsive(self, index):
        """Tạo widget nhân vật với responsive design"""
        group = QGroupBox(f"Nhân vật {index}")
        group.setObjectName("character_group")
        
        # Sử dụng grid layout responsive
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 16, 12, 12)
        group.setLayout(layout)
        
        # Row 1: Enable checkbox và Name
        enabled_cb = QCheckBox("Sử dụng")
        enabled_cb.setChecked(index <= 2)  # Default enable first 2
        layout.addWidget(enabled_cb, 0, 0)
        
        layout.addWidget(QLabel("Tên:"), 0, 1)
        name_input = QLineEdit()
        name_input.setPlaceholderText(f"Nhân vật {index}")
        layout.addWidget(name_input, 0, 2, 1, 2)  # Span 2 columns
        
        # Row 2: ID và Gender
        layout.addWidget(QLabel("ID:"), 1, 0)
        id_input = QLineEdit()
        id_input.setPlaceholderText(f"character{index}")
        layout.addWidget(id_input, 1, 1)
        
        layout.addWidget(QLabel("Giới tính:"), 1, 2)
        gender_combo = QComboBox()
        gender_combo.addItems(["Nữ", "Nam", "Trung tính"])
        layout.addWidget(gender_combo, 1, 3)
        
        # Row 3: TTS Provider selection
        layout.addWidget(QLabel("TTS Provider:"), 2, 0)
        provider_combo = QComboBox()
        provider_combo.addItems([
            "🇻🇳 Google TTS (Vietnamese)",
            "🤖 Chatterbox TTS (English)",
            "🎭 ElevenLabs (English)",
            "🔄 Auto-select"
        ])
        provider_combo.setCurrentText("🔄 Auto-select")
        layout.addWidget(provider_combo, 2, 1, 1, 2)
        
        preview_btn = QPushButton("🔊")
        preview_btn.setMaximumWidth(50)
        preview_btn.setToolTip("Preview giọng đọc")
        preview_btn.clicked.connect(
            lambda checked, idx=index-1: self.preview_character_voice(idx)
        )
        layout.addWidget(preview_btn, 2, 3)
        
        # Row 4: Voice selection (dynamic based on provider)
        layout.addWidget(QLabel("Giọng:"), 3, 0)
        voice_combo = QComboBox()
        self.update_voice_options(voice_combo, provider_combo.currentText())
        layout.addWidget(voice_combo, 3, 1, 1, 3)
        
        # Row 5: Chatterbox-specific controls (initially hidden)
        chatterbox_frame = QFrame()
        chatterbox_layout = QGridLayout()
        chatterbox_layout.setContentsMargins(0, 0, 0, 0)
        chatterbox_frame.setLayout(chatterbox_layout)
        
        # Emotion dropdown (using predefined emotions)
        chatterbox_layout.addWidget(QLabel("🎭 Emotion:"), 0, 0)
        emotion_combo = QComboBox()
        emotion_combo.addItems([
            "😐 neutral", "😊 happy", "😢 sad", "😮 excited", 
            "😌 calm", "😠 angry", "😍 romantic", "😨 fearful",
            "🤔 thoughtful", "😴 sleepy", "💪 confident", "😊 cheerful",
            "😔 melancholic", "🎭 dramatic", "👻 mysterious", "😱 surprised",
            "😤 frustrated", "🥺 pleading"
        ])
        emotion_combo.setCurrentText("😐 neutral")
        emotion_combo.setToolTip("Select emotion for voice generation")
        chatterbox_layout.addWidget(emotion_combo, 0, 1, 1, 2)
        
        # Exaggeration control
        chatterbox_layout.addWidget(QLabel("🎯 Exaggeration:"), 1, 0)
        exag_slider = QSlider(Qt.Horizontal)
        exag_slider.setRange(0, 250)     # 0.0-2.5 scaled to 0-250
        exag_slider.setValue(100)        # Default 1.0
        exag_slider.setToolTip("Emotion exaggeration: 0.0 (flat) - 2.5 (very dramatic)")
        chatterbox_layout.addWidget(exag_slider, 1, 1)
        
        exag_value = QLabel("1.00")
        exag_value.setMinimumWidth(40)
        chatterbox_layout.addWidget(exag_value, 1, 2)
        
        # Speed control
        chatterbox_layout.addWidget(QLabel("⚡ Speed:"), 2, 0)
        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setRange(50, 200)   # 0.5-2.0 scaled to 50-200
        speed_slider.setValue(100)       # Default 1.0
        speed_slider.setToolTip("Speaking speed: 0.5 (slow) - 2.0 (fast)")
        chatterbox_layout.addWidget(speed_slider, 2, 1)
        
        speed_value = QLabel("1.0")
        speed_value.setMinimumWidth(30)
        chatterbox_layout.addWidget(speed_value, 2, 2)
        
        # Voice cloning
        chatterbox_layout.addWidget(QLabel("🎤 Clone:"), 3, 0)
        clone_btn = QPushButton("📁 Upload Voice Sample")
        clone_btn.setToolTip("Upload 3-30s audio file to clone voice")
        chatterbox_layout.addWidget(clone_btn, 3, 1)
        
        clone_status = QLabel("No sample")
        clone_status.setObjectName("clone_status")
        chatterbox_layout.addWidget(clone_status, 3, 2)
        
        layout.addWidget(chatterbox_frame, 4, 0, 1, 4)
        chatterbox_frame.setVisible(False)  # Initially hidden
        
        # Update sliders display
        def update_exag_display(value):
            exag_value.setText(f"{value/100:.2f}")
        
        def update_speed_display(value):
            speed_value.setText(f"{value/100:.1f}")
        
        exag_slider.valueChanged.connect(update_exag_display)
        speed_slider.valueChanged.connect(update_speed_display)
        
        # Voice cloning handler
        def upload_voice_sample():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Voice Sample", "", 
                "Audio Files (*.wav *.mp3 *.flac *.m4a)"
            )
            if file_path:
                clone_status.setText(f"✅ {os.path.basename(file_path)}")
                clone_status.setProperty("file_path", file_path)
            
        clone_btn.clicked.connect(upload_voice_sample)
        
        # Provider change handler
        def on_provider_changed():
            provider = provider_combo.currentText()
            self.update_voice_options(voice_combo, provider)
            
            # Show/hide Chatterbox controls
            is_chatterbox = "Chatterbox" in provider
            chatterbox_frame.setVisible(is_chatterbox)
            
            # Auto-update voice based on gender for Google TTS
            if "Google" in provider:
                gender = gender_combo.currentText()
                if gender == "Nữ":
                    voice_combo.setCurrentText("vi-VN-Wavenet-A (Nữ)")
                elif gender == "Nam":
                    voice_combo.setCurrentText("vi-VN-Wavenet-B (Nam)")
                else:  # Trung tính
                    voice_combo.setCurrentText("vi-VN-Standard-C (Nữ)")
        
        provider_combo.currentTextChanged.connect(on_provider_changed)
        gender_combo.currentTextChanged.connect(on_provider_changed)
        
        # Store references for later access
        widget_refs = {
            'enabled': enabled_cb,
            'name': name_input,
            'id': id_input,
            'gender': gender_combo,
            'provider': provider_combo,
            'voice': voice_combo,
            'chatterbox_frame': chatterbox_frame,
            'emotion_combo': emotion_combo,
            'exag_slider': exag_slider,
            'speed_slider': speed_slider,
            'clone_status': clone_status,
            'preview_btn': preview_btn
        }
        
        # Store widget references for character
        if not hasattr(self, 'character_widget_refs'):
            self.character_widget_refs = []
        self.character_widget_refs.append(widget_refs)
        
        # Enable/disable controls based on checkbox
        def toggle_enabled(checked):
            name_input.setEnabled(checked)
            id_input.setEnabled(checked)
            gender_combo.setEnabled(checked)
            provider_combo.setEnabled(checked)
            voice_combo.setEnabled(checked)
            chatterbox_frame.setEnabled(checked)
            preview_btn.setEnabled(checked)
            
        enabled_cb.toggled.connect(toggle_enabled)
        toggle_enabled(enabled_cb.isChecked())
        
        # Store references
        group.enabled_cb = enabled_cb
        group.name_input = name_input
        group.id_input = id_input
        group.gender_combo = gender_combo
        group.voice_combo = voice_combo
        group.preview_btn = preview_btn
        
        return group
    
    def update_voice_options(self, voice_combo, provider):
        """Update voice options based on selected provider"""
        voice_combo.clear()
        
        if "Google" in provider:
            voice_combo.addItems([
                "vi-VN-Standard-A (Nữ)",
                "vi-VN-Standard-B (Nam)", 
                "vi-VN-Standard-C (Nữ)",
                "vi-VN-Standard-D (Nam)",
                "vi-VN-Wavenet-A (Nữ)",
                "vi-VN-Wavenet-B (Nam)",
                "vi-VN-Wavenet-C (Nữ)", 
                "vi-VN-Wavenet-D (Nam)"
            ])
        elif "Chatterbox" in provider:
            # Get 28 predefined voices from ChatterboxVoicesManager
            try:
                from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                chatterbox_manager = ChatterboxVoicesManager()
                available_voices = chatterbox_manager.get_available_voices()
                
                # Add predefined voices
                voice_options = []
                for voice_id, voice_obj in sorted(available_voices.items()):
                    display_name = f"{voice_obj.name} ({voice_obj.gender})"
                    voice_options.append(display_name)
                
                # Add custom cloning option
                voice_options.append("🎤 Custom Cloned Voice (upload sample)")
                voice_combo.addItems(voice_options)
                
                print(f"✅ Loaded {len(voice_options)} voice options for Chatterbox TTS")
                
            except Exception as e:
                print(f"⚠️ ChatterboxVoicesManager import failed: {e}")
                # Fallback if ChatterboxVoicesManager not available
                voice_combo.addItems([
                    "Default English Voice",
                    "🎤 Custom Cloned Voice (upload sample)"
                ])
                
        elif "ElevenLabs" in provider:
            voice_combo.addItems([
                "Rachel (Female)",
                "Drew (Male)",
                "Clyde (Male)",
                "Paul (Male)",
                "Domi (Female)",
                "Dave (Male)",
                "Fin (Male)",
                "Sarah (Female)"
            ])
        else:  # Auto-select
            voice_combo.addItems([
                "🔄 Auto-select based on text language",
                "🇻🇳 Vietnamese → Google TTS",
                "🇺🇸 English → Chatterbox/ElevenLabs"
            ])
    
    def create_info_panel(self):
        """Tạo panel thông tin và controls"""
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(8, 0, 0, 0)
        panel.setLayout(panel_layout)
        
        # Available voices info
        voices_group = QGroupBox("📋 Giọng đọc có sẵn")
        voices_layout = QVBoxLayout()
        
        self.voices_text = QTextEdit()
        self.voices_text.setMaximumHeight(150)
        self.voices_text.setReadOnly(True)
        
        # Get Chatterbox status
        chatterbox_status = self.voice_generator.get_chatterbox_device_info()
        chatterbox_available = chatterbox_status.get('available', False)
        
        voices_info = f"""🤖 CHATTERBOX TTS:
Status: {'✅ Available' if chatterbox_available else '❌ Not available'}
Device: {chatterbox_status.get('device_name', 'Unknown')}
Features: 28 predefined voices, Voice cloning, Emotion control

🎭 28 PREDEFINED VOICES:
👨 Male: Adrian, Alexander, Austin, Axel, Connor, Eli, Everett, 
Gabriel, Henry, Ian, Jeremiah, Jordan, Julian, Leonardo, 
Michael, Miles, Ryan, Thomas
👩 Female: Abigail, Alice, Cora, Elena, Emily, Gianna, 
Jade, Layla, Olivia, Taylor

🇻🇳 GOOGLE TTS (Vietnamese):
• vi-VN-Standard-A/B/C/D (Standard)  
• vi-VN-Wavenet-A/B/C/D (Natural)

🎭 ELEVENLABS (English):
• Rachel, Drew, Clyde, Paul, Domi, Dave, Fin, Sarah

💡 Tips:
• Chatterbox = 28 high-quality voices + emotion control
• Wavenet = Chất lượng cao cho tiếng Việt
• Auto-select = Tự động chọn provider tốt nhất"""
        
        self.voices_text.setPlainText(voices_info)
        voices_layout.addWidget(self.voices_text)
        voices_group.setLayout(voices_layout)
        panel_layout.addWidget(voices_group)
        
        # Quick actions
        actions_group = QGroupBox("⚡ Thao tác nhanh")
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)
        
        self.preset_btn = QPushButton("⚙️ Load Preset")
        self.preset_btn.setToolTip("Nạp cấu hình mẫu cho các thể loại khác nhau")
        self.preset_btn.clicked.connect(self.load_preset)
        actions_layout.addWidget(self.preset_btn)
        
        self.test_all_btn = QPushButton("🎵 Test tất cả giọng")
        self.test_all_btn.setToolTip("Tạo audio test cho tất cả nhân vật đã kích hoạt")
        self.test_all_btn.clicked.connect(self.test_all_voices)
        actions_layout.addWidget(self.test_all_btn)
        
        self.reset_btn = QPushButton("🔄 Reset về mặc định")
        self.reset_btn.setToolTip("Khôi phục cấu hình mặc định")
        self.reset_btn.clicked.connect(self.reset_all)
        actions_layout.addWidget(self.reset_btn)
        
        # Chatterbox controls
        self.device_info_btn = QPushButton("📱 Chatterbox Device Info")
        self.device_info_btn.setToolTip("Xem thông tin device và memory usage")
        self.device_info_btn.clicked.connect(self.show_chatterbox_device_info)
        actions_layout.addWidget(self.device_info_btn)
        
        self.clear_cache_btn = QPushButton("🧹 Clear Chatterbox Cache")
        self.clear_cache_btn.setToolTip("Xóa voice cloning cache để giải phóng memory")
        self.clear_cache_btn.clicked.connect(self.clear_chatterbox_cache)
        actions_layout.addWidget(self.clear_cache_btn)
        
        actions_group.setLayout(actions_layout)
        panel_layout.addWidget(actions_group)
        
        panel_layout.addStretch()
        
        return panel
    
    def create_action_buttons(self, parent_layout):
        """Tạo action buttons responsive"""
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 16, 0, 0)
        buttons_frame.setLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng cấu hình nhân vật")
        self.status_label.setObjectName("status_label")
        buttons_layout.addWidget(self.status_label)
        
        buttons_layout.addStretch()
        
        # Action buttons
        self.cancel_btn = QPushButton("❌ Hủy")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.safe_reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        self.ok_btn = QPushButton("✅ Áp dụng cấu hình")
        self.ok_btn.setMinimumWidth(150)
        self.ok_btn.setDefault(True)
        self.ok_btn.setObjectName("primary_button")
        self.ok_btn.clicked.connect(self.safe_accept)
        buttons_layout.addWidget(self.ok_btn)
        
        parent_layout.addWidget(buttons_frame)
    
    def apply_responsive_styles(self):
        """Áp dụng styles responsive cho cross-platform"""
        style = """
        QDialog {
            background-color: #f5f5f7;
        }
        
        #dialog_title {
            font-size: 18px;
            font-weight: bold;
            color: #1d1d1f;
            padding: 8px;
        }
        
        #instructions {
            font-size: 14px;
            color: #86868b;
            padding: 4px 16px;
        }
        
        #section_header {
            font-size: 16px;
            font-weight: 600;
            color: #1d1d1f;
            padding: 8px 0;
        }
        
        #character_group {
            font-weight: 600;
            color: #007AFF;
            border: 2px solid #e5e5e7;
            border-radius: 12px;
            padding-top: 8px;
            margin: 4px;
        }
        
        #character_group:hover {
            border-color: #007AFF;
            background-color: #ffffff;
        }
        
        QPushButton {
            background-color: #ffffff;
            border: 1.5px solid #d1d1d6;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            color: #1d1d1f;
        }
        
        QPushButton:hover {
            background-color: #f0f0f0;
            border-color: #007AFF;
        }
        
        QPushButton:pressed {
            background-color: #e8e8e8;
        }
        
        #primary_button {
            background-color: #007AFF;
            color: white;
            border-color: #007AFF;
            font-weight: 600;
        }
        
        #primary_button:hover {
            background-color: #0056CC;
        }
        
        QLineEdit, QComboBox {
            border: 1.5px solid #d1d1d6;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            background-color: #ffffff;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border-color: #007AFF;
        }
        
        QCheckBox {
            font-size: 14px;
            color: #1d1d1f;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #d1d1d6;
        }
        
        QCheckBox::indicator:checked {
            background-color: #007AFF;
            border-color: #007AFF;
        }
        
        QGroupBox {
            font-size: 14px;
            font-weight: 500;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding-top: 8px;
            margin-top: 8px;
        }
        
        QTextEdit {
            border: 1px solid #d1d1d6;
            border-radius: 6px;
            background-color: #ffffff;
            font-size: 13px;
            padding: 8px;
        }
        
        #status_label {
            color: #86868b;
            font-size: 13px;
        }
        
        #header_frame {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 16px;
            border: 1px solid #e5e5e7;
        }
        """
        
        self.setStyleSheet(style)
    
    def setup_default_characters(self):
        """Setup nhân vật mặc định"""
        defaults = [
            {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính", "voice": "vi-VN-Standard-C (Nữ)"},
            {"name": "Nhân vật chính", "id": "character1", "gender": "Nữ", "voice": "vi-VN-Wavenet-A (Nữ)"},
            {"name": "Nhân vật phụ", "id": "character2", "gender": "Nam", "voice": "vi-VN-Wavenet-B (Nam)"},
            {"name": "Động vật", "id": "character3", "gender": "Nam", "voice": "vi-VN-Standard-D (Nam)"},
            {"name": "Nhân vật 5", "id": "character5", "gender": "Nữ", "voice": "vi-VN-Wavenet-C (Nữ)"},
            {"name": "Nhân vật 6", "id": "character6", "gender": "Nam", "voice": "vi-VN-Standard-B (Nam)"}
        ]
        
        for i, default in enumerate(defaults):
            if i < len(self.character_widgets):
                widget = self.character_widgets[i]
                widget.name_input.setText(default["name"])
                widget.id_input.setText(default["id"])
                widget.gender_combo.setCurrentText(default["gender"])
                widget.voice_combo.setCurrentText(default["voice"])
    
    def preview_character_voice(self, index):
        """Preview giọng của nhân vật với cross-platform audio playing"""
        if index >= len(self.character_widgets):
            return
            
        widget = self.character_widgets[index]
        if not widget.enabled_cb.isChecked():
            QMessageBox.information(self, "Thông báo", "Nhân vật này chưa được kích hoạt!")
            return
            
        name = widget.name_input.text() or f"Nhân vật {index+1}"
        voice = widget.voice_combo.currentText().split(' ')[0]
        
        sample_text = f"Xin chào, tôi là {name}. Đây là giọng đọc của tôi."
        
        # Disable preview button during generation
        widget.preview_btn.setEnabled(False)
        widget.preview_btn.setText("⏳")
        self.status_label.setText(f"Đang tạo preview cho {name}...")
        
        temp_file = tempfile.mktemp(suffix=".mp3")
        self.preview_files.append(temp_file)
        
        try:
            result = self.voice_generator.generate_voice_google_with_voice(
                sample_text, voice, temp_file
            )
            
            if result["success"]:
                # Cross-platform audio playing
                if platform.system() == "Darwin":  # macOS
                    os.system(f'open "{temp_file}"')
                elif platform.system() == "Windows":
                    os.system(f'start "" "{temp_file}"')
                else:  # Linux
                    os.system(f'xdg-open "{temp_file}"')
                    
                self.status_label.setText(f"Đang phát preview: {name} ({voice})")
            else:
                QMessageBox.warning(
                    self, "Lỗi", 
                    f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}"
                )
                self.status_label.setText("Lỗi tạo preview")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi preview: {str(e)}")
            self.status_label.setText("Lỗi preview")
        finally:
            widget.preview_btn.setEnabled(True)
            widget.preview_btn.setText("🔊")
    
    def test_all_voices(self):
        """Test tất cả giọng đã kích hoạt"""
        self.test_all_btn.setEnabled(False)
        self.test_all_btn.setText("⏳ Đang test...")
        
        try:
            active_widgets = [w for w in self.character_widgets if w.enabled_cb.isChecked()]
            if not active_widgets:
                QMessageBox.information(self, "Thông báo", "Không có nhân vật nào được kích hoạt!")
                return
            
            self.status_label.setText(f"Đang test {len(active_widgets)} giọng đọc...")
            
            for i, widget in enumerate(active_widgets):
                name = widget.name_input.text() or f"Nhân vật {i+1}"
                voice = widget.voice_combo.currentText().split(' ')[0]
                
                sample_text = f"Test giọng số {i+1}: Tôi là {name}."
                temp_file = tempfile.mktemp(suffix=f"_test_{i+1}.mp3")
                self.preview_files.append(temp_file)
                
                result = self.voice_generator.generate_voice_google_with_voice(
                    sample_text, voice, temp_file
                )
                
                if not result["success"]:
                    QMessageBox.warning(
                        self, "Cảnh báo", 
                        f"Không thể test giọng {name}: {result.get('error')}"
                    )
                    
            QMessageBox.information(
                self, "Hoàn thành", 
                f"✅ Đã test {len(active_widgets)} giọng đọc!\n\n"
                f"Các file audio test đã được tạo và sẽ tự động phát."
            )
            self.status_label.setText("Hoàn thành test tất cả giọng")
        finally:
            self.test_all_btn.setEnabled(True)
            self.test_all_btn.setText("🎵 Test tất cả giọng")
    
    def load_preset(self):
        """Load preset characters với UI responsive"""
        presets = {
            "🏰 Câu chuyện cổ tích": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Công chúa", "id": "princess", "gender": "Nữ"},
                {"name": "Hoàng tử", "id": "prince", "gender": "Nam"},
                {"name": "Phù thủy", "id": "witch", "gender": "Nữ"},
            ],
            "🌟 Phiêu lưu trẻ em": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Cô bé", "id": "girl", "gender": "Nữ"},
                {"name": "Cậu bé", "id": "boy", "gender": "Nam"},
                {"name": "Thú cưng", "id": "pet", "gender": "Nam"},
                {"name": "Người bạn", "id": "friend", "gender": "Nữ"},
            ],
            "👨‍👩‍👧‍👦 Gia đình": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Mẹ", "id": "mother", "gender": "Nữ"},
                {"name": "Bố", "id": "father", "gender": "Nam"},
                {"name": "Con gái", "id": "daughter", "gender": "Nữ"},
                {"name": "Con trai", "id": "son", "gender": "Nam"},
                {"name": "Ông bà", "id": "grandparent", "gender": "Trung tính"},
            ],
            "🎭 Kịch sân khấu": [
                {"name": "Người dẫn chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Nhân vật A", "id": "character_a", "gender": "Nữ"},
                {"name": "Nhân vật B", "id": "character_b", "gender": "Nam"},
                {"name": "Phản diện", "id": "villain", "gender": "Nam"},
                {"name": "Anh hùng", "id": "hero", "gender": "Nữ"},
            ]
        }
        
        preset_name, ok = QInputDialog.getItem(
            self, "🎭 Chọn Preset Nhân vật", 
            "Chọn loại preset phù hợp với nội dung của bạn:",
            list(presets.keys()), 0, False
        )
        
        if ok and preset_name:
            preset_chars = presets[preset_name]
            
            # Reset all first
            for widget in self.character_widgets:
                widget.enabled_cb.setChecked(False)
            
            # Apply preset
            for i, char in enumerate(preset_chars[:6]):  # Max 6
                if i < len(self.character_widgets):
                    widget = self.character_widgets[i]
                    widget.enabled_cb.setChecked(True)
                    widget.name_input.setText(char["name"])
                    widget.id_input.setText(char["id"])
                    widget.gender_combo.setCurrentText(char["gender"])
                    
                    # Auto-select voice based on gender
                    if char["gender"] == "Nữ":
                        widget.voice_combo.setCurrentText("vi-VN-Wavenet-A (Nữ)")
                    elif char["gender"] == "Nam":
                        widget.voice_combo.setCurrentText("vi-VN-Wavenet-B (Nam)")
                    else:
                        widget.voice_combo.setCurrentText("vi-VN-Standard-C (Nữ)")
            
            self.status_label.setText(f"Đã nạp preset: {preset_name}")
    
    def reset_all(self):
        """Reset tất cả về default"""
        self.setup_default_characters()
        for i, widget in enumerate(self.character_widgets):
            widget.enabled_cb.setChecked(i < 2)  # Only first 2 enabled
        self.status_label.setText("Đã reset về cấu hình mặc định")
    
    def get_characters_and_mapping(self):
        """Lấy danh sách characters và voice mapping với Chatterbox support"""
        characters = []
        voice_mapping = {}
        
        for i, widget_refs in enumerate(self.character_widget_refs):
            if widget_refs['enabled'].isChecked():
                name = widget_refs['name'].text().strip()
                char_id = widget_refs['id'].text().strip()
                gender = widget_refs['gender'].currentText()
                provider = widget_refs['provider'].currentText()
                voice = widget_refs['voice'].currentText()
                
                if name and char_id:
                    # Convert gender
                    gender_map = {"Nữ": "female", "Nam": "male", "Trung tính": "neutral"}
                    
                    # Base character info
                    character = {
                        "id": char_id,
                        "name": name,
                        "gender": gender_map[gender],
                        "suggested_voice": voice.split(' ')[0],
                        "provider": provider
                    }
                    
                    # Voice mapping with provider-specific settings
                    voice_config = {
                        "provider": provider,
                        "voice": voice.split(' ')[0]
                    }
                    
                    # Add Chatterbox-specific parameters
                    if "Chatterbox" in provider:
                        emotion_value = widget_refs['exag_slider'].value() / 100.0  # Convert to 0.0-2.0
                        speed_value = widget_refs['speed_slider'].value() / 100.0     # Convert to 0.5-2.0
                        
                        voice_config.update({
                            "emotion_exaggeration": emotion_value,
                            "speed": speed_value
                        })
                        
                        # Voice cloning sample if available
                        clone_status = widget_refs['clone_status']
                        if hasattr(clone_status, 'property') and clone_status.property('file_path'):
                            voice_config["voice_sample_path"] = clone_status.property('file_path')
                        
                        # Add to character info for display
                        character.update({
                            "emotion": emotion_value,
                            "speed": speed_value,
                            "voice_cloned": "voice_sample_path" in voice_config
                        })
                    
                    characters.append(character)
                    voice_mapping[char_id] = voice_config
        
        return characters, voice_mapping
    
    def cleanup_temp_files(self):
        """Clean up temp files safely"""
        for temp_file in self.preview_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.preview_files.clear()
    
    def safe_accept(self):
        """Validate và accept safely"""
        if self._closing:
            return
            
        characters, voice_mapping = self.get_characters_and_mapping()
        
        if not characters:
            QMessageBox.warning(self, "⚠️ Cảnh báo", 
                "Vui lòng kích hoạt ít nhất 1 nhân vật để tiếp tục!")
            return
        
        # Check for duplicate IDs
        ids = [char['id'] for char in characters]
        if len(ids) != len(set(ids)):
            QMessageBox.warning(self, "⚠️ Cảnh báo", 
                "ID nhân vật không được trùng lặp!\nVui lòng kiểm tra lại.")
            return
        
        self.character_configs = characters
        self.voice_mapping = voice_mapping
        
        self._closing = True
        self.cleanup_temp_files()
        super().accept()
    
    def safe_reject(self):
        """Reject safely without recursion"""
        if self._closing:
            return
            
        self._closing = True
        self.cleanup_temp_files()
        super().reject()
    
    def closeEvent(self, event):
        """Handle close event safely"""
        if not self._closing:
            self.safe_reject()
        else:
            super().closeEvent(event)
    
    def show_chatterbox_device_info(self):
        """Hiển thị thông tin device của Chatterbox TTS"""
        try:
            device_info = self.voice_generator.get_chatterbox_device_info()
            providers = self.voice_generator.get_available_tts_providers()
            
            # Find Chatterbox provider info
            chatterbox_info = None
            for provider in providers:
                if provider['id'] == 'chatterbox':
                    chatterbox_info = provider
                    break
            
            # Create info message
            message = "🤖 **Chatterbox TTS Device Information**\n\n"
            
            if device_info.get('available'):
                message += f"✅ **Status**: {device_info.get('initialized', False) and 'Initialized' or 'Available but not initialized'}\n"
                message += f"📱 **Device**: {device_info.get('device_name', 'Unknown')}\n"
                message += f"🔧 **Device Type**: {device_info.get('device', 'Unknown')}\n\n"
                
                # GPU specific info
                if 'cuda_version' in device_info:
                    message += f"🎯 **CUDA Version**: {device_info['cuda_version']}\n"
                    message += f"💾 **GPU Memory**: {device_info.get('gpu_memory_total', 'Unknown')} GB total\n"
                    message += f"🟢 **Available Memory**: {device_info.get('gpu_memory_available', 'Unknown')} GB\n\n"
                
                # Provider features
                if chatterbox_info:
                    message += f"🌍 **Languages**: {', '.join(chatterbox_info['languages'])}\n"
                    message += f"✨ **Features**:\n"
                    for feature in chatterbox_info['features']:
                        message += f"   • {feature}\n"
                
                # Memory usage if available
                memory_info = self.voice_generator.chatterbox_provider.get_memory_usage() if self.voice_generator.chatterbox_provider else {}
                if memory_info:
                    message += f"\n📊 **Current Memory Usage**:\n"
                    if 'gpu_allocated' in memory_info:
                        message += f"   • GPU Allocated: {memory_info['gpu_allocated']} MB\n"
                        message += f"   • GPU Cached: {memory_info['gpu_cached']} MB\n"
                    if 'cpu_memory_mb' in memory_info:
                        message += f"   • CPU Memory: {memory_info['cpu_memory_mb']} MB ({memory_info.get('cpu_memory_percent', 0):.1f}%)\n"
            else:
                message += f"❌ **Status**: Not available\n"
                message += f"🚫 **Reason**: {device_info.get('error', 'Unknown error')}\n\n"
                message += f"💡 **Possible solutions**:\n"
                message += f"   • Install PyTorch with CUDA support for GPU acceleration\n"
                message += f"   • Update graphics drivers\n"
                message += f"   • Ensure sufficient memory available\n"
            
            # Show dialog
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Chatterbox TTS Device Info")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lấy thông tin device:\n{str(e)}")
    
    def clear_chatterbox_cache(self):
        """Xóa cache của Chatterbox TTS"""
        try:
            if self.voice_generator.chatterbox_provider:
                # Get memory info before clearing
                memory_before = self.voice_generator.chatterbox_provider.get_memory_usage()
                
                # Clear cache
                self.voice_generator.cleanup_chatterbox()
                
                # Get memory info after clearing
                memory_after = self.voice_generator.chatterbox_provider.get_memory_usage() if self.voice_generator.chatterbox_provider else {}
                
                # Show result
                message = "🧹 **Chatterbox TTS Cache Cleared**\n\n"
                
                if memory_before and memory_after:
                    message += f"**Memory Usage Before/After**:\n"
                    if 'gpu_allocated' in memory_before:
                        gpu_freed = memory_before.get('gpu_allocated', 0) - memory_after.get('gpu_allocated', 0)
                        message += f"   • GPU: {memory_before['gpu_allocated']} → {memory_after['gpu_allocated']} MB (freed: {gpu_freed} MB)\n"
                    if 'cpu_memory_mb' in memory_before:
                        cpu_freed = memory_before.get('cpu_memory_mb', 0) - memory_after.get('cpu_memory_mb', 0)
                        message += f"   • CPU: {memory_before['cpu_memory_mb']} → {memory_after['cpu_memory_mb']} MB (freed: {cpu_freed} MB)\n"
                else:
                    message += "✅ Voice cloning cache cleared\n"
                    message += "✅ GPU cache cleared (if applicable)\n"
                    message += "✅ Memory resources freed\n"
                
                QMessageBox.information(self, "Thành công", message)
            else:
                QMessageBox.warning(self, "Cảnh báo", "Chatterbox TTS chưa được khởi tạo!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa cache:\n{str(e)}") 
=======
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QLineEdit, QGroupBox,
                               QGridLayout, QMessageBox, QTextEdit, QCheckBox,
                               QScrollArea, QSplitter, QTabWidget, QWidget,
                               QInputDialog, QFrame, QSlider, QSpinBox,
                               QFileDialog, QProgressBar)
from PySide6.QtCore import Qt, QSize, QTimer
import os
import tempfile
import platform

class ManualVoiceSetupDialog(QDialog):
    def __init__(self, voice_generator, parent=None):
        super().__init__(parent)
        self.voice_generator = voice_generator
        self.voice_mapping = {}
        self.character_configs = []
        self.preview_files = []
        self._closing = False  # Prevent recursion
        
        self.setWindowTitle("[THEATER] Cấu hình giọng đọc theo nhân vật")
        self.setModal(True)
        
        # Responsive sizing based on platform
        if platform.system() == "Darwin":  # macOS
            self.resize(1000, 700)
            self.setMinimumSize(900, 600)
        else:  # Windows/Linux
            self.resize(1100, 750)
            self.setMinimumSize(950, 650)
        
        self.setup_ui()
        self.setup_default_characters()
        self.apply_responsive_styles()
    
    def setup_ui(self):
        """Thiết lập UI responsive"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # Header với title và instructions
        self.create_header(main_layout)
        
        # Main content với splitter layout
        self.create_main_content(main_layout)
        
        # Bottom action buttons
        self.create_action_buttons(main_layout)
    
    def create_header(self, parent_layout):
        """Tạo header responsive"""
        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_frame.setLayout(header_layout)
        
        # Title
        title = QLabel("[THEATER] Cấu hình giọng đọc theo nhân vật")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "[IDEA] Thiết lập tối đa 6 nhân vật với giọng đọc riêng biệt. "
            "Chỉ nhân vật được tích [OK] sẽ được sử dụng để tạo audio."
        )
        instructions.setObjectName("instructions")
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(instructions)
        
        parent_layout.addWidget(header_frame)
    
    def create_main_content(self, parent_layout):
        """Tạo main content với responsive layout"""
        # Sử dụng horizontal splitter cho responsive layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Character configurations
        left_panel = self.create_characters_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Voice info và controls
        right_panel = self.create_info_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter ratio (70% - 30%)
        splitter.setSizes([700, 300])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        
        parent_layout.addWidget(splitter)
    
    def create_characters_panel(self):
        """Tạo panel cấu hình nhân vật với scroll"""
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel.setLayout(panel_layout)
        
        # Header
        chars_header = QLabel("[USERS] Cấu hình nhân vật (tối đa 6)")
        chars_header.setObjectName("section_header")
        panel_layout.addWidget(chars_header)
        
        # Scroll area cho characters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(12)
        scroll_content.setLayout(scroll_layout)
        
        # Tạo 6 character widgets với layout responsive
        self.character_widgets = []
        for i in range(6):
            char_widget = self.create_character_widget_responsive(i + 1)
            self.character_widgets.append(char_widget)
            scroll_layout.addWidget(char_widget)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        panel_layout.addWidget(scroll)
        
        return panel
    
    def create_character_widget_responsive(self, index):
        """Tạo widget nhân vật với responsive design"""
        group = QGroupBox(f"Nhân vật {index}")
        group.setObjectName("character_group")
        
        # Sử dụng grid layout responsive
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 16, 12, 12)
        group.setLayout(layout)
        
        # Row 1: Enable checkbox và Name
        enabled_cb = QCheckBox("Sử dụng")
        enabled_cb.setChecked(index <= 2)  # Default enable first 2
        layout.addWidget(enabled_cb, 0, 0)
        
        layout.addWidget(QLabel("Tên:"), 0, 1)
        name_input = QLineEdit()
        name_input.setPlaceholderText(f"Nhân vật {index}")
        layout.addWidget(name_input, 0, 2, 1, 2)  # Span 2 columns
        
        # Row 2: ID và Gender
        layout.addWidget(QLabel("ID:"), 1, 0)
        id_input = QLineEdit()
        id_input.setPlaceholderText(f"character{index}")
        layout.addWidget(id_input, 1, 1)
        
        layout.addWidget(QLabel("Giới tính:"), 1, 2)
        gender_combo = QComboBox()
        gender_combo.addItems(["Nữ", "Nam", "Trung tính"])
        layout.addWidget(gender_combo, 1, 3)
        
        # Row 3: TTS Provider selection
        layout.addWidget(QLabel("TTS Provider:"), 2, 0)
        provider_combo = QComboBox()
        provider_combo.addItems([
            "[EMOJI][EMOJI] Google TTS (Vietnamese)",
            "[BOT] Chatterbox TTS (English)",
            "[THEATER] ElevenLabs (English)",
            "[REFRESH] Auto-select"
        ])
        provider_combo.setCurrentText("[REFRESH] Auto-select")
        layout.addWidget(provider_combo, 2, 1, 1, 2)
        
        preview_btn = QPushButton("[SOUND]")
        preview_btn.setMaximumWidth(50)
        preview_btn.setToolTip("Preview giọng đọc")
        preview_btn.clicked.connect(
            lambda checked, idx=index-1: self.preview_character_voice(idx)
        )
        layout.addWidget(preview_btn, 2, 3)
        
        # Row 4: Voice selection (dynamic based on provider)
        layout.addWidget(QLabel("Giọng:"), 3, 0)
        voice_combo = QComboBox()
        self.update_voice_options(voice_combo, provider_combo.currentText())
        layout.addWidget(voice_combo, 3, 1, 1, 3)
        
        # Row 5: Chatterbox-specific controls (initially hidden)
        chatterbox_frame = QFrame()
        chatterbox_layout = QGridLayout()
        chatterbox_layout.setContentsMargins(0, 0, 0, 0)
        chatterbox_frame.setLayout(chatterbox_layout)
        
        # Emotion dropdown (using predefined emotions)
        chatterbox_layout.addWidget(QLabel("[THEATER] Emotion:"), 0, 0)
        emotion_combo = QComboBox()
        emotion_combo.addItems([
            "[EMOJI] neutral", "[EMOJI] happy", "[EMOJI] sad", "[EMOJI] excited", 
            "[EMOJI] calm", "[EMOJI] angry", "[EMOJI] romantic", "[EMOJI] fearful",
            "🤔 thoughtful", "[EMOJI] sleepy", "[EMOJI] confident", "[EMOJI] cheerful",
            "[EMOJI] melancholic", "[THEATER] dramatic", "[EMOJI] mysterious", "[EMOJI] surprised",
            "[EMOJI] frustrated", "🥺 pleading"
        ])
        emotion_combo.setCurrentText("[EMOJI] neutral")
        emotion_combo.setToolTip("Select emotion for voice generation")
        chatterbox_layout.addWidget(emotion_combo, 0, 1, 1, 2)
        
        # Exaggeration control
        chatterbox_layout.addWidget(QLabel("[TARGET] Exaggeration:"), 1, 0)
        exag_slider = QSlider(Qt.Horizontal)
        exag_slider.setRange(0, 250)     # 0.0-2.5 scaled to 0-250
        exag_slider.setValue(100)        # Default 1.0
        exag_slider.setToolTip("Emotion exaggeration: 0.0 (flat) - 2.5 (very dramatic)")
        chatterbox_layout.addWidget(exag_slider, 1, 1)
        
        exag_value = QLabel("1.00")
        exag_value.setMinimumWidth(40)
        chatterbox_layout.addWidget(exag_value, 1, 2)
        
        # Speed control
        chatterbox_layout.addWidget(QLabel("[FAST] Speed:"), 2, 0)
        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setRange(50, 200)   # 0.5-2.0 scaled to 50-200
        speed_slider.setValue(100)       # Default 1.0
        speed_slider.setToolTip("Speaking speed: 0.5 (slow) - 2.0 (fast)")
        chatterbox_layout.addWidget(speed_slider, 2, 1)
        
        speed_value = QLabel("1.0")
        speed_value.setMinimumWidth(30)
        chatterbox_layout.addWidget(speed_value, 2, 2)
        
        # Voice cloning
        chatterbox_layout.addWidget(QLabel("[EMOJI] Clone:"), 3, 0)
        clone_btn = QPushButton("[FOLDER] Upload Voice Sample")
        clone_btn.setToolTip("Upload 3-30s audio file to clone voice")
        chatterbox_layout.addWidget(clone_btn, 3, 1)
        
        clone_status = QLabel("No sample")
        clone_status.setObjectName("clone_status")
        chatterbox_layout.addWidget(clone_status, 3, 2)
        
        layout.addWidget(chatterbox_frame, 4, 0, 1, 4)
        chatterbox_frame.setVisible(False)  # Initially hidden
        
        # Update sliders display
        def update_exag_display(value):
            exag_value.setText(f"{value/100:.2f}")
        
        def update_speed_display(value):
            speed_value.setText(f"{value/100:.1f}")
        
        exag_slider.valueChanged.connect(update_exag_display)
        speed_slider.valueChanged.connect(update_speed_display)
        
        # Voice cloning handler
        def upload_voice_sample():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Voice Sample", "", 
                "Audio Files (*.wav *.mp3 *.flac *.m4a)"
            )
            if file_path:
                clone_status.setText(f"[OK] {os.path.basename(file_path)}")
                clone_status.setProperty("file_path", file_path)
            
        clone_btn.clicked.connect(upload_voice_sample)
        
        # Provider change handler
        def on_provider_changed():
            provider = provider_combo.currentText()
            self.update_voice_options(voice_combo, provider)
            
            # Show/hide Chatterbox controls
            is_chatterbox = "Chatterbox" in provider
            chatterbox_frame.setVisible(is_chatterbox)
            
            # Auto-update voice based on gender for Google TTS
            if "Google" in provider:
                gender = gender_combo.currentText()
                if gender == "Nữ":
                    voice_combo.setCurrentText("vi-VN-Wavenet-A (Nữ)")
                elif gender == "Nam":
                    voice_combo.setCurrentText("vi-VN-Wavenet-B (Nam)")
                else:  # Trung tính
                    voice_combo.setCurrentText("vi-VN-Standard-C (Nữ)")
        
        provider_combo.currentTextChanged.connect(on_provider_changed)
        gender_combo.currentTextChanged.connect(on_provider_changed)
        
        # Store references for later access
        widget_refs = {
            'enabled': enabled_cb,
            'name': name_input,
            'id': id_input,
            'gender': gender_combo,
            'provider': provider_combo,
            'voice': voice_combo,
            'chatterbox_frame': chatterbox_frame,
            'emotion_combo': emotion_combo,
            'exag_slider': exag_slider,
            'speed_slider': speed_slider,
            'clone_status': clone_status,
            'preview_btn': preview_btn
        }
        
        # Store widget references for character
        if not hasattr(self, 'character_widget_refs'):
            self.character_widget_refs = []
        self.character_widget_refs.append(widget_refs)
        
        # Enable/disable controls based on checkbox
        def toggle_enabled(checked):
            name_input.setEnabled(checked)
            id_input.setEnabled(checked)
            gender_combo.setEnabled(checked)
            provider_combo.setEnabled(checked)
            voice_combo.setEnabled(checked)
            chatterbox_frame.setEnabled(checked)
            preview_btn.setEnabled(checked)
            
        enabled_cb.toggled.connect(toggle_enabled)
        toggle_enabled(enabled_cb.isChecked())
        
        # Store references
        group.enabled_cb = enabled_cb
        group.name_input = name_input
        group.id_input = id_input
        group.gender_combo = gender_combo
        group.voice_combo = voice_combo
        group.preview_btn = preview_btn
        
        return group
    
    def update_voice_options(self, voice_combo, provider):
        """Update voice options based on selected provider"""
        voice_combo.clear()
        
        if "Google" in provider:
            voice_combo.addItems([
                "vi-VN-Standard-A (Nữ)",
                "vi-VN-Standard-B (Nam)", 
                "vi-VN-Standard-C (Nữ)",
                "vi-VN-Standard-D (Nam)",
                "vi-VN-Wavenet-A (Nữ)",
                "vi-VN-Wavenet-B (Nam)",
                "vi-VN-Wavenet-C (Nữ)", 
                "vi-VN-Wavenet-D (Nam)"
            ])
        elif "Chatterbox" in provider:
            # Get 28 predefined voices from ChatterboxVoicesManager
            try:
                from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                chatterbox_manager = ChatterboxVoicesManager()
                available_voices = chatterbox_manager.get_available_voices()
                
                # Add predefined voices
                voice_options = []
                for voice_id, voice_obj in sorted(available_voices.items()):
                    display_name = f"{voice_obj.name} ({voice_obj.gender})"
                    voice_options.append(display_name)
                
                # Add custom cloning option
                voice_options.append("[EMOJI] Custom Cloned Voice (upload sample)")
                voice_combo.addItems(voice_options)
                
                print(f"[OK] Loaded {len(voice_options)} voice options for Chatterbox TTS")
                
            except Exception as e:
                print(f"[WARNING] ChatterboxVoicesManager import failed: {e}")
                # Fallback if ChatterboxVoicesManager not available
                voice_combo.addItems([
                    "Default English Voice",
                    "[EMOJI] Custom Cloned Voice (upload sample)"
                ])
                
        elif "ElevenLabs" in provider:
            voice_combo.addItems([
                "Rachel (Female)",
                "Drew (Male)",
                "Clyde (Male)",
                "Paul (Male)",
                "Domi (Female)",
                "Dave (Male)",
                "Fin (Male)",
                "Sarah (Female)"
            ])
        else:  # Auto-select
            voice_combo.addItems([
                "[REFRESH] Auto-select based on text language",
                "[EMOJI][EMOJI] Vietnamese → Google TTS",
                "[EMOJI][EMOJI] English → Chatterbox/ElevenLabs"
            ])
    
    def create_info_panel(self):
        """Tạo panel thông tin và controls"""
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(8, 0, 0, 0)
        panel.setLayout(panel_layout)
        
        # Available voices info
        voices_group = QGroupBox("[CLIPBOARD] Giọng đọc có sẵn")
        voices_layout = QVBoxLayout()
        
        self.voices_text = QTextEdit()
        self.voices_text.setMaximumHeight(150)
        self.voices_text.setReadOnly(True)
        
        # Get Chatterbox status
        chatterbox_status = self.voice_generator.get_chatterbox_device_info()
        chatterbox_available = chatterbox_status.get('available', False)
        
        voices_info = f"""[BOT] CHATTERBOX TTS:
Status: {'[OK] Available' if chatterbox_available else '[EMOJI] Not available'}
Device: {chatterbox_status.get('device_name', 'Unknown')}
Features: 28 predefined voices, Voice cloning, Emotion control

[THEATER] 28 PREDEFINED VOICES:
[EMOJI] Male: Adrian, Alexander, Austin, Axel, Connor, Eli, Everett, 
Gabriel, Henry, Ian, Jeremiah, Jordan, Julian, Leonardo, 
Michael, Miles, Ryan, Thomas
[EMOJI] Female: Abigail, Alice, Cora, Elena, Emily, Gianna, 
Jade, Layla, Olivia, Taylor

[EMOJI][EMOJI] GOOGLE TTS (Vietnamese):
• vi-VN-Standard-A/B/C/D (Standard)  
• vi-VN-Wavenet-A/B/C/D (Natural)

[THEATER] ELEVENLABS (English):
• Rachel, Drew, Clyde, Paul, Domi, Dave, Fin, Sarah

[IDEA] Tips:
• Chatterbox = 28 high-quality voices + emotion control
• Wavenet = Chất lượng cao cho tiếng Việt
• Auto-select = Tự động chọn provider tốt nhất"""
        
        self.voices_text.setPlainText(voices_info)
        voices_layout.addWidget(self.voices_text)
        voices_group.setLayout(voices_layout)
        panel_layout.addWidget(voices_group)
        
        # Quick actions
        actions_group = QGroupBox("[FAST] Thao tác nhanh")
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)
        
        self.preset_btn = QPushButton("[CONFIG] Load Preset")
        self.preset_btn.setToolTip("Nạp cấu hình mẫu cho các thể loại khác nhau")
        self.preset_btn.clicked.connect(self.load_preset)
        actions_layout.addWidget(self.preset_btn)
        
        self.test_all_btn = QPushButton("[MUSIC] Test tất cả giọng")
        self.test_all_btn.setToolTip("Tạo audio test cho tất cả nhân vật đã kích hoạt")
        self.test_all_btn.clicked.connect(self.test_all_voices)
        actions_layout.addWidget(self.test_all_btn)
        
        self.reset_btn = QPushButton("[REFRESH] Reset về mặc định")
        self.reset_btn.setToolTip("Khôi phục cấu hình mặc định")
        self.reset_btn.clicked.connect(self.reset_all)
        actions_layout.addWidget(self.reset_btn)
        
        # Chatterbox controls
        self.device_info_btn = QPushButton("[MOBILE] Chatterbox Device Info")
        self.device_info_btn.setToolTip("Xem thông tin device và memory usage")
        self.device_info_btn.clicked.connect(self.show_chatterbox_device_info)
        actions_layout.addWidget(self.device_info_btn)
        
        self.clear_cache_btn = QPushButton("[CLEAN] Clear Chatterbox Cache")
        self.clear_cache_btn.setToolTip("Xóa voice cloning cache để giải phóng memory")
        self.clear_cache_btn.clicked.connect(self.clear_chatterbox_cache)
        actions_layout.addWidget(self.clear_cache_btn)
        
        actions_group.setLayout(actions_layout)
        panel_layout.addWidget(actions_group)
        
        panel_layout.addStretch()
        
        return panel
    
    def create_action_buttons(self, parent_layout):
        """Tạo action buttons responsive"""
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 16, 0, 0)
        buttons_frame.setLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng cấu hình nhân vật")
        self.status_label.setObjectName("status_label")
        buttons_layout.addWidget(self.status_label)
        
        buttons_layout.addStretch()
        
        # Action buttons
        self.cancel_btn = QPushButton("[EMOJI] Hủy")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.safe_reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        self.ok_btn = QPushButton("[OK] Áp dụng cấu hình")
        self.ok_btn.setMinimumWidth(150)
        self.ok_btn.setDefault(True)
        self.ok_btn.setObjectName("primary_button")
        self.ok_btn.clicked.connect(self.safe_accept)
        buttons_layout.addWidget(self.ok_btn)
        
        parent_layout.addWidget(buttons_frame)
    
    def apply_responsive_styles(self):
        """Áp dụng styles responsive cho cross-platform"""
        style = """
        QDialog {
            background-color: #f5f5f7;
        }
        
        #dialog_title {
            font-size: 18px;
            font-weight: bold;
            color: #1d1d1f;
            padding: 8px;
        }
        
        #instructions {
            font-size: 14px;
            color: #86868b;
            padding: 4px 16px;
        }
        
        #section_header {
            font-size: 16px;
            font-weight: 600;
            color: #1d1d1f;
            padding: 8px 0;
        }
        
        #character_group {
            font-weight: 600;
            color: #007AFF;
            border: 2px solid #e5e5e7;
            border-radius: 12px;
            padding-top: 8px;
            margin: 4px;
        }
        
        #character_group:hover {
            border-color: #007AFF;
            background-color: #ffffff;
        }
        
        QPushButton {
            background-color: #ffffff;
            border: 1.5px solid #d1d1d6;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            color: #1d1d1f;
        }
        
        QPushButton:hover {
            background-color: #f0f0f0;
            border-color: #007AFF;
        }
        
        QPushButton:pressed {
            background-color: #e8e8e8;
        }
        
        #primary_button {
            background-color: #007AFF;
            color: white;
            border-color: #007AFF;
            font-weight: 600;
        }
        
        #primary_button:hover {
            background-color: #0056CC;
        }
        
        QLineEdit, QComboBox {
            border: 1.5px solid #d1d1d6;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            background-color: #ffffff;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border-color: #007AFF;
        }
        
        QCheckBox {
            font-size: 14px;
            color: #1d1d1f;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #d1d1d6;
        }
        
        QCheckBox::indicator:checked {
            background-color: #007AFF;
            border-color: #007AFF;
        }
        
        QGroupBox {
            font-size: 14px;
            font-weight: 500;
            border: 1px solid #d1d1d6;
            border-radius: 8px;
            padding-top: 8px;
            margin-top: 8px;
        }
        
        QTextEdit {
            border: 1px solid #d1d1d6;
            border-radius: 6px;
            background-color: #ffffff;
            font-size: 13px;
            padding: 8px;
        }
        
        #status_label {
            color: #86868b;
            font-size: 13px;
        }
        
        #header_frame {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 16px;
            border: 1px solid #e5e5e7;
        }
        """
        
        self.setStyleSheet(style)
    
    def setup_default_characters(self):
        """Setup nhân vật mặc định"""
        defaults = [
            {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính", "voice": "vi-VN-Standard-C (Nữ)"},
            {"name": "Nhân vật chính", "id": "character1", "gender": "Nữ", "voice": "vi-VN-Wavenet-A (Nữ)"},
            {"name": "Nhân vật phụ", "id": "character2", "gender": "Nam", "voice": "vi-VN-Wavenet-B (Nam)"},
            {"name": "Động vật", "id": "character3", "gender": "Nam", "voice": "vi-VN-Standard-D (Nam)"},
            {"name": "Nhân vật 5", "id": "character5", "gender": "Nữ", "voice": "vi-VN-Wavenet-C (Nữ)"},
            {"name": "Nhân vật 6", "id": "character6", "gender": "Nam", "voice": "vi-VN-Standard-B (Nam)"}
        ]
        
        for i, default in enumerate(defaults):
            if i < len(self.character_widgets):
                widget = self.character_widgets[i]
                widget.name_input.setText(default["name"])
                widget.id_input.setText(default["id"])
                widget.gender_combo.setCurrentText(default["gender"])
                widget.voice_combo.setCurrentText(default["voice"])
    
    def preview_character_voice(self, index):
        """Preview giọng của nhân vật với cross-platform audio playing"""
        if index >= len(self.character_widgets):
            return
            
        widget = self.character_widgets[index]
        if not widget.enabled_cb.isChecked():
            QMessageBox.information(self, "Thông báo", "Nhân vật này chưa được kích hoạt!")
            return
            
        name = widget.name_input.text() or f"Nhân vật {index+1}"
        voice = widget.voice_combo.currentText().split(' ')[0]
        
        sample_text = f"Xin chào, tôi là {name}. Đây là giọng đọc của tôi."
        
        # Disable preview button during generation
        widget.preview_btn.setEnabled(False)
        widget.preview_btn.setText("⏳")
        self.status_label.setText(f"Đang tạo preview cho {name}...")
        
        temp_file = tempfile.mktemp(suffix=".mp3")
        self.preview_files.append(temp_file)
        
        try:
            result = self.voice_generator.generate_voice_google_with_voice(
                sample_text, voice, temp_file
            )
            
            if result["success"]:
                # Cross-platform audio playing
                if platform.system() == "Darwin":  # macOS
                    os.system(f'open "{temp_file}"')
                elif platform.system() == "Windows":
                    os.system(f'start "" "{temp_file}"')
                else:  # Linux
                    os.system(f'xdg-open "{temp_file}"')
                    
                self.status_label.setText(f"Đang phát preview: {name} ({voice})")
            else:
                QMessageBox.warning(
                    self, "Error", 
                    f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}"
                )
                self.status_label.setText("Error tạo preview")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error preview: {str(e)}")
            self.status_label.setText("Error preview")
        finally:
            widget.preview_btn.setEnabled(True)
            widget.preview_btn.setText("[SOUND]")
    
    def test_all_voices(self):
        """Test tất cả giọng đã kích hoạt"""
        self.test_all_btn.setEnabled(False)
        self.test_all_btn.setText("⏳ Đang test...")
        
        try:
            active_widgets = [w for w in self.character_widgets if w.enabled_cb.isChecked()]
            if not active_widgets:
                QMessageBox.information(self, "Thông báo", "Không có nhân vật nào được kích hoạt!")
                return
            
            self.status_label.setText(f"Đang test {len(active_widgets)} giọng đọc...")
            
            for i, widget in enumerate(active_widgets):
                name = widget.name_input.text() or f"Nhân vật {i+1}"
                voice = widget.voice_combo.currentText().split(' ')[0]
                
                sample_text = f"Test giọng số {i+1}: Tôi là {name}."
                temp_file = tempfile.mktemp(suffix=f"_test_{i+1}.mp3")
                self.preview_files.append(temp_file)
                
                result = self.voice_generator.generate_voice_google_with_voice(
                    sample_text, voice, temp_file
                )
                
                if not result["success"]:
                    QMessageBox.warning(
                        self, "Cảnh báo", 
                        f"Không thể test giọng {name}: {result.get('error')}"
                    )
                    
            QMessageBox.information(
                self, "Hoàn thành", 
                f"[OK] Đã test {len(active_widgets)} giọng đọc!\n\n"
                f"Các file audio test đã được tạo và sẽ tự động phát."
            )
            self.status_label.setText("Hoàn thành test tất cả giọng")
        finally:
            self.test_all_btn.setEnabled(True)
            self.test_all_btn.setText("[MUSIC] Test tất cả giọng")
    
    def load_preset(self):
        """Load preset characters với UI responsive"""
        presets = {
            "[EMOJI] Câu chuyện cổ tích": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Công chúa", "id": "princess", "gender": "Nữ"},
                {"name": "Hoàng tử", "id": "prince", "gender": "Nam"},
                {"name": "Phù thủy", "id": "witch", "gender": "Nữ"},
            ],
            "[STAR] Phiêu lưu trẻ em": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Cô bé", "id": "girl", "gender": "Nữ"},
                {"name": "Cậu bé", "id": "boy", "gender": "Nam"},
                {"name": "Thú cưng", "id": "pet", "gender": "Nam"},
                {"name": "Người bạn", "id": "friend", "gender": "Nữ"},
            ],
            "[EMOJI]‍[EMOJI]‍[EMOJI]‍[EMOJI] Gia đình": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Mẹ", "id": "mother", "gender": "Nữ"},
                {"name": "Bố", "id": "father", "gender": "Nam"},
                {"name": "Con gái", "id": "daughter", "gender": "Nữ"},
                {"name": "Con trai", "id": "son", "gender": "Nam"},
                {"name": "Ông bà", "id": "grandparent", "gender": "Trung tính"},
            ],
            "[THEATER] Kịch sân khấu": [
                {"name": "Người dẫn chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Nhân vật A", "id": "character_a", "gender": "Nữ"},
                {"name": "Nhân vật B", "id": "character_b", "gender": "Nam"},
                {"name": "Phản diện", "id": "villain", "gender": "Nam"},
                {"name": "Anh hùng", "id": "hero", "gender": "Nữ"},
            ]
        }
        
        preset_name, ok = QInputDialog.getItem(
            self, "[THEATER] Chọn Preset Nhân vật", 
            "Chọn loại preset phù hợp với nội dung của bạn:",
            list(presets.keys()), 0, False
        )
        
        if ok and preset_name:
            preset_chars = presets[preset_name]
            
            # Reset all first
            for widget in self.character_widgets:
                widget.enabled_cb.setChecked(False)
            
            # Apply preset
            for i, char in enumerate(preset_chars[:6]):  # Max 6
                if i < len(self.character_widgets):
                    widget = self.character_widgets[i]
                    widget.enabled_cb.setChecked(True)
                    widget.name_input.setText(char["name"])
                    widget.id_input.setText(char["id"])
                    widget.gender_combo.setCurrentText(char["gender"])
                    
                    # Auto-select voice based on gender
                    if char["gender"] == "Nữ":
                        widget.voice_combo.setCurrentText("vi-VN-Wavenet-A (Nữ)")
                    elif char["gender"] == "Nam":
                        widget.voice_combo.setCurrentText("vi-VN-Wavenet-B (Nam)")
                    else:
                        widget.voice_combo.setCurrentText("vi-VN-Standard-C (Nữ)")
            
            self.status_label.setText(f"Đã nạp preset: {preset_name}")
    
    def reset_all(self):
        """Reset tất cả về default"""
        self.setup_default_characters()
        for i, widget in enumerate(self.character_widgets):
            widget.enabled_cb.setChecked(i < 2)  # Only first 2 enabled
        self.status_label.setText("Đã reset về cấu hình mặc định")
    
    def get_characters_and_mapping(self):
        """Lấy danh sách characters và voice mapping với Chatterbox support"""
        characters = []
        voice_mapping = {}
        
        for i, widget_refs in enumerate(self.character_widget_refs):
            if widget_refs['enabled'].isChecked():
                name = widget_refs['name'].text().strip()
                char_id = widget_refs['id'].text().strip()
                gender = widget_refs['gender'].currentText()
                provider = widget_refs['provider'].currentText()
                voice = widget_refs['voice'].currentText()
                
                if name and char_id:
                    # Convert gender
                    gender_map = {"Nữ": "female", "Nam": "male", "Trung tính": "neutral"}
                    
                    # Base character info
                    character = {
                        "id": char_id,
                        "name": name,
                        "gender": gender_map[gender],
                        "suggested_voice": voice.split(' ')[0],
                        "provider": provider
                    }
                    
                    # Voice mapping with provider-specific settings
                    voice_config = {
                        "provider": provider,
                        "voice": voice.split(' ')[0]
                    }
                    
                    # Add Chatterbox-specific parameters
                    if "Chatterbox" in provider:
                        emotion_value = widget_refs['exag_slider'].value() / 100.0  # Convert to 0.0-2.0
                        speed_value = widget_refs['speed_slider'].value() / 100.0     # Convert to 0.5-2.0
                        
                        voice_config.update({
                            "emotion_exaggeration": emotion_value,
                            "speed": speed_value
                        })
                        
                        # Voice cloning sample if available
                        clone_status = widget_refs['clone_status']
                        if hasattr(clone_status, 'property') and clone_status.property('file_path'):
                            voice_config["voice_sample_path"] = clone_status.property('file_path')
                        
                        # Add to character info for display
                        character.update({
                            "emotion": emotion_value,
                            "speed": speed_value,
                            "voice_cloned": "voice_sample_path" in voice_config
                        })
                    
                    characters.append(character)
                    voice_mapping[char_id] = voice_config
        
        return characters, voice_mapping
    
    def cleanup_temp_files(self):
        """Clean up temp files safely"""
        for temp_file in self.preview_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.preview_files.clear()
    
    def safe_accept(self):
        """Validate và accept safely"""
        if self._closing:
            return
            
        characters, voice_mapping = self.get_characters_and_mapping()
        
        if not characters:
            QMessageBox.warning(self, "[WARNING] Cảnh báo", 
                "Vui lòng kích hoạt ít nhất 1 nhân vật để tiếp tục!")
            return
        
        # Check for duplicate IDs
        ids = [char['id'] for char in characters]
        if len(ids) != len(set(ids)):
            QMessageBox.warning(self, "[WARNING] Cảnh báo", 
                "ID nhân vật không được trùng lặp!\nVui lòng kiểm tra lại.")
            return
        
        self.character_configs = characters
        self.voice_mapping = voice_mapping
        
        self._closing = True
        self.cleanup_temp_files()
        super().accept()
    
    def safe_reject(self):
        """Reject safely without recursion"""
        if self._closing:
            return
            
        self._closing = True
        self.cleanup_temp_files()
        super().reject()
    
    def closeEvent(self, event):
        """Handle close event safely"""
        if not self._closing:
            self.safe_reject()
        else:
            super().closeEvent(event)
    
    def show_chatterbox_device_info(self):
        """Hiển thị thông tin device của Chatterbox TTS"""
        try:
            device_info = self.voice_generator.get_chatterbox_device_info()
            providers = self.voice_generator.get_available_tts_providers()
            
            # Find Chatterbox provider info
            chatterbox_info = None
            for provider in providers:
                if provider['id'] == 'chatterbox':
                    chatterbox_info = provider
                    break
            
            # Create info message
            message = "[BOT] **Chatterbox TTS Device Information**\n\n"
            
            if device_info.get('available'):
                message += f"[OK] **Status**: {device_info.get('initialized', False) and 'Initialized' or 'Available but not initialized'}\n"
                message += f"[MOBILE] **Device**: {device_info.get('device_name', 'Unknown')}\n"
                message += f"[TOOL] **Device Type**: {device_info.get('device', 'Unknown')}\n\n"
                
                # GPU specific info
                if 'cuda_version' in device_info:
                    message += f"[TARGET] **CUDA Version**: {device_info['cuda_version']}\n"
                    message += f"[EMOJI] **GPU Memory**: {device_info.get('gpu_memory_total', 'Unknown')} GB total\n"
                    message += f"[ON] **Available Memory**: {device_info.get('gpu_memory_available', 'Unknown')} GB\n\n"
                
                # Provider features
                if chatterbox_info:
                    message += f"[EMOJI] **Languages**: {', '.join(chatterbox_info['languages'])}\n"
                    message += f"[SPARKLE] **Features**:\n"
                    for feature in chatterbox_info['features']:
                        message += f"   • {feature}\n"
                
                # Memory usage if available
                memory_info = self.voice_generator.chatterbox_provider.get_memory_usage() if self.voice_generator.chatterbox_provider else {}
                if memory_info:
                    message += f"\n[STATS] **Current Memory Usage**:\n"
                    if 'gpu_allocated' in memory_info:
                        message += f"   • GPU Allocated: {memory_info['gpu_allocated']} MB\n"
                        message += f"   • GPU Cached: {memory_info['gpu_cached']} MB\n"
                    if 'cpu_memory_mb' in memory_info:
                        message += f"   • CPU Memory: {memory_info['cpu_memory_mb']} MB ({memory_info.get('cpu_memory_percent', 0):.1f}%)\n"
            else:
                message += f"[EMOJI] **Status**: Not available\n"
                message += f"[EMOJI] **Reason**: {device_info.get('error', 'Unknown error')}\n\n"
                message += f"[IDEA] **Possible solutions**:\n"
                message += f"   • Install PyTorch with CUDA support for GPU acceleration\n"
                message += f"   • Update graphics drivers\n"
                message += f"   • Ensure sufficient memory available\n"
            
            # Show dialog
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Chatterbox TTS Device Info")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể lấy thông tin device:\n{str(e)}")
    
    def clear_chatterbox_cache(self):
        """Xóa cache của Chatterbox TTS"""
        try:
            if self.voice_generator.chatterbox_provider:
                # Get memory info before clearing
                memory_before = self.voice_generator.chatterbox_provider.get_memory_usage()
                
                # Clear cache
                self.voice_generator.cleanup_chatterbox()
                
                # Get memory info after clearing
                memory_after = self.voice_generator.chatterbox_provider.get_memory_usage() if self.voice_generator.chatterbox_provider else {}
                
                # Show result
                message = "[CLEAN] **Chatterbox TTS Cache Cleared**\n\n"
                
                if memory_before and memory_after:
                    message += f"**Memory Usage Before/After**:\n"
                    if 'gpu_allocated' in memory_before:
                        gpu_freed = memory_before.get('gpu_allocated', 0) - memory_after.get('gpu_allocated', 0)
                        message += f"   • GPU: {memory_before['gpu_allocated']} → {memory_after['gpu_allocated']} MB (freed: {gpu_freed} MB)\n"
                    if 'cpu_memory_mb' in memory_before:
                        cpu_freed = memory_before.get('cpu_memory_mb', 0) - memory_after.get('cpu_memory_mb', 0)
                        message += f"   • CPU: {memory_before['cpu_memory_mb']} → {memory_after['cpu_memory_mb']} MB (freed: {cpu_freed} MB)\n"
                else:
                    message += "[OK] Voice cloning cache cleared\n"
                    message += "[OK] GPU cache cleared (if applicable)\n"
                    message += "[OK] Memory resources freed\n"
                
                QMessageBox.information(self, "Thành công", message)
            else:
                QMessageBox.warning(self, "Cảnh báo", "Chatterbox TTS chưa được khởi tạo!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể xóa cache:\n{str(e)}") 
>>>>>>> Stashed changes
