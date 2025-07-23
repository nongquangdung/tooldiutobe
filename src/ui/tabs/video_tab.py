from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QProgressBar, QComboBox, QLineEdit, QCheckBox,
    QGroupBox, QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from ui.threads.video_generation import VideoGenerationThread
from ui.styles import (
    BUTTON_STYLE, LABEL_STYLE, GROUP_BOX_STYLE
)

class VideoTab(QWidget):
    generation_started = Signal()
    generation_finished = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
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
        
        # Project name group
        project_group = QGroupBox("Tên Dự Án")
        project_group.setStyleSheet(GROUP_BOX_STYLE)
        project_layout = QHBoxLayout()
        
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Nhập tên dự án...")
        project_layout.addWidget(self.project_name)
        
        project_group.setLayout(project_layout)
        content_layout.addWidget(project_group)
        
        # Prompt group
        prompt_group = QGroupBox("Nội Dung Video")
        prompt_group.setStyleSheet(GROUP_BOX_STYLE)
        prompt_layout = QVBoxLayout()
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Nhập nội dung video...")
        prompt_layout.addWidget(self.prompt_input)
        
        prompt_group.setLayout(prompt_layout)
        content_layout.addWidget(prompt_group)
        
        # Effects group
        effects_group = QGroupBox("Hiệu Ứng")
        effects_group.setStyleSheet(GROUP_BOX_STYLE)
        effects_layout = QHBoxLayout()
        
        self.effects_combo = QComboBox()
        self.effects_combo.addItems(["Không có hiệu ứng", "Fade", "Slide", "Zoom"])
        effects_layout.addWidget(self.effects_combo)
        
        effects_group.setLayout(effects_layout)
        content_layout.addWidget(effects_group)
        
        # Custom images group
        images_group = QGroupBox("Ảnh Tùy Chỉnh")
        images_group.setStyleSheet(GROUP_BOX_STYLE)
        images_layout = QVBoxLayout()
        
        self.use_custom_images = QCheckBox("Sử dụng ảnh tùy chỉnh")
        images_layout.addWidget(self.use_custom_images)
        
        images_select_layout = QHBoxLayout()
        self.custom_images_path = QLineEdit()
        self.custom_images_path.setPlaceholderText("Đường dẫn thư mục ảnh...")
        self.custom_images_path.setEnabled(False)
        images_select_layout.addWidget(self.custom_images_path)
        
        self.browse_button = QPushButton("Chọn thư mục")
        self.browse_button.setStyleSheet(BUTTON_STYLE)
        self.browse_button.setEnabled(False)
        self.browse_button.clicked.connect(self.browse_images)
        images_select_layout.addWidget(self.browse_button)
        
        images_layout.addLayout(images_select_layout)
        images_group.setLayout(images_layout)
        content_layout.addWidget(images_group)
        
        # Progress group
        self.progress_group = QGroupBox("Tiến Độ")
        self.progress_group.setStyleSheet(GROUP_BOX_STYLE)
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Sẵn sàng tạo video")
        self.status_label.setStyleSheet(LABEL_STYLE)
        progress_layout.addWidget(self.status_label)
        
        self.progress_group.setLayout(progress_layout)
        self.progress_group.setVisible(False)
        content_layout.addWidget(self.progress_group)
        
        # Generate button
        self.generate_button = QPushButton("Tạo Video")
        self.generate_button.setStyleSheet(BUTTON_STYLE)
        self.generate_button.clicked.connect(self.start_generation)
        content_layout.addWidget(self.generate_button)
        
        # Connect signals
        self.use_custom_images.stateChanged.connect(self.toggle_custom_images)
        
    def toggle_custom_images(self, state):
        enabled = state == Qt.CheckState.Checked
        self.custom_images_path.setEnabled(enabled)
        self.browse_button.setEnabled(enabled)
        
    def browse_images(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Chọn thư mục ảnh", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.custom_images_path.setText(folder)
            
    def start_generation(self):
        if not self.validate_inputs():
            return
            
        self.generation_started.emit()
        self.generate_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Create and start thread
        self.thread = VideoGenerationThread(
            prompt=self.prompt_input.toPlainText(),
            project_name=self.project_name.text(),
            effects=self.effects_combo.currentText(),
            use_custom_images=self.use_custom_images.isChecked(),
            custom_images_folder=self.custom_images_path.text() if self.use_custom_images.isChecked() else None
        )
        
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.finished.connect(self.generation_complete)
        self.thread.start()
        
    def validate_inputs(self):
        if not self.project_name.text().strip():
            self.status_label.setText("[WARNING] Vui lòng nhập tên dự án")
            return False
            
        if not self.prompt_input.toPlainText().strip():
            self.status_label.setText("[WARNING] Vui lòng nhập nội dung video")
            return False
            
        if (self.use_custom_images.isChecked() and 
            not self.custom_images_path.text().strip()):
            self.status_label.setText("[WARNING] Vui lòng chọn thư mục ảnh")
            return False
            
        return True
        
    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        
    def generation_complete(self, result):
        self.generate_button.setEnabled(True)
        self.generation_finished.emit(result)
        self.status_label.setText("[OK] Tạo video thành công") 