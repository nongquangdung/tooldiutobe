from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QScrollArea, QListWidget, QListWidgetItem,
    QMessageBox, QMenu, QInputDialog
)
from PySide6.QtCore import Qt
import os
import shutil

class ProjectsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_projects()
    
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
        
        # Projects list group
        projects_group = QGroupBox("Danh sách Dự án")
        projects_layout = QVBoxLayout()
        
        self.projects_list = QListWidget()
        self.projects_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.projects_list.customContextMenuRequested.connect(self.show_context_menu)
        projects_layout.addWidget(self.projects_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Làm mới")
        self.refresh_btn.clicked.connect(self.load_projects)
        buttons_layout.addWidget(self.refresh_btn)
        
        self.import_btn = QPushButton("📥 Nhập dự án")
        self.import_btn.clicked.connect(self.import_project)
        buttons_layout.addWidget(self.import_btn)
        
        projects_layout.addLayout(buttons_layout)
        projects_group.setLayout(projects_layout)
        content_layout.addWidget(projects_group)
        
        # Project details group
        details_group = QGroupBox("Chi tiết Dự án")
        details_layout = QVBoxLayout()
        
        self.details_label = QLabel("Chọn một dự án để xem chi tiết")
        details_layout.addWidget(self.details_label)
        
        details_group.setLayout(details_layout)
        content_layout.addWidget(details_group)
        
        # Add stretch to push everything up
        content_layout.addStretch()
        
        # Connect signals
        self.projects_list.itemSelectionChanged.connect(self.update_project_details)
    
    def load_projects(self):
        """Load all projects from the projects directory"""
        try:
            self.projects_list.clear()
            projects_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'projects')
            
            if not os.path.exists(projects_dir):
                os.makedirs(projects_dir)
                return
            
            for project in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project)
                if os.path.isdir(project_path):
                    item = QListWidgetItem(project)
                    item.setData(Qt.ItemDataRole.UserRole, project_path)
                    self.projects_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể tải danh sách dự án: {str(e)}")
    
    def update_project_details(self):
        """Update project details when selection changes"""
        items = self.projects_list.selectedItems()
        if not items:
            self.details_label.setText("Chọn một dự án để xem chi tiết")
            return
        
        project_path = items[0].data(Qt.ItemDataRole.UserRole)
        try:
            # Count files and get total size
            file_count = 0
            total_size = 0
            for root, _, files in os.walk(project_path):
                file_count += len(files)
                total_size += sum(os.path.getsize(os.path.join(root, f)) for f in files)
            
            # Format size
            size_str = self.format_size(total_size)
            
            # Get creation time
            created = os.path.getctime(project_path)
            from datetime import datetime
            created_str = datetime.fromtimestamp(created).strftime('%d/%m/%Y %H:%M:%S')
            
            self.details_label.setText(
                f"Tên dự án: {items[0].text()}\n"
                f"Đường dẫn: {project_path}\n"
                f"Số file: {file_count}\n"
                f"Dung lượng: {size_str}\n"
                f"Ngày tạo: {created_str}"
            )
        except Exception as e:
            self.details_label.setText(f"Lỗi khi tải chi tiết dự án: {str(e)}")
    
    def show_context_menu(self, position):
        """Show context menu for project item"""
        items = self.projects_list.selectedItems()
        if not items:
            return
        
        menu = QMenu()
        open_action = menu.addAction("📂 Mở thư mục")
        rename_action = menu.addAction("✏️ Đổi tên")
        export_action = menu.addAction("📤 Xuất dự án")
        delete_action = menu.addAction("🗑️ Xóa")
        
        action = menu.exec(self.projects_list.mapToGlobal(position))
        if not action:
            return
        
        project_path = items[0].data(Qt.ItemDataRole.UserRole)
        project_name = items[0].text()
        
        if action == open_action:
            self.open_project_folder(project_path)
        elif action == rename_action:
            self.rename_project(project_path, project_name)
        elif action == export_action:
            self.export_project(project_path, project_name)
        elif action == delete_action:
            self.delete_project(project_path, project_name)
    
    def open_project_folder(self, path):
        """Open project folder in file explorer"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể mở thư mục dự án: {str(e)}")
    
    def rename_project(self, path, old_name):
        """Rename a project"""
        new_name, ok = QInputDialog.getText(
            self, "Đổi tên dự án",
            "Nhập tên mới cho dự án:",
            text=old_name
        )
        
        if not ok or not new_name or new_name == old_name:
            return
        
        try:
            new_path = os.path.join(os.path.dirname(path), new_name)
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Lỗi", "Dự án với tên này đã tồn tại")
                return
            
            os.rename(path, new_path)
            self.load_projects()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể đổi tên dự án: {str(e)}")
    
    def export_project(self, path, name):
        """Export a project to a zip file"""
        try:
            from datetime import datetime
            export_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            export_path = QFileDialog.getSaveFileName(
                self, "Xuất dự án",
                export_name,
                "Zip files (*.zip)"
            )[0]
            
            if not export_path:
                return
            
            shutil.make_archive(
                os.path.splitext(export_path)[0],
                'zip',
                path
            )
            
            QMessageBox.information(self, "Thành công", "Dự án đã được xuất thành công")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xuất dự án: {str(e)}")
    
    def delete_project(self, path, name):
        """Delete a project"""
        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa dự án '{name}'?\n"
            "Hành động này không thể hoàn tác!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                shutil.rmtree(path)
                self.load_projects()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Không thể xóa dự án: {str(e)}")
    
    def import_project(self):
        """Import a project from a zip file"""
        try:
            import_path = QFileDialog.getOpenFileName(
                self, "Nhập dự án",
                "",
                "Zip files (*.zip)"
            )[0]
            
            if not import_path:
                return
            
            # Get project name from zip file
            import zipfile
            with zipfile.ZipFile(import_path, 'r') as zip_ref:
                # Get the common prefix of all files in the zip
                paths = zip_ref.namelist()
                if not paths:
                    raise Exception("File zip rỗng")
                
                # Use the first directory name as project name
                project_name = paths[0].split('/')[0]
                if not project_name:
                    project_name = os.path.splitext(os.path.basename(import_path))[0]
            
            # Check if project already exists
            projects_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'projects')
            project_path = os.path.join(projects_dir, project_name)
            
            if os.path.exists(project_path):
                reply = QMessageBox.question(
                    self, "Dự án đã tồn tại",
                    f"Dự án '{project_name}' đã tồn tại. Bạn có muốn ghi đè không?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    return
                
                shutil.rmtree(project_path)
            
            # Extract zip file
            with zipfile.ZipFile(import_path, 'r') as zip_ref:
                zip_ref.extractall(projects_dir)
            
            self.load_projects()
            QMessageBox.information(self, "Thành công", "Dự án đã được nhập thành công")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể nhập dự án: {str(e)}")
    
    @staticmethod
    def format_size(size):
        """Format file size to human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"