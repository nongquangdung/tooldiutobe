"""
Modern macOS Main Window for Voice Studio
Features: Dark Mode, Native styling, Responsive design
"""
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                               QTabWidget, QScrollArea, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon, QPalette
import sys
import platform

from .macos_styles import (get_macos_stylesheet, get_dark_mode_enabled, 
                          get_modern_spacing, get_macos_window_size, 
                          get_accent_color, apply_macos_vibrancy)
from .advanced_window import AdvancedWindow

class ModernMainWindow(QMainWindow):
    """
    Modern macOS-styled Main Window
    
    Features:
    - 🌙 Automatic Dark Mode detection
    - 🍎 Native macOS styling
    - 📱 Responsive design
    - 🎨 System accent color integration
    - ♿ Accessibility support
    """
    
    def __init__(self):
        super().__init__()
        
        # Detect system preferences
        self.dark_mode = get_dark_mode_enabled()
        self.accent_color = get_accent_color()
        
        self.setup_ui()
        self.apply_macos_styling()
        self.setup_signals()
        
        # Auto-detect theme changes (macOS)
        if platform.system() == "Darwin":
            self.theme_timer = QTimer()
            self.theme_timer.timeout.connect(self.check_theme_change)
            self.theme_timer.start(5000)  # Check every 5 seconds
    
    def setup_ui(self):
        """Setup modern UI layout"""
        # Window properties
        window_size = get_macos_window_size()
        self.setWindowTitle("🎙️ Voice Studio - AI Video Generator")
        self.setMinimumSize(window_size['min_width'], window_size['min_height'])
        self.resize(window_size['default_width'], window_size['default_height'])
        
        # Enable native window appearance
        if platform.system() == "Darwin":
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
            # self.setAttribute(Qt.WA_TranslucentBackground)  # For vibrancy
        
        # Central widget with modern layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with modern spacing
        spacing = get_modern_spacing()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            spacing['window_margin'], 
            spacing['window_margin'],
            spacing['window_margin'], 
            spacing['window_margin']
        )
        main_layout.setSpacing(spacing['section_spacing'])
        central_widget.setLayout(main_layout)
        
        # Header section
        self.create_header_section(main_layout, spacing)
        
        # Quick actions section
        self.create_quick_actions_section(main_layout, spacing)
        
        # Advanced features button
        self.create_advanced_section(main_layout, spacing)
        
        # Status section
        self.create_status_section(main_layout, spacing)
    
    def create_header_section(self, parent_layout, spacing):
        """Create modern header with title and subtitle"""
        header_frame = QFrame()
        header_frame.setProperty("class", "header-section")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(spacing['item_spacing'])
        header_frame.setLayout(header_layout)
        
        # Main title
        self.title_label = QLabel("🎙️ Voice Studio")
        self.title_label.setProperty("class", "header")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Professional AI Video & Audio Generator")
        self.subtitle_label.setProperty("class", "subheader")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle_label)
        
        # Platform indicator
        platform_text = f"🍎 macOS {'(Dark Mode)' if self.dark_mode else '(Light Mode)'}"
        if platform.system() != "Darwin":
            platform_text = f"💻 {platform.system()}"
        
        self.platform_label = QLabel(platform_text)
        self.platform_label.setProperty("class", "caption")
        self.platform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.platform_label)
        
        parent_layout.addWidget(header_frame)
    
    def create_quick_actions_section(self, parent_layout, spacing):
        """Create quick start actions"""
        quick_frame = QFrame()
        quick_frame.setProperty("class", "card-section")
        quick_layout = QVBoxLayout()
        quick_layout.setSpacing(spacing['group_spacing'])
        quick_frame.setLayout(quick_layout)
        
        # Section title
        quick_title = QLabel("🚀 Quick Start")
        quick_title.setProperty("class", "subheader")
        quick_layout.addWidget(quick_title)
        
        # Prompt input
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("✨ Enter your video content prompt here...")
        self.prompt_input.setMinimumHeight(50)
        quick_layout.addWidget(self.prompt_input)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(spacing['item_spacing'])
        
        # Generate button (primary)
        self.generate_btn = QPushButton("🎬 Generate Video")
        self.generate_btn.setMinimumHeight(44)
        self.generate_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(self.generate_btn)
        
        # Voice only button (secondary)
        self.voice_only_btn = QPushButton("🎤 Voice Only")
        self.voice_only_btn.setProperty("class", "secondary")
        self.voice_only_btn.setMinimumHeight(44)
        self.voice_only_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(self.voice_only_btn)
        
        quick_layout.addLayout(button_layout)
        parent_layout.addWidget(quick_frame)
    
    def create_advanced_section(self, parent_layout, spacing):
        """Create advanced features section"""
        advanced_frame = QFrame()
        advanced_frame.setProperty("class", "card-section")
        advanced_layout = QVBoxLayout()
        advanced_layout.setSpacing(spacing['group_spacing'])
        advanced_frame.setLayout(advanced_layout)
        
        # Section title
        advanced_title = QLabel("⚙️ Advanced Features")
        advanced_title.setProperty("class", "subheader")
        advanced_layout.addWidget(advanced_title)
        
        # Feature buttons
        feature_layout = QHBoxLayout()
        feature_layout.setSpacing(spacing['item_spacing'])
        
        # Advanced Studio button
        self.advanced_btn = QPushButton("🎛️ Advanced Studio")
        self.advanced_btn.setProperty("class", "secondary")
        self.advanced_btn.setMinimumHeight(40)
        feature_layout.addWidget(self.advanced_btn)
        
        # Voice Cloning button
        self.voice_clone_btn = QPushButton("👥 Voice Cloning")
        self.voice_clone_btn.setProperty("class", "secondary")
        self.voice_clone_btn.setMinimumHeight(40)
        feature_layout.addWidget(self.voice_clone_btn)
        
        # Batch Processing button
        self.batch_btn = QPushButton("📦 Batch Processing")
        self.batch_btn.setProperty("class", "secondary")
        self.batch_btn.setMinimumHeight(40)
        feature_layout.addWidget(self.batch_btn)
        
        advanced_layout.addLayout(feature_layout)
        parent_layout.addWidget(advanced_frame)
    
    def create_status_section(self, parent_layout, spacing):
        """Create status and info section"""
        status_frame = QFrame()
        status_frame.setProperty("class", "status-section")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(spacing['item_spacing'])
        status_frame.setLayout(status_layout)
        
        # Status label
        self.status_label = QLabel("✅ Ready - Enter your prompt to get started")
        self.status_label.setProperty("class", "caption")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label)
        
        # System info
        system_info = self.get_system_info()
        self.system_label = QLabel(system_info)
        self.system_label.setProperty("class", "caption")
        self.system_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.system_label.setWordWrap(True)
        status_layout.addWidget(self.system_label)
        
        parent_layout.addWidget(status_frame)
        
        # Add spacer to push content up
        parent_layout.addStretch()
    
    def apply_macos_styling(self):
        """Apply modern macOS styling"""
        stylesheet = get_macos_stylesheet(self.dark_mode)
        self.setStyleSheet(stylesheet)
        
        # Apply vibrancy if supported
        apply_macos_vibrancy(self)
        
        # Set custom properties for styling
        self.setProperty("dark_mode", self.dark_mode)
        self.setProperty("accent_color", self.accent_color)
    
    def setup_signals(self):
        """Setup signal connections"""
        self.generate_btn.clicked.connect(self.on_generate_video)
        self.voice_only_btn.clicked.connect(self.on_voice_only)
        self.advanced_btn.clicked.connect(self.on_open_advanced)
        self.voice_clone_btn.clicked.connect(self.on_voice_cloning)
        self.batch_btn.clicked.connect(self.on_batch_processing)
        
        # Enter key for quick generation
        self.prompt_input.returnPressed.connect(self.on_generate_video)
    
    def get_system_info(self):
        """Get system information for display"""
        try:
            import torch
            gpu_info = "🚀 GPU Available" if torch.cuda.is_available() else "💻 CPU Mode"
            if platform.system() == "Darwin" and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                gpu_info = "🍎 Apple Silicon MPS"
        except:
            gpu_info = "❓ PyTorch Not Available"
        
        return f"{gpu_info} | Python {sys.version_info.major}.{sys.version_info.minor} | Cross-Platform Compatible"
    
    def check_theme_change(self):
        """Check for macOS theme changes"""
        if platform.system() == "Darwin":
            new_dark_mode = get_dark_mode_enabled()
            if new_dark_mode != self.dark_mode:
                self.dark_mode = new_dark_mode
                self.apply_macos_styling()
                self.update_platform_label()
    
    def update_platform_label(self):
        """Update platform label with current theme"""
        platform_text = f"🍎 macOS {'(Dark Mode)' if self.dark_mode else '(Light Mode)'}"
        self.platform_label.setText(platform_text)
    
    # Event Handlers
    def on_generate_video(self):
        """Handle video generation"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("⚠️ Please enter a prompt!", "warning")
            return
        
        self.update_status(f"🎬 Generating video: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'", "info")
        # TODO: Integrate with video generation system
        self.on_open_advanced()  # For now, open advanced window
    
    def on_voice_only(self):
        """Handle voice-only generation"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("⚠️ Please enter a prompt!", "warning")
            return
        
        self.update_status(f"🎤 Generating voice: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'", "info")
        # TODO: Integrate with voice-only system
        self.on_open_advanced()  # For now, open advanced window
    
    def on_open_advanced(self):
        """Open advanced studio window"""
        try:
            self.advanced_window = AdvancedWindow()
            self.advanced_window.show()
            self.update_status("🎛️ Advanced Studio opened", "success")
        except Exception as e:
            self.update_status(f"❌ Error opening Advanced Studio: {str(e)}", "error")
    
    def on_voice_cloning(self):
        """Handle voice cloning feature"""
        self.update_status("👥 Voice Cloning feature - Opening Advanced Studio...", "info")
        self.on_open_advanced()
    
    def on_batch_processing(self):
        """Handle batch processing feature"""
        self.update_status("📦 Batch Processing feature - Opening Advanced Studio...", "info")
        self.on_open_advanced()
    
    def update_status(self, message, status_type="info"):
        """Update status message with appropriate styling"""
        status_icons = {
            "info": "ℹ️",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌"
        }
        
        icon = status_icons.get(status_type, "ℹ️")
        self.status_label.setText(f"{icon} {message}")
        
        # Optional: Add status-specific styling
        self.status_label.setProperty("status_type", status_type)
        self.status_label.style().polish(self.status_label)


class MainWindow(ModernMainWindow):
    """Alias for backward compatibility"""
    pass


def main():
    """Run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Voice Studio")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Voice Studio")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 