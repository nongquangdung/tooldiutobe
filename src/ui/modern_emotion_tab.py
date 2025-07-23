#!/usr/bin/env python3
"""
[THEATER] MODERN EMOTION LIBRARY UI - PURITY DASHBOARD STYLE
====================================================

UI hiện đại cho thư viện emotion với thiết kế giống Purity UI Dashboard.

Features:
- Modern dashboard layout với card-based design
- Bảng emotions với styling hiện đại
- Status indicators (online/offline)
- Clean typography và spacing
- Responsive design
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QComboBox,
    QSlider, QLineEdit, QMessageBox, QFileDialog,
    QCheckBox, QScrollArea, QFormLayout, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox, QDoubleSpinBox, QProgressBar, QProgressDialog,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer, QSize
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QPen, QBrush, QPalette

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.unified_emotion_system import UnifiedEmotionSystem
from core.unified_emotion_helpers import get_emotion_parameters

# Import TTS provider để preview âm thanh thật
try:
    from tts.real_chatterbox_provider import RealChatterboxProvider
    PREVIEW_AVAILABLE = True
except ImportError:
    PREVIEW_AVAILABLE = False
    print("[WARNING] TTS provider not available - preview will be simulated")

import logging
logger = logging.getLogger(__name__)

# Constants for styling
COLORS = {
    "primary": "#6366F1",
    "secondary": "#64748B",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
    "light": "#F8FAFC",
    "dark": "#1E293B",
    "white": "#FFFFFF",
    "online": "#10B981",
    "offline": "#94A3B8"
}

FONTS = {
    "header": QFont("Segoe UI", 14, QFont.Bold),
    "subheader": QFont("Segoe UI", 12, QFont.Bold),
    "body": QFont("Segoe UI", 10),
    "small": QFont("Segoe UI", 9),
    "button": QFont("Segoe UI", 10, QFont.Medium)
}

class StatusIndicator(QWidget):
    """Custom widget for online/offline status indicator"""
    
    def __init__(self, is_online=True, parent=None):
        super().__init__(parent)
        self.is_online = is_online
        self.setFixedSize(12, 12)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circle
        color = COLORS["online"] if self.is_online else COLORS["offline"]
        painter.setBrush(QBrush(QColor(color)))
        painter.setPen(QPen(QColor(color), 1))
        painter.drawEllipse(2, 2, 8, 8)
    
    def set_status(self, is_online):
        self.is_online = is_online
        self.update()

class Card(QFrame):
    """Custom card widget with modern styling"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        # Card styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS["white"]};
                border-radius: 8px;
                border: none;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        # Title if provided
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(FONTS["subheader"])
            self.layout.addWidget(title_label)
    
    def set_content(self, widget):
        self.layout.addWidget(widget)
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)

