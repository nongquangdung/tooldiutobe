"""
Quality Control Tab - PHASE 3 UI Component
Professional quality control dashboard với real-time metrics,
candidate comparison, và validation controls.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QPushButton,
    QProgressBar, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QTabWidget, QFrame, QScrollArea,
    QCheckBox, QSlider, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QPalette
import json
import os


class QualityMetricsWidget(QWidget):
    """Real-time quality metrics display"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Mock data for demo
        self.metrics = {
            'success_rate': 0.92,
            'avg_quality_score': 0.87,
            'avg_candidates_needed': 2.3,
            'total_tasks': 156
        }
    
    def setup_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Success Rate
        success_group = QGroupBox("🎯 Success Rate")
        success_layout = QVBoxLayout()
        self.success_rate_label = QLabel("92.0%")
        self.success_rate_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #27AE60;")
        self.success_rate_progress = QProgressBar()
        self.success_rate_progress.setValue(92)
        success_layout.addWidget(self.success_rate_label)
        success_layout.addWidget(self.success_rate_progress)
        success_group.setLayout(success_layout)
        layout.addWidget(success_group, 0, 0)
        
        # Average Quality Score
        quality_group = QGroupBox("📊 Avg Quality Score")
        quality_layout = QVBoxLayout()
        self.quality_score_label = QLabel("0.87")
        self.quality_score_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498DB;")
        self.quality_score_progress = QProgressBar()
        self.quality_score_progress.setValue(87)
        quality_layout.addWidget(self.quality_score_label)
        quality_layout.addWidget(self.quality_score_progress)
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group, 0, 1)
        
        # Candidates Needed
        candidates_group = QGroupBox("🔄 Avg Candidates Needed")
        candidates_layout = QVBoxLayout()
        self.candidates_label = QLabel("2.3")
        self.candidates_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #E67E22;")
        candidates_layout.addWidget(self.candidates_label)
        candidates_group.setLayout(candidates_layout)
        layout.addWidget(candidates_group, 0, 2)
        
        # Total Tasks
        tasks_group = QGroupBox("📋 Total Tasks")
        tasks_layout = QVBoxLayout()
        self.tasks_label = QLabel("156")
        self.tasks_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #9B59B6;")
        tasks_layout.addWidget(self.tasks_label)
        tasks_group.setLayout(tasks_layout)
        layout.addWidget(tasks_group, 0, 3)
    
    def update_metrics(self, metrics):
        """Update metrics display"""
        self.metrics.update(metrics)
        
        success_rate = self.metrics['success_rate'] * 100
        self.success_rate_label.setText(f"{success_rate:.1f}%")
        self.success_rate_progress.setValue(int(success_rate))
        
        quality_score = self.metrics['avg_quality_score']
        self.quality_score_label.setText(f"{quality_score:.3f}")
        self.quality_score_progress.setValue(int(quality_score * 100))
        
        self.candidates_label.setText(f"{self.metrics['avg_candidates_needed']:.1f}")
        self.tasks_label.setText(str(self.metrics['total_tasks']))


