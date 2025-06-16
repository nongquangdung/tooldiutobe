from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QLineEdit, QGroupBox,
                               QGridLayout, QMessageBox, QTextEdit, QCheckBox)
from PySide6.QtCore import Qt
import os
import tempfile

class ManualVoiceSetupDialog(QDialog):
    def __init__(self, voice_generator, parent=None):
        super().__init__(parent)
        self.voice_generator = voice_generator
        self.voice_mapping = {}
        self.character_configs = []
        self.preview_files = []
        
        self.setWindowTitle("🎭 Cấu hình giọng đọc thủ công")
        self.setModal(True)
        self.resize(900, 700)
        
        self.setup_ui()
        self.setup_default_characters()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("🎭 Cấu hình giọng đọc thủ công (Tối đa 6 nhân vật)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "💡 Thiết lập tối đa 6 nhân vật với giọng đọc riêng biệt. "
            "Chỉ nhân vật được tích ✅ sẽ được sử dụng."
        )
        instructions.setStyleSheet("color: #666; margin: 5px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Characters setup area
        self.characters_group = QGroupBox("👥 Cấu hình nhân vật")
        characters_layout = QVBoxLayout()
        self.characters_group.setLayout(characters_layout)
        
        # Create 6 character slots
        self.character_widgets = []
        for i in range(6):
            char_widget = self.create_character_widget(i + 1)
            self.character_widgets.append(char_widget)
            characters_layout.addWidget(char_widget)
        
        layout.addWidget(self.characters_group)
        
        # Available voices info
        voices_info = QGroupBox("📋 Giọng đọc có sẵn")
        voices_layout = QVBoxLayout()
        
        self.voices_text = QTextEdit()
        self.voices_text.setMaximumHeight(100)
        self.voices_text.setReadOnly(True)
        
        voices_info_text = "🗣️ NAM: vi-VN-Standard-B, vi-VN-Standard-D, vi-VN-Wavenet-B, vi-VN-Wavenet-D\n"
        voices_info_text += "🗣️ NỮ: vi-VN-Standard-A, vi-VN-Standard-C, vi-VN-Wavenet-A, vi-VN-Wavenet-C"
        
        self.voices_text.setPlainText(voices_info_text)
        voices_layout.addWidget(self.voices_text)
        voices_info.setLayout(voices_layout)
        layout.addWidget(voices_info)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.preset_btn = QPushButton("⚙️ Load Preset")
        self.preset_btn.clicked.connect(self.load_preset)
        buttons_layout.addWidget(self.preset_btn)
        
        self.test_all_btn = QPushButton("🎵 Test tất cả")
        self.test_all_btn.clicked.connect(self.test_all_voices)
        buttons_layout.addWidget(self.test_all_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_all)
        buttons_layout.addWidget(self.reset_btn)
        
        buttons_layout.addStretch()
        
        self.cancel_btn = QPushButton("❌ Hủy")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        self.ok_btn = QPushButton("✅ Áp dụng")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)
        buttons_layout.addWidget(self.ok_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_character_widget(self, index):
        """Tạo widget cho 1 nhân vật"""
        group = QGroupBox(f"Nhân vật {index}")
        layout = QGridLayout()
        group.setLayout(layout)
        
        # Checkbox enable/disable
        enabled_cb = QCheckBox("Sử dụng")
        enabled_cb.setChecked(index <= 2)  # Default enable first 2
        layout.addWidget(enabled_cb, 0, 0)
        
        # Character name
        layout.addWidget(QLabel("Tên:"), 0, 1)
        name_input = QLineEdit()
        name_input.setPlaceholderText(f"Nhân vật {index}")
        layout.addWidget(name_input, 0, 2)
        
        # Character ID
        layout.addWidget(QLabel("ID:"), 0, 3)
        id_input = QLineEdit()
        id_input.setPlaceholderText(f"character{index}")
        layout.addWidget(id_input, 0, 4)
        
        # Gender selection
        layout.addWidget(QLabel("Giới tính:"), 1, 1)
        gender_combo = QComboBox()
        gender_combo.addItems(["Nữ", "Nam", "Trung tính"])
        layout.addWidget(gender_combo, 1, 2)
        
        # Voice selection
        layout.addWidget(QLabel("Giọng:"), 1, 3)
        voice_combo = QComboBox()
        vietnamese_voices = [
            "vi-VN-Standard-A (Nữ)",
            "vi-VN-Standard-B (Nam)", 
            "vi-VN-Standard-C (Nữ)",
            "vi-VN-Standard-D (Nam)",
            "vi-VN-Wavenet-A (Nữ)",
            "vi-VN-Wavenet-B (Nam)",
            "vi-VN-Wavenet-C (Nữ)", 
            "vi-VN-Wavenet-D (Nam)"
        ]
        voice_combo.addItems(vietnamese_voices)
        layout.addWidget(voice_combo, 1, 4)
        
        # Preview button
        preview_btn = QPushButton("🔊")
        preview_btn.setMaximumWidth(40)
        preview_btn.clicked.connect(
            lambda checked, idx=index-1: self.preview_character_voice(idx)
        )
        layout.addWidget(preview_btn, 1, 5)
        
        # Auto-update voice based on gender
        def update_voice_by_gender():
            gender = gender_combo.currentText()
            if gender == "Nữ":
                voice_combo.setCurrentText("vi-VN-Wavenet-A (Nữ)")
            elif gender == "Nam":
                voice_combo.setCurrentText("vi-VN-Wavenet-B (Nam)")
            else:  # Trung tính
                voice_combo.setCurrentText("vi-VN-Standard-C (Nữ)")
        
        gender_combo.currentTextChanged.connect(update_voice_by_gender)
        
        # Enable/disable based on checkbox
        def toggle_enabled(checked):
            name_input.setEnabled(checked)
            id_input.setEnabled(checked)
            gender_combo.setEnabled(checked)
            voice_combo.setEnabled(checked)
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
    
    def setup_default_characters(self):
        """Setup default characters"""
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
        """Preview giọng của nhân vật"""
        if index >= len(self.character_widgets):
            return
            
        widget = self.character_widgets[index]
        if not widget.enabled_cb.isChecked():
            return
            
        name = widget.name_input.text() or f"Nhân vật {index+1}"
        voice = widget.voice_combo.currentText().split(' ')[0]
        
        sample_text = f"Xin chào, tôi là {name}. Đây là giọng đọc của tôi."
        
        temp_file = tempfile.mktemp(suffix=".mp3")
        self.preview_files.append(temp_file)
        
        try:
            result = self.voice_generator.generate_voice_google_with_voice(
                sample_text, voice, temp_file
            )
            
            if result["success"]:
                os.system(f'start "" "{temp_file}"')
                QMessageBox.information(
                    self, "Preview", 
                    f"Đang phát audio preview cho {name}\nGiọng: {voice}"
                )
            else:
                QMessageBox.warning(
                    self, "Lỗi", 
                    f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi preview: {str(e)}")
    
    def test_all_voices(self):
        """Test tất cả giọng đã kích hoạt"""
        self.test_all_btn.setEnabled(False)
        self.test_all_btn.setText("⏳ Đang test...")
        
        try:
            active_count = 0
            for i, widget in enumerate(self.character_widgets):
                if widget.enabled_cb.isChecked():
                    active_count += 1
                    name = widget.name_input.text() or f"Nhân vật {i+1}"
                    voice = widget.voice_combo.currentText().split(' ')[0]
                    
                    sample_text = f"Test giọng số {active_count}: {name}"
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
                f"Đã test {active_count} giọng đọc! Kiểm tra các file audio đã tạo."
            )
        finally:
            self.test_all_btn.setEnabled(True)
            self.test_all_btn.setText("🎵 Test tất cả")
    
    def load_preset(self):
        """Load preset characters"""
        presets = {
            "Câu chuyện cổ tích": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Công chúa", "id": "princess", "gender": "Nữ"},
                {"name": "Hoàng tử", "id": "prince", "gender": "Nam"},
                {"name": "Phù thủy", "id": "witch", "gender": "Nữ"},
            ],
            "Phiêu lưu trẻ em": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Cô bé", "id": "girl", "gender": "Nữ"},
                {"name": "Cậu bé", "id": "boy", "gender": "Nam"},
                {"name": "Thú cưng", "id": "pet", "gender": "Nam"},
                {"name": "Người bạn", "id": "friend", "gender": "Nữ"},
            ],
            "Gia đình": [
                {"name": "Người kể chuyện", "id": "narrator", "gender": "Trung tính"},
                {"name": "Mẹ", "id": "mother", "gender": "Nữ"},
                {"name": "Bố", "id": "father", "gender": "Nam"},
                {"name": "Con gái", "id": "daughter", "gender": "Nữ"},
                {"name": "Con trai", "id": "son", "gender": "Nam"},
                {"name": "Ông bà", "id": "grandparent", "gender": "Trung tính"},
            ]
        }
        
        from PySide6.QtWidgets import QInputDialog
        preset_name, ok = QInputDialog.getItem(
            self, "Chọn Preset", "Chọn preset nhân vật:",
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
    
    def reset_all(self):
        """Reset tất cả về default"""
        self.setup_default_characters()
        for i, widget in enumerate(self.character_widgets):
            widget.enabled_cb.setChecked(i < 2)  # Only first 2 enabled
    
    def get_characters_and_mapping(self):
        """Lấy danh sách characters và voice mapping"""
        characters = []
        voice_mapping = {}
        
        for widget in self.character_widgets:
            if widget.enabled_cb.isChecked():
                name = widget.name_input.text().strip()
                char_id = widget.id_input.text().strip()
                gender = widget.gender_combo.currentText()
                voice = widget.voice_combo.currentText().split(' ')[0]
                
                if name and char_id:
                    # Convert gender
                    gender_map = {"Nữ": "female", "Nam": "male", "Trung tính": "neutral"}
                    
                    characters.append({
                        "id": char_id,
                        "name": name,
                        "gender": gender_map[gender],
                        "suggested_voice": voice
                    })
                    
                    voice_mapping[char_id] = voice
        
        return characters, voice_mapping
    
    def closeEvent(self, event):
        """Clean up temp files"""
        for temp_file in self.preview_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        super().closeEvent(event)
    
    def accept(self):
        """Validate và accept"""
        characters, voice_mapping = self.get_characters_and_mapping()
        
        if not characters:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng kích hoạt ít nhất 1 nhân vật!")
            return
        
        # Check for duplicate IDs
        ids = [char['id'] for char in characters]
        if len(ids) != len(set(ids)):
            QMessageBox.warning(self, "Cảnh báo", "ID nhân vật không được trùng lặp!")
            return
        
        self.character_configs = characters
        self.voice_mapping = voice_mapping
        
        super().accept()
    
    def reject(self):
        """Clean up và reject"""
        self.closeEvent(None)
        super().reject() 