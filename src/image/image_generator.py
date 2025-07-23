import openai
import os
import requests
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv('config.env')

class ImageGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'sk-test-key-replace-with-real-key':
            self.client = None
            print("WARNING  Chua cau hinh OpenAI API key cho tao anh")
        else:
            self.client = openai.OpenAI(api_key=api_key)
    
    def generate_image_dalle(self, prompt, size="1024x1024"):
        """Tạo ảnh bằng DALL-E"""
        if not self.client:
            return {"success": False, "error": "Chưa cấu hình OpenAI API key"}
            
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            return {"success": True, "url": image_url}
        except Exception as e:
            return {"success": False, "error": f"Error tạo ảnh DALL-E: {str(e)}"}
    
    def download_image(self, url, save_path):
        """Tải ảnh từ URL về local"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return {"success": True, "path": save_path}
        except Exception as e:
            return {"success": False, "error": f"Error tải ảnh: {str(e)}"}
    
    def resize_image_for_video(self, image_path, target_size=(1920, 1080)):
        """Resize ảnh cho video (16:9)"""
        try:
            with Image.open(image_path) as img:
                # Resize giữ tỷ lệ, crop nếu cần
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Lưu lại
                img_resized.save(image_path)
                return {"success": True, "path": image_path}
        except Exception as e:
            return {"success": False, "error": f"Error resize ảnh: {str(e)}"}
    
    def generate_and_save_image(self, prompt, save_path, size="1024x1024"):
        """Tạo ảnh và lưu local"""
        # Tạo ảnh
        result = self.generate_image_dalle(prompt, size)
        if not result["success"]:
            return result
        
        # Tải về
        download_result = self.download_image(result["url"], save_path)
        if not download_result["success"]:
            return download_result
        
        # Resize cho video
        resize_result = self.resize_image_for_video(save_path)
        return resize_result
    
    def load_custom_image(self, source_path, save_path):
        """Tải ảnh thủ công từ file local"""
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists(source_path):
                return {"success": False, "error": "File ảnh không tồn tại"}
            
            # Kiểm tra định dạng ảnh
            valid_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
            file_ext = os.path.splitext(source_path)[1].lower()
            if file_ext not in valid_formats:
                return {"success": False, "error": f"Định dạng ảnh không hỗ trợ: {file_ext}"}
            
            # Copy và resize ảnh
            with Image.open(source_path) as img:
                # Convert sang RGB nếu cần (cho JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize cho video (16:9)
                img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                img_resized.save(save_path, 'JPEG', quality=90)
            
            return {"success": True, "path": save_path, "source": "custom"}
        except Exception as e:
            return {"success": False, "error": f"Error tải ảnh thủ công: {str(e)}"}
    
    def validate_image_file(self, file_path):
        """Kiểm tra file ảnh hợp lệ"""
        try:
            if not os.path.exists(file_path):
                return {"valid": False, "error": "File không tồn tại"}
            
            # Kiểm tra định dạng
            valid_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in valid_formats:
                return {"valid": False, "error": f"Định dạng không hỗ trợ: {file_ext}"}
            
            # Thử mở ảnh
            with Image.open(file_path) as img:
                width, height = img.size
                file_size = os.path.getsize(file_path) / (1024*1024)  # MB
                
                return {
                    "valid": True,
                    "width": width,
                    "height": height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_mb": round(file_size, 2)
                }
        except Exception as e:
            return {"valid": False, "error": f"Error kiểm tra ảnh: {str(e)}"} 