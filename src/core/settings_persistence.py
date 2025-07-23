#!/usr/bin/env python3
"""
[EMOJI] SETTINGS PERSISTENCE SYSTEM - PHASE 3 FEATURE
===============================================

Settings persistence system dựa trên original Chatterbox Extended.
Cho phép save/load/export/import settings in JSON và CSV formats.

Features:
- JSON/CSV export/import
- Auto-save settings
- Backup management
- Settings profiles
- Migration support
"""

import os
import json
import csv
import time
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

@dataclass
class VoiceStudioSettings:
    """Voice Studio settings structure"""
    # Performance Settings
    tts_mode: str = "hybrid"
    cache_enabled: bool = True
    parallel_processing: bool = True
    
    # Text Processing Settings
    text_processing_enabled: bool = True
    text_processing_mode: str = "conservative"
    smart_joining_enabled: bool = True
    recursive_splitting_enabled: bool = False
    advanced_preprocessing: bool = False
    
    # Whisper Settings
    whisper_validation_enabled: bool = True
    whisper_model: str = "base"
    whisper_backend: str = "faster_whisper"
    similarity_threshold: float = 0.8
    
    # Quality Settings
    max_retries: int = 3
    quality_threshold: float = 0.7
    candidate_count: int = 3
    
    # Voice Conversion Settings
    conversion_strength: int = 75
    pitch_preservation: int = 50
    quality_mode: str = "Standard (Balanced, 44kHz)"
    preserve_emotion: bool = True
    noise_reduction: bool = True
    normalize_volume: bool = True
    
    # UI Settings
    auto_save_enabled: bool = True
    show_advanced_controls: bool = False
    theme: str = "light"
    
    # File Paths
    default_output_path: str = "./voice_studio_output/"
    voice_clone_base_path: str = "./voices/"
    temp_path: str = "./temp/"
    
    # Character Settings
    character_chatterbox_settings: Dict[str, Any] = None
    voice_mapping: Dict[str, str] = None
    
    def __post_init__(self):
        if self.character_chatterbox_settings is None:
            self.character_chatterbox_settings = {}
        if self.voice_mapping is None:
            self.voice_mapping = {}

