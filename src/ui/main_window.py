<<<<<<< Updated upstream
"""
Modern Cross-Platform Main Window for Voice Studio
Features: Adaptive UI, Platform-optimized styling, Responsive design
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
    Modern Cross-Platform Main Window
    
    Features:
    - 🌙 Automatic Dark Mode detection (macOS)
    - 🍎 Native platform styling (macOS/Windows/Linux)
    - 📱 Responsive design
    - 🎨 System accent color integration
    - ♿ Accessibility support
    """
    
    def __init__(self):
        super().__init__()
        
        # Platform detection
        self.platform = platform.system()
        
        # Platform-specific configurations
        self.setup_platform_config()
        
        self.setup_ui()
        self.apply_platform_styling()
        self.setup_signals()
        
        # Auto-detect theme changes (macOS only)
        if self.platform == "Darwin":
            self.theme_timer = QTimer()
            self.theme_timer.timeout.connect(self.check_theme_change)
            self.theme_timer.start(5000)  # Check every 5 seconds
    
    def setup_platform_config(self):
        """Setup platform-specific configurations"""
        if self.platform == "Darwin":  # macOS
            self.dark_mode = get_dark_mode_enabled()
            self.accent_color = get_accent_color()
            self.native_features = True
        elif self.platform == "Windows":
            # Windows-specific config
            self.dark_mode = self.is_windows_dark_mode()
            self.accent_color = '#0078D4'  # Windows 10/11 blue
            self.native_features = True
        else:  # Linux
            # Linux-specific config  
            self.dark_mode = self.is_linux_dark_mode()
            self.accent_color = '#4A90E2'  # Standard blue
            self.native_features = False
    
    def is_windows_dark_mode(self):
        """Detect Windows dark mode"""
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            return False
    
    def is_linux_dark_mode(self):
        """Detect Linux dark mode (basic detection)"""
        try:
            import subprocess
            # Try GNOME/GTK settings
            result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], 
                                  capture_output=True, text=True)
            return 'dark' in result.stdout.lower()
        except:
            return False
    
    def setup_ui(self):
        """Setup modern UI layout"""
        # Platform-optimized window properties
        if self.platform == "Darwin":
            window_size = get_macos_window_size()
            self.setWindowTitle("🎙️ Voice Studio - AI Video Generator")
        elif self.platform == "Windows":
            window_size = {
                'default_width': 1300, 'default_height': 850,
                'min_width': 1100, 'min_height': 750
            }
            self.setWindowTitle("Voice Studio - AI Video Generator")
        else:  # Linux
            window_size = {
                'default_width': 1250, 'default_height': 800,
                'min_width': 1000, 'min_height': 700
            }
            self.setWindowTitle("Voice Studio - AI Video Generator")
        
        self.setMinimumSize(window_size['min_width'], window_size['min_height'])
        self.resize(window_size['default_width'], window_size['default_height'])
        
        # Enable platform-specific window features
        if self.platform == "Darwin":
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Central widget with modern layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Platform-optimized spacing
        if self.platform == "Darwin":
            spacing = get_modern_spacing()
        else:
            spacing = {
                'window_margin': 16 if self.platform == "Windows" else 12,
                'section_spacing': 20 if self.platform == "Windows" else 16,
                'group_spacing': 12,
                'item_spacing': 6
            }
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            spacing['window_margin'], spacing['window_margin'],
            spacing['window_margin'], spacing['window_margin']
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
        
        # Platform-specific title
        if self.platform == "Darwin":
            title_text = "🎙️ Voice Studio"
        elif self.platform == "Windows":  
            title_text = "🎤 Voice Studio"
        else:
            title_text = "🔊 Voice Studio"
        
        self.title_label = QLabel(title_text)
        self.title_label.setProperty("class", "header")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Professional AI Video & Audio Generator")
        self.subtitle_label.setProperty("class", "subheader")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle_label)
        
        # Platform indicator
        self.update_platform_label()
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
        
        # Prompt input with platform-specific placeholder
        self.prompt_input = QLineEdit()
        if self.platform == "Darwin":
            placeholder = "✨ Enter your video content prompt here..."
        elif self.platform == "Windows":
            placeholder = "💡 Enter your video content prompt here..."
        else:
            placeholder = "📝 Enter your video content prompt here..."
        
        self.prompt_input.setPlaceholderText(placeholder)
        self.prompt_input.setMinimumHeight(44 if self.platform == "Darwin" else 40)
        quick_layout.addWidget(self.prompt_input)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(spacing['item_spacing'])
        
        # Generate button (primary)
        self.generate_btn = QPushButton("🎬 Generate Video")
        self.generate_btn.setMinimumHeight(44 if self.platform == "Darwin" else 40)
        self.generate_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(self.generate_btn)
        
        # Voice only button (secondary)
        self.voice_only_btn = QPushButton("🎤 Voice Only")
        self.voice_only_btn.setProperty("class", "secondary")
        self.voice_only_btn.setMinimumHeight(44 if self.platform == "Darwin" else 40)
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
        
        # Platform-specific button heights
        btn_height = 40 if self.platform == "Darwin" else 36
        
        # Advanced Studio button
        self.advanced_btn = QPushButton("🎛️ Advanced Studio")
        self.advanced_btn.setProperty("class", "secondary")
        self.advanced_btn.setMinimumHeight(btn_height)
        feature_layout.addWidget(self.advanced_btn)
        
        # Voice Cloning button
        self.voice_clone_btn = QPushButton("👥 Voice Cloning")
        self.voice_clone_btn.setProperty("class", "secondary")
        self.voice_clone_btn.setMinimumHeight(btn_height)
        feature_layout.addWidget(self.voice_clone_btn)
        
        # Batch Processing button
        self.batch_btn = QPushButton("📦 Batch Processing")
        self.batch_btn.setProperty("class", "secondary")
        self.batch_btn.setMinimumHeight(btn_height)
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
        
        # Status display
        self.status_label = QLabel("🔗 Ready - Click above to get started")
        self.status_label.setProperty("class", "status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        # System info
        info_text = self.get_system_info()
        self.info_label = QLabel(info_text)
        self.info_label.setProperty("class", "caption")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.info_label)
        
        parent_layout.addWidget(status_frame)
    
    def apply_platform_styling(self):
        """Apply platform-optimized styling"""
        try:
            if self.platform == "Darwin":
                # Use macOS optimized stylesheet
                stylesheet = get_macos_stylesheet(self.dark_mode)
                self.setStyleSheet(stylesheet)
            elif self.platform == "Windows":
                # Use Windows-adapted stylesheet
                stylesheet = self.get_windows_stylesheet()
                self.setStyleSheet(stylesheet)
            else:
                # Use Linux-adapted stylesheet
                stylesheet = self.get_linux_stylesheet()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"⚠️ Styling error: {e}")
            # Fallback to basic styling
            self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")
    
    def get_windows_stylesheet(self):
        """Windows-optimized stylesheet"""
        return get_macos_stylesheet(self.dark_mode).replace(
            "SF Pro Display", "Segoe UI").replace("12px", "10px")
    
    def get_linux_stylesheet(self):
        """Linux-optimized stylesheet"""
        return get_macos_stylesheet(self.dark_mode).replace(
            "SF Pro Display", "Ubuntu, Roboto").replace("border-radius: 12px", "border-radius: 8px")
    
    def setup_signals(self):
        """Setup button signals"""
        self.generate_btn.clicked.connect(self.on_generate_video)
        self.voice_only_btn.clicked.connect(self.on_voice_only)
        self.advanced_btn.clicked.connect(self.on_open_advanced)
        self.voice_clone_btn.clicked.connect(self.on_voice_cloning)
        self.batch_btn.clicked.connect(self.on_batch_processing)
    
    def get_system_info(self):
        """Get system information for display"""
        try:
            gpu_info = "🔥 GPU Available" if self.platform == "Darwin" and hasattr(__import__('torch').backends, 'mps') and __import__('torch').backends.mps.is_available() else "💻 CPU Mode"
            return f"{self.platform} • {gpu_info} • Voice Studio v2.0"
        except:
            return f"{self.platform} • CPU Mode • Voice Studio v2.0"
    
    def check_theme_change(self):
        """Check for system theme changes (macOS)"""
        if self.platform == "Darwin":
            new_dark_mode = get_dark_mode_enabled()
            if new_dark_mode != self.dark_mode:
                self.dark_mode = new_dark_mode
                self.apply_platform_styling()
                self.update_platform_label()
    
    def update_platform_label(self):
        """Update platform indicator label"""
        if self.platform == "Darwin":
            platform_text = f"🍎 macOS {'(Dark Mode)' if self.dark_mode else '(Light Mode)'}"
        elif self.platform == "Windows":
            platform_text = f"🪟 Windows {'(Dark)' if self.dark_mode else '(Light)'}"
        else:
            platform_text = f"🐧 Linux {'(Dark)' if self.dark_mode else '(Light)'}"
        
        if not hasattr(self, 'platform_label'):
            self.platform_label = QLabel(platform_text)
            self.platform_label.setProperty("class", "caption")
            self.platform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.platform_label.setText(platform_text)
    
    def on_generate_video(self):
        """Handle generate video button click"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("⚠️ Please enter a video prompt first", "warning")
            return
        
        self.update_status("🎬 Opening Advanced Studio for video generation...", "info")
        self.on_open_advanced()
    
    def on_voice_only(self):
        """Handle voice only button click"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("⚠️ Please enter a voice prompt first", "warning")
            return
        
        self.update_status("🎤 Opening Advanced Studio for voice generation...", "info")
        self.on_open_advanced()
    
    def on_open_advanced(self):
        """Open advanced studio window"""
        try:
            self.advanced_window = AdvancedWindow()
            
            # Transfer prompt if available
            prompt = self.prompt_input.text().strip()
            if prompt and hasattr(self.advanced_window, 'story_input'):
                self.advanced_window.story_input.setPlainText(prompt)
            
            self.advanced_window.show()
            self.update_status("✅ Advanced Studio opened successfully", "success")
        except Exception as e:
            self.update_status(f"❌ Error opening Advanced Studio: {str(e)}", "error")
    
    def on_voice_cloning(self):
        """Handle voice cloning button"""
        self.update_status("👥 Voice cloning feature - Available in Advanced Studio", "info")
        self.on_open_advanced()
    
    def on_batch_processing(self):
        """Handle batch processing button"""
        self.update_status("📦 Batch processing - Available in Advanced Studio", "info")
        self.on_open_advanced()
    
    def update_status(self, message, status_type="info"):
        """Update status message with type-specific styling"""
        self.status_label.setText(message)
        
        # Update status class for styling
        status_classes = {
            "success": "status-success",
            "warning": "status-warning", 
            "error": "status-error",
            "info": "status"
        }
        
        class_name = status_classes.get(status_type, "status")
        self.status_label.setProperty("class", class_name)
        
        # Force style update
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