class QualityConfigWidget(QWidget):
    """Quality control configuration"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Quality Threshold
        threshold_group = QGroupBox("🎯 Quality Control Settings")
        threshold_layout = QGridLayout()
        
        threshold_layout.addWidget(QLabel("Quality Threshold:"), 0, 0)
        self.quality_threshold_spin = QDoubleSpinBox()
        self.quality_threshold_spin.setRange(0.5, 1.0)
        self.quality_threshold_spin.setSingleStep(0.05)
        self.quality_threshold_spin.setValue(0.85)
        self.quality_threshold_spin.setDecimals(2)
        threshold_layout.addWidget(self.quality_threshold_spin, 0, 1)
        
        threshold_layout.addWidget(QLabel("Number of Candidates:"), 1, 0)
        self.num_candidates_spin = QSpinBox()
        self.num_candidates_spin.setRange(2, 10)
        self.num_candidates_spin.setValue(5)
        threshold_layout.addWidget(self.num_candidates_spin, 1, 1)
        
        threshold_layout.addWidget(QLabel("Max Retries:"), 2, 0)
        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(3, 15)
        self.max_retries_spin.setValue(8)
        threshold_layout.addWidget(self.max_retries_spin, 2, 1)
        
        threshold_layout.addWidget(QLabel("Whisper Model:"), 3, 0)
        self.whisper_model_combo = QComboBox()
        self.whisper_model_combo.addItems(["base", "small", "medium", "large"])
        self.whisper_model_combo.setCurrentText("base")
        threshold_layout.addWidget(self.whisper_model_combo, 3, 1)
        
        threshold_group.setLayout(threshold_layout)
        layout.addWidget(threshold_group)
        
        # Quality Metrics Weights
        weights_group = QGroupBox("⚖️ Quality Metrics Weights")
        weights_layout = QGridLayout()
        
        metrics = [
            ("Transcription Accuracy", 0.40),
            ("Audio Clarity", 0.25),
            ("Speech Naturalness", 0.15),
            ("Emotional Consistency", 0.15),
            ("Technical Quality", 0.05)
        ]
        
        self.weight_sliders = {}
        
        for i, (metric, default_weight) in enumerate(metrics):
            weights_layout.addWidget(QLabel(f"{metric}:"), i, 0)
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(int(default_weight * 100))
            self.weight_sliders[metric] = slider
            weights_layout.addWidget(slider, i, 1)
            
            weight_label = QLabel(f"{default_weight:.2f}")
            slider.valueChanged.connect(lambda v, label=weight_label: label.setText(f"{v/100:.2f}"))
            weights_layout.addWidget(weight_label, i, 2)
        
        weights_group.setLayout(weights_layout)
        layout.addWidget(weights_group)
    
    def get_quality_settings(self):
        """Get current quality control settings"""
        weights = {metric: slider.value() / 100 for metric, slider in self.weight_sliders.items()}
        
        return {
            'quality_threshold': self.quality_threshold_spin.value(),
            'num_candidates': self.num_candidates_spin.value(),
            'max_retries': self.max_retries_spin.value(),
            'whisper_model': self.whisper_model_combo.currentText(),
            'metric_weights': weights
        }


class CandidateComparisonWidget(QWidget):
    """Candidate comparison và selection"""
    
    def __init__(self):
        super().__init__()
        self.candidates = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Candidates Table
        self.candidates_table = QTableWidget()
        self.candidates_table.setColumnCount(7)
        self.candidates_table.setHorizontalHeaderLabels([
            "Candidate ID", "Overall Score", "Transcription", "Audio Clarity", 
            "Naturalness", "Emotional", "Technical"
        ])
        
        # Mock data
        self.populate_mock_candidates()
        
        layout.addWidget(self.candidates_table)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.select_best_btn = QPushButton("🎯 Select Best")
        self.select_best_btn.clicked.connect(self.select_best_candidate)
        buttons_layout.addWidget(self.select_best_btn)
        
        self.listen_candidate_btn = QPushButton("🎵 Listen to Selected")
        self.listen_candidate_btn.clicked.connect(self.listen_to_candidate)
        buttons_layout.addWidget(self.listen_candidate_btn)
        
        self.regenerate_btn = QPushButton("🔄 Regenerate Candidates")
        self.regenerate_btn.clicked.connect(self.regenerate_candidates)
        buttons_layout.addWidget(self.regenerate_btn)
        
        layout.addLayout(buttons_layout)
    
    def populate_mock_candidates(self):
        """Populate table với mock candidate data"""
        mock_candidates = [
            {"id": "candidate_1", "overall": 0.92, "transcription": 0.95, "clarity": 0.88, "naturalness": 0.90, "emotional": 0.94, "technical": 0.87},
            {"id": "candidate_2", "overall": 0.87, "transcription": 0.89, "clarity": 0.85, "naturalness": 0.88, "emotional": 0.85, "technical": 0.90},
            {"id": "candidate_3", "overall": 0.84, "transcription": 0.86, "clarity": 0.82, "naturalness": 0.85, "emotional": 0.80, "technical": 0.88},
            {"id": "candidate_4", "overall": 0.79, "transcription": 0.81, "clarity": 0.78, "naturalness": 0.82, "emotional": 0.75, "technical": 0.85},
            {"id": "candidate_5", "overall": 0.76, "transcription": 0.78, "clarity": 0.75, "naturalness": 0.79, "emotional": 0.72, "technical": 0.82}
        ]
        
        self.candidates_table.setRowCount(len(mock_candidates))
        
        for row, candidate in enumerate(mock_candidates):
            self.candidates_table.setItem(row, 0, QTableWidgetItem(candidate["id"]))
            
            # Color-code based on score
            overall_score = candidate["overall"]
            if overall_score >= 0.9:
                color = QColor(39, 174, 96)  # Green
            elif overall_score >= 0.8:
                color = QColor(52, 152, 219)  # Blue  
            elif overall_score >= 0.7:
                color = QColor(230, 126, 34)  # Orange
            else:
                color = QColor(231, 76, 60)  # Red
            
            score_item = QTableWidgetItem(f"{overall_score:.3f}")
            score_item.setBackground(color)
            self.candidates_table.setItem(row, 1, score_item)
            
            # Other scores
            self.candidates_table.setItem(row, 2, QTableWidgetItem(f"{candidate['transcription']:.3f}"))
            self.candidates_table.setItem(row, 3, QTableWidgetItem(f"{candidate['clarity']:.3f}"))
            self.candidates_table.setItem(row, 4, QTableWidgetItem(f"{candidate['naturalness']:.3f}"))
            self.candidates_table.setItem(row, 5, QTableWidgetItem(f"{candidate['emotional']:.3f}"))
            self.candidates_table.setItem(row, 6, QTableWidgetItem(f"{candidate['technical']:.3f}"))
    
    def select_best_candidate(self):
        """Select best candidate automatically"""
        if self.candidates_table.rowCount() > 0:
            self.candidates_table.selectRow(0)  # Best candidate is first
            QMessageBox.information(self, "Selection", "Best candidate selected!")
    
    def listen_to_candidate(self):
        """Listen to selected candidate"""
        current_row = self.candidates_table.currentRow()
        if current_row >= 0:
            candidate_id = self.candidates_table.item(current_row, 0).text()
            QMessageBox.information(self, "Audio Playback", f"Playing audio for {candidate_id}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a candidate first.")
    
    def regenerate_candidates(self):
        """Regenerate candidates"""
        QMessageBox.information(self, "Regeneration", "Regenerating candidates with current settings...")


class QualityTab(QWidget):
    """Main Quality Control Tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_metrics)
        self.refresh_timer.start(5000)  # Update every 5 seconds
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header_label = QLabel("🎯 QUALITY CONTROL DASHBOARD")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin: 10px;")
        layout.addWidget(header_label)
        
        # Tab widget for different sections
        tab_widget = QTabWidget()
        
        # Metrics Tab
        metrics_tab = QWidget()
        metrics_layout = QVBoxLayout()
        
        self.metrics_widget = QualityMetricsWidget()
        metrics_layout.addWidget(self.metrics_widget)
        
        # Real-time log
        log_group = QGroupBox("📋 Real-time Quality Log")
        log_layout = QVBoxLayout()
        self.quality_log = QTextEdit()
        self.quality_log.setMaximumHeight(200)
        self.quality_log.setPlainText(
            "2024-01-15 10:30:15 - ✅ Task demo_001: Generated 5 candidates, best score: 0.92\n"
            "2024-01-15 10:30:32 - ✅ Task demo_002: Generated 3 candidates, best score: 0.87\n"
            "2024-01-15 10:30:45 - ⚠️ Task demo_003: Quality threshold not met, retrying...\n"
            "2024-01-15 10:30:58 - ✅ Task demo_003: Generated 7 candidates, best score: 0.89\n"
        )
        log_layout.addWidget(self.quality_log)
        log_group.setLayout(log_layout)
        metrics_layout.addWidget(log_group)
        
        metrics_tab.setLayout(metrics_layout)
        tab_widget.addTab(metrics_tab, "📊 Metrics")
        
        # Configuration Tab
        config_tab = QWidget()
        config_layout = QVBoxLayout()
        
        self.config_widget = QualityConfigWidget()
        config_layout.addWidget(self.config_widget)
        
        # Apply button
        apply_btn = QPushButton("✅ Apply Quality Settings")
        apply_btn.clicked.connect(self.apply_quality_settings)
        config_layout.addWidget(apply_btn)
        
        config_tab.setLayout(config_layout)
        tab_widget.addTab(config_tab, "⚙️ Configuration")
        
        # Candidates Tab
        candidates_tab = QWidget()
        candidates_layout = QVBoxLayout()
        
        self.candidates_widget = CandidateComparisonWidget()
        candidates_layout.addWidget(self.candidates_widget)
        
        candidates_tab.setLayout(candidates_layout)
        tab_widget.addTab(candidates_tab, "🔍 Candidates")
        
        layout.addWidget(tab_widget)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Status: Quality Control System Active")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        self.whisper_status_label = QLabel("🎤 Whisper: Ready")
        status_layout.addWidget(self.whisper_status_label)
        
        self.controller_status_label = QLabel("🎯 Controller: Active")
        status_layout.addWidget(self.controller_status_label)
        
        layout.addLayout(status_layout)
    
    def refresh_metrics(self):
        """Refresh metrics display"""
        # Mock updated metrics
        import random
        updated_metrics = {
            'success_rate': min(1.0, self.metrics_widget.metrics['success_rate'] + random.uniform(-0.02, 0.02)),
            'avg_quality_score': min(1.0, self.metrics_widget.metrics['avg_quality_score'] + random.uniform(-0.01, 0.01)),
            'avg_candidates_needed': max(1.0, self.metrics_widget.metrics['avg_candidates_needed'] + random.uniform(-0.1, 0.1)),
            'total_tasks': self.metrics_widget.metrics['total_tasks'] + random.randint(0, 2)
        }
        
        self.metrics_widget.update_metrics(updated_metrics)
    
    def apply_quality_settings(self):
        """Apply quality control settings"""
        settings = self.config_widget.get_quality_settings()
        
        QMessageBox.information(
            self, 
            "Settings Applied", 
            f"Quality control settings updated:\n"
            f"• Quality Threshold: {settings['quality_threshold']:.2f}\n"
            f"• Candidates: {settings['num_candidates']}\n"
            f"• Max Retries: {settings['max_retries']}\n"
            f"• Whisper Model: {settings['whisper_model']}"
        )
        
        # Add log entry
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - ⚙️ Quality settings updated: threshold={settings['quality_threshold']:.2f}\n"
        self.quality_log.append(log_entry)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    window = QualityTab()
    window.show()
    
    sys.exit(app.exec())
