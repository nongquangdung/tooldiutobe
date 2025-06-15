import openai
import os
from dotenv import load_dotenv
import json

load_dotenv('config.env')

class ContentGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'sk-test-key-replace-with-real-key':
            self.client = None
            print("⚠️  Chưa cấu hình OpenAI API key. Vui lòng cập nhật config.env")
        else:
            self.client = openai.OpenAI(api_key=api_key)
    
    def generate_script_from_prompt(self, prompt):
        """Sinh kịch bản từ prompt, chia thành các đoạn"""
        if not self.client:
            return {"error": "Chưa cấu hình OpenAI API key. Vui lòng cập nhật config.env với API key thật."}
        
        system_prompt = """
        Bạn là chuyên gia viết kịch bản video ngắn. Hãy tạo kịch bản từ prompt của người dùng.
        Chia kịch bản thành 3-5 đoạn, mỗi đoạn khoảng 10-15 giây.
        
        Trả về JSON format:
        {
            "segments": [
                {
                    "id": 1,
                    "script": "Nội dung kịch bản đoạn này",
                    "image_prompt": "Mô tả ảnh cho đoạn này",
                    "narration": "Lời thoại cho đoạn này",
                    "duration": 12
                }
            ]
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {"error": f"Lỗi sinh nội dung: {str(e)}"}
    
    def refine_segment(self, segment_data, user_feedback):
        """Chỉnh sửa một đoạn dựa trên feedback"""
        if not self.client:
            return {"error": "Chưa cấu hình OpenAI API key"}
            
        system_prompt = f"""
        Chỉnh sửa đoạn video này dựa trên feedback của người dùng.
        Đoạn hiện tại: {segment_data}
        Feedback: {user_feedback}
        
        Trả về JSON format tương tự đoạn gốc.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt}
                ],
                max_tokens=512,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {"error": f"Lỗi chỉnh sửa: {str(e)}"} 