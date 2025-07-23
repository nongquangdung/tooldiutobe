<<<<<<< Updated upstream
#!/usr/bin/env python3
"""
🎭 INNER VOICE PROCESSOR
=======================

Xử lý hiệu ứng inner voice (thoại nội tâm) cho Voice Studio.
Sử dụng FFmpeg để tạo echo effects cho dialogue với inner_voice: true
"""

import os
import subprocess
import tempfile
from enum import Enum
from typing import Dict, Any, Optional
from pathlib import Path

class InnerVoiceType(Enum):
    """Các loại inner voice effects"""
    LIGHT = "light"      # Nội tâm nhẹ - tự sự, tâm sự
    DEEP = "deep"        # Nội tâm sâu - căng thẳng, hồi tưởng  
    DREAMY = "dreamy"    # Nội tâm cách âm - xa thực tại, mơ hồ

class InnerVoiceProcessor:
    """Processor cho inner voice effects"""
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        
        # Default echo presets cho từng loại inner voice
        self.echo_presets = {
            InnerVoiceType.LIGHT: {
                "name": "Nội tâm nhẹ",
                "description": "Tự sự, tâm sự - phù hợp nữ trẻ, nhân vật suy tư",
                "filter": "aecho=0.6:0.5:50:0.3",
                "suffix": "_inner_light"
            },
            InnerVoiceType.DEEP: {
                "name": "Nội tâm sâu", 
                "description": "Căng thẳng, hồi tưởng - phù hợp độc thoại nam, giọng nặng trĩu",
                "filter": "aecho=0.7:0.6:150:0.4|0.3",
                "suffix": "_inner_deep"
            },
            InnerVoiceType.DREAMY: {
                "name": "Nội tâm cách âm",
                "description": "Xa thực tại, mơ hồ - phù hợp cảnh mộng, mất phương hướng", 
                "filter": "volume=0.8,aecho=0.5:0.6:300:0.4,lowpass=f=3000",
                "suffix": "_inner_dreamy"
            }
        }
        
        # Load custom settings từ config file
        self.load_config_from_file()
    
    def _check_ffmpeg(self) -> bool:
        """Check nếu FFmpeg available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            return True
        except FileNotFoundError:
            return False
    
    def load_config_from_file(self):
        """Load custom inner voice settings từ unified_emotions.json"""
        try:
            config_path = "configs/emotions/unified_emotions.json"
            
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if "inner_voice_config" in config and "presets" in config["inner_voice_config"]:
                    presets = config["inner_voice_config"]["presets"]
                    
                    print(f"🎭 LOADING InnerVoiceProcessor config from file...")
                    
                    for type_name, preset_data in presets.items():
                        try:
                            type_enum = InnerVoiceType(type_name.lower())
                            
                            if type_enum in self.echo_presets:
                                # Update với settings từ file
                                if "filter" in preset_data:
                                    self.echo_presets[type_enum]["filter"] = preset_data["filter"]
                                    print(f"   ✅ {type_name}: filter='{preset_data['filter']}'")
                                
                                # Store UI params cho debugging
                                for key in ["delay", "decay", "gain"]:
                                    if key in preset_data:
                                        self.echo_presets[type_enum][key] = preset_data[key]
                                        
                        except ValueError:
                            print(f"   ⚠️ Unknown inner voice type: {type_name}")
                    
                    print(f"✅ InnerVoiceProcessor config loaded from {config_path}")
                else:
                    print(f"📋 No inner_voice_config found, using defaults")
            else:
                print(f"📋 Config file not found, using default presets")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not load inner voice config: {e}")
            print(f"📋 Using default presets")
    
    def get_inner_voice_type(self, character_name: str, emotion: str, gender: str = "neutral") -> InnerVoiceType:
        """Tự động chọn loại inner voice dựa trên character và emotion"""
        
        # Logic auto-select dựa trên emotion và gender
        emotion_lower = emotion.lower()
        
        # Nội tâm sâu - emotions căng thẳng, nặng nề
        deep_emotions = [
            "sad", "angry", "anxious", "worried", "frustrated", "disappointed",
            "desperate", "commanding", "fierce", "dramatic", "mysterious", "suspenseful"
        ]
        
        # Nội tâm cách âm - emotions mơ hồ, xa vời
        dreamy_emotions = [
            "whisper", "soft", "contemplative", "sleepy", "confused", "bewildered",
            "romantic", "innocent", "gentle"
        ]
        
        # Kiểm tra emotion
        if any(e in emotion_lower for e in deep_emotions):
            return InnerVoiceType.DEEP
        elif any(e in emotion_lower for e in dreamy_emotions):
            return InnerVoiceType.DREAMY
        else:
            # Default: nội tâm nhẹ cho emotions bình thường
            return InnerVoiceType.LIGHT
    
    def set_custom_preset(self, type_name: str, params: dict):
        """Cập nhật preset cho 1 type từ UI/config"""
        try:
            # Convert string to enum
            type_enum = InnerVoiceType(type_name.lower())
            
            if type_enum in self.echo_presets:
                print(f"🎛️ UPDATING {type_name} preset:")
                
                # Tạo filter string từ UI params
                if all(key in params for key in ["delay", "decay", "gain"]):
                    # Build FFmpeg filter từ UI params  
                    delay = params["delay"]
                    decay = params["decay"] 
                    gain = params["gain"]
                    custom_filter = params.get("filter", f"aecho={gain}:{decay}:{delay}:{decay}")
                    
                    print(f"   📊 delay={delay}, decay={decay}, gain={gain}")
                    print(f"   🎛️ filter='{custom_filter}'")
                    
                    # Update preset với UI values
                    self.echo_presets[type_enum].update({
                        "filter": custom_filter,
                        "description": f"{self.echo_presets[type_enum]['description']} - từ UI",
                        **params  # Include all UI params
                    })
                    
                    print(f"✅ Updated {type_name} preset successfully")
                else:
                    print(f"⚠️ Missing required params for {type_name}")
                    
        except ValueError as e:
            print(f"❌ Invalid inner voice type: {type_name} - {e}")
        except Exception as e:
            print(f"❌ Error updating preset {type_name}: {e}")
    
    def process_inner_voice(self, input_path: str, output_path: str, 
                          inner_voice_type: InnerVoiceType = InnerVoiceType.LIGHT) -> Dict[str, Any]:
        """Process audio file để tạo inner voice effect"""
        
        if not self.ffmpeg_available:
            return {
                "success": False,
                "error": "FFmpeg not available - cannot process inner voice"
            }
        
        if not os.path.exists(input_path):
            return {
                "success": False,
                "error": f"Input file not found: {input_path}"
            }
        
        try:
            # Ưu tiên preset custom nếu có
            preset = self.echo_presets.get(inner_voice_type)
            
            if preset is None:
                preset = self.echo_presets[self.get_inner_voice_type(character_name, emotion)]
            
            print(f"🎭 PROCESSING INNER VOICE: {os.path.basename(input_path)}")
            print(f"   🎪 Type: {preset['name']}")
            print(f"   📝 Effect: {preset['description']}")
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-i', input_path,
                '-af', preset['filter'],
                '-y',  # Overwrite output
                output_path
            ]
            
            # Execute FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ INNER VOICE SUCCESS!")
                print(f"   📁 Original: {os.path.basename(input_path)}")
                print(f"   📁 Processed: {os.path.basename(output_path)}")
                
                # Get file info
                original_size = os.path.getsize(input_path)
                processed_size = os.path.getsize(output_path)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "inner_voice_type": inner_voice_type.value,
                    "preset_name": preset['name'],
                    "original_size": original_size,
                    "processed_size": processed_size,
                    "filter": preset['filter']
                }
            else:
                return {
                    "success": False,
                    "error": f"FFmpeg failed: {result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing inner voice: {str(e)}"
            }
    
    def process_dialogue_with_inner_voice(self, input_path: str, dialogue_data: Dict[str, Any],
                                        output_dir: str) -> Dict[str, Any]:
        """Process một dialogue với inner voice flag"""
        
        # Check nếu có inner voice flag
        if not dialogue_data.get("inner_voice", False):
            # Không có inner voice, return original path
            return {
                "success": True,
                "output_path": input_path,
                "inner_voice_applied": False
            }
        
        # Determine inner voice type
        character_id = dialogue_data.get("speaker", "unknown")
        emotion = dialogue_data.get("emotion", "neutral")
        
        # Có thể override type bằng inner_voice_type field
        if "inner_voice_type" in dialogue_data:
            type_str = dialogue_data["inner_voice_type"].lower()
            inner_voice_type = {
                "light": InnerVoiceType.LIGHT,
                "deep": InnerVoiceType.DEEP, 
                "dreamy": InnerVoiceType.DREAMY
            }.get(type_str, InnerVoiceType.LIGHT)
        else:
            # Auto-detect based on emotion
            inner_voice_type = self.get_inner_voice_type(character_id, emotion)
        
        # Generate output filename
        input_name = Path(input_path).stem
        preset = self.echo_presets[inner_voice_type]
        output_name = f"{input_name}{preset['suffix']}.mp3"
        output_path = os.path.join(output_dir, output_name)
        
        # Process inner voice
        result = self.process_inner_voice(input_path, output_path, inner_voice_type)
        
        if result["success"]:
            result["inner_voice_applied"] = True
            result["original_path"] = input_path
        
        return result
    
    def get_available_types(self) -> Dict[str, Dict[str, str]]:
        """Get danh sách available inner voice types"""
        return {
            type_enum.value: {
                "name": preset["name"],
                "description": preset["description"],
                "filter": preset["filter"]
            }
            for type_enum, preset in self.echo_presets.items()
        }

def main():
    """Test inner voice processor"""
    processor = InnerVoiceProcessor()
    
    if not processor.ffmpeg_available:
        print("❌ FFmpeg not available - cannot test inner voice")
        print("💡 Install FFmpeg to use this feature")
        return
    
    print("🎭 Inner Voice Processor - Available Types:")
    print("=" * 50)
    
    types = processor.get_available_types()
    for type_id, info in types.items():
        print(f"\n🎪 {type_id.upper()}:")
        print(f"   📝 Name: {info['name']}")
        print(f"   📖 Description: {info['description']}")
        print(f"   🎛️ Filter: {info['filter']}")
    
    # Test với file có sẵn nếu có
    test_files = [
        "./test_audio_output/emotion_preview_neutral.wav",
        "./test_audio_output/emotion_preview_contemplative.wav"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n🧪 Testing với: {test_file}")
            
            for inner_type in InnerVoiceType:
                output_path = f"./test_inner_voice_{inner_type.value}.mp3"
                result = processor.process_inner_voice(test_file, output_path, inner_type)
                
                if result["success"]:
                    print(f"   ✅ {inner_type.value}: {result['preset_name']}")
                else:
                    print(f"   ❌ {inner_type.value}: {result.get('error', 'Unknown error')}")
            break
    else:
        print("\n📁 No test audio files found")
        print("💡 Create some audio first to test inner voice effects")

if __name__ == '__main__':
=======
#!/usr/bin/env python3
"""
[THEATER] INNER VOICE PROCESSOR
=======================

