#!/usr/bin/env python3
"""
🎭 EMOTION CONFIGURATION MANAGER
================================

Quản lý và điều chỉnh thông số cảm xúc cho Voice Studio.
Cho phép tạo, chỉnh sửa và lưu các cấu hình cảm xúc tùy chỉnh.

Features:
- 25+ predefined emotions với parameters tối ưu
- Custom emotion configurations
- Thông số chi tiết: exaggeration, cfg_weight, temperature, speed
- Lưu/load emotion presets 
- Export/import emotion configs
"""

import os
import json
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import copy

logger = logging.getLogger(__name__)

@dataclass
class EmotionParameters:
    """Emotion parameters configuration"""
    name: str
    exaggeration: float = 1.0      # 0.0-2.5 (emotion intensity)
    cfg_weight: float = 0.5        # 0.0-1.0 (voice guidance strength)
    temperature: float = 0.7       # 0.1-1.5 (creativity/variability)
    speed: float = 1.0             # 0.5-2.0 (speaking speed)
    description: str = ""
    category: str = "neutral"      # neutral, positive, negative, dramatic, special
    voice_tone: str = "balanced"   # soft, balanced, strong, intense
    use_case: str = "general"      # general, narration, dialogue, character

@dataclass
class EmotionPreset:
    """Emotion preset configuration"""
    name: str
    description: str
    emotions: Dict[str, EmotionParameters]
    created_date: str = ""
    author: str = "User"
    version: str = "1.0"

