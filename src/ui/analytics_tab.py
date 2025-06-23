#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 VOICE STUDIO ANALYTICS TAB - PHASE 4
Professional analytics dashboard với real-time metrics,
production reports, performance analysis, và ROI tracking.
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
from datetime import datetime

class MetricsCard(QFrame):
    """Professional metrics display card"""
    
    def __init__(self, title: str, value: str, subtitle: str = "", icon: str = "📊"):
        super().__init__()
        self.setup_ui(title, value, subtitle, icon)
    
    def setup_ui(self, title: str, value: str, subtitle: str, icon: str):
        """Setup metrics card UI"""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                margin: 4px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #495057;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #212529;")
        layout.addWidget(self.value_label)
        
        # Subtitle
        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet("color: #6c757d; font-size: 12px;")
            layout.addWidget(self.subtitle_label)
    
    def update_value(self, new_value: str, new_subtitle: str = ""):
        """Update card values"""
        self.value_label.setText(new_value)
        if hasattr(self, 'subtitle_label') and new_subtitle:
            self.subtitle_label.setText(new_subtitle)

class AnalyticsTab(QWidget):
    """Main analytics tab widget"""
    
    analytics_updated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup analytics dashboard UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📊 Voice Studio Analytics Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 16px;")
        layout.addWidget(title)
        
        # Metrics cards
        metrics_layout = QHBoxLayout()
        
        self.files_card = MetricsCard("Files Processed", "0", "Total today", "📁")
        self.success_card = MetricsCard("Success Rate", "0%", "Last 24 hours", "✅")
        self.quality_card = MetricsCard("Avg Quality", "0.00", "Quality score", "⭐")
        self.roi_card = MetricsCard("ROI", "0%", "Return on investment", "💰")
        
        metrics_layout.addWidget(self.files_card)
        metrics_layout.addWidget(self.success_card)
        metrics_layout.addWidget(self.quality_card)
        metrics_layout.addWidget(self.roi_card)
        
        layout.addLayout(metrics_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.new_session_btn = QPushButton("🔄 Start New Session")
        self.new_session_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)
        self.new_session_btn.clicked.connect(self.start_new_session)
        
        self.export_btn = QPushButton("📄 Export Report")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1e7e34; }
        """)
        self.export_btn.clicked.connect(self.export_report)
        
        controls_layout.addWidget(self.new_session_btn)
        controls_layout.addWidget(self.export_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Insights
        insights_title = QLabel("💡 Insights & Recommendations")
        insights_title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 8px;")
        layout.addWidget(insights_title)
        
        self.insights_text = QTextEdit()
        self.insights_text.setMaximumHeight(150)
        self.insights_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        self.insights_text.setPlainText("📊 Analytics insights will appear here...")
        layout.addWidget(self.insights_text)
        
        # Status
        self.status_label = QLabel("📊 Ready - Waiting for analytics data...")
        self.status_label.setStyleSheet("background-color: #e9ecef; padding: 8px; border-radius: 4px;")
        layout.addWidget(self.status_label)
    
    def start_new_session(self):
        """Start new analytics session"""
        self.status_label.setText("🔄 Starting new analytics session...")
        self.files_card.update_value("0", "Session restarted")
        self.success_card.update_value("0%", "No data yet")
        self.quality_card.update_value("0.00", "No data yet")
        self.roi_card.update_value("0%", "No data yet")
        self.insights_text.setPlainText("🔄 New session started...")
        
        self.analytics_updated.emit({'action': 'new_session', 'timestamp': datetime.now().isoformat()})
    
    def export_report(self):
        """Export analytics report"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Analytics Report",
            f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if filename:
            try:
                report_data = {
                    'timestamp': datetime.now().isoformat(),
                    'metrics': {
                        'files_processed': self.files_card.value_label.text(),
                        'success_rate': self.success_card.value_label.text(),
                        'avg_quality': self.quality_card.value_label.text(),
                        'roi': self.roi_card.value_label.text()
                    },
                    'insights': self.insights_text.toPlainText()
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
                
                self.status_label.setText(f"✅ Report exported: {filename}")
            except Exception as e:
                self.status_label.setText(f"❌ Export failed: {str(e)}")
    
    def update_production_metrics(self, files_processed: int, success_rate: float, 
                                 avg_quality: float, roi_percentage: float):
        """Update production metrics display"""
        self.files_card.update_value(str(files_processed), f"Updated {datetime.now().strftime('%H:%M')}")
        self.success_card.update_value(f"{success_rate:.1f}%", "Real-time data")
        self.quality_card.update_value(f"{avg_quality:.2f}", "Average score")
        self.roi_card.update_value(f"{roi_percentage:.1f}%", "Performance ROI")
        
        # Update insights
        insights = []
        if success_rate > 90:
            insights.append("✅ Excellent success rate - system performing optimally")
        elif success_rate > 75:
            insights.append("📈 Good success rate - minor optimizations possible")
        else:
            insights.append("⚠️ Success rate below target - review quality settings")
        
        if avg_quality > 0.9:
            insights.append("⭐ Outstanding audio quality maintained")
        elif avg_quality > 0.8:
            insights.append("👍 Good audio quality - meeting standards")
        else:
            insights.append("🔧 Audio quality needs improvement")
        
        if roi_percentage > 200:
            insights.append("💰 Excellent ROI - significant time savings achieved")
        
        self.insights_text.setPlainText('\n'.join(insights))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    tab = AnalyticsTab()
    tab.show()
    
    sys.exit(app.exec()) 