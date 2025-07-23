<<<<<<< Updated upstream
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import platform
import json
from pathlib import Path
from .styles import (
    BUTTON_STYLE, LABEL_STYLE, STATUS_LABEL_STYLE, HIGHLIGHTED_LABEL_STYLE,
    GUIDE_TEXT_STYLE, SCRIPT_INFO_STYLE, CHARACTER_LABEL_STYLE,
    GENERATED_INFO_STYLE, IMPORTED_FILE_STYLE
)

class VideoGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, prompt, project_name, effects, use_custom_images=False, custom_images_folder=None,
                 voice_name="vi-VN-Standard-A", project_folder=None):
        super().__init__()
        self.prompt = prompt
        self.project_name = project_name
        self.effects = effects
        self.use_custom_images = use_custom_images
        self.custom_images_folder = custom_images_folder
        self.voice_name = voice_name
        self.project_folder = project_folder

    def run(self):
        try:
            # Existing run implementation
            pass
        except Exception as e:
            print(f"Error in video generation: {e}")

class AdvancedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Studio - Advanced Mode")
        self.setup_ui()
        
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Create tabs
        voice_studio_tab = QWidget()
        tab_widget.addTab(voice_studio_tab, "🎙️ Voice Studio")
        
        # Voice Studio Tab Layout
        voice_studio_layout = QVBoxLayout(voice_studio_tab)
        
        # Data Source Selection
        data_source_group = QGroupBox("📂 Data Source")
        data_source_layout = QVBoxLayout()
        
        # Source buttons
        source_buttons_layout = QHBoxLayout()
        
        self.import_file_btn = QPushButton("📄 Import JSON")
        self.import_file_btn.setStyleSheet(BUTTON_STYLE)
        self.import_file_btn.clicked.connect(self.import_script_file)
        source_buttons_layout.addWidget(self.import_file_btn)
        
        self.import_multiple_btn = QPushButton("📚 Import Multiple JSON")
        self.import_multiple_btn.setStyleSheet(BUTTON_STYLE)
        self.import_multiple_btn.clicked.connect(self.import_multiple_script_files)
        source_buttons_layout.addWidget(self.import_multiple_btn)
        
        self.load_generated_btn = QPushButton("📥 Load from Video Tab")
        self.load_generated_btn.setStyleSheet(BUTTON_STYLE)
        self.load_generated_btn.clicked.connect(self.load_generated_script_data)
        source_buttons_layout.addWidget(self.load_generated_btn)
        
        data_source_layout.addLayout(source_buttons_layout)
        
        # File status
        file_status_layout = QHBoxLayout()
        file_status_layout.addWidget(QLabel("Current File:"))
        self.imported_file_label = QLabel("No file imported")
        self.imported_file_label.setStyleSheet(IMPORTED_FILE_STYLE)
        file_status_layout.addWidget(self.imported_file_label)
        data_source_layout.addLayout(file_status_layout)
        
        data_source_group.setLayout(data_source_layout)
        voice_studio_layout.addWidget(data_source_group)
        
        # Script Overview
        script_overview_group = QGroupBox("📝 Script Overview")
        script_overview_layout = QVBoxLayout()
        
        # Characters
        characters_layout = QHBoxLayout()
        characters_layout.addWidget(QLabel("Characters:"))
        self.characters_label = QLabel("None")
        self.characters_label.setStyleSheet(CHARACTER_LABEL_STYLE)
        characters_layout.addWidget(self.characters_label)
        script_overview_layout.addLayout(characters_layout)
        
        # Segments count
        segments_layout = QHBoxLayout()
        segments_layout.addWidget(QLabel("Total Segments:"))
        self.segments_count_label = QLabel("0")
        self.segments_count_label.setStyleSheet(SCRIPT_INFO_STYLE)
        segments_layout.addWidget(self.segments_count_label)
        script_overview_layout.addLayout(segments_layout)
        
        # Script info
        self.script_info_label = QLabel("No script loaded")
        self.script_info_label.setStyleSheet(GENERATED_INFO_STYLE)
        script_overview_layout.addWidget(self.script_info_label)
        
        script_overview_group.setLayout(script_overview_layout)
        voice_studio_layout.addWidget(script_overview_group)
        
        # Manual Text Input
        manual_input_group = QGroupBox("✍️ Manual Text Input")
        manual_input_layout = QVBoxLayout()
        
        # Voice selection
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.manual_voice_combo = QComboBox()
        self.manual_voice_combo.addItem("Narrator")
        voice_layout.addWidget(self.manual_voice_combo)
        manual_input_layout.addLayout(voice_layout)
        
        # Emotion selection
        emotion_layout = QHBoxLayout()
        emotion_layout.addWidget(QLabel("Emotion:"))
        self.manual_emotion_combo = QComboBox()
        self.manual_emotion_combo.addItems(["Neutral", "Happy", "Sad", "Angry", "Excited"])
        emotion_layout.addWidget(self.manual_emotion_combo)
        manual_input_layout.addLayout(emotion_layout)
        
        # Inner voice options
        inner_voice_layout = QHBoxLayout()
        self.manual_inner_voice_check = QCheckBox("Inner Voice")
        inner_voice_layout.addWidget(self.manual_inner_voice_check)
        
        self.manual_inner_voice_type = QComboBox()
        self.manual_inner_voice_type.addItems(["Light", "Deep", "Dreamy"])
        self.manual_inner_voice_type.setEnabled(False)
        inner_voice_layout.addWidget(self.manual_inner_voice_type)
        
        manual_input_layout.addLayout(inner_voice_layout)
        
        # Connect inner voice checkbox
        self.manual_inner_voice_check.stateChanged.connect(
            lambda state: self.manual_inner_voice_type.setEnabled(state == Qt.Checked)
        )
        
        # Text input
        self.manual_text_input = QTextEdit()
        self.manual_text_input.setPlaceholderText("Enter your text here...")
        manual_input_layout.addWidget(self.manual_text_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        preview_btn = QPushButton("🎧 Preview")
        preview_btn.setStyleSheet(BUTTON_STYLE)
        preview_btn.clicked.connect(self.preview_manual_text)
        buttons_layout.addWidget(preview_btn)
        
        generate_btn = QPushButton("✨ Generate")
        generate_btn.setStyleSheet(BUTTON_STYLE)
        generate_btn.clicked.connect(self.generate_manual_text)
        buttons_layout.addWidget(generate_btn)
        
        manual_input_layout.addLayout(buttons_layout)
        
        manual_input_group.setLayout(manual_input_layout)
        voice_studio_layout.addWidget(manual_input_group)
        
        # Help section
        help_text = QLabel(r"""
• <b>Voice Selection</b>: Choose from available character voices
• <b>Emotion</b>: Select emotion for voice modulation
• <b>Inner Voice</b>: Enable for internal monologue effects
• <b>Preview</b>: Test voice settings before generating
""")
        help_text.setStyleSheet(GUIDE_TEXT_STYLE)
        help_text.setWordWrap(True)
        voice_studio_layout.addWidget(help_text)
        
        # Add stretch to push everything up
        voice_studio_layout.addStretch()

    def create_video_tab(self):
        # Implementation of video tab
        pass

    def create_emotion_config_tab(self):
        # Implementation of emotion config tab
        pass

    def create_license_tab(self):
        # Implementation of license tab
        pass

    def create_status_bar(self):
        # Implementation of status bar
        pass

    def update_api_status_indicator(self):
        # Implementation of API status update
        pass

    def setup_macos_style(self):
        # Implementation of macOS style setup
        pass

    def update_token_preview(self, mode):
        token_estimates = {
            "RAPID": "~500",
            "STANDARD": "~1000",
            "DETAILED": "~2000"
        }
        self.token_preview_label.setText(token_estimates.get(mode, "~500"))

    def generate_ai_request_form(self):
        mode = self.template_mode_combo.currentText()
        template = self.get_template_for_mode(mode)
        
        # Create and show dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("AI Request Form")
        layout = QVBoxLayout()
        
        # Template text
        template_text = QTextEdit()
        template_text.setPlainText(template)
        template_text.setReadOnly(True)
        layout.addWidget(template_text)
        
        # Copy button
        copy_btn = QPushButton("📋 Copy to Clipboard")
        copy_btn.setStyleSheet(BUTTON_STYLE)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(template))
        layout.addWidget(copy_btn)
        
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()

    def get_template_for_mode(self, mode):
        templates = {
            "RAPID": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator"],
    "segments": [
        {
            "character": "Narrator",
            "text": "Text content...",
            "emotion": "Neutral"
        }
    ]
}""",
            "STANDARD": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator", "Character1", "Character2"],
    "segments": [
        {
            "character": "Character name",
            "text": "Text content...",
            "emotion": "Emotion name",
            "inner_voice": false
        }
    ]
}""",
            "DETAILED": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator", "Character1", "Character2"],
    "segments": [
        {
            "character": "Character name",
            "text": "Text content...",
            "emotion": "Emotion name",
            "inner_voice": false,
            "inner_voice_type": "Light/Deep/Dreamy",
            "speed": 1.0,
            "pitch": 0,
            "emphasis": 1.2
        }
    ]
}"""
        }
        return templates.get(mode, templates["STANDARD"])

    def import_script_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn JSON Script File",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.process_imported_data(data)
                self.imported_file_label.setText(Path(file_path).name)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Không thể đọc file: {str(e)}")

    def import_multiple_script_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Chọn nhiều JSON Script Files",
            "",
            "JSON Files (*.json)"
        )
        if files:
            try:
                combined_data = {
                    "characters": set(),
                    "segments": []
                }
                for file_path in files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        combined_data["characters"].update(data.get("characters", []))
                        combined_data["segments"].extend(data.get("segments", []))
                
                combined_data["characters"] = list(combined_data["characters"])
                self.process_imported_data(combined_data)
                self.imported_file_label.setText(f"{len(files)} files imported")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Lỗi khi import files: {str(e)}")

    def load_generated_script_data(self):
        # Implementation depends on video tab data
        pass

    def process_imported_data(self, data):
        try:
            # Validate data structure
            if not isinstance(data, dict):
                raise ValueError("Invalid data format")
            
            if "characters" not in data or "segments" not in data:
                raise ValueError("Missing required fields")
            
            # Update UI
            self.characters_label.setText(", ".join(data["characters"]))
            self.segments_count_label.setText(str(len(data["segments"])))
            self.script_info_label.setText(f"✅ Loaded {len(data['segments'])} segments")
            
            # Update voice selection
            self.manual_voice_combo.clear()
            self.manual_voice_combo.addItems(data["characters"])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid script format: {str(e)}")

    def parse_manual_script(self):
        try:
            text = self.manual_script_input.toPlainText()
            data = json.loads(text)
            self.process_imported_data(data)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON format: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing script: {str(e)}")

    def preview_manual_text(self):
        # Implementation of preview functionality
        pass

    def generate_manual_text(self):
        text = self.manual_text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter some text")
            return
            
        # Create JSON structure
        data = {
            "characters": ["Narrator"],
            "segments": [{
                "character": self.manual_voice_combo.currentText(),
                "text": text,
                "emotion": self.manual_emotion_combo.currentText(),
                "inner_voice": self.manual_inner_voice_check.isChecked(),
                "inner_voice_type": self.manual_inner_voice_type.currentText() if self.manual_inner_voice_check.isChecked() else None
            }]
        }
        
        # Process the data
        self.process_imported_data(data)
=======
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import platform
import json
from pathlib import Path
from .styles import (
    BUTTON_STYLE, LABEL_STYLE, STATUS_LABEL_STYLE, HIGHLIGHTED_LABEL_STYLE,
    GUIDE_TEXT_STYLE, SCRIPT_INFO_STYLE, CHARACTER_LABEL_STYLE,
    GENERATED_INFO_STYLE, IMPORTED_FILE_STYLE
)

class VideoGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, prompt, project_name, effects, use_custom_images=False, custom_images_folder=None,
                 voice_name="vi-VN-Standard-A", project_folder=None):
        super().__init__()
        self.prompt = prompt
        self.project_name = project_name
        self.effects = effects
        self.use_custom_images = use_custom_images
        self.custom_images_folder = custom_images_folder
        self.voice_name = voice_name
        self.project_folder = project_folder

    def run(self):
        try:
            # Existing run implementation
            pass
        except Exception as e:
            print(f"Error in video generation: {e}")

class AdvancedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Studio - Advanced Mode")
        self.setup_ui()
        
    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Create tabs
        voice_studio_tab = QWidget()
        tab_widget.addTab(voice_studio_tab, "[MIC] Voice Studio")
        
        # Voice Studio Tab Layout
        voice_studio_layout = QVBoxLayout(voice_studio_tab)
        
        # Data Source Selection
        data_source_group = QGroupBox("[FOLDER] Data Source")
        data_source_layout = QVBoxLayout()
        
        # Source buttons
        source_buttons_layout = QHBoxLayout()
        
        self.import_file_btn = QPushButton("[FILE] Import JSON")
        self.import_file_btn.setStyleSheet(BUTTON_STYLE)
        self.import_file_btn.clicked.connect(self.import_script_file)
        source_buttons_layout.addWidget(self.import_file_btn)
        
        self.import_multiple_btn = QPushButton("[BOOKS] Import Multiple JSON")
        self.import_multiple_btn.setStyleSheet(BUTTON_STYLE)
        self.import_multiple_btn.clicked.connect(self.import_multiple_script_files)
        source_buttons_layout.addWidget(self.import_multiple_btn)
        
        self.load_generated_btn = QPushButton("[EMOJI] Load from Video Tab")
        self.load_generated_btn.setStyleSheet(BUTTON_STYLE)
        self.load_generated_btn.clicked.connect(self.load_generated_script_data)
        source_buttons_layout.addWidget(self.load_generated_btn)
        
        data_source_layout.addLayout(source_buttons_layout)
        
        # File status
        file_status_layout = QHBoxLayout()
        file_status_layout.addWidget(QLabel("Current File:"))
        self.imported_file_label = QLabel("No file imported")
        self.imported_file_label.setStyleSheet(IMPORTED_FILE_STYLE)
        file_status_layout.addWidget(self.imported_file_label)
        data_source_layout.addLayout(file_status_layout)
        
        data_source_group.setLayout(data_source_layout)
        voice_studio_layout.addWidget(data_source_group)
        
        # Script Overview
        script_overview_group = QGroupBox("[EDIT] Script Overview")
        script_overview_layout = QVBoxLayout()
        
        # Characters
        characters_layout = QHBoxLayout()
        characters_layout.addWidget(QLabel("Characters:"))
        self.characters_label = QLabel("None")
        self.characters_label.setStyleSheet(CHARACTER_LABEL_STYLE)
        characters_layout.addWidget(self.characters_label)
        script_overview_layout.addLayout(characters_layout)
        
        # Segments count
        segments_layout = QHBoxLayout()
        segments_layout.addWidget(QLabel("Total Segments:"))
        self.segments_count_label = QLabel("0")
        self.segments_count_label.setStyleSheet(SCRIPT_INFO_STYLE)
        segments_layout.addWidget(self.segments_count_label)
        script_overview_layout.addLayout(segments_layout)
        
        # Script info
        self.script_info_label = QLabel("No script loaded")
        self.script_info_label.setStyleSheet(GENERATED_INFO_STYLE)
        script_overview_layout.addWidget(self.script_info_label)
        
        script_overview_group.setLayout(script_overview_layout)
        voice_studio_layout.addWidget(script_overview_group)
        
        # Manual Text Input
        manual_input_group = QGroupBox("[EMOJI] Manual Text Input")
        manual_input_layout = QVBoxLayout()
        
        # Voice selection
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.manual_voice_combo = QComboBox()
        self.manual_voice_combo.addItem("Narrator")
        voice_layout.addWidget(self.manual_voice_combo)
        manual_input_layout.addLayout(voice_layout)
        
        # Emotion selection
        emotion_layout = QHBoxLayout()
        emotion_layout.addWidget(QLabel("Emotion:"))
        self.manual_emotion_combo = QComboBox()
        self.manual_emotion_combo.addItems(["Neutral", "Happy", "Sad", "Angry", "Excited"])
        emotion_layout.addWidget(self.manual_emotion_combo)
        manual_input_layout.addLayout(emotion_layout)
        
        # Inner voice options
        inner_voice_layout = QHBoxLayout()
        self.manual_inner_voice_check = QCheckBox("Inner Voice")
        inner_voice_layout.addWidget(self.manual_inner_voice_check)
        
        self.manual_inner_voice_type = QComboBox()
        self.manual_inner_voice_type.addItems(["Light", "Deep", "Dreamy"])
        self.manual_inner_voice_type.setEnabled(False)
        inner_voice_layout.addWidget(self.manual_inner_voice_type)
        
        manual_input_layout.addLayout(inner_voice_layout)
        
        # Connect inner voice checkbox
        self.manual_inner_voice_check.stateChanged.connect(
            lambda state: self.manual_inner_voice_type.setEnabled(state == Qt.Checked)
        )
        
        # Text input
        self.manual_text_input = QTextEdit()
        self.manual_text_input.setPlaceholderText("Enter your text here...")
        manual_input_layout.addWidget(self.manual_text_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        preview_btn = QPushButton("[EMOJI] Preview")
        preview_btn.setStyleSheet(BUTTON_STYLE)
        preview_btn.clicked.connect(self.preview_manual_text)
        buttons_layout.addWidget(preview_btn)
        
        generate_btn = QPushButton("[SPARKLE] Generate")
        generate_btn.setStyleSheet(BUTTON_STYLE)
        generate_btn.clicked.connect(self.generate_manual_text)
        buttons_layout.addWidget(generate_btn)
        
        manual_input_layout.addLayout(buttons_layout)
        
        manual_input_group.setLayout(manual_input_layout)
        voice_studio_layout.addWidget(manual_input_group)
        
        # Help section
        help_text = QLabel(r"""