class EmotionConfigManager:
    """
    🎭 EMOTION CONFIGURATION MANAGER
    
    Quản lý toàn bộ emotion configurations:
    - Predefined emotions (25+ emotions)
    - Custom user emotions  
    - Emotion presets
    - Parameter optimization
    """
    
    def __init__(self, config_dir: str = "configs/emotions"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Emotion storage
        self.default_emotions = {}
        self.custom_emotions = {}
        self.emotion_presets = {}
        
        # Initialize default emotions
        self.setup_default_emotions()
        
        # Load custom configs
        self.load_custom_emotions()
        self.load_emotion_presets()
    
    def setup_default_emotions(self):
        """Setup default 25+ emotion configurations với parameters tối ưu"""
        
        default_configs = [
            # === NEUTRAL EMOTIONS ===
            EmotionParameters(
                name="neutral", exaggeration=0.5, cfg_weight=0.5, temperature=0.7, speed=1.0,
                description="Balanced, objective narration", category="neutral", 
                voice_tone="balanced", use_case="narration"
            ),
            EmotionParameters(
                name="calm", exaggeration=0.5, cfg_weight=0.5, temperature=0.5, speed=0.9,
                description="Peaceful, composed speech", category="neutral",
                voice_tone="soft", use_case="general"
            ),
            EmotionParameters(
                name="contemplative", exaggeration=0.4, cfg_weight=0.4, temperature=0.6, speed=0.8,
                description="Deep inner thoughts", category="neutral",
                voice_tone="soft", use_case="narration"
            ),
            
            # === POSITIVE EMOTIONS ===
            EmotionParameters(
                name="happy", exaggeration=1.35, cfg_weight=0.55, temperature=0.8, speed=1.1,
                description="General joy, positive mood", category="positive",
                voice_tone="balanced", use_case="dialogue"
            ),
            EmotionParameters(
                name="excited", exaggeration=1.6, cfg_weight=0.6, temperature=0.9, speed=1.3,
                description="High energy, enthusiastic", category="positive",
                voice_tone="strong", use_case="character"
            ),
            EmotionParameters(
                name="friendly", exaggeration=1.2, cfg_weight=0.5, temperature=0.8, speed=1.0,
                description="Warm, welcoming tone", category="positive",
                voice_tone="balanced", use_case="general"
            ),
            EmotionParameters(
                name="gentle", exaggeration=0.35, cfg_weight=0.35, temperature=0.6, speed=0.9,
                description="Soft, tender expressions", category="positive",
                voice_tone="soft", use_case="character"
            ),
            EmotionParameters(
                name="confident", exaggeration=1.5, cfg_weight=0.6, temperature=0.8, speed=1.0,
                description="Self-assured, determined", category="positive",
                voice_tone="strong", use_case="character"
            ),
            EmotionParameters(
                name="persuasive", exaggeration=1.35, cfg_weight=0.55, temperature=0.8, speed=1.0,
                description="Convincing argument", category="positive",
                voice_tone="balanced", use_case="dialogue"
            ),
            
            # === NEGATIVE EMOTIONS ===
            EmotionParameters(
                name="sad", exaggeration=0.4, cfg_weight=0.35, temperature=0.6, speed=0.8,
                description="General sadness", category="negative",
                voice_tone="soft", use_case="character"
            ),
            EmotionParameters(
                name="angry", exaggeration=2.0, cfg_weight=0.7, temperature=0.9, speed=1.2,
                description="General anger", category="negative",
                voice_tone="intense", use_case="character"
            ),
            EmotionParameters(
                name="sarcastic", exaggeration=0.85, cfg_weight=0.45, temperature=0.8, speed=1.1,
                description="Mocking, ironic tone", category="negative",
                voice_tone="balanced", use_case="dialogue"
            ),
            
            # === DRAMATIC EMOTIONS ===
            EmotionParameters(
                name="dramatic", exaggeration=1.8, cfg_weight=0.6, temperature=1.0, speed=1.0,
                description="Theatrical, intense", category="dramatic",
                voice_tone="intense", use_case="character"
            ),
            EmotionParameters(
                name="mysterious", exaggeration=1.4, cfg_weight=0.45, temperature=0.7, speed=0.9,
                description="Enigmatic, secretive", category="dramatic",
                voice_tone="balanced", use_case="narration"
            ),
            EmotionParameters(
                name="determined", exaggeration=1.7, cfg_weight=0.65, temperature=0.8, speed=1.1,
                description="Strong will, focused", category="dramatic",
                voice_tone="strong", use_case="character"
            ),
            
            # === SPECIAL EMOTIONS ===
            EmotionParameters(
                name="whisper", exaggeration=0.3, cfg_weight=0.3, temperature=0.4, speed=0.7,
                description="Intimate, secretive tone", category="special",
                voice_tone="soft", use_case="character"
            ),
            EmotionParameters(
                name="innocent", exaggeration=1.2, cfg_weight=0.5, temperature=0.7, speed=1.0,
                description="Childlike, naive expression", category="special",
                voice_tone="soft", use_case="character"
            ),
            EmotionParameters(
                name="cold", exaggeration=0.35, cfg_weight=0.65, temperature=0.5, speed=1.0,
                description="Emotionless, distant", category="special",
                voice_tone="balanced", use_case="character"
            ),
        ]
        
        # Store default emotions
        for emotion in default_configs:
            self.default_emotions[emotion.name] = emotion
    
    def get_all_emotions(self) -> Dict[str, EmotionParameters]:
        """Get all available emotions (default + custom)"""
        all_emotions = self.default_emotions.copy()
        all_emotions.update(self.custom_emotions)
        return all_emotions
    
    def get_emotions_by_category(self, category: str) -> Dict[str, EmotionParameters]:
        """Get emotions filtered by category"""
        all_emotions = self.get_all_emotions()
        return {
            name: emotion for name, emotion in all_emotions.items()
            if emotion.category == category
        }
    
    def get_emotion_categories(self) -> List[str]:
        """Get all available emotion categories"""
        all_emotions = self.get_all_emotions()
        categories = set(emotion.category for emotion in all_emotions.values())
        return sorted(list(categories))
    
    def create_custom_emotion(
        self, 
        name: str,
        exaggeration: float = 1.0,
        cfg_weight: float = 0.5,
        temperature: float = 0.7,
        speed: float = 1.0,
        description: str = "",
        category: str = "custom",
        voice_tone: str = "balanced",
        use_case: str = "general"
    ) -> EmotionParameters:
        """Create a new custom emotion"""
        
        # Validate parameters
        exaggeration = max(0.0, min(2.5, exaggeration))
        cfg_weight = max(0.0, min(1.0, cfg_weight))
        temperature = max(0.1, min(1.5, temperature))
        speed = max(0.5, min(2.0, speed))
        
        emotion = EmotionParameters(
            name=name,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature,
            speed=speed,
            description=description,
            category=category,
            voice_tone=voice_tone,
            use_case=use_case
        )
        
        self.custom_emotions[name] = emotion
        self.save_custom_emotions()
        
        logger.info(f"Created custom emotion: {name}")
        return emotion
    
    def modify_emotion(
        self,
        name: str,
        **kwargs
    ) -> Optional[EmotionParameters]:
        """Modify an existing emotion (custom only)"""
        
        if name not in self.custom_emotions:
            # Create copy from default if exists
            if name in self.default_emotions:
                self.custom_emotions[name] = copy.deepcopy(self.default_emotions[name])
            else:
                logger.error(f"Emotion '{name}' not found")
                return None
        
        emotion = self.custom_emotions[name]
        
        # Update parameters
        for param, value in kwargs.items():
            if hasattr(emotion, param):
                # Validate parameter ranges
                if param == "exaggeration":
                    value = max(0.0, min(2.5, value))
                elif param == "cfg_weight":
                    value = max(0.0, min(1.0, value))
                elif param == "temperature":
                    value = max(0.1, min(1.5, value))
                elif param == "speed":
                    value = max(0.5, min(2.0, value))
                
                setattr(emotion, param, value)
        
        self.save_custom_emotions()
        logger.info(f"Modified emotion: {name}")
        return emotion
    
    def delete_custom_emotion(self, name: str) -> bool:
        """Delete a custom emotion"""
        if name in self.custom_emotions:
            del self.custom_emotions[name]
            self.save_custom_emotions()
            logger.info(f"Deleted custom emotion: {name}")
            return True
        return False
    
    def create_emotion_preset(
        self,
        preset_name: str,
        emotions: List[str],
        description: str = ""
    ) -> EmotionPreset:
        """Create an emotion preset from selected emotions"""
        
        all_emotions = self.get_all_emotions()
        preset_emotions = {}
        
        for emotion_name in emotions:
            if emotion_name in all_emotions:
                preset_emotions[emotion_name] = all_emotions[emotion_name]
        
        preset = EmotionPreset(
            name=preset_name,
            description=description,
            emotions=preset_emotions,
            created_date=str(Path().resolve())
        )
        
        self.emotion_presets[preset_name] = preset
        self.save_emotion_presets()
        
        logger.info(f"Created emotion preset: {preset_name}")
        return preset
    
    def get_emotion_preset(self, preset_name: str) -> Optional[EmotionPreset]:
        """Get an emotion preset by name"""
        return self.emotion_presets.get(preset_name)
    
    def get_all_emotion_presets(self) -> Dict[str, EmotionPreset]:
        """Get all emotion presets"""
        return self.emotion_presets.copy()
    
    def delete_emotion_preset(self, preset_name: str) -> bool:
        """Delete an emotion preset"""
        if preset_name in self.emotion_presets:
            del self.emotion_presets[preset_name]
            self.save_emotion_presets()
            logger.info(f"Deleted emotion preset: {preset_name}")
            return True
        return False
    
    def get_emotion_parameters(self, emotion_name: str) -> Optional[Dict[str, float]]:
        """Get emotion parameters as dict for TTS generation"""
        all_emotions = self.get_all_emotions()
        
        if emotion_name in all_emotions:
            emotion = all_emotions[emotion_name]
            return {
                "exaggeration": emotion.exaggeration,
                "cfg_weight": emotion.cfg_weight,
                "temperature": emotion.temperature,
                "speed": emotion.speed
            }
        
        # Fallback to neutral
        if "neutral" in all_emotions:
            emotion = all_emotions["neutral"]
            return {
                "exaggeration": emotion.exaggeration,
                "cfg_weight": emotion.cfg_weight,
                "temperature": emotion.temperature,
                "speed": emotion.speed
            }
        
        # Ultimate fallback
        return {
            "exaggeration": 1.0,
            "cfg_weight": 0.5,
            "temperature": 0.7,
            "speed": 1.0
        }
    
    def save_custom_emotions(self):
        """Save custom emotions to file"""
        try:
            config_file = self.config_dir / "custom_emotions.json"
            emotions_data = {
                name: asdict(emotion) for name, emotion in self.custom_emotions.items()
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(emotions_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save custom emotions: {e}")
    
    def load_custom_emotions(self):
        """Load custom emotions from file"""
        try:
            config_file = self.config_dir / "custom_emotions.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    emotions_data = json.load(f)
                
                for name, data in emotions_data.items():
                    self.custom_emotions[name] = EmotionParameters(**data)
                    
                logger.info(f"Loaded {len(self.custom_emotions)} custom emotions")
                
        except Exception as e:
            logger.error(f"Failed to load custom emotions: {e}")
    
    def save_emotion_presets(self):
        """Save emotion presets to file"""
        try:
            config_file = self.config_dir / "emotion_presets.json"
            presets_data = {}
            
            for name, preset in self.emotion_presets.items():
                preset_dict = asdict(preset)
                # Convert emotions to serializable format
                preset_dict["emotions"] = {
                    emotion_name: asdict(emotion) 
                    for emotion_name, emotion in preset.emotions.items()
                }
                presets_data[name] = preset_dict
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(presets_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save emotion presets: {e}")
    
    def load_emotion_presets(self):
        """Load emotion presets from file"""
        try:
            config_file = self.config_dir / "emotion_presets.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    presets_data = json.load(f)
                
                for name, data in presets_data.items():
                    # Reconstruct emotions
                    emotions = {
                        emotion_name: EmotionParameters(**emotion_data)
                        for emotion_name, emotion_data in data["emotions"].items()
                    }
                    
                    preset = EmotionPreset(
                        name=data["name"],
                        description=data["description"],
                        emotions=emotions,
                        created_date=data.get("created_date", ""),
                        author=data.get("author", "User"),
                        version=data.get("version", "1.0")
                    )
                    
                    self.emotion_presets[name] = preset
                    
                logger.info(f"Loaded {len(self.emotion_presets)} emotion presets")
                
        except Exception as e:
            logger.error(f"Failed to load emotion presets: {e}")
    
    def import_emotion_config(self, input_path: str) -> bool:
        """Import emotion configurations from file"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Import custom emotions
            if "custom_emotions" in import_data:
                for name, data in import_data["custom_emotions"].items():
                    self.custom_emotions[name] = EmotionParameters(**data)
            
            # Import emotion presets
            if "emotion_presets" in import_data:
                for name, data in import_data["emotion_presets"].items():
                    # Reconstruct emotions
                    emotions = {
                        emotion_name: EmotionParameters(**emotion_data)
                        for emotion_name, emotion_data in data["emotions"].items()
                    }
                    
                    preset = EmotionPreset(
                        name=data["name"],
                        description=data["description"],
                        emotions=emotions,
                        created_date=data.get("created_date", ""),
                        author=data.get("author", "User"),
                        version=data.get("version", "1.0")
                    )
                    
                    self.emotion_presets[name] = preset
            
            # Save imported data
            self.save_custom_emotions()
            self.save_emotion_presets()
            
            logger.info(f"Imported emotion config from: {input_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import emotion config: {e}")
            return False
    
    def export_emotion_config(self, output_path: str):
        """Export all emotion configurations"""
        try:
            export_data = {
                "default_emotions": {
                    name: asdict(emotion) for name, emotion in self.default_emotions.items()
                },
                "custom_emotions": {
                    name: asdict(emotion) for name, emotion in self.custom_emotions.items()
                },
                "emotion_presets": {
                    name: {
                        **asdict(preset),
                        "emotions": {
                            emotion_name: asdict(emotion)
                            for emotion_name, emotion in preset.emotions.items()
                        }
                    } for name, preset in self.emotion_presets.items()
                },
                "metadata": {
                    "total_emotions": len(self.get_all_emotions()),
                    "total_presets": len(self.emotion_presets),
                    "version": "1.0",
                    "export_timestamp": time.time(),
                    "system": "Voice Studio Emotion Manager"
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported emotion config to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export emotion config: {e}")
    
    def get_emotion_statistics(self) -> Dict[str, Any]:
        """Get emotion usage statistics"""
        all_emotions = self.get_all_emotions()
        
        categories = {}
        voice_tones = {}
        use_cases = {}
        
        for emotion in all_emotions.values():
            # Count by category
            categories[emotion.category] = categories.get(emotion.category, 0) + 1
            
            # Count by voice tone
            voice_tones[emotion.voice_tone] = voice_tones.get(emotion.voice_tone, 0) + 1
            
            # Count by use case
            use_cases[emotion.use_case] = use_cases.get(emotion.use_case, 0) + 1
        
        return {
            "total_emotions": len(all_emotions),
            "default_emotions": len(self.default_emotions),
            "custom_emotions": len(self.custom_emotions),
            "total_presets": len(self.emotion_presets),
            "categories": categories,
            "voice_tones": voice_tones,
            "use_cases": use_cases
        }


# Global emotion manager instance
emotion_manager = EmotionConfigManager()


def get_emotion_parameters(emotion_name: str) -> Dict[str, float]:
    """Convenience function to get emotion parameters"""
    return emotion_manager.get_emotion_parameters(emotion_name)


def get_all_emotions() -> Dict[str, EmotionParameters]:
    """Convenience function to get all emotions"""
    return emotion_manager.get_all_emotions() 