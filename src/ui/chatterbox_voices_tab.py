#!/usr/bin/env python3
"""
[MIC] CHATTERBOX VOICES TAB UI
===========================

Voice Studio UI component for Chatterbox TTS integration.
Provides interface for browsing and using 28 high-quality Chatterbox voices.
"""

import os
import sys
import json
from typing import Dict, List, Optional, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QPushButton, QTextEdit, QProgressBar,
    QGroupBox, QDoubleSpinBox, QSplitter, QScrollArea, 
    QFrame, QLineEdit, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

# Add src directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import TTS components
from tts.chatterbox_voices_integration import ChatterboxVoicesManager
from tts.enhanced_voice_generator import EnhancedVoiceGenerator, VoiceGenerationRequest

class VoiceCard(QFrame):
    """Individual voice card widget"""
    
    def __init__(self, voice_id: str, voice_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.voice_id = voice_id
        self.voice_info = voice_info
        self.setup_ui()
    
    def setup_ui(self):
        """Setup voice card UI"""
        self.setFrameStyle(QFrame.Box)
        self.setFixedSize(280, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Voice name và gender
        header_layout = QHBoxLayout()
        
        name_label = QLabel(self.voice_info.get("name", self.voice_id))
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_layout.addWidget(name_label)
        
        # Gender badge
        gender = self.voice_info.get("gender", "unknown")
        gender_label = QLabel(f"[USER] {gender.title()}")
        gender_label.setStyleSheet(f"""
            QLabel {{
                background-color: {'#FFE4E6' if gender == 'female' else '#E4F0FF'};
                border: 1px solid {'#FF9AA2' if gender == 'female' else '#9AB8FF'};
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
            }}
        """)
        header_layout.addWidget(gender_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(self.voice_info.get("description", "High-quality voice"))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(desc_label)
        
        # Quality và provider info
        info_layout = QHBoxLayout()
        
        quality = self.voice_info.get("quality", 8.0)
        quality_label = QLabel(f"[STAR] {quality}/10")
        quality_label.setStyleSheet("font-weight: bold; color: #FFA500;")
        info_layout.addWidget(quality_label)
        
        provider = self.voice_info.get("provider", "unknown")
        provider_label = QLabel(f"[TOOL] {provider}")
        provider_label.setStyleSheet("font-size: 10px; color: #888;")
        info_layout.addWidget(provider_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Select button
        self.select_btn = QPushButton("Select Voice")
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.select_btn)

class VoiceGenerationThread(QThread):
    """Background thread for voice generation"""
    
    progress_update = Signal(str)  # Progress message
    generation_complete = Signal(dict)  # Result dictionary
    
    def __init__(self, generator: EnhancedVoiceGenerator, request: VoiceGenerationRequest):
        super().__init__()
        self.generator = generator
        self.request = request
    
    def run(self):
        """Run voice generation in background"""
        try:
            self.progress_update.emit("[ROCKET] Starting voice generation...")
            
            # Generate voice
            result = self.generator.generate_voice(self.request)
            
            if result.success:
                self.progress_update.emit("[OK] Voice generation completed!")
            else:
                self.progress_update.emit("[EMOJI] Voice generation failed!")
            
            self.generation_complete.emit({
                "success": result.success,
                "output_path": result.output_path,
                "voice_used": result.voice_used,
                "provider_used": result.provider_used,
                "generation_time": result.generation_time,
                "quality_score": result.quality_score,
                "error_message": result.error_message
            })
            
        except Exception as e:
            self.progress_update.emit(f"[EMOJI] Generation error: {str(e)}")
            self.generation_complete.emit({
                "success": False,
                "error_message": str(e)
            })

class ChatterboxVoicesTab(QWidget):
    """
    [MIC] CHATTERBOX VOICES TAB
    
    Main UI tab for Chatterbox TTS integration với Voice Studio.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize TTS components
        self.chatterbox_manager = ChatterboxVoicesManager()
        self.voice_generator = EnhancedVoiceGenerator()
        
        # UI state
        self.selected_voice_id = "olivia"
        self.generation_thread = None
        
        self.setup_ui()
        self.load_voices()
        self.update_provider_status()
    
    def setup_ui(self):
        """Setup main UI layout"""
        layout = QHBoxLayout(self)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Voice browser
        left_panel = self.create_voice_browser()
        splitter.addWidget(left_panel)
        
        # Right panel: Generation controls
        right_panel = self.create_generation_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter sizes
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
    
    def create_voice_browser(self) -> QWidget:
        """Create voice browser panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header_label = QLabel("[MIC] Chatterbox Voices Library")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet("color: #2C3E50; margin: 10px 0;")
        layout.addWidget(header_label)
        
        # Provider status
        self.status_label = QLabel("[SEARCH] Loading providers...")
        self.status_label.setStyleSheet("color: #7F8C8D; margin-bottom: 10px;")
        layout.addWidget(self.status_label)
        
        # Filter controls
        filter_group = QGroupBox("[SEARCH] Voice Filters")
        filter_layout = QHBoxLayout(filter_group)
        
        # Gender filter
        filter_layout.addWidget(QLabel("Gender:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["All", "Female", "Male"])
        self.gender_combo.currentTextChanged.connect(self.filter_voices)
        filter_layout.addWidget(self.gender_combo)
        
        # Quality filter
        filter_layout.addWidget(QLabel("Min Quality:"))
        self.quality_spin = QDoubleSpinBox()
        self.quality_spin.setRange(7.0, 10.0)
        self.quality_spin.setValue(8.0)
        self.quality_spin.setSuffix("/10")
        self.quality_spin.valueChanged.connect(self.filter_voices)
        filter_layout.addWidget(self.quality_spin)
        
        # Character type recommendations
        filter_layout.addWidget(QLabel("Character:"))
        self.character_combo = QComboBox()
        self.character_combo.addItems([
            "All", "Narrator", "Hero", "Villain", 
            "Child", "Elderly", "Professional", "Friendly"
        ])
        self.character_combo.currentTextChanged.connect(self.recommend_voices)
        filter_layout.addWidget(self.character_combo)
        
        layout.addWidget(filter_group)
        
        # Voice cards scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.voices_container = QWidget()
        self.voices_layout = QGridLayout(self.voices_container)
        self.voices_layout.setSpacing(10)
        
        scroll.setWidget(self.voices_container)
        layout.addWidget(scroll)
        
        return widget
    
    def create_generation_panel(self) -> QWidget:
        """Create voice generation control panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Header
        header_label = QLabel("[ROCKET] Voice Generation")
        header_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_label.setStyleSheet("color: #2C3E50; margin: 10px 0;")
        layout.addWidget(header_label)
        
        # Selected voice info
        self.selected_voice_group = QGroupBox("[TARGET] Selected Voice")
        selected_layout = QVBoxLayout(self.selected_voice_group)
        
        self.selected_voice_label = QLabel("olivia (Olivia)")
        self.selected_voice_label.setFont(QFont("Arial", 12, QFont.Bold))
        selected_layout.addWidget(self.selected_voice_label)
        
        self.selected_voice_desc = QLabel("Elegant and refined female voice")
        self.selected_voice_desc.setStyleSheet("color: #666;")
        selected_layout.addWidget(self.selected_voice_desc)
        
        layout.addWidget(self.selected_voice_group)
        
        # Text input
        text_group = QGroupBox("[EDIT] Text Input")
        text_layout = QVBoxLayout(text_group)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("Hello! This is a test of the Chatterbox TTS integration with Voice Studio.")
        self.text_edit.setMaximumHeight(100)
        text_layout.addWidget(self.text_edit)
        
        layout.addWidget(text_group)
        
        # Generation parameters
        params_group = QGroupBox("[EMOJI] Generation Parameters")
        params_layout = QGridLayout(params_group)
        
        # Provider selection
        params_layout.addWidget(QLabel("Provider:"), 0, 0)
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Auto", "Chatterbox TTS", "Real Chatterbox"])
        params_layout.addWidget(self.provider_combo, 0, 1)
        
        # Emotion
        params_layout.addWidget(QLabel("Emotion:"), 1, 0)
        self.emotion_combo = QComboBox()
        self.emotion_combo.addItems([
            "neutral", "happy", "sad", "angry", 
            "excited", "calm", "whisper", "dramatic"
        ])
        params_layout.addWidget(self.emotion_combo, 1, 1)
        
        # Speed
        params_layout.addWidget(QLabel("Speed:"), 2, 0)
        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.5, 2.0)
        self.speed_spin.setValue(1.0)
        self.speed_spin.setSingleStep(0.1)
        params_layout.addWidget(self.speed_spin, 2, 1)
        
        # Temperature (for Chatterbox)
        params_layout.addWidget(QLabel("Temperature:"), 3, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.1, 1.5)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setSingleStep(0.1)
        params_layout.addWidget(self.temperature_spin, 3, 1)
        
        layout.addWidget(params_group)
        
        # Output settings
        output_group = QGroupBox("[EMOJI] Output Settings")
        output_layout = QVBoxLayout(output_group)
        
        output_path_layout = QHBoxLayout()
        self.output_path = QLineEdit("./voice_studio_output/generated_audio.wav")
        output_path_layout.addWidget(self.output_path)
        
        browse_btn = QPushButton("[FOLDER]")
        browse_btn.setMaximumWidth(40)
        browse_btn.clicked.connect(self.browse_output_path)
        output_path_layout.addWidget(browse_btn)
        
        output_layout.addLayout(output_path_layout)
        layout.addWidget(output_group)
        
        # Generate button
        self.generate_btn = QPushButton("[ROCKET] Generate Voice")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_voice)
        layout.addWidget(self.generate_btn)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        layout.addWidget(self.progress_label)
        
        layout.addStretch()
        
        return widget
    
    def load_voices(self):
        """Load and display all available voices"""
        # Get Chatterbox voices from manager
        chatterbox_voices = self.chatterbox_manager.get_available_voices()
        
        # Convert to format expected by UI
        all_voices = {}
        for voice_id, voice_obj in chatterbox_voices.items():
            all_voices[voice_id] = {
                "name": voice_obj.name,
                "gender": voice_obj.gender,
                "description": voice_obj.description,
                "quality": voice_obj.quality_rating,
                "provider": "Chatterbox TTS",
                "sample_rate": voice_obj.sample_rate,
                "language": voice_obj.language
            }
        
        self.all_voices = all_voices
        self.display_voices(all_voices)
    
    def display_voices(self, voices: Dict[str, Dict[str, Any]]):
        """Display voice cards in grid layout"""
        # Clear existing cards
        while self.voices_layout.count():
            child = self.voices_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add new voice cards
        row, col = 0, 0
        for voice_id, voice_info in voices.items():
            card = VoiceCard(voice_id, voice_info)
            card.select_btn.clicked.connect(lambda checked, vid=voice_id: self.select_voice(vid))
            
            self.voices_layout.addWidget(card, row, col)
            
            col += 1
            if col >= 2:  # 2 cards per row
                col = 0
                row += 1
    
    def filter_voices(self):
        """Filter voices based on current filter settings"""
        if not hasattr(self, 'all_voices'):
            return
        
        gender_filter = self.gender_combo.currentText().lower()
        min_quality = self.quality_spin.value()
        
        filtered_voices = {}
        for voice_id, voice_info in self.all_voices.items():
            # Gender filter
            if gender_filter != "all":
                if voice_info.get("gender", "").lower() != gender_filter:
                    continue
            
            # Quality filter
            if voice_info.get("quality", 0) < min_quality:
                continue
            
            filtered_voices[voice_id] = voice_info
        
        self.display_voices(filtered_voices)
    
    def recommend_voices(self):
        """Show recommended voices for character type"""
        character_type = self.character_combo.currentText().lower()
        
        if character_type == "all":
            self.display_voices(self.all_voices)
            return
        
        # Get recommendations
        recommended_ids = self.chatterbox_manager.get_voice_recommendations(character_type)
        
        recommended_voices = {}
        for voice_id in recommended_ids:
            if voice_id in self.all_voices:
                recommended_voices[voice_id] = self.all_voices[voice_id]
        
        self.display_voices(recommended_voices)
    
    def select_voice(self, voice_id: str):
        """Select a voice for generation"""
        self.selected_voice_id = voice_id
        
        if voice_id in self.all_voices:
            voice_info = self.all_voices[voice_id]
            self.selected_voice_label.setText(f"{voice_id} ({voice_info.get('name', voice_id)})")
            self.selected_voice_desc.setText(voice_info.get('description', 'High-quality voice'))
        
        self.progress_label.setText(f"[OK] Selected: {voice_id}")
    
    def browse_output_path(self):
        """Browse for output file path"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Audio File",
            self.output_path.text(),
            "Audio Files (*.wav *.mp3)"
        )
        
        if file_path:
            self.output_path.setText(file_path)
    
    def generate_voice(self):
        """Start voice generation"""
        if self.generation_thread and self.generation_thread.isRunning():
            QMessageBox.warning(self, "Generation in Progress", "Please wait for current generation to complete.")
            return
        
        # Prepare generation request
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "No Text", "Please enter text to generate.")
            return
        
        # Map provider selection
        provider_map = {
            "Auto": "auto",
            "Chatterbox TTS": "chatterbox", 
            "Real Chatterbox": "real_chatterbox"
        }
        
        request = VoiceGenerationRequest(
            text=text,
            character_id="voice_studio_user",
            voice_provider=provider_map[self.provider_combo.currentText()],
            voice_id=self.selected_voice_id,
            emotion=self.emotion_combo.currentText(),
            speed=self.speed_spin.value(),
            output_path=self.output_path.text(),
            temperature=self.temperature_spin.value(),
            exaggeration=1.2 if self.emotion_combo.currentText() != "neutral" else 1.0
        )
        
        # Start generation
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        self.generation_thread = VoiceGenerationThread(self.voice_generator, request)
        self.generation_thread.progress_update.connect(self.update_progress)
        self.generation_thread.generation_complete.connect(self.on_generation_complete)
        self.generation_thread.start()
    
    def update_progress(self, message: str):
        """Update progress display"""
        self.progress_label.setText(message)
    
    def on_generation_complete(self, result: Dict[str, Any]):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result["success"]:
            msg = f"[OK] Voice generated successfully!\n\n"
            msg += f"[MIC] Voice: {result['voice_used']}\n"
            msg += f"[TOOL] Provider: {result['provider_used']}\n"
            msg += f"⏱ Time: {result['generation_time']:.2f}s\n"
            msg += f"[STAR] Quality: {result['quality_score']}/10\n"
            msg += f"[FOLDER] Saved to: {result['output_path']}"
            
            QMessageBox.information(self, "Generation Complete", msg)
            self.progress_label.setText("[OK] Generation completed!")
        else:
            QMessageBox.critical(
                self, 
                "Generation Failed", 
                f"[EMOJI] Voice generation failed:\n\n{result.get('error_message', 'Unknown error')}"
            )
            self.progress_label.setText("[EMOJI] Generation failed!")
    
    def update_provider_status(self):
        """Update provider status display"""
        status = self.voice_generator.get_provider_status()
        
        status_text = "[STATS] Providers: "
        for provider, info in status.items():
            icon = "[OK]" if info["available"] else "[EMOJI]"
            status_text += f"{icon} {provider} ({info['voices_count']}) "
        
        self.status_label.setText(status_text)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create and show tab
    tab = ChatterboxVoicesTab()
    tab.setWindowTitle("[MIC] Chatterbox Voices - Voice Studio")
    tab.resize(1200, 800)
    tab.show()
    
    sys.exit(app.exec()) 