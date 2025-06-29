from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QScrollArea, QLineEdit, QCheckBox, QSpinBox,
    QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
import json
import os

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)
        
        # Main content widget
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        
        # API Settings group
        api_group = QGroupBox("Cài đặt API")
        api_layout = QVBoxLayout()
        
        # OpenAI API Key
        openai_layout = QHBoxLayout()
        openai_layout.addWidget(QLabel("OpenAI API Key:"))
        self.openai_key = QLineEdit()
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        openai_layout.addWidget(self.openai_key)
        api_layout.addLayout(openai_layout)
        
        # Google Cloud API Key
        google_layout = QHBoxLayout()
        google_layout.addWidget(QLabel("Google Cloud API Key:"))
        self.google_key = QLineEdit()
        self.google_key.setEchoMode(QLineEdit.EchoMode.Password)
        google_layout.addWidget(self.google_key)
        api_layout.addLayout(google_layout)
        
        api_group.setLayout(api_layout)
        content_layout.addWidget(api_group)
        
        # Project Settings group
        project_group = QGroupBox("Cài đặt Dự án")
        project_layout = QVBoxLayout()
        
        # Projects directory
        projects_layout = QHBoxLayout()
        projects_layout.addWidget(QLabel("Thư mục dự án:"))
        self.projects_dir = QLineEdit()
        projects_layout.addWidget(self.projects_dir)
        browse_btn = QPushButton("Chọn thư mục")
        browse_btn.clicked.connect(self.browse_projects_dir)
        projects_layout.addWidget(browse_btn)
        project_layout.addLayout(projects_layout)
        
        # Auto-save
        self.auto_save = QCheckBox("Tự động lưu dự án")
        self.auto_save.setChecked(True)
        project_layout.addWidget(self.auto_save)
        
        # Auto-save interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Thời gian tự động lưu (phút):"))
        self.save_interval = QSpinBox()
        self.save_interval.setRange(1, 60)
        self.save_interval.setValue(5)
        interval_layout.addWidget(self.save_interval)
        project_layout.addLayout(interval_layout)
        
        project_group.setLayout(project_layout)
        content_layout.addWidget(project_group)
        
        # Video Settings group
        video_group = QGroupBox("Cài đặt Video")
        video_layout = QVBoxLayout()
        
        # Default resolution
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(QLabel("Độ phân giải mặc định:"))
        self.resolution_width = QSpinBox()
        self.resolution_width.setRange(480, 3840)
        self.resolution_width.setValue(1920)
        resolution_layout.addWidget(self.resolution_width)
        resolution_layout.addWidget(QLabel("x"))
        self.resolution_height = QSpinBox()
        self.resolution_height.setRange(360, 2160)
        self.resolution_height.setValue(1080)
        resolution_layout.addWidget(self.resolution_height)
        video_layout.addLayout(resolution_layout)
        
        # Default FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS mặc định:"))
        self.default_fps = QSpinBox()
        self.default_fps.setRange(24, 60)
        self.default_fps.setValue(30)
        fps_layout.addWidget(self.default_fps)
        video_layout.addLayout(fps_layout)
        
        video_group.setLayout(video_layout)
        content_layout.addWidget(video_group)
        
        # Save/Reset buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Lưu cài đặt")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Khôi phục mặc định")
        reset_btn.clicked.connect(self.reset_settings)
        buttons_layout.addWidget(reset_btn)
        
        content_layout.addLayout(buttons_layout)
        
        # Add stretch to push everything up
        content_layout.addStretch()
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'settings.json')
            if not os.path.exists(config_path):
                return
                
            with open(config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # API settings
            self.openai_key.setText(settings.get('openai_api_key', ''))
            self.google_key.setText(settings.get('google_api_key', ''))
            
            # Project settings
            self.projects_dir.setText(settings.get('projects_directory', ''))
            self.auto_save.setChecked(settings.get('auto_save', True))
            self.save_interval.setValue(settings.get('auto_save_interval', 5))
            
            # Video settings
            resolution = settings.get('default_resolution', {'width': 1920, 'height': 1080})
            self.resolution_width.setValue(resolution['width'])
            self.resolution_height.setValue(resolution['height'])
            self.default_fps.setValue(settings.get('default_fps', 30))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            settings = {
                'openai_api_key': self.openai_key.text(),
                'google_api_key': self.google_key.text(),
                'projects_directory': self.projects_dir.text(),
                'auto_save': self.auto_save.isChecked(),
                'auto_save_interval': self.save_interval.value(),
                'default_resolution': {
                    'width': self.resolution_width.value(),
                    'height': self.resolution_height.value()
                },
                'default_fps': self.default_fps.value()
            }
            
            config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
            os.makedirs(config_dir, exist_ok=True)
            
            config_path = os.path.join(config_dir, 'settings.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            
            QMessageBox.information(self, "Success", "Settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to default values"""
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # API settings
            self.openai_key.clear()
            self.google_key.clear()
            
            # Project settings
            self.projects_dir.clear()
            self.auto_save.setChecked(True)
            self.save_interval.setValue(5)
            
            # Video settings
            self.resolution_width.setValue(1920)
            self.resolution_height.setValue(1080)
            self.default_fps.setValue(30)
    
    def browse_projects_dir(self):
        """Open directory browser for projects directory"""
        current_dir = self.projects_dir.text() or os.path.expanduser("~")
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Projects Directory",
            current_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if dir_path:
            self.projects_dir.setText(dir_path) 