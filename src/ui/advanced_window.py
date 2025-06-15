from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTabWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
                               QProgressBar, QListWidget, QComboBox, QSpinBox, 
                               QCheckBox, QFileDialog, QMessageBox, QScrollArea)
from PySide6.QtCore import QThread, Signal
import sys
import os

# Import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.video_pipeline import VideoPipeline
from video.effects_presets import EffectsPresets
from ai.prompt_templates import PromptTemplates
from core.api_manager import APIManager

class VideoGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, prompt, project_name, effects, use_custom_images=False, custom_images_folder=None):
        super().__init__()
        self.prompt = prompt
        self.project_name = project_name
        self.effects = effects
        self.use_custom_images = use_custom_images
        self.custom_images_folder = custom_images_folder
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
                self.prompt, self.project_name, self.effects, progress_callback
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
        
        # Nút tạo video
        self.generate_btn = QPushButton("Tạo video")
        self.generate_btn.clicked.connect(self.start_video_generation)
        layout.addWidget(self.generate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
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
        
        # Tạo thread
        self.generation_thread = VideoGenerationThread(
            prompt, project_name, effects, use_custom_images, custom_images_folder
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
        # TODO: Lưu API keys và settings vào file config
        QMessageBox.information(self, "Thông báo", "Cài đặt đã được lưu!")
    
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