class AudioPreviewThread(QThread):
    """Thread để generate preview âm thanh thật"""
    preview_completed = Signal(str, str, bool)  # emotion_name, audio_path, success
    preview_progress = Signal(str, int)  # emotion_name, progress_percent
    preview_error = Signal(str, str)  # emotion_name, error_message
    
    # High-quality emotion prompts for better preview
    EMOTION_PROMPTS = {
        "neutral": "Đây là giọng đọc trung tính, không biểu lộ cảm xúc rõ rệt.",
        "happy": "Tôi rất vui khi gặp bạn hôm nay! Thật là một ngày tuyệt vời.",
        "sad": "Tôi cảm thấy buồn khi nghĩ về những kỷ niệm đã qua.",
        "angry": "Tôi thực sự rất tức giận về cách họ đối xử với chúng ta!",
        "surprised": "Ồ! Tôi không thể tin được điều này đang xảy ra!",
        "fearful": "Tôi lo lắng về những gì có thể xảy ra tiếp theo...",
        "disgusted": "Thật kinh tởm khi nhìn thấy cách họ xử lý thực phẩm.",
        "excited": "Tôi không thể đợi để chia sẻ tin tuyệt vời này với bạn!",
        "whisper": "Đây là bí mật giữa chúng ta, đừng nói với ai nhé.",
        "shouting": "Chú ý! Mọi người cần di chuyển ra khỏi tòa nhà ngay lập tức!",
        "default": "Đây là bản preview cho cảm xúc này. Bạn có thể nghe thấy sự khác biệt không?"
    }
    
    def __init__(self, emotion_name: str, parameters: dict):
        super().__init__()
        self.emotion_name = emotion_name
        self.parameters = parameters
        self.audio_path = ""
        
        # Get appropriate prompt text
        lower_name = emotion_name.lower()
        for key in self.EMOTION_PROMPTS:
            if key in lower_name:
                self.prompt_text = self.EMOTION_PROMPTS[key]
                break
        else:
            self.prompt_text = self.EMOTION_PROMPTS["default"]
    
    def run(self):
        try:
            # Report progress
            self.preview_progress.emit(self.emotion_name, 10)
            
            # Initialize TTS provider
            if PREVIEW_AVAILABLE:
                tts_provider = RealChatterboxProvider()
                self.preview_progress.emit(self.emotion_name, 30)
                
                # Generate audio with emotion parameters
                output_dir = os.path.join(os.getcwd(), "voice_studio_output")
                os.makedirs(output_dir, exist_ok=True)
                
                self.preview_progress.emit(self.emotion_name, 50)
                
                # Generate audio
                self.audio_path = tts_provider.generate_audio(
                    text=self.prompt_text,
                    output_dir=output_dir,
                    voice="Abigail",  # Default voice
                    temperature=self.parameters.get("temperature", 0.8),
                    exaggeration=self.parameters.get("exaggeration", 1.0),
                    cfg_weight=self.parameters.get("cfg_weight", 0.6),
                    speed=self.parameters.get("speed", 1.0)
                )
                
                self.preview_progress.emit(self.emotion_name, 90)
                
                # Emit completion signal
                self.preview_completed.emit(self.emotion_name, self.audio_path, True)
            else:
                # Simulate preview if TTS not available
                self.preview_progress.emit(self.emotion_name, 30)
                time.sleep(0.5)
                self.preview_progress.emit(self.emotion_name, 60)
                time.sleep(0.5)
                self.preview_progress.emit(self.emotion_name, 90)
                time.sleep(0.5)
                
                # Emit completion with no audio path
                self.preview_completed.emit(self.emotion_name, "", False)
                
        except Exception as e:
            logger.error(f"Error in preview thread: {str(e)}")
            self.preview_error.emit(self.emotion_name, str(e))

