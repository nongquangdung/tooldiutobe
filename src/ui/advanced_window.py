from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel, QTabWidget, QListWidget, 
    QListWidgetItem, QMessageBox, QProgressBar, QComboBox, 
    QLineEdit, QCheckBox, QSplitter, QScrollArea, QFrame, QGroupBox,
    QGridLayout, QSlider, QSpinBox, QFileDialog, QStatusBar, QDialog,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QSize
from PySide6.QtGui import QTextCursor, QFont, QIcon, QAction, QPixmap
import os
import sys
import json
import subprocess
import tempfile
import platform
import traceback
import shutil
from .manual_voice_setup_dialog import ManualVoiceSetupDialog

# Import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.video_pipeline import VideoPipeline
from video.effects_presets import EffectsPresets
from ai.prompt_templates import PromptTemplates
from core.api_manager import APIManager
from tts.voice_generator import VoiceGenerator

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
        self.pipeline = VideoPipeline()
    
    def run(self):
        def progress_callback(step, message):
            self.progress_updated.emit(step, message)
        
        # Tạo video với hoặc không có ảnh thủ công
        if self.use_custom_images and self.custom_images_folder:
            result = self.pipeline.create_video_with_custom_images(
                self.prompt, self.project_name, self.custom_images_folder, 
                self.effects, progress_callback
            )
        else:
            result = self.pipeline.create_video_from_prompt(
                self.prompt, self.project_name, self.effects, progress_callback,
                self.voice_name, self.project_folder
            )
        self.finished.emit(result)

class AdvancedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Video Generator - Advanced")
        
        # Tối ưu kích thước cho MacOS 13 inch
        if platform.system() == "Darwin":  # macOS
            window_size = get_macos_window_size()
            self.setGeometry(50, 50, window_size['default_width'], window_size['default_height'])
            self.setMinimumSize(window_size['min_width'], window_size['min_height'])
            self.setMaximumSize(window_size['max_width'], window_size['max_height'])
        else:
            self.setGeometry(100, 100, 1000, 700)
        
        # Khởi tạo pipeline và API manager
        self.pipeline = VideoPipeline()
        self.api_manager = APIManager()
        self.voice_generator = VoiceGenerator()
        self.current_project_id = None
        self.current_script_data = None  # Store generated script data
        
        # Thiết lập style cho macOS
        self.setup_macos_style()
        
        # Widget trung tâm với tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Giảm margin
        central_widget.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Tạo các tabs
        self.create_video_tab()
        self.create_voice_studio_tab()
        self.create_projects_tab()
        self.create_settings_tab()
        
        # Tạo status bar
        self.create_status_bar()
    
    def create_status_bar(self):
        """Tạo status bar với thông tin hệ thống"""
        status_bar = self.statusBar()
        
        # Status text chính
        self.status_text = "✅ Sẵn sàng"
        status_bar.showMessage(self.status_text)
        
        # API status indicator
        self.api_status_label = QLabel("🔑 API: Checking...")
        status_bar.addPermanentWidget(self.api_status_label)
        
        # Kiểm tra API status ngay khi khởi động
        self.update_api_status_indicator()
    
    def update_api_status_indicator(self):
        """Cập nhật chỉ báo trạng thái API"""
        # Kiểm tra xem api_status_label đã được tạo chưa
        if not hasattr(self, 'api_status_label'):
            return
            
        try:
            status = self.api_manager.get_provider_status()
            
            # Đếm số API available
            content_available = sum(status['content_providers'].values())
            image_available = sum(status['image_providers'].values()) 
            tts_available = sum(status['tts_providers'].values())
            
            total_available = content_available + image_available + tts_available
            
            if total_available >= 3:
                self.api_status_label.setText("🟢 API: Đầy đủ")
            elif total_available >= 1:
                self.api_status_label.setText("🟡 API: Một phần")
            else:
                self.api_status_label.setText("🔴 API: Chưa cấu hình")
                
        except Exception:
            if hasattr(self, 'api_status_label'):
                self.api_status_label.setText("⚠️ API: Lỗi")
    
    def setup_macos_style(self):
        """Thiết lập style phù hợp với macOS"""
        if platform.system() == "Darwin":
            # Font system của macOS
            font = QFont("-apple-system", 13)  # macOS system font
            self.setFont(font)
            
            # Sử dụng stylesheet từ file riêng
            self.setStyleSheet(get_macos_stylesheet())
    
    def create_video_tab(self):
        """Tab tạo video mới với layout tối ưu cho MacOS"""
        tab = QWidget()
        
        # Sử dụng scroll area để tránh tràn màn hình
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)  # Giảm spacing
        content_widget.setLayout(layout)
        
        # Group 1: Prompt và gợi ý
        prompt_group = QGroupBox("📝 Nội dung video")
        prompt_layout = QVBoxLayout()
        prompt_layout.setSpacing(6)
        
        # Gợi ý prompt - layout compact
        suggestions_layout = QGridLayout()
        suggestions_layout.addWidget(QLabel("Danh mục:"), 0, 0)
        
        self.category_combo = QComboBox()
        categories = PromptTemplates.get_all_categories()
        self.category_combo.addItem("-- Chọn danh mục --", "")
        for key, value in categories.items():
            self.category_combo.addItem(value["category"], key)
        self.category_combo.currentTextChanged.connect(self.load_prompt_suggestions)
        suggestions_layout.addWidget(self.category_combo, 0, 1)
        
        self.random_prompt_btn = QPushButton("🎲 Ngẫu nhiên")
        self.random_prompt_btn.clicked.connect(self.get_random_prompt)
        suggestions_layout.addWidget(self.random_prompt_btn, 0, 2)
        
        prompt_layout.addLayout(suggestions_layout)
        
        # Danh sách prompt gợi ý
        self.prompt_suggestions_list = QComboBox()
        self.prompt_suggestions_list.addItem("-- Chọn prompt mẫu --")
        self.prompt_suggestions_list.currentTextChanged.connect(self.use_suggested_prompt)
        prompt_layout.addWidget(self.prompt_suggestions_list)
        
        # Nhập prompt - giảm chiều cao
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ví dụ: Tạo video giới thiệu về du lịch Việt Nam với 5 điểm đến nổi tiếng...")
        self.prompt_input.setMaximumHeight(80)  # Giảm từ 100 xuống 80
        prompt_layout.addWidget(self.prompt_input)
        
        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)
        
        # Group 2: Cài đặt dự án
        project_group = QGroupBox("⚙️ Cài đặt dự án")
        project_layout = QGridLayout()
        project_layout.setSpacing(6)
        
        # Tên project
        project_layout.addWidget(QLabel("Tên dự án:"), 0, 0)
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("video_project")
        project_layout.addWidget(self.project_name_input, 0, 1, 1, 2)
        
        # Thư mục dự án
        project_layout.addWidget(QLabel("Thư mục:"), 1, 0)
        self.project_folder_input = QLineEdit()
        self.project_folder_input.setPlaceholderText("Mặc định: ./projects/")
        self.project_folder_input.setReadOnly(True)
        project_layout.addWidget(self.project_folder_input, 1, 1)
        
        self.select_project_folder_btn = QPushButton("📁")
        self.select_project_folder_btn.clicked.connect(self.select_project_folder)
        self.select_project_folder_btn.setMaximumWidth(40)
        project_layout.addWidget(self.select_project_folder_btn, 1, 2)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Group 3: Tùy chọn ảnh
        image_group = QGroupBox("🖼️ Tùy chọn ảnh")
        image_layout = QVBoxLayout()
        image_layout.setSpacing(6)
        
        # Radio buttons trong layout ngang
        image_options_layout = QHBoxLayout()
        self.auto_generate_radio = QCheckBox("Tự động tạo ảnh AI")
        self.auto_generate_radio.setChecked(True)
        self.manual_images_radio = QCheckBox("Chọn ảnh thủ công")
        image_options_layout.addWidget(self.auto_generate_radio)
        image_options_layout.addWidget(self.manual_images_radio)
        image_layout.addLayout(image_options_layout)
        
        # Chọn thư mục ảnh
        folder_layout = QHBoxLayout()
        self.select_images_btn = QPushButton("📁 Chọn thư mục ảnh")
        self.select_images_btn.clicked.connect(self.select_images_folder)
        self.select_images_btn.setEnabled(False)
        folder_layout.addWidget(self.select_images_btn)
        
        self.selected_images_label = QLabel("Chưa chọn thư mục ảnh")
        self.selected_images_label.setStyleSheet("color: gray; font-style: italic; font-size: 11px;")
        folder_layout.addWidget(self.selected_images_label)
        image_layout.addLayout(folder_layout)
        
        # Kết nối sự kiện
        self.manual_images_radio.toggled.connect(self.toggle_image_mode)
        
        image_group.setLayout(image_layout)
        layout.addWidget(image_group)
        
        # Group 4: Hiệu ứng
        effects_group = QGroupBox("✨ Hiệu ứng")
        effects_layout = QVBoxLayout()
        effects_layout.setSpacing(6)
        
        # Preset hiệu ứng
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        self.effects_preset_combo = QComboBox()
        presets = EffectsPresets.get_all_presets()
        for key, preset in presets.items():
            self.effects_preset_combo.addItem(f"{preset['name']} - {preset['description']}", key)
        self.effects_preset_combo.setCurrentText("Năng động")
        preset_layout.addWidget(self.effects_preset_combo)
        effects_layout.addLayout(preset_layout)
        
        # Cài đặt hiệu ứng tùy chỉnh
        custom_effects_layout = QHBoxLayout()
        self.zoom_checkbox = QCheckBox("Hiệu ứng zoom")
        self.zoom_checkbox.setChecked(True)
        self.transitions_checkbox = QCheckBox("Chuyển cảnh")
        self.transitions_checkbox.setChecked(True)
        custom_effects_layout.addWidget(self.zoom_checkbox)
        custom_effects_layout.addWidget(self.transitions_checkbox)
        effects_layout.addLayout(custom_effects_layout)
        
        effects_group.setLayout(effects_layout)
        layout.addWidget(effects_group)
        
        # Group 5: Actions
        actions_group = QGroupBox("🎬 Tạo video")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        self.generate_story_btn = QPushButton("📝 Tạo câu chuyện")
        self.generate_story_btn.clicked.connect(self.generate_story_only)
        self.generate_story_btn.setToolTip("Tạo kịch bản video từ prompt (Cmd+1)")
        self.generate_story_btn.setShortcut("Cmd+1" if platform.system() == "Darwin" else "Ctrl+1")
        actions_layout.addWidget(self.generate_story_btn, 0, 0)
        
        self.generate_audio_btn = QPushButton("🎵 Tạo Audio")
        self.generate_audio_btn.clicked.connect(self.generate_audio_only)
        self.generate_audio_btn.setEnabled(False)
        self.generate_audio_btn.setToolTip("Tạo audio từ kịch bản đã có (Cmd+2)")
        self.generate_audio_btn.setShortcut("Cmd+2" if platform.system() == "Darwin" else "Ctrl+2")
        actions_layout.addWidget(self.generate_audio_btn, 0, 1)
        
        # Nút tạo video hoàn chỉnh
        self.generate_video_btn = QPushButton("🎬 Tạo Video Hoàn chỉnh")
        self.generate_video_btn.clicked.connect(self.start_video_generation)
        self.generate_video_btn.setToolTip("Tạo video hoàn chỉnh với ảnh và âm thanh (Cmd+3)")
        self.generate_video_btn.setShortcut("Cmd+3" if platform.system() == "Darwin" else "Ctrl+3")
        actions_layout.addWidget(self.generate_video_btn, 1, 0, 1, 2)
        
        # Nút cấu hình giọng nói thủ công (luôn hiển thị)
        self.manual_voice_setup_btn = QPushButton("🎭 Cấu hình giọng theo nhân vật")
        self.manual_voice_setup_btn.clicked.connect(self.show_manual_voice_setup)
        self.manual_voice_setup_btn.setToolTip("Tạo và cấu hình giọng nói cho các nhân vật thủ công (Cmd+4)")
        self.manual_voice_setup_btn.setShortcut("Cmd+4" if platform.system() == "Darwin" else "Ctrl+4")
        actions_layout.addWidget(self.manual_voice_setup_btn, 2, 0, 1, 2)

        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Group 6: Progress và Status
        progress_group = QGroupBox("📊 Tiến trình")
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(6)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setStyleSheet("color: #666; font-size: 11px;")
        progress_layout.addWidget(self.progress_label)
        
        # Status và preview area
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #007AFF; font-weight: 500;")
        progress_layout.addWidget(self.status_label)
        
        # Preview content area - compact
        preview_label = QLabel("📄 Xem trước nội dung:")
        preview_label.setStyleSheet("font-weight: 600; margin-top: 8px;")
        progress_layout.addWidget(preview_label)
        
        self.content_preview = QTextEdit()
        self.content_preview.setReadOnly(True)
        self.content_preview.setMaximumHeight(120)  # Compact height
        self.content_preview.setPlaceholderText("Nội dung câu chuyện sẽ hiển thị ở đây sau khi tạo...")
        progress_layout.addWidget(self.content_preview)
        
        # Audio controls - compact layout
        audio_controls_layout = QGridLayout()
        audio_controls_layout.setSpacing(6)
        
        self.open_audio_folder_btn = QPushButton("📁 Thư mục Audio")
        self.open_audio_folder_btn.clicked.connect(self.open_audio_folder)
        self.open_audio_folder_btn.setEnabled(False)
        self.open_audio_folder_btn.setToolTip("Mở thư mục chứa các file audio đã tạo")
        audio_controls_layout.addWidget(self.open_audio_folder_btn, 0, 0)
        
        self.play_final_audio_btn = QPushButton("▶️ Nghe Audio")
        self.play_final_audio_btn.clicked.connect(self.play_final_audio)
        self.play_final_audio_btn.setEnabled(False)
        self.play_final_audio_btn.setToolTip("Phát file audio hoàn chỉnh đã ghép")
        audio_controls_layout.addWidget(self.play_final_audio_btn, 0, 1)
        
        progress_layout.addLayout(audio_controls_layout)
        
        # Voice settings - compact
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Giọng TTS:"))
        self.voice_combo = QComboBox()
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
        self.voice_combo.addItems(vietnamese_voices)
        voice_layout.addWidget(self.voice_combo)
        progress_layout.addLayout(voice_layout)
        
        progress_group.setLayout(progress_layout)
        progress_group.setVisible(False)  # Ẩn ban đầu, hiện khi cần
        layout.addWidget(progress_group)
        
        # Store references
        self.progress_group = progress_group
        self.last_audio_output_dir = None
        self.last_final_audio_path = None
        
        # Thêm stretch để đẩy nội dung lên trên
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        
        # Layout chính của tab
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, "🎬 Tạo Video")
    
    def create_voice_studio_tab(self):
        """Tab Voice Studio để cấu hình giọng theo nhân vật và tạo voice"""
        tab = QWidget()
        
        # Sử dụng scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        content_widget.setLayout(layout)
        
        # Group 1: Import Data
        import_group = QGroupBox("📥 Import Script Data")
        import_layout = QVBoxLayout()
        import_layout.setSpacing(8)
        
        # Source selection
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Nguồn dữ liệu:"))
        
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItem("📁 Import từ file JSON", "file")
        self.data_source_combo.addItem("🔄 Sử dụng data từ tab Tạo Video", "generated")
        self.data_source_combo.addItem("✏️ Nhập thủ công", "manual")
        self.data_source_combo.currentTextChanged.connect(self.switch_data_source)
        source_layout.addWidget(self.data_source_combo)
        
        source_layout.addStretch()
        import_layout.addLayout(source_layout)
        
        # File import section
        self.file_import_widget = QWidget()
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        self.import_file_btn = QPushButton("📁 Chọn file JSON")
        self.import_file_btn.clicked.connect(self.import_script_file)
        file_layout.addWidget(self.import_file_btn)
        
        self.imported_file_label = QLabel("Chưa chọn file")
        self.imported_file_label.setStyleSheet("color: gray; font-style: italic;")
        file_layout.addWidget(self.imported_file_label)
        
        file_layout.addStretch()
        self.file_import_widget.setLayout(file_layout)
        import_layout.addWidget(self.file_import_widget)
        
        # Generated data section
        self.generated_data_widget = QWidget()
        generated_layout = QVBoxLayout()
        generated_layout.setContentsMargins(0, 0, 0, 0)
        
        generated_info = QLabel("🔄 Sử dụng script data đã được tạo từ tab 'Tạo Video'")
        generated_info.setStyleSheet("color: #007AFF; font-weight: bold;")
        generated_layout.addWidget(generated_info)
        
        self.use_generated_btn = QPushButton("🔄 Load Data từ tab Tạo Video")
        self.use_generated_btn.clicked.connect(self.load_generated_script_data)
        generated_layout.addWidget(self.use_generated_btn)
        
        self.generated_data_widget.setLayout(generated_layout)
        self.generated_data_widget.setVisible(False)
        import_layout.addWidget(self.generated_data_widget)
        
        # Manual input section
        self.manual_input_widget = QWidget()
        manual_layout = QVBoxLayout()
        manual_layout.setContentsMargins(0, 0, 0, 0)
        
        manual_layout.addWidget(QLabel("✏️ Nhập JSON script:"))
        self.manual_script_input = QTextEdit()
        self.manual_script_input.setPlaceholderText("Paste JSON script vào đây...")
        self.manual_script_input.setMaximumHeight(120)
        manual_layout.addWidget(self.manual_script_input)
        
        self.parse_manual_btn = QPushButton("✅ Parse JSON")
        self.parse_manual_btn.clicked.connect(self.parse_manual_script)
        manual_layout.addWidget(self.parse_manual_btn)
        
        self.manual_input_widget.setLayout(manual_layout)
        self.manual_input_widget.setVisible(False)
        import_layout.addWidget(self.manual_input_widget)
        
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # Group 2: Script Overview
        overview_group = QGroupBox("📋 Script Overview")
        overview_layout = QVBoxLayout()
        overview_layout.setSpacing(8)
        
        # Script info
        self.script_info_label = QLabel("Chưa load script data")
        self.script_info_label.setStyleSheet("color: #666; font-style: italic;")
        overview_layout.addWidget(self.script_info_label)
        
        # Characters list
        characters_layout = QHBoxLayout()
        characters_layout.addWidget(QLabel("Nhân vật:"))
        self.characters_label = QLabel("Chưa có data")
        self.characters_label.setStyleSheet("font-weight: bold; color: #007AFF;")
        characters_layout.addWidget(self.characters_label)
        characters_layout.addStretch()
        overview_layout.addLayout(characters_layout)
        
        # Segments count
        segments_layout = QHBoxLayout()
        segments_layout.addWidget(QLabel("Số segments:"))
        self.segments_count_label = QLabel("0")
        self.segments_count_label.setStyleSheet("font-weight: bold; color: #007AFF;")
        segments_layout.addWidget(self.segments_count_label)
        segments_layout.addStretch()
        overview_layout.addLayout(segments_layout)
        
        overview_group.setLayout(overview_layout)
        layout.addWidget(overview_group)
        
        # Group 4: Advanced Chatterbox Controls (Manual Configuration)
        chatterbox_group = QGroupBox("🎛️ Cấu hình Chatterbox TTS chi tiết (Nâng cao)")
        chatterbox_layout = QVBoxLayout()
        chatterbox_layout.setSpacing(8)
        
        # Enable/disable toggle
        chatterbox_controls_layout = QHBoxLayout()
        self.enable_chatterbox_manual = QCheckBox("Sử dụng cấu hình thủ công cho Chatterbox TTS")
        self.enable_chatterbox_manual.toggled.connect(self.toggle_chatterbox_manual_controls)
        chatterbox_controls_layout.addWidget(self.enable_chatterbox_manual)
        
        # Auto emotion mapping toggle
        self.enable_emotion_mapping = QCheckBox("🎭 Tự động điều chỉnh cảm xúc theo script")
        self.enable_emotion_mapping.setChecked(True)  # Default enabled
        self.enable_emotion_mapping.setToolTip("Tự động map emotion labels (happy, sad, excited...) thành emotion exaggeration values")
        chatterbox_controls_layout.addWidget(self.enable_emotion_mapping)
        
        chatterbox_controls_layout.addStretch()
        chatterbox_layout.addLayout(chatterbox_controls_layout)
        
        # Manual controls container
        self.chatterbox_manual_widget = QWidget()
        chatterbox_manual_layout = QVBoxLayout()
        chatterbox_manual_layout.setContentsMargins(20, 10, 10, 10)
        
        # Global settings với input fields và sliders
        global_settings_layout = QGridLayout()
        global_settings_layout.setSpacing(8)
        
        # Emotion exaggeration row
        global_settings_layout.addWidget(QLabel("🎭 Emotion Exaggeration:"), 0, 0)
        
        # Emotion slider
        self.emotion_slider = QSlider(Qt.Horizontal)
        self.emotion_slider.setRange(0, 300)  # 0.0 to 3.0
        self.emotion_slider.setValue(100)  # Default 1.0
        self.emotion_slider.valueChanged.connect(self.update_emotion_from_slider)
        global_settings_layout.addWidget(self.emotion_slider, 0, 1)
        
        # Emotion input field
        self.emotion_input = QLineEdit()
        self.emotion_input.setText("1.0")
        self.emotion_input.setMaximumWidth(60)
        self.emotion_input.setAlignment(Qt.AlignCenter)
        self.emotion_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
        """)
        self.emotion_input.textChanged.connect(self.update_emotion_from_input)
        global_settings_layout.addWidget(self.emotion_input, 0, 2)
        
        global_settings_layout.addWidget(QLabel("(0.0-3.0)"), 0, 3)
        
        # Speed row
        global_settings_layout.addWidget(QLabel("⚡ Speed:"), 1, 0)
        
        # Speed slider
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 200)  # 0.5 to 2.0
        self.speed_slider.setValue(100)  # Default 1.0
        self.speed_slider.valueChanged.connect(self.update_speed_from_slider)
        global_settings_layout.addWidget(self.speed_slider, 1, 1)
        
        # Speed input field
        self.speed_input = QLineEdit()
        self.speed_input.setText("1.0")
        self.speed_input.setMaximumWidth(60)
        self.speed_input.setAlignment(Qt.AlignCenter)
        self.speed_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
        """)
        self.speed_input.textChanged.connect(self.update_speed_from_input)
        global_settings_layout.addWidget(self.speed_input, 1, 2)
        
        global_settings_layout.addWidget(QLabel("(0.5-2.0)"), 1, 3)
        
        # CFG Weight row (NEW)
        global_settings_layout.addWidget(QLabel("🎚️ CFG Weight:"), 2, 0)
        
        # CFG Weight slider
        self.cfg_weight_slider = QSlider(Qt.Horizontal)
        self.cfg_weight_slider.setRange(0, 100)  # 0.0 to 1.0
        self.cfg_weight_slider.setValue(50)  # Default 0.5
        self.cfg_weight_slider.valueChanged.connect(self.update_cfg_weight_from_slider)
        global_settings_layout.addWidget(self.cfg_weight_slider, 2, 1)
        
        # CFG Weight input field
        self.cfg_weight_input = QLineEdit()
        self.cfg_weight_input.setText("0.5")
        self.cfg_weight_input.setMaximumWidth(60)
        self.cfg_weight_input.setAlignment(Qt.AlignCenter)
        self.cfg_weight_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
            }
        """)
        self.cfg_weight_input.textChanged.connect(self.update_cfg_weight_from_input)
        global_settings_layout.addWidget(self.cfg_weight_input, 2, 2)
        
        global_settings_layout.addWidget(QLabel("(0.0-1.0)"), 2, 3)
        
        # Voice selection row (NEW)
        global_settings_layout.addWidget(QLabel("🗣️ Default Voice:"), 3, 0)
        
        # Voice combo
        self.default_voice_combo = QComboBox()
        self.default_voice_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px;
                color: black;
            }
            QComboBox::drop-down {
                background-color: white;
            }
            QComboBox::down-arrow {
                color: black;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #007AFF;
                selection-color: white;
            }
        """)
        self.update_default_voice_options()
        global_settings_layout.addWidget(self.default_voice_combo, 3, 1, 1, 2)
        
        # Voice preview button
        self.preview_default_voice_btn = QPushButton("🎧")
        self.preview_default_voice_btn.setMaximumWidth(40)
        self.preview_default_voice_btn.setToolTip("Preview default voice")
        self.preview_default_voice_btn.clicked.connect(self.preview_default_voice)
        global_settings_layout.addWidget(self.preview_default_voice_btn, 3, 3)
        
        chatterbox_manual_layout.addLayout(global_settings_layout)
        
        # Character-specific settings
        char_specific_label = QLabel("🎭 Cấu hình riêng cho từng nhân vật:")
        char_specific_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        chatterbox_manual_layout.addWidget(char_specific_label)
        
        # Character settings table
        self.character_settings_table = QTableWidget()
        self.character_settings_table.setColumnCount(9)  # Tăng lên 9 columns (thêm Voice Mode)
        self.character_settings_table.setHorizontalHeaderLabels([
            "Nhân vật", "Emotion", "Speed", "CFG Weight", "Mode", "Voice/Prompt/Clone", "Quick", "Status", "Preview"
        ])
        self.character_settings_table.horizontalHeader().setStretchLastSection(False)
        self.character_settings_table.setMaximumHeight(150)
        
        # Set column widths
        header = self.character_settings_table.horizontalHeader()
        header.resizeSection(0, 120)  # Character name
        header.resizeSection(1, 80)   # Emotion
        header.resizeSection(2, 80)   # Speed  
        header.resizeSection(3, 80)   # CFG Weight
        header.resizeSection(4, 150)  # Voice
        header.resizeSection(5, 80)   # Preview
        
        chatterbox_manual_layout.addWidget(self.character_settings_table)
        
        # Voice cloning section
        voice_clone_layout = QHBoxLayout()
        voice_clone_layout.addWidget(QLabel("🎙️ Voice Cloning:"))
        
        self.enable_voice_cloning = QCheckBox("Bật voice cloning")
        self.enable_voice_cloning.toggled.connect(self.toggle_voice_cloning)
        voice_clone_layout.addWidget(self.enable_voice_cloning)
        
        self.voice_clone_folder_btn = QPushButton("📁 Chọn thư mục voice samples")
        self.voice_clone_folder_btn.clicked.connect(self.select_voice_clone_folder)
        self.voice_clone_folder_btn.setEnabled(False)
        voice_clone_layout.addWidget(self.voice_clone_folder_btn)
        
        voice_clone_layout.addStretch()
        chatterbox_manual_layout.addLayout(voice_clone_layout)
        
        self.voice_clone_path_label = QLabel("Chưa chọn thư mục voice samples")
        self.voice_clone_path_label.setStyleSheet("color: gray; font-style: italic; margin-left: 20px;")
        chatterbox_manual_layout.addWidget(self.voice_clone_path_label)
        
        # 💡 VOICE GENERATION HELP
        help_layout = QVBoxLayout()
        help_layout.addWidget(QLabel("💡 Hướng dẫn sử dụng:"))
        
        help_text = QLabel("""
• <b>Voice Prompt</b>: Nhập mô tả giọng nói cho từng nhân vật riêng biệt trong bảng dưới
• <b>Voice Clone</b>: Chọn thư mục chứa audio samples để clone giọng cho từng nhân vật  
• <b>Priority</b>: Voice Prompt > Voice Clone > Voice Selection
• <b>Preview</b>: Nhấn nút 🎧 để nghe thử giọng với settings hiện tại
        """)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #666; font-size: 12px; padding: 8px; background-color: #f8f8f8; border-radius: 4px;")
        help_layout.addWidget(help_text)
        
        chatterbox_manual_layout.addLayout(help_layout)
        
        # Preset buttons
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("🎨 Presets:"))
        
        self.preset_natural_btn = QPushButton("🌿 Natural")
        self.preset_natural_btn.clicked.connect(lambda: self.apply_preset("natural"))
        preset_layout.addWidget(self.preset_natural_btn)
        
        self.preset_dramatic_btn = QPushButton("🎭 Dramatic")
        self.preset_dramatic_btn.clicked.connect(lambda: self.apply_preset("dramatic"))
        preset_layout.addWidget(self.preset_dramatic_btn)
        
        self.preset_fast_btn = QPushButton("⚡ Fast Speech")
        self.preset_fast_btn.clicked.connect(lambda: self.apply_preset("fast"))
        preset_layout.addWidget(self.preset_fast_btn)
        
        self.preset_slow_btn = QPushButton("🐌 Slow & Clear")
        self.preset_slow_btn.clicked.connect(lambda: self.apply_preset("slow"))
        preset_layout.addWidget(self.preset_slow_btn)
        
        preset_layout.addStretch()
        chatterbox_manual_layout.addLayout(preset_layout)
        
        self.chatterbox_manual_widget.setLayout(chatterbox_manual_layout)
        self.chatterbox_manual_widget.setVisible(False)  # Hidden by default
        chatterbox_layout.addWidget(self.chatterbox_manual_widget)
        
        chatterbox_group.setLayout(chatterbox_layout)
        layout.addWidget(chatterbox_group)
        
        # Group 5: Generation Controls
        generation_group = QGroupBox("🎙️ Tạo Audio")
        generation_layout = QVBoxLayout()
        generation_layout.setSpacing(8)
        
        # TTS Provider - CHỈ CHATTERBOX
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("TTS Provider:"))
        
        provider_info = QLabel("🤖 Chatterbox TTS (AI Voice Cloning)")
        provider_info.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        provider_layout.addWidget(provider_info)
        
        provider_layout.addStretch()
        generation_layout.addLayout(provider_layout)
        
        # Output settings
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Thư mục output:"))
        
        self.voice_output_input = QLineEdit()
        self.voice_output_input.setPlaceholderText("./voice_studio_output/")
        self.voice_output_input.setReadOnly(True)
        output_layout.addWidget(self.voice_output_input)
        
        self.select_voice_output_btn = QPushButton("📁")
        self.select_voice_output_btn.clicked.connect(self.select_voice_output_folder)
        self.select_voice_output_btn.setMaximumWidth(40)
        output_layout.addWidget(self.select_voice_output_btn)
        
        generation_layout.addLayout(output_layout)
        
        # Generation buttons
        generation_buttons_layout = QHBoxLayout()
        
        self.generate_selected_btn = QPushButton("🎤 Tạo voice cho nhân vật đã chọn")
        self.generate_selected_btn.clicked.connect(self.generate_selected_character_voice)
        self.generate_selected_btn.setEnabled(False)
        generation_buttons_layout.addWidget(self.generate_selected_btn)
        
        self.generate_all_btn = QPushButton("🎭 Tạo voice cho tất cả nhân vật")
        self.generate_all_btn.clicked.connect(self.generate_all_voices)
        self.generate_all_btn.setEnabled(False)
        generation_buttons_layout.addWidget(self.generate_all_btn)
        
        generation_layout.addLayout(generation_buttons_layout)
        
        generation_group.setLayout(generation_layout)
        layout.addWidget(generation_group)
        
        # Group 6: Progress & Results
        progress_group = QGroupBox("📊 Tiến trình & Kết quả")
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        
        # Progress bar
        self.voice_progress_bar = QProgressBar()
        self.voice_progress_bar.setVisible(False)
        progress_layout.addWidget(self.voice_progress_bar)
        
        # Progress text
        self.voice_progress_text = QLabel("Sẵn sàng tạo voice")
        self.voice_progress_text.setStyleSheet("color: #666; font-style: italic;")
        progress_layout.addWidget(self.voice_progress_text)
        
        # Results area
        self.voice_results_text = QTextEdit()
        self.voice_results_text.setMaximumHeight(100)
        self.voice_results_text.setReadOnly(True)
        self.voice_results_text.setPlaceholderText("Kết quả tạo voice sẽ hiển thị ở đây...")
        progress_layout.addWidget(self.voice_results_text)
        
        # Action buttons
        action_buttons_layout = QHBoxLayout()
        
        self.open_voice_folder_btn = QPushButton("📁 Mở thư mục output")
        self.open_voice_folder_btn.clicked.connect(self.open_voice_output_folder)
        action_buttons_layout.addWidget(self.open_voice_folder_btn)
        
        self.clear_voice_results_btn = QPushButton("🧹 Xóa kết quả")
        self.clear_voice_results_btn.clicked.connect(self.clear_voice_results)
        action_buttons_layout.addWidget(self.clear_voice_results_btn)
        
        action_buttons_layout.addStretch()
        progress_layout.addLayout(action_buttons_layout)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Initialize data
        self.voice_studio_script_data = None
        self.voice_mapping = {}
        self.character_chatterbox_settings = {}  # Store per-character settings
        self.voice_clone_folder = None
        
        # Set content and add to scroll
        scroll.setWidget(content_widget)
        
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, "🎙️ Voice Studio")
    
    def create_projects_tab(self):
        """Tab quản lý projects với layout tối ưu cho MacOS"""
        tab = QWidget()
        
        # Sử dụng splitter để chia đôi màn hình
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel trái: Danh sách projects
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(8)
        
        # Header với nút refresh
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("📁 Danh sách dự án"))
        header_layout.addStretch()
        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Làm mới danh sách")
        refresh_btn.setMaximumWidth(40)
        refresh_btn.clicked.connect(self.refresh_projects)
        header_layout.addWidget(refresh_btn)
        left_layout.addLayout(header_layout)
        
        # Danh sách projects
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.load_project_details)
        left_layout.addWidget(self.projects_list)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Panel phải: Chi tiết project
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(8)
        
        # Header chi tiết
        right_layout.addWidget(QLabel("📋 Chi tiết dự án"))
        
        # Chi tiết project với scroll
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        details_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.project_details = QTextEdit()
        self.project_details.setReadOnly(True)
        details_scroll.setWidget(self.project_details)
        right_layout.addWidget(details_scroll)
        
        # Nút actions
        actions_group = QGroupBox("🛠️ Thao tác")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        self.open_folder_btn = QPushButton("📁 Mở thư mục")
        self.open_folder_btn.clicked.connect(self.open_project_folder)
        actions_layout.addWidget(self.open_folder_btn, 0, 0)
        
        self.delete_project_btn = QPushButton("🗑️ Xóa dự án")
        self.delete_project_btn.clicked.connect(self.delete_project)
        self.delete_project_btn.setProperty("class", "danger")
        actions_layout.addWidget(self.delete_project_btn, 0, 1)
        
        actions_group.setLayout(actions_layout)
        right_layout.addWidget(actions_group)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        
        # Thiết lập tỷ lệ splitter (40% - 60%)
        splitter.setSizes([400, 600])
        
        # Layout chính của tab
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(splitter)
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, "📁 Dự án")
        
        # Load projects khi khởi tạo
        self.refresh_projects()
    
    def create_settings_tab(self):
        """Tab cài đặt với layout tối ưu cho MacOS"""
        tab = QWidget()
        
        # Sử dụng scroll area cho settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        content_widget.setLayout(layout)
        
        # Group 1: API Keys cho AI Content
        ai_content_group = QGroupBox("📝 AI Sinh nội dung")
        ai_content_layout = QGridLayout()
        ai_content_layout.setSpacing(8)
        
        ai_content_layout.addWidget(QLabel("OpenAI API Key (GPT-4):"), 0, 0)
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setPlaceholderText("sk-...")
        ai_content_layout.addWidget(self.openai_key_input, 0, 1)
        
        ai_content_layout.addWidget(QLabel("Claude API Key:"), 1, 0)
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.Password)
        self.claude_key_input.setPlaceholderText("sk-ant-...")
        ai_content_layout.addWidget(self.claude_key_input, 1, 1)
        
        ai_content_layout.addWidget(QLabel("DeepSeek API Key:"), 2, 0)
        self.deepseek_key_input = QLineEdit()
        self.deepseek_key_input.setEchoMode(QLineEdit.Password)
        self.deepseek_key_input.setPlaceholderText("sk-...")
        ai_content_layout.addWidget(self.deepseek_key_input, 2, 1)
        
        ai_content_group.setLayout(ai_content_layout)
        layout.addWidget(ai_content_group)
        
        # Group 2: API Keys cho Image Generation
        image_gen_group = QGroupBox("🎨 AI Tạo ảnh")
        image_gen_layout = QGridLayout()
        image_gen_layout.setSpacing(8)
        
        # DALL-E info
        dalle_info = QLabel("DALL-E (OpenAI) - dùng chung key OpenAI")
        dalle_info.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        image_gen_layout.addWidget(dalle_info, 0, 0, 1, 2)
        
        image_gen_layout.addWidget(QLabel("Midjourney API Key:"), 1, 0)
        self.midjourney_key_input = QLineEdit()
        self.midjourney_key_input.setEchoMode(QLineEdit.Password)
        image_gen_layout.addWidget(self.midjourney_key_input, 1, 1)
        
        image_gen_layout.addWidget(QLabel("Stability AI Key:"), 2, 0)
        self.stability_key_input = QLineEdit()
        self.stability_key_input.setEchoMode(QLineEdit.Password)
        self.stability_key_input.setPlaceholderText("sk-...")
        image_gen_layout.addWidget(self.stability_key_input, 2, 1)
        
        image_gen_group.setLayout(image_gen_layout)
        layout.addWidget(image_gen_group)
        
        # Group 3: API Keys cho Text-to-Speech
        tts_group = QGroupBox("🎤 Text-to-Speech")
        tts_layout = QGridLayout()
        tts_layout.setSpacing(8)
        
        tts_layout.addWidget(QLabel("ElevenLabs API Key:"), 0, 0)
        self.elevenlabs_key_input = QLineEdit()
        self.elevenlabs_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_key_input.setPlaceholderText("sk_...")
        tts_layout.addWidget(self.elevenlabs_key_input, 0, 1)
        
        tts_layout.addWidget(QLabel("Google Cloud TTS Key:"), 1, 0)
        self.google_tts_key_input = QLineEdit()
        self.google_tts_key_input.setEchoMode(QLineEdit.Password)
        tts_layout.addWidget(self.google_tts_key_input, 1, 1)
        
        tts_layout.addWidget(QLabel("Azure Speech Key:"), 2, 0)
        self.azure_speech_key_input = QLineEdit()
        self.azure_speech_key_input.setEchoMode(QLineEdit.Password)
        tts_layout.addWidget(self.azure_speech_key_input, 2, 1)
        
        # Chatterbox TTS Device Info
        chatterbox_info = QLabel("🤖 Chatterbox TTS: Auto-detect CUDA/MPS/CPU")
        chatterbox_info.setStyleSheet("color: #007AFF; font-weight: bold; font-size: 12px;")
        tts_layout.addWidget(chatterbox_info, 3, 0, 1, 2)
        
        # Device status button
        self.chatterbox_device_btn = QPushButton("📱 Kiểm tra Device")
        self.chatterbox_device_btn.clicked.connect(self.show_chatterbox_device_info)
        tts_layout.addWidget(self.chatterbox_device_btn, 4, 0)
        
        # Clear cache button
        self.chatterbox_clear_btn = QPushButton("🧹 Xóa Cache")
        self.chatterbox_clear_btn.clicked.connect(self.clear_chatterbox_cache)
        tts_layout.addWidget(self.chatterbox_clear_btn, 4, 1)
        
        tts_group.setLayout(tts_layout)
        layout.addWidget(tts_group)
        
        # Group 4: Provider Selection
        providers_group = QGroupBox("⚙️ Chọn nhà cung cấp")
        providers_layout = QGridLayout()
        providers_layout.setSpacing(8)
        
        providers_layout.addWidget(QLabel("AI Sinh nội dung:"), 0, 0)
        self.content_provider_combo = QComboBox()
        self.content_provider_combo.addItems(self.api_manager.get_available_content_providers())
        providers_layout.addWidget(self.content_provider_combo, 0, 1)
        
        providers_layout.addWidget(QLabel("AI Tạo ảnh:"), 1, 0)
        self.image_provider_combo = QComboBox()
        self.image_provider_combo.addItems(self.api_manager.get_available_image_providers())
        providers_layout.addWidget(self.image_provider_combo, 1, 1)
        
        providers_layout.addWidget(QLabel("Text-to-Speech:"), 2, 0)
        self.tts_provider_combo = QComboBox()
        self.tts_provider_combo.addItems(self.api_manager.get_available_tts_providers())
        providers_layout.addWidget(self.tts_provider_combo, 2, 1)
        
        providers_group.setLayout(providers_layout)
        layout.addWidget(providers_group)
        
        # Group 5: Video Settings
        video_group = QGroupBox("🎬 Cài đặt Video")
        video_layout = QGridLayout()
        video_layout.setSpacing(8)
        
        video_layout.addWidget(QLabel("Độ phân giải:"), 0, 0)
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["1920x1080", "1280x720", "1080x1080"])
        video_layout.addWidget(self.resolution_combo, 0, 1)
        
        video_layout.addWidget(QLabel("FPS:"), 1, 0)
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setRange(15, 60)
        self.fps_spinbox.setValue(25)
        video_layout.addWidget(self.fps_spinbox, 1, 1)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # Group 6: Actions
        actions_group = QGroupBox("🛠️ Thao tác")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        save_settings_btn = QPushButton("💾 Lưu cài đặt")
        save_settings_btn.clicked.connect(self.save_settings)
        actions_layout.addWidget(save_settings_btn, 0, 0)
        
        check_api_btn = QPushButton("🔍 Kiểm tra API")
        check_api_btn.clicked.connect(self.check_api_status)
        actions_layout.addWidget(check_api_btn, 0, 1)
        
        refresh_providers_btn = QPushButton("🔄 Làm mới")
        refresh_providers_btn.clicked.connect(self.refresh_providers)
        actions_layout.addWidget(refresh_providers_btn, 1, 0, 1, 2)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Thêm stretch để đẩy nội dung lên trên
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        
        # Layout chính của tab
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, "⚙️ Cài đặt")
        
        # Load cài đặt hiện tại từ file config.env
        self.load_current_settings()
        
        # Update API status when settings change (safe call)
        self.update_api_status_indicator()
    
    def start_video_generation(self):
        """Bắt đầu tạo video"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập prompt!")
            return
        
        project_name = self.project_name_input.text().strip() or "video_project"
        
        # Lấy preset hiệu ứng
        preset_key = self.effects_preset_combo.currentData()
        if preset_key:
            effects = EffectsPresets.get_preset_by_name(preset_key)
        else:
            # Fallback to manual settings
            effects = {
                "zoom": self.zoom_checkbox.isChecked(),
                "transitions": {"crossfade": True} if self.transitions_checkbox.isChecked() else None
            }
        
        # Disable nút và hiện progress
        self.generate_video_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 8)
        
        # Kiểm tra chế độ ảnh thủ công
        use_custom_images = self.manual_images_radio.isChecked()
        custom_images_folder = getattr(self, 'selected_images_folder', None) if use_custom_images else None
        
        if use_custom_images and not custom_images_folder:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục chứa ảnh!")
            return
        
        # Lấy thông tin giọng đọc và thư mục
        voice_name = self.voice_combo.currentText().split(' ')[0]  # Lấy tên giọng (vd: vi-VN-Standard-A)
        project_folder = self.project_folder_input.text() or None
        
        # Tạo thread
        self.generation_thread = VideoGenerationThread(
            prompt, project_name, effects, use_custom_images, custom_images_folder,
            voice_name, project_folder
        )
        self.generation_thread.progress_updated.connect(self.update_progress)
        self.generation_thread.finished.connect(self.generation_finished)
        self.generation_thread.start()
    
    def update_progress(self, step, message):
        """Cập nhật progress"""
        self.progress_group.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(step)
        self.progress_label.setText(message)
    
    def generation_finished(self, result):
        """Hoàn thành tạo video"""
        self.generate_video_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result["success"]:
            self.progress_label.setText(f"Hoàn thành! Video: {result['final_video_path']}")
            QMessageBox.information(self, "Thành công", 
                                  f"Video đã được tạo thành công!\nProject: {result['project_id']}\nĐường dẫn: {result['final_video_path']}")
            self.refresh_projects()
        else:
            self.progress_label.setText(f"Lỗi: {result['error']}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo video:\n{result['error']}")
    
    def refresh_projects(self):
        """Làm mới danh sách projects"""
        self.projects_list.clear()
        result = self.pipeline.project_manager.list_projects()
        if result["success"]:
            for project in result["projects"]:
                item_text = f"{project['name']} ({project['status']}) - {project['created_at'][:10]}"
                self.projects_list.addItem(item_text)
                # Lưu project_id vào item
                item = self.projects_list.item(self.projects_list.count() - 1)
                item.setData(1, project['id'])
    
    def load_project_details(self, item):
        """Load chi tiết project"""
        project_id = item.data(1)
        self.current_project_id = project_id
        
        result = self.pipeline.project_manager.load_project(project_id)
        if result["success"]:
            data = result["data"]
            details = f"""
