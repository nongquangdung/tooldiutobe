from PySide6.QtCore import QThread, Signal
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.video_pipeline import VideoPipeline

class VideoGenerationThread(QThread):
    progress_updated = Signal(int, str)
    finished = Signal(dict)
    
    def __init__(self, prompt, project_name, effects, use_custom_images=False, custom_images_folder=None,
                 voice_name="vi-VN-Standard-A", project_folder=None):
        super().__init__()
        self.prompt = prompt
        self.project_name = project_name
        self.effects = effects
        self.use_custom_images = use_custom_images
        self.custom_images_folder = custom_images_folder
        self.voice_name = voice_name
        self.project_folder = project_folder
        self.pipeline = VideoPipeline()
    
    def run(self):
        def progress_callback(step, message):
            self.progress_updated.emit(step, message)
        
        try:
            # Tạo video với hoặc không có ảnh thủ công
            if self.use_custom_images and self.custom_images_folder:
                result = self.pipeline.create_video_with_custom_images(
                    self.prompt, self.project_name, self.custom_images_folder, 
                    self.effects, progress_callback
                )
            else:
                result = self.pipeline.create_video_from_prompt(
                    self.prompt, self.project_name, self.effects, progress_callback,
                    self.voice_name, self.project_folder
                )
            self.finished.emit(result)
            
        except Exception as e:
            self.finished.emit({
                "success": False,
                "error": str(e)
            }) 