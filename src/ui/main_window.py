from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Video Generator")
        self.setGeometry(100, 100, 600, 400)

        # Widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout chính
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Tiêu đề
        self.title_label = QLabel("Tạo video tự động bằng AI từ prompt")
        layout.addWidget(self.title_label)

        # Ô nhập prompt
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Nhập prompt nội dung video...")
        layout.addWidget(self.prompt_input)

        # Nút tạo video
        self.generate_btn = QPushButton("Tạo video")
        layout.addWidget(self.generate_btn)

        # Label trạng thái
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Kết nối sự kiện
        self.generate_btn.clicked.connect(self.on_generate)

    def on_generate(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.status_label.setText("Vui lòng nhập prompt!")
            return
        self.status_label.setText(f"Đang xử lý prompt: {prompt}")
        # TODO: Gọi module AI để sinh nội dung 