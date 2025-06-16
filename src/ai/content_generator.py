import openai
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv('config.env')

class ContentGenerator:
    def __init__(self, api_manager=None):
        # Khởi tạo tất cả clients
        self.openai_client = None
        self.claude_client = None
        self.deepseek_client = None
        self.api_manager = api_manager
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'sk-test-key-replace-with-real-key':
            self.openai_client = openai.OpenAI(api_key=openai_key)
            
        # Claude/Anthropic
        claude_key = os.getenv('CLAUDE_API_KEY')
        if claude_key and claude_key not in ['your_claude_api_key_here', 'sk-ant-']:
            try:
                import anthropic
                self.claude_client = anthropic.Anthropic(api_key=claude_key)
            except ImportError:
                print("⚠️  Anthropic package chưa được cài đặt. Chạy: pip install anthropic")
                
        # DeepSeek
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_key and deepseek_key not in ['your_deepseek_api_key_here', 'sk-']:
            print(f"🔑 DeepSeek API Key: {deepseek_key[:10]}...")
            try:
                self.deepseek_client = openai.OpenAI(
                    api_key=deepseek_key,
                    base_url="https://api.deepseek.com"
                )
                print("✅ DeepSeek client initialized")
            except Exception as e:
                print(f"❌ DeepSeek client initialization failed: {e}")
                self.deepseek_client = None
        
        if not any([self.openai_client, self.claude_client, self.deepseek_client]):
            print("⚠️  Chưa cấu hình API key cho AI content generation")
    
    def generate_script_from_prompt(self, prompt, provider=None):
        """Sinh kịch bản từ prompt, chia thành các đoạn"""
        # Xác định provider
        if not provider:
            provider = os.getenv('CONTENT_PROVIDER', 'OpenAI GPT-4')
        
        system_prompt = """
        Bạn là chuyên gia viết kịch bản video ngắn. Hãy tạo kịch bản từ prompt của người dùng.
        Chia kịch bản thành 3-5 đoạn, mỗi đoạn khoảng 10-15 giây.
        
        QUAN TRỌNG: Phân biệt rõ các nhân vật/vai trò trong câu chuyện.
        - "narrator": Người kể chuyện (giọng trung tính)
        - "character1": Nhân vật chính (có thể là nam/nữ)
        - "character2": Nhân vật phụ (nếu có)
        - "system": Thông báo hệ thống (nếu có)
        
        Format JSON bắt buộc:
        {
            "segments": [
                {
                    "id": 1,
                    "script": "Nội dung kịch bản đoạn này",
                    "image_prompt": "Mô tả ảnh cho đoạn này",
                    "dialogues": [
                        {
                            "speaker": "narrator",
                            "text": "Lời thoại của người kể chuyện",
                            "emotion": "neutral"
                        },
                        {
                            "speaker": "character1", 
                            "text": "Lời thoại của nhân vật chính",
                            "emotion": "happy"
                        }
                    ],
                    "duration": 12
                }
            ],
            "characters": [
                {
                    "id": "narrator",
                    "name": "Người kể chuyện",
                    "gender": "neutral",
                    "suggested_voice": "vi-VN-Standard-C"
                },
                {
                    "id": "character1",
                    "name": "Tên nhân vật",
                    "gender": "female",
                    "suggested_voice": "vi-VN-Standard-A"
                }
            ]
        }
        
        Lưu ý: Chỉ JSON thuần, không markdown.
        """
        
        # Thử theo thứ tự ưu tiên
        if provider == 'DeepSeek' and self.deepseek_client:
            return self._generate_with_deepseek(system_prompt, prompt)
        elif provider == 'Claude (Anthropic)' and self.claude_client:
            return self._generate_with_claude(system_prompt, prompt)
        elif provider == 'OpenAI GPT-4' and self.openai_client:
            return self._generate_with_openai(system_prompt, prompt)
        elif provider == 'Auto (thử theo thứ tự)':
            # Thử DeepSeek trước (rẻ nhất)
            if self.deepseek_client:
                result = self._generate_with_deepseek(system_prompt, prompt)
                if "error" not in result:
                    return result
            # Rồi Claude
            if self.claude_client:
                result = self._generate_with_claude(system_prompt, prompt)
                if "error" not in result:
                    return result
            # Cuối cùng OpenAI
            if self.openai_client:
                return self._generate_with_openai(system_prompt, prompt)
        else:
            # Fallback tự động
            if self.openai_client:
                return self._generate_with_openai(system_prompt, prompt)
            elif self.claude_client:
                return self._generate_with_claude(system_prompt, prompt)
            elif self.deepseek_client:
                return self._generate_with_deepseek(system_prompt, prompt)
        
        return {"error": "Không có AI provider nào khả dụng. Vui lòng cấu hình ít nhất một API key."}
    
    def _generate_with_openai(self, system_prompt, prompt):
        """Sinh nội dung bằng OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
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
            return {"error": f"Lỗi OpenAI: {str(e)}"}
    
    def _generate_with_claude(self, system_prompt, prompt):
        """Sinh nội dung bằng Claude"""
        try:
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\nUser prompt: {prompt}"}
                ]
            )
            content = response.content[0].text
            return json.loads(content)
        except Exception as e:
            return {"error": f"Lỗi Claude: {str(e)}"}
    
    def _generate_with_deepseek(self, system_prompt, prompt):
        """Sinh nội dung bằng DeepSeek"""
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Debug: In ra content để check
            print(f"🔍 DeepSeek raw response: {content[:200]}...")
            
            # Làm sạch content (đôi khi có markdown wrapper)
            content = content.strip()
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            # Thử parse JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError as je:
                print(f"❌ DeepSeek JSON parse error: {je}")
                print(f"Raw content: {content}")
                
                # Fallback: tạo response mẫu với nhiều characters
                print("🔄 Using fallback with multiple characters...")
                return self._create_fallback_with_characters(prompt, content)
                
        except Exception as e:
            return {"error": f"Lỗi DeepSeek: {str(e)}"}
    
    def _create_fallback_with_characters(self, prompt, content=""):
        """Tạo fallback response với nhiều characters dựa trên prompt"""
        # Phân tích prompt để tìm characters
        prompt_lower = prompt.lower()
        characters = [
            {
                "id": "narrator",
                "name": "Người kể chuyện",
                "gender": "neutral", 
                "suggested_voice": "vi-VN-Standard-C"
            }
        ]
        
        # Detect characters from prompt
        if any(word in prompt_lower for word in ['cô bé', 'cô gái', 'bé gái', 'nữ']):
            characters.append({
                "id": "character1",
                "name": "Nhân vật nữ",
                "gender": "female",
                "suggested_voice": "vi-VN-Wavenet-A"
            })
        
        if any(word in prompt_lower for word in ['cậu bé', 'chàng trai', 'bé trai', 'nam']):
            characters.append({
                "id": "character2", 
                "name": "Nhân vật nam",
                "gender": "male",
                "suggested_voice": "vi-VN-Wavenet-B"
            })
            
        if any(word in prompt_lower for word in ['gấu', 'thú', 'động vật', 'pet']):
            characters.append({
                "id": "character3",
                "name": "Nhân vật động vật",
                "gender": "male",
                "suggested_voice": "vi-VN-Standard-D"
            })
        
        # Create dialogues based on characters
        dialogues = [
            {
                "speaker": "narrator",
                "text": content[:150] if content else f"Đây là câu chuyện từ prompt: {prompt[:100]}...",
                "emotion": "neutral"
            }
        ]
        
        # Add character dialogues if detected
        if len(characters) > 1:
            for i, char in enumerate(characters[1:], 1):
                if char['gender'] == 'female':
                    text = f"Xin chào! Tôi là {char['name']} trong câu chuyện này."
                elif char['gender'] == 'male' and 'động vật' in char['name']:
                    text = f"Grrr... Tôi là {char['name']}, sẵn sàng phiêu lưu!"
                else:
                    text = f"Chào mọi người! Tôi là {char['name']}."
                    
                dialogues.append({
                    "speaker": char['id'],
                    "text": text,
                    "emotion": "friendly"
                })
        
        return {
            "segments": [
                {
                    "id": 1,
                    "script": f"Câu chuyện được tạo từ prompt: {prompt}",
                    "image_prompt": "Hình ảnh minh họa cho câu chuyện phiêu lưu",
                    "dialogues": dialogues,
                    "duration": 15
                }
            ],
            "characters": characters
        }
    
    def refine_segment(self, segment_data, user_feedback, provider=None):
        """Chỉnh sửa một đoạn dựa trên feedback"""
        if not provider:
            provider = os.getenv('CONTENT_PROVIDER', 'OpenAI GPT-4')
            
        system_prompt = f"""
        Chỉnh sửa đoạn video này dựa trên feedback của người dùng.
        Đoạn hiện tại: {segment_data}
        Feedback: {user_feedback}
        
        Trả về JSON format tương tự đoạn gốc.
        """
        
        # Sử dụng provider được chọn
        if provider == 'DeepSeek' and self.deepseek_client:
            return self._refine_with_deepseek(system_prompt)
        elif provider == 'Claude (Anthropic)' and self.claude_client:
            return self._refine_with_claude(system_prompt)
        elif provider == 'OpenAI GPT-4' and self.openai_client:
            return self._refine_with_openai(system_prompt)
        else:
            # Fallback
            if self.openai_client:
                return self._refine_with_openai(system_prompt)
            elif self.claude_client:
                return self._refine_with_claude(system_prompt)
            elif self.deepseek_client:
                return self._refine_with_deepseek(system_prompt)
        
        return {"error": "Không có AI provider nào khả dụng"}
    
    def _refine_with_openai(self, system_prompt):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                max_tokens=512,
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Lỗi OpenAI: {str(e)}"}
    
    def _refine_with_claude(self, system_prompt):
        try:
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=512,
                messages=[{"role": "user", "content": system_prompt}]
            )
            return json.loads(response.content[0].text)
        except Exception as e:
            return {"error": f"Lỗi Claude: {str(e)}"}
    
    def _refine_with_deepseek(self, system_prompt):
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": system_prompt}],
                max_tokens=512,
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Lỗi DeepSeek: {str(e)}"} 