class SettingsPersistence:
    """Settings persistence manager"""
    
    def __init__(self, config_dir: str = "./configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.settings_file = self.config_dir / "voice_studio_settings.json"
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        
        self.current_settings = VoiceStudioSettings()
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Update current settings
                for key, value in data.items():
                    if hasattr(self.current_settings, key):
                        setattr(self.current_settings, key, value)
                
                logger.info(f"[OK] Loaded settings from {self.settings_file}")
            else:
                logger.info("[FILE] No existing settings file, using defaults")
                self._save_settings()  # Create default settings file
                
        except Exception as e:
            logger.error(f"[EMOJI] Error loading settings: {e}")
            # Use default settings
            self.current_settings = VoiceStudioSettings()
    
    def _save_settings(self):
        """Save current settings to file"""
        try:
            # Create backup before saving
            if self.settings_file.exists():
                self._create_backup()
            
            # Convert settings to dict
            settings_dict = asdict(self.current_settings)
            
            # Save to file
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"[EMOJI] Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error saving settings: {e}")
            return False
    
    def _create_backup(self):
        """Create backup of current settings"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"voice_studio_settings_backup_{timestamp}.json"
            
            shutil.copy2(self.settings_file, backup_file)
            
            # Keep only last 10 backups
            self._cleanup_old_backups()
            
            logger.info(f"[CLIPBOARD] Created backup: {backup_file}")
            
        except Exception as e:
            logger.error(f"[EMOJI] Error creating backup: {e}")
    
    def _cleanup_old_backups(self, keep_count: int = 10):
        """Cleanup old backup files"""
        try:
            backup_files = list(self.backup_dir.glob("voice_studio_settings_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old backups
            for old_backup in backup_files[keep_count:]:
                old_backup.unlink()
                logger.info(f"[DELETE] Removed old backup: {old_backup}")
                
        except Exception as e:
            logger.error(f"[EMOJI] Error cleaning up backups: {e}")
    
    def get_settings(self) -> VoiceStudioSettings:
        """Get current settings"""
        return self.current_settings
    
    def update_settings(self, **kwargs):
        """Update settings"""
        for key, value in kwargs.items():
            if hasattr(self.current_settings, key):
                setattr(self.current_settings, key, value)
            else:
                logger.warning(f"[WARNING] Unknown setting key: {key}")
        
        if self.current_settings.auto_save_enabled:
            self._save_settings()
    
    def save_settings_manually(self):
        """Manually save settings"""
        return self._save_settings()
    
    def reset_to_defaults(self):
        """Reset to default settings"""
        self.current_settings = VoiceStudioSettings()
        return self._save_settings()
    
    def export_settings_json(self, export_path: str) -> bool:
        """Export settings to JSON file"""
        try:
            settings_dict = asdict(self.current_settings)
            
            # Add metadata
            export_data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "version": "1.0",
                    "app": "Voice Studio v2"
                },
                "settings": settings_dict
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"[EMOJI] Settings exported to JSON: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error exporting to JSON: {e}")
            return False
    
    def import_settings_json(self, import_path: str) -> bool:
        """Import settings from JSON file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (direct settings) and new format (with metadata)
            if "settings" in data:
                settings_data = data["settings"]
            else:
                settings_data = data
            
            # Create backup before import
            self._create_backup()
            
            # Update settings
            for key, value in settings_data.items():
                if hasattr(self.current_settings, key):
                    setattr(self.current_settings, key, value)
            
            # Save imported settings
            self._save_settings()
            
            logger.info(f"[EMOJI] Settings imported from JSON: {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error importing from JSON: {e}")
            return False
    
    def export_settings_csv(self, export_path: str) -> bool:
        """Export settings to CSV file"""
        try:
            settings_dict = asdict(self.current_settings)
            
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(["Setting", "Value", "Type", "Description"])
                
                # Settings data
                for key, value in settings_dict.items():
                    if isinstance(value, (dict, list)):
                        value_str = json.dumps(value)
                        value_type = type(value).__name__
                    else:
                        value_str = str(value)
                        value_type = type(value).__name__
                    
                    description = self._get_setting_description(key)
                    writer.writerow([key, value_str, value_type, description])
            
            logger.info(f"[EMOJI] Settings exported to CSV: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error exporting to CSV: {e}")
            return False
    
    def import_settings_csv(self, import_path: str) -> bool:
        """Import settings from CSV file"""
        try:
            # Create backup before import
            self._create_backup()
            
            with open(import_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    key = row["Setting"]
                    value_str = row["Value"]
                    value_type = row["Type"]
                    
                    if not hasattr(self.current_settings, key):
                        continue
                    
                    # Convert value based on type
                    try:
                        if value_type == "bool":
                            value = value_str.lower() in ("true", "1", "yes")
                        elif value_type == "int":
                            value = int(value_str)
                        elif value_type == "float":
                            value = float(value_str)
                        elif value_type in ("dict", "list"):
                            value = json.loads(value_str)
                        else:
                            value = value_str
                        
                        setattr(self.current_settings, key, value)
                        
                    except (ValueError, json.JSONDecodeError) as e:
                        logger.warning(f"[WARNING] Skipping invalid value for {key}: {e}")
            
            # Save imported settings
            self._save_settings()
            
            logger.info(f"[EMOJI] Settings imported from CSV: {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error importing from CSV: {e}")
            return False
    
    def _get_setting_description(self, setting_key: str) -> str:
        """Get description for setting"""
        descriptions = {
            "tts_mode": "TTS processing mode (maximum_performance/hybrid/maximum_compatibility)",
            "cache_enabled": "Enable model caching for faster processing",
            "parallel_processing": "Enable parallel processing for multiple files",
            "text_processing_enabled": "Enable advanced text processing",
            "text_processing_mode": "Text processing aggressiveness (conservative/standard/aggressive)",
            "smart_joining_enabled": "Enable smart sentence joining",
            "recursive_splitting_enabled": "Enable recursive sentence splitting",
            "whisper_validation_enabled": "Enable Whisper STT validation",
            "whisper_model": "Whisper model size",
            "conversion_strength": "Voice conversion strength (1-100%)",
            "pitch_preservation": "Pitch preservation level (0-100%)",
            "quality_mode": "Audio quality mode",
            "default_output_path": "Default output directory path",
            "auto_save_enabled": "Enable automatic settings saving"
        }
        
        return descriptions.get(setting_key, "No description available")
    
    def save_profile(self, profile_name: str) -> bool:
        """Save current settings as a profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            profile_data = {
                "name": profile_name,
                "created_at": datetime.now().isoformat(),
                "settings": asdict(self.current_settings)
            }
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"[EMOJI] Profile saved: {profile_name}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error saving profile: {e}")
            return False
    
    def load_profile(self, profile_name: str) -> bool:
        """Load settings from a profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_file.exists():
                logger.error(f"[EMOJI] Profile not found: {profile_name}")
                return False
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Create backup before loading profile
            self._create_backup()
            
            # Load profile settings
            settings_data = profile_data["settings"]
            for key, value in settings_data.items():
                if hasattr(self.current_settings, key):
                    setattr(self.current_settings, key, value)
            
            # Save loaded profile settings
            self._save_settings()
            
            logger.info(f"[EMOJI] Profile loaded: {profile_name}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error loading profile: {e}")
            return False
    
    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all available profiles"""
        profiles = []
        
        try:
            for profile_file in self.profiles_dir.glob("*.json"):
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                profiles.append({
                    "name": profile_data.get("name", profile_file.stem),
                    "created_at": profile_data.get("created_at", "Unknown"),
                    "file_path": str(profile_file)
                })
                
        except Exception as e:
            logger.error(f"[EMOJI] Error listing profiles: {e}")
        
        return sorted(profiles, key=lambda x: x["created_at"], reverse=True)
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if profile_file.exists():
                profile_file.unlink()
                logger.info(f"[DELETE] Profile deleted: {profile_name}")
                return True
            else:
                logger.error(f"[EMOJI] Profile not found: {profile_name}")
                return False
                
        except Exception as e:
            logger.error(f"[EMOJI] Error deleting profile: {e}")
            return False
    
    def get_backup_files(self) -> List[Dict[str, Any]]:
        """Get list of backup files"""
        backups = []
        
        try:
            for backup_file in self.backup_dir.glob("voice_studio_settings_backup_*.json"):
                stat = backup_file.stat()
                
                backups.append({
                    "filename": backup_file.name,
                    "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size_bytes": stat.st_size,
                    "file_path": str(backup_file)
                })
                
        except Exception as e:
            logger.error(f"[EMOJI] Error listing backups: {e}")
        
        return sorted(backups, key=lambda x: x["created_at"], reverse=True)
    
    def restore_from_backup(self, backup_filename: str) -> bool:
        """Restore settings from backup"""
        try:
            backup_file = self.backup_dir / backup_filename
            
            if not backup_file.exists():
                logger.error(f"[EMOJI] Backup file not found: {backup_filename}")
                return False
            
            # Create backup of current settings before restore
            self._create_backup()
            
            # Copy backup to main settings file
            shutil.copy2(backup_file, self.settings_file)
            
            # Reload settings
            self._load_settings()
            
            logger.info(f"[REFRESH] Settings restored from backup: {backup_filename}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Error restoring from backup: {e}")
            return False

# Global settings persistence instance
settings_manager = SettingsPersistence()

def get_settings() -> VoiceStudioSettings:
    """Get current settings"""
    return settings_manager.get_settings()

def update_settings(**kwargs):
    """Update settings"""
    settings_manager.update_settings(**kwargs)

def save_settings():
    """Save settings manually"""
    return settings_manager.save_settings_manually()

def export_settings(export_path: str, format_type: str = "json") -> bool:
    """Export settings to file"""
    if format_type.lower() == "json":
        return settings_manager.export_settings_json(export_path)
    elif format_type.lower() == "csv":
        return settings_manager.export_settings_csv(export_path)
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def import_settings(import_path: str, format_type: str = "json") -> bool:
    """Import settings from file"""
    if format_type.lower() == "json":
        return settings_manager.import_settings_json(import_path)
    elif format_type.lower() == "csv":
        return settings_manager.import_settings_csv(import_path)
    else:
        raise ValueError(f"Unsupported format: {format_type}")

if __name__ == "__main__":
    # Test settings persistence
    print("[TEST] Testing Settings Persistence...")
    
    # Test basic functionality
    settings = get_settings()
    print(f"Default TTS mode: {settings.tts_mode}")
    
    # Update settings
    update_settings(tts_mode="maximum_performance", cache_enabled=False)
    print(f"Updated TTS mode: {get_settings().tts_mode}")
    
    # Test export/import
    export_settings("./test_settings.json", "json")
    export_settings("./test_settings.csv", "csv")
    
    print("[OK] Settings persistence test completed!") 