# Backward compatibility alias
class MainWindow(ModernMainWindow):
    """Backward compatibility alias for ModernMainWindow"""
    pass

def main():
    """Main application entry point with cross-platform support"""
    app = QApplication(sys.argv)
    
    # Platform-specific app setup
    if platform.system() == "Darwin":
        app.setApplicationName("Voice Studio")
        app.setApplicationDisplayName("🎙️ Voice Studio")
    elif platform.system() == "Windows":
        app.setApplicationName("Voice Studio")
    
    window = ModernMainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
=======
"""
Modern Cross-Platform Main Window for Voice Studio
Features: Adaptive UI, Platform-optimized styling, Responsive design
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
    Modern Cross-Platform Main Window
    
    Features:
    - [EMOJI] Automatic Dark Mode detection (macOS)
    - [APPLE] Native platform styling (macOS/Windows/Linux)
    - [MOBILE] Responsive design
    - [PAINT] System accent color integration
    - [EMOJI] Accessibility support
    """
    
    def __init__(self):
        super().__init__()
        
        # Platform detection
        self.platform = platform.system()
        
        # Platform-specific configurations
        self.setup_platform_config()
        
        self.setup_ui()
        self.apply_platform_styling()
        self.setup_signals()
        
        # Auto-detect theme changes (macOS only)
        if self.platform == "Darwin":
            self.theme_timer = QTimer()
            self.theme_timer.timeout.connect(self.check_theme_change)
            self.theme_timer.start(5000)  # Check every 5 seconds
    
    def setup_platform_config(self):
        """Setup platform-specific configurations"""
        if self.platform == "Darwin":  # macOS
            self.dark_mode = get_dark_mode_enabled()
            self.accent_color = get_accent_color()
            self.native_features = True
        elif self.platform == "Windows":
            # Windows-specific config
            self.dark_mode = self.is_windows_dark_mode()
            self.accent_color = '#0078D4'  # Windows 10/11 blue
            self.native_features = True
        else:  # Linux
            # Linux-specific config  
            self.dark_mode = self.is_linux_dark_mode()
            self.accent_color = '#4A90E2'  # Standard blue
            self.native_features = False
    
    def is_windows_dark_mode(self):
        """Detect Windows dark mode"""
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except:
            return False
    
    def is_linux_dark_mode(self):
        """Detect Linux dark mode (basic detection)"""
        try:
            import subprocess
            # Try GNOME/GTK settings
            result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], 
                                  capture_output=True, text=True)
            return 'dark' in result.stdout.lower()
        except:
            return False
    
    def setup_ui(self):
        """Setup modern UI layout"""
        # Platform-optimized window properties
        if self.platform == "Darwin":
            window_size = get_macos_window_size()
            self.setWindowTitle("[MIC] Voice Studio - AI Video Generator")
        elif self.platform == "Windows":
            window_size = {
                'default_width': 1300, 'default_height': 850,
                'min_width': 1100, 'min_height': 750
            }
            self.setWindowTitle("Voice Studio - AI Video Generator")
        else:  # Linux
            window_size = {
                'default_width': 1250, 'default_height': 800,
                'min_width': 1000, 'min_height': 700
            }
            self.setWindowTitle("Voice Studio - AI Video Generator")
        
        self.setMinimumSize(window_size['min_width'], window_size['min_height'])
        self.resize(window_size['default_width'], window_size['default_height'])
        
        # Enable platform-specific window features
        if self.platform == "Darwin":
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Central widget with modern layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Platform-optimized spacing
        if self.platform == "Darwin":
            spacing = get_modern_spacing()
        else:
            spacing = {
                'window_margin': 16 if self.platform == "Windows" else 12,
                'section_spacing': 20 if self.platform == "Windows" else 16,
                'group_spacing': 12,
                'item_spacing': 6
            }
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            spacing['window_margin'], spacing['window_margin'],
            spacing['window_margin'], spacing['window_margin']
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
        
        # Platform-specific title
        if self.platform == "Darwin":
            title_text = "[MIC] Voice Studio"
        elif self.platform == "Windows":  
            title_text = "[EMOJI] Voice Studio"
        else:
            title_text = "[SOUND] Voice Studio"
        
        self.title_label = QLabel(title_text)
        self.title_label.setProperty("class", "header")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Professional AI Video & Audio Generator")
        self.subtitle_label.setProperty("class", "subheader")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle_label)
        
        # Platform indicator
        self.update_platform_label()
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
        quick_title = QLabel("[ROCKET] Quick Start")
        quick_title.setProperty("class", "subheader")
        quick_layout.addWidget(quick_title)
        
        # Prompt input with platform-specific placeholder
        self.prompt_input = QLineEdit()
        if self.platform == "Darwin":
            placeholder = "[SPARKLE] Enter your video content prompt here..."
        elif self.platform == "Windows":
            placeholder = "[IDEA] Enter your video content prompt here..."
        else:
            placeholder = "[EDIT] Enter your video content prompt here..."
        
        self.prompt_input.setPlaceholderText(placeholder)
        self.prompt_input.setMinimumHeight(44 if self.platform == "Darwin" else 40)
        quick_layout.addWidget(self.prompt_input)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(spacing['item_spacing'])
        
        # Generate button (primary)
        self.generate_btn = QPushButton("[ACTION] Generate Video")
        self.generate_btn.setMinimumHeight(44 if self.platform == "Darwin" else 40)
        self.generate_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(self.generate_btn)
        
        # Voice only button (secondary)
        self.voice_only_btn = QPushButton("[EMOJI] Voice Only")
        self.voice_only_btn.setProperty("class", "secondary")
        self.voice_only_btn.setMinimumHeight(44 if self.platform == "Darwin" else 40)
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
        advanced_title = QLabel("[CONFIG] Advanced Features")
        advanced_title.setProperty("class", "subheader")
        advanced_layout.addWidget(advanced_title)
        
        # Feature buttons
        feature_layout = QHBoxLayout()
        feature_layout.setSpacing(spacing['item_spacing'])
        
        # Platform-specific button heights
        btn_height = 40 if self.platform == "Darwin" else 36
        
        # Advanced Studio button
        self.advanced_btn = QPushButton("[EMOJI] Advanced Studio")
        self.advanced_btn.setProperty("class", "secondary")
        self.advanced_btn.setMinimumHeight(btn_height)
        feature_layout.addWidget(self.advanced_btn)
        
        # Voice Cloning button
        self.voice_clone_btn = QPushButton("[USERS] Voice Cloning")
        self.voice_clone_btn.setProperty("class", "secondary")
        self.voice_clone_btn.setMinimumHeight(btn_height)
        feature_layout.addWidget(self.voice_clone_btn)
        
        # Batch Processing button
        self.batch_btn = QPushButton("[EMOJI] Batch Processing")
        self.batch_btn.setProperty("class", "secondary")
        self.batch_btn.setMinimumHeight(btn_height)
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
        
        # Status display
        self.status_label = QLabel("[EMOJI] Ready - Click above to get started")
        self.status_label.setProperty("class", "status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        # System info
        info_text = self.get_system_info()
        self.info_label = QLabel(info_text)
        self.info_label.setProperty("class", "caption")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.info_label)
        
        parent_layout.addWidget(status_frame)
    
    def apply_platform_styling(self):
        """Apply platform-optimized styling"""
        try:
            if self.platform == "Darwin":
                # Use macOS optimized stylesheet
                stylesheet = get_macos_stylesheet(self.dark_mode)
                self.setStyleSheet(stylesheet)
            elif self.platform == "Windows":
                # Use Windows-adapted stylesheet
                stylesheet = self.get_windows_stylesheet()
                self.setStyleSheet(stylesheet)
            else:
                # Use Linux-adapted stylesheet
                stylesheet = self.get_linux_stylesheet()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"[WARNING] Styling error: {e}")
            # Fallback to basic styling
            self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")
    
    def get_windows_stylesheet(self):
        """Windows-optimized stylesheet"""
        return get_macos_stylesheet(self.dark_mode).replace(
            "SF Pro Display", "Segoe UI").replace("12px", "10px")
    
    def get_linux_stylesheet(self):
        """Linux-optimized stylesheet"""
        return get_macos_stylesheet(self.dark_mode).replace(
            "SF Pro Display", "Ubuntu, Roboto").replace("border-radius: 12px", "border-radius: 8px")
    
    def setup_signals(self):
        """Setup button signals"""
        self.generate_btn.clicked.connect(self.on_generate_video)
        self.voice_only_btn.clicked.connect(self.on_voice_only)
        self.advanced_btn.clicked.connect(self.on_open_advanced)
        self.voice_clone_btn.clicked.connect(self.on_voice_cloning)
        self.batch_btn.clicked.connect(self.on_batch_processing)
    
    def get_system_info(self):
        """Get system information for display"""
        try:
            gpu_info = "[HOT] GPU Available" if self.platform == "Darwin" and hasattr(__import__('torch').backends, 'mps') and __import__('torch').backends.mps.is_available() else "[PC] CPU Mode"
            return f"{self.platform} • {gpu_info} • Voice Studio v2.0"
        except:
            return f"{self.platform} • CPU Mode • Voice Studio v2.0"
    
    def check_theme_change(self):
        """Check for system theme changes (macOS)"""
        if self.platform == "Darwin":
            new_dark_mode = get_dark_mode_enabled()
            if new_dark_mode != self.dark_mode:
                self.dark_mode = new_dark_mode
                self.apply_platform_styling()
                self.update_platform_label()
    
    def update_platform_label(self):
        """Update platform indicator label"""
        if self.platform == "Darwin":
            platform_text = f"[APPLE] macOS {'(Dark Mode)' if self.dark_mode else '(Light Mode)'}"
        elif self.platform == "Windows":
            platform_text = f"🪟 Windows {'(Dark)' if self.dark_mode else '(Light)'}"
        else:
            platform_text = f"[EMOJI] Linux {'(Dark)' if self.dark_mode else '(Light)'}"
        
        if not hasattr(self, 'platform_label'):
            self.platform_label = QLabel(platform_text)
            self.platform_label.setProperty("class", "caption")
            self.platform_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.platform_label.setText(platform_text)
    
    def on_generate_video(self):
        """Handle generate video button click"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("[WARNING] Please enter a video prompt first", "warning")
            return
        
        self.update_status("[ACTION] Opening Advanced Studio for video generation...", "info")
        self.on_open_advanced()
    
    def on_voice_only(self):
        """Handle voice only button click"""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            self.update_status("[WARNING] Please enter a voice prompt first", "warning")
            return
        
        self.update_status("[EMOJI] Opening Advanced Studio for voice generation...", "info")
        self.on_open_advanced()
    
    def on_open_advanced(self):
        """Open advanced studio window"""
        try:
            self.advanced_window = AdvancedWindow()
            
            # Transfer prompt if available
            prompt = self.prompt_input.text().strip()
            if prompt and hasattr(self.advanced_window, 'story_input'):
                self.advanced_window.story_input.setPlainText(prompt)
            
            self.advanced_window.show()
            self.update_status("[OK] Advanced Studio opened successfully", "success")
        except Exception as e:
            self.update_status(f"[EMOJI] Error opening Advanced Studio: {str(e)}", "error")
    
    def on_voice_cloning(self):
        """Handle voice cloning button"""
        self.update_status("[USERS] Voice cloning feature - Available in Advanced Studio", "info")
        self.on_open_advanced()
    
    def on_batch_processing(self):
        """Handle batch processing button"""
        self.update_status("[EMOJI] Batch processing - Available in Advanced Studio", "info")
        self.on_open_advanced()
    
    def update_status(self, message, status_type="info"):
        """Update status message with type-specific styling"""
        self.status_label.setText(message)
        
        # Update status class for styling
        status_classes = {
            "success": "status-success",
            "warning": "status-warning", 
            "error": "status-error",
            "info": "status"
        }
        
        class_name = status_classes.get(status_type, "status")
        self.status_label.setProperty("class", class_name)
        
        # Force style update
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

# Backward compatibility alias
class MainWindow(ModernMainWindow):
    """Backward compatibility alias for ModernMainWindow"""
    pass

def main():
    """Main application entry point with cross-platform support"""
    app = QApplication(sys.argv)
    
    # Platform-specific app setup
    if platform.system() == "Darwin":
        app.setApplicationName("Voice Studio")
        app.setApplicationDisplayName("[MIC] Voice Studio")
    elif platform.system() == "Windows":
        app.setApplicationName("Voice Studio")
    
    window = ModernMainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
>>>>>>> Stashed changes
    main() 