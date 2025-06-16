from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QMessageBox, QTextEdit, QGroupBox)
from PySide6.QtCore import Qt
import os
import tempfile

class CharacterVoiceDialog(QDialog):
    def __init__(self, characters, voice_generator, parent=None):
        super().__init__(parent)
        self.characters = characters
        self.voice_generator = voice_generator
        self.voice_mapping = {}
        self.preview_files = []  # Track temporary files
        
        self.setWindowTitle("Chọn giọng đọc cho từng nhân vật")
        self.setModal(True)
        self.resize(800, 600)
        
        self.setup_ui()
        self.load_characters()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("🎭 Cấu hình giọng đọc cho từng nhân vật")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Characters table
        self.characters_table = QTableWidget()
        self.characters_table.setColumnCount(5)
        self.characters_table.setHorizontalHeaderLabels([
            "Nhân vật", "Giới tính", "Giọng gợi ý", "Giọng chọn", "Preview"
        ])
        
        # Auto resize columns
        header = self.characters_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.characters_table)
        
        # Available voices info
        voices_info = QGroupBox("📋 Danh sách giọng đọc có sẵn")
        voices_layout = QVBoxLayout()
        
        self.voices_text = QTextEdit()
        self.voices_text.setMaximumHeight(120)
        self.voices_text.setReadOnly(True)
        
        # Load available voices
        voices_info_text = "🗣️ GIỌNG NAM:\n"
        voices_info_text += "• vi-VN-Standard-B, vi-VN-Standard-D\n"
        voices_info_text += "• vi-VN-Wavenet-B, vi-VN-Wavenet-D\n\n"
        voices_info_text += "🗣️ GIỌNG NỮ:\n"
        voices_info_text += "• vi-VN-Standard-A, vi-VN-Standard-C\n"
        voices_info_text += "• vi-VN-Wavenet-A, vi-VN-Wavenet-C\n\n"
        voices_info_text += "💡 Wavenet chất lượng cao hơn Standard"
        
        self.voices_text.setPlainText(voices_info_text)
        voices_layout.addWidget(self.voices_text)
        voices_info.setLayout(voices_layout)
        layout.addWidget(voices_info)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.test_all_btn = QPushButton("🎵 Test tất cả")
        self.test_all_btn.clicked.connect(self.test_all_voices)
        buttons_layout.addWidget(self.test_all_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_voices)
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
    
    def load_characters(self):
        """Load danh sách nhân vật vào table"""
        self.characters_table.setRowCount(len(self.characters))
        
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
        
        for row, character in enumerate(self.characters):
            # Character name
            name_item = QTableWidgetItem(character.get('name', character['id']))
            self.characters_table.setItem(row, 0, name_item)
            
            # Gender
            gender_text = {"male": "Nam", "female": "Nữ", "neutral": "Trung tính"}.get(
                character.get('gender', 'neutral'), 'Trung tính'
            )
            gender_item = QTableWidgetItem(gender_text)
            self.characters_table.setItem(row, 1, gender_item)
            
            # Suggested voice
            suggested = character.get('suggested_voice', 'vi-VN-Standard-A')
            suggested_item = QTableWidgetItem(suggested)
            self.characters_table.setItem(row, 2, suggested_item)
            
            # Voice selection combo
            voice_combo = QComboBox()
            voice_combo.addItems(vietnamese_voices)
            
            # Set default based on suggested voice
            for i, voice_text in enumerate(vietnamese_voices):
                if suggested in voice_text:
                    voice_combo.setCurrentIndex(i)
                    break
            
            self.characters_table.setCellWidget(row, 3, voice_combo)
            
            # Preview button
            preview_btn = QPushButton("🔊")
            preview_btn.setMaximumWidth(40)
            preview_btn.clicked.connect(
                lambda checked, r=row: self.preview_voice(r)
            )
            self.characters_table.setCellWidget(row, 4, preview_btn)
            
            # Store initial mapping
            self.voice_mapping[character['id']] = suggested
    
    def preview_voice(self, row):
        """Preview giọng đọc của nhân vật"""
        character = self.characters[row]
        voice_combo = self.characters_table.cellWidget(row, 3)
        selected_voice = voice_combo.currentText().split(' ')[0]  # Get voice name
        
        # Sample text
        sample_text = f"Xin chào, tôi là {character.get('name', character['id'])}. Đây là giọng đọc của tôi."
        
        # Create temp file
        temp_file = tempfile.mktemp(suffix=".mp3")
        self.preview_files.append(temp_file)
        
        try:
            # Generate voice
            result = self.voice_generator.generate_voice_google_with_voice(
                sample_text, selected_voice, temp_file
            )
            
            if result["success"]:
                # Play audio file (Windows)
                os.system(f'start "" "{temp_file}"')
                QMessageBox.information(
                    self, "Preview", 
                    f"Đang phát audio preview cho {character.get('name', character['id'])}\n"
                    f"Giọng: {selected_voice}"
                )
            else:
                QMessageBox.warning(
                    self, "Lỗi", 
                    f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi preview: {str(e)}")
    
    def test_all_voices(self):
        """Test tất cả giọng đã chọn"""
        self.test_all_btn.setEnabled(False)
        self.test_all_btn.setText("⏳ Đang test...")
        
        try:
            for row in range(len(self.characters)):
                character = self.characters[row]
                voice_combo = self.characters_table.cellWidget(row, 3)
                selected_voice = voice_combo.currentText().split(' ')[0]
                
                sample_text = f"Tôi là {character.get('name', character['id'])}"
                temp_file = tempfile.mktemp(suffix=f"_test_{character['id']}.mp3")
                self.preview_files.append(temp_file)
                
                result = self.voice_generator.generate_voice_google_with_voice(
                    sample_text, selected_voice, temp_file
                )
                
                if not result["success"]:
                    QMessageBox.warning(
                        self, "Cảnh báo", 
                        f"Không thể test giọng {character.get('name')}: {result.get('error')}"
                    )
                    
            QMessageBox.information(
                self, "Hoàn thành", 
                "Đã test tất cả giọng đọc! Kiểm tra các file audio đã tạo."
            )
        finally:
            self.test_all_btn.setEnabled(True)
            self.test_all_btn.setText("🎵 Test tất cả")
    
    def reset_voices(self):
        """Reset về giọng gợi ý"""
        for row, character in enumerate(self.characters):
            voice_combo = self.characters_table.cellWidget(row, 3)
            suggested = character.get('suggested_voice', 'vi-VN-Standard-A')
            
            for i in range(voice_combo.count()):
                if suggested in voice_combo.itemText(i):
                    voice_combo.setCurrentIndex(i)
                    break
    
    def get_voice_mapping(self):
        """Lấy mapping giọng đọc cuối cùng"""
        mapping = {}
        for row, character in enumerate(self.characters):
            voice_combo = self.characters_table.cellWidget(row, 3)
            selected_voice = voice_combo.currentText().split(' ')[0]
            mapping[character['id']] = selected_voice
        
        return mapping
    
    def closeEvent(self, event):
        """Clean up temp files khi đóng dialog"""
        for temp_file in self.preview_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        super().closeEvent(event)
    
    def accept(self):
        """Lưu voice mapping và đóng"""
        self.voice_mapping = self.get_voice_mapping()
        super().accept()
    
    def reject(self):
        """Hủy và clean up"""
        self.closeEvent(None)
        super().reject() 