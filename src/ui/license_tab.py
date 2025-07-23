# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
                             QMessageBox, QProgressBar, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFormLayout, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor
import sys
import os

# Import license manager  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.license_manager import license_manager

class LicenseCheckThread(QThread):
    """Thread để check license không block UI"""
    license_checked = Signal(bool, str)
    
    def __init__(self, license_key):
        super().__init__()
        self.license_key = license_key
    
    def run(self):
        try:
            success, message = license_manager.activate_license(self.license_key)
            self.license_checked.emit(success, message)
        except Exception as e:
            self.license_checked.emit(False, f"Error: {str(e)}")

class LicenseTab(QWidget):
    """Tab quản lý License cho Voice Studio"""
    
    def __init__(self):
        super().__init__()
        self.license_check_thread = None
        self.init_ui()
        self.load_license_info()
        
        # Auto refresh license info mỗi 30 giây
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_license_info)
        self.refresh_timer.start(30000)  # 30 seconds
    
    def init_ui(self):
        """Khởi tạo giao diện License tab"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # === HEADER ===
        header_layout = QHBoxLayout()
        
        # Logo và title
        title_label = QLabel("License Manager")
        title_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2E86AB;
            padding: 10px;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel(" Loading...")
        self.status_label.setStyleSheet("""
            font-size: 14px;
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            background-color: #f8f9fa;
        """)
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # === LICENSE ACTIVATION GROUP ===
        activation_group = QGroupBox(" License Activation")
        activation_layout = QVBoxLayout()
        
        # License key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("License Key:"))
        
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("VS-XXXXXXXX-XXXXXXXX-XXXXXXXX")
        key_layout.addWidget(self.license_input)
        
        # Activate button
        self.activate_btn = QPushButton(" Activate License")
        self.activate_btn.clicked.connect(self.activate_license)
        key_layout.addWidget(self.activate_btn)
        
        activation_layout.addLayout(key_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        activation_layout.addWidget(self.progress_bar)
        
        activation_group.setLayout(activation_layout)
        layout.addWidget(activation_group)
        
        # === LICENSE INFO GROUP ===
        info_group = QGroupBox(" Current License Information")
        info_layout = QVBoxLayout()
        
        # Info text area
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setReadOnly(True)
        info_layout.addWidget(self.info_text)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton(" Refresh")
        self.refresh_btn.clicked.connect(self.load_license_info)
        button_layout.addWidget(self.refresh_btn)
        
        self.deactivate_btn = QPushButton(" Deactivate")
        self.deactivate_btn.clicked.connect(self.deactivate_license)
        button_layout.addWidget(self.deactivate_btn)
        
        button_layout.addStretch()
        
        self.hardware_id_btn = QPushButton(" Show Hardware ID")
        self.hardware_id_btn.clicked.connect(self.show_hardware_id)
        button_layout.addWidget(self.hardware_id_btn)
        
        info_layout.addLayout(button_layout)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # === FEATURES TABLE ===
        features_group = QGroupBox(" Available Features")
        features_layout = QVBoxLayout()
        
        self.features_table = QTableWidget()
        self.features_table.setColumnCount(2)
        self.features_table.setHorizontalHeaderLabels(["Feature", "Status"])
        self.features_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.features_table.setAlternatingRowColors(True)
        self.features_table.setMaximumHeight(200)
        features_layout.addWidget(self.features_table)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # === TRIAL MODE INFO ===
        trial_frame = QFrame()
        trial_frame.setFrameStyle(QFrame.Box)
        trial_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 2px solid #ffeaa7;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        trial_layout = QVBoxLayout()
        
        trial_title = QLabel(" Trial Mode Information")
        trial_title.setStyleSheet("font-weight: bold; color: #856404; font-size: 14px;")
        trial_layout.addWidget(trial_title)
        
        trial_info = QLabel("""
