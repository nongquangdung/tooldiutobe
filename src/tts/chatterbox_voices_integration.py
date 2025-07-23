#!/usr/bin/env python3
"""
[MIC] CHATTERBOX TTS VOICES INTEGRATION
=====================================

Integration của Chatterbox TTS Server voices vào Voice Studio system.
Cung cấp 28 predefined voices chất lượng cao từ Chatterbox model.

Chatterbox Repository: https://github.com/devnen/Chatterbox-TTS-Server
"""

import os
import sys
import json
import requests
import tempfile
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Add src directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# [THEATER] Unified Emotion System Import
from core.unified_emotion_system import unified_emotion_system, get_emotion_parameters


logger = logging.getLogger(__name__)

@dataclass
class ChatterboxVoice:
    """Chatterbox voice profile data"""
    voice_id: str
    name: str
    gender: str
    language: str = "en"
    description: str = ""
    sample_rate: int = 24000
    quality_rating: float = 9.0  # High quality for Chatterbox voices
    
@dataclass
class ChatterboxConfig:
    """Chatterbox TTS Server configuration"""
    server_url: str = "http://localhost:8004"
    api_endpoint: str = "/tts"
    timeout: int = 60
    quality_mode: str = "high"
    chunk_size: int = 250

class ChatterboxVoicesManager:
    """
    [MIC] CHATTERBOX VOICES INTEGRATION MANAGER
    
    Quản lý integration với Chatterbox TTS Server để:
    - Load 28 predefined voices từ Chatterbox
    - Generate audio với voice cloning capabilities
    - Tích hợp với Voice Studio existing system
    """
    
    def __init__(self, config: ChatterboxConfig = None):
        self.config = config or ChatterboxConfig()
        self.voices_cache = {}
        self.voices_directory = Path("voices")
        self.setup_predefined_voices()
        
    def setup_predefined_voices(self):
        """Setup predefined voices từ thư mục voices/ directory"""
        try:
            if not self.voices_directory.exists():
                # [SEARCH] Try fallback to project-root voices directory
                alt_dir = Path(__file__).resolve().parent.parent.parent / "voices"
                if alt_dir.exists():
                    logger.info(f"Voices directory fallback found at: {alt_dir}")
                    self.voices_directory = alt_dir
                else:
                    logger.warning(f"Voices directory not found: {self.voices_directory} or fallback {alt_dir}")
                    return
            
            # Gender classification based on common name patterns
            # Này dựa trên analysis các voices có sẵn từ Chatterbox
            female_names = {
                'abigail', 'alice', 'cora', 'elena', 'emily', 
                'gianna', 'jade', 'layla', 'olivia', 'taylor'
            }
            
            male_names = {
                'adrian', 'alexander', 'austin', 'axel', 'connor',
                'eli', 'everett', 'gabriel', 'henry', 'ian', 
                'jeremiah', 'jordan', 'julian', 'leonardo', 
                'michael', 'miles', 'ryan', 'thomas'
            }
            
            # Voice descriptions mapping
            voice_descriptions = {
                'abigail': "Warm and professional female voice",
                'alice': "Clear and articulate young female voice",
                'cora': "Sophisticated mature female voice", 
                'elena': "Expressive and melodic female voice",
                'emily': "Friendly and approachable female voice",
                'gianna': "Dynamic and energetic female voice",
                'jade': "Calm and soothing female voice",
                'layla': "Rich and deep female voice",
                'olivia': "Elegant and refined female voice",
                'taylor': "Versatile and natural female voice",
                'adrian': "Strong and confident male voice",
                'alexander': "Distinguished and authoritative male voice",
                'austin': "Casual and friendly male voice",
                'axel': "Dynamic and powerful male voice",
                'connor': "Young and energetic male voice",
                'eli': "Wise and mature male voice",
                'everett': "Professional and clear male voice",
                'gabriel': "Smooth and charismatic male voice",
                'henry': "Reliable and steady male voice",
                'ian': "Articulate and precise male voice",
                'jeremiah': "Deep and resonant male voice",
                'jordan': "Versatile and adaptable male voice",
                'julian': "Sophisticated and cultured male voice",
                'leonardo': "Creative and expressive male voice",
                'michael': "Classic and dependable male voice",
                'miles': "Modern and contemporary male voice",
                'ryan': "Energetic and upbeat male voice",
                'thomas': "Traditional and trustworthy male voice"
            }
            
            # Scan voices directory for .wav files
            voice_files = list(self.voices_directory.glob("*.wav"))
            
            if not voice_files:
                logger.warning(f"No .wav files found in {self.voices_directory}")
                return
                
            for voice_file in voice_files:
                # Extract voice_id from filename (remove .wav extension)
                voice_id = voice_file.stem.lower()
                voice_name = voice_file.stem  # Keep original case for display
                
                # Determine gender
                if voice_id in female_names:
                    gender = "female"
                elif voice_id in male_names:
                    gender = "male"
                else:
                    # Default fallback based on common naming patterns
                    gender = "female" if voice_id.endswith(('a', 'e', 'i')) else "male"
                
                # Get description
                description = voice_descriptions.get(voice_id, f"High-quality {gender} voice")
                
                # Create voice profile
                self.voices_cache[voice_id] = ChatterboxVoice(
                    voice_id=voice_id,
                    name=voice_name,
                    gender=gender,
                    description=description
                )
                
                logger.debug(f"Loaded voice: {voice_name} ({gender})")
            
            logger.info(f"Successfully loaded {len(self.voices_cache)} predefined voices from {self.voices_directory}")
            
        except Exception as e:
            logger.error(f"Error setting up predefined voices: {e}")
            self.voices_cache = {}  # Reset cache on error
    
    def get_available_voices(self) -> Dict[str, ChatterboxVoice]:
        """Get all available Chatterbox voices"""
        return self.voices_cache.copy()
    
    def get_voices_by_gender(self, gender: str) -> Dict[str, ChatterboxVoice]:
        """Get voices filtered by gender"""
        return {
            voice_id: voice for voice_id, voice in self.voices_cache.items()
            if voice.gender.lower() == gender.lower()
        }
    
    def generate_audio_chatterbox(
        self,
        text: str,
        voice_id: str,
        output_path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate audio using Chatterbox TTS Server
        
        Args:
            text: Text to synthesize
            voice_id: Chatterbox voice ID 
            output_path: Where to save generated audio
            **kwargs: Additional parameters (temperature, speed, etc.)
        
        Returns:
            Dict with generation results and metadata
        """
        try:
            # Check if voice exists
            if voice_id not in self.voices_cache:
                raise ValueError(f"Voice '{voice_id}' not found in Chatterbox voices")
            
            voice = self.voices_cache[voice_id]
            
            # Prepare request data for Chatterbox API
            request_data = {
                "text": text,
                "voice_mode": "predefined",
                "predefined_voice_id": f"{voice_id}.wav",  # Chatterbox expects .wav extension
                "output_format": "wav",
                "split_text": len(text) > self.config.chunk_size,
                "chunk_size": self.config.chunk_size,
                "temperature": kwargs.get("temperature", 0.7),
                "speed_factor": kwargs.get("speed", 1.0),
                "cfg_weight": kwargs.get("cfg_weight", 3.0),
                "seed": kwargs.get("seed", -1),  # -1 for random
                "language": kwargs.get("language", "en")
            }
            
            # Optional advanced parameters
            if "exaggeration" in kwargs:
                request_data["exaggeration"] = kwargs["exaggeration"]
            
            # Make request to Chatterbox TTS Server
            response = requests.post(
                f"{self.config.server_url}{self.config.api_endpoint}",
                json=request_data,
                timeout=self.config.timeout,
                stream=True
            )
            
            if response.status_code == 200:
                # Save audio to output path
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Get file info
                file_size = os.path.getsize(output_path)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "voice_used": voice.name,
                    "voice_id": voice_id,
                    "text_length": len(text),
                    "file_size": file_size,
                    "quality_rating": voice.quality_rating,
                    "generation_params": request_data,
                    "server_url": self.config.server_url
                }
            else:
                error_msg = f"Chatterbox TTS Server error: {response.status_code}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "voice_id": voice_id
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection to Chatterbox TTS Server failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "voice_id": voice_id
            }
        except Exception as e:
            error_msg = f"Chatterbox generation failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "voice_id": voice_id
            }
    
    def test_chatterbox_connection(self) -> Dict[str, Any]:
        """Test connection to Chatterbox TTS Server"""
        try:
            # Try to get server status
            health_endpoint = f"{self.config.server_url}/api/ui/initial-data"
            response = requests.get(health_endpoint, timeout=10)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "Chatterbox TTS Server is online",
                    "server_url": self.config.server_url,
                    "available_voices": len(self.voices_cache)
                }
            else:
                return {
                    "success": False,
                    "status": f"Server responded with status {response.status_code}",
                    "server_url": self.config.server_url
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status": f"Connection failed: {str(e)}",
                "server_url": self.config.server_url,
                "suggestion": "Make sure Chatterbox TTS Server is running on localhost:8004"
            }
    
    def get_voice_recommendations(self, character_type: str = None) -> List[str]:
        """
        Get voice recommendations based on character type
        
        Args:
            character_type: "narrator", "hero", "villain", "child", "elderly", etc.
        
        Returns:
            List of recommended voice IDs
        """
        recommendations = {
            "narrator": ["thomas", "olivia", "henry", "alice"],
            "hero": ["gabriel", "emily", "alexander", "taylor"],
            "villain": ["axel", "layla", "jeremiah", "jade"],
            "child": ["connor", "gianna", "austin", "emily"],
            "elderly": ["eli", "cora", "thomas", "elena"],
            "professional": ["adrian", "olivia", "everett", "alice"],
            "friendly": ["ryan", "taylor", "austin", "emily"],
            "authoritative": ["alexander", "elena", "henry", "olivia"],
            "mysterious": ["ian", "jade", "leonardo", "layla"]
        }
        
        if character_type and character_type.lower() in recommendations:
            return recommendations[character_type.lower()]
        
        # Default popular voices
        return ["gabriel", "olivia", "alexander", "emily", "thomas", "taylor"]
    
    def export_voices_config(self, output_path: str):
        """Export voices configuration to JSON file"""
        voices_data = {
            "chatterbox_voices": {
                voice_id: asdict(voice) 
                for voice_id, voice in self.voices_cache.items()
            },
            "server_config": asdict(self.config),
            "total_voices": len(self.voices_cache),
            "export_timestamp": "2025-06-20"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(voices_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(self.voices_cache)} Chatterbox voices to {output_path}")


class ChatterboxTTSProvider:
    """
    [ROCKET] CHATTERBOX TTS PROVIDER for Voice Studio Integration
    
    Enhanced TTS provider that integrates với existing Voice Studio system
    """
    
    def __init__(self, config: ChatterboxConfig = None):
        self.voices_manager = ChatterboxVoicesManager(config)
        self.name = "Chatterbox TTS"
        self.quality_rating = 9.5
        self.supports_emotions = True
        self.supports_speed_control = True
        
    def get_voices(self) -> Dict[str, Dict[str, Any]]:
        """Get voices in Voice Studio compatible format"""
        voices = {}
        for voice_id, voice in self.voices_manager.get_available_voices().items():
            voices[voice_id] = {
                "name": voice.name,
                "gender": voice.gender, 
                "language": voice.language,
                "description": voice.description,
                "quality": voice.quality_rating,
                "provider": "Chatterbox",
                "voice_id": voice_id
            }
        return voices
    
    def generate_speech(
        self,
        text: str,
        voice_id: str,
        output_path: str,
        emotion: str = "neutral",
        speed: float = 1.0,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate speech with Voice Studio compatible interface"""
        
        # Map emotions to Chatterbox parameters
        # [TARGET] Use Unified Emotion System for all emotion parameters
        from core.unified_emotion_helpers import get_emotion_parameters
        emotion_params = get_emotion_parameters(emotion)
        
        # Combine parameters
        generation_params = {
            "speed": speed,
            "temperature": emotion_params["temperature"],
            "exaggeration": emotion_params["exaggeration"],
            **kwargs
        }
        
        # Generate with Chatterbox
        return self.voices_manager.generate_audio_chatterbox(
            text=text,
            voice_id=voice_id,
            output_path=output_path,
            **generation_params
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Chatterbox TTS Server connection"""
        return self.voices_manager.test_chatterbox_connection()


# Demo function
def demo_chatterbox_integration():
    """Demo Chatterbox integration capabilities"""
    print("[MIC] CHATTERBOX TTS INTEGRATION DEMO")
    print("=" * 50)
    
    # Initialize manager
    manager = ChatterboxVoicesManager()
    
    # Test connection
    print("\n[SEARCH] Testing Chatterbox TTS Server connection...")
    connection_result = manager.test_chatterbox_connection()
    print(f"Status: {connection_result}")
    
    # Show available voices
    voices = manager.get_available_voices()
    print(f"\n[CLIPBOARD] Available Voices: {len(voices)}")
    
    # Show by gender
    female_voices = manager.get_voices_by_gender("female")
    male_voices = manager.get_voices_by_gender("male")
    
    print(f"   Female voices: {len(female_voices)}")
    for voice_id, voice in list(female_voices.items())[:3]:
        print(f"      • {voice.name} ({voice_id}): {voice.description}")
    
    print(f"   Male voices: {len(male_voices)}")
    for voice_id, voice in list(male_voices.items())[:3]:
        print(f"      • {voice.name} ({voice_id}): {voice.description}")
    
    # Voice recommendations
    print(f"\n[TARGET] Voice Recommendations:")
    for char_type in ["narrator", "hero", "villain"]:
        recommendations = manager.get_voice_recommendations(char_type)
        print(f"   {char_type.title()}: {', '.join(recommendations[:3])}")
    
    print(f"\n[OK] Chatterbox Integration Demo Complete!")


if __name__ == "__main__":
    demo_chatterbox_integration() 