import json
import os
from datetime import datetime
from pathlib import Path

class ProjectManager:
    def __init__(self, projects_dir="projects"):
        self.projects_dir = projects_dir
        Path(self.projects_dir).mkdir(exist_ok=True)
    
    def create_project(self, name, prompt):
        """Tạo project mới"""
        project_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_dir = os.path.join(self.projects_dir, project_id)
        Path(project_dir).mkdir(exist_ok=True)
        
        # Tạo các thư mục con
        for subdir in ['images', 'audio', 'videos', 'segments']:
            Path(os.path.join(project_dir, subdir)).mkdir(exist_ok=True)
        
        # Tạo file project.json
        project_data = {
            "id": project_id,
            "name": name,
            "prompt": prompt,
            "created_at": datetime.now().isoformat(),
            "segments": [],
            "status": "created",
            "settings": {
                "video_resolution": "1920x1080",
                "fps": 25,
                "effects": {"zoom": True, "transitions": True}
            }
        }
        
        project_file = os.path.join(project_dir, "project.json")
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        return {"success": True, "project_id": project_id, "project_dir": project_dir}
    
    def load_project(self, project_id):
        """Tải project từ file"""
        project_file = os.path.join(self.projects_dir, project_id, "project.json")
        if not os.path.exists(project_file):
            return {"success": False, "error": "Project không tồn tại"}
        
        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            return {"success": True, "data": project_data}
        except Exception as e:
            return {"success": False, "error": f"Lỗi tải project: {str(e)}"}
    
    def save_project(self, project_id, project_data):
        """Lưu project"""
        project_file = os.path.join(self.projects_dir, project_id, "project.json")
        try:
            project_data["updated_at"] = datetime.now().isoformat()
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"Lỗi lưu project: {str(e)}"}
    
    def add_segment(self, project_id, segment_data):
        """Thêm segment vào project"""
        result = self.load_project(project_id)
        if not result["success"]:
            return result
        
        project_data = result["data"]
        segment_data["id"] = len(project_data["segments"]) + 1
        segment_data["created_at"] = datetime.now().isoformat()
        project_data["segments"].append(segment_data)
        
        return self.save_project(project_id, project_data)
    
    def update_segment(self, project_id, segment_id, updated_data):
        """Cập nhật segment"""
        result = self.load_project(project_id)
        if not result["success"]:
            return result
        
        project_data = result["data"]
        for i, segment in enumerate(project_data["segments"]):
            if segment["id"] == segment_id:
                project_data["segments"][i].update(updated_data)
                project_data["segments"][i]["updated_at"] = datetime.now().isoformat()
                break
        
        return self.save_project(project_id, project_data)
    
    def get_project_path(self, project_id, subdir=""):
        """Lấy đường dẫn thư mục project"""
        if subdir:
            return os.path.join(self.projects_dir, project_id, subdir)
        return os.path.join(self.projects_dir, project_id)
    
    def list_projects(self):
        """Liệt kê tất cả projects"""
        projects = []
        for project_dir in os.listdir(self.projects_dir):
            project_path = os.path.join(self.projects_dir, project_dir)
            if os.path.isdir(project_path):
                result = self.load_project(project_dir)
                if result["success"]:
                    projects.append({
                        "id": project_dir,
                        "name": result["data"].get("name", "Unknown"),
                        "created_at": result["data"].get("created_at", ""),
                        "status": result["data"].get("status", "unknown")
                    })
        
        return {"success": True, "projects": projects}
    
    def delete_project(self, project_id):
        """Xóa project"""
        project_path = os.path.join(self.projects_dir, project_id)
        if not os.path.exists(project_path):
            return {"success": False, "error": "Project không tồn tại"}
        
        try:
            import shutil
            shutil.rmtree(project_path)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"Lỗi xóa project: {str(e)}"} 