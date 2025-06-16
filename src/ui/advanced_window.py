from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTabWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
                               QProgressBar, QListWidget, QComboBox, QSpinBox, 
                               QCheckBox, QFileDialog, QMessageBox, QScrollArea,
                               QDialog, QRadioButton, QButtonGroup, QSplitter,
                               QGroupBox, QGridLayout)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont
import sys
import os
import subprocess
import platform

# Import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.video_pipeline import VideoPipeline
from video.effects_presets import EffectsPresets
from ai.prompt_templates import PromptTemplates
from core.api_manager import APIManager
from tts.voice_generator import VoiceGenerator
from .character_voice_dialog import CharacterVoiceDialog
from .manual_voice_setup_dialog import ManualVoiceSetupDialog
from .macos_styles import get_macos_stylesheet, get_macos_window_size

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
        """Tạo audio từ script data đã có với character voice selection"""
        if not self.current_script_data:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tạo câu chuyện trước!")
            return
        
        characters = self.current_script_data.get('characters', [])
        if not characters:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy thông tin nhân vật!")
            return
        
        # Import voice generator
        from tts.voice_generator import VoiceGenerator
        voice_gen = VoiceGenerator()
        
        # Open character voice dialog
        dialog = CharacterVoiceDialog(characters, voice_gen, self)
        if dialog.exec_() == QDialog.Accepted:
            voice_mapping = dialog.get_voice_mapping()
            
            # Disable button during generation
            self.generate_audio_btn.setEnabled(False)
            self.generate_audio_btn.setText("⏳ Đang tạo...")
            self.progress_label.setText("Đang tạo audio...")
            
            try:
                # Get project folder
                project_folder = self.project_folder_input.text() or "./projects"
                project_name = self.project_name_input.text() or "audio_project"
                
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