• Basic TTS functionality is available
• Emotion preview with limited options  
• Maximum 5 exports per day in trial mode
• Get a license key to unlock all premium features
• Contact support for enterprise solutions
        """)
        trial_info.setStyleSheet("color: #856404; margin-left: 10px;")
        trial_layout.addWidget(trial_info)
        
        trial_frame.setLayout(trial_layout)
        layout.addWidget(trial_frame)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def activate_license(self):
        """Kích hoạt license key"""
        license_key = self.license_input.text().strip()
        if not license_key:
            QMessageBox.warning(self, "Warning", "Please enter a license key")
            return
        
        # Disable UI during activation
        self.activate_btn.setEnabled(False)
        self.license_input.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Start license check in background thread
        self.license_check_thread = LicenseCheckThread(license_key)
        self.license_check_thread.license_checked.connect(self.on_license_checked)
        self.license_check_thread.start()
    
    def on_license_checked(self, success, message):
        """Callback khi license check hoàn thành"""
        # Re-enable UI
        self.activate_btn.setEnabled(True)
        self.license_input.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.license_input.clear()
            self.load_license_info()
        else:
            QMessageBox.critical(self, "Activation Failed", message)
    
    def load_license_info(self):
        """Load và hiển thị thông tin license hiện tại"""
        try:
            # Try to load existing license first
            license_manager.load_current_license()
            
            license_info = license_manager.get_license_info()
            hardware_id = license_manager.get_hardware_id()
            
            # Update status label
            if license_info["status"] == "trial":
                self.status_label.setText(" Trial Mode")
            elif license_info["status"] == "valid":
                offline_text = " (Offline)" if license_info.get("offline") else ""
                self.status_label.setText(f" Licensed{offline_text}")
            else:
                self.status_label.setText(" Invalid")
            
            # Update info text
            info_text = f"""
License Status: {license_info['mode']}
Expires: {license_info['expires']}
Hardware ID: {hardware_id}

Available Features:
{chr(10).join('• ' + feature for feature in license_info['features'])}
            """.strip()
            
            self.info_text.setPlainText(info_text)
            
            # Update features table
            self.update_features_table(license_info)
            
        except Exception as e:
            self.info_text.setPlainText(f"Error loading license info: {str(e)}")
    
    def deactivate_license(self):
        """Hủy kích hoạt license"""
        reply = QMessageBox.question(
            self, 
            "Confirm Deactivation", 
            "Are you sure you want to deactivate the current license?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if license_manager.deactivate_license():
                QMessageBox.information(self, "Success", "License deactivated successfully")
                self.load_license_info()
            else:
                QMessageBox.critical(self, "Error", "Failed to deactivate license")
    
    def show_hardware_id(self):
        """Hiển thị Hardware ID"""
        hardware_id = license_manager.get_hardware_id()
        
        QMessageBox.information(
            self, 
            "Hardware ID", 
            f"Your Hardware ID:\n\n{hardware_id}"
        )
    
    def check_feature_access(self, feature_name):
        """Kiểm tra quyền truy cập tính năng"""
        return license_manager.is_feature_enabled(feature_name)
    
    def update_features_table(self, license_info):
        """Cập nhật bảng features"""
        feature_descriptions = {
            "basic_tts": "Basic Text-to-Speech",
            "emotion_config": "Emotion Configuration",
            "export_unlimited": "Unlimited Exports",
            "inner_voice": "Inner Voice Effects",
            "batch_processing": "Batch Processing",
            "api_access": "API Access",
            "export_limit_5": "Limited Exports (5/day)"
        }
        
        # Clear existing rows
        self.features_table.setRowCount(0)
        
        # Add rows for each feature
        for i, feature in enumerate(license_info['features']):
            self.features_table.insertRow(i)
            
            # Feature name
            feature_name = feature_descriptions.get(feature, feature.replace('_', ' ').title())
            self.features_table.setItem(i, 0, QTableWidgetItem(feature_name))
            
            # Status
            status_item = QTableWidgetItem("✅ Enabled")
            status_item.setBackground(QColor("#d4edda"))
            self.features_table.setItem(i, 1, status_item)
 