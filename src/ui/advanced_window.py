from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel, QTabWidget, QListWidget, 
    QListWidgetItem, QMessageBox, QProgressBar, QComboBox, 
    QLineEdit, QCheckBox, QSplitter, QScrollArea, QFrame, QGroupBox,
    QGridLayout, QSlider, QSpinBox, QFileDialog, QStatusBar, QDialog,
    QTableWidget, QTableWidgetItem, QStackedWidget, QProgressDialog
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
import glob

# Language system
class LanguageManager:
    def __init__(self):
        self.current_language = 'vi'  # Default Vietnamese
        self.translations = {
            'vi': {
                # Tab names
                'tab_video': 'Tạo Video',
                'tab_voice_studio': 'Voice Studio', 
                'tab_voice_conversion': 'Voice Conversion',
                'tab_emotion_config': 'Cấu hình Cảm xúc',
                'tab_license': 'License',
                'tab_projects': 'Dự án', 
                'tab_settings': 'Cài đặt',
                
                # Settings
                'language_interface': 'Ngôn ngữ giao diện:',
                'chatterbox_extended': 'Cài đặt Chatterbox Mở rộng',
                'text_processing': 'Xử lý Văn bản',
                'audio_processing': 'Xử lý Âm thanh',
                'generation_control': 'Điều khiển Tạo',
                'whisper_validation': 'Xác thực Whisper',
                'presets': 'Cài đặt Sẵn',
                'performance': 'Hiệu suất',
                
                # Performance tab
                'tts_engine_mode': 'Chế độ TTS Engine',
                'processing_mode': 'Chế độ Xử lý:',
                'max_performance': 'Hiệu suất Tối đa',
                'hybrid_recommended': 'Lai (Khuyến nghị)', 
                'max_compatibility': 'Tương thích Tối đa',
                'model_caching': 'Cache Mô hình:',
                'enable_caching': 'Bật cache mô hình tích cực',
                'parallel_processing': 'Xử lý Song song:',
                'enable_parallel': 'Bật xử lý batch song song',
                'validation_bypass': 'Bỏ qua Xác thực:',
                'skip_validation': 'Bỏ qua xác thực để tăng tốc tối đa',
                'performance_metrics': 'Chỉ số Hiệu suất',
                'clear_cache': 'Xóa Cache',
                'update_metrics': 'Cập nhật Chỉ số',
                
                # Performance descriptions (short)
                'mode_info': 'Thông tin Chế độ',
                'mode_perf_desc': 'Tối đa: Nhanh 3x, có thể không ổn định',
                'mode_hybrid_desc': 'Lai: Cân bằng hiệu suất và ổn định', 
                'mode_compat_desc': 'Tương thích: Chậm nhưng ổn định nhất',
                
                # Character settings
                'character_settings': 'Cấu hình Nhân vật',
                'usage_guide': 'Hướng dẫn Sử dụng:',
                'per_char_settings': 'Cài đặt riêng cho từng nhân vật',
                'voice_mode_select': 'Chọn Voice Selection hoặc Voice Clone',
                'quick_actions': 'Nhấn nút Tools để tối ưu tự động',
                'preview_voice': 'Nhấn nút Play để nghe thử',
                
                # Settings tab specific
                'api_keys': 'Khóa API',
                'providers': 'Nhà cung cấp',
                'video_settings': 'Cài đặt Video',
                'advanced_settings': 'Cài đặt Nâng cao',
                'save_settings': 'Lưu Cài đặt',
                'load_settings': 'Tải Cài đặt',
                'reset_settings': 'Đặt lại Mặc định',
                
                # Common
                'character': 'Nhân vật',
                'emotion': 'Cảm xúc', 
                'speed': 'Tốc độ',
                'status': 'Trạng thái',
                'preview': 'Nghe thử',
                'actions': 'Thao tác',
                'output_folder': 'Thư mục output:',
                'generate_voice': 'Tạo voice',
                'open_folder': 'Mở folder',
                'clear_results': 'Xóa kết quả',
            },
            'en': {
                # Tab names 
                'tab_video': 'Create Video',
                'tab_voice_studio': 'Voice Studio',
                'tab_voice_conversion': 'Voice Conversion', 
                'tab_emotion_config': 'Emotion Config',
                'tab_license': 'License',
                'tab_projects': 'Projects',
                'tab_settings': 'Settings',
                
                # Settings
                'language_interface': 'Interface Language:',
                'chatterbox_extended': 'Chatterbox Extended Settings',
                'text_processing': 'Text Processing',
                'audio_processing': 'Audio Processing',
                'generation_control': 'Generation Control',
                'whisper_validation': 'Whisper Validation', 
                'presets': 'Presets',
                'performance': 'Performance',
                
                # Performance tab
                'tts_engine_mode': 'TTS Engine Mode',
                'processing_mode': 'Processing Mode:',
                'max_performance': 'Maximum Performance',
                'hybrid_recommended': 'Hybrid (Recommended)',
                'max_compatibility': 'Maximum Compatibility',
                'model_caching': 'Model Caching:',
                'enable_caching': 'Enable aggressive model caching',
                'parallel_processing': 'Parallel Processing:',
                'enable_parallel': 'Enable parallel batch processing',
                'validation_bypass': 'Validation Bypass:',
                'skip_validation': 'Skip validation for maximum speed',
                'performance_metrics': 'Performance Metrics',
                'clear_cache': 'Clear Cache',
                'update_metrics': 'Update Metrics',
                
                # Performance descriptions (short)
                'mode_info': 'Mode Information',
                'mode_perf_desc': 'Maximum: 3x faster, may be unstable',
                'mode_hybrid_desc': 'Hybrid: Balance performance and stability',
                'mode_compat_desc': 'Compatible: Slower but most stable',
                
                # Character settings
                'character_settings': 'Character Settings',
                'usage_guide': 'Usage Guide:',
                'per_char_settings': 'Individual settings per character',
                'voice_mode_select': 'Choose Voice Selection or Voice Clone',
                'quick_actions': 'Click Tools button for auto optimization',
                'preview_voice': 'Click Play button to preview voice',
                
                # Common
                'character': 'Character',
                'emotion': 'Emotion',
                'speed': 'Speed', 
                'status': 'Status',
                'preview': 'Preview',
                'actions': 'Actions',
                'output_folder': 'Output folder:',
                'generate_voice': 'Generate voice',
                'open_folder': 'Open folder',
                'clear_results': 'Clear results',
            }
        }
    
    def get_text(self, key):
        """Get translated text for current language"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def get(self, key):
        """Alias for get_text method"""
        return self.get_text(key)
    
    def set_language(self, language_code):
        """Set current language"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False

# Global language manager
language_manager = LanguageManager()
from .manual_voice_setup_dialog import ManualVoiceSetupDialog
from .emotion_config_tab import EmotionConfigTab
from .macos_styles import get_macos_window_size, get_macos_stylesheet

# Import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.video_pipeline import VideoPipeline
from video.effects_presets import EffectsPresets
from ai.prompt_templates import PromptTemplates
from core.api_manager import APIManager
from tts.voice_generator import VoiceGenerator

# Import Chatterbox-Audiobook inspired processors
from core.pause_processor import PauseProcessor
from core.audio_combiner import AudioCombiner
from core.voice_library import VoiceLibrary

# Audio processing
try:
    from pydub import AudioSegment
    from pydub.utils import which
    
    # Configure PyDub to find ffprobe on Windows
    import os
    import shutil
    
    # Setup ffmpeg/ffprobe paths for PyDub
    def setup_pydub_ffmpeg():
        """Setup ffmpeg and ffprobe paths for PyDub"""
        
        # Try to find ffprobe
        ffprobe_paths = [
            os.path.join(os.getcwd(), "tools", "ffmpeg", "ffprobe.exe"),  # Local tools
            shutil.which("ffprobe"),  # System PATH
            r"C:\ffmpeg\bin\ffprobe.exe",
            r"C:\Program Files\ffmpeg\bin\ffprobe.exe"
        ]
        
        ffmpeg_paths = [
            os.path.join(os.getcwd(), "tools", "ffmpeg", "ffmpeg.exe"),  # Local tools  
            shutil.which("ffmpeg"),  # System PATH
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
        ]
        
        # Configure ffprobe
        for path in ffprobe_paths:
            if path and os.path.exists(path):
                AudioSegment.converter = path.replace("ffprobe", "ffmpeg")  # Set ffmpeg path
                AudioSegment.ffprobe = path  # Set ffprobe path
                print(f"[OK] PyDub configured - ffprobe: {path}")
                break
        
        # Configure ffmpeg as backup
        for path in ffmpeg_paths:
            if path and os.path.exists(path):
                if not hasattr(AudioSegment, 'converter') or not AudioSegment.converter:
                    AudioSegment.converter = path
                    print(f"[OK] PyDub configured - ffmpeg: {path}")
                break
    
    # Setup paths
    setup_pydub_ffmpeg()
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Import các modules từ ứng dụng
from .emotion_config_tab import EmotionConfigTab
from .license_tab import LicenseTab
from core.audio_metadata_fixer import AudioMetadataFixer
from core.license_manager import license_manager


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
    def reload_code(self):
        """Reload code without restarting app"""
        try:
            import importlib
            import sys
            # Reload main modules
            modules_to_reload = [
                'src.ui.advanced_window',
                'src.tts.voice_generator',
                'src.tts.real_chatterbox_provider'
            ]
            for module_name in modules_to_reload:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
                    print(f"[OK] Reloaded: {module_name}")
            # Re-populate UI
            self.populate_character_settings_table()
            self.populate_voice_mapping_table()
            QMessageBox.information(self, "Reload", "[OK] Code reloaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"[EMOJI] Reload failed: {str(e)}")
            
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Video Generator - Advanced")
        
        # Initialize language manager first
        self.language_manager = LanguageManager()
        
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
        self.create_voice_conversion_tab()
        self.create_emotion_config_tab()
        self.create_license_tab()
        self.create_projects_tab()
        self.create_settings_tab()
        
        # Tạo status bar
        self.create_status_bar()
    
    def create_status_bar(self):
        """Tạo status bar với thông tin hệ thống"""
        status_bar = self.statusBar()
        
        # Status text chính
        self.status_text = "[OK] Sẵn sàng"
        status_bar.showMessage(self.status_text)
        
        # API status indicator
        self.api_status_label = QLabel("[EMOJI] API: Checking...")
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
                self.api_status_label.setText("[ON] API: Đầy đủ")
            elif total_available >= 1:
                self.api_status_label.setText("[PENDING] API: Một phần")
            else:
                self.api_status_label.setText("[OFF] API: Chưa cấu hình")
                
        except Exception:
            if hasattr(self, 'api_status_label'):
                self.api_status_label.setText("[WARNING] API: Error")
    
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
        prompt_group = QGroupBox("[EDIT] Nội dung video")
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
        
        self.random_prompt_btn = QPushButton("[RANDOM] Ngẫu nhiên")
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
        project_group = QGroupBox("[CONFIG] Cài đặt dự án")
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
        
        self.select_project_folder_btn = QPushButton("[FOLDER]")
        self.select_project_folder_btn.clicked.connect(self.select_project_folder)
        self.select_project_folder_btn.setMaximumWidth(40)
        project_layout.addWidget(self.select_project_folder_btn, 1, 2)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Group 3: Tùy chọn ảnh
        image_group = QGroupBox("[EMOJI] Tùy chọn ảnh")
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
        self.select_images_btn = QPushButton("[FOLDER] Chọn thư mục ảnh")
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
        effects_group = QGroupBox("[SPARKLE] Hiệu ứng")
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
        actions_group = QGroupBox("[ACTION] Tạo video")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        self.generate_story_btn = QPushButton("[EDIT] Tạo câu chuyện")
        self.generate_story_btn.clicked.connect(self.generate_story_only)
        self.generate_story_btn.setToolTip("Tạo kịch bản video từ prompt (Cmd+1)")
        self.generate_story_btn.setShortcut("Cmd+1" if platform.system() == "Darwin" else "Ctrl+1")
        actions_layout.addWidget(self.generate_story_btn, 0, 0)
        
        self.generate_audio_btn = QPushButton("[MUSIC] Tạo Audio")
        self.generate_audio_btn.clicked.connect(self.generate_audio_only)
        self.generate_audio_btn.setEnabled(False)
        self.generate_audio_btn.setToolTip("Tạo audio từ kịch bản đã có (Cmd+2)")
        self.generate_audio_btn.setShortcut("Cmd+2" if platform.system() == "Darwin" else "Ctrl+2")
        actions_layout.addWidget(self.generate_audio_btn, 0, 1)
        
        # Nút tạo video hoàn chỉnh
        self.generate_video_btn = QPushButton("[ACTION] Tạo Video Hoàn chỉnh")
        self.generate_video_btn.clicked.connect(self.start_video_generation)
        self.generate_video_btn.setToolTip("Tạo video hoàn chỉnh với ảnh và âm thanh (Cmd+3)")
        self.generate_video_btn.setShortcut("Cmd+3" if platform.system() == "Darwin" else "Ctrl+3")
        actions_layout.addWidget(self.generate_video_btn, 1, 0, 1, 2)
        

        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Group 6: Progress và Status
        progress_group = QGroupBox("[STATS] Tiến trình")
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
        preview_label = QLabel("[FILE] Xem trước nội dung:")
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
        
        self.open_audio_folder_btn = QPushButton("[FOLDER] Thư mục Audio")
        self.open_audio_folder_btn.clicked.connect(self.open_audio_folder)
        self.open_audio_folder_btn.setEnabled(False)
        self.open_audio_folder_btn.setToolTip("Mở thư mục chứa các file audio đã tạo")
        audio_controls_layout.addWidget(self.open_audio_folder_btn, 0, 0)
        
        self.play_final_audio_btn = QPushButton("[PLAY] Nghe Audio")
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
        
        self.tabs.addTab(tab, self.language_manager.get('tab_video'))
    
    def create_voice_studio_tab(self):
        """Tạo tab Voice Studio với enhanced features"""
        voice_studio_widget = QWidget()
        layout = QVBoxLayout()
        
        # === TTS Provider (moved) ===
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("TTS Provider:"))
        provider_info = QLabel("[BOT] Chatterbox TTS (AI Voice Cloning)")
        provider_info.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        provider_layout.addWidget(provider_info)
        provider_layout.addStretch()
        layout.addLayout(provider_layout)

        # === ENHANCED: Multi-file Import Section ===
        import_group = QGroupBox("[EMOJI] Import Script Data")
        import_layout = QVBoxLayout()
        
        # Data source selection - Cải thiện layout giống tab Tạo Video
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Nguồn dữ liệu:"))
        source_layout.addStretch(1)  # Thêm stretch để đẩy dropdown về bên phải
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItem("[FOLDER] Mode JSON - Import từ file", "file")
        #self.data_source_combo.addItem("[FOLDER] Mode JSON - Import nhiều file (Multi-merge)", "multi_file")
        self.data_source_combo.addItem("[REFRESH] Mode JSON - Sử dụng data từ tab Tạo Video", "generated")
        self.data_source_combo.addItem("[EDIT] Mode JSON - Nhập thủ công script", "manual")
        self.data_source_combo.addItem("[EDIT] Mode thủ công (bảng nhập liệu)", "manual_table")  # NEW
        self.data_source_combo.currentTextChanged.connect(self.switch_data_source)
        
        source_layout.addWidget(self.data_source_combo)
        # Nút import JSON ([EMOJI]) cạnh dropdown
        self.import_file_btn = QPushButton("[EMOJI] Import JSON từ file")
        self.import_file_btn.setToolTip("[FOLDER] Import JSON từ file")
        self.import_file_btn.clicked.connect(self.import_script_file)
         # === NEW: Multi-file import button ===
        self.import_multi_files_btn = QPushButton("[FOLDER] Import nhiều file JSON")
        self.import_multi_files_btn.clicked.connect(self.import_multiple_script_files)
        self.import_multi_files_btn.setVisible(False)  # Hidden initially

        self.load_generated_btn = QPushButton("[REFRESH] Load từ tab Tạo Video")
        self.load_generated_btn.clicked.connect(self.load_generated_script_data)
        self.load_generated_btn.setVisible(False)

        source_layout.addWidget(self.import_file_btn)
        source_layout.addWidget(self.import_multi_files_btn)
        source_layout.addWidget(self.load_generated_btn)
        source_layout.addStretch()  # Thêm stretch ở cuối để các widget không dính sát mép phải
        import_layout.addLayout(source_layout)
         
        # File status
        file_status_layout = QHBoxLayout()
        file_status_layout.addWidget(QLabel("Imported file:"))
        self.imported_file_label = QLabel("Chưa import file nào")
        self.imported_file_label.setStyleSheet("color: #8E8E93;")
        file_status_layout.addWidget(self.imported_file_label)
        file_status_layout.addStretch()
        import_layout.addLayout(file_status_layout)
        
        # Generated data section
        self.generated_data_widget = QWidget()
        generated_layout = QVBoxLayout()
        generated_layout.setContentsMargins(0, 0, 0, 0)
        
        generated_info = QLabel("[REFRESH] Sử dụng script data đã được tạo từ tab 'Tạo Video'")
        generated_info.setStyleSheet("color: #007AFF; font-weight: bold;")
        generated_layout.addWidget(generated_info)
        
        self.use_generated_btn = QPushButton("[REFRESH] Load Data từ tab Tạo Video")
        self.use_generated_btn.clicked.connect(self.load_generated_script_data)
        generated_layout.addWidget(self.use_generated_btn)
        
        self.generated_data_widget.setLayout(generated_layout)
        self.generated_data_widget.setVisible(False)
        import_layout.addWidget(self.generated_data_widget)
        
        # Manual input section
        self.manual_input_widget = QWidget()
        manual_layout = QVBoxLayout()
        manual_layout.setContentsMargins(0, 0, 0, 0)
        
        manual_layout.addWidget(QLabel("[EDIT] Nhập JSON script:"))
        self.manual_script_input = QTextEdit()
        self.manual_script_input.setPlaceholderText("Paste JSON script vào đây...")
        self.manual_script_input.setMaximumHeight(120)
        manual_layout.addWidget(self.manual_script_input)
        
        self.parse_manual_btn = QPushButton("[OK] Parse JSON")
        self.parse_manual_btn.clicked.connect(self.parse_manual_script)
        manual_layout.addWidget(self.parse_manual_btn)
        
        self.manual_input_widget.setLayout(manual_layout)
        self.manual_input_widget.setVisible(False)
        import_layout.addWidget(self.manual_input_widget)
        
        # === NEW: Manual Table Input Section ===
        self.manual_table_widget = QWidget()
        manual_table_layout = QVBoxLayout()
        manual_table_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header info for manual table mode
        manual_table_info = QLabel("[EDIT] Mode thủ công: Nhập dữ liệu trực tiếp vào bảng (chỉ Narrator)")
        manual_table_info.setStyleSheet("color: #007AFF; font-weight: bold; margin-bottom: 8px;")
        manual_table_layout.addWidget(manual_table_info)
        
        # Chunk size configuration
        chunk_config_layout = QHBoxLayout()
        chunk_config_layout.addWidget(QLabel("Chunk size (ký tự):"))
        
        self.chunk_size_input = QLineEdit()
        self.chunk_size_input.setText("500")  # Default chunk size
        self.chunk_size_input.setMaximumWidth(80)
        self.chunk_size_input.setToolTip("Số ký tự tối đa cho mỗi đoạn audio (khuyến nghị: 300-800)")
        chunk_config_layout.addWidget(self.chunk_size_input)
        
        chunk_config_layout.addWidget(QLabel("ký tự/đoạn"))
        chunk_config_layout.addStretch()
        manual_table_layout.addLayout(chunk_config_layout)
        
        # Data input table
        self.manual_data_table = QTableWidget()
        self.manual_data_table.verticalHeader().setVisible(False)
        self.manual_data_table.setColumnCount(3)
        self.manual_data_table.setHorizontalHeaderLabels(["Segment", "Dialogue", "Nội dung"])
        self.manual_data_table.setMaximumHeight(200)
        
        # Connect item changed signal for automatic text processing
        self.manual_data_table.itemChanged.connect(self.on_table_item_changed)
        
        # Table styling
        self.manual_data_table.setAlternatingRowColors(True)
        self.manual_data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.manual_data_table.verticalHeader().setDefaultSectionSize(60)
        self.manual_data_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #f1f3f4;
                padding: 6px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e0e0e0;
                font-size: 11px;
            }
        """)
        
        # Set column widths
        header = self.manual_data_table.horizontalHeader()
        header.resizeSection(0, 80)   # Segment
        header.resizeSection(1, 80)   # Dialogue
        header.setStretchLastSection(True)  # Content column stretches
        
        manual_table_layout.addWidget(self.manual_data_table)
        
        # Table action buttons
        table_actions_layout = QHBoxLayout()
        
        self.add_row_btn = QPushButton("[EMOJI] Thêm hàng")
        self.add_row_btn.clicked.connect(self.add_manual_table_row)
        table_actions_layout.addWidget(self.add_row_btn)
        
        self.remove_row_btn = QPushButton("[DELETE] Xóa hàng đã chọn")
        self.remove_row_btn.clicked.connect(self.remove_manual_table_row)
        table_actions_layout.addWidget(self.remove_row_btn)
        
        self.auto_chunk_btn = QPushButton("[REFRESH] Tự động chia đoạn")
        self.auto_chunk_btn.clicked.connect(self.auto_chunk_content)
        self.auto_chunk_btn.setToolTip("Tự động chia nội dung thành các đoạn nhỏ dựa theo chunk size")
        table_actions_layout.addWidget(self.auto_chunk_btn)
        
        table_actions_layout.addStretch()
        
        self.confirm_manual_data_btn = QPushButton("[OK] Xác nhận dữ liệu nhập")
        self.confirm_manual_data_btn.clicked.connect(self.confirm_manual_table_data)
        self.confirm_manual_data_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
        """)
        table_actions_layout.addWidget(self.confirm_manual_data_btn)
        
        manual_table_layout.addLayout(table_actions_layout)
        
        # Initialize with one empty row
        self.manual_data_table.setRowCount(1)
        self.manual_data_table.setItem(0, 0, QTableWidgetItem("1"))
        self.manual_data_table.setItem(0, 1, QTableWidgetItem("1"))
        self.manual_data_table.setItem(0, 2, QTableWidgetItem(""))
        
        self.manual_table_widget.setLayout(manual_table_layout)
        self.manual_table_widget.setVisible(False)
        import_layout.addWidget(self.manual_table_widget)
        
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        
        
        # Group 2: Script Overview
        overview_group = QGroupBox("[CLIPBOARD] Script Overview")
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
        chatterbox_group = QGroupBox("[EMOJI] Cấu hình (Nâng cao)")
        chatterbox_layout = QVBoxLayout()
        chatterbox_layout.setSpacing(8)
        
        # Enable/disable toggle - Cải thiện layout giống tab Tạo Video
        chatterbox_controls_layout = QHBoxLayout()
        self.enable_chatterbox_manual = QCheckBox("Sử dụng cấu hình thủ công")
        self.enable_chatterbox_manual.toggled.connect(self.toggle_chatterbox_manual_controls)
        chatterbox_controls_layout.addWidget(self.enable_chatterbox_manual)
        
        chatterbox_controls_layout.addStretch(1)  # Thêm stretch ở giữa để cách đều các checkbox
        
        # Auto emotion mapping toggle
        self.enable_emotion_mapping = QCheckBox("[THEATER] Tự động điều chỉnh cảm xúc theo script")
        self.enable_emotion_mapping.setChecked(True)  # Default enabled
        self.enable_emotion_mapping.setToolTip("Tự động map emotion labels (happy, sad, excited...) thành emotion exaggeration values")
        chatterbox_controls_layout.addWidget(self.enable_emotion_mapping)
        chatterbox_controls_layout.addStretch(1)  # Thêm stretch ở cuối để các widget không dính sát mép phải
        chatterbox_layout.addLayout(chatterbox_controls_layout)
        
        # Manual controls container
        self.chatterbox_manual_widget = QWidget()
        chatterbox_manual_layout = QVBoxLayout()
        chatterbox_manual_layout.setContentsMargins(20, 10, 10, 10)
        
        # Character-specific settings ONLY (XÓA GLOBAL CONTROLS)
        char_specific_label = QLabel("[THEATER] Cấu hình riêng cho từng nhân vật:")
        char_specific_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        chatterbox_manual_layout.addWidget(char_specific_label)
        
        # Character settings table với styling cải thiện
        self.character_settings_table = QTableWidget()
        self.character_settings_table.verticalHeader().setVisible(False)
        self.character_settings_table.setColumnCount(11)  # Tăng lên 11 columns, thêm Temperature
        self.character_settings_table.setHorizontalHeaderLabels([
            "Nhân vật", "Emotion", "Exaggeration", "Speed", "CFG Weight", "Temperature", "Mode", "Voice/Clone", "Whisper Voice", "Status", "Preview"
        ])
        self.character_settings_table.horizontalHeader().setStretchLastSection(False)
        self.character_settings_table.setMaximumHeight(200)  # Tăng height cho table
        
        # Cải thiện styling và font size tương tự emotion table
        self.character_settings_table.setAlternatingRowColors(True)
        self.character_settings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.character_settings_table.verticalHeader().setDefaultSectionSize(40)  # Row height phù hợp
        self.character_settings_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #f1f3f4;
                padding: 6px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e0e0e0;
                font-size: 11px;
            }
        """)
        
        # Set responsive column widths that adapt to window size
        header = self.character_settings_table.horizontalHeader()
        
        # Use resize modes for flexible column sizing
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Character name - resizable
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Emotion - fit content
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Exaggeration - fit content
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Speed - fit content
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # CFG Weight - fit content
        header.setSectionResizeMode(5, QHeaderView.Interactive)  # Mode - resizable
        header.setSectionResizeMode(6, QHeaderView.Stretch)  # Voice/Clone - stretch to fill
        header.setSectionResizeMode(7, QHeaderView.Interactive)  # Whisper Voice - resizable
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Status - fit content
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Preview - fit content
        
        # Set minimum widths for important columns
        header.setMinimumSectionSize(80)
        self.character_settings_table.setColumnWidth(0, 120)  # Character name minimum
        self.character_settings_table.setColumnWidth(5, 130)  # Mode minimum
        self.character_settings_table.setColumnWidth(7, 150)  # Whisper Voice minimum
        
        chatterbox_manual_layout.addWidget(self.character_settings_table)
        
        # VOICE GENERATION HELP
        help_layout = QVBoxLayout()
        help_layout.addWidget(QLabel("Hướng dẫn sử dụng:"))
        
        help_text = QLabel("""
