import os
from ai.content_generator import ContentGenerator
from image.image_generator import ImageGenerator
from tts.voice_generator import VoiceGenerator
from video.video_composer import VideoComposer
from project.project_manager import ProjectManager

class VideoPipeline:
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.image_gen = ImageGenerator()
        self.voice_gen = VoiceGenerator()
        self.video_composer = VideoComposer()
        self.project_manager = ProjectManager()
    
    def create_video_from_prompt(self, prompt, project_name="video_project", 
                                effects=None, progress_callback=None):
        """Pipeline chính: từ prompt → video hoàn chỉnh"""
        
        def update_progress(step, message):
            if progress_callback:
                progress_callback(step, message)
        
        try:
            # Bước 1: Tạo project
            update_progress(1, "Tạo project...")
            project_result = self.project_manager.create_project(project_name, prompt)
            if not project_result["success"]:
                return project_result
            
            project_id = project_result["project_id"]
            project_dir = project_result["project_dir"]
            
            # Bước 2: Sinh nội dung từ AI
            update_progress(2, "Sinh kịch bản từ AI...")
            script_result = self.content_gen.generate_script_from_prompt(prompt)
            if "error" in script_result:
                return {"success": False, "error": script_result["error"]}
            
            segments = script_result["segments"]
            segment_videos = []
            
            # Bước 3-6: Xử lý từng segment
            for i, segment in enumerate(segments):
                segment_id = segment["id"]
                update_progress(3 + i, f"Xử lý đoạn {segment_id}/{len(segments)}...")
                
                # Tạo ảnh
                image_path = os.path.join(project_dir, "images", f"segment_{segment_id}.jpg")
                image_result = self.image_gen.generate_and_save_image(
                    segment["image_prompt"], image_path
                )
                if not image_result["success"]:
                    return {"success": False, "error": f"Lỗi tạo ảnh đoạn {segment_id}: {image_result['error']}"}
                
                # Tạo giọng nói
                audio_path = os.path.join(project_dir, "audio", f"segment_{segment_id}.mp3")
                voice_result = self.voice_gen.generate_voice_auto(
                    segment["narration"], audio_path
                )
                if not voice_result["success"]:
                    return {"success": False, "error": f"Lỗi tạo giọng đoạn {segment_id}: {voice_result['error']}"}
                
                # Tạo video segment
                segment_video_path = os.path.join(project_dir, "segments", f"segment_{segment_id}.mp4")
                video_result = self.video_composer.create_segment_video(
                    image_path, audio_path, segment_video_path, effects
                )
                if not video_result["success"]:
                    return {"success": False, "error": f"Lỗi tạo video đoạn {segment_id}: {video_result['error']}"}
                
                segment_videos.append(segment_video_path)
                
                # Lưu thông tin segment vào project
                segment_data = {
                    **segment,
                    "image_path": image_path,
                    "audio_path": audio_path,
                    "video_path": segment_video_path,
                    "status": "completed"
                }
                self.project_manager.add_segment(project_id, segment_data)
            
            # Bước 7: Ghép video hoàn chỉnh
            update_progress(7, "Ghép video hoàn chỉnh...")
            final_video_path = os.path.join(project_dir, "final_video.mp4")
            merge_result = self.video_composer.merge_segments(
                segment_videos, final_video_path, 
                transitions=effects.get("transitions") if effects else None
            )
            
            if not merge_result["success"]:
                return {"success": False, "error": f"Lỗi ghép video: {merge_result['error']}"}
            
            # Cập nhật project status
            project_data = self.project_manager.load_project(project_id)["data"]
            project_data["status"] = "completed"
            project_data["final_video_path"] = final_video_path
            self.project_manager.save_project(project_id, project_data)
            
            update_progress(8, "Hoàn thành!")
            
            return {
                "success": True,
                "project_id": project_id,
                "final_video_path": final_video_path,
                "segments": len(segments),
                "project_dir": project_dir
            }
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi pipeline: {str(e)}"}
    
    def regenerate_segment(self, project_id, segment_id, new_prompt=None, effects=None):
        """Tạo lại một segment cụ thể"""
        try:
            project_result = self.project_manager.load_project(project_id)
            if not project_result["success"]:
                return project_result
            
            project_data = project_result["data"]
            segment = None
            for s in project_data["segments"]:
                if s["id"] == segment_id:
                    segment = s
                    break
            
            if not segment:
                return {"success": False, "error": "Segment không tồn tại"}
            
            project_dir = self.project_manager.get_project_path(project_id)
            
            # Tạo lại ảnh nếu có prompt mới
            if new_prompt:
                image_path = segment["image_path"]
                image_result = self.image_gen.generate_and_save_image(new_prompt, image_path)
                if not image_result["success"]:
                    return image_result
            
            # Tạo lại video segment
            video_result = self.video_composer.create_segment_video(
                segment["image_path"], segment["audio_path"], 
                segment["video_path"], effects
            )
            
            if video_result["success"]:
                # Cập nhật segment
                updated_data = {"status": "regenerated", "image_prompt": new_prompt or segment["image_prompt"]}
                self.project_manager.update_segment(project_id, segment_id, updated_data)
            
            return video_result
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi tạo lại segment: {str(e)}"}
    
    def add_background_music(self, project_id, music_path, volume=0.3):
        """Thêm nhạc nền vào video hoàn chỉnh"""
        try:
            project_result = self.project_manager.load_project(project_id)
            if not project_result["success"]:
                return project_result
            
            project_data = project_result["data"]
            if "final_video_path" not in project_data:
                return {"success": False, "error": "Video chưa được tạo"}
            
            project_dir = self.project_manager.get_project_path(project_id)
            output_path = os.path.join(project_dir, "final_video_with_music.mp4")
            
            result = self.video_composer.add_background_music(
                project_data["final_video_path"], music_path, output_path, volume
            )
            
            if result["success"]:
                project_data["final_video_with_music_path"] = output_path
                self.project_manager.save_project(project_id, project_data)
            
            return result
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi thêm nhạc nền: {str(e)}"}
    
    def create_video_with_custom_images(self, prompt, project_name, images_folder, 
                                       effects=None, progress_callback=None):
        """Pipeline với ảnh thủ công: từ prompt + ảnh có sẵn → video hoàn chỉnh"""
        
        def update_progress(step, message):
            if progress_callback:
                progress_callback(step, message)
        
        try:
            # Bước 1: Tạo project
            update_progress(1, "Tạo project...")
            project_result = self.project_manager.create_project(project_name, prompt)
            if not project_result["success"]:
                return project_result
            
            project_id = project_result["project_id"]
            project_dir = project_result["project_dir"]
            
            # Bước 2: Sinh kịch bản từ AI
            update_progress(2, "Sinh kịch bản từ AI...")
            script_result = self.content_gen.generate_script_from_prompt(prompt)
            if "error" in script_result:
                return {"success": False, "error": script_result["error"]}
            
            segments = script_result["segments"]
            
            # Lấy danh sách ảnh từ thư mục
            image_files = self._get_image_files_from_folder(images_folder)
            if len(image_files) < len(segments):
                return {"success": False, "error": f"Không đủ ảnh! Cần {len(segments)} ảnh, chỉ có {len(image_files)} ảnh"}
            
            segment_videos = []
            
            # Bước 3-6: Xử lý từng segment với ảnh có sẵn
            for i, segment in enumerate(segments):
                segment_id = segment["id"]
                update_progress(3 + i, f"Xử lý đoạn {segment_id}/{len(segments)}...")
                
                # Sử dụng ảnh có sẵn
                source_image = image_files[i % len(image_files)]  # Lặp lại nếu không đủ ảnh
                image_path = os.path.join(project_dir, "images", f"segment_{segment_id}.jpg")
                
                # Copy và resize ảnh
                image_result = self.image_gen.load_custom_image(source_image, image_path)
                if not image_result["success"]:
                    return {"success": False, "error": f"Lỗi xử lý ảnh đoạn {segment_id}: {image_result['error']}"}
                
                # Tạo giọng nói
                audio_path = os.path.join(project_dir, "audio", f"segment_{segment_id}.mp3")
                voice_result = self.voice_gen.generate_voice_auto(
                    segment["narration"], audio_path
                )
                if not voice_result["success"]:
                    return {"success": False, "error": f"Lỗi tạo giọng đoạn {segment_id}: {voice_result['error']}"}
                
                # Tạo video segment
                segment_video_path = os.path.join(project_dir, "segments", f"segment_{segment_id}.mp4")
                video_result = self.video_composer.create_segment_video(
                    image_path, audio_path, segment_video_path, effects
                )
                if not video_result["success"]:
                    return {"success": False, "error": f"Lỗi tạo video đoạn {segment_id}: {video_result['error']}"}
                
                segment_videos.append(segment_video_path)
                
                # Lưu thông tin segment vào project
                segment_data = {
                    **segment,
                    "image_path": image_path,
                    "audio_path": audio_path,
                    "video_path": segment_video_path,
                    "source_image": source_image,  # Lưu đường dẫn ảnh gốc
                    "image_source": "custom",
                    "status": "completed"
                }
                self.project_manager.add_segment(project_id, segment_data)
            
            # Bước 7: Ghép video hoàn chỉnh
            update_progress(7, "Ghép video hoàn chỉnh...")
            final_video_path = os.path.join(project_dir, "final_video.mp4")
            merge_result = self.video_composer.merge_segments(
                segment_videos, final_video_path, 
                transitions=effects.get("transitions") if effects else None
            )
            
            if not merge_result["success"]:
                return {"success": False, "error": f"Lỗi ghép video: {merge_result['error']}"}
            
            # Cập nhật project status
            project_data = self.project_manager.load_project(project_id)["data"]
            project_data["status"] = "completed"
            project_data["final_video_path"] = final_video_path
            project_data["image_source"] = "custom"
            project_data["custom_images_folder"] = images_folder
            self.project_manager.save_project(project_id, project_data)
            
            update_progress(8, "Hoàn thành!")
            
            return {
                "success": True,
                "project_id": project_id,
                "final_video_path": final_video_path,
                "segments": len(segments),
                "project_dir": project_dir,
                "image_source": "custom"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi pipeline với ảnh thủ công: {str(e)}"}
    
    def _get_image_files_from_folder(self, folder_path):
        """Lấy danh sách file ảnh từ thư mục"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        image_files = []
        
        try:
            for file in os.listdir(folder_path):
                if any(file.lower().endswith(ext) for ext in valid_extensions):
                    image_files.append(os.path.join(folder_path, file))
        except Exception:
            pass
        
        return sorted(image_files) 