class ModernEmotionTab(QWidget):
    """Modern Emotion Configuration Tab với thiết kế Purity Dashboard"""
    
    def __init__(self):
        super().__init__()
        self.unified_emotion_system = UnifiedEmotionSystem()
        self.preview_threads = {}  # Track active preview threads
        
        # Store original/default Inner Voice values for reset
        self.inner_voice_original_values = {}
        
        self.setup_ui()
        self.load_emotions_to_table()
        self.connect_signals()
        
        # Update statistics
        self.update_statistics()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header with title and search
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("PURITY UI DASHBOARD")
        title_label.setFont(FONTS["header"])
        header_layout.addWidget(title_label)
        
        # Tabs label
        tabs_label = QLabel("Tables")
        tabs_label.setFont(FONTS["body"])
        tabs_label.setStyleSheet(f"color: {COLORS['secondary']};")
        header_layout.addWidget(tabs_label, 0, Qt.AlignLeft)
        
        header_layout.addStretch()
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Type here...")
        search_box.setFixedWidth(200)
        search_box.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #E2E8F0;
                border-radius: 15px;
                padding: 8px 15px;
                background-color: {COLORS['white']};
            }}
        """)
        header_layout.addWidget(search_box)
        
        # Sign in button
        sign_in_btn = QPushButton("Sign In")
        sign_in_btn.setFont(FONTS["body"])
        sign_in_btn.setCursor(Qt.PointingHandCursor)
        sign_in_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['dark']};
                border: none;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                color: {COLORS['primary']};
            }}
        """)
        header_layout.addWidget(sign_in_btn)
        
        main_layout.addLayout(header_layout)
        
        # Authors Table Card
        authors_card = Card("Authors Table")
        
        # Table container
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(10)
        
        # Table header
        table_header = QWidget()
        table_header_layout = QHBoxLayout(table_header)
        table_header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Header columns
        headers = ["AUTHOR", "FUNCTION", "STATUS", "EMPLOYED", ""]
        for header_text in headers:
            header_label = QLabel(header_text)
            header_label.setFont(FONTS["small"])
            header_label.setStyleSheet(f"color: {COLORS['secondary']};")
            table_header_layout.addWidget(header_label)
            if header_text == "":
                table_header_layout.setStretch(headers.index(header_text), 0)
            else:
                table_header_layout.setStretch(headers.index(header_text), 1)
        
        table_layout.addWidget(table_header)
        
        # Table rows
        authors_data = [
            {
                "name": "Esthera Jackson",
                "email": "esthera@simmmple.com",
                "function": "Manager",
                "department": "Organization",
                "status": "Online",
                "employed": "14/06/21"
            },
            {
                "name": "Alexa Liras",
                "email": "alexa@simmmple.com",
                "function": "Programmer",
                "department": "Developer",
                "status": "Offline",
                "employed": "14/06/21"
            },
            {
                "name": "Laurent Michael",
                "email": "laurent@simmmple.com",
                "function": "Executive",
                "department": "Projects",
                "status": "Online",
                "employed": "14/06/21"
            },
            {
                "name": "Freduardo Hill",
                "email": "freduardo@simmmple.com",
                "function": "Manager",
                "department": "Organization",
                "status": "Online",
                "employed": "14/06/21"
            },
            {
                "name": "Daniel Thomas",
                "email": "daniel@simmmple.com",
                "function": "Programmer",
                "department": "Developer",
                "status": "Offline",
                "employed": "14/06/21"
            },
            {
                "name": "Mark Wilson",
                "email": "mark@simmmple.com",
                "function": "Designer",
                "department": "UI/UX Design",
                "status": "Offline",
                "employed": "14/06/21"
            }
        ]
        
        for author in authors_data:
            row = QFrame()
            row.setFrameShape(QFrame.NoFrame)
            row.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['white']};
                    border-bottom: 1px solid #E2E8F0;
                    padding: 10px 0;
                }}
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 10, 0, 10)
            
            # Author column
            author_widget = QWidget()
            author_layout = QHBoxLayout(author_widget)
            author_layout.setContentsMargins(0, 0, 0, 0)
            
            # Avatar placeholder
            avatar = QLabel()
            avatar.setFixedSize(36, 36)
            avatar.setStyleSheet(f"""
                QLabel {{
                    background-color: #E2E8F0;
                    border-radius: 18px;
                }}
            """)
            author_layout.addWidget(avatar)
            
            # Name and email
            name_email = QWidget()
            name_email_layout = QVBoxLayout(name_email)
            name_email_layout.setContentsMargins(10, 0, 0, 0)
            name_email_layout.setSpacing(2)
            
            name_label = QLabel(author["name"])
            name_label.setFont(FONTS["body"])
            name_email_layout.addWidget(name_label)
            
            email_label = QLabel(author["email"])
            email_label.setFont(FONTS["small"])
            email_label.setStyleSheet(f"color: {COLORS['secondary']};")
            name_email_layout.addWidget(email_label)
            
            author_layout.addWidget(name_email)
            row_layout.addWidget(author_widget, 1)
            
            # Function column
            function_widget = QWidget()
            function_layout = QVBoxLayout(function_widget)
            function_layout.setContentsMargins(0, 0, 0, 0)
            function_layout.setSpacing(2)
            
            function_label = QLabel(author["function"])
            function_label.setFont(FONTS["body"])
            function_layout.addWidget(function_label)
            
            department_label = QLabel(author["department"])
            department_label.setFont(FONTS["small"])
            department_label.setStyleSheet(f"color: {COLORS['secondary']};")
            function_layout.addWidget(department_label)
            
            row_layout.addWidget(function_widget, 1)
            
            # Status column
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(0, 0, 0, 0)
            
            status_indicator = StatusIndicator(author["status"] == "Online")
            status_layout.addWidget(status_indicator)
            
            status_label = QLabel(author["status"])
            status_label.setFont(FONTS["body"])
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            
            row_layout.addWidget(status_widget, 1)
            
            # Employed column
            employed_label = QLabel(author["employed"])
            employed_label.setFont(FONTS["body"])
            row_layout.addWidget(employed_label, 1)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setFont(FONTS["small"])
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['secondary']};
                    border: none;
                }}
                QPushButton:hover {{
                    color: {COLORS['primary']};
                }}
            """)
            row_layout.addWidget(edit_btn, 0)
            
            table_layout.addWidget(row)
        
        authors_card.set_content(table_container)
        main_layout.addWidget(authors_card)
        
        # Projects Table Card
        projects_card = Card("Projects")
        
        # Projects container
        projects_container = QWidget()
        projects_layout = QVBoxLayout(projects_container)
        projects_layout.setContentsMargins(0, 0, 0, 0)
        projects_layout.setSpacing(10)
        
        # Projects header
        projects_header = QWidget()
        projects_header_layout = QHBoxLayout(projects_header)
        projects_header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Header with completion indicator
        projects_header_layout.addWidget(QLabel("30 done this month"))
        
        projects_layout.addWidget(projects_header)
        
        # Projects table header
        projects_table_header = QWidget()
        projects_header_layout = QHBoxLayout(projects_table_header)
        projects_header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Header columns
        project_headers = ["COMPANIES", "BUDGET", "STATUS", "COMPLETION", ""]
        for header_text in project_headers:
            header_label = QLabel(header_text)
            header_label.setFont(FONTS["small"])
            header_label.setStyleSheet(f"color: {COLORS['secondary']};")
            projects_header_layout.addWidget(header_label)
            if header_text == "":
                projects_header_layout.setStretch(project_headers.index(header_text), 0)
            else:
                projects_header_layout.setStretch(project_headers.index(header_text), 1)
        
        projects_layout.addWidget(projects_table_header)
        
        # Projects data
        projects_data = [
            {
                "name": "Chakra Soft UI Version",
                "budget": "$14,000",
                "status": "Working",
                "completion": 60
            },
            {
                "name": "Add Progress Track",
                "budget": "$3,000",
                "status": "Canceled",
                "completion": 10
            },
            {
                "name": "Fix Platform Errors",
                "budget": "Not set",
                "status": "Done",
                "completion": 100
            },
            {
                "name": "Launch our Mobile App",
                "budget": "$32,000",
                "status": "Done",
                "completion": 100
            },
            {
                "name": "Add the New Pricing Page",
                "budget": "$400",
                "status": "Working",
                "completion": 25
            }
        ]
        
        for project in projects_data:
            row = QFrame()
            row.setFrameShape(QFrame.NoFrame)
            row.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['white']};
                    border-bottom: 1px solid #E2E8F0;
                    padding: 10px 0;
                }}
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 10, 0, 10)
            
            # Company column
            company_label = QLabel(project["name"])
            company_label.setFont(FONTS["body"])
            row_layout.addWidget(company_label, 1)
            
            # Budget column
            budget_label = QLabel(project["budget"])
            budget_label.setFont(FONTS["body"])
            row_layout.addWidget(budget_label, 1)
            
            # Status column
            status_label = QLabel(project["status"])
            status_label.setFont(FONTS["body"])
            
            # Set color based on status
            if project["status"] == "Working":
                status_color = COLORS["info"]
            elif project["status"] == "Done":
                status_color = COLORS["success"]
            elif project["status"] == "Canceled":
                status_color = COLORS["danger"]
            else:
                status_color = COLORS["secondary"]
                
            status_label.setStyleSheet(f"color: {status_color};")
            row_layout.addWidget(status_label, 1)
            
            # Completion column with progress bar
            completion_widget = QWidget()
            completion_layout = QVBoxLayout(completion_widget)
            completion_layout.setContentsMargins(0, 0, 0, 0)
            completion_layout.setSpacing(5)
            
            completion_text = QLabel(f"{project['completion']}%")
            completion_text.setFont(FONTS["small"])
            completion_layout.addWidget(completion_text)
            
            progress_bar = QProgressBar()
            progress_bar.setValue(project["completion"])
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(4)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #E2E8F0;
                    border-radius: 2px;
                    border: none;
                }}
                QProgressBar::chunk {{
                    background-color: {COLORS['primary']};
                    border-radius: 2px;
                }}
            """)
            completion_layout.addWidget(progress_bar)
            
            row_layout.addWidget(completion_widget, 1)
            
            # Actions column
            actions_btn = QPushButton("...")
            actions_btn.setFixedWidth(30)
            actions_btn.setFont(FONTS["body"])
            actions_btn.setCursor(Qt.PointingHandCursor)
            actions_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['secondary']};
                    border: none;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    color: {COLORS['primary']};
                }}
            """)
            row_layout.addWidget(actions_btn, 0)
            
            projects_layout.addWidget(row)
        
        projects_card.set_content(projects_container)
        main_layout.addWidget(projects_card)
        
        # Footer
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 10, 0, 0)
        
        copyright_text = QLabel("© 2021, Made with [HEART] by Creative Tim × Simmmple for a better web")
        copyright_text.setFont(FONTS["small"])
        copyright_text.setStyleSheet(f"color: {COLORS['secondary']};")
        footer_layout.addWidget(copyright_text)
        
        footer_layout.addStretch()
        
        footer_links = ["Creative Tim", "Simmmple", "Blog", "License"]
        for link in footer_links:
            link_label = QLabel(link)
            link_label.setFont(FONTS["small"])
            link_label.setStyleSheet(f"color: {COLORS['secondary']};")
            footer_layout.addWidget(link_label)
        
        main_layout.addWidget(footer)
    
    def load_emotions_to_table(self):
        """Load emotions to table (placeholder for now)"""
        pass
    
    def connect_signals(self):
        """Connect signals for UI interactions"""
        pass
    
    def update_statistics(self):
        """Update emotion statistics"""
        pass

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ModernEmotionTab()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec()) 