Xử lý hiệu ứng inner voice (thoại nội tâm) cho Voice Studio.
Sử dụng FFmpeg để tạo echo effects cho dialogue với inner_voice: true
"""

import os
import subprocess
import tempfile
from enum import Enum
from typing import Dict, Any, Optional
from pathlib import Path

class InnerVoiceType(Enum):
    """Các loại inner voice effects"""
    LIGHT = "light"      # Nội tâm nhẹ - tự sự, tâm sự
    DEEP = "deep"        # Nội tâm sâu - căng thẳng, hồi tưởng  
    DREAMY = "dreamy"    # Nội tâm cách âm - xa thực tại, mơ hồ

class InnerVoiceProcessor:
    """Processor cho inner voice effects"""
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        
        # Default echo presets cho từng loại inner voice
        self.echo_presets = {
            InnerVoiceType.LIGHT: {
                "name": "Nội tâm nhẹ",
                "description": "Tự sự, tâm sự - phù hợp nữ trẻ, nhân vật suy tư",
                "filter": "aecho=0.6:0.5:50:0.3",
                "suffix": "_inner_light"
            },
            InnerVoiceType.DEEP: {
                "name": "Nội tâm sâu", 
                "description": "Căng thẳng, hồi tưởng - phù hợp độc thoại nam, giọng nặng trĩu",
                "filter": "aecho=0.7:0.6:150:0.4|0.3",
                "suffix": "_inner_deep"
            },
            InnerVoiceType.DREAMY: {
                "name": "Nội tâm cách âm",
                "description": "Xa thực tại, mơ hồ - phù hợp cảnh mộng, mất phương hướng", 
                "filter": "volume=0.8,aecho=0.5:0.6:300:0.4,lowpass=f=3000",
                "suffix": "_inner_dreamy"
            }
        }
        
        # Load custom settings từ config file
        self.load_config_from_file()
    
    def _check_ffmpeg(self) -> bool:
        """Check nếu FFmpeg available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True,
                         stderr=subprocess.DEVNULL)  # Suppress stderr
            return True
        except FileNotFoundError:
            return False
    
    def load_config_from_file(self):
        """Load custom inner voice settings từ unified_emotions.json"""
        try:
            config_path = "configs/emotions/unified_emotions.json"
            
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if "inner_voice_config" in config and "presets" in config["inner_voice_config"]:
                    presets = config["inner_voice_config"]["presets"]
                    
                    print(f"[THEATER] LOADING InnerVoiceProcessor config from file...")
                    
                    for type_name, preset_data in presets.items():
                        try:
                            type_enum = InnerVoiceType(type_name.lower())
                            
                            if type_enum in self.echo_presets:
                                # Update với settings từ file
                                if "filter" in preset_data:
                                    self.echo_presets[type_enum]["filter"] = preset_data["filter"]
                                    print(f"   [OK] {type_name}: filter='{preset_data['filter']}'")
                                
                                # Store UI params cho debugging
                                for key in ["delay", "decay", "gain"]:
                                    if key in preset_data:
                                        self.echo_presets[type_enum][key] = preset_data[key]
                                        
                        except ValueError:
                            print(f"   [WARNING] Unknown inner voice type: {type_name}")
                    
                    print(f"[OK] InnerVoiceProcessor config loaded from {config_path}")
                else:
                    print(f"[CLIPBOARD] No inner_voice_config found, using defaults")
            else:
                print(f"[CLIPBOARD] Config file not found, using default presets")
                
        except Exception as e:
            print(f"[WARNING] Warning: Could not load inner voice config: {e}")
            print(f"[CLIPBOARD] Using default presets")
    
    def get_inner_voice_type(self, character_name: str, emotion: str, gender: str = "neutral") -> InnerVoiceType:
        """Tự động chọn loại inner voice dựa trên character và emotion"""
        
        # Logic auto-select dựa trên emotion và gender
        emotion_lower = emotion.lower()
        
        # Nội tâm sâu - emotions căng thẳng, nặng nề
        deep_emotions = [
            "sad", "angry", "anxious", "worried", "frustrated", "disappointed",
            "desperate", "commanding", "fierce", "dramatic", "mysterious", "suspenseful"
        ]
        
        # Nội tâm cách âm - emotions mơ hồ, xa vời
        dreamy_emotions = [
            "whisper", "soft", "contemplative", "sleepy", "confused", "bewildered",
            "romantic", "innocent", "gentle"
        ]
        
        # Kiểm tra emotion
        if any(e in emotion_lower for e in deep_emotions):
            return InnerVoiceType.DEEP
        elif any(e in emotion_lower for e in dreamy_emotions):
            return InnerVoiceType.DREAMY
        else:
            # Default: nội tâm nhẹ cho emotions bình thường
            return InnerVoiceType.LIGHT
    
    def set_custom_preset(self, type_name: str, params: dict):
        """Cập nhật preset cho 1 type từ UI/config"""
        try:
            # Convert string to enum
            type_enum = InnerVoiceType(type_name.lower())
            
            if type_enum in self.echo_presets:
                print(f"[EMOJI] UPDATING {type_name} preset:")
                
                # Tạo filter string từ UI params
                if all(key in params for key in ["delay", "decay", "gain"]):
                    # Build FFmpeg filter từ UI params  
                    delay = params["delay"]
                    decay = params["decay"] 
                    gain = params["gain"]
                    custom_filter = params.get("filter", f"aecho={gain}:{decay}:{delay}:{decay}")
                    
                    print(f"   [STATS] delay={delay}, decay={decay}, gain={gain}")
                    print(f"   [EMOJI] filter='{custom_filter}'")
                    
                    # Update preset với UI values
                    self.echo_presets[type_enum].update({
                        "filter": custom_filter,
                        "description": f"{self.echo_presets[type_enum]['description']} - từ UI",
                        **params  # Include all UI params
                    })
                    
                    print(f"[OK] Updated {type_name} preset successfully")
                else:
                    print(f"[WARNING] Missing required params for {type_name}")
                    
        except ValueError as e:
            print(f"[EMOJI] Invalid inner voice type: {type_name} - {e}")
        except Exception as e:
            print(f"[EMOJI] Error updating preset {type_name}: {e}")
    
    def process_inner_voice(self, input_path: str, output_path: str, 
                          inner_voice_type: InnerVoiceType = InnerVoiceType.LIGHT) -> Dict[str, Any]:
        """Process audio file để tạo inner voice effect"""
        
        if not self.ffmpeg_available:
            return {
                "success": False,
                "error": "FFmpeg not available - cannot process inner voice"
            }
        
        if not os.path.exists(input_path):
            return {
                "success": False,
                "error": f"Input file not found: {input_path}"
            }
        
        try:
            # Ưu tiên preset custom nếu có
            preset = self.echo_presets.get(inner_voice_type)
            
            if preset is None:
                preset = self.echo_presets[self.get_inner_voice_type(character_name, emotion)]
            
            print(f"[THEATER] PROCESSING INNER VOICE: {os.path.basename(input_path)}")
            print(f"   [CIRCUS] Type: {preset['name']}")
            print(f"   [EDIT] Effect: {preset['description']}")
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-i', input_path,
                '-af', preset['filter'],
                '-y',  # Overwrite output
                output_path
            ]
            
            # Execute FFmpeg (suppress stderr noise)
            result = subprocess.run(cmd, capture_output=True, text=True,
                                  stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                print(f"[OK] INNER VOICE SUCCESS!")
                print(f"   [FOLDER] Original: {os.path.basename(input_path)}")
                print(f"   [FOLDER] Processed: {os.path.basename(output_path)}")
                
                # Get file info
                original_size = os.path.getsize(input_path)
                processed_size = os.path.getsize(output_path)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "inner_voice_type": inner_voice_type.value,
                    "preset_name": preset['name'],
                    "original_size": original_size,
                    "processed_size": processed_size,
                    "filter": preset['filter']
                }
            else:
                return {
                    "success": False,
                    "error": f"FFmpeg failed: {result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing inner voice: {str(e)}"
            }
    
    def process_dialogue_with_inner_voice(self, input_path: str, dialogue_data: Dict[str, Any],
                                        output_dir: str) -> Dict[str, Any]:
        """Process một dialogue với inner voice flag"""
        
        # Check nếu có inner voice flag
        if not dialogue_data.get("inner_voice", False):
            # Không có inner voice, return original path
            return {
                "success": True,
                "output_path": input_path,
                "inner_voice_applied": False
            }
        
        # Determine inner voice type
        character_id = dialogue_data.get("speaker", "unknown")
        emotion = dialogue_data.get("emotion", "neutral")
        
        # Có thể override type bằng inner_voice_type field
        if "inner_voice_type" in dialogue_data:
            type_str = dialogue_data["inner_voice_type"].lower()
            inner_voice_type = {
                "light": InnerVoiceType.LIGHT,
                "deep": InnerVoiceType.DEEP, 
                "dreamy": InnerVoiceType.DREAMY
            }.get(type_str, InnerVoiceType.LIGHT)
        else:
            # Auto-detect based on emotion
            inner_voice_type = self.get_inner_voice_type(character_id, emotion)
        
        # Generate output filename
        input_name = Path(input_path).stem
        preset = self.echo_presets[inner_voice_type]
        output_name = f"{input_name}{preset['suffix']}.mp3"
        output_path = os.path.join(output_dir, output_name)
        
        # Process inner voice
        result = self.process_inner_voice(input_path, output_path, inner_voice_type)
        
        if result["success"]:
            result["inner_voice_applied"] = True
            result["original_path"] = input_path
        
        return result
    
    def get_available_types(self) -> Dict[str, Dict[str, str]]:
        """Get danh sách available inner voice types"""
        return {
            type_enum.value: {
                "name": preset["name"],
                "description": preset["description"],
                "filter": preset["filter"]
            }
            for type_enum, preset in self.echo_presets.items()
        }