• <b>Voice Selection</b>: Choose from available character voices
• <b>Emotion</b>: Select emotion for voice modulation
• <b>Inner Voice</b>: Enable for internal monologue effects
• <b>Preview</b>: Test voice settings before generating
""")
        help_text.setStyleSheet(GUIDE_TEXT_STYLE)
        help_text.setWordWrap(True)
        voice_studio_layout.addWidget(help_text)
        
        # Add stretch to push everything up
        voice_studio_layout.addStretch()

    def create_video_tab(self):
        # Implementation of video tab
        pass

    def create_emotion_config_tab(self):
        # Implementation of emotion config tab
        pass

    def create_license_tab(self):
        # Implementation of license tab
        pass

    def create_status_bar(self):
        # Implementation of status bar
        pass

    def update_api_status_indicator(self):
        # Implementation of API status update
        pass

    def setup_macos_style(self):
        # Implementation of macOS style setup
        pass

    def update_token_preview(self, mode):
        token_estimates = {
            "RAPID": "~500",
            "STANDARD": "~1000",
            "DETAILED": "~2000"
        }
        self.token_preview_label.setText(token_estimates.get(mode, "~500"))

    def generate_ai_request_form(self):
        mode = self.template_mode_combo.currentText()
        template = self.get_template_for_mode(mode)
        
        # Create and show dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("AI Request Form")
        layout = QVBoxLayout()
        
        # Template text
        template_text = QTextEdit()
        template_text.setPlainText(template)
        template_text.setReadOnly(True)
        layout.addWidget(template_text)
        
        # Copy button
        copy_btn = QPushButton("[CLIPBOARD] Copy to Clipboard")
        copy_btn.setStyleSheet(BUTTON_STYLE)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(template))
        layout.addWidget(copy_btn)
        
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()

    def get_template_for_mode(self, mode):
        templates = {
            "RAPID": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator"],
    "segments": [
        {
            "character": "Narrator",
            "text": "Text content...",
            "emotion": "Neutral"
        }
    ]
}""",
            "STANDARD": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator", "Character1", "Character2"],
    "segments": [
        {
            "character": "Character name",
            "text": "Text content...",
            "emotion": "Emotion name",
            "inner_voice": false
        }
    ]
}""",
            "DETAILED": """Tạo JSON script cho story với format sau:
{
    "characters": ["Narrator", "Character1", "Character2"],
    "segments": [
        {
            "character": "Character name",
            "text": "Text content...",
            "emotion": "Emotion name",
            "inner_voice": false,
            "inner_voice_type": "Light/Deep/Dreamy",
            "speed": 1.0,
            "pitch": 0,
            "emphasis": 1.2
        }
    ]
}"""
        }
        return templates.get(mode, templates["STANDARD"])

    def import_script_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn JSON Script File",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.process_imported_data(data)
                self.imported_file_label.setText(Path(file_path).name)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Không thể đọc file: {str(e)}")

    def import_multiple_script_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Chọn nhiều JSON Script Files",
            "",
            "JSON Files (*.json)"
        )
        if files:
            try:
                combined_data = {
                    "characters": set(),
                    "segments": []
                }
                for file_path in files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        combined_data["characters"].update(data.get("characters", []))
                        combined_data["segments"].extend(data.get("segments", []))
                
                combined_data["characters"] = list(combined_data["characters"])
                self.process_imported_data(combined_data)
                self.imported_file_label.setText(f"{len(files)} files imported")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error khi import files: {str(e)}")

    def load_generated_script_data(self):
        # Implementation depends on video tab data
        pass

    def process_imported_data(self, data):
        try:
            # Validate data structure
            if not isinstance(data, dict):
                raise ValueError("Invalid data format")
            
            if "characters" not in data or "segments" not in data:
                raise ValueError("Missing required fields")
            
            # Update UI
            self.characters_label.setText(", ".join(data["characters"]))
            self.segments_count_label.setText(str(len(data["segments"])))
            self.script_info_label.setText(f"[OK] Loaded {len(data['segments'])} segments")
            
            # Update voice selection
            self.manual_voice_combo.clear()
            self.manual_voice_combo.addItems(data["characters"])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid script format: {str(e)}")

    def parse_manual_script(self):
        try:
            text = self.manual_script_input.toPlainText()
            data = json.loads(text)
            self.process_imported_data(data)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON format: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing script: {str(e)}")

    def preview_manual_text(self):
        # Implementation of preview functionality
        pass

    def generate_manual_text(self):
        text = self.manual_text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter some text")
            return
            
        # Create JSON structure
        data = {
            "characters": ["Narrator"],
            "segments": [{
                "character": self.manual_voice_combo.currentText(),
                "text": text,
                "emotion": self.manual_emotion_combo.currentText(),
                "inner_voice": self.manual_inner_voice_check.isChecked(),
                "inner_voice_type": self.manual_inner_voice_type.currentText() if self.manual_inner_voice_check.isChecked() else None
            }]
        }
        
        # Process the data
        self.process_imported_data(data)
>>>>>>> Stashed changes
        self.manual_text_input.clear()  # Clear input after successful generation 