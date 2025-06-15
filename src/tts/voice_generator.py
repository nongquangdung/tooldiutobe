import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('config.env')

class VoiceGenerator:
    def __init__(self):
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_TTS_API_KEY')
    
    def generate_voice_elevenlabs(self, text, voice_id="21m00Tcm4TlvDq8ikWAM", save_path="output.mp3"):
        """Tạo giọng nói bằng ElevenLabs"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return {"success": True, "path": save_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi ElevenLabs TTS: {str(e)}"}
    
    def generate_voice_google(self, text, language_code="vi-VN", save_path="output.wav"):
        """Tạo giọng nói bằng Google TTS"""
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_api_key}"
        
        data = {
            "input": {"text": text},
            "voice": {
                "languageCode": language_code,
                "name": "vi-VN-Standard-A",
                "ssmlGender": "FEMALE"
            },
            "audioConfig": {
                "audioEncoding": "MP3"
            }
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            audio_content = result['audioContent']
            
            # Decode base64 và lưu file
            import base64
            with open(save_path, 'wb') as f:
                f.write(base64.b64decode(audio_content))
            
            return {"success": True, "path": save_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi Google TTS: {str(e)}"}
    
    def get_available_voices_elevenlabs(self):
        """Lấy danh sách giọng nói có sẵn từ ElevenLabs"""
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": self.elevenlabs_api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Lỗi lấy danh sách giọng: {str(e)}"}
    
    def generate_voice_auto(self, text, save_path, prefer_elevenlabs=True):
        """Tự động chọn TTS service (ưu tiên ElevenLabs nếu có key)"""
        if prefer_elevenlabs and self.elevenlabs_api_key:
            return self.generate_voice_elevenlabs(text, save_path=save_path)
        elif self.google_api_key:
            return self.generate_voice_google(text, save_path=save_path)
        else:
            return {"success": False, "error": "Không có API key TTS nào được cấu hình"} 