def main():
    """Test inner voice processor"""
    processor = InnerVoiceProcessor()
    
    if not processor.ffmpeg_available:
        print("[EMOJI] FFmpeg not available - cannot test inner voice")
        print("[IDEA] Install FFmpeg to use this feature")
        return
    
    print("[THEATER] Inner Voice Processor - Available Types:")
    print("=" * 50)
    
    types = processor.get_available_types()
    for type_id, info in types.items():
        print(f"\n[CIRCUS] {type_id.upper()}:")
        print(f"   [EDIT] Name: {info['name']}")
        print(f"   [BOOK] Description: {info['description']}")
        print(f"   [EMOJI] Filter: {info['filter']}")
    
    # Test với file có sẵn nếu có
    test_files = [
        "./test_audio_output/emotion_preview_neutral.wav",
        "./test_audio_output/emotion_preview_contemplative.wav"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n[TEST] Testing với: {test_file}")
            
            for inner_type in InnerVoiceType:
                output_path = f"./test_inner_voice_{inner_type.value}.mp3"
                result = processor.process_inner_voice(test_file, output_path, inner_type)
                
                if result["success"]:
                    print(f"   [OK] {inner_type.value}: {result['preset_name']}")
                else:
                    print(f"   [EMOJI] {inner_type.value}: {result.get('error', 'Unknown error')}")
            break
    else:
        print("\n[FOLDER] No test audio files found")
        print("[IDEA] Create some audio first to test inner voice effects")

if __name__ == '__main__':
>>>>>>> Stashed changes
    main() 