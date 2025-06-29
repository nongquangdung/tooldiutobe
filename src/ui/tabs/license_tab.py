from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QScrollArea, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from core.license_manager import LicenseManager

class LicenseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.license_manager = LicenseManager()
        self.setup_ui()
        self.update_license_status()
    
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
        
        # License status group
        status_group = QGroupBox("License Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel()
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        content_layout.addWidget(status_group)
        
        # License activation group
        activation_group = QGroupBox("License Activation")
        activation_layout = QVBoxLayout()
        
        # License key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("License Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter your license key")
        key_layout.addWidget(self.key_input)
        activation_layout.addLayout(key_layout)
        
        # Activation button
        self.activate_btn = QPushButton("Activate License")
        self.activate_btn.clicked.connect(self.activate_license)
        activation_layout.addWidget(self.activate_btn)
        
        activation_group.setLayout(activation_layout)
        content_layout.addWidget(activation_group)
        
        # Add stretch to push everything up
        content_layout.addStretch()
    
    def update_license_status(self):
        """Update the license status display"""
        try:
            status = self.license_manager.check_license()
            if status['valid']:
                self.status_label.setText(
                    f"✅ Licensed to: {status['user']}\n"
                    f"Expires: {status['expiry_date']}\n"
                    f"Features: {', '.join(status['features'])}"
                )
                self.activate_btn.setEnabled(False)
                self.key_input.setEnabled(False)
            else:
                self.status_label.setText("❌ No valid license found")
                self.activate_btn.setEnabled(True)
                self.key_input.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"⚠️ Error checking license: {str(e)}")
            self.activate_btn.setEnabled(True)
            self.key_input.setEnabled(True)
    
    def activate_license(self):
        """Attempt to activate the license"""
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Error", "Please enter a license key")
            return
            
        try:
            result = self.license_manager.activate_license(key)
            if result['success']:
                QMessageBox.information(self, "Success", "License activated successfully!")
                self.update_license_status()
            else:
                QMessageBox.warning(self, "Error", f"Failed to activate license: {result['message']}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error activating license: {str(e)}") 