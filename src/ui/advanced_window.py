from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTabWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
                               QProgressBar, QListWidget, QComboBox, QSpinBox, 
                               QCheckBox, QFileDialog, QMessageBox, QScrollArea,
                               QDialog, QRadioButton, QButtonGroup)
from PySide6.QtCore import QThread, Signal
import sys
import os
import subprocess

# Import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.video_pipeline import VideoPipeline
from video.effects_presets import EffectsPresets
from ai.prompt_templates import PromptTemplates
from core.api_manager import APIManager
from .character_voice_dialog import CharacterVoiceDialog
from .manual_voice_setup_dialog import ManualVoiceSetupDialog

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
        self.setGeometry(100, 100, 1000, 700)
        
        # Khởi tạo pipeline và API manager
        self.pipeline = VideoPipeline()
        self.api_manager = APIManager()
        self.current_project_id = None
        self.current_script_data = None  # Store generated script data
        
        # Widget trung tâm với tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Tạo các tabs
        self.create_video_tab()
        self.create_projects_tab()
        self.create_settings_tab()
    
    def create_video_tab(self):
        """Tab tạo video mới"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Gợi ý prompt
        prompt_suggestions_layout = QHBoxLayout()
        prompt_suggestions_layout.addWidget(QLabel("Gợi ý prompt:"))
        self.category_combo = QComboBox()
        categories = PromptTemplates.get_all_categories()
        self.category_combo.addItem("-- Chọn danh mục --", "")
        for key, value in categories.items():
            self.category_combo.addItem(value["category"], key)
        self.category_combo.currentTextChanged.connect(self.load_prompt_suggestions)
        prompt_suggestions_layout.addWidget(self.category_combo)
        
        self.random_prompt_btn = QPushButton("Prompt ngẫu nhiên")
        self.random_prompt_btn.clicked.connect(self.get_random_prompt)
        prompt_suggestions_layout.addWidget(self.random_prompt_btn)
        layout.addLayout(prompt_suggestions_layout)
        
        # Danh sách prompt gợi ý
        self.prompt_suggestions_list = QComboBox()
        self.prompt_suggestions_list.addItem("-- Chọn prompt mẫu --")
        self.prompt_suggestions_list.currentTextChanged.connect(self.use_suggested_prompt)
        layout.addWidget(self.prompt_suggestions_list)
        
        # Nhập prompt
        layout.addWidget(QLabel("Prompt nội dung video:"))
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ví dụ: Tạo video giới thiệu về du lịch Việt Nam với 5 điểm đến nổi tiếng...")
        self.prompt_input.setMaximumHeight(100)
        layout.addWidget(self.prompt_input)
        
        # Tên project
        layout.addWidget(QLabel("Tên project:"))
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("video_project")
        layout.addWidget(self.project_name_input)
        
        # Chọn thư mục dự án
        project_folder_layout = QHBoxLayout()
        project_folder_layout.addWidget(QLabel("Thư mục dự án:"))
        self.project_folder_input = QLineEdit()
        self.project_folder_input.setPlaceholderText("Mặc định: ./projects/")
        self.project_folder_input.setReadOnly(True)
        project_folder_layout.addWidget(self.project_folder_input)
        
        self.select_project_folder_btn = QPushButton("📁 Chọn")
        self.select_project_folder_btn.clicked.connect(self.select_project_folder)
        project_folder_layout.addWidget(self.select_project_folder_btn)
        
        layout.addLayout(project_folder_layout)
        
        # Tùy chọn tạo ảnh
        layout.addWidget(QLabel("Tùy chọn tạo ảnh:"))
        image_options_layout = QHBoxLayout()
        self.auto_generate_radio = QCheckBox("Tự động tạo ảnh AI")
        self.auto_generate_radio.setChecked(True)
        self.manual_images_radio = QCheckBox("Chọn ảnh thủ công")
        image_options_layout.addWidget(self.auto_generate_radio)
        image_options_layout.addWidget(self.manual_images_radio)
        
        self.select_images_btn = QPushButton("Chọn thư mục ảnh")
        self.select_images_btn.clicked.connect(self.select_images_folder)
        self.select_images_btn.setEnabled(False)
        image_options_layout.addWidget(self.select_images_btn)
        layout.addLayout(image_options_layout)
        
        # Kết nối sự kiện
        self.manual_images_radio.toggled.connect(self.toggle_image_mode)
        
        # Hiển thị thư mục ảnh đã chọn
        self.selected_images_label = QLabel("Chưa chọn thư mục ảnh")
        self.selected_images_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.selected_images_label)
        
        # Preset hiệu ứng
        layout.addWidget(QLabel("Preset hiệu ứng:"))
        self.effects_preset_combo = QComboBox()
        presets = EffectsPresets.get_all_presets()
        for key, preset in presets.items():
            self.effects_preset_combo.addItem(f"{preset['name']} - {preset['description']}", key)
        self.effects_preset_combo.setCurrentText("Năng động")
        layout.addWidget(self.effects_preset_combo)
        
        # Cài đặt hiệu ứng tùy chỉnh
        effects_layout = QHBoxLayout()
        self.zoom_checkbox = QCheckBox("Hiệu ứng zoom")
        self.zoom_checkbox.setChecked(True)
        self.transitions_checkbox = QCheckBox("Chuyển cảnh")
        self.transitions_checkbox.setChecked(True)
        effects_layout.addWidget(self.zoom_checkbox)
        effects_layout.addWidget(self.transitions_checkbox)
        layout.addLayout(effects_layout)
        
        # Nút actions
        actions_layout = QHBoxLayout()
        
        self.generate_story_btn = QPushButton("📝 Tạo câu chuyện")
        self.generate_story_btn.clicked.connect(self.generate_story_only)
        actions_layout.addWidget(self.generate_story_btn)
        
        self.generate_audio_btn = QPushButton("🎵 Tạo Audio")
        self.generate_audio_btn.clicked.connect(self.generate_audio_only)
        self.generate_audio_btn.setEnabled(False)  # Enabled after story creation
        actions_layout.addWidget(self.generate_audio_btn)
        
        self.generate_btn = QPushButton("🎬 Tạo video")
        self.generate_btn.clicked.connect(self.start_video_generation)
        actions_layout.addWidget(self.generate_btn)
        
        layout.addLayout(actions_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Preview content area
        layout.addWidget(QLabel("Preview nội dung:"))
        self.content_preview = QTextEdit()
        self.content_preview.setReadOnly(True)
        self.content_preview.setMaximumHeight(150)
        
        # Audio controls
        audio_controls_layout = QHBoxLayout()
        
        self.manual_voice_setup_btn = QPushButton("🎭 Cấu hình giọng thủ công")
        self.manual_voice_setup_btn.clicked.connect(self.show_manual_voice_setup)
        audio_controls_layout.addWidget(self.manual_voice_setup_btn)
        
        self.open_audio_folder_btn = QPushButton("📁 Mở thư mục Audio")
        self.open_audio_folder_btn.clicked.connect(self.open_audio_folder)
        self.open_audio_folder_btn.setEnabled(False)
        audio_controls_layout.addWidget(self.open_audio_folder_btn)
        
        self.play_final_audio_btn = QPushButton("▶️ Nghe Audio hoàn chỉnh")
        self.play_final_audio_btn.clicked.connect(self.play_final_audio)
        self.play_final_audio_btn.setEnabled(False)
        audio_controls_layout.addWidget(self.play_final_audio_btn)
        
        audio_controls_layout.addStretch()
        layout.addLayout(audio_controls_layout)
        
        # Store audio paths
        self.last_audio_output_dir = None
        self.last_final_audio_path = None
        self.content_preview.setPlaceholderText("Nội dung câu chuyện sẽ hiển thị ở đây sau khi tạo...")
        layout.addWidget(self.content_preview)
        
        # Voice settings
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Giọng đọc Google TTS:"))
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
        layout.addLayout(voice_layout)
        
        self.tabs.addTab(tab, "Tạo Video")
    
    def create_projects_tab(self):
        """Tab quản lý projects"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Nút refresh
        refresh_btn = QPushButton("Làm mới danh sách")
        refresh_btn.clicked.connect(self.refresh_projects)
        layout.addWidget(refresh_btn)
        
        # Danh sách projects
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.load_project_details)
        layout.addWidget(self.projects_list)
        
        # Chi tiết project
        self.project_details = QTextEdit()
        self.project_details.setReadOnly(True)
        self.project_details.setMaximumHeight(200)
        layout.addWidget(self.project_details)
        
        # Nút actions
        actions_layout = QHBoxLayout()
        self.open_folder_btn = QPushButton("Mở thư mục")
        self.open_folder_btn.clicked.connect(self.open_project_folder)
        self.delete_project_btn = QPushButton("Xóa project")
        self.delete_project_btn.clicked.connect(self.delete_project)
        actions_layout.addWidget(self.open_folder_btn)
        actions_layout.addWidget(self.delete_project_btn)
        layout.addLayout(actions_layout)
        
        self.tabs.addTab(tab, "Projects")
        
        # Load projects khi khởi tạo
        self.refresh_projects()
    
    def create_settings_tab(self):
        """Tab cài đặt"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # API Keys
        layout.addWidget(QLabel("🔑 Cài đặt API Keys:"))
        
        # AI Content Generation
        layout.addWidget(QLabel("📝 AI Sinh nội dung:"))
        
        layout.addWidget(QLabel("OpenAI API Key (GPT-4):"))
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.openai_key_input)
        
        layout.addWidget(QLabel("Claude API Key (Anthropic):"))
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.Password)
        self.claude_key_input.setPlaceholderText("sk-ant-...")
        layout.addWidget(self.claude_key_input)
        
        layout.addWidget(QLabel("DeepSeek API Key:"))
        self.deepseek_key_input = QLineEdit()
        self.deepseek_key_input.setEchoMode(QLineEdit.Password)
        self.deepseek_key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.deepseek_key_input)
        
        # Image Generation
        layout.addWidget(QLabel("🎨 AI Tạo ảnh:"))
        
        layout.addWidget(QLabel("DALL-E (OpenAI) - dùng chung key OpenAI"))
        
        layout.addWidget(QLabel("Midjourney API Key:"))
        self.midjourney_key_input = QLineEdit()
        self.midjourney_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.midjourney_key_input)
        
        layout.addWidget(QLabel("Stability AI Key (Stable Diffusion):"))
        self.stability_key_input = QLineEdit()
        self.stability_key_input.setEchoMode(QLineEdit.Password)
        self.stability_key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.stability_key_input)
        
        # Text-to-Speech
        layout.addWidget(QLabel("🎤 Text-to-Speech:"))
        
        layout.addWidget(QLabel("ElevenLabs API Key:"))
        self.elevenlabs_key_input = QLineEdit()
        self.elevenlabs_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_key_input.setPlaceholderText("sk_...")
        layout.addWidget(self.elevenlabs_key_input)
        
        layout.addWidget(QLabel("Google Cloud TTS Key:"))
        self.google_tts_key_input = QLineEdit()
        self.google_tts_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.google_tts_key_input)
        
        layout.addWidget(QLabel("Azure Speech Key:"))
        self.azure_speech_key_input = QLineEdit()
        self.azure_speech_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.azure_speech_key_input)
        
        # Provider Selection
        layout.addWidget(QLabel("⚙️ Chọn nhà cung cấp:"))
        
        # AI Content Provider
        content_provider_layout = QHBoxLayout()
        content_provider_layout.addWidget(QLabel("AI Sinh nội dung:"))
        self.content_provider_combo = QComboBox()
        self.content_provider_combo.addItems(self.api_manager.get_available_content_providers())
        content_provider_layout.addWidget(self.content_provider_combo)
        layout.addLayout(content_provider_layout)
        
        # Image Generation Provider
        image_provider_layout = QHBoxLayout()
        image_provider_layout.addWidget(QLabel("AI Tạo ảnh:"))
        self.image_provider_combo = QComboBox()
        self.image_provider_combo.addItems(self.api_manager.get_available_image_providers())
        image_provider_layout.addWidget(self.image_provider_combo)
        layout.addLayout(image_provider_layout)
        
        # TTS Provider
        tts_provider_layout = QHBoxLayout()
        tts_provider_layout.addWidget(QLabel("Text-to-Speech:"))
        self.tts_provider_combo = QComboBox()
        self.tts_provider_combo.addItems(self.api_manager.get_available_tts_providers())
        tts_provider_layout.addWidget(self.tts_provider_combo)
        layout.addLayout(tts_provider_layout)
        
        # Video settings
        layout.addWidget(QLabel("🎬 Cài đặt Video:"))
        
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(QLabel("Độ phân giải:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["1920x1080", "1280x720", "1080x1080"])
        resolution_layout.addWidget(self.resolution_combo)
        layout.addLayout(resolution_layout)
        
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setRange(15, 60)
        self.fps_spinbox.setValue(25)
        fps_layout.addWidget(self.fps_spinbox)
        layout.addLayout(fps_layout)
        
        # Nút actions
        settings_actions_layout = QHBoxLayout()
        
        save_settings_btn = QPushButton("💾 Lưu cài đặt")
        save_settings_btn.clicked.connect(self.save_settings)
        settings_actions_layout.addWidget(save_settings_btn)
        
        check_api_btn = QPushButton("🔍 Kiểm tra API")
        check_api_btn.clicked.connect(self.check_api_status)
        settings_actions_layout.addWidget(check_api_btn)
        
        refresh_providers_btn = QPushButton("🔄 Làm mới")
        refresh_providers_btn.clicked.connect(self.refresh_providers)
        settings_actions_layout.addWidget(refresh_providers_btn)
        
        layout.addLayout(settings_actions_layout)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Cài đặt")
        
        # Load cài đặt hiện tại từ file config.env
        self.load_current_settings()
    
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
        self.generate_btn.setEnabled(False)
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
        self.progress_bar.setValue(step)
        self.status_label.setText(message)
    
    def generation_finished(self, result):
        """Hoàn thành tạo video"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result["success"]:
            self.status_label.setText(f"Hoàn thành! Video: {result['final_video_path']}")
            QMessageBox.information(self, "Thành công", 
                                  f"Video đã được tạo thành công!\nProject: {result['project_id']}\nĐường dẫn: {result['final_video_path']}")
            self.refresh_projects()
        else:
            self.status_label.setText(f"Lỗi: {result['error']}")
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
    
    def generate_story_only(self):
        """Chỉ tạo câu chuyện/kịch bản từ prompt"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập prompt!")
            return
        
        # Disable nút để tránh spam
        self.generate_story_btn.setEnabled(False)
        self.status_label.setText("Đang tạo câu chuyện...")
        
        try:
            # Lấy provider được chọn
            content_provider = self.content_provider_combo.currentText()
            
            # Tạo câu chuyện
            result = self.pipeline.content_gen.generate_script_from_prompt(prompt, provider=content_provider)
            
            if "error" in result:
                QMessageBox.critical(self, "Lỗi", f"Không thể tạo câu chuyện:\n{result['error']}")
                self.status_label.setText("Lỗi tạo câu chuyện")
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
                self.status_label.setText("Đã tạo câu chuyện thành công!")
                
                # Hiển thị preview ngay trong ứng dụng
                preview_text = ""
                for i, segment in enumerate(result["segments"], 1):
                    preview_text += f"ĐOẠN {i}: {segment['narration']}\n"
                self.content_preview.setPlainText(preview_text)
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định:\n{str(e)}")
            self.status_label.setText("Lỗi tạo câu chuyện")
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
            self.status_label.setText(f"Đã chọn thư mục: {folder_path}")
    
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
            self.status_label.setText("Đang tạo audio...")
            
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
                    self.status_label.setText("Đã tạo audio thành công!")
                    
                else:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi tạo audio:\n{result.get('error', 'Unknown error')}")
                    self.status_label.setText("Lỗi tạo audio")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định:\n{str(e)}")
                self.status_label.setText("Lỗi tạo audio")
            finally:
                self.generate_audio_btn.setEnabled(True)
                self.generate_audio_btn.setText("🎵 Tạo Audio")
    
    def open_audio_folder(self):
        """Mở thư mục chứa audio đã tạo"""
        if self.last_audio_output_dir and os.path.exists(self.last_audio_output_dir):
            # Open folder in file explorer (Windows)
            subprocess.Popen(['explorer', self.last_audio_output_dir])
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy thư mục audio!")
    
    def play_final_audio(self):
        """Phát audio hoàn chỉnh"""
        if self.last_final_audio_path and os.path.exists(self.last_final_audio_path):
            # Play audio file (Windows)
            os.system(f'start "" "{self.last_final_audio_path}"')
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
        self.status_label.setText("Đang tạo audio...")
        
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
                self.status_label.setText("Đã tạo audio thành công!")
                
            else:
                QMessageBox.critical(self, "Lỗi", f"Lỗi tạo audio:\n{result.get('error', 'Unknown error')}")
                self.status_label.setText("Lỗi tạo audio")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định:\n{str(e)}")
            self.status_label.setText("Lỗi tạo audio")
        finally:
            self.generate_audio_btn.setEnabled(True)
            self.generate_audio_btn.setText("🎵 Tạo Audio") 