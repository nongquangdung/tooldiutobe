import os
import requests
from dotenv import load_dotenv
import json
import re
from gtts import gTTS
import tempfile

# Conditional import for pydub (có thể có lỗi trên Python 3.13)
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    print("⚠️ pydub không available, chức năng ghép audio sẽ bị giới hạn")
    PYDUB_AVAILABLE = False

load_dotenv('config.env')

class VoiceGenerator:
    def __init__(self):
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_TTS_API_KEY')
        
        # Danh sách giọng Google TTS
        self.google_voices = {
            "vi-VN-Standard-A": {"gender": "FEMALE", "name": "vi-VN-Standard-A"},
            "vi-VN-Standard-B": {"gender": "MALE", "name": "vi-VN-Standard-B"},
            "vi-VN-Standard-C": {"gender": "FEMALE", "name": "vi-VN-Standard-C"},
            "vi-VN-Standard-D": {"gender": "MALE", "name": "vi-VN-Standard-D"},
            "vi-VN-Wavenet-A": {"gender": "FEMALE", "name": "vi-VN-Wavenet-A"},
            "vi-VN-Wavenet-B": {"gender": "MALE", "name": "vi-VN-Wavenet-B"},
            "vi-VN-Wavenet-C": {"gender": "FEMALE", "name": "vi-VN-Wavenet-C"},
            "vi-VN-Wavenet-D": {"gender": "MALE", "name": "vi-VN-Wavenet-D"}
        }
    
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
    
    def split_text_by_sentences(self, text, max_chars=200):
        """Tách văn bản thành các câu ngắn để tạo audio riêng"""
        # Tách theo dấu câu
        sentences = re.split(r'[.!?。！？]+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Nếu câu quá dài thì tách thêm theo dấu phẩy
            if len(sentence) > max_chars:
                sub_sentences = re.split(r'[,，；;]+', sentence)
                for sub in sub_sentences:
                    sub = sub.strip()
                    if sub and len(current_chunk + sub) < max_chars:
                        current_chunk += sub + ", "
                    elif sub:
                        if current_chunk:
                            chunks.append(current_chunk.strip().rstrip(','))
                        current_chunk = sub + ", "
            else:
                if len(current_chunk + sentence) < max_chars:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if chunk.strip()]
    
    def generate_voice_google_free(self, text, save_path, lang='vi'):
        """Tạo giọng nói bằng Google TTS miễn phí (gTTS)"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(save_path)
            return {"success": True, "path": save_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi Google TTS Free: {str(e)}"}
    
    def generate_voice_with_multiple_voices(self, segments, output_dir, voice_mapping=None):
        """
        Tạo audio cho nhiều segment với giọng đọc khác nhau
        segments: list of {"text": "...", "character": "narrator/character1/..."}
        voice_mapping: {"narrator": "vi-VN-Standard-A", "character1": "vi-VN-Standard-B"}
        """
        if not voice_mapping:
            voice_mapping = {
                "narrator": "vi-VN-Standard-A",
                "character1": "vi-VN-Standard-B"
            }
        
        audio_files = []
        
        for i, segment in enumerate(segments):
            text = segment.get("text", "")
            character = segment.get("character", "narrator")
            voice_name = voice_mapping.get(character, "vi-VN-Standard-A")
            
            # Tách văn bản thành các chunk nhỏ
            text_chunks = self.split_text_by_sentences(text)
            segment_audios = []
            
            for j, chunk in enumerate(text_chunks):
                chunk_path = os.path.join(output_dir, f"segment_{i+1}_chunk_{j+1}.mp3")
                
                # Tạo audio cho chunk
                if self.google_api_key:
                    result = self.generate_voice_google_with_voice(chunk, voice_name, chunk_path)
                else:
                    result = self.generate_voice_google_free(chunk, chunk_path)
                
                if result["success"]:
                    segment_audios.append(chunk_path)
                else:
                    return {"success": False, "error": f"Lỗi tạo audio chunk {j+1} của segment {i+1}: {result['error']}"}
            
            # Ghép các chunk thành segment hoàn chỉnh
            if len(segment_audios) > 1:
                segment_final_path = os.path.join(output_dir, f"segment_{i+1}_complete.mp3")
                merge_result = self.merge_audio_files(segment_audios, segment_final_path)
                if merge_result["success"]:
                    audio_files.append(segment_final_path)
                    # Xóa các file chunk tạm
                    for chunk_file in segment_audios:
                        try:
                            os.remove(chunk_file)
                        except:
                            pass
                else:
                    return {"success": False, "error": f"Lỗi ghép audio segment {i+1}"}
            else:
                audio_files.append(segment_audios[0])
        
        return {"success": True, "audio_files": audio_files}
    
    def generate_audio_by_characters(self, script_data, output_dir, voice_mapping):
        """
        Tạo audio theo nhân vật từ script data có format mới
        script_data: {"segments": [...], "characters": [...]}
        voice_mapping: {"narrator": "vi-VN-Standard-A", ...}
        """
        os.makedirs(output_dir, exist_ok=True)
        
        all_audio_files = []
        character_audio_files = {}  # Track files by character
        
        # Khởi tạo dict cho từng character
        for character in script_data.get('characters', []):
            character_audio_files[character['id']] = []
        
        try:
            # Xử lý từng segment
            for segment_idx, segment in enumerate(script_data.get('segments', [])):
                segment_audio_files = []
                
                # Xử lý từng dialogue trong segment
                for dialogue_idx, dialogue in enumerate(segment.get('dialogues', [])):
                    speaker = dialogue['speaker']
                    text = dialogue['text']
                    voice_name = voice_mapping.get(speaker, 'vi-VN-Standard-A')
                    
                    # Tên file cho dialogue này
                    audio_filename = f"s{segment_idx+1}_d{dialogue_idx+1}_{speaker}.mp3"
                    audio_path = os.path.join(output_dir, audio_filename)
                    
                    # Tạo audio
                    result = self.generate_voice_google_with_voice(text, voice_name, audio_path)
                    
                    if result["success"]:
                        segment_audio_files.append(audio_path)
                        character_audio_files[speaker].append(audio_path)
                        print(f"✅ Created audio: {audio_filename} ({voice_name})")
                    else:
                        print(f"❌ Failed to create audio for {speaker}: {result.get('error')}")
                        return {"success": False, "error": f"Lỗi tạo audio cho {speaker}: {result.get('error')}"}
                
                # Ghép các dialogue trong segment thành 1 file
                if segment_audio_files:
                    segment_final_path = os.path.join(output_dir, f"segment_{segment_idx+1}_complete.mp3")
                    
                    if len(segment_audio_files) > 1:
                        merge_result = self.merge_audio_files(segment_audio_files, segment_final_path)
                        if merge_result["success"]:
                            all_audio_files.append(segment_final_path)
                        else:
                            return {"success": False, "error": f"Lỗi ghép segment {segment_idx+1}"}
                    else:
                        # Chỉ có 1 file, copy luôn
                        import shutil
                        shutil.copy2(segment_audio_files[0], segment_final_path)
                        all_audio_files.append(segment_final_path)
            
            # Tạo file hoàn chỉnh cuối cùng
            final_audio_path = os.path.join(output_dir, "final_complete_audio.mp3")
            if len(all_audio_files) > 1:
                merge_result = self.merge_audio_files(all_audio_files, final_audio_path)
                if not merge_result["success"]:
                    return {"success": False, "error": "Lỗi tạo file audio cuối cùng"}
            else:
                import shutil
                shutil.copy2(all_audio_files[0], final_audio_path)
            
            return {
                "success": True,
                "final_audio_path": final_audio_path,
                "segment_audio_files": all_audio_files,
                "character_audio_files": character_audio_files,
                "output_dir": output_dir
            }
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi tạo audio: {str(e)}"}
    
    def generate_voice_google_with_voice(self, text, voice_name, save_path):
        """Tạo giọng nói bằng Google TTS với giọng cụ thể"""
        if not self.google_api_key:
            return self.generate_voice_google_free(text, save_path)
        
        voice_config = self.google_voices.get(voice_name, self.google_voices["vi-VN-Standard-A"])
        
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_api_key}"
        
        data = {
            "input": {"text": text},
            "voice": {
                "languageCode": "vi-VN",
                "name": voice_config["name"],
                "ssmlGender": voice_config["gender"]
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
            
            import base64
            with open(save_path, 'wb') as f:
                f.write(base64.b64decode(audio_content))
            
            return {"success": True, "path": save_path}
        except Exception as e:
            # Fallback to free TTS
            return self.generate_voice_google_free(text, save_path)
    
    def merge_audio_files(self, file_paths, output_path):
        """Ghép nhiều file audio thành một file"""
        if not PYDUB_AVAILABLE:
            # Fallback: chỉ sử dụng file đầu tiên
            if file_paths and os.path.exists(file_paths[0]):
                import shutil
                shutil.copy2(file_paths[0], output_path)
                return {"success": True, "path": output_path}
            return {"success": False, "error": "Không thể ghép audio - pydub không available"}
        
        try:
            combined = AudioSegment.empty()
            
            for file_path in file_paths:
                if os.path.exists(file_path):
                    audio = AudioSegment.from_mp3(file_path)
                    combined += audio
                    # Thêm khoảng im lặng ngắn giữa các đoạn
                    combined += AudioSegment.silent(duration=300)  # 300ms
            
            combined.export(output_path, format="mp3")
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Lỗi ghép audio: {str(e)}"}
    
    def generate_voice_auto(self, text, save_path, voice_name="vi-VN-Standard-A", prefer_elevenlabs=True):
        """Tự động chọn TTS service (ưu tiên ElevenLabs nếu có key)"""
        if prefer_elevenlabs and self.elevenlabs_api_key:
            return self.generate_voice_elevenlabs(text, save_path=save_path)
        elif self.google_api_key:
            return self.generate_voice_google_with_voice(text, voice_name, save_path)
        else:
            return self.generate_voice_google_free(text, save_path) 