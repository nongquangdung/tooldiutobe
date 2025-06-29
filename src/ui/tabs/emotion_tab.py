from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QScrollArea, QSlider, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt

class EmotionTab(QWidget):
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
        
        # Emotion selection group
        emotion_group = QGroupBox("Emotion Selection")
        emotion_layout = QVBoxLayout()
        
        # Primary emotion
        primary_layout = QHBoxLayout()
        primary_layout.addWidget(QLabel("Primary Emotion:"))
        self.primary_emotion = QComboBox()
        self.primary_emotion.addItems([
            "Happy", "Sad", "Angry", "Surprised",
            "Fearful", "Disgusted", "Neutral"
        ])
        primary_layout.addWidget(self.primary_emotion)
        emotion_layout.addLayout(primary_layout)
        
        # Intensity control
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(QLabel("Intensity:"))
        self.intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.intensity_slider.setRange(0, 100)
        self.intensity_slider.setValue(50)
        intensity_layout.addWidget(self.intensity_slider)
        self.intensity_spin = QSpinBox()
        self.intensity_spin.setRange(0, 100)
        self.intensity_spin.setValue(50)
        intensity_layout.addWidget(self.intensity_spin)
        emotion_layout.addLayout(intensity_layout)
        
        emotion_group.setLayout(emotion_layout)
        content_layout.addWidget(emotion_group)
        
        # Voice effects group
        effects_group = QGroupBox("Voice Effects")
        effects_layout = QVBoxLayout()
        
        # Pitch variation
        pitch_var_layout = QHBoxLayout()
        pitch_var_layout.addWidget(QLabel("Pitch Variation:"))
        self.pitch_var_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_var_slider.setRange(0, 100)
        self.pitch_var_slider.setValue(20)
        pitch_var_layout.addWidget(self.pitch_var_slider)
        self.pitch_var_spin = QSpinBox()
        self.pitch_var_spin.setRange(0, 100)
        self.pitch_var_spin.setValue(20)
        pitch_var_layout.addWidget(self.pitch_var_spin)
        effects_layout.addLayout(pitch_var_layout)
        
        # Speed variation
        speed_var_layout = QHBoxLayout()
        speed_var_layout.addWidget(QLabel("Speed Variation:"))
        self.speed_var_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_var_slider.setRange(0, 100)
        self.speed_var_slider.setValue(20)
        speed_var_layout.addWidget(self.speed_var_slider)
        self.speed_var_spin = QSpinBox()
        self.speed_var_spin.setRange(0, 100)
        self.speed_var_spin.setValue(20)
        speed_var_layout.addWidget(self.speed_var_spin)
        effects_layout.addLayout(speed_var_layout)
        
        effects_group.setLayout(effects_layout)
        content_layout.addWidget(effects_group)
        
        # Add stretch to push everything up
        content_layout.addStretch()
        
        # Connect signals
        self.intensity_slider.valueChanged.connect(self.intensity_spin.setValue)
        self.intensity_spin.valueChanged.connect(self.intensity_slider.setValue)
        self.pitch_var_slider.valueChanged.connect(self.pitch_var_spin.setValue)
        self.pitch_var_spin.valueChanged.connect(self.pitch_var_slider.setValue)
        self.speed_var_slider.valueChanged.connect(self.speed_var_spin.setValue)
        self.speed_var_spin.valueChanged.connect(self.speed_var_slider.setValue)
    
    def get_emotion_settings(self):
        """Get current emotion settings"""
        return {
            'primary_emotion': self.primary_emotion.currentText(),
            'intensity': self.intensity_spin.value() / 100.0,
            'pitch_variation': self.pitch_var_spin.value() / 100.0,
            'speed_variation': self.speed_var_spin.value() / 100.0
        } 