Project: {data['name']}
ID: {data['id']}
Prompt: {data['prompt']}
Status: {data['status']}
Segments: {len(data['segments'])}
Created: {data['created_at']}
            """
            self.project_details.setText(details.strip())
    
    def open_project_folder(self):
        """Mở thư mục project"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn project!")
            return
        
        project_path = self.pipeline.project_manager.get_project_path(self.current_project_id)
        os.system(f"open '{project_path}'" if sys.platform == "darwin" else f"explorer '{project_path}'")
    
    def delete_project(self):
        """Xóa project"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn project!")
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa project này?")
        if reply == QMessageBox.Yes:
            result = self.pipeline.project_manager.delete_project(self.current_project_id)
            if result["success"]:
                QMessageBox.information(self, "Thành công", "Đã xóa project!")
                self.refresh_projects()
                self.project_details.clear()
                self.current_project_id = None
            else:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa: {result['error']}")
    
    def save_settings(self):
        """Lưu cài đặt"""
        try:
            # Đọc file config.env hiện tại
            config_path = 'config.env'
            config_data = {}
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            config_data[key.strip()] = value.strip()
            
            # Cập nhật API keys từ UI
            if self.openai_key_input.text().strip():
                config_data['OPENAI_API_KEY'] = self.openai_key_input.text().strip()
            if self.claude_key_input.text().strip():
                config_data['CLAUDE_API_KEY'] = self.claude_key_input.text().strip()
            if self.deepseek_key_input.text().strip():
                config_data['DEEPSEEK_API_KEY'] = self.deepseek_key_input.text().strip()
            if self.midjourney_key_input.text().strip():
                config_data['MIDJOURNEY_API_KEY'] = self.midjourney_key_input.text().strip()
            if self.stability_key_input.text().strip():
                config_data['STABILITY_AI_KEY'] = self.stability_key_input.text().strip()
            if self.elevenlabs_key_input.text().strip():
                config_data['ELEVENLABS_API_KEY'] = self.elevenlabs_key_input.text().strip()
            if self.google_tts_key_input.text().strip():
                config_data['GOOGLE_TTS_API_KEY'] = self.google_tts_key_input.text().strip()
            if self.azure_speech_key_input.text().strip():
                config_data['AZURE_SPEECH_KEY'] = self.azure_speech_key_input.text().strip()
            
            # Cập nhật provider preferences
            config_data['CONTENT_PROVIDER'] = self.content_provider_combo.currentText()
            config_data['IMAGE_PROVIDER'] = self.image_provider_combo.currentText()
            config_data['TTS_PROVIDER'] = self.tts_provider_combo.currentText()
            
            # Cập nhật video settings
            config_data['VIDEO_RESOLUTION'] = self.resolution_combo.currentText()
            config_data['VIDEO_FPS'] = str(self.fps_spinbox.value())
            
            # Ghi lại file config.env
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write("# ===========================================\n")
                f.write("# API KEYS - Auto-generated from settings\n")
                f.write("# ===========================================\n\n")
                
                f.write("# AI Content Generation\n")
                f.write(f"OPENAI_API_KEY={config_data.get('OPENAI_API_KEY', '')}\n")
                f.write(f"CLAUDE_API_KEY={config_data.get('CLAUDE_API_KEY', '')}\n")
                f.write(f"DEEPSEEK_API_KEY={config_data.get('DEEPSEEK_API_KEY', '')}\n\n")
                
                f.write("# Image Generation\n")
                f.write(f"MIDJOURNEY_API_KEY={config_data.get('MIDJOURNEY_API_KEY', '')}\n")
                f.write(f"STABILITY_AI_KEY={config_data.get('STABILITY_AI_KEY', '')}\n\n")
                
                f.write("# Text-to-Speech\n")
                f.write(f"ELEVENLABS_API_KEY={config_data.get('ELEVENLABS_API_KEY', '')}\n")
                f.write(f"GOOGLE_TTS_API_KEY={config_data.get('GOOGLE_TTS_API_KEY', '')}\n")
                f.write(f"AZURE_SPEECH_KEY={config_data.get('AZURE_SPEECH_KEY', '')}\n")
                f.write(f"AZURE_SPEECH_REGION={config_data.get('AZURE_SPEECH_REGION', 'eastus')}\n\n")
                
                f.write("# ===========================================\n")
                f.write("# PROVIDER PREFERENCES\n")
                f.write("# ===========================================\n")
                f.write(f"CONTENT_PROVIDER={config_data.get('CONTENT_PROVIDER', 'OpenAI GPT-4')}\n")
                f.write(f"IMAGE_PROVIDER={config_data.get('IMAGE_PROVIDER', 'DALL-E (OpenAI)')}\n")
                f.write(f"TTS_PROVIDER={config_data.get('TTS_PROVIDER', 'Google TTS (Free)')}\n\n")
                
                f.write("# ===========================================\n")
                f.write("# SETTINGS\n")
                f.write("# ===========================================\n")
                f.write(f"DEFAULT_VOICE=alloy\n")
                f.write(f"DEFAULT_LANGUAGE=vi\n")
                f.write(f"VIDEO_RESOLUTION={config_data.get('VIDEO_RESOLUTION', '1920x1080')}\n")
                f.write(f"VIDEO_FPS={config_data.get('VIDEO_FPS', '25')}\n")
            
            # Reload API manager để áp dụng thay đổi
            self.api_manager = APIManager()
            self.refresh_providers()
            
            QMessageBox.information(self, "Thành công", "Cài đặt đã được lưu thành công!\nAPI keys đã được cập nhật vào config.env")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu cài đặt:\n{str(e)}")
    
    def load_current_settings(self):
        """Load cài đặt hiện tại từ file config.env"""
        try:
            config_path = 'config.env'
            if not os.path.exists(config_path):
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Load API keys
                        if key == 'OPENAI_API_KEY' and value and value != 'your_openai_api_key_here':
                            self.openai_key_input.setText(value)
                        elif key == 'CLAUDE_API_KEY' and value and value != 'your_claude_api_key_here':
                            self.claude_key_input.setText(value)
                        elif key == 'DEEPSEEK_API_KEY' and value and value != 'your_deepseek_api_key_here':
                            self.deepseek_key_input.setText(value)
                        elif key == 'MIDJOURNEY_API_KEY' and value and value != 'your_midjourney_api_key_here':
                            self.midjourney_key_input.setText(value)
                        elif key == 'STABILITY_AI_KEY' and value and value != 'your_stability_ai_key_here':
                            self.stability_key_input.setText(value)
                        elif key == 'ELEVENLABS_API_KEY' and value and value != 'your_elevenlabs_api_key_here':
                            self.elevenlabs_key_input.setText(value)
                        elif key == 'GOOGLE_TTS_API_KEY' and value and value != 'your_google_tts_api_key_here':
                            self.google_tts_key_input.setText(value)
                        elif key == 'AZURE_SPEECH_KEY' and value and value != 'your_azure_speech_key_here':
                            self.azure_speech_key_input.setText(value)
                        
                        # Load provider preferences
                        elif key == 'CONTENT_PROVIDER' and value:
                            index = self.content_provider_combo.findText(value)
                            if index >= 0:
                                self.content_provider_combo.setCurrentIndex(index)
                        elif key == 'IMAGE_PROVIDER' and value:
                            index = self.image_provider_combo.findText(value)
                            if index >= 0:
                                self.image_provider_combo.setCurrentIndex(index)
                        elif key == 'TTS_PROVIDER' and value:
                            index = self.tts_provider_combo.findText(value)
                            if index >= 0:
                                self.tts_provider_combo.setCurrentIndex(index)
                        
                        # Load video settings
                        elif key == 'VIDEO_RESOLUTION' and value:
                            index = self.resolution_combo.findText(value)
                            if index >= 0:
                                self.resolution_combo.setCurrentIndex(index)
                        elif key == 'VIDEO_FPS' and value:
                            try:
                                fps = int(value)
                                self.fps_spinbox.setValue(fps)
                            except ValueError:
                                pass
        except Exception as e:
            print(f"Lỗi load cài đặt: {str(e)}")
    
    def load_prompt_suggestions(self):
        """Load prompt suggestions theo danh mục"""
        self.prompt_suggestions_list.clear()
        self.prompt_suggestions_list.addItem("-- Chọn prompt mẫu --")
        
        current_data = self.category_combo.currentData()
        if current_data:
            categories = PromptTemplates.get_all_categories()
            if current_data in categories:
                prompts = categories[current_data]["prompts"]
                for prompt in prompts:
                    # Truncate long prompts for display
                    display_text = prompt[:80] + "..." if len(prompt) > 80 else prompt
                    self.prompt_suggestions_list.addItem(display_text, prompt)
    
    def use_suggested_prompt(self):
        """Sử dụng prompt được gợi ý"""
        current_data = self.prompt_suggestions_list.currentData()
        if current_data:
            self.prompt_input.setPlainText(current_data)
    
    def get_random_prompt(self):
        """Lấy prompt ngẫu nhiên"""
        random_prompt = PromptTemplates.get_random_prompt()
        self.prompt_input.setPlainText(random_prompt)
    
    def toggle_image_mode(self):
        """Chuyển đổi chế độ tạo ảnh"""
        manual_mode = self.manual_images_radio.isChecked()
        self.select_images_btn.setEnabled(manual_mode)
        
        if manual_mode:
            self.auto_generate_radio.setChecked(False)
        else:
            self.auto_generate_radio.setChecked(True)
    
    def select_images_folder(self):
        """Chọn thư mục chứa ảnh"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Chọn thư mục chứa ảnh", ""
        )
        
        if folder_path:
            # Kiểm tra ảnh trong thư mục
            image_files = self.get_image_files_in_folder(folder_path)
            
            if image_files:
                self.selected_images_folder = folder_path
                self.selected_images_label.setText(
                    f"Đã chọn: {folder_path} ({len(image_files)} ảnh)"
                )
                self.selected_images_label.setStyleSheet("color: green;")
            else:
                QMessageBox.warning(
                    self, "Cảnh báo", 
                    "Thư mục không chứa ảnh hợp lệ!\nHỗ trợ: .jpg, .jpeg, .png, .bmp, .gif, .webp"
                )
    
    def get_image_files_in_folder(self, folder_path):
        """Lấy danh sách file ảnh trong thư mục"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        image_files = []
        
        try:
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in valid_extensions):
                    image_files.append(os.path.join(folder_path, file))
        except Exception:
            pass
        
        return sorted(image_files)
    
    def check_api_status(self):
        """Kiểm tra trạng thái tất cả API"""
        status = self.api_manager.get_provider_status()
        
        status_text = "🔍 TRẠNG THÁI API:\n\n"
        
        # Content providers
        status_text += "📝 AI Sinh nội dung:\n"
        for provider, available in status['content_providers'].items():
            icon = "✅" if available else "❌"
            status_text += f"  {icon} {provider}\n"
        
        # Image providers
        status_text += "\n🎨 AI Tạo ảnh:\n"
        for provider, available in status['image_providers'].items():
            icon = "✅" if available else "❌"
            status_text += f"  {icon} {provider}\n"
        
        # TTS providers
        status_text += "\n🎤 Text-to-Speech:\n"
        for provider, available in status['tts_providers'].items():
            icon = "✅" if available else "❌"
            status_text += f"  {icon} {provider}\n"
        
        QMessageBox.information(self, "Trạng thái API", status_text)
    
    def refresh_providers(self):
        """Làm mới danh sách providers"""
        # Reload API manager
        self.api_manager = APIManager()
        
        # Update combo boxes
        self.content_provider_combo.clear()
        self.content_provider_combo.addItems(self.api_manager.get_available_content_providers())
        
        self.image_provider_combo.clear()
        self.image_provider_combo.addItems(self.api_manager.get_available_image_providers())
        
        self.tts_provider_combo.clear()
        self.tts_provider_combo.addItems(self.api_manager.get_available_tts_providers())
        
        QMessageBox.information(self, "Thông báo", "Đã làm mới danh sách providers!")
        
        # Update API status indicator
        self.update_api_status_indicator()
    
    def generate_story_only(self):
        """Chỉ tạo câu chuyện/kịch bản từ prompt"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập prompt!")
            return
        
        # Disable nút để tránh spam
        self.generate_story_btn.setEnabled(False)
        self.progress_group.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Đang tạo câu chuyện...")
        
        try:
            # Lấy provider được chọn
            content_provider = self.content_provider_combo.currentText()
            
            # Tạo câu chuyện
            result = self.pipeline.content_gen.generate_script_from_prompt(prompt, provider=content_provider)
            
            if "error" in result:
                QMessageBox.critical(self, "Lỗi", f"Không thể tạo câu chuyện:\n{result['error']}")
                self.progress_label.setText("Lỗi tạo câu chuyện")
            else:
                # Store script data for audio generation
                self.current_script_data = result
                
                # Hiển thị kết quả với format mới
                story_text = "🎬 CÂU CHUYỆN ĐÃ TẠO:\n\n"
                
                # Show characters if available
                characters = result.get("characters", [])
                if characters:
                    story_text += "🎭 NHÂN VẬT:\n"
                    for char in characters:
                        story_text += f"• {char.get('name', char['id'])} ({char.get('gender', 'neutral')}) - {char.get('suggested_voice', 'N/A')}\n"
                    story_text += "\n"
                
                for i, segment in enumerate(result["segments"], 1):
                    story_text += f"📝 ĐOẠN {i} ({segment.get('duration', 10)}s):\n"
                    story_text += f"Kịch bản: {segment.get('script', '')}\n"
                    
                    # Show dialogues if available
                    dialogues = segment.get('dialogues', [])
                    if dialogues:
                        story_text += "Dialogues:\n"
                        for dialogue in dialogues:
                            speaker = dialogue.get('speaker', 'unknown')
                            text = dialogue.get('text', '')
                            emotion = dialogue.get('emotion', 'neutral')
                            story_text += f"  - {speaker} ({emotion}): {text}\n"
                    else:
                        # Fallback for old format
                        story_text += f"Lời thoại: {segment.get('narration', '')}\n"
                    
                    story_text += f"Mô tả ảnh: {segment.get('image_prompt', '')}\n"
                    story_text += "-" * 50 + "\n\n"
                
                # Enable audio generation button
                self.generate_audio_btn.setEnabled(True)
                
                # Tạo dialog hiển thị
                dialog = QDialog(self)
                dialog.setWindowTitle(f"Câu chuyện từ prompt - {content_provider}")
                dialog.setModal(True)
                dialog.resize(800, 600)
                
                layout = QVBoxLayout()
                dialog.setLayout(layout)
                
                # Text area hiển thị story
                story_display = QTextEdit()
                story_display.setPlainText(story_text)
                story_display.setReadOnly(True)
                layout.addWidget(story_display)
                
                # Nút actions
                buttons_layout = QHBoxLayout()
                
                copy_btn = QPushButton("📋 Copy")
                copy_btn.clicked.connect(lambda: self.copy_to_clipboard(story_text))
                buttons_layout.addWidget(copy_btn)
                
                save_btn = QPushButton("💾 Lưu vào file")
                save_btn.clicked.connect(lambda: self.save_story_to_file(story_text, prompt))
                buttons_layout.addWidget(save_btn)
                
                close_btn = QPushButton("❌ Đóng")
                close_btn.clicked.connect(dialog.close)
                buttons_layout.addWidget(close_btn)
                
                layout.addLayout(buttons_layout)
                
                dialog.exec_()
                self.progress_label.setText("Đã tạo câu chuyện thành công!")
                
                # Hiển thị preview ngay trong ứng dụng
                preview_text = ""
                for i, segment in enumerate(result["segments"], 1):
                    # Handle both old and new format
                    narration = segment.get('narration', '')
                    if not narration and 'dialogues' in segment:
                        # New format with dialogues
                        narration = " ".join([d.get('text', '') for d in segment['dialogues']])
                    preview_text += f"ĐOẠN {i}: {narration}\n"
                self.content_preview.setPlainText(preview_text)
                
                # Show progress group
                self.progress_group.setVisible(True)
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định:\n{str(e)}")
            self.progress_label.setText("Lỗi tạo câu chuyện")
        finally:
            self.generate_story_btn.setEnabled(True)
    
    def copy_to_clipboard(self, text):
        """Copy text vào clipboard"""
        try:
            from PySide6.QtGui import QClipboard, QGuiApplication
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Thành công", "Đã copy vào clipboard!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể copy: {str(e)}")
    
    def save_story_to_file(self, story_text, prompt):
        """Lưu câu chuyện vào file"""
        try:
            from PySide6.QtWidgets import QFileDialog
            from datetime import datetime
            
            # Tạo tên file mặc định
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"story_{timestamp}.txt"
            
            # Mở dialog lưu file
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu câu chuyện", default_filename, 
                "Text Files (*.txt);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"PROMPT GỐC:\n{prompt}\n\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(story_text)
                    
                QMessageBox.information(self, "Thành công", f"Đã lưu câu chuyện vào:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu file:\n{str(e)}")
    
    def select_project_folder(self):
        """Chọn thư mục để lưu dự án"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Chọn thư mục lưu dự án", "./projects"
        )
        
        if folder_path:
            self.project_folder_input.setText(folder_path)
            self.progress_label.setText(f"Đã chọn thư mục: {folder_path}")
    
    def generate_audio_only(self):
        """Tạo audio từ script data có sẵn với Enhanced Voice Setup"""
        if not self.current_script_data:
            QMessageBox.warning(self, "Cảnh báo", 
                "Chưa có script data! Hãy tạo story trước.")
            return
        
        # Import Enhanced Voice Setup Dialog
        from ui.manual_voice_setup_dialog import ManualVoiceSetupDialog
        from tts.voice_generator import VoiceGenerator
        
        # Initialize voice generator
        voice_gen = VoiceGenerator()
        
        # Create Enhanced dialog
        dialog = ManualVoiceSetupDialog(voice_gen, self)
        
        # Pre-populate dialog với characters từ script data
        dialog.populate_from_script_characters(self.current_script_data)
        
        # Show dialog and get configuration
        if dialog.exec_() == QDialog.Accepted:
            characters, voice_mapping = dialog.get_characters_and_mapping()
            
            # Update current script with new character configs
            self.current_script_data["characters"] = characters
            
            # Generate audio với Enhanced voice mapping
            self.generate_audio_with_mapping(voice_mapping)
    
    def open_audio_folder(self):
        """Mở thư mục chứa audio đã tạo"""
        if self.last_audio_output_dir and os.path.exists(self.last_audio_output_dir):
            # Cross-platform folder opening
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', self.last_audio_output_dir])
            elif platform.system() == "Windows":
                subprocess.Popen(['explorer', self.last_audio_output_dir])
            else:  # Linux
                subprocess.Popen(['xdg-open', self.last_audio_output_dir])
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy thư mục audio!")
    
    def play_final_audio(self):
        """Phát audio hoàn chỉnh"""
        if self.last_final_audio_path and os.path.exists(self.last_final_audio_path):
            # Cross-platform audio playing
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', self.last_final_audio_path])
            elif platform.system() == "Windows":
                os.system(f'start "" "{self.last_final_audio_path}"')
            else:  # Linux
                subprocess.Popen(['xdg-open', self.last_final_audio_path])
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy file audio!")
    
    def show_manual_voice_setup(self):
        """Hiển thị dialog cấu hình giọng đọc thủ công"""
        from tts.voice_generator import VoiceGenerator
        voice_gen = VoiceGenerator()
        
        dialog = ManualVoiceSetupDialog(voice_gen, self)
        if dialog.exec_() == QDialog.Accepted:
            characters, voice_mapping = dialog.get_characters_and_mapping()
            
            # Create manual script data
            manual_script_data = {
                "segments": [
                    {
                        "id": 1,
                        "script": "Audio được tạo từ cấu hình thủ công",
                        "image_prompt": "Hình ảnh minh họa",
                        "dialogues": [
                            {
                                "speaker": char['id'],
                                "text": f"Xin chào, tôi là {char['name']}. Đây là giọng nói {char['suggested_voice']} của tôi.",
                                "emotion": "friendly"
                            }
                            for char in characters
                        ],
                        "duration": 10
                    }
                ],
                "characters": characters
            }
            
            # Generate audio immediately
            self.current_script_data = manual_script_data
            self.generate_audio_with_mapping(voice_mapping)
    
    def generate_audio_with_mapping(self, voice_mapping):
        """Tạo audio với voice mapping đã có"""
        if not self.current_script_data:
            return
        
        # Import voice generator
        from tts.voice_generator import VoiceGenerator
        voice_gen = VoiceGenerator()
        
        # Disable button during generation
        self.generate_audio_btn.setEnabled(False)
        self.generate_audio_btn.setText("⏳ Đang tạo...")
        self.progress_label.setText("Đang tạo audio...")
        
        try:
            # Get project folder
            project_folder = self.project_folder_input.text() or "./projects"
            project_name = self.project_name_input.text() or "manual_audio_project"
            
            # Create audio output directory
            audio_output_dir = os.path.join(project_folder, project_name, "audio")
            os.makedirs(audio_output_dir, exist_ok=True)
            
            # Generate audio by characters
            result = voice_gen.generate_audio_by_characters(
                self.current_script_data, 
                audio_output_dir, 
                voice_mapping
            )
            
            if result["success"]:
                # Store paths for buttons
                self.last_audio_output_dir = result["output_dir"]
                self.last_final_audio_path = result["final_audio_path"]
                
                # Enable audio control buttons
                self.open_audio_folder_btn.setEnabled(True)
                self.play_final_audio_btn.setEnabled(True)
                
                # Show success message
                message = f"✅ Đã tạo audio thành công!\n\n"
                message += f"📁 Thư mục: {result['output_dir']}\n"
                message += f"🎵 File cuối: {os.path.basename(result['final_audio_path'])}\n\n"
                message += f"📊 Chi tiết:\n"
                for character, files in result["character_audio_files"].items():
                    message += f"  • {character}: {len(files)} file(s)\n"
                
                QMessageBox.information(self, "Thành công", message)
                self.progress_label.setText("Đã tạo audio thành công!")
                
            else:
                QMessageBox.critical(self, "Lỗi", f"Lỗi tạo audio:\n{result.get('error', 'Unknown error')}")
                self.progress_label.setText("Lỗi tạo audio")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định:\n{str(e)}")
            self.progress_label.setText("Lỗi tạo audio")
        finally:
            self.generate_audio_btn.setEnabled(True)
            self.generate_audio_btn.setText("🎵 Tạo Audio")
    
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
    
    # ===== VOICE STUDIO TAB METHODS =====
    
    def switch_data_source(self):
        """Chuyển đổi nguồn dữ liệu trong Voice Studio"""
        source = self.data_source_combo.currentData()
        
        # Hide all widgets first
        self.file_import_widget.setVisible(False)
        self.generated_data_widget.setVisible(False)
        self.manual_input_widget.setVisible(False)
        
        # Show appropriate widget
        if source == "file":
            self.file_import_widget.setVisible(True)
        elif source == "generated":
            self.generated_data_widget.setVisible(True)
        elif source == "manual":
            self.manual_input_widget.setVisible(True)
    
    def import_script_file(self):
        """Import script từ file JSON"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file JSON script",
            "",
            "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    script_data = json.load(f)
                
                # Validate script data
                if self.validate_script_data(script_data):
                    self.voice_studio_script_data = script_data
                    self.imported_file_label.setText(os.path.basename(file_path))
                    self.imported_file_label.setStyleSheet("color: #007AFF; font-weight: bold;")
                    self.update_voice_studio_overview()
                    QMessageBox.information(self, "Thành công", "Đã import script thành công!")
                else:
                    QMessageBox.warning(self, "Lỗi", "File JSON không đúng format!")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc file:\n{str(e)}")
    
    def load_generated_script_data(self):
        """Load script data từ tab Tạo Video"""
        if self.current_script_data:
            self.voice_studio_script_data = self.current_script_data
            self.update_voice_studio_overview()
            QMessageBox.information(self, "Thành công", "Đã load script data từ tab Tạo Video!")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Chưa có script data nào được tạo trong tab Tạo Video!")
    
    def parse_manual_script(self):
        """Parse JSON script được nhập thủ công"""
        try:
            script_text = self.manual_script_input.toPlainText().strip()
            if not script_text:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập JSON script!")
                return
            
            script_data = json.loads(script_text)
            
            if self.validate_script_data(script_data):
                self.voice_studio_script_data = script_data
                self.update_voice_studio_overview()
                QMessageBox.information(self, "Thành công", "Đã parse JSON script thành công!")
            else:
                QMessageBox.warning(self, "Lỗi", "JSON script không đúng format!")
                
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Lỗi JSON", f"JSON không hợp lệ:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể parse script:\n{str(e)}")
    
    def validate_script_data(self, script_data):
        """Validate format của script data"""
        try:
            # Check required fields
            if not isinstance(script_data, dict):
                return False
            
            if 'segments' not in script_data or 'characters' not in script_data:
                return False
            
            # Check segments
            segments = script_data['segments']
            if not isinstance(segments, list) or len(segments) == 0:
                return False
            
            # Check characters
            characters = script_data['characters']
            if not isinstance(characters, list) or len(characters) == 0:
                return False
            
            # Basic structure validation
            for segment in segments:
                if not all(key in segment for key in ['id', 'dialogues']):
                    return False
                
                for dialogue in segment['dialogues']:
                    if not all(key in dialogue for key in ['speaker', 'text']):
                        return False
            
            for character in characters:
                if not all(key in character for key in ['id', 'name']):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def update_voice_studio_overview(self):
        """Cập nhật overview của script trong Voice Studio"""
        if not self.voice_studio_script_data:
            return
        
        try:
            segments = self.voice_studio_script_data['segments']
            characters = self.voice_studio_script_data['characters']
            
            # Update info labels
            total_dialogues = sum(len(segment['dialogues']) for segment in segments)
            self.script_info_label.setText(
                f"✅ Script loaded: {len(segments)} segments, {total_dialogues} dialogues"
            )
            self.script_info_label.setStyleSheet("color: #007AFF; font-weight: bold;")
            
            # Update characters
            character_names = [char['name'] for char in characters]
            self.characters_label.setText(", ".join(character_names))
            
            # Update segments count
            self.segments_count_label.setText(str(len(segments)))
            
            # Update voice mapping table
            self.populate_voice_mapping_table()
            
            # Enable generation buttons
            self.generate_selected_btn.setEnabled(True)
            self.generate_all_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật overview:\n{str(e)}")
    
    def populate_voice_mapping_table(self):
        """Populate character settings table - FIXED METHOD"""
        if not self.voice_studio_script_data:
            return
        
        # Call the correct method for character settings table
        self.populate_character_settings_table()
        
        # Enable generation buttons
        self.generate_selected_btn.setEnabled(True)
        self.generate_all_btn.setEnabled(True)
        
        print("✅ Character settings table populated successfully")
        return

    
    def reset_voice_mapping(self):
        """Reset voice mapping về mặc định"""
        if not self.voice_studio_script_data:
            return
        
        # Reset table
        self.populate_character_settings_table()
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Thông báo", "Đã reset voice mapping về mặc định!")
    
    def preview_selected_voice(self):
        """Preview giọng nói của nhân vật được chọn - CHỈ CHATTERBOX TTS"""
        current_row = self.character_settings_table.currentRow()
        if current_row < 0:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân vật!")
            return
        
        try:
            # Get character info
            character_id = self.character_settings_table.item(current_row, 0).text()
            voice_combo = self.character_settings_table.cellWidget(current_row, 4)  # Voice column
            selected_voice = voice_combo.currentData()  # Get Chatterbox voice ID
            
            # Get settings from character_settings_table
            emotion_input = self.character_settings_table.cellWidget(current_row, 1)
            speed_input = self.character_settings_table.cellWidget(current_row, 2)
            cfg_weight_input = self.character_settings_table.cellWidget(current_row, 3)
            
            emotion = float(emotion_input.text()) if emotion_input else 1.0
            speed = float(speed_input.text()) if speed_input else 1.0
            cfg_weight = float(cfg_weight_input.text()) if cfg_weight_input else 0.5
            
            # Preview text
            preview_text = f"Xin chào, tôi là {character_id}. Đây là giọng nói {voice_combo.currentText().split(' ')[1]} của tôi với emotion {emotion:.1f}, speed {speed:.1f}x."
            
            # Generate preview audio
            import tempfile
            temp_dir = tempfile.mkdtemp()
            preview_path = os.path.join(temp_dir, f"preview_{character_id}.mp3")
            
            # Check if prompt-based voice is enabled for preview
            voice_prompt = None
            if self.enable_prompt_voice.isChecked() and self.voice_prompt_input.text().strip():
                voice_prompt = self.voice_prompt_input.text().strip()
                print(f"🎧 Preview with PROMPT: '{voice_prompt}'")
                preview_text = f"Xin chào, tôi là {character_id}. Đây là giọng được tạo từ prompt: {voice_prompt[:50]}..."
            else:
                print(f"🎧 Preview Settings for {character_id}:")
                print(f"   Voice: {selected_voice}")
                print(f"   Emotion: {emotion:.1f}")
                print(f"   Speed: {speed:.1f}x")
                print(f"   CFG Weight: {cfg_weight:.2f}")
                
            result = self.voice_generator.generate_voice_chatterbox(
                text=preview_text,
                save_path=preview_path,
                voice_sample_path=None,
                emotion_exaggeration=emotion,
                speed=speed,
                voice_name=selected_voice if not voice_prompt else None,  # Skip voice_name if using prompt
                cfg_weight=cfg_weight,
                voice_prompt=voice_prompt  # NEW: Pass voice prompt for preview
            )
            
            if result.get('success'):
                # Play preview
                self.play_audio_file(preview_path)
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "🎧 Preview Voice", 
                    f"Character: {character_id}\n"
                    f"Voice: {voice_combo.currentText()}\n"
                    f"Emotion: {emotion:.1f}\n"
                    f"Speed: {speed:.1f}x\n"
                    f"CFG Weight: {cfg_weight:.2f}\n"
                    f"\n🤖 Generated by Chatterbox TTS")
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "❌ Lỗi Preview", f"Không thể tạo preview Chatterbox TTS:\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "❌ Lỗi Critical", f"Lỗi preview voice:\n{str(e)}")
    
    def play_audio_file(self, file_path):
        """Play audio file"""
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', file_path])
            elif platform.system() == "Windows":
                os.startfile(file_path)
            else:  # Linux
                subprocess.Popen(['xdg-open', file_path])
        except Exception as e:
            print(f"Không thể play audio: {e}")
    
    def select_voice_output_folder(self):
        """Chọn thư mục output cho voice"""
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục output")
        if folder:
            self.voice_output_input.setText(folder)
    
    def generate_selected_character_voice(self):
        """Tạo voice cho nhân vật được chọn"""
        current_row = self.character_settings_table.currentRow()
        if current_row < 0:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân vật!")
            return
        
        # Get character ID
        character_id = self.character_settings_table.item(current_row, 0).text()
        
        # Generate for single character
        self.generate_voices_for_characters([character_id])
    
    def generate_all_voices(self):
        """Tạo voice cho tất cả nhân vật"""
        if not self.voice_studio_script_data:
            return
        
        # Get all character IDs
        character_ids = [char['id'] for char in self.voice_studio_script_data['characters']]
        
        # Generate for all characters
        self.generate_voices_for_characters(character_ids)
    
    def generate_voices_for_characters(self, character_ids):
        """Tạo voice cho danh sách character IDs"""
        try:
            # Show progress
            self.voice_progress_bar.setVisible(True)
            self.voice_progress_bar.setRange(0, 0)  # Indeterminate progress
            self.voice_progress_text.setText("Đang tạo voice...")
            
            # Get output directory
            output_dir = self.voice_output_input.text() or "./voice_studio_output"
            os.makedirs(output_dir, exist_ok=True)
            
            # CHỈ SỬ DỤNG CHATTERBOX TTS
            # provider = "chatterbox"  # Fixed provider
            
            # Collect voice mapping from character_settings_table
            current_voice_mapping = {}
            for i in range(self.character_settings_table.rowCount()):
                char_id = self.character_settings_table.item(i, 0).text()
                voice_combo = self.character_settings_table.cellWidget(i, 4)  # Voice column
                emotion_input = self.character_settings_table.cellWidget(i, 1)
                speed_input = self.character_settings_table.cellWidget(i, 2)
                cfg_weight_input = self.character_settings_table.cellWidget(i, 3)
                
                current_voice_mapping[char_id] = {
                    'name': char_id,
                    'suggested_voice': voice_combo.currentData() if voice_combo else 'female_young',
                    'emotion': float(emotion_input.text()) if emotion_input and emotion_input.text() else 1.0,
                    'speed': float(speed_input.text()) if speed_input and speed_input.text() else 1.0,
                    'cfg_weight': float(cfg_weight_input.text()) if cfg_weight_input and cfg_weight_input.text() else 0.5
                }
            
            # Generate audio
            total_generated = 0
            total_failed = 0
            results_text = ""
            
            for segment in self.voice_studio_script_data['segments']:
                for dialogue in segment['dialogues']:
                    speaker = dialogue['speaker']
                    
                    # Skip if not in selected characters
                    if speaker not in character_ids:
                        continue
                    
                    text = dialogue['text']
                    emotion = dialogue.get('emotion', 'neutral')
                    
                    # Get voice settings from character_settings_table
                    voice_settings = current_voice_mapping.get(speaker, {})
                    voice_name = voice_settings.get('suggested_voice', 'female_young')
                    emotion_exaggeration = voice_settings.get('emotion', 1.0)
                    speed = voice_settings.get('speed', 1.0)
                    cfg_weight = voice_settings.get('cfg_weight', 0.5)
                    
                    # Get per-character settings từ character_chatterbox_settings
                    char_settings = self.character_chatterbox_settings.get(speaker, {})
                    voice_prompt = char_settings.get('voice_prompt', '').strip()
                    voice_clone_path = char_settings.get('voice_clone_path', None)
                    
                    # Generate filename
                    segment_id = segment['id']
                    dialogue_idx = segment['dialogues'].index(dialogue) + 1
                    filename = f"segment_{segment_id}_dialogue_{dialogue_idx}_{speaker}.mp3"
                    file_path = os.path.join(output_dir, filename)
                    
                    # Generate voice - CHỈ SỬ DỤNG CHATTERBOX TTS với per-character settings
                    try:
                        # Apply emotion mapping if enabled
                        if self.enable_emotion_mapping.isChecked():
                            mapped_emotion, mapped_cfg = self.map_emotion_to_parameters(emotion, emotion_exaggeration)
                            emotion_exaggeration = mapped_emotion
                            cfg_weight = mapped_cfg
                        
                        # Validate voice settings và log generation info
                        voice_mode = self.validate_character_voice_settings(speaker)
                        
                        # CHỈ SỬ DỤNG CHATTERBOX TTS với optimized parameter passing
                        result = self.voice_generator.generate_voice_chatterbox(
                            text=text,
                            save_path=file_path,
                            voice_sample_path=voice_clone_path if voice_mode == 'clone' else None,
                            emotion_exaggeration=emotion_exaggeration,
                            speed=speed,
                            voice_name=voice_name if voice_mode == 'selection' else None,
                            cfg_weight=cfg_weight,
                            voice_prompt=voice_prompt if voice_mode == 'prompt' else None
                        )
                        
                        if result.get('success'):
                            total_generated += 1
                            results_text += f"✅ {filename}\n"
                        else:
                            total_failed += 1
                            results_text += f"❌ {filename}: {result.get('error', 'Unknown error')}\n"
                            
                    except Exception as e:
                        total_failed += 1
                        results_text += f"❌ {filename}: {str(e)}\n"
            
            # Update results
            self.voice_results_text.setText(results_text)
            
            # Show summary
            summary = f"🎯 Hoàn thành!\n\n"
            summary += f"✅ Thành công: {total_generated} files\n"
            summary += f"❌ Thất bại: {total_failed} files\n"
            summary += f"📁 Output: {output_dir}"
            
            QMessageBox.information(self, "Kết quả", summary)
            
            # Update progress
            self.voice_progress_text.setText(f"Hoàn thành: {total_generated} thành công, {total_failed} thất bại")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tạo voice:\n{str(e)}")
            self.voice_progress_text.setText("Lỗi tạo voice")
        finally:
            self.voice_progress_bar.setVisible(False)
    
    def open_voice_output_folder(self):
        """Mở thư mục output voice"""
        output_dir = self.voice_output_input.text() or "./voice_studio_output"
        
        if os.path.exists(output_dir):
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', output_dir])
            elif platform.system() == "Windows":
                os.startfile(output_dir)
            else:  # Linux
                subprocess.Popen(['xdg-open', output_dir])
        else:
            QMessageBox.warning(self, "Cảnh báo", f"Thư mục không tồn tại: {output_dir}")
    
    def clear_voice_results(self):
        """Xóa kết quả voice generation"""
        self.voice_results_text.clear()
        self.voice_progress_text.setText("Sẵn sàng tạo voice")
        QMessageBox.information(self, "Thông báo", "Đã xóa kết quả!")
    
    # ========== CHATTERBOX MANUAL CONTROLS ==========
    
    def toggle_chatterbox_manual_controls(self, enabled):
        """Toggle hiển thị manual controls cho Chatterbox"""
        self.chatterbox_manual_widget.setVisible(enabled)
        if enabled:
            self.populate_character_settings_table()
    
    def update_emotion_label(self, value):
        """Cập nhật label emotion từ slider"""
        emotion_value = value / 100.0  # Convert 0-300 to 0.0-3.0
        self.emotion_label.setText(f"{emotion_value:.1f}")
    
    def update_speed_label(self, value):
        """Cập nhật label speed từ slider"""
        speed_value = value / 100.0  # Convert 50-200 to 0.5-2.0
        self.speed_label.setText(f"{speed_value:.1f}x")
    
    def populate_character_settings_table(self):
        """Populate bảng settings cho từng nhân vật với CFG Weight và Voice selection"""
        if not self.voice_studio_script_data:
            return
        
        characters = self.voice_studio_script_data['characters']
        # Thêm 2 cột mới cho Voice Prompt và Voice Clone
        self.character_settings_table.setRowCount(len(characters))
        
        for i, character in enumerate(characters):
            char_id = character['id']
            
            # Character name
            name_item = QTableWidgetItem(character['name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.character_settings_table.setItem(i, 0, name_item)
            
            # Emotion input field (thay vì slider) - Fix màu đen
            emotion_input = QLineEdit()
            emotion_input.setText("1.0")
            emotion_input.setAlignment(Qt.AlignCenter)
            emotion_input.setMaximumWidth(60)
            emotion_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            emotion_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_emotion_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 1, emotion_input)
            
            # Speed input field (thay vì slider) - Fix màu đen
            speed_input = QLineEdit()
            speed_input.setText("1.0")
            speed_input.setAlignment(Qt.AlignCenter)
            speed_input.setMaximumWidth(60)
            speed_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            speed_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_speed_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 2, speed_input)
            
            # CFG Weight input field (NEW) - Fix màu đen
            cfg_weight_input = QLineEdit()
            cfg_weight_input.setText("0.5")
            cfg_weight_input.setAlignment(Qt.AlignCenter)
            cfg_weight_input.setMaximumWidth(60)
            cfg_weight_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            cfg_weight_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_cfg_weight_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 3, cfg_weight_input)
            
            # Voice selection combo (NEW) - Fix dropdown đen
            voice_combo = QComboBox()
            voice_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                }
                QComboBox::drop-down {
                    background-color: white;
                }
                QComboBox::down-arrow {
                    color: black;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    color: black;
                    selection-background-color: #007AFF;
                    selection-color: white;
                }
            """)
            
            # Always use fallback voices để đảm bảo có data
            fallback_voices = [
                ("👩 Young Female (female)", "female_young"),
                ("👨 Young Male (male)", "male_young"),
                ("🗣️ Narrator (neutral)", "neutral_narrator"),
                ("👩 Mature Female (female)", "female_mature"),
                ("👨 Mature Male (male)", "male_mature"),
                ("👩 Gentle Female (female)", "female_gentle"),
                ("👨 Deep Male (male)", "male_deep"),
                ("👶 Child Voice (neutral)", "child_voice"),
                ("👴 Elder Voice (neutral)", "elder_voice"),
                ("🎤 Voice Cloning (variable)", "cloned")
            ]
            
            for display, voice_id in fallback_voices:
                voice_combo.addItem(display, voice_id)
            
            # Set default selection
            voice_combo.setCurrentIndex(0)  # Default to Young Female
            
            voice_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, combo=voice_combo: self.update_character_voice(cid, combo.currentData())
            )
            
            # Voice Mode selector (NEW) - Chọn giữa Voice Selection vs Voice Clone
            # NOTE: Voice Prompt bị loại bỏ vì ChatterboxTTS không hỗ trợ text prompt
            mode_combo = QComboBox()
            mode_combo.setMaximumWidth(120)
            mode_combo.addItem("🗣️ Voice", "voice_selection")
            mode_combo.addItem("🎤 Clone", "voice_clone")
            mode_combo.setCurrentIndex(0)  # Default to voice selection
            mode_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    color: black;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    color: black;
                    selection-background-color: #007AFF;
                    selection-color: white;
                }
            """)
            mode_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, combo=mode_combo: self.update_character_voice_mode(cid, combo.currentData())
            )
            self.character_settings_table.setCellWidget(i, 4, mode_combo)

            # Stacked widget để chuyển đổi giữa Voice/Prompt/Clone
            stacked_widget = QStackedWidget()
            stacked_widget.setMaximumHeight(30)
            
            # 1. Voice Selection Widget
            voice_widget = QWidget()
            voice_layout = QHBoxLayout(voice_widget)
            voice_layout.setContentsMargins(2, 2, 2, 2)
            voice_layout.addWidget(voice_combo)
            
            # 2. Voice Clone Widget (moved up, prompt removed)
            
            clone_widget = QWidget()
            clone_layout = QHBoxLayout(clone_widget)
            clone_layout.setContentsMargins(2, 2, 2, 2)
            clone_layout.setSpacing(4)
            
            voice_clone_btn = QPushButton("📁 Select")
            voice_clone_btn.setMaximumWidth(80)
            voice_clone_btn.setToolTip(f"Chọn voice samples cho {character['name']}")
            voice_clone_btn.clicked.connect(lambda checked, cid=char_id: self.select_character_voice_clone_folder(cid))
            clone_layout.addWidget(voice_clone_btn)
            
            # Add widgets to stack (only 2 now)
            stacked_widget.addWidget(voice_widget)     # Index 0 - Voice Selection
            stacked_widget.addWidget(clone_widget)     # Index 1 - Voice Clone
            stacked_widget.setCurrentIndex(0)  # Default to voice selection
            
            self.character_settings_table.setCellWidget(i, 5, stacked_widget)
            
            # Quick action button (test for clone, etc.)
            quick_btn = QPushButton("🔧")
            quick_btn.setMaximumWidth(30)
            quick_btn.setToolTip("Quick actions")
            quick_btn.clicked.connect(lambda checked, cid=char_id: self.show_voice_quick_actions(cid))
            self.character_settings_table.setCellWidget(i, 6, quick_btn)
            
            # Status indicator
            status_label = QLabel("🗣️")
            status_label.setMaximumWidth(30)
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setToolTip("Voice Selection mode")
            self.character_settings_table.setCellWidget(i, 7, status_label)
            
            # Preview button
            preview_btn = QPushButton("🎧")
            preview_btn.setMaximumWidth(40)
            preview_btn.setToolTip(f"Preview {character['name']}")
            preview_btn.clicked.connect(lambda checked, cid=char_id: self.preview_character_with_settings(cid))
            self.character_settings_table.setCellWidget(i, 8, preview_btn)
            
            # Initialize character settings với voice mode
            self.character_chatterbox_settings[char_id] = {
                'emotion': 1.0,
                'speed': 1.0,
                'cfg_weight': 0.5,
                'voice_mode': 'voice_selection',  # NEW: voice_selection | voice_clone
                'voice_id': 'female_young',  # For voice_selection mode
                'voice_clone_path': None,  # For voice_clone mode
                'voice_clone_status': 'none'  # Track clone status
            }
            
            # Store widget references for mode switching
            if not hasattr(self, 'character_widgets'):
                self.character_widgets = {}
            self.character_widgets[char_id] = {
                'mode_combo': mode_combo,
                'stacked_widget': stacked_widget,
                'voice_combo': voice_combo,
                'voice_clone_btn': voice_clone_btn,
                'status_label': status_label,
                'quick_btn': quick_btn
            }
    
    def update_character_emotion_from_input(self, char_id, text):
        """Cập nhật emotion cho nhân vật cụ thể từ input"""
        try:
            value = float(text)
            value = max(0.0, min(3.0, value))  # Clamp to 0.0-3.0
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            self.character_chatterbox_settings[char_id]['emotion'] = value
        except ValueError:
            pass  # Ignore invalid input
    
    def update_character_speed_from_input(self, char_id, text):
        """Cập nhật speed cho nhân vật cụ thể từ input"""
        try:
            value = float(text)
            value = max(0.5, min(2.0, value))  # Clamp to 0.5-2.0
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            self.character_chatterbox_settings[char_id]['speed'] = value
        except ValueError:
            pass  # Ignore invalid input
    
    def update_character_cfg_weight_from_input(self, char_id, text):
        """Cập nhật CFG weight cho nhân vật cụ thể từ input"""
        try:
            value = float(text)
            value = max(0.0, min(1.0, value))  # Clamp to 0.0-1.0
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            self.character_chatterbox_settings[char_id]['cfg_weight'] = value
        except ValueError:
            pass  # Ignore invalid input
    
    def update_character_voice(self, char_id, voice_id):
        """Cập nhật voice cho nhân vật cụ thể và tự động adjust parameters theo gender"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        # Lưu voice_id
        self.character_chatterbox_settings[char_id]['voice_id'] = voice_id
        
        # 🎯 AUTO-ADJUST PARAMETERS dựa trên voice gender (như AI Gender Analysis)
        voice_gender_params = self._get_voice_gender_parameters(voice_id)
        
        # Cập nhật parameters trong settings
        self.character_chatterbox_settings[char_id]['emotion'] = voice_gender_params['emotion']
        self.character_chatterbox_settings[char_id]['speed'] = voice_gender_params['speed'] 
        self.character_chatterbox_settings[char_id]['cfg_weight'] = voice_gender_params['cfg_weight']
        
        # 🔄 CẬP NHẬT UI: Tìm và update input fields trong table
        for row in range(self.character_settings_table.rowCount()):
            name_item = self.character_settings_table.item(row, 0)
            if name_item and name_item.text() == char_id:
                # Update emotion input
                emotion_input = self.character_settings_table.cellWidget(row, 1)
                if emotion_input:
                    emotion_input.setText(f"{voice_gender_params['emotion']:.1f}")
                
                # Update speed input  
                speed_input = self.character_settings_table.cellWidget(row, 2)
                if speed_input:
                    speed_input.setText(f"{voice_gender_params['speed']:.1f}")
                
                # Update cfg weight input
                cfg_weight_input = self.character_settings_table.cellWidget(row, 3)
                if cfg_weight_input:
                    cfg_weight_input.setText(f"{voice_gender_params['cfg_weight']:.2f}")
                
                break
        
        print(f"🎭 Voice changed for {char_id}: {voice_id}")
        print(f"   ✨ Auto-adjusted: emotion={voice_gender_params['emotion']:.1f}, speed={voice_gender_params['speed']:.1f}, cfg_weight={voice_gender_params['cfg_weight']:.2f}")
    
    def update_character_voice_mode(self, char_id, voice_mode):
        """Cập nhật voice mode cho nhân vật và switch UI accordingly"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        # Update voice mode
        self.character_chatterbox_settings[char_id]['voice_mode'] = voice_mode
        
        # Get widget references
        if hasattr(self, 'character_widgets') and char_id in self.character_widgets:
            widgets = self.character_widgets[char_id]
            stacked_widget = widgets['stacked_widget']
            status_label = widgets['status_label']
            quick_btn = widgets['quick_btn']
            
            # Switch stacked widget and update status
            if voice_mode == 'voice_selection':
                stacked_widget.setCurrentIndex(0)  # Voice combo
                status_label.setText("🗣️")
                status_label.setToolTip("Voice Selection mode - chọn giọng có sẵn")
                quick_btn.setToolTip("Voice options")
                print(f"🗣️ {char_id}: Switched to VOICE SELECTION mode")
                
            elif voice_mode == 'voice_clone':
                stacked_widget.setCurrentIndex(1)  # Voice clone button
                status_label.setText("🎤")
                status_label.setToolTip("Voice Clone mode - nhân bản giọng từ mẫu audio")
                quick_btn.setToolTip("Test voice clone")
                print(f"🎤 {char_id}: Switched to VOICE CLONE mode")
    
    def _get_voice_gender_parameters(self, voice_id):
        """Lấy parameters tối ưu cho voice dựa trên gender (như AI Gender Analysis system)"""
        
        # 👩 FEMALE VOICES - nhẹ nhàng, biểu cảm hơn
        female_voices = ['female_young', 'female_mature', 'female_gentle']
        if voice_id in female_voices:
            return {
                'emotion': 1.2,     # Biểu cảm hơn
                'speed': 0.95,      # Chậm hơn một chút  
                'cfg_weight': 0.6   # Chất lượng cao
            }
        
        # 👨 MALE VOICES - mạnh mẽ, ít biểu cảm
        male_voices = ['male_young', 'male_mature', 'male_deep'] 
        if voice_id in male_voices:
            return {
                'emotion': 0.8,     # Ít biểu cảm, mạnh mẽ
                'speed': 1.05,      # Nhanh hơn một chút
                'cfg_weight': 0.4   # Cân bằng
            }
        
        # 🗣️ NEUTRAL VOICES - cân bằng
        neutral_voices = ['neutral_narrator', 'neutral_child', 'neutral_elder']
        if voice_id in neutral_voices:
            return {
                'emotion': 1.0,     # Cân bằng
                'speed': 1.0,       # Bình thường  
                'cfg_weight': 0.5   # Cân bằng
            }
        
        # 🎤 VOICE CLONING - default balanced
        if voice_id == 'cloned':
            return {
                'emotion': 1.0,     # Cân bằng
                'speed': 1.0,       # Bình thường
                'cfg_weight': 0.5   # Cân bằng
            }
        
        # Default fallback
        return {
            'emotion': 1.0,
            'speed': 1.0, 
            'cfg_weight': 0.5
        }
    
    def preview_character_with_settings(self, char_id):
        """Preview giọng với settings cụ thể của nhân vật"""
        try:
            # Validate và hiển thị priority logic
            voice_mode = self.validate_character_voice_settings(char_id)
            
            settings = self.character_chatterbox_settings.get(char_id, {})
            emotion = settings.get('emotion', 1.0)
            speed = settings.get('speed', 1.0) 
            cfg_weight = settings.get('cfg_weight', 0.5)
            voice_id = settings.get('voice_id', 'female_young')
            voice_clone_path = settings.get('voice_clone_path', None)
            voice_prompt = settings.get('voice_prompt', '').strip()
            
            char_name = self.get_character_name_by_id(char_id)
            
            # Tạo preview text dựa trên voice mode
            if voice_mode == 'clone':
                preview_text = f"Xin chào, tôi là {char_name}. Đây là giọng được clone từ voice samples."
            else:
                # Tìm voice display name
                voice_display_name = voice_id
                fallback_voices = [
                    ("👩 Young Female (female)", "female_young"),
                    ("👨 Young Male (male)", "male_young"),
                    ("🗣️ Narrator (neutral)", "neutral_narrator"),
                    ("👩 Mature Female (female)", "female_mature"),
                    ("👨 Mature Male (male)", "male_mature"),
                    ("👩 Gentle Female (female)", "female_gentle"),
                    ("👨 Deep Male (male)", "male_deep"),
                    ("👶 Child Voice (neutral)", "child_voice"),
                    ("👴 Elder Voice (neutral)", "elder_voice"),
                    ("🎤 Voice Cloning (variable)", "cloned")
                ]
                
                for display, vid in fallback_voices:
                    if vid == voice_id:
                        voice_display_name = display
                        break
                
                preview_text = f"Xin chào, tôi là {char_name}. Đây là giọng {voice_display_name} với emotion {emotion:.1f}, speed {speed:.1f}x và CFG weight {cfg_weight:.2f}"
            
            # Generate preview
            import tempfile
            temp_dir = tempfile.mkdtemp()
            preview_path = os.path.join(temp_dir, f"preview_{char_id}.mp3")
                
            result = self.voice_generator.generate_voice_chatterbox(
                text=preview_text,
                save_path=preview_path,
                voice_sample_path=voice_clone_path if voice_mode == 'clone' else None,
                emotion_exaggeration=emotion,
                speed=speed,
                voice_name=voice_id if voice_mode == 'selection' else None,
                cfg_weight=cfg_weight
            )
            
            if result.get('success'):
                self.play_audio_file(preview_path)
                from PySide6.QtWidgets import QMessageBox
                
                # Tạo message với priority info
                message = f"Character: {char_name}\n"
                message += f"Mode: {voice_mode.upper()}\n\n"
                
                if voice_mode == 'clone':
                    message += f"Voice Clone: {voice_clone_path}\n"
                else:
                    message += f"Voice: {voice_display_name}\n"
                
                message += f"Emotion: {emotion:.1f}\n"
                message += f"Speed: {speed:.1f}x\n"
                message += f"CFG Weight: {cfg_weight:.2f}\n"
                message += f"\n🤖 Generated by Chatterbox TTS"
                
                QMessageBox.information(self, "🎧 Preview Voice", message)
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "❌ Lỗi Preview", f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "❌ Lỗi Critical", f"Lỗi preview voice:\n{str(e)}")
    
    def update_character_voice_prompt(self, char_id, prompt_text):
        """Cập nhật voice prompt cho nhân vật cụ thể"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        self.character_chatterbox_settings[char_id]['voice_prompt'] = prompt_text
        
        if prompt_text.strip():
            print(f"💬 Voice prompt updated for {self.get_character_name_by_id(char_id)}: '{prompt_text[:50]}...'")
        else:
            print(f"💬 Voice prompt cleared for {self.get_character_name_by_id(char_id)}")
    
    def show_voice_quick_actions(self, char_id):
        """Hiển thị quick actions cho voice mode hiện tại"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_mode = settings.get('voice_mode', 'voice_selection')
        char_name = self.get_character_name_by_id(char_id)
        
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Quick Actions - {char_name}")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        if voice_mode == 'voice_selection':
            layout.addWidget(QLabel(f"🗣️ Voice Selection Mode - {char_name}"))
            layout.addWidget(QLabel("Quick actions for voice selection:"))
            
            # Auto-optimize button
            optimize_btn = QPushButton("🎯 Auto-optimize Parameters")
            optimize_btn.clicked.connect(lambda: self.auto_optimize_voice_params(char_id, dialog))
            layout.addWidget(optimize_btn)
            
            # Reset to defaults
            reset_btn = QPushButton("🔄 Reset to Defaults")
            reset_btn.clicked.connect(lambda: self.reset_voice_params(char_id, dialog))
            layout.addWidget(reset_btn)
            
        elif voice_mode == 'voice_clone':
            layout.addWidget(QLabel(f"🎤 Voice Clone Mode - {char_name}"))
            layout.addWidget(QLabel("Quick actions for voice cloning:"))
            
            # Test clone button
            test_btn = QPushButton("🧪 Test Voice Clone")
            test_btn.clicked.connect(lambda: self.test_voice_clone(char_id, dialog))
            layout.addWidget(test_btn)
            
            # Clear clone path
            clear_btn = QPushButton("🗑️ Clear Clone Path")
            clear_btn.clicked.connect(lambda: self.clear_voice_clone_path(char_id, dialog))
            layout.addWidget(clear_btn)
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def auto_optimize_voice_params(self, char_id, dialog):
        """Tự động tối ưu parameters cho voice"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_id = settings.get('voice_id', 'female_young')
        
        # Get optimized params
        optimized_params = self._get_voice_gender_parameters(voice_id)
        
        # Update settings
        self.character_chatterbox_settings[char_id].update(optimized_params)
        
        # Update UI
        self.populate_character_settings_table()
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(dialog, "✅ Optimized", 
                              f"Parameters optimized for {voice_id}:\n"
                              f"Emotion: {optimized_params['emotion']:.1f}\n"
                              f"Speed: {optimized_params['speed']:.1f}\n"
                              f"CFG Weight: {optimized_params['cfg_weight']:.2f}")
        dialog.close()
    
    def reset_voice_params(self, char_id, dialog):
        """Reset voice parameters về defaults"""
        self.character_chatterbox_settings[char_id].update({
            'emotion': 1.0,
            'speed': 1.0,
            'cfg_weight': 0.5
        })
        
        # Update UI
        self.populate_character_settings_table()
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(dialog, "🔄 Reset", "Parameters reset to defaults")
        dialog.close()
    
    def test_voice_clone(self, char_id, dialog):
        """Test voice clone với sample text"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_clone_path = settings.get('voice_clone_path')
        
        if not voice_clone_path:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(dialog, "⚠️ Warning", "No voice clone path selected!")
            return
        
        # Test với sample text
        char_name = self.get_character_name_by_id(char_id)
        test_text = f"Xin chào, tôi là {char_name}. Đây là test voice cloning."
        
        import tempfile
        temp_dir = tempfile.mkdtemp()
        test_path = os.path.join(temp_dir, f"test_clone_{char_id}.mp3")
        
        result = self.voice_generator.generate_voice_chatterbox(
            text=test_text,
            save_path=test_path,
            voice_sample_path=voice_clone_path,
            emotion_exaggeration=settings.get('emotion', 1.0),
            speed=settings.get('speed', 1.0),
            cfg_weight=settings.get('cfg_weight', 0.5)
        )
        
        if result.get('success'):
            self.play_audio_file(test_path)
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(dialog, "✅ Test Success", "Voice clone test completed!")
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(dialog, "❌ Test Failed", f"Test failed: {result.get('error', 'Unknown error')}")
    
    def clear_voice_clone_path(self, char_id, dialog):
        """Clear voice clone path"""
        self.character_chatterbox_settings[char_id]['voice_clone_path'] = None
        self.character_chatterbox_settings[char_id]['voice_clone_status'] = 'none'
        
        # Update UI
        self._update_voice_clone_status_ui(char_id, 'none', "No voice samples")
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(dialog, "🗑️ Cleared", "Voice clone path cleared")
        dialog.close()
    
    def show_voice_prompt_examples(self, char_id, input_field):
        """Hiển thị dialog với voice prompt examples"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Voice Prompt Examples - {self.get_character_name_by_id(char_id)}")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chọn example hoặc tự viết prompt:"))
        
        examples = [
            ("👩 MC Radio", "Giọng nữ trẻ, vui vẻ, năng động như MC radio, nói nhanh và có intonation rõ ràng"),
            ("👨 Tin tức", "Giọng nam trầm, nghiêm túc, uy tín như người dẫn chương trình tin tức"),
            ("👶 Trẻ em", "Giọng trẻ em vui vẻ, trong trẻo, hồn nhiên như trong truyện cổ tích"),
            ("👩 Gentle", "Giọng nữ nhẹ nhàng, dịu dàng, ấm áp như người mẹ kể chuyện"),
            ("👨 Hero", "Giọng nam mạnh mẽ, quyết đoán, anh hùng như trong phim hành động"),
            ("🎭 Dramatic", "Giọng kịch tính, cảm xúc mạnh, như diễn viên sân khấu"),
            ("😄 Happy", "Giọng vui vẻ, tươi tắn, luôn cười, tích cực"),
            ("😢 Sad", "Giọng buồn bã, u sầu, chậm rãi, đầy cảm xúc"),
            ("😠 Angry", "Giọng tức giận, quyết liệt, mạnh mẽ, có sức thuyết phục"),
            ("🤫 Mysterious", "Giọng bí ẩn, thầm thì, huyền bí như trong phim trinh thám")
        ]
        
        for title, prompt in examples:
            btn = QPushButton(f"{title}")
            btn.setToolTip(prompt)
            btn.clicked.connect(lambda checked, p=prompt: self.apply_voice_prompt_example(input_field, p, dialog))
            layout.addWidget(btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def apply_voice_prompt_example(self, input_field, prompt, dialog):
        """Apply voice prompt example to input field"""
        input_field.setText(prompt)
        dialog.accept()
    
    def select_character_voice_clone_folder(self, char_id):
        """Chọn thư mục voice samples cho nhân vật cụ thể với progress tracking"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
        from PySide6.QtCore import QTimer
        
        character_name = self.get_character_name_by_id(char_id)
        folder = QFileDialog.getExistingDirectory(
            self, 
            f"Chọn thư mục voice samples cho {character_name}",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            # Show progress dialog
            progress = QProgressDialog(f"Đang xử lý voice samples cho {character_name}...", "Hủy", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            # Update status to processing
            self._update_voice_clone_status_ui(char_id, 'processing', 'Đang xử lý...')
            
            # Kiểm tra xem folder có audio files không
            import os
            audio_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
            audio_files = []
            
            progress.setValue(20)
            
            try:
                for file in os.listdir(folder):
                    if any(file.lower().endswith(ext) for ext in audio_extensions):
                        audio_files.append(file)
                
                progress.setValue(50)
                
                if not audio_files:
                    progress.close()
                    self._update_voice_clone_status_ui(char_id, 'error', 'Không tìm thấy audio files')
                    QMessageBox.warning(
                        self, 
                        "⚠️ Không tìm thấy audio files", 
                        f"Thư mục '{folder}' không chứa file audio nào (.wav, .mp3, .flac, .ogg, .m4a)"
                    )
                    return
                
                progress.setValue(80)
                
                # Lưu path và update status
                if char_id not in self.character_chatterbox_settings:
                    self.character_chatterbox_settings[char_id] = {}
                
                self.character_chatterbox_settings[char_id]['voice_clone_path'] = folder
                self.character_chatterbox_settings[char_id]['voice_clone_status'] = 'ready'
                
                progress.setValue(100)
                progress.close()
                
                # Update UI status
                self._update_voice_clone_status_ui(char_id, 'ready', f"{len(audio_files)} files sẵn sàng")
                
                print(f"📁 Voice clone folder set for {character_name}: {folder}")
                print(f"   🎵 Found {len(audio_files)} audio files: {', '.join(audio_files[:3])}{'...' if len(audio_files) > 3 else ''}")
                
                QMessageBox.information(
                    self,
                    "✅ Voice Clone Setup",
                    f"Đã thiết lập voice cloning cho {character_name}\n"
                    f"Thư mục: {folder}\n"
                    f"Tìm thấy: {len(audio_files)} audio files"
                )
                
            except Exception as e:
                progress.close()
                self._update_voice_clone_status_ui(char_id, 'error', f'Lỗi: {str(e)}')
                QMessageBox.critical(
                    self,
                    "❌ Lỗi Voice Clone Setup",
                    f"Không thể thiết lập voice cloning:\n{str(e)}"
                )
    
    def _update_voice_clone_status_ui(self, char_id, status, tooltip_text=""):
        """Cập nhật UI status cho voice clone của nhân vật"""
        status_icons = {
            'none': '❌',
            'ready': '✅', 
            'processing': '⏳',
            'error': '❌'
        }
        
        status_colors = {
            'none': 'color: red;',
            'ready': 'color: green;',
            'processing': 'color: orange;',
            'error': 'color: red;'
        }
        
        # Tìm row của character này
        for i in range(self.character_settings_table.rowCount()):
            name_item = self.character_settings_table.item(i, 0)
            if name_item and name_item.text() == self.get_character_name_by_id(char_id):
                # Lấy voice clone container
                voice_clone_container = self.character_settings_table.cellWidget(i, 6)
                if voice_clone_container:
                    # Tìm status label (widget thứ 2 trong layout)
                    layout = voice_clone_container.layout()
                    if layout and layout.count() > 1:
                        status_label = layout.itemAt(1).widget()
                        if status_label:
                            status_label.setText(status_icons.get(status, '❓'))
                            status_label.setStyleSheet(status_colors.get(status, ''))
                            status_label.setToolTip(tooltip_text or f"Status: {status}")
                break
    
    def get_character_name_by_id(self, char_id):
        """Helper để lấy tên nhân vật từ ID"""
        if self.voice_studio_script_data:
            for character in self.voice_studio_script_data['characters']:
                if character['id'] == char_id:
                    return character['name']
        return f"Character {char_id}"
    
    def toggle_voice_cloning(self, enabled):
        """Toggle voice cloning controls"""
        self.voice_clone_folder_btn.setEnabled(enabled)
    
    def select_voice_clone_folder(self):
        """Chọn thư mục chứa voice samples"""
        from PySide6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục voice samples")
        if folder:
            self.voice_clone_folder = folder
            self.voice_clone_path_label.setText(f"📁 {folder}")
            self.voice_clone_path_label.setStyleSheet("color: green; font-weight: bold; margin-left: 20px;")
    
    def validate_character_voice_settings(self, char_id):
        """Validate character voice settings dựa trên voice mode được chọn"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_mode = settings.get('voice_mode', 'voice_selection')
        char_name = self.get_character_name_by_id(char_id)
        
        if voice_mode == 'voice_clone':
            voice_clone_path = settings.get('voice_clone_path')
            if voice_clone_path and os.path.exists(voice_clone_path):
                print(f"🎯 {char_name}: Using VOICE CLONE - {voice_clone_path}")
                return 'clone'
            else:
                # Fallback to voice selection if no clone
                print(f"⚠️ {char_name}: Voice clone mode selected but no samples provided, fallback to voice selection")
                voice_id = settings.get('voice_id', 'female_young')
                print(f"🎯 {char_name}: Using VOICE SELECTION (fallback) - {voice_id}")
                return 'selection'
                
        else:  # voice_selection mode
            voice_id = settings.get('voice_id', 'female_young')
            print(f"🎯 {char_name}: Using VOICE SELECTION - {voice_id}")
            return 'selection'
    
    def apply_preset(self, preset_type):
        """Áp dụng preset settings"""
        presets = {
            "natural": {"emotion": 1.0, "speed": 1.0},
            "dramatic": {"emotion": 2.5, "speed": 0.9},
            "fast": {"emotion": 1.2, "speed": 1.5},
            "slow": {"emotion": 0.8, "speed": 0.7}
        }
        
        if preset_type in presets:
            preset = presets[preset_type]
            
            # Update global sliders
            emotion_value = int(preset["emotion"] * 100)
            speed_value = int(preset["speed"] * 100)
            
            self.emotion_slider.setValue(emotion_value)
            self.speed_slider.setValue(speed_value)
            
            # Update all character settings
            for char_id in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id]['emotion'] = preset["emotion"]
                self.character_chatterbox_settings[char_id]['speed'] = preset["speed"]
            
            # Update character table sliders
            for i in range(self.character_settings_table.rowCount()):
                emotion_slider = self.character_settings_table.cellWidget(i, 1)
                speed_slider = self.character_settings_table.cellWidget(i, 2)
                if emotion_slider:
                    emotion_slider.setValue(emotion_value)
                if speed_slider:
                    speed_slider.setValue(speed_value)
            
            QMessageBox.information(self, "Preset", f"Đã áp dụng preset '{preset_type.title()}'!")
    
    def get_character_chatterbox_settings(self, char_id):
        """Lấy settings cho character khi manual mode enabled"""
        if self.enable_chatterbox_manual.isChecked():
            return self.character_chatterbox_settings.get(char_id, {
                'emotion': self.emotion_slider.value() / 100.0,
                'speed': self.speed_slider.value() / 100.0,
                'voice_clone_path': None
            })
        else:
            return {'emotion': 1.0, 'speed': 1.0, 'voice_clone_path': None}
    
    def map_emotion_to_parameters(self, emotion_label, base_exaggeration=1.0):
        """Map emotion label thành emotion exaggeration + cfg_weight cho chất lượng tối ưu"""
        
        # Enhanced emotion mapping table với cả exaggeration và cfg_weight
        emotion_mapping = {
            # Mục đích: Tự nhiên, giọng kể chuyện
            'neutral': {'exaggeration_mult': 0.4, 'cfg_weight': 0.5},
            
            # Giọng nhân mạnh (hùng biện, tức giận) 
            'angry': {'exaggeration_mult': 1.2, 'cfg_weight': 0.35},
            'threatening': {'exaggeration_mult': 1.2, 'cfg_weight': 0.35},
            'confident': {'exaggeration_mult': 1.1, 'cfg_weight': 0.35},
            'proud': {'exaggeration_mult': 1.1, 'cfg_weight': 0.35},
            'dramatic': {'exaggeration_mult': 1.3, 'cfg_weight': 0.35},
            'shout': {'exaggeration_mult': 1.3, 'cfg_weight': 0.30},
            
            # Cảm xúc nhẹ nhàng, nữ tính
            'happy': {'exaggeration_mult': 0.7, 'cfg_weight': 0.45},
            'excited': {'exaggeration_mult': 0.8, 'cfg_weight': 0.45},
            'friendly': {'exaggeration_mult': 0.7, 'cfg_weight': 0.45},
            'romantic': {'exaggeration_mult': 0.7, 'cfg_weight': 0.45},
            'surprised': {'exaggeration_mult': 0.7, 'cfg_weight': 0.45},
            'pleading': {'exaggeration_mult': 0.8, 'cfg_weight': 0.45},
            
            # Cảm xúc đặc biệt
            'sad': {'exaggeration_mult': 0.6, 'cfg_weight': 0.45},
            'fear': {'exaggeration_mult': 0.7, 'cfg_weight': 0.40},
            'calm': {'exaggeration_mult': 0.4, 'cfg_weight': 0.50},
            'whisper': {'exaggeration_mult': 0.3, 'cfg_weight': 0.50},
            'shy': {'exaggeration_mult': 0.4, 'cfg_weight': 0.45},
            'mysterious': {'exaggeration_mult': 0.5, 'cfg_weight': 0.40},
            'sarcastic': {'exaggeration_mult': 1.0, 'cfg_weight': 0.35},
        }
        
        # Get mapping cho emotion label
        mapping = emotion_mapping.get(emotion_label.lower(), {'exaggeration_mult': 1.0, 'cfg_weight': 0.5})
        
        # Calculate final parameters
        final_exaggeration = base_exaggeration * mapping['exaggeration_mult']
        cfg_weight = mapping['cfg_weight']
        
        # Clamp exaggeration vào range 0.0-2.0
        final_exaggeration = max(0.0, min(2.0, final_exaggeration))
        
        # Clamp cfg_weight vào range 0.0-1.0  
        cfg_weight = max(0.0, min(1.0, cfg_weight))
        
        # Log để user thấy emotion được áp dụng
        if emotion_label.lower() != 'neutral':
            print(f"   🎭 Emotion Auto-Mapping: '{emotion_label}' → exaggeration={final_exaggeration:.2f}, cfg_weight={cfg_weight:.2f}")
        
        return final_exaggeration, cfg_weight
    
    def update_emotion_from_slider(self, value):
        """Cập nhật emotion input từ slider"""
        emotion_value = value / 100.0  # Convert 0-300 to 0.0-3.0
        self.emotion_input.setText(f"{emotion_value:.1f}")
    
    def update_emotion_from_input(self):
        """Cập nhật emotion slider từ input"""
        try:
            value = float(self.emotion_input.text())
            value = max(0.0, min(3.0, value))  # Clamp to 0.0-3.0
            slider_value = int(value * 100)  # Convert to 0-300
            self.emotion_slider.setValue(slider_value)
        except ValueError:
            pass  # Ignore invalid input
    
    def update_speed_from_slider(self, value):
        """Cập nhật speed input từ slider"""
        speed_value = value / 100.0  # Convert 50-200 to 0.5-2.0
        self.speed_input.setText(f"{speed_value:.1f}")
    
    def update_speed_from_input(self):
        """Cập nhật speed slider từ input"""
        try:
            value = float(self.speed_input.text())
            value = max(0.5, min(2.0, value))  # Clamp to 0.5-2.0
            slider_value = int(value * 100)  # Convert to 50-200
            self.speed_slider.setValue(slider_value)
        except ValueError:
            pass  # Ignore invalid input
    
    def update_cfg_weight_from_slider(self, value):
        """Cập nhật CFG weight input từ slider"""
        cfg_value = value / 100.0  # Convert 0-100 to 0.0-1.0
        self.cfg_weight_input.setText(f"{cfg_value:.2f}")
    
    def update_cfg_weight_from_input(self):
        """Cập nhật CFG weight slider từ input"""
        try:
            value = float(self.cfg_weight_input.text())
            value = max(0.0, min(1.0, value))  # Clamp to 0.0-1.0
            slider_value = int(value * 100)  # Convert to 0-100
            self.cfg_weight_slider.setValue(slider_value)
        except ValueError:
            pass  # Ignore invalid input
    
    def update_default_voice_options(self):
        """Cập nhật danh sách giọng default"""
        self.default_voice_combo.clear()
        
        # Lấy voices từ Chatterbox provider
        if self.voice_generator.chatterbox_provider:
            available_voices = self.voice_generator.chatterbox_provider.get_available_voices()
            for voice in available_voices:
                display_text = f"{voice['name']} ({voice['gender']})"
                self.default_voice_combo.addItem(display_text, voice['id'])
        else:
            # Fallback voices
            fallback_voices = [
                ("Young Female (female)", "female_young"),
                ("Young Male (male)", "male_young"),
                ("Narrator (neutral)", "neutral_narrator"),
                ("Voice Cloning (variable)", "cloned")
            ]
            for display, voice_id in fallback_voices:
                self.default_voice_combo.addItem(display, voice_id)
    
    def preview_default_voice(self):
        """Preview giọng default với settings hiện tại"""
        try:
            # Get current settings
            emotion = float(self.emotion_input.text())
            speed = float(self.speed_input.text())
            cfg_weight = float(self.cfg_weight_input.text())
            voice_id = self.default_voice_combo.currentData()
            voice_name = self.default_voice_combo.currentText()
            
            # Preview text
            preview_text = f"Đây là giọng {voice_name} với emotion {emotion}, speed {speed}, và CFG weight {cfg_weight}."
            
            # Generate preview audio
            import tempfile
            temp_dir = tempfile.mkdtemp()
            preview_path = os.path.join(temp_dir, "preview_default_voice.mp3")
            
            result = self.voice_generator.generate_voice_chatterbox(
                text=preview_text,
                save_path=preview_path,
                voice_sample_path=None,
                emotion_exaggeration=emotion,
                speed=speed,
                voice_name=voice_id,
                cfg_weight=cfg_weight
            )
            
            if result.get('success'):
                self.play_audio_file(preview_path)
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Preview", f"Preview: {voice_name}\nEmotion: {emotion}\nSpeed: {speed}\nCFG Weight: {cfg_weight}")
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Lỗi", f"Không thể tạo preview:\\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Lỗi", f"Lỗi preview voice:\\n{str(e)}")