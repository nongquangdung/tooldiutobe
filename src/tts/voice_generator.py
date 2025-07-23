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
    print("[WARNING] pydub không available, chức năng ghép audio sẽ bị giới hạn")
    PYDUB_AVAILABLE = False

# Import Chatterbox TTS Provider
try:
    from .real_chatterbox_provider import RealChatterboxProvider
    CHATTERBOX_PROVIDER_AVAILABLE = True
    print("[SUCCESS] RealChatterboxProvider imported successfully")
except ImportError as e:
    CHATTERBOX_PROVIDER_AVAILABLE = False
    print(f"[WARNING] RealChatterboxProvider not available: {e}")

# Import Inner Voice Processor
try:
    import sys
    import os
    # Add current directory to path for inner voice processor
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from core.inner_voice_processor import InnerVoiceProcessor
    INNER_VOICE_AVAILABLE = True
    print("[SUCCESS] InnerVoiceProcessor imported successfully")
except ImportError as e:
    INNER_VOICE_AVAILABLE = False
    print(f"[WARNING] InnerVoiceProcessor not available: {e}")

load_dotenv('config.env')

class VoiceGenerator:
    def __init__(self):
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_TTS_API_KEY')
        
        # Initialize Chatterbox TTS Provider (Singleton)
        self.chatterbox_provider = None
        if CHATTERBOX_PROVIDER_AVAILABLE:
            try:
                self.chatterbox_provider = RealChatterboxProvider.get_instance()
                print(f"[MIC] REAL Chatterbox TTS Status: {self.chatterbox_provider.get_device_info()}")
            except Exception as e:
                print(f"[WARNING] Failed to initialize Real Chatterbox TTS: {e}")
        
        # Initialize Inner Voice Processor
        self.inner_voice_processor = None
        if INNER_VOICE_AVAILABLE:
            try:
                self.inner_voice_processor = InnerVoiceProcessor()
                if self.inner_voice_processor.ffmpeg_available:
                    print("[THEATER] Inner Voice Processor initialized successfully")
                else:
                    print("[WARNING] Inner Voice Processor initialized but FFmpeg not available")
            except Exception as e:
                print(f"[WARNING] Failed to initialize Inner Voice Processor: {e}")
                self.inner_voice_processor = None
        
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
    
    def get_available_voices(self, provider="chatterbox"):
        """Lấy danh sách giọng nói có sẵn theo provider"""
        if provider == "chatterbox" and self.chatterbox_provider:
            try:
                return self.chatterbox_provider.get_available_voices()
            except Exception as e:
                print(f"[WARNING] Error getting chatterbox voices: {e}")
                return {}
        elif provider == "google":
            return self.google_voices
        elif provider == "elevenlabs":
            return self.get_available_voices_elevenlabs()
        else:
            return {}
    
    def get_available_tts_providers(self):
        """Lấy danh sách TTS providers có sẵn"""
        providers = []
        
        if self.elevenlabs_api_key:
            providers.append({
                "id": "elevenlabs",
                "name": "ElevenLabs",
                "status": "[OK] Available",
                "languages": ["English", "Multi-language"],
                "features": ["Voice cloning", "High quality"]
            })
        
        if self.google_api_key:
            providers.append({
                "id": "google_cloud",
                "name": "Google Cloud TTS",
                "status": "[OK] Available",
                "languages": ["Vietnamese", "Multi-language"],
                "features": ["Standard & Wavenet voices", "SSML support"]
            })
        
        providers.append({
            "id": "google_free",
            "name": "Google TTS (Free)",
            "status": "[OK] Available",
            "languages": ["Vietnamese", "Multi-language"],
            "features": ["Free", "Basic quality"]
        })
        
        if self.chatterbox_provider and self.chatterbox_provider.is_initialized:
            device_info = self.chatterbox_provider.get_device_info()
            providers.append({
                "id": "chatterbox",
                "name": "[ROCKET] REAL Chatterbox TTS",
                "status": f"[OK] Available ({device_info['device_name']})",
                "languages": ["English"],
                "features": ["REAL cfg_weight support", "True emotion control", "Voice cloning", f"Device: {device_info['device_name']}"]
            })
        elif CHATTERBOX_PROVIDER_AVAILABLE:
            providers.append({
                "id": "chatterbox",
                "name": "[ROCKET] REAL Chatterbox TTS",
                "status": "[EMOJI] Failed to initialize",
                "languages": ["English"],
                "features": ["REAL cfg_weight support", "True emotion control", "Voice cloning"]
            })
        
        return providers
    
    def generate_voice_chatterbox(self, text, save_path, voice_sample_path=None, emotion_exaggeration=1.0, speed=1.0, voice_name=None, cfg_weight=0.5, voice_prompt=None):
        """Tạo giọng nói bằng REAL Chatterbox TTS với TRUE cfg_weight và emotion control + PROMPT-BASED VOICE"""
        if not self.chatterbox_provider or not self.chatterbox_provider.is_initialized:
            return {"success": False, "error": "Real Chatterbox TTS not available or not initialized"}
        
        return self.chatterbox_provider.generate_voice(
            text=text,
            save_path=save_path,
            voice_sample_path=voice_sample_path,
            emotion_exaggeration=emotion_exaggeration,
            speed=speed,
            voice_name=voice_name,
            cfg_weight=cfg_weight,
            voice_prompt=voice_prompt  # NEW: Support prompt-based voice generation
        )
    
    def generate_voice_auto_v2(self, text, save_path, provider="auto", language="vi", **kwargs):
        """
        Auto TTS với provider selection và language detection
        
        Args:
            text: Text to synthesize
            save_path: Output file path
            provider: "auto", "google", "elevenlabs", "chatterbox", "google_free"
            language: "vi", "en", "auto"
            **kwargs: Provider-specific options
        """
        # Auto-detect language nếu cần
        if language == "auto":
            language = self._detect_language(text)
        
        # Auto-select provider dựa trên language và availability
        if provider == "auto":
            if language == "vi":
                # Vietnamese: Ưu tiên Google Cloud TTS
                if self.google_api_key:
                    provider = "google"
                else:
                    provider = "google_free"
            elif language == "en":
                # English: Ưu tiên Chatterbox nếu có, otherwise ElevenLabs
                if self.chatterbox_provider and self.chatterbox_provider.is_initialized:
                    provider = "chatterbox"
                elif self.elevenlabs_api_key:
                    provider = "elevenlabs"
                else:
                    provider = "google_free"
            else:
                # Other languages: Google services
                provider = "google" if self.google_api_key else "google_free"
        
        # Generate với provider được chọn
        if provider == "chatterbox":
            return self.generate_voice_chatterbox(text, save_path, **kwargs)
        elif provider == "elevenlabs":
            voice_id = kwargs.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
            return self.generate_voice_elevenlabs(text, voice_id, save_path)
        elif provider == "google":
            voice_name = kwargs.get("voice_name", "abigail")
            return self.generate_voice_chatterbox(text, save_path, voice_name=voice_name)
        elif provider == "google_free":
            lang = "vi" if language == "vi" else "en"
            return self.generate_voice_google_free(text, save_path, lang)
        else:
            return {"success": False, "error": f"Unknown provider: {provider}"}
    
    def _detect_language(self, text):
        """Simple language detection"""
        # Check for Vietnamese characters
        vietnamese_chars = "àáãạảăắằẳẵặâấầẩẫậđèéẹẻẽêềếểễệìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳýỵỷỹ"
        vietnamese_count = sum(1 for char in text.lower() if char in vietnamese_chars)
        
        if vietnamese_count > len(text) * 0.1:  # 10% threshold
            return "vi"
        else:
            return "en"
    
    def get_chatterbox_device_info(self):
        """Lấy thông tin device của Real Chatterbox TTS"""
        if self.chatterbox_provider:
            return self.chatterbox_provider.get_device_info()
        return {"available": False, "error": "Real Chatterbox TTS not initialized"}
    
    def cleanup_chatterbox(self):
        """Cleanup Real Chatterbox TTS resources (Singleton safe)"""
        if self.chatterbox_provider:
            # Sử dụng soft_cleanup cho Singleton để không destroy shared instance
            self.chatterbox_provider.soft_cleanup()
    
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
            return {"success": False, "error": f"Error ElevenLabs TTS: {str(e)}"}
    
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
            return {"success": False, "error": f"Error Google TTS: {str(e)}"}
    
    def get_available_voices_elevenlabs(self):
        """Lấy danh sách giọng nói có sẵn từ ElevenLabs"""
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": self.elevenlabs_api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Error lấy danh sách giọng: {str(e)}"}
    
    def split_text_by_sentences(self, text, max_chars=200):
        """Tách văn bản thành các câu ngắn để tạo audio riêng"""
        # Tách theo dấu câu
        sentences = re.split(r'[.!?[EMOJI][EMOJI][EMOJI]]+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Nếu câu quá dài thì tách thêm theo dấu phẩy
            if len(sentence) > max_chars:
                sub_sentences = re.split(r'[,[EMOJI][EMOJI];]+', sentence)
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
            return {"success": False, "error": f"Error Google TTS Free: {str(e)}"}
    
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
            voice_name = voice_mapping.get(character, "abigail")  # Use Chatterbox default
            
            # Tách văn bản thành các chunk nhỏ
            text_chunks = self.split_text_by_sentences(text)
            segment_audios = []
            
            for j, chunk in enumerate(text_chunks):
                chunk_path = os.path.join(output_dir, f"segment_{i+1}_chunk_{j+1}.mp3")
                
                # Tạo audio cho chunk với Chatterbox TTS
                result = self.generate_voice_chatterbox(
                    text=chunk,
                    save_path=chunk_path,
                    voice_name=voice_name
                )
                
                if result["success"]:
                    segment_audios.append(chunk_path)
                else:
                    return {"success": False, "error": f"Error tạo audio chunk {j+1} của segment {i+1}: {result['error']}"}
            
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
                    return {"success": False, "error": f"Error ghép audio segment {i+1}"}
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
                    
                    # Case-insensitive voice mapping lookup
                    voice_name = None
                    for map_key, map_voice in voice_mapping.items():
                        if map_key.lower() == speaker.lower():
                            voice_name = map_voice
                            break
                    
                    dialogue_count = segment_idx * 10 + dialogue_idx + 1  # Unique number
                    if voice_name is None:
                        voice_name = 'abigail'  # Final fallback
                        print(f"[VOICE DEBUG #{dialogue_count}] ❌ FAIL: speaker='{speaker}' NOT FOUND in voice_mapping={voice_mapping} -> fallback='abigail'")
                    else:
                        print(f"[VOICE DEBUG #{dialogue_count}] ✅ OK: speaker='{speaker}' -> voice='{voice_name}'")
                    
                    # Check inner voice flag
                    inner_voice = dialogue.get('inner_voice', False)
                    
                    # Tên file cho dialogue này
                    audio_filename = f"s{segment_idx+1}_d{dialogue_idx+1}_{speaker}.mp3"
                    audio_path = os.path.join(output_dir, audio_filename)
                    
                    # Tạo audio với Chatterbox TTS
                    result = self.generate_voice_chatterbox(
                        text=text,
                        save_path=audio_path,
                        voice_name=voice_name
                    )
                    
                    if result["success"]:
                        final_audio_path = audio_path
                        
                        # Xử lý inner voice nếu có flag
                        if inner_voice and self.inner_voice_processor:
                            print(f"[THEATER] Processing inner voice for: {speaker}")
                            inner_result = self.inner_voice_processor.process_dialogue_with_inner_voice(
                                audio_path, dialogue, output_dir
                            )
                            
                            # Log JSON cho inner voice
                            log_data = {
                                "segment": segment_idx+1,
                                "dialogue": dialogue_idx+1,
                                "speaker": speaker,
                                "inner_voice": True,
                                "inner_voice_type": dialogue.get("inner_voice_type", "auto"),
                                "preset": inner_result.get("preset_name", "Unknown"),
                                "success": inner_result.get("success", False),
                                "output_path": inner_result.get("output_path", None),
                                "error": inner_result.get("error", None)
                            }
                            print("[INNER_VOICE_LOG]", json.dumps(log_data, ensure_ascii=False, indent=2))
                            if inner_result["success"] and inner_result.get("inner_voice_applied", False):
                                final_audio_path = inner_result["output_path"]
                                print(f"   [OK] Inner voice applied: {inner_result.get('preset_name', 'Unknown')}")
                                
                                # Xóa file gốc nếu đã tạo inner voice version
                                try:
                                    os.remove(audio_path)
                                except:
                                    pass
                            else:
                                print(f"   [WARNING] Inner voice failed: {inner_result.get('error', 'Unknown error')}")
                        elif inner_voice and not self.inner_voice_processor:
                            print(f"[WARNING] Inner voice requested but processor not available for: {speaker}")
                        
                        segment_audio_files.append(final_audio_path)
                        character_audio_files[speaker].append(final_audio_path)
                        
                        # Update filename display
                        display_filename = os.path.basename(final_audio_path)
                        inner_indicator = "[THEATER]" if inner_voice else ""
                        print(f"[OK] Created audio: {display_filename} ({voice_name}) {inner_indicator}")
                    else:
                        print(f"[EMOJI] Failed to create audio for {speaker}: {result.get('error')}")
                        return {"success": False, "error": f"Error tạo audio cho {speaker}: {result.get('error')}"}
                
                # Ghép các dialogue trong segment thành 1 file
                if segment_audio_files:
                    segment_final_path = os.path.join(output_dir, f"segment_{segment_idx+1}_complete.mp3")
                    
                    if len(segment_audio_files) > 1:
                        merge_result = self.merge_audio_files(segment_audio_files, segment_final_path)
                        if merge_result["success"]:
                            all_audio_files.append(segment_final_path)
                        else:
                            return {"success": False, "error": f"Error ghép segment {segment_idx+1}"}
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
                    return {"success": False, "error": "Error tạo file audio cuối cùng"}
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
            return {"success": False, "error": f"Error tạo audio: {str(e)}"}
    
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
                    # Suppress FFmpeg stderr for PyDub operations
                    import os, contextlib
                    with contextlib.redirect_stderr(open(os.devnull, 'w')):
                        audio = AudioSegment.from_mp3(file_path)
                    combined += audio
                    # Thêm khoảng im lặng ngắn giữa các đoạn
                    combined += AudioSegment.silent(duration=300)  # 300ms
            
            # Suppress FFmpeg stderr for export
            with contextlib.redirect_stderr(open(os.devnull, 'w')):
                combined.export(output_path, format="mp3")
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": f"Error ghép audio: {str(e)}"} 