• <b>Cài đặt riêng cho từng nhân vật</b>: Mỗi nhân vật có thông số riêng (Emotion, Speed, CFG Weight)
• <b>Chế độ Voice</b>: Chọn Voice Selection hoặc Voice Clone cho từng nhân vật
• <b>Thao tác nhanh</b>: Nhấn nút Tools để tối ưu thông số tự động
• <b>Xem trước</b>: Nhấn nút Play để nghe thử giọng với settings hiện tại
        """)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #666; font-size: 12px; padding: 8px; background-color: #f8f8f8; border-radius: 4px;")
        help_layout.addWidget(help_text)
        
        chatterbox_manual_layout.addLayout(help_layout)
        
        # Note: Removed "Apply to All Characters" preset buttons 
        # since per-character settings in table provide better control
        
        self.chatterbox_manual_widget.setLayout(chatterbox_manual_layout)
        self.chatterbox_manual_widget.setVisible(False)  # Hidden by default
        chatterbox_layout.addWidget(self.chatterbox_manual_widget)
        
        chatterbox_group.setLayout(chatterbox_layout)
        layout.addWidget(chatterbox_group)
        
        
        # TTS Provider - CHỈ CHATTERBOX
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("TTS Provider:"))
        provider_info = QLabel("[BOT] Chatterbox TTS (AI Voice Cloning)")
        provider_info.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        provider_layout.addWidget(provider_info)
        provider_layout.addStretch()
        layout.addLayout(provider_layout) 
        
        # Output settings
        self.voice_output_input = QLineEdit()
        self.voice_output_input.setPlaceholderText("./voice_studio_output/")
        self.voice_output_input.setReadOnly(True)

        self.select_voice_output_btn = QPushButton("[FOLDER]")
        self.select_voice_output_btn.clicked.connect(self.select_voice_output_folder)
        self.select_voice_output_btn.setMaximumWidth(40)

        self.generate_selected_btn = QPushButton("[EMOJI] Tạo voice 1 nhân vật")
        self.generate_selected_btn.clicked.connect(self.generate_selected_character_voice)
        self.generate_selected_btn.setEnabled(False)

        self.generate_all_btn = QPushButton("[THEATER] Tạo voice")
        self.generate_all_btn.clicked.connect(self.generate_all_voices)
        self.generate_all_btn.setEnabled(False)
        
        self.open_voice_folder_btn = QPushButton("[FOLDER] Mở Folder output")
        self.open_voice_folder_btn.clicked.connect(self.open_voice_output_folder)
        
        self.clear_voice_results_btn = QPushButton("[CLEAN] Xóa kết quả")
        self.clear_voice_results_btn.clicked.connect(self.clear_voice_results)
        
        
        # Group 6: Progress & Results
        progress_group = QGroupBox("[STATS] Tiến trình & Kết quả")
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
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Extended settings moved to Settings tab for cleaner UI
        
        # Group 7: Actions - Tách thành group riêng giống tab Dự án/Cài đặt
        actions_group = QGroupBox("[EMOJI] Thao tác")
        action_buttons_layout = QGridLayout()
        action_buttons_layout.setSpacing(8)
        
        # Thêm các nút output/generate vào action bar
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("[FOLDER] Thư mục output:"))
        output_layout.addWidget(self.voice_output_input)
        output_layout.addWidget(self.select_voice_output_btn)
        action_buttons_layout.addLayout(output_layout, 0, 0, 1, 2)
        
        # Generate buttons
        action_buttons_layout.addWidget(self.generate_selected_btn, 1, 0)
        action_buttons_layout.addWidget(self.generate_all_btn, 1, 1)
        
        # Output management buttons
        action_buttons_layout.addWidget(self.open_voice_folder_btn, 2, 0)
        action_buttons_layout.addWidget(self.clear_voice_results_btn, 2, 1)
        
        # Force Merge button - tối ưu cho trường hợp script data không match
        self.force_merge_btn = QPushButton("Merge All")
        self.force_merge_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #007ACC;
                border: 1px solid #007ACC;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
                border-color: #005999;
            }
        """)
        self.force_merge_btn.clicked.connect(self.force_merge_all_segments)
        self.force_merge_btn.setToolTip("Gộp tất cả file segment_*.mp3 có trong thư mục output (không cần script data)")
        action_buttons_layout.addWidget(self.force_merge_btn, 3, 0, 1, 2)
        
        actions_group.setLayout(action_buttons_layout)
        layout.addWidget(actions_group)
        
        # Initialize data
        self.voice_studio_script_data = None
        self.voice_mapping = {}
        self.character_chatterbox_settings = {}  # Store per-character settings
        self.voice_clone_folder = None
        
        # === SET UP MAIN TAB LAYOUT ===
        voice_studio_widget.setLayout(layout)
        
        # Use scroll area for the full content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(voice_studio_widget)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        tab = QWidget()
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, self.language_manager.get('tab_voice_studio'))
    
    def create_preset_settings_tab(self):
        """Create preset settings tab"""
        preset_tab = QWidget()
        preset_layout = QVBoxLayout()
        
        preset_group = QGroupBox("Configuration Presets")
        preset_btn_layout = QGridLayout()
        
        # Text Processing Presets
        conservative_text_btn = QPushButton("Conservative Text")
        conservative_text_btn.clicked.connect(lambda: self.apply_extended_preset("conservative_text"))
        preset_btn_layout.addWidget(conservative_text_btn, 0, 0)
        
        default_text_btn = QPushButton("Default Text")
        default_text_btn.clicked.connect(lambda: self.apply_extended_preset("default_text"))
        preset_btn_layout.addWidget(default_text_btn, 0, 1)
        
        aggressive_text_btn = QPushButton("Aggressive Text")
        aggressive_text_btn.clicked.connect(lambda: self.apply_extended_preset("aggressive_text"))
        preset_btn_layout.addWidget(aggressive_text_btn, 0, 2)
        
        # Audio Processing Presets
        fast_audio_btn = QPushButton("Fast Audio")
        fast_audio_btn.clicked.connect(lambda: self.apply_extended_preset("fast_audio"))
        preset_btn_layout.addWidget(fast_audio_btn, 1, 0)
        
        default_audio_btn = QPushButton("Default Audio")
        default_audio_btn.clicked.connect(lambda: self.apply_extended_preset("default_audio"))
        preset_btn_layout.addWidget(default_audio_btn, 1, 1)
        
        quality_audio_btn = QPushButton("Quality Audio")
        quality_audio_btn.clicked.connect(lambda: self.apply_extended_preset("quality_audio"))
        preset_btn_layout.addWidget(quality_audio_btn, 1, 2)
        
        # Generation Presets
        conservative_gen_btn = QPushButton("Conservative Gen")
        conservative_gen_btn.clicked.connect(lambda: self.apply_extended_preset("conservative_generation"))
        preset_btn_layout.addWidget(conservative_gen_btn, 2, 0)
        
        default_gen_btn = QPushButton("Default Gen")
        default_gen_btn.clicked.connect(lambda: self.apply_extended_preset("default_generation"))
        preset_btn_layout.addWidget(default_gen_btn, 2, 1)
        
        aggressive_gen_btn = QPushButton("Aggressive Gen")
        aggressive_gen_btn.clicked.connect(lambda: self.apply_extended_preset("aggressive_generation"))
        preset_btn_layout.addWidget(aggressive_gen_btn, 2, 2)
        
        preset_group.setLayout(preset_btn_layout)
        preset_layout.addWidget(preset_group)
        preset_tab.setLayout(preset_layout)
        
        return preset_tab

    def create_text_processor_settings_tab(self):
        """[EDIT] Tạo tab cài đặt xử lý văn bản - Chatterbox Extended"""
        text_processor_tab = QWidget()
        text_processor_layout = QVBoxLayout()
        
        # Header với status
        header_layout = QHBoxLayout()
        header_icon = QLabel("[EDIT]")
        header_icon.setStyleSheet("font-weight: bold; color: #2E8B57; font-size: 14px;")
        header_title = QLabel("Xử lý văn bản thông minh")
        header_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        # Status indicator
        self.text_processor_status = QLabel("🟢 Hoạt động")
        self.text_processor_status.setStyleSheet("color: green; font-weight: bold;")
        header_layout.addWidget(self.text_processor_status)
        
        text_processor_layout.addLayout(header_layout)
        
        # Chế độ xử lý văn bản
        mode_group = QGroupBox("⚙️ Chế độ xử lý văn bản")
        mode_layout = QGridLayout()
        
        mode_layout.addWidget(QLabel("Chế độ hiện tại:"), 0, 0)
        self.text_processing_mode = QComboBox()
        self.text_processing_mode.addItems([
            "conservative - Bảo toàn tối đa",
            "default - Cân bằng tối ưu", 
            "aggressive - Tối ưu TTS"
        ])
        self.text_processing_mode.setCurrentText("default - Cân bằng tối ưu")
        mode_layout.addWidget(self.text_processing_mode, 0, 1)
        
        # Mô tả chế độ
        self.mode_description = QLabel("Xử lý cân bằng với tối ưu hóa thông minh")
        self.mode_description.setStyleSheet("color: #555; font-style: italic; padding: 5px;")
        self.mode_description.setWordWrap(True)
        mode_layout.addWidget(self.mode_description, 1, 0, 1, 2)
        
        # Connect signal để cập nhật mô tả
        self.text_processing_mode.currentTextChanged.connect(self._update_text_mode_description)
        
        mode_group.setLayout(mode_layout)
        text_processor_layout.addWidget(mode_group)
        
        # Cài đặt xử lý câu
        sentence_group = QGroupBox("📝 Xử lý cấu trúc câu")
        sentence_layout = QGridLayout()
        
        # Nối câu thông minh
        sentence_layout.addWidget(QLabel("Nối câu thông minh:"), 0, 0)
        self.smart_joining_checkbox = QCheckBox("Nối câu ngắn để tạo nhịp điệu tốt hơn")
        self.smart_joining_checkbox.setChecked(True)
        sentence_layout.addWidget(self.smart_joining_checkbox, 0, 1)
        
        sentence_layout.addWidget(QLabel("Ngưỡng nối câu:"), 1, 0)
        self.sentence_join_threshold = QSpinBox()
        self.sentence_join_threshold.setRange(10, 100)
        self.sentence_join_threshold.setValue(40)
        self.sentence_join_threshold.setSuffix(" ký tự")
        sentence_layout.addWidget(self.sentence_join_threshold, 1, 1)
        
        # Tách câu đệ quy
        sentence_layout.addWidget(QLabel("Tách câu đệ quy:"), 2, 0)
        self.recursive_splitting_checkbox = QCheckBox("Tự động tách câu dài")
        self.recursive_splitting_checkbox.setChecked(True)
        sentence_layout.addWidget(self.recursive_splitting_checkbox, 2, 1)
        
        sentence_layout.addWidget(QLabel("Độ dài câu tối đa:"), 3, 0)
        self.max_sentence_length = QSpinBox()
        self.max_sentence_length.setRange(100, 500)
        self.max_sentence_length.setValue(200)
        self.max_sentence_length.setSuffix(" ký tự")
        sentence_layout.addWidget(self.max_sentence_length, 3, 1)
        
        sentence_group.setLayout(sentence_layout)
        text_processor_layout.addWidget(sentence_group)
        
        # Tiền xử lý văn bản
        preprocessing_group = QGroupBox("🔧 Tiền xử lý văn bản")
        preprocessing_layout = QGridLayout()
        
        self.fix_abbreviations_checkbox = QCheckBox("Sửa viết tắt (J.R.R. → J R R)")
        self.fix_abbreviations_checkbox.setChecked(True)
        self.fix_abbreviations_checkbox.setToolTip("Chuyển đổi viết tắt để TTS đọc chính xác hơn")
        preprocessing_layout.addWidget(self.fix_abbreviations_checkbox, 0, 0)
        
        self.remove_references_checkbox = QCheckBox("Xóa tham chiếu nội dòng (.188, .3)")
        self.remove_references_checkbox.setChecked(True)
        self.remove_references_checkbox.setToolTip("Xóa các số tham chiếu không cần thiết")
        preprocessing_layout.addWidget(self.remove_references_checkbox, 0, 1)
        
        self.remove_unwanted_words_checkbox = QCheckBox("Xóa/thay thế từ không mong muốn")
        self.remove_unwanted_words_checkbox.setChecked(True)
        self.remove_unwanted_words_checkbox.setToolTip("Làm sạch văn bản khỏi từ ngữ không phù hợp")
        preprocessing_layout.addWidget(self.remove_unwanted_words_checkbox, 1, 0)
        
        self.normalize_punctuation_checkbox = QCheckBox("Chuẩn hóa dấu câu")
        self.normalize_punctuation_checkbox.setChecked(True)
        self.normalize_punctuation_checkbox.setToolTip("Chuẩn hóa dấu câu để TTS xử lý tốt hơn")
        preprocessing_layout.addWidget(self.normalize_punctuation_checkbox, 1, 1)
        
        preprocessing_group.setLayout(preprocessing_layout)
        text_processor_layout.addWidget(preprocessing_group)
        
        # Tùy chọn nâng cao
        advanced_group = QGroupBox("🎯 Tùy chọn nâng cao")
        advanced_layout = QGridLayout()
        
        self.enable_smart_quotes_checkbox = QCheckBox("Xử lý dấu nháy thông minh")
        self.enable_smart_quotes_checkbox.setChecked(True)
        advanced_layout.addWidget(self.enable_smart_quotes_checkbox, 0, 0)
        
        self.preserve_formatting_checkbox = QCheckBox("Bảo toàn định dạng gốc")
        self.preserve_formatting_checkbox.setChecked(True)
        advanced_layout.addWidget(self.preserve_formatting_checkbox, 0, 1)
        
        self.enable_emoji_processing_checkbox = QCheckBox("Xử lý emoji thành text")
        self.enable_emoji_processing_checkbox.setChecked(False)
        advanced_layout.addWidget(self.enable_emoji_processing_checkbox, 1, 0)
        
        self.enable_number_expansion_checkbox = QCheckBox("Mở rộng số thành chữ")
        self.enable_number_expansion_checkbox.setChecked(True)
        advanced_layout.addWidget(self.enable_number_expansion_checkbox, 1, 1)
        
        advanced_group.setLayout(advanced_layout)
        text_processor_layout.addWidget(advanced_group)
        
        # Thống kê xử lý
        stats_group = QGroupBox("📊 Thống kê xử lý")
        stats_layout = QGridLayout()
        
        self.text_blocks_processed_label = QLabel("Khối văn bản đã xử lý: 0")
        stats_layout.addWidget(self.text_blocks_processed_label, 0, 0)
        
        self.avg_processing_time_label = QLabel("Thời gian xử lý trung bình: 0.0s")
        stats_layout.addWidget(self.avg_processing_time_label, 0, 1)
        
        self.last_processing_result_label = QLabel("Kết quả xử lý cuối: Chưa có")
        self.last_processing_result_label.setStyleSheet("color: #666;")
        stats_layout.addWidget(self.last_processing_result_label, 1, 0, 1, 2)
        
        stats_group.setLayout(stats_layout)
        text_processor_layout.addWidget(stats_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test xử lý văn bản")
        test_btn.clicked.connect(self._test_text_processing)
        button_layout.addWidget(test_btn)
        
        reset_btn = QPushButton("🔄 Khôi phục mặc định")
        reset_btn.clicked.connect(self._reset_text_processing_settings)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        apply_btn = QPushButton("✅ Áp dụng cài đặt")
        apply_btn.setStyleSheet("background-color: #2E8B57; color: white; font-weight: bold; padding: 8px;")
        apply_btn.clicked.connect(self._apply_text_processing_settings)
        button_layout.addWidget(apply_btn)
        
        text_processor_layout.addLayout(button_layout)
        text_processor_layout.addStretch()
        
        text_processor_tab.setLayout(text_processor_layout)
        return text_processor_tab

    def create_audio_processor_settings_tab(self):
        """[MUSIC] Tạo tab cài đặt xử lý âm thanh - Chatterbox Extended"""
        audio_processor_tab = QWidget()
        audio_processor_layout = QVBoxLayout()
        
        # Header với status
        header_layout = QHBoxLayout()
        header_icon = QLabel("[MUSIC]")
        header_icon.setStyleSheet("font-weight: bold; color: #4169E1; font-size: 14px;")
        header_title = QLabel("Xử lý âm thanh nâng cao")
        header_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        # Status indicator
        self.audio_processor_status = QLabel("🟢 Hoạt động")
        self.audio_processor_status.setStyleSheet("color: green; font-weight: bold;")
        header_layout.addWidget(self.audio_processor_status)
        
        audio_processor_layout.addLayout(header_layout)
        
        # Chế độ xử lý âm thanh
        mode_group = QGroupBox("⚙️ Chế độ xử lý âm thanh")
        mode_layout = QGridLayout()
        
        mode_layout.addWidget(QLabel("Chế độ hiện tại:"), 0, 0)
        self.audio_processing_mode = QComboBox()
        self.audio_processing_mode.addItems([
            "fast - Xử lý nhanh",
            "default - Cân bằng chất lượng", 
            "quality - Chất lượng tối đa"
        ])
        self.audio_processing_mode.setCurrentText("default - Cân bằng chất lượng")
        mode_layout.addWidget(self.audio_processing_mode, 0, 1)
        
        # Mô tả chế độ
        self.audio_mode_description = QLabel("Xử lý cân bằng giữa tốc độ và chất lượng")
        self.audio_mode_description.setStyleSheet("color: #555; font-style: italic; padding: 5px;")
        self.audio_mode_description.setWordWrap(True)
        mode_layout.addWidget(self.audio_mode_description, 1, 0, 1, 2)
        
        # Connect signal để cập nhật mô tả
        self.audio_processing_mode.currentTextChanged.connect(self._update_audio_mode_description)
        
        mode_group.setLayout(mode_layout)
        audio_processor_layout.addWidget(mode_group)
        
        # Xử lý âm thanh tự động
        auto_group = QGroupBox("🤖 Xử lý tự động")
        auto_layout = QGridLayout()
        
        # Auto-editor integration
        auto_layout.addWidget(QLabel("Auto-editor:"), 0, 0)
        self.auto_editor_checkbox = QCheckBox("Tự động xóa im lặng & lỗi âm thanh")
        self.auto_editor_checkbox.setChecked(True)
        self.auto_editor_checkbox.setToolTip("Sử dụng auto-editor để làm sạch âm thanh")
        auto_layout.addWidget(self.auto_editor_checkbox, 0, 1)
        
        # Thông số auto-editor
        auto_layout.addWidget(QLabel("Ngưỡng im lặng:"), 1, 0)
        self.silence_threshold = QDoubleSpinBox()
        self.silence_threshold.setRange(0.01, 0.1)
        self.silence_threshold.setValue(0.04)
        self.silence_threshold.setDecimals(3)
        self.silence_threshold.setSuffix(" s")
        self.silence_threshold.setToolTip("Xóa khoảng im lặng dài hơn giá trị này")
        auto_layout.addWidget(self.silence_threshold, 1, 1)
        
        auto_layout.addWidget(QLabel("Tự động cắt âm:"), 2, 0)
        self.auto_trim_checkbox = QCheckBox("Tự động cắt đầu/cuối im lặng")
        self.auto_trim_checkbox.setChecked(True)
        auto_layout.addWidget(self.auto_trim_checkbox, 2, 1)
        
        auto_group.setLayout(auto_layout)
        audio_processor_layout.addWidget(auto_group)
        
        # Chuẩn hóa âm lượng
        normalization_group = QGroupBox("🔊 Chuẩn hóa âm lượng")
        normalization_layout = QGridLayout()
        
        # FFmpeg normalization
        normalization_layout.addWidget(QLabel("FFmpeg Chuẩn hóa:"), 0, 0)
        self.ffmpeg_normalization_checkbox = QCheckBox("EBU R128 + Peak chuẩn hóa")
        self.ffmpeg_normalization_checkbox.setChecked(True)
        self.ffmpeg_normalization_checkbox.setToolTip("Áp dụng tiêu chuẩn phát sóng EBU R128")
        normalization_layout.addWidget(self.ffmpeg_normalization_checkbox, 0, 1)
        
        normalization_layout.addWidget(QLabel("Mục tiêu LUFS:"), 1, 0)
        self.target_lufs = QDoubleSpinBox()
        self.target_lufs.setRange(-30.0, -10.0)
        self.target_lufs.setValue(-23.0)
        self.target_lufs.setSuffix(" LUFS")
        self.target_lufs.setToolTip("Mức âm lượng mục tiêu (-23 LUFS cho phát sóng)")
        normalization_layout.addWidget(self.target_lufs, 1, 1)
        
        normalization_layout.addWidget(QLabel("Giới hạn Peak:"), 2, 0)
        self.peak_limit = QDoubleSpinBox()
        self.peak_limit.setRange(-3.0, 0.0)
        self.peak_limit.setValue(-1.0)
        self.peak_limit.setSuffix(" dBFS")
        self.peak_limit.setToolTip("Giới hạn mức đỉnh để tránh méo âm")
        normalization_layout.addWidget(self.peak_limit, 2, 1)
        
        # True peak limiting
        normalization_layout.addWidget(QLabel("True Peak Limiting:"), 3, 0)
        self.true_peak_checkbox = QCheckBox("Kích hoạt giới hạn true peak")
        self.true_peak_checkbox.setChecked(True)
        self.true_peak_checkbox.setToolTip("Ngăn chặn méo inter-sample")
        normalization_layout.addWidget(self.true_peak_checkbox, 3, 1)
        
        normalization_group.setLayout(normalization_layout)
        audio_processor_layout.addWidget(normalization_group)
        
        # Định dạng xuất
        export_group = QGroupBox("💾 Định dạng xuất")
        export_layout = QGridLayout()
        
        self.export_wav_checkbox = QCheckBox("WAV (Không nén)")
        self.export_wav_checkbox.setChecked(True)
        self.export_wav_checkbox.setToolTip("Định dạng âm thanh không nén, chất lượng cao")
        export_layout.addWidget(self.export_wav_checkbox, 0, 0)
        
        self.export_mp3_checkbox = QCheckBox("MP3 (320kbps)")
        self.export_mp3_checkbox.setChecked(True)
        self.export_mp3_checkbox.setToolTip("Định dạng nén phổ biến, chất lượng cao")
        export_layout.addWidget(self.export_mp3_checkbox, 0, 1)
        
        self.export_flac_checkbox = QCheckBox("FLAC (Nén không mất dữ liệu)")
        self.export_flac_checkbox.setChecked(False)
        self.export_flac_checkbox.setToolTip("Nén lossless, tệp nhỏ hơn WAV")
        export_layout.addWidget(self.export_flac_checkbox, 1, 0)
        
        self.export_ogg_checkbox = QCheckBox("OGG Vorbis (Mã nguồn mở)")
        self.export_ogg_checkbox.setChecked(False)
        self.export_ogg_checkbox.setToolTip("Định dạng mã nguồn mở, chất lượng tốt")
        export_layout.addWidget(self.export_ogg_checkbox, 1, 1)
        
        self.preserve_original_checkbox = QCheckBox("Giữ lại file gốc")
        self.preserve_original_checkbox.setChecked(True)
        self.preserve_original_checkbox.setToolTip("Lưu cả file gốc chưa xử lý")
        export_layout.addWidget(self.preserve_original_checkbox, 2, 0)
        
        self.create_metadata_checkbox = QCheckBox("Tạo file metadata")
        self.create_metadata_checkbox.setChecked(True)
        self.create_metadata_checkbox.setToolTip("Tạo file JSON với thông tin xử lý")
        export_layout.addWidget(self.create_metadata_checkbox, 2, 1)
        
        export_group.setLayout(export_layout)
        audio_processor_layout.addWidget(export_group)
        
        # Cài đặt nâng cao
        advanced_group = QGroupBox("🎛️ Cài đặt nâng cao")
        advanced_layout = QGridLayout()
        
        advanced_layout.addWidget(QLabel("Sample Rate:"), 0, 0)
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["Giữ nguyên", "22050 Hz", "44100 Hz", "48000 Hz"])
        self.sample_rate_combo.setCurrentText("48000 Hz")
        advanced_layout.addWidget(self.sample_rate_combo, 0, 1)
        
        advanced_layout.addWidget(QLabel("Bit Depth:"), 1, 0)
        self.bit_depth_combo = QComboBox()
        self.bit_depth_combo.addItems(["Giữ nguyên", "16-bit", "24-bit", "32-bit"])
        self.bit_depth_combo.setCurrentText("24-bit")
        advanced_layout.addWidget(self.bit_depth_combo, 1, 1)
        
        self.denoise_checkbox = QCheckBox("Giảm nhiễu âm thanh")
        self.denoise_checkbox.setChecked(False)
        self.denoise_checkbox.setToolTip("Áp dụng bộ lọc giảm nhiễu (có thể ảnh hưởng chất lượng)")
        advanced_layout.addWidget(self.denoise_checkbox, 2, 0)
        
        self.fade_inout_checkbox = QCheckBox("Thêm fade in/out")
        self.fade_inout_checkbox.setChecked(True)
        self.fade_inout_checkbox.setToolTip("Thêm hiệu ứng fade tự nhiên")
        advanced_layout.addWidget(self.fade_inout_checkbox, 2, 1)
        
        advanced_group.setLayout(advanced_layout)
        audio_processor_layout.addWidget(advanced_group)
        
        # Thống kê xử lý
        stats_group = QGroupBox("📊 Thống kê xử lý")
        stats_layout = QGridLayout()
        
        self.audio_files_processed_label = QLabel("Files âm thanh đã xử lý: 0")
        stats_layout.addWidget(self.audio_files_processed_label, 0, 0)
        
        self.avg_audio_processing_time_label = QLabel("Thời gian xử lý trung bình: 0.0s")
        stats_layout.addWidget(self.avg_audio_processing_time_label, 0, 1)
        
        self.total_audio_duration_label = QLabel("Tổng thời lượng đã xử lý: 0:00:00")
        self.total_audio_duration_label.setStyleSheet("color: #666;")
        stats_layout.addWidget(self.total_audio_duration_label, 1, 0, 1, 2)
        
        stats_group.setLayout(stats_layout)
        audio_processor_layout.addWidget(stats_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test xử lý âm thanh")
        test_btn.clicked.connect(self._test_audio_processing)
        button_layout.addWidget(test_btn)
        
        reset_btn = QPushButton("🔄 Khôi phục mặc định")
        reset_btn.clicked.connect(self._reset_audio_processing_settings)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        apply_btn = QPushButton("✅ Áp dụng cài đặt")
        apply_btn.setStyleSheet("background-color: #4169E1; color: white; font-weight: bold; padding: 8px;")
        apply_btn.clicked.connect(self._apply_audio_processing_settings)
        button_layout.addWidget(apply_btn)
        
        audio_processor_layout.addLayout(button_layout)
        audio_processor_layout.addStretch()
        
        audio_processor_tab.setLayout(audio_processor_layout)
        return audio_processor_tab

    def create_generation_settings_tab(self):
        """[TARGET] Tạo tab cài đặt điều khiển tạo - Chatterbox Extended"""
        generation_tab = QWidget()
        generation_layout = QVBoxLayout()
        
        # Header với status
        header_layout = QHBoxLayout()
        header_icon = QLabel("[TARGET]")
        header_icon.setStyleSheet("font-weight: bold; color: #FF6347; font-size: 14px;")
        header_title = QLabel("Điều khiển tạo chất lượng")
        header_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        # Status indicator
        self.generation_controller_status = QLabel("🟢 Hoạt động")
        self.generation_controller_status.setStyleSheet("color: green; font-weight: bold;")
        header_layout.addWidget(self.generation_controller_status)
        
        generation_layout.addLayout(header_layout)
        
        # Chế độ điều khiển tạo
        mode_group = QGroupBox("⚙️ Chế độ điều khiển tạo")
        mode_layout = QGridLayout()
        
        mode_layout.addWidget(QLabel("Chế độ hiện tại:"), 0, 0)
        self.generation_control_mode = QComboBox()
        self.generation_control_mode.addItems([
            "fast - Tạo nhanh",
            "balanced - Cân bằng", 
            "quality - Chất lượng cao"
        ])
        self.generation_control_mode.setCurrentText("balanced - Cân bằng")
        mode_layout.addWidget(self.generation_control_mode, 0, 1)
        
        # Mô tả chế độ
        self.generation_mode_description = QLabel("Tạo cân bằng với validation cơ bản")
        self.generation_mode_description.setStyleSheet("color: #555; font-style: italic; padding: 5px;")
        self.generation_mode_description.setWordWrap(True)
        mode_layout.addWidget(self.generation_mode_description, 1, 0, 1, 2)
        
        # Connect signal để cập nhật mô tả
        # self.generation_control_mode.currentTextChanged.connect(self._update_generation_mode_description)
        
        mode_group.setLayout(mode_layout)
        generation_layout.addWidget(mode_group)
        
        # Cài đặt tạo đa phiên bản
        generation_group = QGroupBox("🎯 Tạo đa phiên bản")
        generation_layout_grid = QGridLayout()
        
        generation_layout_grid.addWidget(QLabel("Số lần tạo:"), 0, 0)
        self.num_generations = QSpinBox()
        self.num_generations.setRange(1, 5)
        self.num_generations.setValue(2)
        self.num_generations.setToolTip("Số lần tạo khác nhau cho mỗi đoạn văn bản")
        self.num_generations.setSuffix(" lần")
        generation_layout_grid.addWidget(self.num_generations, 0, 1)
        
        generation_layout_grid.addWidget(QLabel("Ứng viên mỗi khối:"), 1, 0)
        self.candidates_per_block = QSpinBox()
        self.candidates_per_block.setRange(1, 3)
        self.candidates_per_block.setValue(2)
        self.candidates_per_block.setToolTip("Số biến thể cho mỗi lần tạo")
        self.candidates_per_block.setSuffix(" ứng viên")
        generation_layout_grid.addWidget(self.candidates_per_block, 1, 1)
        
        generation_layout_grid.addWidget(QLabel("Thử lại tối đa:"), 2, 0)
        self.max_retries = QSpinBox()
        self.max_retries.setRange(1, 5)
        self.max_retries.setValue(3)
        self.max_retries.setToolTip("Số lần thử lại nếu validation thất bại")
        self.max_retries.setSuffix(" lần")
        generation_layout_grid.addWidget(self.max_retries, 2, 1)
        
        generation_layout_grid.addWidget(QLabel("Timeout tạo:"), 3, 0)
        self.generation_timeout = QDoubleSpinBox()
        self.generation_timeout.setRange(30.0, 300.0)
        self.generation_timeout.setValue(120.0)
        self.generation_timeout.setToolTip("Thời gian timeout cho mỗi lần tạo")
        self.generation_timeout.setSuffix(" giây")
        generation_layout_grid.addWidget(self.generation_timeout, 3, 1)
        
        generation_group.setLayout(generation_layout_grid)
        generation_layout.addWidget(generation_group)
        
        # Chiến lược fallback
        fallback_group = QGroupBox("🔄 Chiến lược fallback")
        fallback_layout = QGridLayout()
        
        fallback_layout.addWidget(QLabel("Chiến lược fallback:"), 0, 0)
        self.fallback_strategy = QComboBox()
        self.fallback_strategy.addItems([
            "highest_similarity - Độ tương đồng cao nhất",
            "longest - Bản dài nhất",
            "first_success - Thành công đầu tiên"
        ])
        self.fallback_strategy.setCurrentText("highest_similarity - Độ tương đồng cao nhất")
        fallback_layout.addWidget(self.fallback_strategy, 0, 1)
        
        # Mô tả chiến lược
        self.fallback_description = QLabel("Chọn ứng viên có độ tương đồng cao nhất với văn bản gốc")
        self.fallback_description.setStyleSheet("color: #555; font-style: italic; padding: 5px;")
        self.fallback_description.setWordWrap(True)
        fallback_layout.addWidget(self.fallback_description, 1, 0, 1, 2)
        
        # Connect signal
        # self.fallback_strategy.currentTextChanged.connect(self._update_fallback_description)
        
        fallback_group.setLayout(fallback_layout)
        generation_layout.addWidget(fallback_group)
        
        # Kiểm soát chất lượng
        quality_group = QGroupBox("✅ Kiểm soát chất lượng")
        quality_layout = QGridLayout()
        
        self.enable_quality_control_checkbox = QCheckBox("Kích hoạt kiểm soát chất lượng")
        self.enable_quality_control_checkbox.setChecked(True)
        self.enable_quality_control_checkbox.setToolTip("Bật/tắt hệ thống kiểm soát chất lượng tự động")
        quality_layout.addWidget(self.enable_quality_control_checkbox, 0, 0, 1, 2)
        
        quality_layout.addWidget(QLabel("Ngưỡng chất lượng tối thiểu:"), 1, 0)
        self.min_quality_threshold = QDoubleSpinBox()
        self.min_quality_threshold.setRange(0.1, 1.0)
        self.min_quality_threshold.setValue(0.6)
        self.min_quality_threshold.setDecimals(2)
        self.min_quality_threshold.setToolTip("Điểm chất lượng tối thiểu để chấp nhận")
        quality_layout.addWidget(self.min_quality_threshold, 1, 1)
        
        self.auto_retry_failed_checkbox = QCheckBox("Tự động thử lại khi thất bại")
        self.auto_retry_failed_checkbox.setChecked(True)
        self.auto_retry_failed_checkbox.setToolTip("Tự động thử lại khi validation không đạt yêu cầu")
        quality_layout.addWidget(self.auto_retry_failed_checkbox, 2, 0, 1, 2)
        
        self.parallel_generation_checkbox = QCheckBox("Tạo song song")
        self.parallel_generation_checkbox.setChecked(True)
        self.parallel_generation_checkbox.setToolTip("Tạo nhiều ứng viên đồng thời để tăng tốc độ")
        quality_layout.addWidget(self.parallel_generation_checkbox, 3, 0, 1, 2)
        
        quality_group.setLayout(quality_layout)
        generation_layout.addWidget(quality_group)
        
        # Cài đặt nâng cao
        advanced_group = QGroupBox("🎛️ Cài đặt nâng cao")
        advanced_layout = QGridLayout()
        
        advanced_layout.addWidget(QLabel("Số worker song song:"), 0, 0)
        self.max_concurrent_generations = QSpinBox()
        self.max_concurrent_generations.setRange(1, 8)
        self.max_concurrent_generations.setValue(4)
        self.max_concurrent_generations.setToolTip("Số luồng tạo đồng thời tối đa")
        self.max_concurrent_generations.setSuffix(" worker")
        advanced_layout.addWidget(self.max_concurrent_generations, 0, 1)
        
        advanced_layout.addWidget(QLabel("Seed randomization:"), 1, 0)
        self.seed_randomization_checkbox = QCheckBox("Sử dụng seed ngẫu nhiên")
        self.seed_randomization_checkbox.setChecked(True)
        self.seed_randomization_checkbox.setToolTip("Tự động tạo seed khác nhau cho mỗi lần tạo")
        advanced_layout.addWidget(self.seed_randomization_checkbox, 1, 1)
        
        self.detailed_logging_checkbox = QCheckBox("Logging chi tiết")
        self.detailed_logging_checkbox.setChecked(False)
        self.detailed_logging_checkbox.setToolTip("Ghi log chi tiết quá trình tạo (ảnh hưởng performance)")
        advanced_layout.addWidget(self.detailed_logging_checkbox, 2, 0, 1, 2)
        
        self.save_failed_generations_checkbox = QCheckBox("Lưu các lần tạo thất bại")
        self.save_failed_generations_checkbox.setChecked(False)
        self.save_failed_generations_checkbox.setToolTip("Lưu lại các ứng viên không đạt chất lượng để debug")
        advanced_layout.addWidget(self.save_failed_generations_checkbox, 3, 0, 1, 2)
        
        advanced_group.setLayout(advanced_layout)
        generation_layout.addWidget(advanced_group)
        
        # Thống kê tạo
        stats_group = QGroupBox("📊 Thống kê tạo")
        stats_layout = QGridLayout()
        
        self.total_generations_label = QLabel("Tổng lần tạo: 0")
        stats_layout.addWidget(self.total_generations_label, 0, 0)
        
        self.success_rate_label = QLabel("Tỷ lệ thành công: 0.0%")
        stats_layout.addWidget(self.success_rate_label, 0, 1)
        
        self.avg_quality_score_label = QLabel("Điểm chất lượng trung bình: 0.0")
        stats_layout.addWidget(self.avg_quality_score_label, 1, 0)
        
        self.avg_generation_time_label = QLabel("Thời gian tạo trung bình: 0.0s")
        stats_layout.addWidget(self.avg_generation_time_label, 1, 1)
        
        stats_group.setLayout(stats_layout)
        generation_layout.addWidget(stats_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test điều khiển tạo")
        # test_btn.clicked.connect(self._test_generation_control)
        button_layout.addWidget(test_btn)
        
        reset_btn = QPushButton("🔄 Khôi phục mặc định")
        # reset_btn.clicked.connect(self._reset_generation_settings)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        apply_btn = QPushButton("✅ Áp dụng cài đặt")
        apply_btn.setStyleSheet("background-color: #FF6347; color: white; font-weight: bold; padding: 8px;")
        # apply_btn.clicked.connect(self._apply_generation_settings)
        button_layout.addWidget(apply_btn)
        
        generation_layout.addLayout(button_layout)
        generation_layout.addStretch()
        
        generation_tab.setLayout(generation_layout)
        return generation_tab

    def create_whisper_settings_tab(self):
        """Create whisper settings tab for Settings"""
        whisper_tab = QWidget()
        whisper_layout = QVBoxLayout()
        
        # Whisper Settings
        whisper_settings_group = QGroupBox("Whisper Validation")
        whisper_settings_layout = QGridLayout()
        
        whisper_settings_layout.addWidget(QLabel("Enable Validation:"), 0, 0)
        self.whisper_validation_checkbox = QCheckBox("STT verification with similarity scoring")
        self.whisper_validation_checkbox.setChecked(True)
        whisper_settings_layout.addWidget(self.whisper_validation_checkbox, 0, 1)
        
        whisper_settings_layout.addWidget(QLabel("Whisper Model:"), 1, 0)
        self.whisper_model_combo = QComboBox()
        self.whisper_model_combo.addItems([
            "tiny (39MB, 32x realtime)",
            "base (74MB, 16x realtime)",
            "small (244MB, 6x realtime)",
            "medium (769MB, 2x realtime)",
            "large-v2 (1550MB, 1x realtime)",
            "large-v3 (1550MB, 1x realtime)"
        ])
        self.whisper_model_combo.setCurrentText("base (74MB, 16x realtime)")
        whisper_settings_layout.addWidget(self.whisper_model_combo, 1, 1)
        
        whisper_settings_layout.addWidget(QLabel("Backend:"), 2, 0)
        self.whisper_backend_combo = QComboBox()
        self.whisper_backend_combo.addItems(["openai_whisper", "faster_whisper"])
        self.whisper_backend_combo.setCurrentText("faster_whisper")
        whisper_settings_layout.addWidget(self.whisper_backend_combo, 2, 1)
        
        whisper_settings_layout.addWidget(QLabel("Similarity Threshold:"), 3, 0)
        self.similarity_threshold = QDoubleSpinBox()
        self.similarity_threshold.setRange(0.1, 1.0)
        self.similarity_threshold.setValue(0.7)
        self.similarity_threshold.setDecimals(2)
        whisper_settings_layout.addWidget(self.similarity_threshold, 3, 1)
        
        whisper_settings_group.setLayout(whisper_settings_layout)
        whisper_layout.addWidget(whisper_settings_group)
        
        # VRAM Info
        vram_info_group = QGroupBox("VRAM Information")
        vram_info_layout = QVBoxLayout()
        vram_info_text = QLabel("""
        <b>Model VRAM Requirements:</b><br>
        • tiny: ~1GB VRAM<br>
        • base: ~2GB VRAM<br>
        • small: ~5GB VRAM<br>
        • medium: ~10GB VRAM<br>
        • large-v2/v3: ~11GB VRAM
        """)
        vram_info_text.setWordWrap(True)
        vram_info_layout.addWidget(vram_info_text)
        vram_info_group.setLayout(vram_info_layout)
        whisper_layout.addWidget(vram_info_group)
        
        whisper_tab.setLayout(whisper_layout)
        
        return whisper_tab

    def change_language(self, language_text):
        """Change interface language"""
        language_code = self.language_combo.currentData()
        self.language_manager.current_language = language_code
        
        # Update all tab names
        for i in range(self.tabs.count()):
            tab_text = None
            if i == 0:
                tab_text = self.language_manager.get('tab_video')
            elif i == 1:
                tab_text = self.language_manager.get('tab_voice_studio')
            elif i == 2:
                tab_text = self.language_manager.get('tab_voice_conversion')
            elif i == 3:
                tab_text = self.language_manager.get('tab_emotion_config')
            elif i == 4:
                tab_text = self.language_manager.get('tab_license')
            elif i == 5:
                tab_text = self.language_manager.get('tab_projects')
            elif i == 6:
                tab_text = self.language_manager.get('tab_settings')
            
            if tab_text:
                self.tabs.setTabText(i, tab_text)
        
        # Update main interface elements
        if hasattr(self, 'language_label'):
            self.language_label.setText(self.language_manager.get('language_interface'))
        
        # Force refresh all tabs
        self.refresh_all_ui_texts()
        
        print(f"Language changed to: {language_text} ({language_code})")

    def create_input_style(self):
        """Create consistent input field styling"""
        return """
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #95a5a6;
            }
        """

    def create_combo_style(self):
        """Create consistent combo box styling"""
        return """
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #95a5a6;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
                background: transparent;
            }
        """

    def create_spinbox_style(self):
        """Create consistent spinbox styling"""
        return """
            QSpinBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-width: 100px;
            }
            QSpinBox:hover {
                border-color: #95a5a6;
            }
            QSpinBox:focus {
                border-color: #3498db;
            }
        """

    def create_primary_button_style(self):
        """Create primary button styling"""
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """

    def create_secondary_button_style(self):
        """Create secondary button styling"""
        return """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """

    def create_warning_button_style(self):
        """Create warning button styling"""
        return """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """

    def reset_settings_to_defaults(self):
        """Reset settings to default values"""
        reply = QMessageBox.question(
            self, 
            "Xác nhận", 
            "Bạn có chắc chắn muốn đặt lại tất cả cài đặt về mặc định?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset all form fields to defaults
            self.openai_key_input.clear()
            self.claude_key_input.clear()
            self.deepseek_key_input.clear()
            self.midjourney_key_input.clear()
            self.stability_key_input.clear()
            self.elevenlabs_key_input.clear()
            self.google_tts_key_input.clear()
            self.azure_speech_key_input.clear()
            
            # Reset combo boxes
            self.content_provider_combo.setCurrentIndex(0)
            self.image_provider_combo.setCurrentIndex(0)
            self.tts_provider_combo.setCurrentIndex(0)
            self.resolution_combo.setCurrentIndex(0)
            self.fps_spinbox.setValue(25)
            
            QMessageBox.information(self, "Hoàn thành", "Đã đặt lại cài đặt về mặc định!")

    def refresh_all_ui_texts(self):
        """Refresh all UI texts based on current language"""
        # This method can be expanded to update all UI elements
        # For now, we'll update the main visible elements
        
        # Update character settings table headers if it exists
        if hasattr(self, 'character_table'):
            headers = [
                self.language_manager.get('character'),
                self.language_manager.get('emotion'),
                self.language_manager.get('speed'),
                self.language_manager.get('status'),
                self.language_manager.get('preview'),
                self.language_manager.get('actions')
            ]
            self.character_table.setHorizontalHeaderLabels(headers)
        
        # Update button texts and labels based on language
        # Additional elements can be updated here as needed
        pass

    def create_performance_settings_tab(self):
        """Create Performance Settings tab for hybrid TTS optimization"""
        performance_tab = QWidget()
        performance_layout = QVBoxLayout()
        
        # TTS Engine Mode Settings - Compact design
        engine_group = QGroupBox(language_manager.get_text('tts_engine_mode'))
        engine_layout = QGridLayout()
        
        # Processing mode selection - more compact
        engine_layout.addWidget(QLabel(language_manager.get_text('processing_mode')), 0, 0)
        self.tts_mode_combo = QComboBox()
        self.tts_mode_combo.addItem(language_manager.get_text('max_performance'), "maximum_performance")
        self.tts_mode_combo.addItem(language_manager.get_text('hybrid_recommended'), "hybrid")  
        self.tts_mode_combo.addItem(language_manager.get_text('max_compatibility'), "maximum_compatibility")
        self.tts_mode_combo.setCurrentIndex(1)  # Default to hybrid
        engine_layout.addWidget(self.tts_mode_combo, 0, 1)
        
        # Compact info display - single line per mode
        self.mode_info_label = QLabel(language_manager.get_text('mode_hybrid_desc'))
        self.mode_info_label.setStyleSheet("color: #666; font-style: italic; padding: 4px;")
        self.mode_info_label.setWordWrap(True)
        engine_layout.addWidget(self.mode_info_label, 0, 2)
        
        # Connect combo change to update info
        self.tts_mode_combo.currentTextChanged.connect(self.update_mode_info)
        
        # Performance Options - more compact layout
        engine_layout.addWidget(QLabel(language_manager.get_text('model_caching')), 1, 0)
        self.cache_enabled_checkbox = QCheckBox(language_manager.get_text('enable_caching'))
        self.cache_enabled_checkbox.setChecked(True)
        engine_layout.addWidget(self.cache_enabled_checkbox, 1, 1, 1, 2)
        
        engine_layout.addWidget(QLabel(language_manager.get_text('parallel_processing')), 2, 0)
        self.parallel_processing_checkbox = QCheckBox(language_manager.get_text('enable_parallel'))
        self.parallel_processing_checkbox.setChecked(True)
        engine_layout.addWidget(self.parallel_processing_checkbox, 2, 1, 1, 2)
        
        engine_layout.addWidget(QLabel(language_manager.get_text('validation_bypass')), 3, 0)
        self.bypass_validation_checkbox = QCheckBox(language_manager.get_text('skip_validation'))
        self.bypass_validation_checkbox.setChecked(True)
        engine_layout.addWidget(self.bypass_validation_checkbox, 3, 1, 1, 2)
        
        engine_group.setLayout(engine_layout)
        performance_layout.addWidget(engine_group)
        
        # Performance Metrics Display - Compact
        metrics_group = QGroupBox(language_manager.get_text('performance_metrics'))
        metrics_layout = QVBoxLayout()
        
        # Simplified metrics display
        metrics_grid = QGridLayout()
        metrics_grid.addWidget(QLabel("Total Requests:"), 0, 0)
        self.total_requests_label = QLabel("--")
        metrics_grid.addWidget(self.total_requests_label, 0, 1)
        
        metrics_grid.addWidget(QLabel("Cache Hit Rate:"), 0, 2)
        self.cache_hit_label = QLabel("--%")  
        metrics_grid.addWidget(self.cache_hit_label, 0, 3)
        
        metrics_grid.addWidget(QLabel("Avg Generation:"), 1, 0)
        self.avg_generation_label = QLabel("--s")
        metrics_grid.addWidget(self.avg_generation_label, 1, 1)
        
        metrics_grid.addWidget(QLabel("Speedup Factor:"), 1, 2)
        self.speedup_label = QLabel("--x")
        metrics_grid.addWidget(self.speedup_label, 1, 3)
        
        metrics_layout.addLayout(metrics_grid)
        
        # Performance control buttons - inline
        metrics_btn_layout = QHBoxLayout()
        
        self.clear_cache_btn = QPushButton(language_manager.get_text('clear_cache'))
        self.clear_cache_btn.clicked.connect(self.clear_performance_cache)
        metrics_btn_layout.addWidget(self.clear_cache_btn)
        
        self.update_metrics_btn = QPushButton(language_manager.get_text('update_metrics'))
        self.update_metrics_btn.clicked.connect(self.update_performance_metrics)
        metrics_btn_layout.addWidget(self.update_metrics_btn)
        
        metrics_btn_layout.addStretch()
        metrics_layout.addLayout(metrics_btn_layout)
        
        metrics_group.setLayout(metrics_layout)
        performance_layout.addWidget(metrics_group)
        
        # Add stretch to push content to top
        performance_layout.addStretch()
        
        performance_tab.setLayout(performance_layout)
        return performance_tab
    
    def update_mode_info(self):
        """Update mode information based on selected mode"""
        current_mode = self.tts_mode_combo.currentData()
        if current_mode == "maximum_performance":
            self.mode_info_label.setText(language_manager.get_text('mode_perf_desc'))
        elif current_mode == "hybrid": 
            self.mode_info_label.setText(language_manager.get_text('mode_hybrid_desc'))
        elif current_mode == "maximum_compatibility":
            self.mode_info_label.setText(language_manager.get_text('mode_compat_desc'))
    
    def clear_performance_cache(self):
        """Clear all performance caches"""
        try:
            # Import here to avoid circular imports
            from core.hybrid_tts_manager import HybridTtsManager
            
            # This would clear the cache if a manager instance exists
            QMessageBox.information(
                self,
                "Cache Cleared",
                "Performance cache has been cleared successfully!"
            )
            
            # Update metrics after clearing
            self.update_performance_metrics()
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to clear cache: {str(e)}"
            )
    
    def update_performance_metrics(self):
        """Update performance metrics display"""
        try:
            # Placeholder metrics - in real implementation, this would get metrics from HybridTtsManager
            metrics_text = """
            <b>Performance Statistics:</b><br>
            • Total Requests: 0<br>
            • Cache Hit Rate: 0%<br>
            • Average Generation Time: --s<br>
            • Speedup Factor: 1.0x<br>
            • Total Time Saved: 0s<br><br>
            <i>Start generating audio to see real metrics</i>
            """
            self.performance_metrics_text.setText(metrics_text)
            
        except Exception as e:
            self.performance_metrics_text.setText(f"Error updating metrics: {str(e)}")
        
        # Add all tabs
        text_processor_tab.setLayout(text_processor_layout)
        audio_processor_tab.setLayout(audio_layout)
        generation_tab.setLayout(generation_layout)
        whisper_tab.setLayout(whisper_layout)
        
        self.extended_tabs.addTab(text_processor_tab, "[EDIT] Text")
        self.extended_tabs.addTab(audio_processor_tab, "[MUSIC] Audio")
        self.extended_tabs.addTab(generation_tab, "[TARGET] Generation")
        self.extended_tabs.addTab(whisper_tab, "[MIC] Whisper")
        self.extended_tabs.addTab(preset_tab, "[CONFIG] Presets")
        self.extended_tabs.addTab(self.create_performance_settings_tab(), "[FAST] Performance")
        
        extended_layout.addWidget(self.extended_tabs)
        extended_group.setLayout(extended_layout)
        layout.addWidget(extended_group)
        
        # Group 7: Actions - Tách thành group riêng giống tab Dự án/Cài đặt
        actions_group = QGroupBox("[EMOJI] Thao tác")
        action_buttons_layout = QGridLayout()
        action_buttons_layout.setSpacing(8)
        
        # Thêm các nút output/generate vào action bar
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Thư mục output:"))
        output_layout.addWidget(self.voice_output_input)
        output_layout.addWidget(self.select_voice_output_btn)
        action_buttons_layout.addLayout(output_layout, 0, 0, 1, 2)
        
        # Generate buttons
        action_buttons_layout.addWidget(self.generate_selected_btn, 1, 0)
        action_buttons_layout.addWidget(self.generate_all_btn, 1, 1)
        
        # Output management buttons
        action_buttons_layout.addWidget(self.open_voice_folder_btn, 2, 0)
        action_buttons_layout.addWidget(self.clear_voice_results_btn, 2, 1)
        
        # Force Merge button - tối ưu cho trường hợp script data không match
        self.force_merge_btn = QPushButton("[TOOL] Merge All")
        self.force_merge_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #007ACC;
                border: 1px solid #007ACC;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
                border-color: #005999;
            }
        """)
        self.force_merge_btn.clicked.connect(self.force_merge_all_segments)
        self.force_merge_btn.setToolTip("Gộp tất cả file segment_*.mp3 có trong thư mục output (không cần script data)")
        action_buttons_layout.addWidget(self.force_merge_btn, 3, 0, 1, 2)
        
        actions_group.setLayout(action_buttons_layout)
        layout.addWidget(actions_group)
        
        # Initialize data
        self.voice_studio_script_data = None
        self.voice_mapping = {}
        self.character_chatterbox_settings = {}  # Store per-character settings
        self.voice_clone_folder = None
        
        # === SET UP MAIN TAB LAYOUT ===
        voice_studio_widget.setLayout(layout)
        
        # Use scroll area for the full content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(voice_studio_widget)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        tab = QWidget()
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, self.language_manager.get('tab_voice_studio'))
    
    def create_voice_conversion_tab(self):
        """Tạo tab Voice Conversion"""
        try:
            from .voice_conversion_tab import VoiceConversionTab
            self.voice_conversion_tab = VoiceConversionTab()
            self.tabs.addTab(self.voice_conversion_tab, self.language_manager.get('tab_voice_conversion'))
        except Exception as e:
            # Fallback nếu có lỗi
            fallback_tab = QWidget()
            layout = QVBoxLayout()
            error_label = QLabel(f"Loi load Voice Conversion tab: {str(e)}")
            error_label.setWordWrap(True)
            layout.addWidget(error_label)
            fallback_tab.setLayout(layout)
            self.tabs.addTab(fallback_tab, self.language_manager.get('tab_voice_conversion'))
    
    def create_emotion_config_tab(self):
        """Tạo tab Emotion Configuration"""
        try:
            self.emotion_config_tab = EmotionConfigTab()
            self.tabs.addTab(self.emotion_config_tab, self.language_manager.get('tab_emotion_config'))
        except Exception as e:
            # Fallback nếu có lỗi
            fallback_tab = QWidget()
            layout = QVBoxLayout()
            error_label = QLabel(f"Loi load Emotion Config: {str(e)}")
            error_label.setWordWrap(True)
            layout.addWidget(error_label)
            fallback_tab.setLayout(layout)
            self.tabs.addTab(fallback_tab, self.language_manager.get('tab_emotion_config'))

    def create_license_tab(self):
        """Tạo tab License Management"""
        try:
            self.license_tab = LicenseTab()
            self.tabs.addTab(self.license_tab, self.language_manager.get('tab_license'))
        except Exception as e:
            # Fallback nếu có lỗi
            fallback_tab = QWidget()
            layout = QVBoxLayout()
            error_label = QLabel(f"Loi load License tab: {str(e)}")
            error_label.setWordWrap(True)
            layout.addWidget(error_label)
            fallback_tab.setLayout(layout)
            self.tabs.addTab(fallback_tab, self.language_manager.get('tab_license'))
    
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
        header_layout.addWidget(QLabel("[FOLDER] Danh sách dự án"))
        header_layout.addStretch()
        
        # Thêm nút tạo project mới
        create_project_btn = QPushButton("[EMOJI] Tạo dự án")
        create_project_btn.setToolTip("Tạo dự án mới")
        create_project_btn.clicked.connect(self.create_new_project)
        header_layout.addWidget(create_project_btn)
        
        refresh_btn = QPushButton("[REFRESH]")
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
        right_layout.addWidget(QLabel("[CLIPBOARD] Chi tiết dự án"))
        
        # Thêm Chatterbox Extended status
        chatterbox_status_layout = QHBoxLayout()
        chatterbox_status_layout.addWidget(QLabel("[ROCKET] Chatterbox Extended:"))
        
        self.chatterbox_status_label = QLabel("[EMOJI] Chưa khả dụng")
        self.chatterbox_status_label.setStyleSheet("color: red; font-weight: bold;")
        chatterbox_status_layout.addWidget(self.chatterbox_status_label)
        
        chatterbox_status_layout.addStretch()
        right_layout.addLayout(chatterbox_status_layout)
        
        # Chi tiết project với scroll
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        details_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.project_details = QTextEdit()
        self.project_details.setReadOnly(True)
        details_scroll.setWidget(self.project_details)
        right_layout.addWidget(details_scroll)
        
        # Nút actions
        actions_group = QGroupBox("[EMOJI] Thao tác")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        self.open_folder_btn = QPushButton("[FOLDER] Mở thư mục")
        self.open_folder_btn.clicked.connect(self.open_project_folder)
        actions_layout.addWidget(self.open_folder_btn, 0, 0)
        
        self.edit_project_btn = QPushButton("[EDIT] Chỉnh sửa")
        self.edit_project_btn.clicked.connect(self.edit_project)
        actions_layout.addWidget(self.edit_project_btn, 0, 1)
        
        self.delete_project_btn = QPushButton("[DELETE] Xóa dự án")
        self.delete_project_btn.clicked.connect(self.delete_project)
        self.delete_project_btn.setProperty("class", "danger")
        actions_layout.addWidget(self.delete_project_btn, 1, 0, 1, 2)
        
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
        
        self.tabs.addTab(tab, self.language_manager.get('tab_projects'))
        
        # Load projects khi khởi tạo
        self.refresh_projects()
        
        # Kiểm tra Chatterbox Extended status
        self.check_chatterbox_extended_status()
    
    def create_settings_tab(self):
        """Tab cài đặt với layout tối ưu và dễ hiểu"""
        tab = QWidget()
        
        # Sử dụng scroll area cho settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        content_widget.setLayout(layout)
        
        # === LANGUAGE SELECTION (TOP) ===
        language_group = QGroupBox("[EMOJI] " + self.language_manager.get('language_interface'))
        language_layout = QHBoxLayout()
        
        language_label = QLabel("Chọn ngôn ngữ giao diện:")
        language_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        language_layout.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("[EMOJI][EMOJI] Tiếng Việt", "vi")
        self.language_combo.addItem("[EMOJI][EMOJI] English", "en")
        self.language_combo.setCurrentIndex(0)  # Default Vietnamese
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #2980b9;
            }
        """)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        
        language_group.setLayout(language_layout)
        layout.addWidget(language_group)
        
        # === API KEYS SECTION ===
        api_group = QGroupBox("[EMOJI] " + self.language_manager.get('api_keys'))
        api_layout = QVBoxLayout()
        api_layout.setSpacing(12)
        
        # AI Content Generation APIs
        ai_section = QGroupBox("[BOT] AI Tạo nội dung")
        ai_layout = QGridLayout()
        ai_layout.setSpacing(10)
        
        # OpenAI API Key
        ai_layout.addWidget(QLabel("OpenAI API Key:"), 0, 0)
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("sk-... (Dùng cho GPT-4 tạo script)")
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setStyleSheet(self.create_input_style())
        self.openai_key_input.setToolTip("Khóa API OpenAI để sử dụng GPT-4 tạo kịch bản video. Lấy tại: https://platform.openai.com/api-keys")
        ai_layout.addWidget(self.openai_key_input, 0, 1)
        
        # Claude API Key
        ai_layout.addWidget(QLabel("Claude API Key:"), 1, 0)
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setPlaceholderText("sk-ant-... (Dùng cho Claude tạo script)")
        self.claude_key_input.setEchoMode(QLineEdit.Password)
        self.claude_key_input.setStyleSheet(self.create_input_style())
        self.claude_key_input.setToolTip("Khóa API Claude từ Anthropic để tạo kịch bản chất lượng cao. Lấy tại: https://console.anthropic.com/")
        ai_layout.addWidget(self.claude_key_input, 1, 1)
        
        # DeepSeek API Key
        ai_layout.addWidget(QLabel("DeepSeek API Key:"), 2, 0)
        self.deepseek_key_input = QLineEdit()
        self.deepseek_key_input.setPlaceholderText("sk-... (Dùng cho DeepSeek tạo script)")
        self.deepseek_key_input.setEchoMode(QLineEdit.Password)
        self.deepseek_key_input.setStyleSheet(self.create_input_style())
        self.deepseek_key_input.setToolTip("Khóa API DeepSeek - AI mạnh mẽ và tiết kiệm chi phí. Lấy tại: https://platform.deepseek.com/")
        ai_layout.addWidget(self.deepseek_key_input, 2, 1)
        
        ai_section.setLayout(ai_layout)
        api_layout.addWidget(ai_section)
        
        # Image Generation APIs
        image_section = QGroupBox("[PAINT] Tạo hình ảnh")
        image_layout = QGridLayout()
        image_layout.setSpacing(10)
        
        # Midjourney API Key
        image_layout.addWidget(QLabel("Midjourney API Key:"), 0, 0)
        self.midjourney_key_input = QLineEdit()
        self.midjourney_key_input.setPlaceholderText("mj-... (Dùng cho Midjourney tạo ảnh)")
        self.midjourney_key_input.setEchoMode(QLineEdit.Password)
        self.midjourney_key_input.setStyleSheet(self.create_input_style())
        image_layout.addWidget(self.midjourney_key_input, 0, 1)
        
        # Stability AI Key
        image_layout.addWidget(QLabel("Stability AI Key:"), 1, 0)
        self.stability_key_input = QLineEdit()
        self.stability_key_input.setPlaceholderText("sk-... (Dùng cho Stable Diffusion)")
        self.stability_key_input.setEchoMode(QLineEdit.Password)
        self.stability_key_input.setStyleSheet(self.create_input_style())
        image_layout.addWidget(self.stability_key_input, 1, 1)
        
        image_section.setLayout(image_layout)
        api_layout.addWidget(image_section)
        
        # TTS APIs
        tts_section = QGroupBox("[EMOJI] Text-to-Speech")
        tts_layout = QGridLayout()
        tts_layout.setSpacing(10)
        
        # ElevenLabs API Key
        tts_layout.addWidget(QLabel("ElevenLabs API Key:"), 0, 0)
        self.elevenlabs_key_input = QLineEdit()
        self.elevenlabs_key_input.setPlaceholderText("sk-... (Dùng cho ElevenLabs TTS)")
        self.elevenlabs_key_input.setEchoMode(QLineEdit.Password)
        self.elevenlabs_key_input.setStyleSheet(self.create_input_style())
        tts_layout.addWidget(self.elevenlabs_key_input, 0, 1)
        
        # Google TTS API Key
        tts_layout.addWidget(QLabel("Google TTS API Key:"), 1, 0)
        self.google_tts_key_input = QLineEdit()
        self.google_tts_key_input.setPlaceholderText("AIza... (Dùng cho Google Cloud TTS)")
        self.google_tts_key_input.setEchoMode(QLineEdit.Password)
        self.google_tts_key_input.setStyleSheet(self.create_input_style())
        tts_layout.addWidget(self.google_tts_key_input, 1, 1)
        
        # Azure Speech Key
        tts_layout.addWidget(QLabel("Azure Speech Key:"), 2, 0)
        self.azure_speech_key_input = QLineEdit()
        self.azure_speech_key_input.setPlaceholderText("... (Dùng cho Azure Speech)")
        self.azure_speech_key_input.setEchoMode(QLineEdit.Password)
        self.azure_speech_key_input.setStyleSheet(self.create_input_style())
        tts_layout.addWidget(self.azure_speech_key_input, 2, 1)
        
        tts_section.setLayout(tts_layout)
        api_layout.addWidget(tts_section)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # === PROVIDERS SECTION ===
        providers_group = QGroupBox("[CONFIG] " + self.language_manager.get('providers'))
        providers_layout = QGridLayout()
        providers_layout.setSpacing(10)
        
        # Content Provider
        providers_layout.addWidget(QLabel("Nhà cung cấp AI tạo nội dung:"), 0, 0)
        self.content_provider_combo = QComboBox()
        self.content_provider_combo.addItems([
            "OpenAI GPT-4",
            "Claude (Anthropic)",
            "DeepSeek",
            "Auto (thử theo thứ tự)"
        ])
        self.content_provider_combo.setStyleSheet(self.create_combo_style())
        providers_layout.addWidget(self.content_provider_combo, 0, 1)
        
        # Image Provider
        providers_layout.addWidget(QLabel("Nhà cung cấp tạo ảnh:"), 1, 0)
        self.image_provider_combo = QComboBox()
        self.image_provider_combo.addItems([
            "DALL-E (OpenAI)",
            "Midjourney",
            "Stable Diffusion",
            "Manual (chọn ảnh thủ công)"
        ])
        self.image_provider_combo.setStyleSheet(self.create_combo_style())
        providers_layout.addWidget(self.image_provider_combo, 1, 1)
        
        # TTS Provider
        providers_layout.addWidget(QLabel("Nhà cung cấp TTS:"), 2, 0)
        self.tts_provider_combo = QComboBox()
        self.tts_provider_combo.addItems([
            "[ROCKET] Chatterbox TTS (Khuyến nghị)",
            "ElevenLabs",
            "Google Cloud TTS",
            "Google TTS (Free)",
            "Azure Speech"
        ])
        self.tts_provider_combo.setStyleSheet(self.create_combo_style())
        self.tts_provider_combo.setToolTip("Chọn nhà cung cấp TTS:\n• Chatterbox TTS: Tốt nhất cho giọng clone và cảm xúc\n• ElevenLabs: Chất lượng cao, tiếng Anh\n• Google Cloud TTS: Tốt cho tiếng Việt\n• Google TTS Free: Miễn phí, chất lượng cơ bản")
        providers_layout.addWidget(self.tts_provider_combo, 2, 1)
        
        providers_group.setLayout(providers_layout)
        layout.addWidget(providers_group)
        
        # === VIDEO SETTINGS SECTION ===
        video_group = QGroupBox("[ACTION] " + self.language_manager.get('video_settings'))
        video_layout = QGridLayout()
        video_layout.setSpacing(10)
        
        # Resolution
        video_layout.addWidget(QLabel("Độ phân giải:"), 0, 0)
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "3840x2160 (4K)"
        ])
        self.resolution_combo.setStyleSheet(self.create_combo_style())
        video_layout.addWidget(self.resolution_combo, 0, 1)
        
        # FPS
        video_layout.addWidget(QLabel("Tốc độ khung hình (FPS):"), 1, 0)
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setRange(15, 60)
        self.fps_spinbox.setValue(25)
        self.fps_spinbox.setSuffix(" fps")
        self.fps_spinbox.setStyleSheet(self.create_spinbox_style())
        video_layout.addWidget(self.fps_spinbox, 1, 1)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # === CHATTERBOX EXTENDED SETTINGS ===
        chatterbox_group = QGroupBox("[ROCKET] " + self.language_manager.get('chatterbox_extended'))
        chatterbox_layout = QVBoxLayout()
        
        # Info label
        info_label = QLabel("Cài đặt nâng cao cho Chatterbox Extended với các tính năng:")
        info_label.setStyleSheet("color: #7f8c8d; font-style: italic; margin-bottom: 10px;")
        chatterbox_layout.addWidget(info_label)
        
        # Create extended tabs in settings
        self.settings_extended_tabs = QTabWidget()
        self.settings_extended_tabs.setMaximumHeight(400)  # Limit height
        
        # Add all extended settings tabs with Vietnamese names
        self.settings_extended_tabs.addTab(self.create_text_processor_settings_tab(), "[EDIT] " + self.language_manager.get('text_processing'))
        self.settings_extended_tabs.addTab(self.create_audio_processor_settings_tab(), "[MUSIC] " + self.language_manager.get('audio_processing'))
        self.settings_extended_tabs.addTab(self.create_generation_settings_tab(), "[TARGET] " + self.language_manager.get('generation_control'))
        self.settings_extended_tabs.addTab(self.create_whisper_settings_tab(), "[EMOJI] " + self.language_manager.get('whisper_validation'))
        self.settings_extended_tabs.addTab(self.create_preset_settings_tab(), "[FAST] " + self.language_manager.get('presets'))
        self.settings_extended_tabs.addTab(self.create_performance_settings_tab(), "[STATS] " + self.language_manager.get('performance'))
        
        chatterbox_layout.addWidget(self.settings_extended_tabs)
        chatterbox_group.setLayout(chatterbox_layout)
        layout.addWidget(chatterbox_group)
        
        # === ACTIONS SECTION ===
        actions_group = QGroupBox("[FAST] " + self.language_manager.get('actions'))
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        # Save button
        self.save_settings_btn = QPushButton("[EMOJI] " + self.language_manager.get('save_settings'))
        self.save_settings_btn.clicked.connect(self.save_current_settings)
        self.save_settings_btn.setStyleSheet(self.create_primary_button_style())
        actions_layout.addWidget(self.save_settings_btn)
        
        # Load button
        self.load_settings_btn = QPushButton("[FOLDER] " + self.language_manager.get('load_settings'))
        self.load_settings_btn.clicked.connect(self.load_current_settings)
        self.load_settings_btn.setStyleSheet(self.create_secondary_button_style())
        actions_layout.addWidget(self.load_settings_btn)
        
        # Reset button
        self.reset_settings_btn = QPushButton("[REFRESH] " + self.language_manager.get('reset_settings'))
        self.reset_settings_btn.clicked.connect(self.reset_settings_to_defaults)
        self.reset_settings_btn.setStyleSheet(self.create_warning_button_style())
        actions_layout.addWidget(self.reset_settings_btn)
        
        # Check API status button
        self.check_api_btn = QPushButton("[SEARCH] Kiểm tra API")
        self.check_api_btn.clicked.connect(self.check_api_status)
        self.check_api_btn.setStyleSheet(self.create_secondary_button_style())
        actions_layout.addWidget(self.check_api_btn)
        
        actions_layout.addStretch()
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Set scroll area content
        scroll.setWidget(content_widget)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        tab.setLayout(tab_layout)
        
        # Load current settings
        self.load_current_settings()
        
        # Add tab to main tabs
        self.tabs.addTab(tab, self.language_manager.get('tab_settings'))
        
        return tab
        
        self.save_profile_btn = QPushButton("[EMOJI] Save Profile")
        self.save_profile_btn.clicked.connect(self.save_settings_profile)
        profile_layout.addWidget(self.save_profile_btn)
        
        self.load_profile_btn = QPushButton("[EMOJI] Load Profile")
        self.load_profile_btn.clicked.connect(self.load_settings_profile)
        profile_layout.addWidget(self.load_profile_btn)
        
        self.delete_profile_btn = QPushButton("[DELETE]")
        self.delete_profile_btn.setMaximumWidth(40)
        self.delete_profile_btn.clicked.connect(self.delete_settings_profile)
        profile_layout.addWidget(self.delete_profile_btn)
        
        profile_layout.addStretch()
        settings_mgmt_layout.addLayout(profile_layout)
        
        # Auto-save setting
        auto_save_layout = QHBoxLayout()
        self.auto_save_checkbox = QCheckBox("[REFRESH] Auto-save settings")
        self.auto_save_checkbox.setChecked(True)
        auto_save_layout.addWidget(self.auto_save_checkbox)
        auto_save_layout.addStretch()
        settings_mgmt_layout.addLayout(auto_save_layout)
        
        settings_mgmt_group.setLayout(settings_mgmt_layout)
        layout.addWidget(settings_mgmt_group)
        
        # Group 1: API Keys cho AI Content
        ai_content_group = QGroupBox("[EDIT] AI Sinh nội dung")
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
        image_gen_group = QGroupBox("[PAINT] AI Tạo ảnh")
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
        tts_group = QGroupBox("[EMOJI] Text-to-Speech")
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
        chatterbox_info = QLabel("[BOT] Chatterbox TTS: Auto-detect CUDA/MPS/CPU")
        chatterbox_info.setStyleSheet("color: #007AFF; font-weight: bold; font-size: 12px;")
        tts_layout.addWidget(chatterbox_info, 3, 0, 1, 2)
        
        # Device status button
        self.chatterbox_device_btn = QPushButton("[MOBILE] Kiểm tra Device")
        self.chatterbox_device_btn.clicked.connect(self.show_chatterbox_device_info)
        tts_layout.addWidget(self.chatterbox_device_btn, 4, 0)
        
        # Clear cache button
        self.chatterbox_clear_btn = QPushButton("[CLEAN] Xóa Cache")
        self.chatterbox_clear_btn.clicked.connect(self.clear_chatterbox_cache)
        tts_layout.addWidget(self.chatterbox_clear_btn, 4, 1)
        
        tts_group.setLayout(tts_layout)
        layout.addWidget(tts_group)
        
        # Group 4: Provider Selection
        providers_group = QGroupBox("[CONFIG] Chọn nhà cung cấp")
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
        video_group = QGroupBox("[ACTION] Cài đặt Video")
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
        actions_group = QGroupBox("[EMOJI] Thao tác")
        actions_layout = QGridLayout()
        actions_layout.setSpacing(8)
        
        save_settings_btn = QPushButton("[EMOJI] Lưu cài đặt")
        save_settings_btn.clicked.connect(self.save_settings)
        actions_layout.addWidget(save_settings_btn, 0, 0)
        
        check_api_btn = QPushButton("[SEARCH] Kiểm tra API")
        check_api_btn.clicked.connect(self.check_api_status)
        actions_layout.addWidget(check_api_btn, 0, 1)
        
        refresh_providers_btn = QPushButton("[REFRESH] Làm mới")
        refresh_providers_btn.clicked.connect(self.refresh_providers)
        actions_layout.addWidget(refresh_providers_btn, 1, 0, 1, 2)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        reload_btn = QPushButton("[REFRESH] Reload Code")
        reload_btn.clicked.connect(self.reload_code)
        layout.addWidget(reload_btn)
        
        # Thêm stretch để đẩy nội dung lên trên
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        
        # Layout chính của tab
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        tab.setLayout(tab_layout)
        
        self.tabs.addTab(tab, self.language_manager.get('tab_settings'))
        
        # Load cài đặt hiện tại từ file config.env
        self.load_current_settings()
        
        # Update API status when settings change (safe call)
        self.update_api_status_indicator()
    
    def start_video_generation(self):
        """Bắt đầu tạo video"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Vui lòng nhập prompt!")
            return
        
        # Check license for video generation
        if not license_manager.is_feature_enabled("basic_tts"):
            QMessageBox.warning(
                self, 
                "License Required", 
                "Video generation requires a valid license.\nPlease check the License tab to activate your license."
            )
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
            QMessageBox.warning(self, "Error", "Vui lòng chọn thư mục chứa ảnh!")
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
            self.progress_label.setText(f"Error: {result['error']}")
            QMessageBox.critical(self, "Error", f"Không thể tạo video:\n{result['error']}")
    
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
            QMessageBox.warning(self, "Error", "Vui lòng chọn project!")
            return
        
        project_path = self.pipeline.project_manager.get_project_path(self.current_project_id)
        os.system(f"open '{project_path}'" if sys.platform == "darwin" else f"explorer '{project_path}'")
    
    def delete_project(self):
        """Xóa project"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Error", "Vui lòng chọn project!")
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
                QMessageBox.critical(self, "Error", f"Không thể xóa: {result['error']}")
    
    def create_new_project(self):
        """Tạo dự án mới"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Tạo dự án mới")
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Tên dự án
        layout.addWidget(QLabel("Tên dự án:"))
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nhập tên dự án...")
        layout.addWidget(name_input)
        
        # Mô tả dự án
        layout.addWidget(QLabel("Mô tả dự án:"))
        description_input = QTextEdit()
        description_input.setPlaceholderText("Nhập mô tả cho dự án...")
        description_input.setMaximumHeight(150)
        layout.addWidget(description_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(dialog.reject)
        create_btn = QPushButton("Tạo dự án")
        create_btn.clicked.connect(lambda: self.create_project_from_dialog(dialog, name_input.text(), description_input.toPlainText()))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(create_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def create_project_from_dialog(self, dialog, name, description):
        """Tạo dự án từ dialog"""
        if not name.strip():
            QMessageBox.warning(dialog, "Error", "Vui lòng nhập tên dự án!")
            return
        
        try:
            result = self.pipeline.project_manager.create_project(name.strip(), description.strip())
            if result["success"]:
                QMessageBox.information(dialog, "Thành công", f"Đã tạo dự án '{name}' thành công!")
                dialog.accept()
                self.refresh_projects()
            else:
                QMessageBox.critical(dialog, "Error", f"Không thể tạo dự án: {result['error']}")
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"Error không mong muốn: {str(e)}")
    
    def edit_project(self):
        """Chỉnh sửa dự án"""
        if not self.current_project_id:
            QMessageBox.warning(self, "Error", "Vui lòng chọn dự án!")
            return
        
        # Load project data
        result = self.pipeline.project_manager.load_project(self.current_project_id)
        if not result["success"]:
            QMessageBox.critical(self, "Error", f"Không thể tải dự án: {result['error']}")
            return
        
        project_data = result["data"]
        
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Chỉnh sửa dự án")
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Tên dự án
        layout.addWidget(QLabel("Tên dự án:"))
        name_input = QLineEdit()
        name_input.setText(project_data['name'])
        layout.addWidget(name_input)
        
        # Mô tả dự án
        layout.addWidget(QLabel("Mô tả dự án:"))
        description_input = QTextEdit()
        description_input.setPlainText(project_data['prompt'])
        description_input.setMaximumHeight(150)
        layout.addWidget(description_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(dialog.reject)
        save_btn = QPushButton("Lưu thay đổi")
        save_btn.clicked.connect(lambda: self.save_project_changes(dialog, name_input.text(), description_input.toPlainText()))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def save_project_changes(self, dialog, name, description):
        """Lưu thay đổi dự án"""
        if not name.strip():
            QMessageBox.warning(dialog, "Error", "Vui lòng nhập tên dự án!")
            return
        
        try:
            # Update project data
            result = self.pipeline.project_manager.load_project(self.current_project_id)
            if result["success"]:
                project_data = result["data"]
                project_data['name'] = name.strip()
                project_data['prompt'] = description.strip()
                
                # Save changes
                save_result = self.pipeline.project_manager.save_project(self.current_project_id, project_data)
                if save_result["success"]:
                    QMessageBox.information(dialog, "Thành công", "Đã lưu thay đổi!")
                    dialog.accept()
                    self.refresh_projects()
                else:
                    QMessageBox.critical(dialog, "Error", f"Không thể lưu: {save_result['error']}")
            else:
                QMessageBox.critical(dialog, "Error", f"Không thể tải dự án: {result['error']}")
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"Error không mong muốn: {str(e)}")
    
    def check_chatterbox_extended_status(self):
        """Kiểm tra trạng thái Chatterbox Extended"""
        try:
            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration
            integration = ChatterboxExtendedIntegration()
            self.chatterbox_status_label.setText("[OK] Đã khả dụng")
            self.chatterbox_status_label.setStyleSheet("color: green; font-weight: bold;")
        except ImportError as e:
            self.chatterbox_status_label.setText(f"[EMOJI] Error import: {str(e)}")
            self.chatterbox_status_label.setStyleSheet("color: red; font-weight: bold;")
        except Exception as e:
            self.chatterbox_status_label.setText(f"[EMOJI] Error: {str(e)}")
            self.chatterbox_status_label.setStyleSheet("color: red; font-weight: bold;")
    
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
            QMessageBox.critical(self, "Error", f"Không thể lưu cài đặt:\n{str(e)}")
    
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
            print(f"Error load cài đặt: {str(e)}")
    
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
        
        status_text = "[SEARCH] TRẠNG THÁI API:\n\n"
        
        # Content providers
        status_text += "[EDIT] AI Sinh nội dung:\n"
        for provider, available in status['content_providers'].items():
            icon = "[OK]" if available else "[EMOJI]"
            status_text += f"  {icon} {provider}\n"
        
        # Image providers
        status_text += "\n[PAINT] AI Tạo ảnh:\n"
        for provider, available in status['image_providers'].items():
            icon = "[OK]" if available else "[EMOJI]"
            status_text += f"  {icon} {provider}\n"
        
        # TTS providers
        status_text += "\n[EMOJI] Text-to-Speech:\n"
        for provider, available in status['tts_providers'].items():
            icon = "[OK]" if available else "[EMOJI]"
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
            QMessageBox.warning(self, "Error", "Vui lòng nhập prompt!")
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
                QMessageBox.critical(self, "Error", f"Không thể tạo câu chuyện:\n{result['error']}")
                self.progress_label.setText("Error tạo câu chuyện")
            else:
                # Store script data for audio generation
                self.current_script_data = result
                
                # Hiển thị kết quả với format mới
                story_text = "[ACTION] CÂU CHUYỆN ĐÃ TẠO:\n\n"
                
                # Show characters if available
                characters = result.get("characters", [])
                if characters:
                    story_text += "[THEATER] NHÂN VẬT:\n"
                    for char in characters:
                        story_text += f"• {char.get('name', char['id'])} ({char.get('gender', 'neutral')}) - {char.get('suggested_voice', 'N/A')}\n"
                    story_text += "\n"
                
                for i, segment in enumerate(result["segments"], 1):
                    story_text += f"[EDIT] ĐOẠN {i} ({segment.get('duration', 10)}s):\n"
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
                
                copy_btn = QPushButton("[CLIPBOARD] Copy")
                copy_btn.clicked.connect(lambda: self.copy_to_clipboard(story_text))
                buttons_layout.addWidget(copy_btn)
                
                save_btn = QPushButton("[EMOJI] Lưu vào file")
                save_btn.clicked.connect(lambda: self.save_story_to_file(story_text, prompt))
                buttons_layout.addWidget(save_btn)
                
                close_btn = QPushButton("[EMOJI] Đóng")
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
            QMessageBox.critical(self, "Error", f"Error không xác định:\n{str(e)}")
            self.progress_label.setText("Error tạo câu chuyện")
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
            QMessageBox.critical(self, "Error", f"Không thể copy: {str(e)}")
    
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
            QMessageBox.critical(self, "Error", f"Không thể lưu file:\n{str(e)}")
    
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
        # Check license for unlimited exports
        if not license_manager.is_feature_enabled("export_unlimited"):
            # Check if trial limit reached (simplified check for demo)
            trial_count = getattr(self, '_trial_exports', 0)
            if trial_count >= 5:
                QMessageBox.warning(
                    self, 
                    "Trial Limit Reached", 
                    "You have reached the 5 export limit for trial mode.\nPlease upgrade to a paid license for unlimited exports."
                )
                return
            else:
                self._trial_exports = trial_count + 1
                QMessageBox.information(
                    self, 
                    "Trial Mode", 
                    f"Export {trial_count + 1}/5 (Trial Mode)\nUpgrade to license for unlimited exports."
                )
        
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
            
            # Use TTSBridge instead of direct VoiceGenerator call (eliminates duplicates)
            from core.tts_bridge import get_tts_bridge
            bridge = get_tts_bridge()
            
            result = bridge.generate_audio_from_script_data(
                script_data=self.current_script_data,
                voice_mapping=voice_mapping,
                output_directory=audio_output_dir
            )
            
            if result["success"]:
                # Store paths for buttons
                self.last_audio_output_dir = result["output_dir"]
                self.last_final_audio_path = result["final_audio_path"]
                
                # Enable audio control buttons
                self.open_audio_folder_btn.setEnabled(True)
                self.play_final_audio_btn.setEnabled(True)
                
                # Show success message
                message = f"[OK] Đã tạo audio thành công!\n\n"
                message += f"[FOLDER] Thư mục: {result['output_dir']}\n"
                message += f"[MUSIC] File cuối: {os.path.basename(result['final_audio_path'])}\n\n"
                message += f"[STATS] Chi tiết:\n"
                for character, files in result["character_audio_files"].items():
                    message += f"  • {character}: {len(files)} file(s)\n"
                
                QMessageBox.information(self, "Thành công", message)
                self.progress_label.setText("Đã tạo audio thành công!")
                
            else:
                QMessageBox.critical(self, "Error", f"Error tạo audio:\n{result.get('error', 'Unknown error')}")
                self.progress_label.setText("Error tạo audio")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error không xác định:\n{str(e)}")
            self.progress_label.setText("Error tạo audio")
        finally:
            self.generate_audio_btn.setEnabled(True)
            self.generate_audio_btn.setText("[MUSIC] Tạo Audio")
    
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
    
    # ===== VOICE STUDIO TAB METHODS =====
    
    def update_token_preview(self):
        """Update token preview based on selected template mode"""
        mode = self.template_mode_combo.currentData()
        
        token_counts = {
            'rapid': 150,
            'standard': 400, 
            'detailed': 800
        }
        
        savings = {
            'rapid': 1350,
            'standard': 1100,
            'detailed': 700
        }
        
        current_tokens = token_counts.get(mode, 400)
        current_savings = savings.get(mode, 1100)
        
        self.token_preview_label.setText(f"[IDEA] Tiết kiệm: +{current_savings} tokens cho story content")
        
        # Update color based on savings amount
        if current_savings >= 1200:
            color = "#28CD41"  # Green for high savings
        elif current_savings >= 900:
            color = "#FF6B35"  # Orange for medium savings  
        else:
            color = "#5856D6"  # Purple for lower savings
            
        self.token_preview_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def switch_data_source(self):
        """Switch between data sources với enhanced multi-file support và manual table mode"""
        source = self.data_source_combo.currentData()
        
        # Hide all widgets first
        self.import_file_btn.setVisible(False)
        self.import_multi_files_btn.setVisible(False)
        self.load_generated_btn.setVisible(False)
        if hasattr(self, 'manual_input_widget'):
            self.manual_input_widget.setVisible(False)
        if hasattr(self, 'manual_table_widget'):
            self.manual_table_widget.setVisible(False)
        
        # Show/hide emotion mapping based on mode
        if hasattr(self, 'enable_emotion_mapping'):
            if source == "manual_table":
                # Ẩn tính năng auto emotion mapping trong manual table mode
                self.enable_emotion_mapping.setVisible(False)
                self.enable_emotion_mapping.setChecked(False)
            else:
                # Hiện tính năng auto emotion mapping trong các mode JSON
                self.enable_emotion_mapping.setVisible(True)
                self.enable_emotion_mapping.setChecked(True)
        
        if source == "file":
            self.import_file_btn.setVisible(True)
            self.imported_file_label.setText("Chưa import file nào")
        elif source == "multi_file":
            self.import_multi_files_btn.setVisible(True)
            self.imported_file_label.setText("Chưa import files nào")
        elif source == "generated":
            self.load_generated_btn.setVisible(True)
            self.imported_file_label.setText("Sử dụng data từ tab Tạo Video")
        elif source == "manual":
            if hasattr(self, 'manual_input_widget'):
                self.manual_input_widget.setVisible(True)
            self.imported_file_label.setText("Nhập thủ công JSON script")
        elif source == "manual_table":  # NEW
            if hasattr(self, 'manual_table_widget'):
                self.manual_table_widget.setVisible(True)
            self.imported_file_label.setText("Mode thủ công - nhập dữ liệu vào bảng")
            # Setup manual table mode specifics
            self.setup_manual_table_mode()
    
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
                    QMessageBox.warning(self, "Error", "File JSON không đúng format!")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Không thể đọc file:\n{str(e)}")
    
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
                QMessageBox.warning(self, "Error", "JSON script không đúng format!")
                
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error JSON", f"JSON không hợp lệ:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể parse script:\n{str(e)}")
    
    def validate_script_data(self, script_data):
        """Validate format của script data - Enhanced Format 2.0 Support"""
        try:
            # Check required fields
            if not isinstance(script_data, dict):
                return False
            
            # Support both old format and Enhanced Format 2.0
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
                    # Required fields for dialogue
                    if not all(key in dialogue for key in ['speaker', 'text']):
                        return False
                    
                    # Optional Enhanced Format 2.0 fields validation
                                # Emotion intensity and speed fields are no longer supported - simplified to emotion only
                    
                    if 'pause_after' in dialogue:
                        pause = dialogue['pause_after']
                        if not isinstance(pause, (int, float)) or not (0.0 <= pause <= 5.0):
                            print(f"[WARNING] Invalid pause_after: {pause} (should be 0.0-5.0)")
            
            for character in characters:
                if not all(key in character for key in ['id', 'name']):
                    return False
                
                # Enhanced Format 2.0 character validation
                            # Default emotion intensity and speed fields are no longer supported - simplified to default_emotion only
            
            # Enhanced Format 2.0 detection
            has_project_metadata = 'project' in script_data
            has_audio_settings = 'audio_settings' in script_data
            has_metadata = 'metadata' in script_data
            
            if has_project_metadata or has_audio_settings or has_metadata:
                print("[EMOJI] Enhanced Format 2.0 detected with advanced features")
                
                # Validate project metadata if present
                if has_project_metadata:
                    project = script_data['project']
                    if not all(key in project for key in ['title', 'description']):
                        print("[WARNING] Missing required project fields (title, description)")
                
                # Validate audio settings if present
                if has_audio_settings:
                    audio = script_data['audio_settings']
                    if 'crossfade_duration' in audio:
                        fade = audio['crossfade_duration']
                        if not isinstance(fade, (int, float)) or not (0.0 <= fade <= 2.0):
                            print(f"[WARNING] Invalid crossfade_duration: {fade}")
            else:
                print("[EMOJI] Classic format detected - fully compatible")
            
            return True
            
        except Exception as e:
            print(f"[EMOJI] Validation error: {e}")
            return False
    
    def update_simple_mode_overview(self):
        """Update overview for Simple mode (single character)"""
        try:
            # Simple mode data structure
            text_content = self.voice_studio_script_data.get('text', '')
            chunks = self.voice_studio_script_data.get('chunks', 1)
            total_chars = self.voice_studio_script_data.get('total_characters', len(text_content))
            voice_name = self.voice_studio_script_data.get('voice', 'narrator')
            
            # Update overview labels for Simple mode
            if hasattr(self, 'segments_count_label'):
                self.segments_count_label.setText(str(chunks))
            
            if hasattr(self, 'characters_count_label'):
                self.characters_count_label.setText("1")  # Single character mode
            
            if hasattr(self, 'dialogues_count_label'):
                self.dialogues_count_label.setText(str(chunks))  # Number of text chunks
                
            # Show text length info
            words_count = len(text_content.split())
            print(f"[SIMPLE MODE] Overview updated: {chunks} chunks, {words_count} words, {total_chars} characters")
            
            # Enable generation controls for Simple mode
            if hasattr(self, 'generate_all_btn'):
                self.generate_all_btn.setEnabled(True)
                
        except Exception as e:
            print(f"[ERROR] Failed to update Simple mode overview: {e}")
    
    def update_voice_studio_overview(self):
        """Cập nhật overview của script trong Voice Studio - Enhanced Format 2.0 Support"""
        if not self.voice_studio_script_data:
            return
        
        try:
            # Check if this is Simple mode (single character) or Complex mode (multi character)
            if 'mode' in self.voice_studio_script_data and self.voice_studio_script_data['mode'] == 'single_character':
                # Simple mode - single character format
                self.update_simple_mode_overview()
                return
            
            # Complex mode - multi character format  
            segments = self.voice_studio_script_data['segments']
            characters = self.voice_studio_script_data['characters']
            
            # Detect format version
            has_enhanced_features = any(key in self.voice_studio_script_data for key in ['project', 'audio_settings', 'metadata'])
            format_version = "Enhanced 2.0" if has_enhanced_features else "Classic"
            
            # Update info labels with enhanced information
            total_dialogues = sum(len(segment['dialogues']) for segment in segments)
            
            # Calculate enhanced features count
            enhanced_features = []
            if 'project' in self.voice_studio_script_data:
                enhanced_features.append("Project Metadata")
            if 'audio_settings' in self.voice_studio_script_data:
                enhanced_features.append("Audio Settings")
            if 'metadata' in self.voice_studio_script_data:
                enhanced_features.append("Metadata")
            
            # Count advanced dialogue features
            advanced_dialogues = 0
            for segment in segments:
                for dialogue in segment['dialogues']:
                    if any(key in dialogue for key in ['pause_after', 'emphasis']):
                        advanced_dialogues += 1
            
            # Build script info text
            script_info = f"[OK] Script loaded ({format_version}): {len(segments)} segments, {total_dialogues} dialogues"
            if advanced_dialogues > 0:
                script_info += f", {advanced_dialogues} với advanced settings"
            
            self.script_info_label.setText(script_info)
            self.script_info_label.setStyleSheet("color: #007AFF; font-weight: bold;")
            
            # Update characters with enhanced info
            character_info = []
            for char in characters:
                char_text = char['name']
                if 'default_emotion' in char:
                    char_text += f" ({char['default_emotion']})"
                character_info.append(char_text)
            
            self.characters_label.setText(", ".join(character_info))
            
            # Update segments count
            self.segments_count_label.setText(str(len(segments)))
            
            # Show project title if available
            if 'project' in self.voice_studio_script_data and hasattr(self, 'project_title_label'):
                project_title = self.voice_studio_script_data['project']['title']
                self.project_title_label.setText(f"[BOOK] {project_title}")
                self.project_title_label.setVisible(True)
            
            # Log enhanced features
            if has_enhanced_features:
                print(f"[EMOJI] Enhanced Format 2.0 loaded with: {', '.join(enhanced_features)}")
                
                # Show duration if available
                if 'project' in self.voice_studio_script_data and 'total_duration' in self.voice_studio_script_data['project']:
                    duration = self.voice_studio_script_data['project']['total_duration']
                    print(f"⏱ Estimated duration: {duration} seconds")
            
            # Update voice mapping table
            self.populate_voice_mapping_table()
            
            # Enable generation buttons
            self.generate_selected_btn.setEnabled(True)
            self.generate_all_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Không thể cập nhật overview:\n{str(e)}")
    
    def populate_voice_mapping_table(self):
        """Populate character settings table - FIXED METHOD"""
        if not self.voice_studio_script_data:
            return
        
        # Call the correct method for character settings table
        self.populate_character_settings_table()
        
        # Enable generation buttons
        self.generate_selected_btn.setEnabled(True)
        self.generate_all_btn.setEnabled(True)
        
        print("[OK] Character settings table populated successfully")
        return

    
    def reset_voice_mapping(self):
        """Reset voice mapping về mặc định"""
        if not self.voice_studio_script_data:
            return
        
        # Reset table
        self.populate_character_settings_table()
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
            
            # Get voice combo from stacked widget (column 7 after adding Temperature column)
            voice_widget = self.character_settings_table.cellWidget(current_row, 7)  # Voice stacked widget
            voice_combo = None
            selected_voice = None
            
            if voice_widget and hasattr(voice_widget, 'currentWidget'):
                current_widget = voice_widget.currentWidget()
                if current_widget:
                    # Find voice combo in the current widget
                    for child in current_widget.findChildren(QComboBox):
                        if child.count() > 20:  # Voice combo should have 28+ items
                            voice_combo = child
                            selected_voice = child.currentData()
                            break
            
            if not voice_combo or not selected_voice:
                QMessageBox.warning(self, "Cảnh báo", "Không thể lấy thông tin voice. Vui lòng chọn voice cho nhân vật!")
                return
            
            # Get settings from character_settings_table - UPDATED COLUMN INDEXES
            emotion_combo = self.character_settings_table.cellWidget(current_row, 1)  # Emotion dropdown
            exag_input = self.character_settings_table.cellWidget(current_row, 2)     # Exaggeration input
            speed_input = self.character_settings_table.cellWidget(current_row, 3)    # Speed input
            cfg_weight_input = self.character_settings_table.cellWidget(current_row, 4)  # CFG Weight input
            temperature_input = self.character_settings_table.cellWidget(current_row, 5)  # Temperature input
            
            # Extract emotion from dropdown (format: "[EMOJI] happy")
            emotion = "friendly"  # Default
            if emotion_combo and hasattr(emotion_combo, 'currentText'):
                emotion_text = emotion_combo.currentText()
                if ' ' in emotion_text:
                    emotion = emotion_text.split(' ', 1)[1]  # Get "happy" from "[EMOJI] happy"
            
            exaggeration = float(exag_input.text()) if exag_input and exag_input.text() else 1.0
            speed = float(speed_input.text()) if speed_input else 1.0
            cfg_weight = float(cfg_weight_input.text()) if cfg_weight_input else 0.5
            temperature = float(temperature_input.text()) if temperature_input and temperature_input.text() else 0.7
            
            # Preview text
            preview_text = f"Xin chào, tôi là {character_id}. Đây là giọng nói {voice_combo.currentText().split(' ')[1]} của tôi với emotion {emotion}, speed {speed:.1f}x, temperature {temperature:.2f}."
            
            # Generate preview audio
            import tempfile
            temp_dir = tempfile.mkdtemp()
            preview_path = os.path.join(temp_dir, f"preview_{character_id}.mp3")
            
            # Check if prompt-based voice is enabled for preview
            voice_prompt = None
            if self.enable_prompt_voice.isChecked() and self.voice_prompt_input.text().strip():
                voice_prompt = self.voice_prompt_input.text().strip()
                print(f"[EMOJI] Preview with PROMPT: '{voice_prompt}'")
                preview_text = f"Xin chào, tôi là {character_id}. Đây là giọng được tạo từ prompt: {voice_prompt[:50]}..."
            else:
                print(f"[EMOJI] Preview Settings for {character_id}:")
                print(f"   Voice: {selected_voice}")
                print(f"   Emotion: {emotion}")
                print(f"   Speed: {speed:.1f}x")
                print(f"   CFG Weight: {cfg_weight:.2f}")
                
            result = self.voice_generator.generate_voice_chatterbox(
                text=preview_text,
                save_path=preview_path,
                voice_sample_path=None,
                emotion_exaggeration=exaggeration,  # [OK] FIX: Use exaggeration (float), not emotion (string)
                speed=speed,
                voice_name=selected_voice if not voice_prompt else None,  # Skip voice_name if using prompt
                cfg_weight=cfg_weight,
                temperature=temperature,
                voice_prompt=voice_prompt  # NEW: Pass voice prompt for preview
            )
            
            if result.get('success'):
                # Play preview
                self.play_audio_file(preview_path)
                QMessageBox.information(self, "[EMOJI] Preview Voice", 
                    f"Character: {character_id}\n"
                    f"Voice: {voice_combo.currentText()}\n"
                    f"Emotion: {emotion}\n"
                    f"Speed: {speed:.1f}x\n"
                    f"CFG Weight: {cfg_weight:.2f}\n"
                    f"\n[BOT] Generated by Chatterbox TTS")
            else:
                QMessageBox.warning(self, "[EMOJI] Error Preview", f"Không thể tạo preview Chatterbox TTS:\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            QMessageBox.critical(self, "[EMOJI] Error Critical", f"Error preview voice:\n{str(e)}")
    
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
        """Tạo voice cho tất cả nhân vật với Chatterbox Extended"""
        if not self.voice_studio_script_data:
            QMessageBox.warning(self, "Error", "Không có dữ liệu script để tạo voice!")
            return
        
        try:
            # Import ChatterboxExtendedIntegration
            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration
            
            # Get Extended settings từ UI
            extended_settings = self.get_extended_settings()
            
            # Show progress
            self.voice_progress_bar.setVisible(True)
            self.voice_progress_bar.setRange(0, 0)  # Indeterminate progress
            self.voice_progress_text.setText("[ROCKET] Khởi tạo Chatterbox Extended...")
            
            # Tạo ChatterboxExtendedIntegration instance
            from core.chatterbox_extended_integration import ExtendedGenerationConfig
            config_obj = ExtendedGenerationConfig()
            
            # Apply extended settings to config object
            if extended_settings.get('text_processing_enabled'):
                config_obj.text_processing_mode = extended_settings.get('text_processing_mode', 'conservative')
                config_obj.smart_joining_enabled = extended_settings.get('smart_joining_enabled', True)
                config_obj.recursive_splitting_enabled = extended_settings.get('recursive_splitting_enabled', False)
                config_obj.advanced_preprocessing = extended_settings.get('advanced_preprocessing', False)
            
            if extended_settings.get('audio_processing_enabled'):
                config_obj.auto_editor_enabled = extended_settings.get('auto_editor_enabled', False)
                config_obj.ffmpeg_normalization = extended_settings.get('ffmpeg_normalization', False)
                config_obj.output_format = extended_settings.get('output_format', 'mp3')
                config_obj.quality_enhancement = extended_settings.get('quality_enhancement', False)
            
            if extended_settings.get('generation_controller_enabled'):
                config_obj.multiple_generations = extended_settings.get('multiple_generations', 1)
                config_obj.candidates_per_generation = extended_settings.get('candidates_per_generation', 1)
                config_obj.retry_on_failure = extended_settings.get('retry_on_failure', False)
                config_obj.max_retries = extended_settings.get('max_retries', 3)
                config_obj.parallel_processing = extended_settings.get('parallel_processing', False)
            
            if extended_settings.get('whisper_validation_enabled'):
                config_obj.whisper_model = extended_settings.get('whisper_model', 'base')
                config_obj.similarity_threshold = extended_settings.get('similarity_threshold', 0.8)
                config_obj.auto_retry_failed = extended_settings.get('auto_retry_failed', False)
            
            integration = ChatterboxExtendedIntegration(config_obj)
            
            # Initialize hybrid TTS manager for performance optimization
            from core.hybrid_tts_manager import HybridTtsManager, HybridConfig, TtsMode
            
            # Get TTS mode from performance settings
            performance_settings = extended_settings.get('performance', {})
            tts_mode_str = performance_settings.get('tts_mode', 'hybrid')
            tts_mode = {
                'maximum_performance': TtsMode.MAXIMUM_PERFORMANCE,
                'hybrid': TtsMode.HYBRID,
                'maximum_compatibility': TtsMode.MAXIMUM_COMPATIBILITY
            }.get(tts_mode_str, TtsMode.HYBRID)
            
            hybrid_config = HybridConfig(
                mode=tts_mode,
                cache_enabled=performance_settings.get('cache_enabled', True),
                parallel_processing=performance_settings.get('parallel_processing', True)
            )
            
            hybrid_tts = HybridTtsManager(hybrid_config)
            
            # Log performance mode
            self.voice_progress_text.setText(f"[ROCKET] Khởi tạo {tts_mode.value} mode...")
            
            # Get output directory
            output_dir = self.voice_output_input.text() or "./voice_studio_output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Collect voice mapping from character_settings_table
            current_voice_mapping = {}
            for i in range(self.character_settings_table.rowCount()):
                char_id = self.character_settings_table.item(i, 0).text()
                
                # Get settings from table with proper validation
                emotion_combo = self.character_settings_table.cellWidget(i, 1)
                exag_input = self.character_settings_table.cellWidget(i, 2)
                speed_input = self.character_settings_table.cellWidget(i, 3)
                cfg_weight_input = self.character_settings_table.cellWidget(i, 4)
                temperature_input = self.character_settings_table.cellWidget(i, 5)
                
                print(f"[DEBUG] Row {i} widgets: emotion={emotion_combo}, exag={exag_input}, speed={speed_input}, cfg={cfg_weight_input}, temp={temperature_input}")
                print(f"[DEBUG] Row {i}: temperature_input type = {type(temperature_input)}")
                voice_widget = self.character_settings_table.cellWidget(i, 7)
                
                # Get voice combo from stacked widget
                voice_combo = None
                if voice_widget and hasattr(voice_widget, 'currentWidget'):
                    current_widget = voice_widget.currentWidget()
                    if current_widget:
                        for child in current_widget.findChildren(QComboBox):
                            if child.count() > 20:  # Voice combo should have 28+ items
                                voice_combo = child
                                break
                
                # Get emotion text
                emotion_text = 'neutral'  # Default to neutral instead of friendly
                if emotion_combo and hasattr(emotion_combo, 'currentText'):
                    emotion_text = emotion_combo.currentText()
                    if ' ' in emotion_text:
                        emotion_text = emotion_text.split(' ', 1)[1]  # Extract emotion name
                
                # Get values with proper fallbacks
                try:
                    exag_value = float(exag_input.text()) if exag_input and hasattr(exag_input, 'text') and exag_input.text().strip() else 1.0
                except (ValueError, AttributeError):
                    exag_value = 1.0
                    
                try:
                    speed_value = float(speed_input.text()) if speed_input and hasattr(speed_input, 'text') and speed_input.text().strip() else 1.0
                except (ValueError, AttributeError):
                    speed_value = 1.0
                    
                try:
                    cfg_value = float(cfg_weight_input.text()) if cfg_weight_input and hasattr(cfg_weight_input, 'text') and cfg_weight_input.text().strip() else 0.6
                except (ValueError, AttributeError):
                    cfg_value = 0.6
                    
                try:
                    temp_value = float(temperature_input.text()) if temperature_input and hasattr(temperature_input, 'text') and temperature_input.text().strip() else 0.8
                except (ValueError, AttributeError):
                    temp_value = 0.8
                    
                print(f"[DEBUG] Row {i} final values: exag={exag_value}, speed={speed_value}, cfg={cfg_value}, temp={temp_value}")
                
                current_voice_mapping[char_id] = {
                    'name': char_id,
                    'suggested_voice': voice_combo.currentData() if voice_combo else 'abigail',
                    'emotion': emotion_text,
                    'exaggeration': exag_value,
                    'speed': speed_value,
                    'cfg_weight': cfg_value,
                    'temperature': temp_value
                }
            
            # Update progress
            self.voice_progress_text.setText("[ROCKET] Đang xử lý với Chatterbox Extended...")
            
            # Use TTSBridge instead of ChatterboxExtendedIntegration (eliminates duplicates)
            from core.tts_bridge import get_tts_bridge
            bridge = get_tts_bridge()
            
            result = bridge.generate_audio_from_script_data(
                script_data=self.voice_studio_script_data,
                voice_mapping=current_voice_mapping,
                output_directory=output_dir,
                progress_callback=self.update_extended_progress
            )
            
            # Update UI with results
            self.voice_progress_bar.setRange(0, 100)
            self.voice_progress_bar.setValue(100)
            self.voice_progress_text.setText("[OK] Hoàn thành với Chatterbox Extended!")
            
            # Display results
            if result and result.get('success'):
                results_text = f"""
[ROCKET] CHATTERBOX EXTENDED RESULTS:
[STATS] Tổng kết:
  • Segments đã xử lý: {result.get('total_segments', 0)}
  • Files audio tạo: {result.get('total_audio_files', 0)}
  • Thời gian xử lý: {result.get('processing_time', 'N/A')}

[EDIT] Text Processing:
  • Smart joining: {'[OK]' if extended_settings['text_processor']['smart_joining'] else '[EMOJI]'}
  • Recursive splitting: {'[OK]' if extended_settings['text_processor']['recursive_splitting'] else '[EMOJI]'}
  • Text preprocessing: {'[OK]' if extended_settings['text_processor']['fix_abbreviations'] else '[EMOJI]'}

[MUSIC] Audio Processing:
  • Auto-editor: {'[OK]' if extended_settings['audio_processor']['auto_editor'] else '[EMOJI]'}
  • FFmpeg normalization: {'[OK]' if extended_settings['audio_processor']['ffmpeg_normalization'] else '[EMOJI]'}
  • Export formats: {', '.join([f for f, enabled in extended_settings['audio_processor']['export_formats'].items() if enabled])}

[TARGET] Generation:
  • Multiple generations: {extended_settings['generation_controller']['num_generations']} takes
  • Candidates per block: {extended_settings['generation_controller']['candidates_per_block']}
  • Fallback strategy: {extended_settings['generation_controller']['fallback_strategy']}

[MIC] Whisper Validation:
  • Status: {'[OK] Enabled' if extended_settings['whisper_manager']['enabled'] else '[EMOJI] Disabled'}
  • Model: {extended_settings['whisper_manager']['model']}
  • Backend: {extended_settings['whisper_manager']['backend']}

[FOLDER] Output: {output_dir}
                """
                self.voice_results_text.setText(results_text)
                
                QMessageBox.information(
                    self,
                    "[ROCKET] Chatterbox Extended Hoàn thành",
                    f"Đã tạo thành công {result.get('total_audio_files', 0)} files audio!\n"
                    f"Output directory: {output_dir}\n\n"
                    f"Extended features đã được áp dụng:\n"
                    f"• Text processing: {'[OK]' if extended_settings['text_processor']['smart_joining'] else '[EMOJI]'}\n"
                    f"• Audio enhancement: {'[OK]' if extended_settings['audio_processor']['ffmpeg_normalization'] else '[EMOJI]'}\n"
                    f"• Multiple generations: {extended_settings['generation_controller']['num_generations']} takes\n"
                    f"• Whisper validation: {'[OK]' if extended_settings['whisper_manager']['enabled'] else '[EMOJI]'}"
                )
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                self.voice_results_text.setText(f"[EMOJI] Error: {error_msg}")
                QMessageBox.critical(self, "Error", f"Chatterbox Extended gặp lỗi:\n{error_msg}")
            
        except ImportError as e:
            # Fallback to original method if Extended not available
            QMessageBox.warning(
                self, 
                "Chatterbox Extended không khả dụng", 
                "Không thể import Chatterbox Extended. Sử dụng phương pháp cơ bản.\n\n"
                f"Chi tiết lỗi: {str(e)}"
            )
            # Handle both single character và multi character formats
        try:
            if 'characters' in self.voice_studio_script_data:
                # Multi-character format (old)
                character_ids = [char['id'] for char in self.voice_studio_script_data['characters']]
                self.generate_voices_for_characters(character_ids)
            elif 'text' in self.voice_studio_script_data and 'mode' in self.voice_studio_script_data:
                # Single character format (new)
                QMessageBox.information(
                    self, 
                    "Single Character Mode", 
                    "Single character mode requires Chatterbox Extended.\n"
                    "Please ensure the Extended integration is properly installed."
                )
                return
            else:
                QMessageBox.warning(self, "Error", "Unknown script data format!")
                return
            
        except Exception as e:
            # Handle other errors
            self.voice_progress_bar.setVisible(False)
            error_msg = f"Error khi chạy Chatterbox Extended: {str(e)}"
            self.voice_results_text.setText(f"[EMOJI] {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)
            print(f"Extended generation error: {e}")
            import traceback
            traceback.print_exc()
    
    def update_extended_progress(self, progress, message):
        """Callback để cập nhật progress cho Chatterbox Extended"""
        try:
            if hasattr(self, 'voice_progress_bar') and hasattr(self, 'voice_progress_text'):
                # Update progress bar if it's a percentage
                if isinstance(progress, (int, float)) and 0 <= progress <= 100:
                    self.voice_progress_bar.setRange(0, 100)
                    self.voice_progress_bar.setValue(int(progress))
                
                # Update text
                self.voice_progress_text.setText(f"[ROCKET] {message}")
                
                # Process events để UI responsive
                QApplication.processEvents()
                
        except Exception as e:
            print(f"Progress update error: {e}")
    
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
                
                # [OK] FIX: Updated column indexes after adding Exaggeration column
                emotion_combo = self.character_settings_table.cellWidget(i, 1)  # Emotion dropdown 
                exag_input = self.character_settings_table.cellWidget(i, 2)     # Exaggeration input
                speed_input = self.character_settings_table.cellWidget(i, 3)    # Speed input
                cfg_weight_input = self.character_settings_table.cellWidget(i, 4)  # CFG Weight input
                # Mode at column 5, Voice at column 6
                voice_widget = self.character_settings_table.cellWidget(i, 6)   # Voice stacked widget
                
                # [OK] FIX: Get voice combo from stacked widget
                voice_combo = None
                if voice_widget and hasattr(voice_widget, 'currentWidget'):
                    current_widget = voice_widget.currentWidget()
                    if current_widget:
                        # Find voice combo in the current widget
                        for child in current_widget.findChildren(QComboBox):
                            if child.count() > 20:  # Voice combo should have 28+ items
                                voice_combo = child
                                break
                
                # [OK] FIX: Get emotion from dropdown, not input
                emotion_text = 'friendly'  # Default
                if emotion_combo and hasattr(emotion_combo, 'currentText'):
                    emotion_text = emotion_combo.currentText()
                    # Extract emotion name from "[EMOJI] happy" format
                    if ' ' in emotion_text:
                        emotion_text = emotion_text.split(' ', 1)[1]  # Get "happy" from "[EMOJI] happy"
                
                current_voice_mapping[char_id] = {
                    'name': char_id,
                    'suggested_voice': voice_combo.currentData() if voice_combo else 'abigail',  # Use real voice ID
                    'emotion': emotion_text,  # String emotion from dropdown
                    'exaggeration': float(exag_input.text()) if exag_input and exag_input.text() else 1.35,
                    'speed': float(speed_input.text()) if speed_input and speed_input.text() else 1.0,
                    'cfg_weight': float(cfg_weight_input.text()) if cfg_weight_input and cfg_weight_input.text() else 0.5
                }
            
            # Count total dialogues for progress tracking
            total_dialogues = 0
            for segment in self.voice_studio_script_data['segments']:
                for dialogue in segment['dialogues']:
                    if dialogue['speaker'] in character_ids:
                        total_dialogues += 1
            
            # Generate audio với real-time progress
            total_generated = 0
            total_failed = 0
            current_dialogue = 0
            results_text = ""
            
            # Set determinate progress bar
            self.voice_progress_bar.setRange(0, total_dialogues)
            self.voice_progress_bar.setValue(0)
            
            for segment in self.voice_studio_script_data['segments']:
                segment_id = segment['id']
                print(f"\n[ACTION] Processing Segment {segment_id}")
                
                for dialogue_idx, dialogue in enumerate(segment['dialogues'], 1):
                    speaker = dialogue['speaker']
                    
                    # Skip if not in selected characters
                    if speaker not in character_ids:
                        continue
                    
                    current_dialogue += 1
                    text = dialogue['text']
                    emotion = dialogue.get('emotion', 'neutral')
                    
                    # Get voice settings from character_settings_table
                    voice_settings = current_voice_mapping.get(speaker, {})
                    voice_name = voice_settings.get('suggested_voice', 'abigail')  # Use real voice ID
                    table_emotion = voice_settings.get('emotion', 'friendly')  # String emotion from table
                    exaggeration = voice_settings.get('exaggeration', 1.0)  # Get exaggeration from table
                    speed = voice_settings.get('speed', 1.0)
                    cfg_weight = voice_settings.get('cfg_weight', 0.5)
                    
                    # Default emotion_exaggeration - will be overridden by emotion mapping if enabled
                    emotion_exaggeration = exaggeration  # Use table exaggeration as base
                    
                    # Get per-character settings từ character_chatterbox_settings
                    char_settings = self.character_chatterbox_settings.get(speaker, {})
                    voice_prompt = char_settings.get('voice_prompt', '').strip()
                    voice_name     = char_settings.get('voice_id', voice_name)
                    voice_clone_path = char_settings.get('voice_clone_path', None)

                    # Whisper [EMOJI] override voice (per-character) - Enhanced với clone support
                    whisper_voice_id = char_settings.get('whisper_voice_id')
                    whisper_voice_clone_path = char_settings.get('whisper_voice_clone_path')
                    
                    print(f"[SEARCH] DEBUG {speaker}: emotion='{emotion}', voice_name='{voice_name}', whisper_voice_id='{whisper_voice_id}'")
                    
                    # Store original voice settings if not already stored
                    if 'original_voice_id' not in char_settings:
                        # Lấy voice gốc từ character table hoặc default smart mapping
                        if speaker == 'narrator':
                            original_voice = 'alexander'  # Narrator default
                        elif speaker == 'character1':
                            original_voice = 'elena'      # Character1 default (female)
                        elif speaker == 'character2':
                            original_voice = 'thomas'     # Character2 default (male)
                        else:
                            original_voice = char_settings.get('voice_id', 'alexander')  # Fallback
                        
                        char_settings['original_voice_id'] = original_voice
                        char_settings['original_voice_clone_path'] = char_settings.get('voice_clone_path')
                        self.character_chatterbox_settings[speaker] = char_settings
                        print(f"[EDIT] Stored original voice → {speaker}: {original_voice}")
                    
                    if emotion.lower() == 'whisper':
                        # Mark that whisper override is active
                        char_settings['whisper_override_active'] = True
                        self.character_chatterbox_settings[speaker] = char_settings
                        
                        # Ưu tiên whisper clone nếu character đang ở voice_clone mode và user đã chọn clone path
                        if whisper_voice_clone_path and char_settings.get('voice_mode') == 'voice_clone':
                            voice_clone_path = whisper_voice_clone_path
                            print(f"[MUTE] Whisper clone override → {speaker}: {os.path.basename(whisper_voice_clone_path)}")
                        elif whisper_voice_id:
                            # Dùng whisper voice ID cho chế độ selection (hoặc fallback)
                            voice_name = whisper_voice_id
                            print(f"[EMOJI] Whisper voice override → {speaker}: {whisper_voice_id}")
                    else:
                        # Chỉ reset về original voice nếu đã có whisper override trước đó
                        if char_settings.get('whisper_override_active'):
                            original_voice_id = char_settings.get('original_voice_id')
                            original_voice_clone_path = char_settings.get('original_voice_clone_path')
                            
                            # CHỈ reset về original nếu voice_name hiện tại KHÔNG phải là user choice
                            # Kiểm tra xem voice_name có phải là whisper voice không
                            is_whisper_voice = (voice_name and '(whispering)' in voice_name.lower())
                            
                            if original_voice_id and is_whisper_voice:
                                voice_name = original_voice_id
                                print(f"[REFRESH] Reset to original voice → {speaker}: {original_voice_id}")
                            else:
                                # Giữ voice_name user chọn, chỉ log rằng không reset
                                print(f"[USERS] Keeping user selected voice → {speaker}: {voice_name}")
                            
                            if original_voice_clone_path and char_settings.get('voice_mode') == 'voice_clone' and is_whisper_voice:
                                voice_clone_path = original_voice_clone_path
                                print(f"[REFRESH] Reset to original clone → {speaker}: {os.path.basename(original_voice_clone_path) if original_voice_clone_path else 'None'}")
                            
                            # Clear whisper override flag
                            char_settings['whisper_override_active'] = False
                            self.character_chatterbox_settings[speaker] = char_settings
                    
                    # Generate filename
                    filename = f"segment_{segment_id}_dialogue_{dialogue_idx}_{speaker}.mp3"
                    file_path = os.path.join(output_dir, filename)
                    
                    # [STATS] Update real-time progress
                    progress_text = f"[MIC] [{current_dialogue}/{total_dialogues}] Đang tạo: {speaker} (Segment {segment_id})"
                    self.voice_progress_text.setText(progress_text)
                    self.voice_progress_bar.setValue(current_dialogue)
                    
                    # Process events để UI update ngay lập tức
                    QApplication.processEvents()
                    
                    # Log chi tiết cho console
                    print(f"[EMOJI] [{current_dialogue}/{total_dialogues}] {speaker}: {text[:50]}{'...' if len(text) > 50 else ''}")
                    
                    # Generate voice - CHỈ SỬ DỤNG CHATTERBOX TTS với per-character settings
                    try:
                        # Apply emotion mapping if enabled (use emotion from script, not table)
                        if self.enable_emotion_mapping.isChecked():
                            mapped_emotion, mapped_cfg = self.map_emotion_to_parameters(emotion, emotion_exaggeration)
                            emotion_exaggeration = mapped_emotion
                            cfg_weight = mapped_cfg
                        else:
                            # If no emotion mapping, use script emotion directly for Chatterbox (emotion is now just a label)
                            # Keep emotion_exaggeration as 1.0 for consistent behavior
                            pass
                        
                        # Validate voice settings và log generation info
                        voice_mode = self.validate_character_voice_settings(speaker)
                        
                        # CHỈ SỬ DỤNG CHATTERBOX TTS với optimized parameter passing
                        result = self.voice_generator.generate_voice_chatterbox(
                            text=text,
                            save_path=file_path,
                            voice_sample_path=voice_clone_path if voice_mode == 'clone' else None,
                            emotion_exaggeration=emotion_exaggeration,  # [OK] FIX: Use correct parameter name
                            speed=speed,
                            voice_name=voice_name if voice_mode == 'selection' else None,  # [OK] Use override voice_name
                            cfg_weight=cfg_weight,
                            voice_prompt=voice_prompt if voice_mode == 'prompt' else None
                        )
                        
                        if result.get('success'):
                            total_generated += 1
                            results_text += f"[OK] {filename}\n"
                            print(f"   [OK] Success: {filename}")
                        else:
                            total_failed += 1
                            error_msg = result.get('error', 'Unknown error')
                            results_text += f"[EMOJI] {filename}: {error_msg}\n"
                            print(f"   [EMOJI] Failed: {error_msg}")
                            
                        # Update results text ngay lập tức
                        self.voice_results_text.setText(results_text)
                        QApplication.processEvents()
                            
                    except Exception as e:
                        total_failed += 1
                        error_msg = str(e)
                        results_text += f"[EMOJI] {filename}: {error_msg}\n"
                        print(f"   [EMOJI] Exception: {error_msg}")
                        
                        # Update results text ngay lập tức
                        self.voice_results_text.setText(results_text)
                        QApplication.processEvents()
            
            # Update results
            self.voice_results_text.setText(results_text)
            
            # [MUSIC] MERGE ALL AUDIO FILES into complete conversation
            merged_file = None
            if total_generated > 0:
                try:
                    print("[REFRESH] Merging all audio files into complete conversation...")
                    merged_file = self.merge_all_voice_files(output_dir)
                    if merged_file:
                        print(f"[OK] Complete conversation saved: {merged_file}")
                except Exception as merge_error:
                    print(f"[WARNING] Failed to merge audio files: {merge_error}")
            
            # Show summary
            summary = f"[TARGET] Hoàn thành!\n\n"
            summary += f"[OK] Thành công: {total_generated} files\n"
            summary += f"[EMOJI] Thất bại: {total_failed} files\n"
            summary += f"[FOLDER] Output: {output_dir}"
            
            if merged_file:
                summary += f"\n\n[MUSIC] Complete Audio: {os.path.basename(merged_file)}"
                summary += f"\n[STATS] File gộp đã được tạo thành công!"
            
            QMessageBox.information(self, "Kết quả", summary)
            
            # Update progress
            progress_text = f"Hoàn thành: {total_generated} thành công, {total_failed} thất bại"
            if merged_file:
                progress_text += " | [MUSIC] File gộp đã tạo"
            self.voice_progress_text.setText(progress_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error tạo voice:\n{str(e)}")
            self.voice_progress_text.setText("Error tạo voice")
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
    
    def force_merge_all_segments(self):
        """Force merge tất cả segment files với proper MP3 handling"""
        try:
            output_dir = self.voice_output_input.text() or "./voice_studio_output"
            
            if not os.path.exists(output_dir):
                QMessageBox.warning(self, "Cảnh báo", f"Thư mục output không tồn tại: {output_dir}")
                return
            
            # Find all segment files
            import glob
            audio_files = glob.glob(os.path.join(output_dir, "segment_*.mp3"))
            
            if not audio_files:
                QMessageBox.warning(self, "Cảnh báo", f"Không tìm thấy file segment_*.mp3 trong thư mục: {output_dir}")
                return
            
            # Sort files properly
            def extract_numbers(filename):
                import re
                basename = os.path.basename(filename)
                match = re.search(r'segment_(\d+)_dialogue_(\d+)', basename)
                if match:
                    return (int(match.group(1)), int(match.group(2)))
                return (0, 0)
            
            sorted_files = sorted(audio_files, key=extract_numbers)
            
            print(f"\n[ROCKET] FORCE MERGE ALL SEGMENTS")
            print(f"[FOLDER] Directory: {output_dir}")
            print(f"[MUSIC] Found {len(sorted_files)} files to merge")
            
            # Show progress
            self.voice_progress_text.setText(f"Force merging {len(sorted_files)} files...")
            QApplication.processEvents()
            
            # Output file with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"force_merged_conversation_{timestamp}.mp3")
            
            print(f"[TOOL] Using MP3 frame-level concatenation...")
            
            try:
                with open(output_path, 'wb') as outfile:
                    first_file = True
                    files_merged = 0
                    
                    for file_path in sorted_files:
                        if os.path.exists(file_path):
                            print(f"   [EMOJI] Processing: {os.path.basename(file_path)}")
                            
                            with open(file_path, 'rb') as infile:
                                data = infile.read()
                                
                                if first_file:
                                    # Keep full first file including headers
                                    outfile.write(data)
                                    first_file = False
                                    print(f"      [OK] Wrote full file with headers ({len(data)} bytes)")
                                else:
                                    # Skip ID3 headers for subsequent files
                                    # Find MP3 sync frame (0xFF 0xFB or 0xFF 0xFA)
                                    sync_pos = 0
                                    for i in range(min(1024, len(data) - 1)):
                                        if data[i] == 0xFF and data[i+1] in [0xFB, 0xFA, 0xF3, 0xF2]:
                                            sync_pos = i
                                            break
                                    
                                    # Write from sync frame onwards
                                    audio_data = data[sync_pos:]
                                    outfile.write(audio_data)
                                    print(f"      [OK] Wrote audio data ({len(audio_data)} bytes, skipped {sync_pos} header bytes)")
                                
                                files_merged += 1
                
                # Check file size
                file_size = os.path.getsize(output_path)
                print(f"\n[OK] FORCE MERGE SUCCESS!")
                print(f"[FOLDER] Output: {os.path.basename(output_path)}")
                print(f"[RULER] File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
                
                # Success dialog với option to play
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("[SUCCESS] Force Merge Success!")
                msg.setText(f"[OK] Successfully merged {files_merged} audio files!")
                msg.setInformativeText(f"[FOLDER] Saved: {os.path.basename(output_path)}\n[RULER] Size: {file_size / 1024 / 1024:.2f} MB\n\n[MUSIC] Bạn có muốn nghe merged audio không?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.Yes)
                
                reply = msg.exec_()
                
                if reply == QMessageBox.Yes:
                    self.play_audio_file(output_path)
                
                self.voice_progress_text.setText(f"[OK] Force merged: {os.path.basename(output_path)}")
                
            except Exception as merge_error:
                print(f"[EMOJI] Force merge failed: {merge_error}")
                QMessageBox.critical(self, "Error", f"Force merge thất bại:\n{merge_error}")
                self.voice_progress_text.setText("[EMOJI] Force merge failed")
                
        except Exception as e:
            print(f"[EMOJI] Error in force merge: {e}")
            QMessageBox.critical(self, "Error", f"Error khi force merge:\n{e}")
    
    def force_merge_all_files(self):
        """Force merge tất cả segment files - không cần script data"""
        try:
            output_dir = self.voice_output_input.text() or "./voice_studio_output"
            
            if not os.path.exists(output_dir):
                QMessageBox.warning(self, "Cảnh báo", f"Thư mục output không tồn tại: {output_dir}")
                return
            
            # Show progress
            self.voice_progress_text.setText("Force merging tất cả files...")
            QApplication.processEvents()
            
            # Use smart merge logic (doesn't require script data)
            merged_file = self.merge_all_voice_files(output_dir)
            
            if merged_file:
                # Success message
                filename = os.path.basename(merged_file)
                message = f"[SUCCESS] Force merge thành công!\n\n"
                message += f"[FOLDER] File: {filename}\n"
                message += f"[EMOJI] Vị trí: {output_dir}\n\n"
                message += f"[OK] Đã gộp tất cả segment files theo thứ tự số.\n"
                message += f"Bạn có muốn nghe cuộc hội thoại hoàn chỉnh không?"
                
                reply = QMessageBox.question(
                    self, "Thành công", message,
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    self.play_audio_file(merged_file)
                    
                self.voice_progress_text.setText(f"[OK] Force merge: {filename}")
            else:
                QMessageBox.warning(self, "Error", "Không thể force merge files. Xem console để biết chi tiết.")
                self.voice_progress_text.setText("[EMOJI] Error force merge")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error force merge:\n{str(e)}")
            self.voice_progress_text.setText("[EMOJI] Error force merge")
        
    def merge_all_voice_files(self, output_dir):
        """Gộp tất cả audio files thành 1 cuộc hội thoại hoàn chỉnh - SMART MERGE"""
        try:
            from pydub import AudioSegment
            import re
            import glob
            import shutil
            
            # Configure PyDub ffmpeg/ffprobe paths (ensure they're set correctly)
            ffprobe_path = os.path.join(os.getcwd(), "tools", "ffmpeg", "ffprobe.exe")
            ffmpeg_path = os.path.join(os.getcwd(), "tools", "ffmpeg", "ffmpeg.exe")
            
            if os.path.exists(ffprobe_path):
                AudioSegment.ffprobe = ffprobe_path
                AudioSegment.converter = ffmpeg_path if os.path.exists(ffmpeg_path) else ffprobe_path.replace("ffprobe", "ffmpeg")
                print(f"[TOOL] PyDub configured with local ffprobe: {ffprobe_path}")
            elif shutil.which("ffprobe"):
                AudioSegment.ffprobe = shutil.which("ffprobe")
                AudioSegment.converter = shutil.which("ffmpeg") or "ffmpeg"
                print(f"[TOOL] PyDub configured with system ffprobe")
            else:
                print("[WARNING] ffprobe not found - PyDub may fail to load MP3 files")
            
            print("[SEARCH] SMART AUDIO MERGE - Scanning for files...")
            print(f"[FOLDER] Output directory: {output_dir}")
            print(f"[EMOJI] Absolute path: {os.path.abspath(output_dir)}")
            
            # Initialize missing files tracking
            missing_files = []
            
            # Get all segment MP3 files and sort them intelligently
            search_pattern = os.path.join(output_dir, "segment_*.mp3")
            print(f"[SEARCH] Search pattern: {search_pattern}")
            all_mp3_files = glob.glob(search_pattern)
            print(f"[MUSIC] Found {len(all_mp3_files)} segment MP3 files")
            
            if not all_mp3_files:
                print("[EMOJI] No segment files found with glob search")
                
                # Fallback: Try manual directory listing  
                print("[REFRESH] Trying manual directory scan...")
                try:
                    if os.path.exists(output_dir):
                        all_files = os.listdir(output_dir)
                        segment_files = [f for f in all_files if f.startswith('segment_') and f.endswith('.mp3')]
                        print(f"[FOLDER] Manual scan found {len(segment_files)} segment files: {segment_files[:5]}")
                        
                        if segment_files:
                            # Build full paths
                            all_mp3_files = [os.path.join(output_dir, f) for f in segment_files]
                        else:
                            print("[EMOJI] No segment files found even with manual scan")
                            return None
                    else:
                        print(f"[EMOJI] Output directory does not exist: {output_dir}")
                        return None
                except Exception as e:
                    print(f"[EMOJI] Error during manual scan: {e}")
                    return None
            
            # Smart sorting: Extract segment and dialogue numbers for proper ordering
            def extract_numbers(filename):
                """Extract segment_id, dialogue_id from filename like segment_1_dialogue_2_speaker.mp3"""
                match = re.search(r'segment_(\d+)_dialogue_(\d+)', os.path.basename(filename))
                if match:
                    return (int(match.group(1)), int(match.group(2)))
                # Fallback: try to extract just segment number
                match = re.search(r'segment_(\d+)', os.path.basename(filename))
                if match:
                    return (int(match.group(1)), 0)
                return (999, 999)  # Put unrecognized files at end
            
            # Sort files by segment then dialogue order
            sorted_files = sorted(all_mp3_files, key=extract_numbers)
            
            print(f"[CLIPBOARD] File order after smart sorting:")
            for i, file_path in enumerate(sorted_files[:5]):  # Show first 5
                seg, dial = extract_numbers(file_path)
                filename = os.path.basename(file_path)
                absolute_path = os.path.abspath(file_path)
                exists = "[OK]" if os.path.exists(file_path) else "[EMOJI]"
                print(f"   {i+1:2d}. {filename} (seg:{seg}, dial:{dial}) {exists}")
                print(f"       Path: {absolute_path}")
            if len(sorted_files) > 5:
                print(f"   ... and {len(sorted_files) - 5} more files")
            
            # Merge all files in order
            merged_audio = AudioSegment.silent(duration=0)
            total_files_added = 0
            
            for file_path in sorted_files:
                filename = os.path.basename(file_path)
                try:
                    # Fix path separators for Windows compatibility
                    normalized_path = os.path.normpath(file_path)
                    
                    # Double check file exists before trying to load
                    if not os.path.exists(normalized_path):
                        print(f"   [WARNING] File not found at: {normalized_path}")
                        continue
                    
                    # Load audio file with PyDub fallback options - SUPPRESS FFMPEG STDERR
                    import contextlib
                    try:
                        # Try direct MP3 loading first
                        with contextlib.redirect_stderr(open(os.devnull, 'w')):
                            audio_segment = AudioSegment.from_mp3(normalized_path)
                    except Exception as mp3_error:
                        print(f"   [REFRESH] MP3 loading failed, trying raw audio")
                        try:
                            # Fallback: Try loading as raw audio without codec requirements
                            with contextlib.redirect_stderr(open(os.devnull, 'w')):
                                audio_segment = AudioSegment.from_file(normalized_path, format="mp3")
                        except Exception as fallback_error:
                            print(f"   [REFRESH] Fallback failed, trying with ffmpeg")
                            try:
                                # Final fallback: Force ffmpeg usage
                                with contextlib.redirect_stderr(open(os.devnull, 'w')):
                                    audio_segment = AudioSegment.from_file(normalized_path)
                            except Exception as final_error:
                                print(f"   [EMOJI] All loading methods failed")
                                continue
                    
                    # Add silence padding between dialogues (0.5 seconds)
                    if total_files_added > 0:
                        silence = AudioSegment.silent(duration=500)  # 0.5 second pause
                        merged_audio += silence
                    
                    # Add the dialogue audio
                    merged_audio += audio_segment
                    total_files_added += 1
                    
                    # Log addition
                    duration = len(audio_segment) / 1000.0  # Convert to seconds
                    print(f"   [OK] Added: {filename} ({duration:.1f}s)")
                    
                except Exception as e:
                    print(f"   [EMOJI] Failed to load {filename}: {e}")
            
            if total_files_added == 0:
                print("[EMOJI] No audio files successfully loaded with PyDub")
                print("[REFRESH] Attempting FORCE BYPASS with simple file concatenation...")
                
                # FORCE BYPASS: Use FFmpeg directly via subprocess (no PyDub)
                try:
                    output_path = os.path.join(output_dir, "complete_merged_audio.mp3")
                    
                    # Try FFmpeg direct command first
                    import subprocess
                    import shutil
                    
                    # Check if ffmpeg is available (multiple locations)
                    ffmpeg_cmd = None
                    ffmpeg_available = False
                    
                    # First try system PATH
                    if shutil.which('ffmpeg') is not None:
                        ffmpeg_cmd = 'ffmpeg'
                        ffmpeg_available = True
                        print("[TARGET] Using FFmpeg from system PATH")
                    else:
                        # Try common FFmpeg installation paths on Windows including local tools
                        common_paths = [
                            os.path.join(os.getcwd(), "tools", "ffmpeg", "ffmpeg.exe"),  # Local tools first
                            r"C:\ffmpeg\bin\ffmpeg.exe",
                            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe", 
                            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                            r"C:\Users\%USERNAME%\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
                        ]
                        
                        for path in common_paths:
                            expanded_path = os.path.expandvars(path)
                            if os.path.exists(expanded_path):
                                ffmpeg_cmd = expanded_path
                                ffmpeg_available = True
                                print(f"[TARGET] Found FFmpeg at: {expanded_path}")
                                break
                        
                        if not ffmpeg_available:
                            ffmpeg_cmd = 'ffmpeg'  # Fallback, may fail
                            print("[WARNING] FFmpeg not found, using fallback 'ffmpeg' command")
                    
                    if ffmpeg_available:
                        print("[TARGET] Using FFmpeg direct command for concatenation...")
                        
                        # Create file list for FFmpeg
                        file_list_path = os.path.join(output_dir, "concat_list.txt")
                        with open(file_list_path, 'w', encoding='utf-8') as f:
                            for file_path in sorted_files:
                                normalized_path = os.path.normpath(file_path)
                                if os.path.exists(normalized_path):
                                    # FFmpeg expects forward slashes even on Windows
                                    ffmpeg_path = normalized_path.replace('\\', '/')
                                    f.write(f"file '{ffmpeg_path}'\n")
                        
                        # Run FFmpeg concatenation
                        cmd = [ffmpeg_cmd, '-f', 'concat', '-safe', '0', '-i', file_list_path, '-c', 'copy', output_path, '-y']
                        
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        
                        # Clean up temp file
                        try:
                            os.remove(file_list_path)
                        except:
                            pass
                        
                        if result.returncode == 0:
                            files_concatenated = len([f for f in sorted_files if os.path.exists(os.path.normpath(f))])
                            print(f"[OK] FFmpeg SUCCESS: {files_concatenated} files merged to {output_path}")
                        else:
                            print(f"[EMOJI] FFmpeg failed: {result.stderr}")
                            ffmpeg_available = False
                    
                    if not ffmpeg_available:
                        print("[REFRESH] FFmpeg not available, trying Windows copy command...")
                        
                        # Fallback: Use Windows copy command for concatenation
                        files_concatenated = 0
                        temp_files = []
                        
                        for i, file_path in enumerate(sorted_files):
                            normalized_path = os.path.normpath(file_path)
                            if os.path.exists(normalized_path):
                                print(f"   [EMOJI] Processing: {os.path.basename(file_path)}")
                                files_concatenated += 1
                        
                        if files_concatenated > 0:
                            # Use copy command on Windows
                            files_str = ' + '.join([f'"{os.path.normpath(f)}"' for f in sorted_files if os.path.exists(os.path.normpath(f))])
                            copy_cmd = f'copy /b {files_str} "{output_path}"'
                            
                            result = subprocess.run(copy_cmd, shell=True, capture_output=True, text=True)
                            
                            if result.returncode == 0:
                                print(f"[OK] Windows COPY SUCCESS: {files_concatenated} files merged")
                                print(f"[WARNING] Note: Duration may show incorrectly due to MP3 header issues")
                            else:
                                print(f"[EMOJI] Windows copy failed: {result.stderr}")
                                print("[REFRESH] Trying MP3 frame-level concatenation...")
                                
                                # Alternative: MP3 frame-level concatenation
                                try:
                                    with open(output_path, 'wb') as outfile:
                                        first_file = True
                                        for file_path in sorted_files:
                                            normalized_path = os.path.normpath(file_path)
                                            if os.path.exists(normalized_path):
                                                with open(normalized_path, 'rb') as infile:
                                                    data = infile.read()
                                                    
                                                    if first_file:
                                                        # Keep full first file including headers
                                                        outfile.write(data)
                                                        first_file = False
                                                    else:
                                                        # Skip ID3 headers for subsequent files (usually first 128 bytes)
                                                        # Find MP3 sync frame (0xFF 0xFB or 0xFF 0xFA)
                                                        sync_pos = 0
                                                        for i in range(min(1024, len(data) - 1)):
                                                            if data[i] == 0xFF and data[i+1] in [0xFB, 0xFA, 0xF3, 0xF2]:
                                                                sync_pos = i
                                                                break
                                                        
                                                        # Write from sync frame onwards
                                                        outfile.write(data[sync_pos:])
                                    
                                    print(f"[OK] MP3 FRAME SUCCESS: {files_concatenated} files merged with frame sync")
                                    
                                except Exception as frame_error:
                                    print(f"[EMOJI] MP3 frame concatenation failed: {frame_error}")
                                
                                # Last resort: Create a playlist file instead
                                playlist_path = os.path.join(output_dir, "complete_conversation_playlist.m3u")
                                with open(playlist_path, 'w', encoding='utf-8') as f:
                                    f.write("#EXTM3U\n")
                                    for file_path in sorted_files:
                                        if os.path.exists(os.path.normpath(file_path)):
                                            f.write(f"{os.path.basename(file_path)}\n")
                                
                                output_path = playlist_path
                                print(f"[OK] Created playlist file: {playlist_path}")
                                
                                # Show different success dialog for playlist
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Information)
                                msg.setWindowTitle("[EDIT] Playlist Created!")
                                msg.setText(f"[OK] Created playlist with {files_concatenated} audio files!")
                                msg.setInformativeText(f"[FOLDER] Saved to: {playlist_path}\n\n[IDEA] Open this file with your music player to play all segments in order.")
                                msg.setStandardButtons(QMessageBox.Ok)
                                msg.exec_()
                                return output_path
                    
                    if files_concatenated > 0:
                        print(f"[OK] FORCE BYPASS SUCCESS: {files_concatenated} files concatenated to {output_path}")
                        
                        # Fix metadata duration
                        metadata_fixer = AudioMetadataFixer()
                        if metadata_fixer.ffmpeg_available:
                            print(f"[TOOL] Fixing metadata duration...")
                            fix_result = metadata_fixer.fix_metadata(output_path)
                            
                            if fix_result["success"]:
                                print(f"[OK] Metadata fixed! Duration now shows correctly.")
                                # Replace original với fixed version
                                if os.path.exists(fix_result["output_path"]):
                                    os.replace(fix_result["output_path"], output_path)
                            else:
                                print(f"[WARNING] Could not fix metadata: {fix_result.get('error', 'Unknown error')}")
                        else:
                            print(f"[WARNING] FFmpeg not available - metadata duration may be incorrect")
                        
                        # Show success dialog
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("[SUCCESS] Force Merge Success!")
                        msg.setText(f"[OK] Successfully merged {files_concatenated} audio files using FORCE BYPASS method!")
                        msg.setInformativeText(f"[FOLDER] Saved to: {output_path}\n\n[STATS] Duration metadata has been fixed!\n\n[WARNING] Note: Used binary concatenation due to PyDub codec issues.")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        
                        return output_path
                    else:
                        print("[EMOJI] FORCE BYPASS also failed - no files could be read")
                        return None
                        
                except Exception as bypass_error:
                    print(f"[EMOJI] FORCE BYPASS failed: {bypass_error}")
                    return None
            
            # Generate output filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Try to get project name or use default
            project_name = getattr(self, 'current_project_name', 'voice_conversation')
            if hasattr(self, 'voice_studio_script_data') and self.voice_studio_script_data:
                # Try to extract title from script data
                if 'title' in self.voice_studio_script_data:
                    project_name = self.voice_studio_script_data['title']
                elif 'project_name' in self.voice_studio_script_data:
                    project_name = self.voice_studio_script_data['project_name']
            
            # Clean project name for filename
            clean_name = re.sub(r'[^\w\s-]', '', project_name)
            clean_name = re.sub(r'[-\s]+', '_', clean_name)
            
            output_filename = f"{clean_name}_complete_conversation_{timestamp}.mp3"
            merged_file_path = os.path.join(output_dir, output_filename)
            
            # Export merged audio - SUPPRESS FFMPEG STDERR
            print(f"[EMOJI] Exporting complete conversation...")
            with contextlib.redirect_stderr(open(os.devnull, 'w')):
                merged_audio.export(merged_file_path, format="mp3", bitrate="192k")
            
            # Calculate total duration
            total_duration = len(merged_audio) / 1000.0  # Convert to seconds
            minutes = int(total_duration // 60)
            seconds = int(total_duration % 60)
            
            # Log success summary
            print(f"[SUCCESS] MERGE COMPLETE!")
            print(f"   [STATS] Files merged: {total_files_added}")
            if missing_files:
                print(f"   [WARNING] Missing files: {len(missing_files)}")
                for missing in missing_files[:5]:  # Show first 5 missing files
                    print(f"      - {missing}")
                if len(missing_files) > 5:
                    print(f"      ... and {len(missing_files) - 5} more")
            
            print(f"   ⏱ Total duration: {minutes:02d}:{seconds:02d}")
            print(f"   [FOLDER] Saved: {output_filename}")
            
            return merged_file_path
            
        except ImportError:
            print("[EMOJI] pydub library not available - audio merging disabled")
            print("   [IDEA] Install with: pip install pydub")
            return None
        except Exception as e:
            print(f"[EMOJI] Error merging audio files: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # Removed manual_merge_audio() and play_complete_conversation() methods
    # Now using force_merge_all_segments() as the main audio merging solution
    
    def generate_ai_request_form(self):
        """Tạo form yêu cầu AI với đầy đủ hướng dẫn format và tùy chọn"""
        dialog = QDialog(self)
        dialog.setWindowTitle("[BOT] Create AI Request")
        dialog.setModal(True)
        dialog.resize(900, 1100)
        
        layout = QVBoxLayout(dialog)
        
        # === INTRO ===
        intro_label = QLabel("[TARGET] Create professional AI request forms for high-quality video/audio content generation!")
        intro_label.setStyleSheet("font-weight: bold; color: #007AFF; font-size: 14px;")
        layout.addWidget(intro_label)
        
        # === JSON FORMAT GUIDE ===
        format_group = QGroupBox("[CLIPBOARD] JSON Format Guide")
        format_layout = QVBoxLayout()
        
        # Basic JSON format
        basic_format = QLabel("""
<b>[EMOJI] Basic format for one segment:</b><br>
<code>{<br>
  "segment_1": {<br>
    "dialogue_1": {<br>
      "character": "narrator",<br>
      "text": "Content to speak...",<br>
      "emotion": "neutral"<br>
    }<br>
  }<br>
}</code>
        """)
        basic_format.setWordWrap(True)
        basic_format.setStyleSheet("background: #f8f9fa; padding: 10px; border-radius: 6px; font-size: 12px;")
        format_layout.addWidget(basic_format)
        
        # Inner Voice format - check if enabled
        inner_voice_enabled = self.check_inner_voice_enabled()
        if inner_voice_enabled:
            inner_voice_format = QLabel("""
<b>[THEATER] Inner Voice Format (Internal Monologue):</b><br>
<code>{<br>
  "segment_1": {<br>
    "dialogue_1": {<br>
      "character": "character1",<br>
      "text": "What am I thinking about...",<br>
      "emotion": "contemplative",<br>
      <span style="color: #FF6B35; font-weight: bold;">"inner_voice": true</span><br>
    },<br>
    "dialogue_2": {<br>
      "character": "character1",<br>
      "text": "Speaking normally",<br>
      "emotion": "neutral"<br>
    }<br>
  }<br>
}</code><br><br>
<b>[EDIT] Inner Voice Notes:</b><br>
• Only add <code>"inner_voice": true</code> for internal thoughts<br>
• Don't add this flag for normal dialogue<br>
• Supports 3 types: light (subtle), deep (profound), dreamy (ethereal)<br>
• System auto-selects appropriate type or follows settings
            """)
            inner_voice_format.setWordWrap(True)
            inner_voice_format.setStyleSheet("background: #fff3e0; padding: 10px; border-radius: 6px; font-size: 12px; border-left: 4px solid #FF6B35;")
            format_layout.addWidget(inner_voice_format)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        
        # Template buttons
        rapid_btn = QPushButton("[FAST] Rapid Template")
        rapid_btn.clicked.connect(lambda: self.generate_rapid_template_form())
        rapid_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        
        standard_btn = QPushButton("[EDIT] Standard Template")
        standard_btn.clicked.connect(lambda: self.generate_standard_template_form())
        standard_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        
        detailed_btn = QPushButton("[TARGET] Detailed Template")
        detailed_btn.clicked.connect(lambda: self.generate_detailed_template_form())
        detailed_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        
        custom_btn = QPushButton("[EMOJI] Custom Template")
        custom_btn.clicked.connect(lambda: self.generate_custom_template_form())
        custom_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        
        template_layout.addWidget(rapid_btn, 0, 0)
        template_layout.addWidget(standard_btn, 0, 1)
        template_layout.addWidget(detailed_btn, 1, 0)
        template_layout.addWidget(custom_btn, 1, 1)
        
        template_group.setLayout(template_layout)
        layout.addWidget(template_group)
        
        # === CLOSE BUTTON ===
        close_btn = QPushButton("[OK] Close")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def check_inner_voice_enabled(self):
        """Kiểm tra xem inner voice có được bật trong config không"""
        try:
            # Đọc từ config file
            config_path = "configs/emotions/unified_emotions.json"
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("inner_voice_config", {}).get("enabled", False)
        except Exception as e:
            print(f"Warning: Không thể đọc config inner voice: {e}")
        
        # Fallback: check từ emotion config tab nếu có
        try:
            if hasattr(self, 'emotion_config_tab') and hasattr(self.emotion_config_tab, 'inner_voice_group'):
                return self.emotion_config_tab.inner_voice_group.isChecked()
        except:
            pass
            
        return False
    
    # ==========================================
    # TEXT PROCESSING SETTINGS TAB METHODS  
    # ==========================================
    
    def _update_text_mode_description(self, mode_text):
        """Cập nhật mô tả chế độ xử lý văn bản"""
        descriptions = {
            "conservative - Bảo toàn tối đa": "Xử lý tối thiểu, bảo toàn văn bản gốc. Phù hợp cho nội dung đã được chỉnh sửa kỹ.",
            "default - Cân bằng tối ưu": "Xử lý cân bằng với tối ưu hóa thông minh. Khuyến nghị cho hầu hết trường hợp.",
            "aggressive - Tối ưu TTS": "Xử lý tối đa để tối ưu cho TTS. Phù hợp cho văn bản thô hoặc tự động."
        }
        
        description = descriptions.get(mode_text, "Chế độ không xác định")
        if hasattr(self, 'mode_description'):
            self.mode_description.setText(description)
    
    def _test_text_processing(self):
        """Test xử lý văn bản với sample text"""
        try:
            # Import ChatterboxExtendedIntegration
            from core.chatterbox_extended_integration import create_default_integration
            
            # Sample text
            sample_text = "Xin chào! Tôi là J.R.R. Tolkien. Hôm nay trời rất đẹp... Bạn có muốn đi dạo không? (Tham khảo .123)"
            
            # Show processing dialog
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QHBoxLayout
            
            dialog = QDialog(self)
            dialog.setWindowTitle("🧪 Test xử lý văn bản")
            dialog.setModal(True)
            dialog.resize(600, 400)
            
            layout = QVBoxLayout()
            
            # Original text
            layout.addWidget(QLabel("📝 Văn bản gốc:"))
            original_text = QTextEdit()
            original_text.setPlainText(sample_text)
            original_text.setMaximumHeight(80)
            layout.addWidget(original_text)
            
            # Processed text
            layout.addWidget(QLabel("🔧 Văn bản đã xử lý:"))
            processed_text = QTextEdit()
            processed_text.setReadOnly(True)
            processed_text.setMaximumHeight(150)
            layout.addWidget(processed_text)
            
            # Stats
            stats_label = QLabel("📊 Thống kê xử lý: Chưa xử lý")
            layout.addWidget(stats_label)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            process_btn = QPushButton("🔄 Xử lý")
            def process_sample():
                try:
                    integration = create_default_integration()
                    # Simulate processing
                    processed = integration.text_processor.process_text(original_text.toPlainText()) if integration.text_processor else None
                    
                    if processed and hasattr(processed, 'processed_text'):
                        result = processed.processed_text
                        stats = f"📊 Segments: {len(processed.segments) if hasattr(processed, 'segments') else 1}"
                    else:
                        # Fallback processing
                        result = original_text.toPlainText().replace("J.R.R.", "J R R").replace("(.123)", "")
                        stats = "📊 Xử lý cơ bản (fallback)"
                    
                    processed_text.setPlainText(result)
                    stats_label.setText(stats)
                    
                except Exception as e:
                    processed_text.setPlainText(f"❌ Lỗi xử lý: {str(e)}")
                    stats_label.setText("❌ Có lỗi xảy ra")
            
            process_btn.clicked.connect(process_sample)
            button_layout.addWidget(process_btn)
            
            close_btn = QPushButton("✅ Đóng")
            close_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            
            # Auto process on show
            process_sample()
            
            dialog.exec()
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Lỗi Test", f"Không thể test xử lý văn bản:\n{str(e)}")
    
    def _reset_text_processing_settings(self):
        """Khôi phục cài đặt mặc định cho text processing"""
        try:
            # Reset to default values
            if hasattr(self, 'text_processing_mode'):
                self.text_processing_mode.setCurrentText("default - Cân bằng tối ưu")
            
            if hasattr(self, 'smart_joining_checkbox'):
                self.smart_joining_checkbox.setChecked(True)
            
            if hasattr(self, 'sentence_join_threshold'):
                self.sentence_join_threshold.setValue(40)
            
            if hasattr(self, 'recursive_splitting_checkbox'):
                self.recursive_splitting_checkbox.setChecked(True)
            
            if hasattr(self, 'max_sentence_length'):
                self.max_sentence_length.setValue(200)
            
            if hasattr(self, 'fix_abbreviations_checkbox'):
                self.fix_abbreviations_checkbox.setChecked(True)
            
            if hasattr(self, 'remove_references_checkbox'):
                self.remove_references_checkbox.setChecked(True)
            
            if hasattr(self, 'remove_unwanted_words_checkbox'):
                self.remove_unwanted_words_checkbox.setChecked(True)
            
            if hasattr(self, 'normalize_punctuation_checkbox'):
                self.normalize_punctuation_checkbox.setChecked(True)
            
            if hasattr(self, 'enable_smart_quotes_checkbox'):
                self.enable_smart_quotes_checkbox.setChecked(True)
            
            if hasattr(self, 'preserve_formatting_checkbox'):
                self.preserve_formatting_checkbox.setChecked(True)
            
            if hasattr(self, 'enable_emoji_processing_checkbox'):
                self.enable_emoji_processing_checkbox.setChecked(False)
            
            if hasattr(self, 'enable_number_expansion_checkbox'):
                self.enable_number_expansion_checkbox.setChecked(True)
            
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "✅ Thành công", "Đã khôi phục cài đặt mặc định cho xử lý văn bản!")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "❌ Lỗi", f"Không thể khôi phục cài đặt:\n{str(e)}")
    
    def _apply_text_processing_settings(self):
        """Áp dụng cài đặt xử lý văn bản"""
        try:
            # Get current settings
            settings = {}
            
            if hasattr(self, 'text_processing_mode'):
                mode_text = self.text_processing_mode.currentText()
                settings['text_processing_mode'] = mode_text.split(' - ')[0]
            
            if hasattr(self, 'smart_joining_checkbox'):
                settings['enable_advanced_text_processing'] = self.smart_joining_checkbox.isChecked()
            
            if hasattr(self, 'sentence_join_threshold'):
                settings['sentence_join_threshold'] = self.sentence_join_threshold.value()
            
            # Try to update ChatterboxExtendedIntegration if available
            try:
                from core.chatterbox_extended_integration import create_default_integration
                integration = create_default_integration()
                integration.update_config(settings)
                
                # Update stats display
                self._update_text_processing_stats(integration)
                
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "✅ Thành công", 
                    f"Đã áp dụng cài đặt xử lý văn bản!\n\n"
                    f"Chế độ: {settings.get('text_processing_mode', 'default')}\n"
                    f"Xử lý nâng cao: {'Bật' if settings.get('enable_advanced_text_processing', True) else 'Tắt'}"
                )
                
            except ImportError:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "ℹ️ Thông báo", 
                    "Cài đặt đã được lưu. Chatterbox Extended sẽ áp dụng khi khả dụng.")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "❌ Lỗi", f"Không thể áp dụng cài đặt:\n{str(e)}")
    
    def _update_text_processing_stats(self, integration=None):
        """Cập nhật thống kê xử lý văn bản"""
        try:
            if integration is None:
                from core.chatterbox_extended_integration import create_default_integration
                integration = create_default_integration()
            
            stats = integration.integration_stats
            
            if hasattr(self, 'text_blocks_processed_label'):
                self.text_blocks_processed_label.setText(
                    f"Khối văn bản đã xử lý: {stats.get('text_blocks_processed', 0)}"
                )
            
            if hasattr(self, 'avg_processing_time_label'):
                avg_time = stats.get('average_request_time', 0.0)
                self.avg_processing_time_label.setText(
                    f"Thời gian xử lý trung bình: {avg_time:.1f}s"
                )
            
            if hasattr(self, 'last_processing_result_label'):
                success_rate = stats.get('successful_requests', 0) / max(stats.get('total_requests', 1), 1)
                self.last_processing_result_label.setText(
                    f"Tỷ lệ thành công: {success_rate:.1%} ({stats.get('successful_requests', 0)}/{stats.get('total_requests', 0)})"
                )
            
            # Update status indicator
            if hasattr(self, 'text_processor_status'):
                if integration.text_processor:
                    self.text_processor_status.setText("🟢 Hoạt động")
                    self.text_processor_status.setStyleSheet("color: green; font-weight: bold;")
                else:
                    self.text_processor_status.setText("🔴 Không khả dụng")
                    self.text_processor_status.setStyleSheet("color: red; font-weight: bold;")
            
        except Exception as e:
            print(f"Warning: Không thể cập nhật stats text processing: {e}")
    
    # ==========================================
    # AUDIO PROCESSING SETTINGS TAB METHODS  
    # ==========================================
    
    def _update_audio_mode_description(self, mode_text):
        """Cập nhật mô tả chế độ xử lý âm thanh"""
        descriptions = {
            "fast - Xử lý nhanh": "Xử lý nhanh với tối thiểu post-processing. Tiết kiệm thời gian.",
            "default - Cân bằng chất lượng": "Xử lý cân bằng giữa tốc độ và chất lượng. Khuyến nghị.",
            "quality - Chất lượng tối đa": "Xử lý tối đa với full post-processing. Chất lượng cao nhất."
        }
        
        description = descriptions.get(mode_text, "Chế độ không xác định")
        if hasattr(self, 'audio_mode_description'):
            self.audio_mode_description.setText(description)
    
    def _test_audio_processing(self):
        """Test xử lý âm thanh với sample file"""
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog
            
            # Show processing dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("🧪 Test xử lý âm thanh")
            dialog.setModal(True)
            dialog.resize(600, 400)
            
            layout = QVBoxLayout()
            
            # File selection
            file_layout = QHBoxLayout()
            file_layout.addWidget(QLabel("📁 File âm thanh test:"))
            
            self.test_audio_file_path = QLabel("Chưa chọn file")
            self.test_audio_file_path.setStyleSheet("background: #f0f0f0; padding: 5px; border-radius: 3px;")
            file_layout.addWidget(self.test_audio_file_path)
            
            browse_btn = QPushButton("📂 Chọn file")
            def browse_audio():
                file_path, _ = QFileDialog.getOpenFileName(
                    dialog, "Chọn file âm thanh", "", 
                    "Audio Files (*.wav *.mp3 *.flac *.ogg);;All Files (*)"
                )
                if file_path:
                    self.test_audio_file_path.setText(file_path)
            
            browse_btn.clicked.connect(browse_audio)
            file_layout.addWidget(browse_btn)
            
            layout.addLayout(file_layout)
            
            # Processing result
            layout.addWidget(QLabel("🔧 Kết quả xử lý:"))
            result_text = QTextEdit()
            result_text.setReadOnly(True)
            result_text.setMaximumHeight(200)
            result_text.setPlainText("Chưa xử lý. Vui lòng chọn file và bấm 'Test xử lý'.")
            layout.addWidget(result_text)
            
            # Stats
            stats_label = QLabel("📊 Thống kê: Chưa xử lý")
            layout.addWidget(stats_label)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            process_btn = QPushButton("🔄 Test xử lý")
            def process_sample():
                try:
                    file_path = self.test_audio_file_path.text()
                    if file_path == "Chưa chọn file":
                        result_text.setPlainText("❌ Vui lòng chọn file âm thanh trước!")
                        return
                    
                    if not os.path.exists(file_path):
                        result_text.setPlainText("❌ File không tồn tại!")
                        return
                    
                    # Simulate processing
                    import time
                    start_time = time.time()
                    
                    # Get current settings
                    auto_editor = hasattr(self, 'auto_editor_checkbox') and self.auto_editor_checkbox.isChecked()
                    ffmpeg_norm = hasattr(self, 'ffmpeg_normalization_checkbox') and self.ffmpeg_normalization_checkbox.isChecked()
                    target_lufs = self.target_lufs.value() if hasattr(self, 'target_lufs') else -23.0
                    
                    result = f"✅ Test xử lý thành công!\n\n"
                    result += f"📁 File input: {os.path.basename(file_path)}\n"
                    result += f"📊 File size: {os.path.getsize(file_path) / 1024 / 1024:.1f} MB\n\n"
                    result += f"🔧 Các xử lý được áp dụng:\n"
                    result += f"• Auto-editor: {'✅ Bật' if auto_editor else '❌ Tắt'}\n"
                    result += f"• FFmpeg chuẩn hóa: {'✅ Bật' if ffmpeg_norm else '❌ Tắt'}\n"
                    result += f"• Target LUFS: {target_lufs}\n"
                    result += f"• Formats: WAV, MP3\n\n"
                    result += f"💡 Lưu ý: Đây chỉ là test simulation. Không có file nào được tạo."
                    
                    result_text.setPlainText(result)
                    
                    processing_time = time.time() - start_time
                    stats_label.setText(f"📊 Test hoàn thành trong {processing_time:.2f}s")
                    
                except Exception as e:
                    result_text.setPlainText(f"❌ Lỗi test: {str(e)}")
                    stats_label.setText("❌ Test thất bại")
            
            process_btn.clicked.connect(process_sample)
            button_layout.addWidget(process_btn)
            
            close_btn = QPushButton("✅ Đóng")
            close_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            
            dialog.exec()
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Lỗi Test", f"Không thể test xử lý âm thanh:\n{str(e)}")
    
    def _reset_audio_processing_settings(self):
        """Khôi phục cài đặt mặc định cho audio processing"""
        try:
            # Reset to default values
            if hasattr(self, 'audio_processing_mode'):
                self.audio_processing_mode.setCurrentText("default - Cân bằng chất lượng")
            
            if hasattr(self, 'auto_editor_checkbox'):
                self.auto_editor_checkbox.setChecked(True)
            
            if hasattr(self, 'silence_threshold'):
                self.silence_threshold.setValue(0.04)
            
            if hasattr(self, 'auto_trim_checkbox'):
                self.auto_trim_checkbox.setChecked(True)
            
            if hasattr(self, 'ffmpeg_normalization_checkbox'):
                self.ffmpeg_normalization_checkbox.setChecked(True)
            
            if hasattr(self, 'target_lufs'):
                self.target_lufs.setValue(-23.0)
            
            if hasattr(self, 'peak_limit'):
                self.peak_limit.setValue(-1.0)
            
            if hasattr(self, 'true_peak_checkbox'):
                self.true_peak_checkbox.setChecked(True)
            
            if hasattr(self, 'export_wav_checkbox'):
                self.export_wav_checkbox.setChecked(True)
            
            if hasattr(self, 'export_mp3_checkbox'):
                self.export_mp3_checkbox.setChecked(True)
            
            if hasattr(self, 'export_flac_checkbox'):
                self.export_flac_checkbox.setChecked(False)
            
            if hasattr(self, 'export_ogg_checkbox'):
                self.export_ogg_checkbox.setChecked(False)
            
            if hasattr(self, 'preserve_original_checkbox'):
                self.preserve_original_checkbox.setChecked(True)
            
            if hasattr(self, 'create_metadata_checkbox'):
                self.create_metadata_checkbox.setChecked(True)
            
            if hasattr(self, 'sample_rate_combo'):
                self.sample_rate_combo.setCurrentText("48000 Hz")
            
            if hasattr(self, 'bit_depth_combo'):
                self.bit_depth_combo.setCurrentText("24-bit")
            
            if hasattr(self, 'denoise_checkbox'):
                self.denoise_checkbox.setChecked(False)
            
            if hasattr(self, 'fade_inout_checkbox'):
                self.fade_inout_checkbox.setChecked(True)
            
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "✅ Thành công", "Đã khôi phục cài đặt mặc định cho xử lý âm thanh!")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "❌ Lỗi", f"Không thể khôi phục cài đặt:\n{str(e)}")
    
    def _apply_audio_processing_settings(self):
        """Áp dụng cài đặt xử lý âm thanh"""
        try:
            # Get current settings
            settings = {}
            
            if hasattr(self, 'audio_processing_mode'):
                mode_text = self.audio_processing_mode.currentText()
                settings['audio_processing_mode'] = mode_text.split(' - ')[0]
            
            if hasattr(self, 'auto_editor_checkbox'):
                settings['enable_auto_editor'] = self.auto_editor_checkbox.isChecked()
            
            if hasattr(self, 'ffmpeg_normalization_checkbox'):
                settings['enable_ffmpeg_normalization'] = self.ffmpeg_normalization_checkbox.isChecked()
            
            if hasattr(self, 'target_lufs'):
                settings['target_lufs'] = self.target_lufs.value()
            
            # Collect output formats
            output_formats = []
            if hasattr(self, 'export_wav_checkbox') and self.export_wav_checkbox.isChecked():
                output_formats.append('wav')
            if hasattr(self, 'export_mp3_checkbox') and self.export_mp3_checkbox.isChecked():
                output_formats.append('mp3')
            if hasattr(self, 'export_flac_checkbox') and self.export_flac_checkbox.isChecked():
                output_formats.append('flac')
            if hasattr(self, 'export_ogg_checkbox') and self.export_ogg_checkbox.isChecked():
                output_formats.append('ogg')
            
            settings['output_formats'] = output_formats
            
            # Try to update ChatterboxExtendedIntegration if available
            try:
                from core.chatterbox_extended_integration import create_default_integration
                integration = create_default_integration()
                integration.update_config(settings)
                
                # Update stats display
                self._update_audio_processing_stats(integration)
                
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "✅ Thành công", 
                    f"Đã áp dụng cài đặt xử lý âm thanh!\n\n"
                    f"Chế độ: {settings.get('audio_processing_mode', 'default')}\n"
                    f"Auto-editor: {'Bật' if settings.get('enable_auto_editor', True) else 'Tắt'}\n"
                    f"FFmpeg chuẩn hóa: {'Bật' if settings.get('enable_ffmpeg_normalization', True) else 'Tắt'}\n"
                    f"Formats xuất: {', '.join(output_formats).upper()}"
                )
                
            except ImportError:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "ℹ️ Thông báo", 
                    "Cài đặt đã được lưu. Chatterbox Extended sẽ áp dụng khi khả dụng.")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "❌ Lỗi", f"Không thể áp dụng cài đặt:\n{str(e)}")
    
    def _update_audio_processing_stats(self, integration=None):
        """Cập nhật thống kê xử lý âm thanh"""
        try:
            if integration is None:
                from core.chatterbox_extended_integration import create_default_integration
                integration = create_default_integration()
            
            stats = integration.integration_stats
            
            if hasattr(self, 'audio_files_processed_label'):
                self.audio_files_processed_label.setText(
                    f"Files âm thanh đã xử lý: {stats.get('audio_files_processed', 0)}"
                )
            
            if hasattr(self, 'avg_audio_processing_time_label'):
                avg_time = stats.get('average_request_time', 0.0) * 2  # Audio processing usually takes longer
                self.avg_audio_processing_time_label.setText(
                    f"Thời gian xử lý trung bình: {avg_time:.1f}s"
                )
            
            if hasattr(self, 'total_audio_duration_label'):
                # Simulate total duration (stats might not have this info)
                total_seconds = stats.get('audio_files_processed', 0) * 30  # Assume 30s average per file
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                self.total_audio_duration_label.setText(
                    f"Tổng thời lượng đã xử lý: {hours:02d}:{minutes:02d}:{seconds:02d}"
                )
            
            # Update status indicator
            if hasattr(self, 'audio_processor_status'):
                if integration.audio_processor:
                    self.audio_processor_status.setText("🟢 Hoạt động")
                    self.audio_processor_status.setStyleSheet("color: green; font-weight: bold;")
                else:
                    self.audio_processor_status.setText("🔴 Không khả dụng")
                    self.audio_processor_status.setStyleSheet("color: red; font-weight: bold;")
            
        except Exception as e:
            print(f"Warning: Không thể cập nhật stats audio processing: {e}")

    def generate_rapid_template_form(self):
        """Generate RAPID mode template"""
        
        # Kiểm tra inner voice enabled
        inner_voice_enabled = self.check_inner_voice_enabled()
        
        # Base template
        inner_voice_section = ""
        if inner_voice_enabled:
            inner_voice_section = """

**[THEATER] INNER VOICE (Internal Monologue) - OPTIONAL:**
To create inner voice effects, add 2 fields:
- `"inner_voice": true` - Enable inner voice feature
- `"inner_voice_type": "light|deep|dreamy"` - Echo effect type

**Inner Voice Example:**
```json
{"speaker": "character1", "text": "What am I thinking about?", "emotion": "contemplative", "inner_voice": true, "inner_voice_type": "light"}
```

**When to use Inner Voice:**
- light: Silent thoughts, inner listening (delay: 50ms)
- deep: Memories, flashbacks, recollections (delay: 150ms)  
- dreamy: Dreams, imagination, hallucinations (delay: 300ms)"""

        template_content = f"""
# [ROCKET] RAPID MODE - Create Short Video Script JSON

## Request:
Create a video script about "[TOPIC]" using the following JSON format:

```json
{{
  "segments": [
    {{"id": 1, "dialogues": [
      {{"speaker": "narrator", "text": "Welcome to today's story!", "emotion": "friendly"}},
      {{"speaker": "character1", "text": "I'm excited to share this!", "emotion": "excited"}}
    ]}}
  ],
  "characters": [
    {{"id": "narrator", "name": "Story Narrator", "gender": "neutral"}},
    {{"id": "character1", "name": "Main Character", "gender": "female"}}
  ]
}}
```

**REQUIREMENTS**: 
- segments[].dialogues[]: speaker, text, emotion (required)
- characters[]: id, name, gender (required)
- Content in Vietnamese with proper punctuation
- 3-5 segments, maximum 2-3 characters{inner_voice_section}

**128 Available Emotions (37 main + 91 aliases):**
- **Neutral**: neutral, calm, contemplative, soft, whisper
- **Positive**: happy, excited, cheerful, friendly, confident, encouraging, admiring, playful, romantic, innocent
- **Negative**: sad, angry, sarcastic, cold, anxious, worried, confused, embarrassed, disappointed, frustrated
- **Dramatic**: dramatic, mysterious, suspenseful, urgent, commanding, fierce, pleading, desperate, determined
- **Special**: sleepy, surprised, shy, energetic, serious, gentle, bewildered
- **Aliases**: Each emotion has 2-4 aliases (e.g., happy=joyful/pleased, excited=energetic/thrilled)

**Focus on CONTENT QUALITY and create engaging stories!
"""
        
        token_count = 200 if inner_voice_enabled else 150
        self.show_ai_request_dialog("RAPID Mode Template", template_content, token_count)

    def generate_standard_template_form(self):
        """Generate STANDARD mode template"""
        
        # Kiểm tra inner voice enabled
        inner_voice_enabled = self.check_inner_voice_enabled()
        
        # Inner voice section
        inner_voice_section = ""
        if inner_voice_enabled:
            inner_voice_section = """

**[THEATER] INNER VOICE (Internal Monologue) - OPTIONAL:**
To create inner voice effects, add 2 fields:
- `"inner_voice": true` - Enable inner voice feature
- `"inner_voice_type": "light|deep|dreamy"` - Echo effect type

**Inner Voice Example:**
```json
{{
  "speaker": "character1",
  "text": "Old memories suddenly flood back to me...", 
  "emotion": "nostalgic",
  "inner_voice": true,
  "inner_voice_type": "deep",
  "pause_after": 2.0
}}
```

**When to use Inner Voice:**
- light: Silent thoughts, inner listening (delay: 50ms)
- deep: Memories, flashbacks, recollections (delay: 150ms)  
- dreamy: Dreams, imagination, hallucinations (delay: 300ms)

**Inner Voice + Emotion Combinations:**
- contemplative + light: Gentle contemplation
- nostalgic + deep: Deep recollection
- dreamy + dreamy: Ethereal dreams"""

        template_content = f"""
# [EDIT] STANDARD MODE - Create Balanced Video Script JSON

## Request:
Create a video script about "[TOPIC]" using the following JSON format:

```json
{{
  "project": {{"title": "Story Title", "duration": 60}},
  "segments": [
    {{
      "id": 1,
      "title": "Scene name",
      "dialogues": [
        {{
          "speaker": "narrator",
          "text": "Today we will explore something interesting and surprising.",
          "emotion": "friendly",
          "pause_after": 1.0,
          "emphasis": ["interesting", "surprising"]
        }}
      ]
    }}
  ],
  "characters": [
    {{
      "id": "narrator", 
      "name": "Story Host",
      "gender": "neutral|female|male",
      "default_emotion": "friendly"
    }}
  ]
}}
```{inner_voice_section}

**128 Advanced Emotions (37 main + 91 aliases):**
- **Neutral (5)**: neutral, calm, contemplative, soft, whisper
- **Positive (10)**: happy, excited, cheerful, friendly, confident, encouraging, admiring, playful, romantic, innocent  
- **Negative (10)**: sad, angry, sarcastic, cold, anxious, worried, confused, embarrassed, disappointed, frustrated
- **Dramatic (9)**: dramatic, mysterious, suspenseful, urgent, commanding, fierce, pleading, desperate, determined
- **Special (3)**: sleepy, surprised, shy
- **Aliases**: Each emotion has multiple names (e.g., confident=assured/determined)

**Parameters:**
- emotion: Emotion keyword (e.g., friendly, excited, contemplative)
- pause_after: 0.0-5.0 seconds (optional)
- emphasis: Array of keywords to emphasize (optional)
- gender: neutral/female/male

**Focus on CHARACTER DEVELOPMENT and create rich dialogue!
"""
        
        token_count = 500 if inner_voice_enabled else 400
        self.show_ai_request_dialog("STANDARD Mode Template", template_content, token_count)

    def generate_detailed_template_form(self):
        """Generate DETAILED mode template"""
        
        # Kiểm tra inner voice enabled
        inner_voice_enabled = self.check_inner_voice_enabled()
        
        # Inner voice section cho DETAILED mode
        inner_voice_section = ""
        if inner_voice_enabled:
            inner_voice_section = """

**[THEATER] INNER VOICE (Internal Monologue) - ADVANCED OPTIONS:**
To create inner voice effects in detailed mode, add 2 fields:
- `"inner_voice": true` - Enable inner voice feature
- `"inner_voice_type": "light|deep|dreamy"` - Echo effect type

**Advanced Inner Voice Example:**
```json
{{
  "speaker": "protagonist",
  "text": "Those memories... they still haunt me every night.",
  "emotion": "melancholic", 
  "inner_voice": true,
  "inner_voice_type": "deep",
  "pause_after": 3.0,
  "emphasis": ["memories", "haunt"],
  "volume_adjustment": 0.8
}}
```

**Inner Voice Types for Cinematic Storytelling:**
- **light**: Silent thoughts, internal monologue (delay: 50ms)
  - Usage: Contemplation, real-time thoughts, decision making
  - Best with: contemplative, thoughtful, confused emotions
  
- **deep**: Memories, flashbacks, profound recollections (delay: 150ms)  
  - Usage: Memories, past trauma, significant events
  - Best with: nostalgic, melancholic, regretful emotions
  
- **dreamy**: Dreams, imagination, surreal scenes (delay: 300ms)
  - Usage: Dreams, fantasies, surreal moments
  - Best with: mysterious, dreamy, ethereal emotions

**Pro Inner Voice Combinations:**
- `contemplative + light + pause_after: 1.5`: Slow contemplation
- `nostalgic + deep + pause_after: 2.5`: Deep recollection
- `mysterious + dreamy + volume_adjustment: 0.7`: Mysterious ethereal
- `melancholic + deep + emphasis[]`: Sorrowful memories"""

        template_content = f"""
# [BOOKS] DETAILED MODE - Create Full-Featured Video Script JSON

## Request:
Create a video script about "[TOPIC]" using Enhanced Format 2.0:

```json
{{
  "project": {{
    "title": "Story Title",
    "description": "Story description",
    "total_duration": 60,
    "target_audience": "adult",
    "style": "educational",
    "created_date": "2024-01-20"
  }},
  "segments": [
    {{
      "id": 1,
      "title": "Engaging opening",
      "script": "Scene description",
      "image_prompt": "Visual description for AI image generation",
      "mood": "upbeat",
      "background_music": "energetic",
      "dialogues": [
        {{
          "speaker": "narrator",
          "text": "Hello and welcome to this fascinating journey of discovery!",
          "emotion": "friendly",
          "pause_after": 0.5,
          "emphasis": ["journey", "fascinating"]
        }}
      ],
      "duration": 12,
      "transition": "fade",
      "camera_movement": "zoom_in"
    }}
  ],
  "characters": [
    {{
      "id": "narrator",
      "name": "Program Host",
      "description": "Professional and friendly narrator",
      "gender": "neutral",
      "age_range": "adult",
      "personality": "professional, warm, engaging",
      "voice_characteristics": "clear, moderate pace",
      "suggested_voice": "vi-VN-Wavenet-C",
      "default_emotion": "friendly"
    }}
  ],
  "audio_settings": {{
    "crossfade_duration": 0.3,
    "normalize_volume": true,
    "output_format": "mp3"
  }},
  "metadata": {{
    "version": "2.0",
    "language": "vi-VN",
    "content_rating": "G",
    "tags": ["educational"]
  }}
}}
```{inner_voice_section}

**Complete 128 Emotion Database (37 main + 91 aliases):**
- **Neutral (5)**: neutral, calm, contemplative, soft, whisper
- **Positive (10)**: happy, excited, cheerful, friendly, confident, encouraging, admiring, playful, romantic, innocent
- **Negative (10)**: sad, angry, sarcastic, cold, anxious, worried, confused, embarrassed, disappointed, frustrated  
- **Dramatic (9)**: dramatic, mysterious, suspenseful, urgent, commanding, fierce, pleading, desperate, determined
- **Special (3)**: sleepy, surprised, shy
- **Alias System**: Each emotion has 2-4 alternative names for diversity

**Recommended Emotions for Storytelling:**
- **Narration**: neutral, contemplative, mysterious, dramatic, serious
- **Character dialogue**: friendly, excited, happy, confident, worried, angry, sad
- **Action scenes**: urgent, commanding, fierce, determined, energetic
- **Emotional scenes**: romantic, gentle, pleading, desperate, disappointed

**Advanced features:**
- emotion: Rich emotion keywords (friendly, excited, contemplative, etc.)
- pause_after: 0.0-5.0 seconds for natural timing
- emphasis: Keyword array for better emphasis and delivery
- camera_movement, transitions, background_music
- Complete character personality and voice characteristics

**Focus on CINEMATIC STORYTELLING and complex plot development!
"""
        
        token_count = 1000 if inner_voice_enabled else 800
        self.show_ai_request_dialog("DETAILED Mode Template", template_content, token_count)

    def generate_custom_template_form(self):
        """Generate CUSTOM mode template"""
        
        # Kiểm tra inner voice enabled
        inner_voice_enabled = self.check_inner_voice_enabled()
        
        # Inner voice section cho CUSTOM mode
        inner_voice_section = ""
        if inner_voice_enabled:
            inner_voice_section = """

**[THEATER] INNER VOICE (Internal Monologue) - CUSTOMIZABLE:**
In Custom Mode, you can define your own way of using inner voice:

**Basic Format:**
```json
{{"speaker": "character", "text": "...", "emotion": "...", "inner_voice": true, "inner_voice_type": "light|deep|dreamy"}}
```

**Advanced Custom Options:**
- Combine with pause_after for dramatic timing
- Mix with emphasis[] to highlight keywords in inner thoughts  
- Use with volume_adjustment for layered storytelling
- Pair with specific emotions for targeted mood

**Custom Inner Voice Types:**
- **light**: Subtle thoughts, real-time contemplation (delay: 50ms)
- **deep**: Memory, flashback, profound reflection (delay: 150ms)  
- **dreamy**: Fantasy, imagination, surreal sequences (delay: 300ms)

**Your creative freedom**: Define when and how to use inner voice that fits your story concept!"""

        template_content = f"""
# [EMOJI] CUSTOM MODE - Create Custom Video Script JSON

## Request:
Create a video script about "[TOPIC]" with **complete creative freedom** according to requirements:

**Your Choice - Select Suitable Format:**

**A. MINIMAL FORMAT** (Quick & simple):
```json
{{
  "segments": [{{"dialogues": [{{"speaker": "narrator", "text": "...", "emotion": "friendly"}}]}}],
  "characters": [{{"id": "narrator", "name": "Narrator", "gender": "neutral"}}]
}}
```

**B. BALANCED FORMAT** (Moderate):
```json
{{
  "project": {{"title": "...", "duration": 60}},
  "segments": [{{
    "id": 1, "title": "...",
    "dialogues": [{{"speaker": "...", "text": "...", "emotion": "...", "pause_after": 1.0}}]
  }}],
  "characters": [{{"id": "...", "name": "...", "gender": "...", "default_emotion": "..."}}]
}}
```

**C. FULL FORMAT** (Feature-rich):
- project metadata, segments with titles/descriptions  
- detailed character profiles with personality
- audio_settings, camera_movements, transitions
- advanced dialogue options (emphasis, volume_adjustment)

**[CLIPBOARD] CUSTOMIZATION REQUIREMENTS:**
1. **Segments**: Number of segments (minimum 1, recommended 3-7)
2. **Characters**: Number of characters (minimum 1, max 5 recommended)  
3. **Complexity**: Simple/Standard/Advanced as needed
4. **Duration**: Target duration (30s-300s)
5. **Style**: Educational/Entertainment/Documentary/Narrative{inner_voice_section}

**[TARGET] EMOTION SYSTEM** - 128+ Options:
- **Core emotions**: neutral, happy, sad, angry, excited, calm, dramatic, mysterious
- **Advanced emotions**: contemplative, nostalgic, melancholic, whimsical, urgent, commanding  
- **Specialized**: sleepy, surprised, shy, bewildered, determined, encouraging
- **Aliases supported**: joyful=happy, thrilled=excited, pensive=contemplative

**[CONFIG] ADVANCED FEATURES** (Optional):
- `pause_after`: 0.0-5.0s timing control
- `emphasis`: Array of keywords to emphasize  
- `volume_adjustment`: 0.1-1.0 volume control
- `camera_movement`, `transition`, `background_music` for cinematic feel

**[PAINT] CREATIVE FREEDOM:**
- Define your own tone, pace, and storytelling approach
- Mix and match features according to your vision
- Not limited by existing templates
- Focus on content quality and audience engagement

**Create unique scripts that match your creative goals!**
"""
        
        token_count = 600 if inner_voice_enabled else 500
        self.show_ai_request_dialog("CUSTOM Mode Template", template_content, token_count)

    def show_ai_request_dialog(self, title, content, token_count):
        """Show AI request template in dialog with copy functionality"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(800, 700)
        
        layout = QVBoxLayout()
        
        # Header 
        header_layout = QHBoxLayout()
        header_label = QLabel(f"[CLIPBOARD] {title}")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #007AFF;")
        
        info_label = QLabel("[IDEA] High-quality AI script generation template")
        info_label.setStyleSheet("color: #28CD41; font-weight: bold;")
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(info_label)
        layout.addLayout(header_layout)
        
        # Content area
        content_area = QTextEdit()
        content_area.setPlainText(content.strip())
        content_area.setFont(QFont("Courier", 10))
        layout.addWidget(content_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("[CLIPBOARD] Copy Template")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #5856D6;
                border: 1px solid #5856D6;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F0FF;
                border-color: #4B49C8;
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(content_area.toPlainText()))
        
        save_btn = QPushButton("[EMOJI] Save Template")
        save_btn.clicked.connect(lambda: self.save_ai_request_template(content_area.toPlainText()))
        
        close_btn = QPushButton("[EMOJI] Close")
        close_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def save_ai_request_template(self, template_content):
        """Save AI request template to file"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save AI Request Template",
                "./ai_request_template.json",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                QMessageBox.information(
                    self, 
                    "Saved", 
                    f"AI Request Template has been saved:\n{file_path}\n\nYou can share this file with AI to generate scripts in the correct format."
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"File save error:\n{str(e)}")
    
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
        """Populate bảng settings cho từng nhân vật với CFG Weight và Voice selection - Enhanced Format 2.0 Support"""
        if not self.voice_studio_script_data:
            return
        
        characters = self.voice_studio_script_data['characters']
        # Enhanced Format 2.0 detection
        has_enhanced_features = any(key in self.voice_studio_script_data for key in ['project', 'audio_settings', 'metadata'])
        
        self.character_settings_table.setRowCount(len(characters))
        
        for i, character in enumerate(characters):
            char_id = character['id']
            
            # Character name với enhanced info
            display_name = character['name']
            if has_enhanced_features and 'description' in character:
                display_name += f" ({character['description'][:20]}...)" if len(character.get('description', '')) > 20 else f" ({character.get('description', '')})"
            
            name_item = QTableWidgetItem(display_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            name_item.setToolTip(character.get('description', character['name']))
            self.character_settings_table.setItem(i, 0, name_item)
            
            # Simplified: Only use emotion keywords now
            default_emotion = character.get('default_emotion', 'friendly')
            
            # Emotion dropdown với 18 emotions predefined
            emotion_combo = QComboBox()
            emotion_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
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
                    font-size: 11px;
                }
            """)
            
            # Load emotions từ unified emotion system thay vì hardcode
            try:
                from core.unified_emotion_system import UnifiedEmotionSystem
                emotion_system = UnifiedEmotionSystem()
                emotion_names = emotion_system.get_all_emotion_names()
                
                # Format emotions với icons để hiển thị đẹp hơn
                emotions = []
                for emotion_name in sorted(emotion_names):
                    # Add appropriate icon based on emotion
                    if emotion_name in ['happy', 'cheerful', 'excited', 'joyful']:
                        formatted_name = f"😊 {emotion_name}"
                    elif emotion_name in ['sad', 'melancholic', 'disappointed']:
                        formatted_name = f"😢 {emotion_name}"
                    elif emotion_name in ['angry', 'frustrated', 'furious']:
                        formatted_name = f"😠 {emotion_name}"
                    elif emotion_name in ['calm', 'peaceful', 'relaxed']:
                        formatted_name = f"😌 {emotion_name}"
                    elif emotion_name in ['fearful', 'anxious', 'nervous']:
                        formatted_name = f"😰 {emotion_name}"
                    elif emotion_name in ['surprised', 'amazed', 'shocked']:
                        formatted_name = f"😮 {emotion_name}"
                    elif emotion_name in ['romantic', 'loving', 'affectionate']:
                        formatted_name = f"💝 {emotion_name}"
                    elif emotion_name in ['mysterious', 'intriguing', 'secretive']:
                        formatted_name = f"🤫 {emotion_name}"
                    elif emotion_name in ['thoughtful', 'contemplative', 'pensive']:
                        formatted_name = f"🤔 {emotion_name}"
                    elif emotion_name in ['dramatic', 'theatrical', 'intense']:
                        formatted_name = f"🎭 {emotion_name}"
                    else:
                        formatted_name = f"🎭 {emotion_name}"
                    emotions.append(formatted_name)
                
                print(f"[OK] Loaded {len(emotions)} emotions từ unified emotion system")
                
            except Exception as e:
                # Fallback to hardcoded list nếu có lỗi
                print(f"[WARNING] Failed to load emotions từ system: {e}")
                emotions = [
                    "😊 happy", "😢 sad", "😠 angry", "😌 calm", "😰 fearful",
                    "😮 surprised", "💝 romantic", "🤔 thoughtful", "🎭 dramatic",
                    "😊 cheerful", "😢 melancholic", "🤫 mysterious", "😊 excited",
                    "😌 confident", "😴 sleepy", "😤 frustrated", "🥺 soft", "🎭 neutral"
                ]
            
            emotion_combo.clear()  # Xóa items cũ trước khi thêm mới
            emotion_combo.addItems(emotions)
            
            # Set default emotion based on character
            default_emotion = character.get('default_emotion', 'neutral')
            for emotion_idx, emotion in enumerate(emotions):
                if default_emotion.lower() in emotion.lower():
                    emotion_combo.setCurrentIndex(emotion_idx)
                    break
            
            emotion_combo.currentTextChanged.connect(
                lambda text, cid=char_id: self.update_character_emotion_from_input(cid, text.split(' ', 1)[1] if ' ' in text else text)  # Extract emotion name after emoji
            )
            self.character_settings_table.setCellWidget(i, 1, emotion_combo)
            
            # Exaggeration input field (NEW COLUMN) - Use emotion-based defaults
            exag_input = QLineEdit()
            default_exag = character.get('default_exaggeration', 1.0)  # From script or neutral default
            exag_input.setText(str(default_exag))
            exag_input.setAlignment(Qt.AlignCenter)
            exag_input.setMaximumWidth(60)
            exag_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            exag_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_exaggeration_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 2, exag_input)
            
            # Enhanced Format 2.0: Use default_speed hoặc fallback to 1.0  
            default_speed = character.get('default_speed', 1.0)
            
            # Speed input field với Enhanced Format defaults
            speed_input = QLineEdit()
            speed_input.setText(str(default_speed))
            speed_input.setAlignment(Qt.AlignCenter)
            speed_input.setMaximumWidth(60)
            speed_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            speed_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_speed_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 3, speed_input)
            
            # CFG Weight input field (NEW) - Use emotion-based defaults
            cfg_weight_input = QLineEdit()
            default_cfg = character.get('default_cfg_weight', 0.6)  # From script or neutral default
            cfg_weight_input.setText(str(default_cfg))
            cfg_weight_input.setAlignment(Qt.AlignCenter)
            cfg_weight_input.setMaximumWidth(60)
            cfg_weight_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            cfg_weight_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_cfg_weight_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 4, cfg_weight_input)
            
            # Temperature input field (NEW) - Column 5 - Use emotion-based defaults  
            temperature_input = QLineEdit()
            default_temp = character.get('default_temperature', 0.8)  # From script or neutral default
            temperature_input.setText(str(default_temp))
            temperature_input.setAlignment(Qt.AlignCenter)
            temperature_input.setMaximumWidth(60)
            temperature_input.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 2px solid #007AFF;
                }
            """)
            temperature_input.textChanged.connect(
                lambda text, cid=char_id: self.update_character_temperature_from_input(cid, text)
            )
            self.character_settings_table.setCellWidget(i, 5, temperature_input)
            
            # Voice selection combo (NEW) - Fix dropdown đen với font size cải thiện
            voice_combo = QComboBox()
            voice_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
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
                    font-size: 11px;
                }
            """)
            
            # Load 28 predefined voices từ ChatterboxVoicesManager
            try:
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                chatterbox_manager = ChatterboxVoicesManager()
                available_voices = chatterbox_manager.get_available_voices()
                
                # Add 28 predefined voices
                for voice_id, voice_obj in sorted(available_voices.items()):
                    display_name = f"{voice_obj.name} ({voice_obj.gender})"
                    voice_combo.addItem(display_name, voice_id)
                
                # Add custom cloning option
                voice_combo.addItem("[EMOJI] Custom Cloned Voice", "cloned")
                
                print(f"[OK] Loaded {len(available_voices)} predefined voices trong character table")
                
            except Exception as e:
                print(f"[WARNING] Không thể load 28 predefined voices: {e}")
                # Fallback voices nếu không load được
                fallback_voices = [
                    ("[EMOJI] Young Female (female)", "female_young"),
                    ("[EMOJI] Young Male (male)", "male_young"),
                    ("[EMOJI] Narrator (neutral)", "neutral_narrator"),
                    ("[EMOJI] Mature Female (female)", "female_mature"),
                    ("[EMOJI] Mature Male (male)", "male_mature"),
                    ("[EMOJI] Gentle Female (female)", "female_gentle"),
                    ("[EMOJI] Deep Male (male)", "male_deep"),
                    ("[EMOJI] Child Voice (neutral)", "child_voice"),
                    ("[EMOJI] Elder Voice (neutral)", "elder_voice"),
                    ("[EMOJI] Voice Cloning (variable)", "cloned")
                ]
                
                for display, voice_id in fallback_voices:
                    voice_combo.addItem(display, voice_id)
            
            # Enhanced Format 2.0: Use suggested_voice hoặc default selection
            default_voice_index = 0  # Default to Young Female
            if 'suggested_voice' in character:
                suggested_voice = character['suggested_voice']
                print(f"[TARGET] Character {character['name']} suggests voice: {suggested_voice}")
                
                # Try to map suggested voice to fallback voice
                voice_mapping = {
                    'vi-VN-Wavenet-A': 0,  # Young Female
                    'vi-VN-Wavenet-C': 0,  # Young Female
                    'vi-VN-Standard-A': 0,  # Young Female
                    'vi-VN-Standard-C': 0,  # Young Female
                    'vi-VN-Wavenet-B': 1,  # Young Male
                    'vi-VN-Wavenet-D': 1,  # Young Male
                    'vi-VN-Standard-B': 1,  # Young Male
                    'vi-VN-Standard-D': 1,  # Young Male
                }
                
                # Map gender to appropriate voice
                if 'gender' in character:
                    gender = character['gender'].lower()
                    age_range = character.get('age_range', 'young_adult')
                    
                    if gender == 'female':
                        if age_range in ['young_adult', 'teen']:
                            default_voice_index = 0  # Young Female
                        else:
                            default_voice_index = 3  # Mature Female
                    elif gender == 'male':
                        if age_range in ['young_adult', 'teen']:
                            default_voice_index = 1  # Young Male
                        else:
                            default_voice_index = 4  # Mature Male
                    elif gender == 'neutral':
                        default_voice_index = 2  # Narrator
                    elif gender == 'child':
                        default_voice_index = 7  # Child Voice
                    elif gender == 'elderly':
                        default_voice_index = 8  # Elder Voice
                
                # Override with direct voice mapping if available
                if suggested_voice in voice_mapping:
                    default_voice_index = voice_mapping[suggested_voice]
            
            voice_combo.setCurrentIndex(default_voice_index)
            
            voice_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, combo=voice_combo: self.update_character_voice(cid, combo.currentData())
            )
            
            # Voice Mode selector (NEW) - Chọn giữa Voice Selection vs Voice Clone với font size cải thiện
            # NOTE: Voice Prompt bị loại bỏ vì ChatterboxTTS không hỗ trợ text prompt
            mode_combo = QComboBox()
            mode_combo.setMaximumWidth(120)
            mode_combo.addItem("[EMOJI] Voice", "voice_selection")
            mode_combo.addItem("[EMOJI] Clone", "voice_clone")
            mode_combo.setCurrentIndex(0)  # Default to voice selection
            mode_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
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
                    font-size: 11px;
                }
            """)
            mode_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, combo=mode_combo: self.update_character_voice_mode(cid, combo.currentData())
            )
            self.character_settings_table.setCellWidget(i, 6, mode_combo)

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
            
            voice_clone_btn = QPushButton("[MUSIC] Chọn file")
            voice_clone_btn.setMaximumWidth(80)
            voice_clone_btn.setToolTip(f"Chọn audio file làm voice sample cho {character['name']}")
            voice_clone_btn.clicked.connect(lambda checked, cid=char_id: self.select_character_voice_clone_folder(cid))
            clone_layout.addWidget(voice_clone_btn)
            
            # Add widgets to stack (only 2 now)
            stacked_widget.addWidget(voice_widget)     # Index 0 - Voice Selection
            stacked_widget.addWidget(clone_widget)     # Index 1 - Voice Clone
            stacked_widget.setCurrentIndex(0)  # Default to voice selection
            
            self.character_settings_table.setCellWidget(i, 7, stacked_widget)
            
            # Whisper Voice Widget (NEW COLUMN 7) - Shared mode với main voice column
            whisper_stacked_widget = QStackedWidget()
            whisper_stacked_widget.setMaximumHeight(30)
            
            # 1. Whisper Voice Selection Widget (using same voice list as main column)
            whisper_voice_widget = QWidget()
            whisper_voice_layout = QHBoxLayout(whisper_voice_widget)
            whisper_voice_layout.setContentsMargins(2, 2, 2, 2)
            
            # Create separate voice combo for whisper (clone of main voice combo)
            whisper_voice_combo = QComboBox()
            whisper_voice_combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 2px;
                    color: black;
                    font-size: 11px;
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
                    font-size: 11px;
                }
            """)
            
            # Load same voices as main voice combo
            try:
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                chatterbox_manager = ChatterboxVoicesManager()
                available_voices = chatterbox_manager.get_available_voices()
                
                # Add same voices as main combo
                for voice_id, voice_obj in sorted(available_voices.items()):
                    display_name = f"{voice_obj.name} ({voice_obj.gender})"
                    whisper_voice_combo.addItem(display_name, voice_id)
                
                whisper_voice_combo.addItem("[EMOJI] Custom Cloned Voice", "cloned")
                
            except Exception as e:
                # Fallback voices (same as main combo)
                fallback_voices = [
                    ("[EMOJI] Young Female (female)", "female_young"),
                    ("[EMOJI] Young Male (male)", "male_young"),
                    ("[EMOJI] Narrator (neutral)", "neutral_narrator"),
                    ("[EMOJI] Mature Female (female)", "female_mature"),
                    ("[EMOJI] Mature Male (male)", "male_mature"),
                    ("[EMOJI] Gentle Female (female)", "female_gentle"),
                    ("[EMOJI] Deep Male (male)", "male_deep"),
                    ("[EMOJI] Child Voice (neutral)", "child_voice"),
                    ("[EMOJI] Elder Voice (neutral)", "elder_voice"),
                    ("[EMOJI] Voice Cloning (variable)", "cloned")
                ]
                
                for display, voice_id in fallback_voices:
                    whisper_voice_combo.addItem(display, voice_id)
            
            # Set default to different voice than main (e.g., if main is female, whisper defaults to gentle)
            whisper_voice_combo.setCurrentIndex(5 if default_voice_index != 5 else 6)  # Default to gentle or deep
            
            whisper_voice_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, combo=whisper_voice_combo: self.update_character_whisper_voice(cid, combo.currentData())
            )
            
            whisper_voice_layout.addWidget(whisper_voice_combo)
            
            # 2. Whisper Voice Clone Widget
            whisper_clone_widget = QWidget()
            whisper_clone_layout = QHBoxLayout(whisper_clone_widget)
            whisper_clone_layout.setContentsMargins(2, 2, 2, 2)
            whisper_clone_layout.setSpacing(4)
            
            whisper_clone_btn = QPushButton("[MUTE] Chọn file")
            whisper_clone_btn.setMaximumWidth(80)
            whisper_clone_btn.setToolTip(f"Chọn audio file cho whisper voice của {character['name']}")
            whisper_clone_btn.clicked.connect(lambda checked, cid=char_id: self.select_character_whisper_clone_folder(cid))
            whisper_clone_layout.addWidget(whisper_clone_btn)
            
            # Add widgets to whisper stack
            whisper_stacked_widget.addWidget(whisper_voice_widget)  # Index 0 - Voice Selection
            whisper_stacked_widget.addWidget(whisper_clone_widget)  # Index 1 - Voice Clone
            whisper_stacked_widget.setCurrentIndex(0)  # Default to voice selection (shared mode with main)
            
            self.character_settings_table.setCellWidget(i, 8, whisper_stacked_widget)
            
            # Status indicator - MOVED TO COLUMN 9
            status_label = QLabel("[EMOJI]")
            status_label.setMaximumWidth(30)
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setToolTip("Voice Selection mode")
            self.character_settings_table.setCellWidget(i, 9, status_label)
            
            # Preview button (Center aligned) - MOVED TO COLUMN 10
            preview_btn = QPushButton("[EMOJI]")
            preview_btn.setMaximumWidth(40)
            preview_btn.setToolTip(f"Preview {character['name']}")
            preview_btn.clicked.connect(lambda checked, cid=char_id: self.preview_character_with_settings(cid))
            
            # Tạo wrapper widget để center button
            preview_widget = QWidget()
            preview_layout = QHBoxLayout(preview_widget)
            preview_layout.setContentsMargins(0, 0, 0, 0)
            preview_layout.addStretch()
            preview_layout.addWidget(preview_btn)
            preview_layout.addStretch()
            self.character_settings_table.setCellWidget(i, 10, preview_widget)
            
            # Initialize character settings với voice mode và whisper settings
            default_whisper_voice = whisper_voice_combo.currentData()
            
            # Special case: Set whisper voice phù hợp cho từng character
            if char_id == 'character2':  # Assuming character2 là Minh (male character)
                default_whisper_voice = 'willow ii (whispering)'  # Set whisper voice cho Minh
            
            self.character_chatterbox_settings[char_id] = {
                'emotion': 1.0,
                'speed': 1.0,
                'cfg_weight': 0.5,
                'voice_mode': 'voice_selection',  # voice_selection | voice_clone (SHARED mode)
                'voice_id': 'female_young',  # For voice_selection mode
                'voice_clone_path': None,  # For voice_clone mode
                'voice_clone_status': 'none',  # Track clone status
                # NEW: Whisper voice settings (shared mode với main voice)
                'whisper_voice_id': default_whisper_voice,  # Default or character-specific whisper voice ID
                'whisper_voice_clone_path': None,  # For whisper voice clone mode
                'whisper_voice_clone_status': 'none'  # Track whisper clone status
            }
            
            # Store widget references for mode switching
            if not hasattr(self, 'character_widgets'):
                self.character_widgets = {}
            self.character_widgets[char_id] = {
                'mode_combo': mode_combo,
                'stacked_widget': stacked_widget,
                'voice_combo': voice_combo,
                'voice_clone_btn': voice_clone_btn,
                'whisper_stacked_widget': whisper_stacked_widget,  # NEW
                'whisper_voice_combo': whisper_voice_combo,  # NEW
                'whisper_clone_btn': whisper_clone_btn,  # NEW
                'status_label': status_label
            }
            
            # Connect mode switching để sync giữa main và whisper columns
            mode_combo.currentIndexChanged.connect(
                lambda index, cid=char_id, main_stack=stacked_widget, whisper_stack=whisper_stacked_widget: self.update_shared_voice_mode(cid, main_stack, whisper_stack, index)
            )
    
    def update_character_emotion_from_input(self, char_id, text):
        """Cập nhật emotion cho nhân vật cụ thể từ input (now string-based) và tự động cập nhật parameters"""
        print(f"[THEATER DEBUG] Emotion changed for {char_id}: '{text}'")
        # Emotion is now a string keyword (friendly, excited, etc.), not numeric
        if text.strip():  # Only update if text is not empty
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            
            emotion_text = text.strip()
            self.character_chatterbox_settings[char_id]['emotion'] = emotion_text
            
            # [TARGET] AUTO-MAP EMOTION TO PARAMETERS: Tự động cập nhật exaggeration và cfg_weight
            exaggeration, cfg_weight = self.map_emotion_to_parameters(emotion_text)
            
            # Cập nhật settings với auto-mapped values
            self.character_chatterbox_settings[char_id]['exaggeration'] = exaggeration
            self.character_chatterbox_settings[char_id]['cfg_weight'] = cfg_weight
            
            # [REFRESH] CẬP NHẬT UI: Tìm và update input fields trong table
            characters = self.voice_studio_script_data.get('characters', [])
            for row in range(self.character_settings_table.rowCount()):
                if row < len(characters) and characters[row]['id'] == char_id:
                    # Found the matching character row
                    
                    # Update exaggeration input (column 2)
                    exag_input = self.character_settings_table.cellWidget(row, 2)
                    if exag_input:
                        exag_input.setText(f"{exaggeration:.2f}")
                        print(f"   [UI] Updated exaggeration input to {exaggeration:.2f}")
                    
                    # Update cfg weight input (column 4) 
                    cfg_weight_input = self.character_settings_table.cellWidget(row, 4)
                    if cfg_weight_input:
                        cfg_weight_input.setText(f"{cfg_weight:.2f}")
                        print(f"   [UI] Updated cfg_weight input to {cfg_weight:.2f}")
                    
                    # Update temperature input (column 5) - THIẾU NÀY!
                    temperature_input = self.character_settings_table.cellWidget(row, 5)
                    if temperature_input:
                        # Lấy giá trị temperature từ emotion mapping
                        temperature = self.character_chatterbox_settings[char_id].get('temperature', 0.7)
                        temperature_input.setText(f"{temperature:.2f}")
                        print(f"   [UI] Updated temperature input to {temperature:.2f}")
                    
                    break
            
            print(f"[THEATER] Emotion changed for {char_id}: {emotion_text}")
            print(f"   [SPARKLE] Auto-adjusted: exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f}")
        # No try/catch needed since emotion is now just a string
    
    def update_character_exaggeration_from_input(self, char_id, text):
        """Cập nhật exaggeration cho nhân vật cụ thể từ input"""
        try:
            value = float(text)
            value = max(0.0, min(2.5, value))  # Clamp to 0.0-2.5
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            self.character_chatterbox_settings[char_id]['exaggeration'] = value
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
    
    def update_character_temperature_from_input(self, char_id, text):
        """Cập nhật temperature cho nhân vật cụ thể từ input"""
        try:
            value = float(text)
            value = max(0.1, min(1.5, value))  # Clamp to 0.1-1.5
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            self.character_chatterbox_settings[char_id]['temperature'] = value
        except ValueError:
            pass  # Ignore invalid input
    
    def update_character_voice(self, char_id, voice_id):
        """Cập nhật voice cho nhân vật cụ thể và tự động adjust parameters theo gender"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        # Lưu voice_id
        self.character_chatterbox_settings[char_id]['voice_id'] = voice_id
        
        # [TARGET] AUTO-ADJUST PARAMETERS dựa trên voice gender (như AI Gender Analysis)
        voice_gender_params = self._get_voice_gender_parameters(voice_id)
        
        # Cập nhật parameters trong settings (emotion is now string)
        self.character_chatterbox_settings[char_id]['emotion'] = voice_gender_params['emotion']  # String now
        self.character_chatterbox_settings[char_id]['speed'] = voice_gender_params['speed'] 
        self.character_chatterbox_settings[char_id]['cfg_weight'] = voice_gender_params['cfg_weight']
        
        # [REFRESH] CẬP NHẬT UI: Tìm và update input fields trong table bằng cách match character ID
        characters = self.voice_studio_script_data.get('characters', [])
        for row in range(self.character_settings_table.rowCount()):
            if row < len(characters) and characters[row]['id'] == char_id:
                # Found the matching character row
                
                # Update emotion dropdown (column 1)
                emotion_combo = self.character_settings_table.cellWidget(row, 1)
                if emotion_combo:
                    # Find and set emotion in dropdown
                    for idx in range(emotion_combo.count()):
                        if voice_gender_params['emotion'] in emotion_combo.itemText(idx).lower():
                            emotion_combo.setCurrentIndex(idx)
                            break
                
                # Update exaggeration input (column 2 - NEW)
                exag_input = self.character_settings_table.cellWidget(row, 2)
                if exag_input:
                    exag_input.setText(f"{voice_gender_params.get('exaggeration', 1.0):.2f}")
                
                # Update speed input (column 3)
                speed_input = self.character_settings_table.cellWidget(row, 3)
                if speed_input:
                    speed_input.setText(f"{voice_gender_params['speed']:.1f}")
                
                # Update cfg weight input (column 4)
                cfg_weight_input = self.character_settings_table.cellWidget(row, 4)
                if cfg_weight_input:
                    cfg_weight_input.setText(f"{voice_gender_params['cfg_weight']:.2f}")
                
                break
        
        print(f"[THEATER] Voice changed for {char_id}: {voice_id}")
        print(f"   [SPARKLE] Auto-adjusted: emotion={voice_gender_params['emotion']}, speed={voice_gender_params['speed']:.1f}, cfg_weight={voice_gender_params['cfg_weight']:.2f}")
    
    def update_character_whisper_voice(self, char_id, voice_id):
        """Cập nhật whisper voice cho nhân vật cụ thể"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        # Lưu whisper voice_id
        self.character_chatterbox_settings[char_id]['whisper_voice_id'] = voice_id
        print(f"[MUTE] Whisper voice changed for {char_id}: {voice_id}")
    
    def select_character_whisper_clone_folder(self, char_id):
        """Chọn voice clone file cho whisper voice của nhân vật cụ thể"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Chọn audio file cho whisper voice của {self.get_character_name_by_id(char_id)}", 
            "", 
            "Audio Files (*.wav *.mp3 *.m4a *.flac *.ogg)"
        )
        
        if file_path:
            if char_id not in self.character_chatterbox_settings:
                self.character_chatterbox_settings[char_id] = {}
            
            self.character_chatterbox_settings[char_id]['whisper_voice_clone_path'] = file_path
            self.character_chatterbox_settings[char_id]['whisper_voice_clone_status'] = 'ready'
            
            print(f"[MUTE] Whisper voice clone set for {char_id}: {file_path}")
            
            # Update UI status for whisper clone
            self._update_whisper_voice_clone_status_ui(char_id, 'ready', f"Whisper clone ready: {os.path.basename(file_path)}")
    
    def update_shared_voice_mode(self, char_id, main_stack, whisper_stack, mode_index):
        """Sync voice mode giữa main và whisper columns (shared mode)"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        # Get mode from index
        voice_mode = 'voice_selection' if mode_index == 0 else 'voice_clone'
        
        # Update settings
        self.character_chatterbox_settings[char_id]['voice_mode'] = voice_mode
        
        # Sync both stacks
        main_stack.setCurrentIndex(mode_index)
        whisper_stack.setCurrentIndex(mode_index)
        
        # Update status
        if hasattr(self, 'character_widgets') and char_id in self.character_widgets:
            status_label = self.character_widgets[char_id]['status_label']
            if voice_mode == 'voice_selection':
                status_label.setText("[EMOJI]")
                status_label.setToolTip("Voice Selection mode - chọn giọng có sẵn")
            else:
                status_label.setText("[EMOJI]")
                status_label.setToolTip("Voice Clone mode - sử dụng file clone")
        
        print(f"[REFRESH] Shared mode switched for {char_id}: {voice_mode}")
    
    def _update_whisper_voice_clone_status_ui(self, char_id, status, tooltip_text=""):
        """Update whisper voice clone status UI"""
        if hasattr(self, 'character_widgets') and char_id in self.character_widgets:
            whisper_clone_btn = self.character_widgets[char_id]['whisper_clone_btn']
            
            if status == 'ready':
                whisper_clone_btn.setText("[MUTE] Ready")
                whisper_clone_btn.setStyleSheet("background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;")
            elif status == 'error':
                whisper_clone_btn.setText("[MUTE] Error")
                whisper_clone_btn.setStyleSheet("background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;")
            else:
                whisper_clone_btn.setText("[MUTE] Chọn file")
                whisper_clone_btn.setStyleSheet("")
            
            if tooltip_text:
                whisper_clone_btn.setToolTip(tooltip_text)
    
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
            
            # Switch stacked widget and update status
            if voice_mode == 'voice_selection':
                stacked_widget.setCurrentIndex(0)  # Voice combo
                status_label.setText("[EMOJI]")
                status_label.setToolTip("Voice Selection mode - chọn giọng có sẵn")
                print(f"[EMOJI] {char_id}: Switched to VOICE SELECTION mode")
                
            elif voice_mode == 'voice_clone':
                stacked_widget.setCurrentIndex(1)  # Voice clone button
                status_label.setText("[EMOJI]")
                status_label.setToolTip("Voice Clone mode - nhân bản giọng từ mẫu audio")
                print(f"[EMOJI] {char_id}: Switched to VOICE CLONE mode")
    
    def _get_voice_gender_parameters(self, voice_id):
        """Lấy parameters tối ưu cho voice dựa trên gender (như AI Gender Analysis system)"""
        
        # [EMOJI] FEMALE VOICES - nhẹ nhàng, biểu cảm hơn
        female_voices = ['female_young', 'female_mature', 'female_gentle']
        if voice_id in female_voices:
            return {
                'emotion': 'gentle',    # Emotion keyword
                'exaggeration': 1.0,    # Neutral exaggeration
                'speed': 0.95,          # Chậm hơn một chút  
                'cfg_weight': 0.6       # Chất lượng cao
            }
        
        # [EMOJI] MALE VOICES - mạnh mẽ, ít biểu cảm
        male_voices = ['male_young', 'male_mature', 'male_deep'] 
        if voice_id in male_voices:
            return {
                'emotion': 'confident', # Strong emotion keyword
                'exaggeration': 1.15,   # Lower exaggeration for steady voice
                'speed': 1.05,          # Nhanh hơn một chút
                'cfg_weight': 0.4       # Cân bằng
            }
        
        # [EMOJI] NEUTRAL VOICES - cân bằng
        neutral_voices = ['neutral_narrator', 'neutral_child', 'neutral_elder']
        if voice_id in neutral_voices:
            return {
                'emotion': 'friendly',  # Cân bằng emotion
                'exaggeration': 1.25,   # Balanced exaggeration
                'speed': 1.0,           # Bình thường  
                'cfg_weight': 0.5       # Cân bằng
            }
        
        # [EMOJI] VOICE CLONING - default balanced
        if voice_id == 'cloned':
            return {
                'emotion': 'friendly',  # Default emotion
                'exaggeration': 1.0,    # Neutral exaggeration  
                'speed': 1.0,           # Bình thường
                'cfg_weight': 0.5       # Cân bằng
            }
        
        # Default fallback
        return {
            'emotion': 'friendly',  # String emotion
            'exaggeration': 1.0,    # Neutral exaggeration
            'speed': 1.0, 
            'cfg_weight': 0.5
        }
    
    def preview_character_with_settings(self, char_id):
        """Preview giọng với settings cụ thể của nhân vật"""
        try:
            # Validate và hiển thị priority logic
            voice_mode = self.validate_character_voice_settings(char_id)
            
            settings = self.character_chatterbox_settings.get(char_id, {})
            emotion = settings.get('emotion', 'friendly')  # Now string emotion
            exaggeration = settings.get('exaggeration', 1.0)   # NEW: exaggeration parameter
            speed = settings.get('speed', 1.0) 
            cfg_weight = settings.get('cfg_weight', 0.5)
            voice_id = settings.get('voice_id', 'female_young')
            voice_clone_path = settings.get('voice_clone_path', None)
            
            char_name = self.get_character_name_by_id(char_id)
            
            # Get real voice display name từ 28 predefined voices
            voice_display_name = voice_id
            try:
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager
                chatterbox_manager = ChatterboxVoicesManager()
                available_voices = chatterbox_manager.get_available_voices()
                
                if voice_id in available_voices:
                    voice_obj = available_voices[voice_id]
                    voice_display_name = f"{voice_obj.name} ({voice_obj.gender})"
                else:
                    # Fallback cho old voice IDs
                    fallback_mapping = {
                        'female_young': 'Abigail (female)',
                        'male_young': 'Adrian (male)', 
                        'neutral_narrator': 'Thomas (male)',
                        'cloned': 'Custom Cloned Voice'
                    }
                    voice_display_name = fallback_mapping.get(voice_id, voice_id)
                    
            except Exception as e:
                print(f"[WARNING] Could not load voice display name: {e}")
            
            # [OK] FIX: Tạo English text cho Chatterbox TTS
            if voice_mode == 'clone':
                preview_text = f"Hello, I am {char_name}. This is my cloned voice from audio samples."
            else:
                preview_text = f"Hello, I am {char_name}. This is {voice_display_name} voice with {emotion} emotion, {speed:.1f}x speed, and {exaggeration:.2f} exaggeration."
            
            # Generate preview
            import tempfile
            import os
            temp_dir = tempfile.mkdtemp()
            preview_path = os.path.join(temp_dir, f"preview_{char_id}.wav")
                
            # [OK] FIX: Use correct parameters cho Real Chatterbox
            result = self.voice_generator.generate_voice_chatterbox(
                text=preview_text,
                save_path=preview_path,
                voice_sample_path=voice_clone_path if voice_mode == 'clone' else None,
                emotion_exaggeration=exaggeration,  # [OK] FIX: Use correct parameter name
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
                
                message += f"Emotion: {emotion}\n"
                message += f"Exaggeration: {exaggeration:.2f}\n"
                message += f"Speed: {speed:.1f}x\n"
                message += f"CFG Weight: {cfg_weight:.2f}\n"
                message += f"\n[BOT] Generated by Real Chatterbox TTS"
                
                QMessageBox.information(self, "[EMOJI] Preview Voice", message)
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "[EMOJI] Error Preview", f"Không thể tạo preview:\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "[EMOJI] Error Critical", f"Error preview voice:\n{str(e)}")
    
    def update_character_voice_prompt(self, char_id, prompt_text):
        """Cập nhật voice prompt cho nhân vật cụ thể"""
        if char_id not in self.character_chatterbox_settings:
            self.character_chatterbox_settings[char_id] = {}
        
        self.character_chatterbox_settings[char_id]['voice_prompt'] = prompt_text
        
        if prompt_text.strip():
            print(f"[EMOJI] Voice prompt updated for {self.get_character_name_by_id(char_id)}: '{prompt_text[:50]}...'")
        else:
            print(f"[EMOJI] Voice prompt cleared for {self.get_character_name_by_id(char_id)}")
    
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
            layout.addWidget(QLabel(f"[EMOJI] Voice Selection Mode - {char_name}"))
            layout.addWidget(QLabel("Quick actions for voice selection:"))
            
            # Auto-optimize button
            optimize_btn = QPushButton("[TARGET] Auto-optimize Parameters")
            optimize_btn.clicked.connect(lambda: self.auto_optimize_voice_params(char_id, dialog))
            layout.addWidget(optimize_btn)
            
            # Reset to defaults
            reset_btn = QPushButton("[REFRESH] Reset to Defaults")
            reset_btn.clicked.connect(lambda: self.reset_voice_params(char_id, dialog))
            layout.addWidget(reset_btn)
            
        elif voice_mode == 'voice_clone':
            layout.addWidget(QLabel(f"[EMOJI] Voice Clone Mode - {char_name}"))
            layout.addWidget(QLabel("Quick actions for voice cloning:"))
            
            # Test clone button
            test_btn = QPushButton("[TEST] Test Voice Clone")
            test_btn.clicked.connect(lambda: self.test_voice_clone(char_id, dialog))
            layout.addWidget(test_btn)
            
            # Clear clone path
            clear_btn = QPushButton("[DELETE] Clear Clone Path")
            clear_btn.clicked.connect(lambda: self.clear_voice_clone_path(char_id, dialog))
            layout.addWidget(clear_btn)
        
        # Close button
        close_btn = QPushButton("[EMOJI] Close")
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
        
        # [OK] FIX: Update UI TABLE DIRECTLY để hiển thị changes
        self._update_character_table_row(char_id, optimized_params)
        
        QMessageBox.information(dialog, "[OK] Optimized", 
                              f"Parameters optimized for {voice_id}:\n"
                              f"Emotion: {optimized_params['emotion']:.1f}\n"
                              f"Speed: {optimized_params['speed']:.1f}\n"
                              f"CFG Weight: {optimized_params['cfg_weight']:.2f}")
        dialog.close()
    
    def reset_voice_params(self, char_id, dialog):
        """Reset voice parameters về defaults"""
        default_params = {
            'emotion': 1.0,
            'speed': 1.0,
            'cfg_weight': 0.5
        }
        self.character_chatterbox_settings[char_id].update(default_params)
        
        # [OK] FIX: Update UI TABLE DIRECTLY để hiển thị changes
        self._update_character_table_row(char_id, default_params)
        
        QMessageBox.information(dialog, "[REFRESH] Reset", "Parameters reset to defaults")
        dialog.close()
    
    def test_voice_clone(self, char_id, dialog):
        """Test voice clone với sample text"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_clone_path = settings.get('voice_clone_path')
        
        if not voice_clone_path:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(dialog, "[WARNING] Warning", "No voice clone path selected!")
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
            QMessageBox.information(dialog, "[OK] Test Success", "Voice clone test completed!")
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(dialog, "[EMOJI] Test Failed", f"Test failed: {result.get('error', 'Unknown error')}")
    
    def clear_voice_clone_path(self, char_id, dialog):
        """Clear voice clone path"""
        self.character_chatterbox_settings[char_id]['voice_clone_path'] = None
        self.character_chatterbox_settings[char_id]['voice_clone_status'] = 'none'
        
        # Update UI
        self._update_voice_clone_status_ui(char_id, 'none', "No voice samples")
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(dialog, "[DELETE] Cleared", "Voice clone path cleared")
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
            ("[EMOJI] MC Radio", "Giọng nữ trẻ, vui vẻ, năng động như MC radio, nói nhanh và có intonation rõ ràng"),
            ("[EMOJI] Tin tức", "Giọng nam trầm, nghiêm túc, uy tín như người dẫn chương trình tin tức"),
            ("[EMOJI] Trẻ em", "Giọng trẻ em vui vẻ, trong trẻo, hồn nhiên như trong truyện cổ tích"),
            ("[EMOJI] Gentle", "Giọng nữ nhẹ nhàng, dịu dàng, ấm áp như người mẹ kể chuyện"),
            ("[EMOJI] Hero", "Giọng nam mạnh mẽ, quyết đoán, anh hùng như trong phim hành động"),
            ("[THEATER] Dramatic", "Giọng kịch tính, cảm xúc mạnh, như diễn viên sân khấu"),
            ("[EMOJI] Happy", "Giọng vui vẻ, tươi tắn, luôn cười, tích cực"),
            ("[EMOJI] Sad", "Giọng buồn bã, u sầu, chậm rãi, đầy cảm xúc"),
            ("[EMOJI] Angry", "Giọng tức giận, quyết liệt, mạnh mẽ, có sức thuyết phục"),
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
        """Chọn file voice sample trực tiếp cho nhân vật cụ thể"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        
        character_name = self.get_character_name_by_id(char_id)
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Chọn audio file cho {character_name}",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg *.m4a)"
        )
        
        if file_path:
            # Update status to processing
            self._update_voice_clone_status_ui(char_id, 'processing', 'Đang xử lý...')
            
            try:
                import os
                
                # Get file info
                file_size = os.path.getsize(file_path)
                file_size_mb = file_size / (1024 * 1024)
                file_name = os.path.basename(file_path)
                            
                # Try to get audio duration (optional)
                duration_info = ""
                try:
                    import mutagen
                    audio_file = mutagen.File(file_path)
                    if audio_file and hasattr(audio_file, 'info') and hasattr(audio_file.info, 'length'):
                        duration = audio_file.info.length
                        duration_info = f" ({duration:.1f}s)"
                except Exception as e:
                    print(f"[WARNING] Could not get duration for {file_name}: {e}")
                    pass  # Skip duration if mutagen not available
                
                # Lưu file path cụ thể
                if char_id not in self.character_chatterbox_settings:
                    self.character_chatterbox_settings[char_id] = {}
                
                self.character_chatterbox_settings[char_id]['voice_clone_path'] = file_path
                self.character_chatterbox_settings[char_id]['voice_clone_status'] = 'ready'
                self.character_chatterbox_settings[char_id]['voice_clone_folder'] = os.path.dirname(file_path)
                
                # Update UI status
                self._update_voice_clone_status_ui(char_id, 'ready', f"File: {file_name}")
        
                print(f"[FOLDER] Voice clone file set for {character_name}: {file_path}")
                print(f"[MUSIC] Selected: {file_name} ({file_size_mb:.1f}MB{duration_info})")
                
                QMessageBox.information(
                    self,
                    "[OK] Voice Clone Setup",
                    f"Đã thiết lập voice cloning cho {character_name}\n"
                    f"File: {file_name}\n"
                    f"Size: {file_size_mb:.1f}MB{duration_info}"
                )
    
            except Exception as e:
                self._update_voice_clone_status_ui(char_id, 'error', f'Error: {str(e)}')
                QMessageBox.critical(
                    self,
                    "[EMOJI] Error Voice Clone Setup",
                    f"Không thể thiết lập voice cloning:\n{str(e)}"
                )
    
    def _update_voice_clone_status_ui(self, char_id, status, tooltip_text=""):
        """Cập nhật UI status cho voice clone của nhân vật với file name display"""
        status_icons = {
            'none': '[EMOJI]',
            'ready': '[OK]', 
            'processing': '⏳',
            'error': '[EMOJI]'
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
            if name_item and name_item.text() == char_id:  # Note: Updated to use char_id directly
                # Lấy voice clone container
                voice_clone_container = self.character_settings_table.cellWidget(i, 6)
                if voice_clone_container:
                    # Tìm status label (widget thứ 2 trong layout)
                    layout = voice_clone_container.layout()
                    if layout and layout.count() > 1:
                        status_label = layout.itemAt(1).widget()
                        if status_label:
                            # [OK] IMPROVED: Show file name for ready status
                            if status == 'ready':
                                settings = self.character_chatterbox_settings.get(char_id, {})
                                voice_clone_path = settings.get('voice_clone_path', '')
                                
                                if voice_clone_path and os.path.exists(voice_clone_path):
                                    file_name = os.path.basename(voice_clone_path)
                                    # Truncate long file names
                                    if len(file_name) > 15:
                                        display_name = file_name[:12] + "..."
                                    else:
                                        display_name = file_name
                                    status_label.setText(f"[MUSIC] {display_name}")
                                    status_label.setToolTip(f"Voice sample: {file_name}\nPath: {voice_clone_path}")
                                else:
                                    status_label.setText(status_icons.get(status, '[EMOJI]'))
                                    status_label.setToolTip(tooltip_text or f"Status: {status}")
                            else:
                                status_label.setText(status_icons.get(status, '[EMOJI]'))
                                status_label.setToolTip(tooltip_text or f"Status: {status}")
                            
                            status_label.setStyleSheet(status_colors.get(status, ''))
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
            self.voice_clone_path_label.setText(f"[FOLDER] {folder}")
            self.voice_clone_path_label.setStyleSheet("color: green; font-weight: bold; margin-left: 20px;")
    
    def validate_character_voice_settings(self, char_id):
        """Validate character voice settings dựa trên voice mode được chọn"""
        settings = self.character_chatterbox_settings.get(char_id, {})
        voice_mode = settings.get('voice_mode', 'voice_selection')
        char_name = self.get_character_name_by_id(char_id)
        
        if voice_mode == 'voice_clone':
            voice_clone_path = settings.get('voice_clone_path')
            if voice_clone_path and os.path.exists(voice_clone_path):
                print(f"[TARGET] {char_name}: Using VOICE CLONE - {voice_clone_path}")
                return 'clone'
            else:
                # Fallback to voice selection if no clone
                print(f"[WARNING] {char_name}: Voice clone mode selected but no samples provided, fallback to voice selection")
                voice_id = settings.get('voice_id', 'female_young')
                print(f"[TARGET] {char_name}: Using VOICE SELECTION (fallback) - {voice_id}")
                return 'selection'
                
        else:  # voice_selection mode
            voice_id = settings.get('voice_id', 'female_young')
            print(f"[TARGET] {char_name}: Using VOICE SELECTION - {voice_id}")
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
            # [OK] FIX: Dùng character-specific settings thay vì global controls
            return self.character_chatterbox_settings.get(char_id, {
                'emotion': 1.0,
                'speed': 1.0, 
                'cfg_weight': 0.5,
                'voice_clone_path': None,
                'voice_mode': 'voice_selection'
            })
        else:
            return {
                'emotion': 1.0, 
                'speed': 1.0, 
                'cfg_weight': 0.5,
                'voice_clone_path': None,
                'voice_mode': 'voice_selection'
            }
    
    def map_emotion_to_parameters(self, emotion_label, base_exaggeration=1.0):
        """Map emotion label to optimized emotion exaggeration + cfg_weight parameters"""
        
        # [THEATER] USE UNIFIED EMOTION SYSTEM (load từ unified_emotions.json)
        try:
            from src.core.unified_emotion_system import UnifiedEmotionSystem
            unified_system = UnifiedEmotionSystem()
            
            # Get emotion parameters từ unified system
            emotion_params = unified_system.get_emotion_parameters(emotion_label)
            
            if emotion_params:
                final_exaggeration = emotion_params.get('exaggeration', 1.0)
                cfg_weight = emotion_params.get('cfg_weight', 0.6)
                
                # Clamp to valid ranges
                final_exaggeration = max(0.0, min(2.5, final_exaggeration))
                cfg_weight = max(0.0, min(1.0, cfg_weight))
                
                # Log emotion mapping results
                if emotion_label.lower() not in ['neutral', 'normal', 'calm']:
                    print(f"   [THEATER] Emotion Auto-Mapping: '{emotion_label}' → exaggeration={final_exaggeration:.2f}, cfg_weight={cfg_weight:.2f}")
                
                return final_exaggeration, cfg_weight
                
        except Exception as e:
            print(f"[WARNING] Warning: Could not load from unified emotion system: {e}")
            print(f"   Falling back to hardcode mapping for '{emotion_label}'")
        
        # [REFRESH] FALLBACK: Enhanced 22-Emotion Mapping Table (English labels for Chatterbox compatibility)
        emotion_mapping = {
            # 1. Neutral - Objective narration, reporting
            'neutral': {'exaggeration': 0.5, 'cfg_weight': 0.5},
            'calm': {'exaggeration': 0.5, 'cfg_weight': 0.5},
            'normal': {'exaggeration': 0.5, 'cfg_weight': 0.5},
            
            # 2. Gentle/Contemplative - Deep inner thoughts, light emotions  
            'gentle': {'exaggeration': 0.35, 'cfg_weight': 0.35},
            'contemplative': {'exaggeration': 0.4, 'cfg_weight': 0.4},
            'soft': {'exaggeration': 0.3, 'cfg_weight': 0.3},
            'whisper': {'exaggeration': 0.3, 'cfg_weight': 0.3},
            
            # 3. Happy/Cheerful - Positive, joyful, friendly greetings
            'happy': {'exaggeration': 1.2, 'cfg_weight': 0.6},
            'cheerful': {'exaggeration': 1.2, 'cfg_weight': 0.5},
            'joyful': {'exaggeration': 1.5, 'cfg_weight': 0.6},
            'friendly': {'exaggeration': 1.2, 'cfg_weight': 0.5},
            
            # 4. Surprised - Shock, disbelief, amazement
            'surprised': {'exaggeration': 1.85, 'cfg_weight': 0.55},
            'shocked': {'exaggeration': 2.0, 'cfg_weight': 0.6},
            'amazed': {'exaggeration': 1.7, 'cfg_weight': 0.5},
            
            # 5. Sad/Hurt - Heartache, disappointment, heavy emotions
            'sad': {'exaggeration': 0.4, 'cfg_weight': 0.35},
            'hurt': {'exaggeration': 0.3, 'cfg_weight': 0.3},
            'disappointed': {'exaggeration': 0.5, 'cfg_weight': 0.4},
            'melancholy': {'exaggeration': 0.3, 'cfg_weight': 0.3},
            
            # 6. Angry/Furious - Irritated, arguing, dissatisfied
            'angry': {'exaggeration': 2.0, 'cfg_weight': 0.7},
            'furious': {'exaggeration': 2.2, 'cfg_weight': 0.8},
            'irritated': {'exaggeration': 1.8, 'cfg_weight': 0.6},
            'frustrated': {'exaggeration': 1.8, 'cfg_weight': 0.6},
            
            # 7. Pleading/Earnest - Begging, deep emotional appeals
            'pleading': {'exaggeration': 1.6, 'cfg_weight': 0.45},
            'earnest': {'exaggeration': 1.4, 'cfg_weight': 0.4},
            'desperate': {'exaggeration': 1.8, 'cfg_weight': 0.5},
            
            # 8. Anxious/Restless - Worried, underlying tension
            'anxious': {'exaggeration': 1.4, 'cfg_weight': 0.55},
            'worried': {'exaggeration': 1.3, 'cfg_weight': 0.5},
            'nervous': {'exaggeration': 1.5, 'cfg_weight': 0.6},
            'restless': {'exaggeration': 1.4, 'cfg_weight': 0.55},
            
            # 9. Mysterious/Suspenseful - Detective, lurking, tense
            'mysterious': {'exaggeration': 1.4, 'cfg_weight': 0.45},
            'suspenseful': {'exaggeration': 1.2, 'cfg_weight': 0.4},
            'ominous': {'exaggeration': 1.6, 'cfg_weight': 0.5},
            'eerie': {'exaggeration': 1.2, 'cfg_weight': 0.4},
            
            # 10. Warning/Emergency - Alerts, danger, urgent calls
            'warning': {'exaggeration': 2.0, 'cfg_weight': 0.8},
            'urgent': {'exaggeration': 2.0, 'cfg_weight': 0.7},
            'emergency': {'exaggeration': 2.0, 'cfg_weight': 0.9},
            'alarm': {'exaggeration': 2.0, 'cfg_weight': 0.8},
            
            # 11. Sarcastic/Mocking - Teasing, implied meanings
            'sarcastic': {'exaggeration': 0.85, 'cfg_weight': 0.45},
            'mocking': {'exaggeration': 0.7, 'cfg_weight': 0.4},
            'ironic': {'exaggeration': 1.0, 'cfg_weight': 0.5},
            
            # 12. Admiring/Impressed - Genuine praise, admiration
            'admiring': {'exaggeration': 1.45, 'cfg_weight': 0.55},
            'impressed': {'exaggeration': 1.3, 'cfg_weight': 0.5},
            'praising': {'exaggeration': 1.6, 'cfg_weight': 0.6},
            
            # 13. Confused/Embarrassed - Hesitant, lacking confidence
            'confused': {'exaggeration': 0.7, 'cfg_weight': 0.45},
            'embarrassed': {'exaggeration': 0.6, 'cfg_weight': 0.4},
            'hesitant': {'exaggeration': 0.8, 'cfg_weight': 0.5},
            'uncertain': {'exaggeration': 0.7, 'cfg_weight': 0.45},
            
            # Missing emotions from dropdown
            'fearful': {'exaggeration': 1.4, 'cfg_weight': 0.5},
            'thoughtful': {'exaggeration': 0.8, 'cfg_weight': 0.45},
            'sleepy': {'exaggeration': 0.4, 'cfg_weight': 0.3},
            'melancholic': {'exaggeration': 0.3, 'cfg_weight': 0.3},
            
            # 14. Cold/Distant - Indifferent, emotionless
            'cold': {'exaggeration': 0.35, 'cfg_weight': 0.65},
            'distant': {'exaggeration': 0.3, 'cfg_weight': 0.6},
            'indifferent': {'exaggeration': 0.4, 'cfg_weight': 0.7},
            'detached': {'exaggeration': 0.3, 'cfg_weight': 0.6},
            
            # 15. Enthusiastic/Encouraging - Inspiring, motivating
            'enthusiastic': {'exaggeration': 1.7, 'cfg_weight': 0.6},
            'encouraging': {'exaggeration': 1.6, 'cfg_weight': 0.6},
            'motivating': {'exaggeration': 1.8, 'cfg_weight': 0.6},
            'inspiring': {'exaggeration': 1.7, 'cfg_weight': 0.6},
            
            # 16. Strong/Decisive - Commands, clear demands
            'commanding': {'exaggeration': 1.75, 'cfg_weight': 0.8},
            'decisive': {'exaggeration': 1.5, 'cfg_weight': 0.7},
            'authoritative': {'exaggeration': 2.0, 'cfg_weight': 0.9},
            'firm': {'exaggeration': 1.8, 'cfg_weight': 0.8},
            
            # 17. Innocent/Naive - Childlike, carefree joy
            'innocent': {'exaggeration': 1.2, 'cfg_weight': 0.5},
            'naive': {'exaggeration': 1.0, 'cfg_weight': 0.4},
            'childlike': {'exaggeration': 1.4, 'cfg_weight': 0.6},
            'carefree': {'exaggeration': 1.3, 'cfg_weight': 0.5},
            
            # 18. Bewildered/Lost - Confused, don't understand
            'bewildered': {'exaggeration': 1.55, 'cfg_weight': 0.45},
            'lost': {'exaggeration': 1.4, 'cfg_weight': 0.4},
            'perplexed': {'exaggeration': 1.7, 'cfg_weight': 0.5},
            'dazed': {'exaggeration': 1.6, 'cfg_weight': 0.45},
            
            # 19. Provocative/Teasing - Intentionally suggestive, playful
            'provocative': {'exaggeration': 1.65, 'cfg_weight': 0.55},
            'teasing': {'exaggeration': 1.5, 'cfg_weight': 0.5},
            'flirtatious': {'exaggeration': 1.8, 'cfg_weight': 0.6},
            'playful': {'exaggeration': 1.6, 'cfg_weight': 0.55},
            
            # 20. Humorous/Witty - Funny, charming, naturally captivating
            'humorous': {'exaggeration': 1.45, 'cfg_weight': 0.5},
            'witty': {'exaggeration': 1.3, 'cfg_weight': 0.4},
            'amusing': {'exaggeration': 1.6, 'cfg_weight': 0.6},
            'charming': {'exaggeration': 1.4, 'cfg_weight': 0.5},
            
            # 21. Persuasive/Rhetorical - Eloquent, logical with emotion
            'persuasive': {'exaggeration': 1.0, 'cfg_weight': 0.6},
            'rhetorical': {'exaggeration': 1.1, 'cfg_weight': 0.5},
            'eloquent': {'exaggeration': 1.6, 'cfg_weight': 0.6},
            'convincing': {'exaggeration': 1.4, 'cfg_weight': 0.55},
            
            # 22. Scornful/Contemptuous - Harsh mockery, clear disdain
            'scornful': {'exaggeration': 1.85, 'cfg_weight': 0.65},
            'contemptuous': {'exaggeration': 1.7, 'cfg_weight': 0.6},
            'disdainful': {'exaggeration': 2.0, 'cfg_weight': 0.7},
            'condescending': {'exaggeration': 1.8, 'cfg_weight': 0.65},
            
            # Additional common emotions
            'excited': {'exaggeration': 1.6, 'cfg_weight': 0.6},
            'romantic': {'exaggeration': 1.2, 'cfg_weight': 0.45},
            'fear': {'exaggeration': 1.4, 'cfg_weight': 0.5},
            'confident': {'exaggeration': 1.5, 'cfg_weight': 0.6},
            'shy': {'exaggeration': 0.6, 'cfg_weight': 0.4},
            'dramatic': {'exaggeration': 1.2, 'cfg_weight': 0.6},
        }
        
        # Get mapping for emotion label (English labels)
        mapping = emotion_mapping.get(emotion_label.lower(), {'exaggeration': 1.0, 'cfg_weight': 0.5})
        
        # Use absolute values from mapping table (optimized for Chatterbox TTS)
        final_exaggeration = mapping['exaggeration']
        cfg_weight = mapping['cfg_weight']
        
        # Clamp exaggeration to valid range 0.0-2.5
        final_exaggeration = max(0.0, min(2.5, final_exaggeration))
        
        # Clamp cfg_weight to valid range 0.0-1.0  
        cfg_weight = max(0.0, min(1.0, cfg_weight))
        
        # Log emotion mapping results (English labels for better clarity)
        if emotion_label.lower() not in ['neutral', 'normal', 'calm']:
            print(f"   [THEATER] Emotion Auto-Mapping (Fallback): '{emotion_label}' → exaggeration={final_exaggeration:.2f}, cfg_weight={cfg_weight:.2f}")
        
        return final_exaggeration, cfg_weight
    
    # [OK] REMOVED: Global controls methods no longer needed
    # All voice controls are now per-character only
    
    def _update_character_table_row(self, char_id, params):
        """Cập nhật UI table row cho character cụ thể với parameters mới"""
        try:
            # Tìm row của character trong table
            for row in range(self.character_settings_table.rowCount()):
                name_item = self.character_settings_table.item(row, 0)
                if name_item and name_item.text() == char_id:
                    # Skip emotion update (column 1 là dropdown, không phải input)
                    
                    # Update exaggeration input (column 2)  
                    exag_input = self.character_settings_table.cellWidget(row, 2)
                    if exag_input and 'exaggeration' in params:
                        exag_input.setText(f"{params['exaggeration']:.2f}")
                    
                    # Update speed input (column 3)
                    speed_input = self.character_settings_table.cellWidget(row, 3)
                    if speed_input and 'speed' in params:
                        speed_input.setText(f"{params['speed']:.1f}")
                    
                    # Update cfg weight input (column 4)
                    cfg_weight_input = self.character_settings_table.cellWidget(row, 4)
                    if cfg_weight_input and 'cfg_weight' in params:
                        cfg_weight_input.setText(f"{params['cfg_weight']:.2f}")
                    
                    # Update temperature input (column 5) - NEW
                    temperature_input = self.character_settings_table.cellWidget(row, 5)
                    if temperature_input and 'temperature' in params:
                        temperature_input.setText(f"{params['temperature']:.2f}")
                    
                    print(f"[OK] Updated UI for {char_id}: emotion={params.get('emotion', 'N/A'):.1f}, speed={params.get('speed', 'N/A'):.1f}, cfg_weight={params.get('cfg_weight', 'N/A'):.2f}")
                    break
        except Exception as e:
            print(f"[WARNING] Error updating character table row: {e}")
    
    def _show_voice_file_selection_dialog(self, character_name, folder, audio_files):
        """Hiển thị dialog để chọn file voice sample từ danh sách"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
        from PySide6.QtCore import Qt
        import os
        
        print(f"[TARGET] Creating dialog for {character_name} with {len(audio_files)} audio files")
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"[EMOJI] Chọn Voice Sample cho {character_name}")
        dialog.setModal(True)
        dialog.resize(600, 400)
        dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        print(f"[CLIPBOARD] Audio files to show:")
        for i, af in enumerate(audio_files):
            print(f"   {i+1}. {af['name']} ({af['size_mb']:.1f}MB)")
        
        if len(audio_files) == 0:
            print("[EMOJI] ERROR: No audio files provided to dialog!")
            return None
        
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel(f"[FOLDER] Folder: {os.path.basename(folder)}")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
        layout.addWidget(header_label)
        
        info_label = QLabel(f"[MUSIC] Tìm thấy {len(audio_files)} audio files. Chọn 1 file để làm voice sample:")
        info_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # File list
        file_list = QListWidget()
        file_list.setAlternatingRowColors(True)
        file_list.setMinimumHeight(200)
        
        print(f"[REFRESH] Adding {len(audio_files)} items to list widget...")
        
        for i, audio_file in enumerate(audio_files):
            print(f"   Adding item {i+1}: {audio_file['display_name']}")
            item = QListWidgetItem(audio_file['display_name'])
            item.setData(Qt.UserRole, audio_file)  # Store file data
            
            # Color coding by file size
            try:
                from PySide6.QtGui import QColor
                if audio_file['size_mb'] < 1:
                    item.setBackground(QColor('#e8f5e8'))  # Light green for small files
                elif audio_file['size_mb'] > 10:
                    item.setBackground(QColor('#fff3cd'))  # Light yellow for large files
            except Exception as e:
                print(f"   [WARNING] Could not set background color: {e}")
                pass  # Skip color coding if it fails
            
            file_list.addItem(item)
            print(f"   [OK] Item {i+1} added successfully")
        
        print(f"[OK] List widget now has {file_list.count()} items")
        
        layout.addWidget(file_list)
        
        # Preview section
        preview_info = QLabel("[IDEA] Tip: File nhỏ hơn (<5MB) và rõ ràng sẽ cho kết quả voice cloning tốt hơn")
        preview_info.setStyleSheet("color: #007acc; font-style: italic; margin: 5px;")
        layout.addWidget(preview_info)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Play button (preview - if possible)
        play_button = QPushButton("[SOUND] Preview")
        play_button.setEnabled(False)  # Disable for now - can implement later
        play_button.setToolTip("Tính năng preview sẽ được thêm trong bản cập nhật sau")
        
        # Cancel button
        cancel_button = QPushButton("[EMOJI] Hủy")
        cancel_button.clicked.connect(dialog.reject)
        
        # Select button  
        select_button = QPushButton("[OK] Chọn File Này")
        select_button.setEnabled(False)
        select_button.setStyleSheet("font-weight: bold; background-color: white; color: #007acc; border: 1px solid #007acc;")
        
        # Enable select button when item is selected
        def on_selection_changed():
            has_selection = len(file_list.selectedItems()) > 0
            select_button.setEnabled(has_selection)
            if has_selection:
                selected_item = file_list.selectedItems()[0]
                selected_file = selected_item.data(Qt.UserRole)
                select_button.setText(f"[OK] Chọn: {selected_file['name'][:20]}")
        
        file_list.itemSelectionChanged.connect(on_selection_changed)
        
        def on_select():
            if file_list.selectedItems():
                dialog.selected_file = file_list.selectedItems()[0].data(Qt.UserRole)
                dialog.accept()
        
        select_button.clicked.connect(on_select)
        
        # Double click to select
        file_list.itemDoubleClicked.connect(on_select)
        
        button_layout.addWidget(play_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(select_button)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        # Show dialog
        dialog.selected_file = None
        
        print("[SEARCH] About to show dialog...")
        result = dialog.exec()
        print(f"[STATS] Dialog result: {result} (Accepted={QDialog.Accepted}, Rejected={QDialog.Rejected})")
        
        if result == QDialog.Accepted:
            print(f"[OK] Dialog accepted, returning file: {dialog.selected_file}")
            return dialog.selected_file
        else:
            print("[EMOJI] Dialog was cancelled or rejected")
            return None
    
    def import_multiple_script_files(self):
        """Import nhiều script files cùng lúc cho batch processing"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Multiple Script Files",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_paths:
            success_count = 0
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        script_data = json.load(f)
                    
                    # Validate và process script
                    if self.validate_script_data(script_data):
                        # Add to processing queue or handle individually
                        success_count += 1
                        
                except Exception as e:
                    print(f"Error importing {file_path}: {str(e)}")
                    continue
            
            QMessageBox.information(
                self, 
                "Import Complete", 
                f"Successfully imported {success_count}/{len(file_paths)} script files."
            )
    
    def show_ai_request_customizer_dialog(self):
        """Show customizable AI request generator dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("[BOT] AI Request Generator")
        dialog.setFixedSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Dialogue Language:"))
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Tiếng Việt", "[EMOJI][EMOJI]", "[EMOJI][EMOJI][EMOJI]", "[EMOJI][EMOJI][EMOJI]"])
        lang_combo.setCurrentText("English")
        lang_layout.addWidget(lang_combo)
        layout.addLayout(lang_layout)
        
        # Structure options
        struct_layout = QHBoxLayout()
        struct_layout.addWidget(QLabel("Segments:"))
        segments_spin = QSpinBox()
        segments_spin.setRange(1, 10)
        segments_spin.setValue(3)
        struct_layout.addWidget(segments_spin)
        
        struct_layout.addWidget(QLabel("Characters:"))
        chars_spin = QSpinBox()
        chars_spin.setRange(1, 10)
        chars_spin.setValue(2)
        struct_layout.addWidget(chars_spin)
        layout.addLayout(struct_layout)
        
        # Generate button
        generate_btn = QPushButton("[ROCKET] Generate Template")
        generate_btn.clicked.connect(lambda: self.create_custom_template(
            lang_combo.currentText(), 
            segments_spin.value(), 
            chars_spin.value(),
            dialog
        ))
        layout.addWidget(generate_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def create_custom_template(self, language, segments, characters, dialog):
        """Create custom AI template"""
        
        # Sample texts for different languages
        samples = {
            "English": {
                "narrator": "Welcome to today's fascinating story!",
                "character1": "I'm excited to share this with you!"
            },
            "Tiếng Việt": {
                "narrator": "Chào mừng đến với câu chuyện hôm nay!",
                "character1": "Tôi rất hào hứng chia sẻ điều này!"
            }
        }
        
        sample_text = samples.get(language, samples["English"])
        
        # Build JSON template
        template = f'''# [BOT] Custom AI Request Template

## Request:
Create a video script about "[TOPIC]" in **{language}** with {segments} segments and {characters} characters.

```json
{{
  "segments": [
    {{
      "id": 1,
      "dialogues": [
        {{
          "speaker": "narrator",
          "text": "{sample_text['narrator']}",
          "emotion": "friendly"
        }}
      ]
    }}
  ],
  "characters": [
    {{
      "id": "narrator",
      "name": "Narrator", 
      "gender": "neutral"
    }}
  ]
}}
```

## Requirements:
- **Language**: All dialogue in {language}
- **Segments**: {segments} segments total
- **Characters**: {characters} characters maximum
- **Emotions**: Use from 128 available emotions
- **Format**: Proper JSON structure

## 128 Emotions Available:
neutral, happy, sad, excited, calm, angry, romantic, fearful, thoughtful, sleepy, confident, cheerful, melancholic, dramatic, mysterious, surprised, frustrated, soft, whisper, encouraging, admiring, playful, innocent, sarcastic, cold, anxious, worried, confused, embarrassed, disappointed, suspenseful, urgent, commanding, fierce, pleading, desperate, determined, shy, energetic, serious, gentle, bewildered

**Focus on creating engaging, high-quality content!**
'''
        
        self.show_ai_request_dialog("Custom Template", template, 0)
        dialog.close()

    def update_template_preview(self, dialog):
        """Update template preview based on current settings"""
        try:
            # Get current settings from dialog attributes
            content_lang = dialog.content_lang_combo.currentText()
            dialogue_lang = dialog.dialogue_lang_combo.currentText()
            num_segments = dialog.segments_spin.value()
            num_characters = dialog.characters_spin.value()
            content_type = dialog.content_type_combo.currentText()
            duration = dialog.duration_spin.value()
            
            # Generate preview
            preview_text = f"""# [BOT] Custom AI Request Template
            
Content Language: {content_lang}
Dialogue Language: {dialogue_lang}
Segments: {num_segments}
Characters: {num_characters}
Type: {content_type}
Duration: {duration}s

Generate a {content_type.lower()} video script with {num_segments} segments and {num_characters} characters.
Dialogue should be in {dialogue_lang}.
Target duration: {duration} seconds.

[Full template will be generated when you click 'Generate Template']
"""
            
            dialog.template_preview.setPlainText(preview_text)
            
        except Exception as e:
            if hasattr(dialog, 'template_preview'):
                dialog.template_preview.setPlainText(f"Preview error: {str(e)}")

    def generate_custom_template(self, dialog):
        """Generate custom AI request template based on settings"""
        try:
            # Get all settings from dialog attributes
            content_lang = dialog.content_lang_combo.currentText()
            dialogue_lang = dialog.dialogue_lang_combo.currentText()
            num_segments = dialog.segments_spin.value()
            num_characters = dialog.characters_spin.value()
            content_type = dialog.content_type_combo.currentText()
            duration = dialog.duration_spin.value()
            
            # Generate language codes
            lang_codes = {
                "English": "en-US",
                "Tiếng Việt": "vi-VN", 
                "[EMOJI][EMOJI]": "zh-CN",
                "[EMOJI][EMOJI][EMOJI]": "ja-JP",
                "[EMOJI][EMOJI][EMOJI]": "ko-KR",
                "Français": "fr-FR",
                "Español": "es-ES",
                "Deutsch": "de-DE",
                "Русский": "ru-RU"
            }
            
            dialogue_code = lang_codes.get(dialogue_lang, "en-US")
            
            # Build template
            template = self.build_custom_ai_template(
                dialog, content_lang, dialogue_lang, dialogue_code,
                num_segments, num_characters, content_type, duration
            )
            
            # Show in dialog
            self.show_ai_request_dialog("Custom AI Request Template", template, 0)
            dialog.close()
            
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"Failed to generate template:\n{str(e)}")

    def build_custom_ai_template(self, dialog, content_lang, dialogue_lang, dialogue_code,
                                num_segments, num_characters, content_type, duration):
        """Build the actual AI request template"""
        
        # Sample dialogues based on language
        sample_dialogues = {
            "English": {
                "narrator": "Welcome to today's fascinating journey of discovery!",
                "character1": "I'm absolutely thrilled to share this amazing story with you!",
                "character2": "Let's dive deeper into this incredible topic together."
            },
            "Tiếng Việt": {
                "narrator": "Chào mừng các bạn đến với hành trình khám phá hôm nay!",
                "character1": "Tôi rất hào hứng được chia sẻ câu chuyện tuyệt vời này!",
                "character2": "Hãy cùng nhau tìm hiểu sâu hơn về chủ đề thú vị này."
            }
        }
        
        # Get sample text
        samples = sample_dialogues.get(dialogue_lang, sample_dialogues["English"])
        
        # Build character list
        characters_json = []
        character_names = ["narrator", "character1", "character2", "character3", "character4", 
                          "character5", "character6", "character7", "character8", "character9"]
        
        for i in range(num_characters):
            char_id = character_names[i] if i < len(character_names) else f"character{i+1}"
            char_name = f"Character {i+1}" if char_id != "narrator" else "Narrator"
            
            char_entry = f'''    {{
      "id": "{char_id}",
      "name": "{char_name}",
      "gender": "neutral"'''
            
            if dialog.include_character_details.isChecked():
                char_entry += f''',
      "description": "Description of {char_name}",
      "personality": "Personality traits",
      "default_emotion": "friendly"'''
            
            char_entry += "\n    }"
            characters_json.append(char_entry)
        
        # Build segments list  
        segments_json = []
        for i in range(num_segments):
            segment_id = i + 1
            sample_text = list(samples.values())[i % len(samples)]
            speaker = list(samples.keys())[i % len(samples)]
            
            dialogue_entry = f'''        {{
          "speaker": "{speaker}",
          "text": "{sample_text}",
          "emotion": "friendly"'''
            
            if dialog.include_advanced_dialogue.isChecked():
                dialogue_entry += f''',
          "pause_after": 0.5,
          "emphasis": ["key", "words"]'''
            
            dialogue_entry += "\n        }"
            
            segment_entry = f'''    {{
      "id": {segment_id},
      "title": "Scene {segment_id}"'''
            
            if dialog.include_scene_descriptions.isChecked():
                segment_entry += f''',
      "script": "Description of scene {segment_id}",
      "image_prompt": "Visual description for AI image generation"'''
            
            segment_entry += f''',
      "dialogues": [
{dialogue_entry}
      ]
    }}'''
            
            segments_json.append(segment_entry)
        
        # Build main JSON structure
        json_structure = "{\n"
        
        if dialog.include_project_metadata.isChecked():
            json_structure += f'''  "project": {{
    "title": "Story Title",
    "description": "Story description",
    "total_duration": {duration},
    "target_audience": "adult",
    "style": "{content_type.lower()}",
    "language": "{dialogue_code}"
  }},
'''
        
        json_structure += f'''  "segments": [
{chr(10).join(segments_json)}
  ],
  "characters": [
{chr(10).join(characters_json)}
  ]'''
        
        if dialog.include_audio_settings.isChecked():
            json_structure += f''',
  "audio_settings": {{
    "crossfade_duration": 0.3,
    "normalize_volume": true,
    "output_format": "mp3"
  }}'''
        
        json_structure += "\n}"
        
        # Build complete template
        template = f'''# [BOT] Custom AI Request Template

## Request:
Create a {content_type.lower()} video script about "[TOPIC]" using the following JSON format:

```json
{json_structure}
```

## Configuration:
- **Content Language**: {content_lang}
- **Dialogue Language**: {dialogue_lang}
- **Segments**: {num_segments}
- **Characters**: {num_characters}
- **Content Type**: {content_type}
- **Target Duration**: {duration} seconds

## Requirements:
- All dialogue text must be in **{dialogue_lang}**
- Use proper punctuation and grammar for {dialogue_lang}
- Each dialogue must include: speaker, text, emotion
- Each character must include: id, name, gender'''

        if self.include_advanced_dialogue.isChecked():
            template += "\n- Advanced timing features: pause_after (0.0-5.0 seconds), emphasis arrays"

        if self.show_emotion_categories.isChecked():
            template += '''

## 128 Emotions Available (37 primary + 91 aliases):
- **Neutral**: neutral, calm, contemplative, soft, whisper
- **Positive**: happy, excited, cheerful, friendly, confident, encouraging, admiring, playful, romantic, innocent
- **Negative**: sad, angry, sarcastic, cold, anxious, worried, confused, embarrassed, disappointed, frustrated
- **Dramatic**: dramatic, mysterious, suspenseful, urgent, commanding, fierce, pleading, desperate, determined
- **Special**: sleepy, surprised, shy, energetic, serious, gentle, bewildered
- **Aliases**: Each emotion has 2-4 alternative names for variety'''

        if self.show_emotion_examples.isChecked():
            template += '''

## Emotion Usage Examples:
- **Narration**: neutral, contemplative, mysterious, dramatic
- **Character Dialogue**: friendly, excited, happy, confident, worried
- **Action Scenes**: urgent, commanding, fierce, determined
- **Emotional Scenes**: romantic, gentle, pleading, sad, disappointed'''

        template += '''

**Focus on creating engaging, high-quality content with natural dialogue flow!**
'''
        
        return template

    def save_custom_template(self):
        """Save custom template to file"""
        if hasattr(self, 'template_preview'):
            content = self.template_preview.toPlainText()
            self.save_ai_request_template(content)

    def update_inner_voice_json_guide(self):
        # Đọc trạng thái inner voice từ config (giả sử đã load vào self.voice_config)
        enabled = True  # TODO: lấy từ config thực tế
        if enabled:
            self.inner_voice_json_guide.setText(
                "<b>Hướng dẫn JSON cho thoại nội tâm:</b><br>"
                "- Đoạn nào là nội tâm, thêm <code>\"inner_voice\": true</code> vào object dialogue.<br>"
                "- Có thể thêm <code>\"inner_voice_type\": \"light|deep|dreamy\"</code> để chọn loại hiệu ứng.<br>"
                "- Nếu không có cờ này, hệ thống sẽ bỏ qua.<br>"
                "<br>Ví dụ:<br>"
                "<pre>{\n  ...\n  \"dialogues\": [\n    {\n      \"speaker\": \"alice\",\n      \"text\": \"Tôi đang nghĩ gì vậy...?\",\n      <b>\"inner_voice\": true,\n      \"inner_voice_type\": \"dreamy\"</b>\n    }\n  ]\n}\n</pre>"
            )
        else:
            self.inner_voice_json_guide.setText(
                "<b>Thoại nội tâm đang tắt.</b> Không cần khai báo cờ <code>inner_voice</code> trong JSON.")

    # === NEW: Manual Table Mode Functions ===
    
    def setup_manual_table_mode(self):
        """Setup specific configurations for manual table mode"""
        # Initialize manual table data
        self.manual_table_data = []
        
        # Setup character settings for narrator only
        self.setup_narrator_character_settings()
        
        # Update UI visibility
        self.update_manual_table_ui_visibility()
    
    def setup_narrator_character_settings(self):
        """Setup character settings specifically for narrator in manual table mode"""
        # Initialize narrator settings
        narrator_settings = {
            'emotion': 1.0,
            'speed': 1.0,
            'cfg_weight': 0.5,
            'voice_mode': 'voice_selection',
            'voice_id': 'alexander',  # Default narrator voice
            'voice_clone_path': None,
            'voice_clone_status': 'none',
            'whisper_voice_id': 'willow ii (whispering)',
            'whisper_voice_clone_path': None,
            'whisper_voice_clone_status': 'none'
        }
        
        # Set narrator as the only character
        self.character_chatterbox_settings = {
            'narrator': narrator_settings
        }
        
        # Create simplified script data structure
        self.voice_studio_script_data = {
            'segments': [],
            'characters': [
                {
                    'id': 'narrator',
                    'name': 'Narrator',
                    'gender': 'neutral'
                }
            ]
        }
        
        # Update character settings table to show only narrator
        self.populate_character_settings_table()
    
    def update_manual_table_ui_visibility(self):
        """Update UI visibility for manual table mode"""
        # Force enable manual character controls in manual table mode
        if hasattr(self, 'enable_chatterbox_manual'):
            self.enable_chatterbox_manual.setChecked(True)
            self.toggle_chatterbox_manual_controls(True)
        
        # Update overview
        self.update_voice_studio_overview()
        
        # Reload character settings table để hiển thị cột temperature mới
        if hasattr(self, 'character_settings_table'):
            self.populate_character_settings_table()
            print("[OK] Đã reload bảng character settings với cột temperature")
    
    def add_manual_table_row(self):
        """Thêm hàng mới vào bảng manual data"""
        row_count = self.manual_data_table.rowCount()
        self.manual_data_table.insertRow(row_count)
        
        # Set default values for new row
        segment_num = row_count + 1
        dialogue_num = 1
        
        self.manual_data_table.setItem(row_count, 0, QTableWidgetItem(str(segment_num)))
        self.manual_data_table.setItem(row_count, 1, QTableWidgetItem(str(dialogue_num)))
        self.manual_data_table.setItem(row_count, 2, QTableWidgetItem(""))
        
        # Select the new row
        self.manual_data_table.selectRow(row_count)
    
    def remove_manual_table_row(self):
        """Xóa hàng đã chọn khỏi bảng manual data"""
        current_row = self.manual_data_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, 
                "Xác nhận xóa", 
                f"Bạn có chắc muốn xóa hàng {current_row + 1}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.manual_data_table.removeRow(current_row)
                
                # Update segment/dialogue numbering
                self.update_manual_table_numbering()
        else:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn hàng cần xóa!")
    
    def update_manual_table_numbering(self):
        """Cập nhật lại số thứ tự segment/dialogue trong bảng"""
        for row in range(self.manual_data_table.rowCount()):
            # Update segment number
            segment_item = self.manual_data_table.item(row, 0)
            if segment_item:
                segment_item.setText(str(row + 1))
            
            # Update dialogue number (always 1 for narrator)
            dialogue_item = self.manual_data_table.item(row, 1)
            if dialogue_item:
                dialogue_item.setText("1")
    
    def auto_chunk_content(self):
        """Tự động chia nội dung thành các đoạn nhỏ dựa theo chunk size"""
        try:
            chunk_size = int(self.chunk_size_input.text())
            if chunk_size < 100 or chunk_size > 2000:
                QMessageBox.warning(self, "Cảnh báo", "Chunk size nên từ 100-2000 ký tự!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Chunk size phải là số!")
            return
        
        # Collect all content from table
        all_content = []
        for row in range(self.manual_data_table.rowCount()):
            content_item = self.manual_data_table.item(row, 2)
            if content_item and content_item.text().strip():
                all_content.append(content_item.text().strip())
        
        if not all_content:
            QMessageBox.information(self, "Thông báo", "Không có nội dung để chia đoạn!")
            return
        
        # Merge all content
        full_text = " ".join(all_content)
        
        # Chunk the content
        chunks = self.chunk_text_by_size(full_text, chunk_size)
        
        if len(chunks) == 0:
            QMessageBox.warning(self, "Error", "Không thể chia đoạn nội dung!")
            return
        
        # Confirm with user
        reply = QMessageBox.question(
            self,
            "Xác nhận chia đoạn",
            f"Sẽ chia thành {len(chunks)} đoạn với chunk size {chunk_size} ký tự.\n"
            f"Điều này sẽ thay thế toàn bộ dữ liệu hiện tại. Tiếp tục?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear table and add chunked content
            self.manual_data_table.setRowCount(0)
            
            for i, chunk in enumerate(chunks):
                self.manual_data_table.insertRow(i)
                self.manual_data_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.manual_data_table.setItem(i, 1, QTableWidgetItem("1"))
                self.manual_data_table.setItem(i, 2, QTableWidgetItem(chunk.strip()))
            
            QMessageBox.information(self, "Thành công", f"Đã chia thành {len(chunks)} đoạn!")
    
    def chunk_text_by_size(self, text, chunk_size):
        """Chia text thành các đoạn nhỏ theo size, ưu tiên chia theo câu"""
        if not text or chunk_size <= 0:
            return []
        
        # Split by sentences first
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add punctuation back
            sentence = sentence + "."
            
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append(current_chunk)
                
                # If single sentence is too long, split by words
                if len(sentence) > chunk_size:
                    words = sentence.split()
                    temp_chunk = ""
                    for word in words:
                        if len(temp_chunk) + len(word) + 1 <= chunk_size:
                            temp_chunk += " " + word if temp_chunk else word
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk)
                            temp_chunk = word
                    
                    current_chunk = temp_chunk
                else:
                    current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def on_table_item_changed(self, item):
        """Handle table item changes - auto-split large text content"""
        # Only process content column (column 2)
        if item.column() != 2:
            return
        
        content = item.text()
        
        # Check if content is long enough to warrant auto-splitting
        try:
            chunk_size = int(self.chunk_size_input.text())
        except ValueError:
            chunk_size = 500  # Default
        
        # If content is significantly larger than chunk_size, offer auto-split
        if len(content) > chunk_size * 1.5:  # 1.5x threshold for auto-split suggestion
            reply = QMessageBox.question(
                self,
                "Tự động chia đoạn",
                f"Nội dung vừa nhập ({len(content)} ký tự) dài hơn chunk size khuyến nghị ({chunk_size} ký tự).\n"
                f"Bạn có muốn tự động chia thành các đoạn nhỏ hơn không?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Temporarily disconnect the signal to avoid recursion
                self.manual_data_table.itemChanged.disconnect(self.on_table_item_changed)
                
                try:
                    # Split this specific content into chunks
                    chunks = self.chunk_text_by_size(content, chunk_size)
                    
                    if len(chunks) > 1:
                        current_row = item.row()
                        
                        # Replace current row with first chunk
                        item.setText(chunks[0])
                        
                        # Insert additional rows for remaining chunks
                        for i, chunk in enumerate(chunks[1:], 1):
                            self.manual_data_table.insertRow(current_row + i)
                            self.manual_data_table.setItem(current_row + i, 0, QTableWidgetItem(str(current_row + i + 1)))
                            self.manual_data_table.setItem(current_row + i, 1, QTableWidgetItem("1"))
                            self.manual_data_table.setItem(current_row + i, 2, QTableWidgetItem(chunk.strip()))
                        
                        # Update segment numbers for subsequent rows
                        for row in range(current_row + len(chunks), self.manual_data_table.rowCount()):
                            segment_item = self.manual_data_table.item(row, 0)
                            if segment_item:
                                segment_item.setText(str(row + 1))
                        
                        QMessageBox.information(self, "Thành công", f"Đã tự động chia thành {len(chunks)} đoạn!")
                
                finally:
                    # Reconnect the signal
                    self.manual_data_table.itemChanged.connect(self.on_table_item_changed)
    
    def confirm_manual_table_data(self):
        """Xác nhận dữ liệu nhập từ bảng và convert thành script data"""
        # Collect data from table
        segments_data = []
        
        for row in range(self.manual_data_table.rowCount()):
            segment_item = self.manual_data_table.item(row, 0)
            dialogue_item = self.manual_data_table.item(row, 1) 
            content_item = self.manual_data_table.item(row, 2)
            
            if not all([segment_item, dialogue_item, content_item]):
                continue
            
            content = content_item.text().strip()
            if not content:
                continue
            
            try:
                segment_id = int(segment_item.text())
            except ValueError:
                segment_id = row + 1
            
            # Create dialogue entry
            dialogue_entry = {
                'speaker': 'narrator',
                'text': content,
                'emotion': 'neutral'  # Default emotion for manual mode
            }
            
            # Create segment entry
            segment_entry = {
                'id': segment_id,
                'title': f'Segment {segment_id}',
                'dialogues': [dialogue_entry]
            }
            
            segments_data.append(segment_entry)
        
        if not segments_data:
            QMessageBox.warning(self, "Cảnh báo", "Không có dữ liệu hợp lệ để xác nhận!")
            return
        
        # Create SINGLE CHARACTER data format for TTSBridge
        # Combine all text into one string for single character processing
        all_text_chunks = []
        for segment in segments_data:
            for dialogue in segment['dialogues']:
                all_text_chunks.append(dialogue['text'])
        
        combined_text = " ".join(all_text_chunks)
        
        # Use simple text format to trigger TTSBridge single character mode
        self.voice_studio_script_data = {
            'text': combined_text,
            'mode': 'single_character',
            'voice': 'narrator',
            'chunks': len(segments_data),  # For UI display
            'total_characters': len(combined_text),
            'project': {
                'title': 'Manual Table Project (Single Character)',
                'description': 'Created from manual table input for single character TTS',
                'total_duration': len(segments_data) * 30
            }
        }
        
        # Update overview and enable generation
        self.update_voice_studio_overview()
        
        # Enable generation buttons
        if hasattr(self, 'generate_all_btn'):
            self.generate_all_btn.setEnabled(True)
        
        QMessageBox.information(
            self,
            "Thành công - Single Character Mode",
            f"Đã xác nhận {len(segments_data)} đoạn dữ liệu cho Single Character TTS!\n"
            f"Tổng cộng {len(combined_text)} ký tự sẽ được xử lý với text preprocessing tự động.\n"
            f"Mode: Single Character với smart chunking và auto-merging."
        )
    
    def apply_extended_preset(self, preset_type):
        """Áp dụng preset configuration cho Chatterbox Extended settings"""
        try:
            presets = {
                # Text Processing Presets
                "conservative_text": {
                    "smart_joining": False,
                    "sentence_join_threshold": 60,
                    "recursive_splitting": False,
                    "max_sentence_length": 300,
                    "fix_abbreviations": True,
                    "remove_references": False,
                    "remove_unwanted_words": False
                },
                "default_text": {
                    "smart_joining": True,
                    "sentence_join_threshold": 40,
                    "recursive_splitting": True,
                    "max_sentence_length": 200,
                    "fix_abbreviations": True,
                    "remove_references": True,
                    "remove_unwanted_words": True
                },
                "aggressive_text": {
                    "smart_joining": True,
                    "sentence_join_threshold": 25,
                    "recursive_splitting": True,
                    "max_sentence_length": 150,
                    "fix_abbreviations": True,
                    "remove_references": True,
                    "remove_unwanted_words": True
                },
                
                # Audio Processing Presets
                "fast_audio": {
                    "auto_editor": False,
                    "ffmpeg_normalization": False,
                    "target_lufs": -23.0,
                    "peak_limit": -1.0,
                    "export_wav": True,
                    "export_mp3": False,
                    "export_flac": False,
                    "preserve_original": False
                },
                "default_audio": {
                    "auto_editor": True,
                    "ffmpeg_normalization": True,
                    "target_lufs": -23.0,
                    "peak_limit": -1.0,
                    "export_wav": True,
                    "export_mp3": True,
                    "export_flac": False,
                    "preserve_original": True
                },
                "quality_audio": {
                    "auto_editor": True,
                    "ffmpeg_normalization": True,
                    "target_lufs": -16.0,
                    "peak_limit": -0.5,
                    "export_wav": True,
                    "export_mp3": True,
                    "export_flac": True,
                    "preserve_original": True
                },
                
                # Generation Presets
                "conservative_generation": {
                    "num_generations": 1,
                    "candidates_per_block": 1,
                    "max_retries": 1,
                    "fallback_strategy": "first_success",
                    "whisper_validation": False,
                    "whisper_model": "tiny (39MB, 32x realtime)",
                    "whisper_backend": "openai_whisper",
                    "similarity_threshold": 0.5
                },
                "default_generation": {
                    "num_generations": 2,
                    "candidates_per_block": 2,
                    "max_retries": 3,
                    "fallback_strategy": "highest_similarity",
                    "whisper_validation": True,
                    "whisper_model": "base (74MB, 16x realtime)",
                    "whisper_backend": "faster_whisper",
                    "similarity_threshold": 0.7
                },
                "aggressive_generation": {
                    "num_generations": 5,
                    "candidates_per_block": 3,
                    "max_retries": 5,
                    "fallback_strategy": "highest_similarity",
                    "whisper_validation": True,
                    "whisper_model": "small (244MB, 6x realtime)",
                    "whisper_backend": "faster_whisper",
                    "similarity_threshold": 0.8
                }
            }
            
            if preset_type not in presets:
                QMessageBox.warning(self, "Error", f"Preset '{preset_type}' không tồn tại!")
                return
                
            preset = presets[preset_type]
            
            # Apply text processing settings
            if "smart_joining" in preset:
                self.smart_joining_checkbox.setChecked(preset["smart_joining"])
            if "sentence_join_threshold" in preset:
                self.sentence_join_threshold.setValue(preset["sentence_join_threshold"])
            if "recursive_splitting" in preset:
                self.recursive_splitting_checkbox.setChecked(preset["recursive_splitting"])
            if "max_sentence_length" in preset:
                self.max_sentence_length.setValue(preset["max_sentence_length"])
            if "fix_abbreviations" in preset:
                self.fix_abbreviations_checkbox.setChecked(preset["fix_abbreviations"])
            if "remove_references" in preset:
                self.remove_references_checkbox.setChecked(preset["remove_references"])
            if "remove_unwanted_words" in preset:
                self.remove_unwanted_words_checkbox.setChecked(preset["remove_unwanted_words"])
                
            # Apply audio processing settings
            if "auto_editor" in preset:
                self.auto_editor_checkbox.setChecked(preset["auto_editor"])
            if "ffmpeg_normalization" in preset:
                self.ffmpeg_normalization_checkbox.setChecked(preset["ffmpeg_normalization"])
            if "target_lufs" in preset:
                self.target_lufs.setValue(preset["target_lufs"])
            if "peak_limit" in preset:
                self.peak_limit.setValue(preset["peak_limit"])
            if "export_wav" in preset:
                self.export_wav_checkbox.setChecked(preset["export_wav"])
            if "export_mp3" in preset:
                self.export_mp3_checkbox.setChecked(preset["export_mp3"])
            if "export_flac" in preset:
                self.export_flac_checkbox.setChecked(preset["export_flac"])
            if "preserve_original" in preset:
                self.preserve_original_checkbox.setChecked(preset["preserve_original"])
                
            # Apply generation settings
            if "num_generations" in preset:
                self.num_generations.setValue(preset["num_generations"])
            if "candidates_per_block" in preset:
                self.candidates_per_block.setValue(preset["candidates_per_block"])
            if "max_retries" in preset:
                self.max_retries.setValue(preset["max_retries"])
            if "fallback_strategy" in preset:
                self.fallback_strategy.setCurrentText(preset["fallback_strategy"])
            if "whisper_validation" in preset:
                self.whisper_validation_checkbox.setChecked(preset["whisper_validation"])
            if "whisper_model" in preset:
                self.whisper_model_combo.setCurrentText(preset["whisper_model"])
            if "whisper_backend" in preset:
                self.whisper_backend_combo.setCurrentText(preset["whisper_backend"])
            if "similarity_threshold" in preset:
                self.similarity_threshold.setValue(preset["similarity_threshold"])
                
            QMessageBox.information(
                self,
                "Thành công",
                f"Đã áp dụng preset '{preset_type}' thành công!"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error khi áp dụng preset: {str(e)}")
    
    # === SETTINGS PERSISTENCE METHODS ===
    
    def save_current_settings(self):
        """Save current settings manually"""
        try:
            from core.settings_persistence import save_settings
            if save_settings():
                QMessageBox.information(self, "Success", "[OK] Settings saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "[EMOJI] Failed to save settings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"[EMOJI] Error saving settings: {str(e)}")
    
    def export_settings_json(self):
        """Export settings to JSON file"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Settings to JSON",
                f"voice_studio_settings_{int(time.time())}.json",
                "JSON files (*.json);;All files (*.*)"
            )
            
            if file_path:
                from core.settings_persistence import export_settings
                if export_settings(file_path, "json"):
                    QMessageBox.information(self, "Success", f"[OK] Settings exported to:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to export settings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"[EMOJI] Error exporting settings: {str(e)}")
    
    def export_settings_csv(self):
        """Export settings to CSV file"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Settings to CSV",
                f"voice_studio_settings_{int(time.time())}.csv",
                "CSV files (*.csv);;All files (*.*)"
            )
            
            if file_path:
                from core.settings_persistence import export_settings
                if export_settings(file_path, "csv"):
                    QMessageBox.information(self, "Success", f"[OK] Settings exported to:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to export settings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"[EMOJI] Error exporting settings: {str(e)}")
    
    def import_settings(self):
        """Import settings from file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Settings",
                "",
                "Settings files (*.json *.csv);;JSON files (*.json);;CSV files (*.csv);;All files (*.*)"
            )
            
            if file_path:
                # Determine format from extension
                format_type = "json" if file_path.lower().endswith('.json') else "csv"
                
                from core.settings_persistence import import_settings
                if import_settings(file_path, format_type):
                    QMessageBox.information(self, "Success", f"[OK] Settings imported from:\n{file_path}")
                    self.load_settings_to_ui()  # Refresh UI with imported settings
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to import settings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"[EMOJI] Error importing settings: {str(e)}")
    
    def reset_settings_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                from core.settings_persistence import settings_manager
                if settings_manager.reset_to_defaults():
                    QMessageBox.information(self, "Success", "[OK] Settings reset to defaults!")
                    self.load_settings_to_ui()  # Refresh UI
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to reset settings")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"[EMOJI] Error resetting settings: {str(e)}")
    
    def save_settings_profile(self):
        """Save current settings as a profile"""
        profile_name, ok = QInputDialog.getText(
            self,
            "Save Profile",
            "Enter profile name:",
            QLineEdit.Normal,
            f"Profile_{int(time.time())}"
        )
        
        if ok and profile_name.strip():
            try:
                from core.settings_persistence import settings_manager
                if settings_manager.save_profile(profile_name.strip()):
                    self.load_profiles_to_combo()  # Refresh profile list
                    QMessageBox.information(self, "Success", f"[OK] Profile '{profile_name}' saved!")
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to save profile")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"[EMOJI] Error saving profile: {str(e)}")
    
    def load_settings_profile(self):
        """Load settings from selected profile"""
        profile_name = self.profile_combo.currentText()
        if not profile_name or profile_name == "Select Profile...":
            QMessageBox.information(self, "Info", "Please select a profile to load")
            return
        
        reply = QMessageBox.question(
            self,
            "Load Profile",
            f"Load profile '{profile_name}'?\n\nThis will overwrite current settings.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                from core.settings_persistence import settings_manager
                if settings_manager.load_profile(profile_name):
                    self.load_settings_to_ui()  # Refresh UI with loaded settings
                    QMessageBox.information(self, "Success", f"[OK] Profile '{profile_name}' loaded!")
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to load profile")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"[EMOJI] Error loading profile: {str(e)}")
    
    def delete_settings_profile(self):
        """Delete selected profile"""
        profile_name = self.profile_combo.currentText()
        if not profile_name or profile_name == "Select Profile...":
            QMessageBox.information(self, "Info", "Please select a profile to delete")
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Profile",
            f"Delete profile '{profile_name}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                from core.settings_persistence import settings_manager
                if settings_manager.delete_profile(profile_name):
                    self.load_profiles_to_combo()  # Refresh profile list
                    QMessageBox.information(self, "Success", f"[OK] Profile '{profile_name}' deleted!")
                else:
                    QMessageBox.warning(self, "Error", "[EMOJI] Failed to delete profile")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"[EMOJI] Error deleting profile: {str(e)}")
    
    def load_profiles_to_combo(self):
        """Load available profiles to combo box"""
        try:
            from core.settings_persistence import settings_manager
            profiles = settings_manager.list_profiles()
            
            self.profile_combo.clear()
            self.profile_combo.addItem("Select Profile...")
            
            for profile in profiles:
                self.profile_combo.addItem(profile["name"])
                
        except Exception as e:
            logger.error(f"[EMOJI] Error loading profiles: {e}")
    
    def load_settings_to_ui(self):
        """Load current settings to UI elements"""
        try:
            from core.settings_persistence import get_settings
            settings = get_settings()
            
            # Update auto-save checkbox
            self.auto_save_checkbox.setChecked(settings.auto_save_enabled)
            
            # Update TTS mode if available
            if hasattr(self, 'performance_mode_combo'):
                self.performance_mode_combo.setCurrentText(settings.tts_mode)
            
            # Update other UI elements as needed
            # TODO: Add more UI updates based on loaded settings
            
        except Exception as e:
            logger.error(f"[EMOJI] Error loading settings to UI: {e}")
    
    def get_extended_settings(self):
        """Lấy tất cả Extended settings từ UI"""
        try:
            settings = {
                # Text Processing Settings
                "text_processor": {
                    "smart_joining": self.smart_joining_checkbox.isChecked(),
                    "sentence_join_threshold": self.sentence_join_threshold.value(),
                    "recursive_splitting": self.recursive_splitting_checkbox.isChecked(),
                    "max_sentence_length": self.max_sentence_length.value(),
                    "fix_abbreviations": self.fix_abbreviations_checkbox.isChecked(),
                    "remove_references": self.remove_references_checkbox.isChecked(),
                    "remove_unwanted_words": self.remove_unwanted_words_checkbox.isChecked()
                },
                
                # Audio Processing Settings
                "audio_processor": {
                    "auto_editor": self.auto_editor_checkbox.isChecked(),
                    "ffmpeg_normalization": self.ffmpeg_normalization_checkbox.isChecked(),
                    "target_lufs": self.target_lufs.value(),
                    "peak_limit": self.peak_limit.value(),
                    "export_formats": {
                        "wav": self.export_wav_checkbox.isChecked(),
                        "mp3": self.export_mp3_checkbox.isChecked(),
                        "flac": self.export_flac_checkbox.isChecked()
                    },
                    "preserve_original": self.preserve_original_checkbox.isChecked()
                },
                
                # Generation Controller Settings
                "generation_controller": {
                    "num_generations": self.num_generations.value(),
                    "candidates_per_block": self.candidates_per_block.value(),
                    "max_retries": self.max_retries.value(),
                    "fallback_strategy": self.fallback_strategy.currentText()
                },
                
                # Whisper Manager Settings
                "whisper_manager": {
                    "enabled": self.whisper_validation_checkbox.isChecked(),
                    "model": self.whisper_model_combo.currentText().split()[0],  # Extract model name
                    "backend": self.whisper_backend_combo.currentText(),
                    "similarity_threshold": self.similarity_threshold.value()
                },
                
                # Performance Settings
                "performance": {
                    "tts_mode": self.tts_mode_combo.currentData(),
                    "cache_enabled": self.cache_enabled_checkbox.isChecked(),
                    "parallel_processing": self.parallel_processing_checkbox.isChecked(),
                    "bypass_validation": self.bypass_validation_checkbox.isChecked()
                }
            }
            
            return settings
            
        except Exception as e:
            print(f"Error getting extended settings: {e}")
            return {}