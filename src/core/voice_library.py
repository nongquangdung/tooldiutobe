"""
Voice Library Management - Theo cách Chatterbox-Audiobook implement
Cấu trúc: voice_library/voice_name/config.json + voice.wav
"""

import os
import json
import shutil
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class VoiceLibrary:
    """
    Voice Library Management theo cách Chatterbox-Audiobook
    Cấu trúc thư mục: voice_library/voice_name/config.json + voice.wav
    """
    
    def __init__(self, voice_library_path: str = "voice_library"):
        """
        Args:
            voice_library_path: Path to voice library directory
        """
        self.voice_library_path = voice_library_path
        self.ensure_voice_library_exists()
        logger.info(f"VoiceLibrary initialized with path: {voice_library_path}")
    
    def ensure_voice_library_exists(self) -> None:
        """Ensure voice library directory exists."""
        if not os.path.exists(self.voice_library_path):
            os.makedirs(self.voice_library_path)
            logger.info(f"Created voice library directory: {self.voice_library_path}")
    
    def get_voice_profiles(self) -> List[Dict[str, Any]]:
        """
        Get all voice profiles from the library.
        
        Returns:
            List of voice profile dictionaries
        """
        profiles = []
        
        if not os.path.exists(self.voice_library_path):
            return profiles
        
        for item in os.listdir(self.voice_library_path):
            profile_dir = os.path.join(self.voice_library_path, item)
            if os.path.isdir(profile_dir):
                config_path = os.path.join(profile_dir, "config.json")
                if os.path.exists(config_path):
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            config['voice_name'] = item  # Ensure voice_name is set
                            profiles.append(config)
                    except Exception as e:
                        logger.warning(f"Error loading config for {item}: {e}")
                        # Create basic profile if config is corrupted
                        profiles.append({
                            'voice_name': item,
                            'display_name': item,
                            'description': 'Voice profile',
                            'exaggeration': 1.0,
                            'cfg_weight': 1.0,
                            'temperature': 0.7
                        })
        
        logger.debug(f"Found {len(profiles)} voice profiles")
        return profiles
    
    def get_voice_choices(self) -> List[str]:
        """
        Get list of available voice names for dropdowns.
        
        Returns:
            List of voice names
        """
        profiles = self.get_voice_profiles()
        choices = [profile['voice_name'] for profile in profiles]
        logger.debug(f"Available voice choices: {choices}")
        return choices
    
    def get_audiobook_voice_choices(self) -> List[str]:
        """
        Get voice choices formatted for audiobook interface.
        
        Returns:
            List of formatted voice choices
        """
        profiles = self.get_voice_profiles()
        choices = []
        
        for profile in profiles:
            display_name = profile.get('display_name', profile['voice_name'])
            description = profile.get('description', '')
            if description:
                choice = f"{display_name} - {description}"
            else:
                choice = display_name
            choices.append(choice)
        
        logger.debug(f"Audiobook voice choices: {choices}")
        return choices
    
    def get_voice_config(self, voice_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific voice.
        
        Args:
            voice_name: Name of the voice
            
        Returns:
            Voice configuration dictionary
        """
        config_path = os.path.join(self.voice_library_path, voice_name, "config.json")
        
        # Default configuration
        default_config = {
            'voice_name': voice_name,
            'display_name': voice_name,
            'description': '',
            'exaggeration': 1.0,
            'cfg_weight': 1.0,
            'temperature': 0.7
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(config)
                    logger.debug(f"Loaded config for {voice_name}")
                    return default_config
            except Exception as e:
                logger.warning(f"Error loading config for {voice_name}: {e}")
        
        logger.debug(f"Using default config for {voice_name}")
        return default_config
    
    def load_voice_for_tts(self, voice_name: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Load voice audio file and configuration for TTS.
        
        Args:
            voice_name: Name of the voice
            
        Returns:
            Tuple of (audio_file_path, config)
        """
        if not voice_name:
            return None, {}
        
        profile_dir = os.path.join(self.voice_library_path, voice_name)
        
        if not os.path.exists(profile_dir):
            logger.warning(f"Voice profile directory not found: {profile_dir}")
            return None, {}
        
        # Look for audio file
        audio_file = None
        for ext in ['.wav', '.mp3', '.flac']:
            potential_file = os.path.join(profile_dir, f"voice{ext}")
            if os.path.exists(potential_file):
                audio_file = potential_file
                break
        
        # Get voice configuration
        config = self.get_voice_config(voice_name)
        
        logger.debug(f"Loaded voice {voice_name}: audio={audio_file}, config={config}")
        return audio_file, config
    
    def save_voice_profile(self, voice_name: str, display_name: str, description: str,
                          audio_file: Any, exaggeration: float, cfg_weight: float,
                          temperature: float) -> str:
        """
        Save a new voice profile to the library.
        
        Args:
            voice_name: Internal voice name (used for directory)
            display_name: Display name for UI
            description: Voice description
            audio_file: Audio file data
            exaggeration: Exaggeration parameter
            cfg_weight: CFG weight parameter
            temperature: Temperature parameter
            
        Returns:
            Status message
        """
        if not voice_name.strip():
            return "[EMOJI] Voice name cannot be empty"
        
        # Sanitize voice name for directory
        safe_voice_name = "".join(c for c in voice_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_voice_name = safe_voice_name.replace(' ', '_')
        
        if not safe_voice_name:
            return "[EMOJI] Voice name contains only invalid characters"
        
        self.ensure_voice_library_exists()
        
        profile_dir = os.path.join(self.voice_library_path, safe_voice_name)
        os.makedirs(profile_dir, exist_ok=True)
        
        try:
            # Save audio file
            if audio_file is not None:
                audio_path = os.path.join(profile_dir, "voice.wav")
                if isinstance(audio_file, str):
                    # File path provided
                    shutil.copy2(audio_file, audio_path)
                elif hasattr(audio_file, 'name'):
                    # File object
                    shutil.copy2(audio_file.name, audio_path)
                else:
                    return "[EMOJI] Invalid audio file format"
            
            # Save configuration
            config = {
                'voice_name': safe_voice_name,
                'display_name': display_name or safe_voice_name,
                'description': description or '',
                'exaggeration': float(exaggeration),
                'cfg_weight': float(cfg_weight),
                'temperature': float(temperature)
            }
            
            config_path = os.path.join(profile_dir, "config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved voice profile: {safe_voice_name}")
            return f"[OK] Voice profile '{display_name}' saved successfully"
            
        except Exception as e:
            logger.error(f"Error saving voice profile {safe_voice_name}: {e}")
            return f"[EMOJI] Error saving voice profile: {str(e)}"
    
    def load_voice_profile(self, voice_name: str) -> Tuple[str, str, str, float, float, float]:
        """
        Load voice profile data for editing.
        
        Args:
            voice_name: Name of voice to load
            
        Returns:
            tuple: (display_name, description, audio_path, exaggeration, cfg_weight, temperature)
        """
        if not voice_name:
            return "", "", "", 1.0, 1.0, 0.7
        
        config = self.get_voice_config(voice_name)
        audio_file, _ = self.load_voice_for_tts(voice_name)
        
        return (
            config.get('display_name', voice_name),
            config.get('description', ''),
            audio_file or "",
            config.get('exaggeration', 1.0),
            config.get('cfg_weight', 1.0),
            config.get('temperature', 0.7)
        )
    
    def delete_voice_profile(self, voice_name: str) -> str:
        """
        Delete a voice profile from the library.
        
        Args:
            voice_name: Name of voice to delete
            
        Returns:
            Status message
        """
        if not voice_name:
            return "[EMOJI] No voice selected for deletion"
        
        profile_dir = os.path.join(self.voice_library_path, voice_name)
        
        if not os.path.exists(profile_dir):
            return f"[EMOJI] Voice profile '{voice_name}' not found"
        
        try:
            shutil.rmtree(profile_dir)
            logger.info(f"Deleted voice profile: {voice_name}")
            return f"[OK] Voice profile '{voice_name}' deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting voice profile {voice_name}: {e}")
            return f"[EMOJI] Error deleting voice profile: {str(e)}"
    
    def refresh_voice_list(self) -> List[str]:
        """
        Refresh and return the current voice list.
        
        Returns:
            Updated list of voice names
        """
        return self.get_voice_choices()
    
    def create_assignment_interface_data(self, voice_counts: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Create data for voice assignment interface.
        
        Args:
            voice_counts: Dictionary mapping character names to word counts
            
        Returns:
            List of interface data dictionaries
        """
        characters = list(voice_counts.keys())
        available_voices = self.get_voice_choices()
        
        # Return data that can be used to create dropdowns
        return [
            {
                'character': char,
                'word_count': voice_counts[char],
                'available_voices': available_voices
            }
            for char in characters[:6]  # Limit to 6 characters
        ]

# Convenience functions
def create_voice_library(voice_library_path: str = "voice_library") -> VoiceLibrary:
    """
    Create a VoiceLibrary instance.
    
    Args:
        voice_library_path: Path to voice library directory
        
    Returns:
        VoiceLibrary instance
    """
    return VoiceLibrary(voice_library_path) 