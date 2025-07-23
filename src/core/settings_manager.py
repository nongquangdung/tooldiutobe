<<<<<<< Updated upstream
"""
Voice Studio Settings Manager - Professional Workflow System
Quản lý templates, presets, và generation history cho Voice Studio
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    name: str
    voice_id: str
    gender: str
    language: str
    default_emotion: str = "friendly"
    default_speed: float = 1.0
    default_pitch: float = 1.0
    description: str = ""


@dataclass
class AudioProcessingSettings:
    """Audio post-processing configuration"""
    normalize_volume: bool = True
    target_lufs: float = -23.0  # EBU R128 broadcast standard
    remove_silence: bool = True
    silence_threshold: float = 0.1
    apply_compression: bool = False
    compression_ratio: float = 2.0
    export_formats: List[str] = None  # ['mp3', 'wav', 'flac']
    
    def __post_init__(self):
        if self.export_formats is None:
            self.export_formats = ['mp3']


@dataclass
class ProjectTemplate:
    """Complete project template configuration"""
    name: str
    description: str
    category: str  # 'youtube', 'podcast', 'audiobook', 'gaming'
    voice_profiles: Dict[str, VoiceProfile]
    audio_settings: AudioProcessingSettings
    default_output_dir: str = "./voice_studio_output"
    created_date: str = ""
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()


@dataclass
class GenerationRecord:
    """Record of voice generation session"""
    timestamp: str
    project_name: str
    template_used: str
    segments_generated: int
    success_rate: float
    total_duration: float  # seconds
    output_files: List[str]
    settings_snapshot: Dict[str, Any]
    quality_score: Optional[float] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class SettingsManager:
    """Professional settings management system"""
    
    def __init__(self, config_dir: str = "./configs"):
        self.config_dir = config_dir
        self.templates_file = os.path.join(config_dir, "project_templates.json")
        self.history_file = os.path.join(config_dir, "generation_history.json")
        self.user_settings_file = os.path.join(config_dir, "user_settings.json")
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        # Load existing data
        self.templates = self._load_templates()
        self.history = self._load_history()
        self.user_settings = self._load_user_settings()
        
        # Initialize with built-in templates if none exist
        if not self.templates:
            self._create_builtin_templates()
    
    def _load_templates(self) -> Dict[str, ProjectTemplate]:
        """Load project templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    templates = {}
                    for name, template_data in data.items():
                        # Convert voice profiles
                        voice_profiles = {}
                        for vp_name, vp_data in template_data['voice_profiles'].items():
                            voice_profiles[vp_name] = VoiceProfile(**vp_data)
                        
                        # Convert audio settings
                        audio_settings = AudioProcessingSettings(**template_data['audio_settings'])
                        
                        # Create template
                        template = ProjectTemplate(
                            name=template_data['name'],
                            description=template_data['description'],
                            category=template_data['category'],
                            voice_profiles=voice_profiles,
                            audio_settings=audio_settings,
                            default_output_dir=template_data.get('default_output_dir', "./voice_studio_output"),
                            created_date=template_data.get('created_date', datetime.now().isoformat())
                        )
                        templates[name] = template
                    return templates
        except Exception as e:
            print(f"⚠️ Error loading templates: {e}")
        return {}
    
    def _load_history(self) -> List[GenerationRecord]:
        """Load generation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [GenerationRecord(**record) for record in data]
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
        return []
    
    def _load_user_settings(self) -> Dict[str, Any]:
        """Load user preferences"""
        try:
            if os.path.exists(self.user_settings_file):
                with open(self.user_settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading user settings: {e}")
        return {
            'default_template': 'YouTube_Standard',
            'auto_save_history': True,
            'backup_settings': True,
            'theme': 'light',
            'language': 'vi'
        }
    
    def _create_builtin_templates(self):
        """Create built-in professional templates"""
        
        # YouTube Standard Template
        youtube_template = ProjectTemplate(
            name="YouTube_Standard",
            description="Optimized cho YouTube videos - natural và engaging",
            category="youtube",
            voice_profiles={
                "narrator": VoiceProfile(
                    name="YouTube Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="friendly",
                    default_speed=1.1,
                    description="Energetic narrator cho YouTube content"
                ),
                "character1": VoiceProfile(
                    name="Main Character",
                    voice_id="character1", 
                    gender="male",
                    language="vietnamese",
                    default_emotion="confident",
                    default_speed=1.0,
                    description="Confident male voice cho main character"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-16.0,  # YouTube recommended
                remove_silence=True,
                silence_threshold=0.15,
                apply_compression=True,
                compression_ratio=2.5,
                export_formats=['mp3', 'wav']
            )
        )
        
        # Podcast Professional Template  
        podcast_template = ProjectTemplate(
            name="Podcast_Professional",
            description="Professional podcast quality - clear và consistent",
            category="podcast",
            voice_profiles={
                "host": VoiceProfile(
                    name="Podcast Host",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese", 
                    default_emotion="professional",
                    default_speed=0.95,
                    description="Clear và authoritative host voice"
                ),
                "guest": VoiceProfile(
                    name="Podcast Guest",
                    voice_id="character1",
                    gender="female", 
                    language="vietnamese",
                    default_emotion="friendly",
                    default_speed=1.0,
                    description="Warm guest voice"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-23.0,  # Broadcast standard
                remove_silence=True,
                silence_threshold=0.1,
                apply_compression=True,
                compression_ratio=3.0,
                export_formats=['mp3', 'wav', 'flac']
            )
        )
        
        # Audiobook Premium Template
        audiobook_template = ProjectTemplate(
            name="Audiobook_Premium", 
            description="Premium audiobook quality - immersive storytelling",
            category="audiobook",
            voice_profiles={
                "narrator": VoiceProfile(
                    name="Audiobook Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="storytelling",
                    default_speed=0.9,
                    description="Rich storytelling voice"
                ),
                "character_male": VoiceProfile(
                    name="Male Character",
                    voice_id="character1",
                    gender="male",
                    language="vietnamese", 
                    default_emotion="dramatic",
                    default_speed=0.95,
                    description="Expressive male character"
                ),
                "character_female": VoiceProfile(
                    name="Female Character", 
                    voice_id="character2",
                    gender="female",
                    language="vietnamese",
                    default_emotion="emotional",
                    default_speed=1.0,
                    description="Emotional female character"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-20.0,  # Audiobook standard
                remove_silence=False,  # Keep dramatic pauses
                silence_threshold=0.05,
                apply_compression=False,  # Natural dynamics
                export_formats=['mp3', 'flac']
            )
        )
        
        # Gaming Character Template
        gaming_template = ProjectTemplate(
            name="Gaming_Character",
            description="Dynamic gaming characters - expressive và dramatic", 
            category="gaming",
            voice_profiles={
                "hero": VoiceProfile(
                    name="Hero Voice",
                    voice_id="character1",
                    gender="male",
                    language="vietnamese",
                    default_emotion="heroic",
                    default_speed=1.1,
                    description="Strong heroic voice"
                ),
                "villain": VoiceProfile(
                    name="Villain Voice",
                    voice_id="character2", 
                    gender="male",
                    language="vietnamese",
                    default_emotion="sinister",
                    default_speed=0.9,
                    description="Dark villainous voice"
                ),
                "narrator": VoiceProfile(
                    name="Game Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="epic",
                    default_speed=1.0,
                    description="Epic gaming narrator"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-18.0,  # Gaming standard
                remove_silence=True,
                silence_threshold=0.2,
                apply_compression=True,
                compression_ratio=2.0,
                export_formats=['mp3', 'wav']
            )
        )
        
        # Add to templates
        self.templates = {
            "YouTube_Standard": youtube_template,
            "Podcast_Professional": podcast_template, 
            "Audiobook_Premium": audiobook_template,
            "Gaming_Character": gaming_template
        }
        
        # Save templates
        self.save_templates()
    
    def save_templates(self):
        """Save templates to file"""
        try:
            # Convert to JSON-serializable format
            templates_data = {}
            for name, template in self.templates.items():
                # Convert voice profiles to dict
                voice_profiles_data = {}
                for vp_name, vp in template.voice_profiles.items():
                    voice_profiles_data[vp_name] = asdict(vp)
                
                templates_data[name] = {
                    'name': template.name,
                    'description': template.description,
                    'category': template.category,
                    'voice_profiles': voice_profiles_data,
                    'audio_settings': asdict(template.audio_settings),
                    'default_output_dir': template.default_output_dir,
                    'created_date': template.created_date
                }
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Templates saved to {self.templates_file}")
        except Exception as e:
            print(f"❌ Error saving templates: {e}")
    
    def save_history(self):
        """Save generation history to file"""
        try:
            history_data = [asdict(record) for record in self.history]
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving history: {e}")
    
    def save_user_settings(self):
        """Save user settings to file"""
        try:
            with open(self.user_settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving user settings: {e}")
    
    def get_template(self, name: str) -> Optional[ProjectTemplate]:
        """Get template by name"""
        return self.templates.get(name)
    
    def get_templates_by_category(self, category: str) -> List[ProjectTemplate]:
        """Get all templates in a category"""
        return [t for t in self.templates.values() if t.category == category]
    
    def add_template(self, template: ProjectTemplate) -> bool:
        """Add new template"""
        try:
            self.templates[template.name] = template
            self.save_templates()
            return True
        except Exception as e:
            print(f"❌ Error adding template: {e}")
            return False
    
    def delete_template(self, name: str) -> bool:
        """Delete template"""
        try:
            if name in self.templates:
                del self.templates[name]
                self.save_templates()
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting template: {e}")
            return False
    
    def record_generation(self, record: GenerationRecord):
        """Record a voice generation session"""
        self.history.append(record)
        
        # Keep only last 100 records
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        if self.user_settings.get('auto_save_history', True):
            self.save_history()
    
    def get_recent_history(self, limit: int = 10) -> List[GenerationRecord]:
        """Get recent generation history"""
        return sorted(self.history, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        if not self.history:
            return {
                'total_generations': 0,
                'avg_success_rate': 0.0,
                'most_used_template': 'None',
                'total_audio_time': 0.0
            }
        
        total_generations = len(self.history)
        avg_success_rate = sum(r.success_rate for r in self.history) / total_generations
        total_audio_time = sum(r.total_duration for r in self.history)
        
        # Most used template
        template_usage = {}
        for record in self.history:
            template_usage[record.template_used] = template_usage.get(record.template_used, 0) + 1
        most_used_template = max(template_usage.items(), key=lambda x: x[1])[0] if template_usage else 'None'
        
        return {
            'total_generations': total_generations,
            'avg_success_rate': avg_success_rate,
            'most_used_template': most_used_template, 
            'total_audio_time': total_audio_time,
            'template_usage': template_usage
        }
    
    def export_settings(self, filepath: str) -> bool:
        """Export all settings to file"""
        try:
            export_data = {
                'templates': {},
                'user_settings': self.user_settings,
                'export_date': datetime.now().isoformat()
            }
            
            # Export templates
            for name, template in self.templates.items():
                voice_profiles_data = {}
                for vp_name, vp in template.voice_profiles.items():
                    voice_profiles_data[vp_name] = asdict(vp)
                
                export_data['templates'][name] = {
                    'name': template.name,
                    'description': template.description,
                    'category': template.category,
                    'voice_profiles': voice_profiles_data,
                    'audio_settings': asdict(template.audio_settings),
                    'default_output_dir': template.default_output_dir,
                    'created_date': template.created_date
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Settings exported to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exporting settings: {e}")
            return False
    
    def import_settings(self, filepath: str) -> bool:
        """Import settings from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Import templates
            if 'templates' in import_data:
                for name, template_data in import_data['templates'].items():
                    # Convert voice profiles
                    voice_profiles = {}
                    for vp_name, vp_data in template_data['voice_profiles'].items():
                        voice_profiles[vp_name] = VoiceProfile(**vp_data)
                    
                    # Convert audio settings
                    audio_settings = AudioProcessingSettings(**template_data['audio_settings'])
                    
                    # Create template
                    template = ProjectTemplate(
                        name=template_data['name'],
                        description=template_data['description'],
                        category=template_data['category'],
                        voice_profiles=voice_profiles,
                        audio_settings=audio_settings,
                        default_output_dir=template_data.get('default_output_dir', "./voice_studio_output"),
                        created_date=template_data.get('created_date', datetime.now().isoformat())
                    )
                    self.templates[name] = template
            
            # Import user settings
            if 'user_settings' in import_data:
                self.user_settings.update(import_data['user_settings'])
            
            # Save imported data
            self.save_templates()
            self.save_user_settings()
            
            print(f"✅ Settings imported from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error importing settings: {e}")
            return False


# Usage example
if __name__ == "__main__":
    # Initialize settings manager
    settings = SettingsManager()
    
    # Get YouTube template
    youtube_template = settings.get_template("YouTube_Standard")
    if youtube_template:
        print(f"📋 Template: {youtube_template.name}")
        print(f"📝 Description: {youtube_template.description}")
        print(f"🎵 Voice Profiles: {list(youtube_template.voice_profiles.keys())}")
        print(f"🔊 Target LUFS: {youtube_template.audio_settings.target_lufs}")
    
    # Record a generation session
    record = GenerationRecord(
        timestamp=datetime.now().isoformat(),
        project_name="Test Project",
        template_used="YouTube_Standard",
        segments_generated=5,
        success_rate=0.95,
        total_duration=120.5,
        output_files=["segment_1.mp3", "segment_2.mp3"],
        settings_snapshot={"template": "YouTube_Standard"},
        quality_score=0.92
    )
    settings.record_generation(record)
    
    # Get statistics
    stats = settings.get_statistics()
    print(f"📊 Statistics: {stats}") 
=======
"""
Voice Studio Settings Manager - Professional Workflow System
Quản lý templates, presets, và generation history cho Voice Studio
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    name: str
    voice_id: str
    gender: str
    language: str
    default_emotion: str = "friendly"
    default_speed: float = 1.0
    default_pitch: float = 1.0
    description: str = ""


@dataclass
class AudioProcessingSettings:
    """Audio post-processing configuration"""
    normalize_volume: bool = True
    target_lufs: float = -23.0  # EBU R128 broadcast standard
    remove_silence: bool = True
    silence_threshold: float = 0.1
    apply_compression: bool = False
    compression_ratio: float = 2.0
    export_formats: List[str] = None  # ['mp3', 'wav', 'flac']
    
    def __post_init__(self):
        if self.export_formats is None:
            self.export_formats = ['mp3']


@dataclass
class ProjectTemplate:
    """Complete project template configuration"""
    name: str
    description: str
    category: str  # 'youtube', 'podcast', 'audiobook', 'gaming'
    voice_profiles: Dict[str, VoiceProfile]
    audio_settings: AudioProcessingSettings
    default_output_dir: str = "./voice_studio_output"
    created_date: str = ""
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()


@dataclass
class GenerationRecord:
    """Record of voice generation session"""
    timestamp: str
    project_name: str
    template_used: str
    segments_generated: int
    success_rate: float
    total_duration: float  # seconds
    output_files: List[str]
    settings_snapshot: Dict[str, Any]
    quality_score: Optional[float] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class SettingsManager:
    """Professional settings management system"""
    
    def __init__(self, config_dir: str = "./configs"):
        self.config_dir = config_dir
        self.templates_file = os.path.join(config_dir, "project_templates.json")
        self.history_file = os.path.join(config_dir, "generation_history.json")
        self.user_settings_file = os.path.join(config_dir, "user_settings.json")
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        # Load existing data
        self.templates = self._load_templates()
        self.history = self._load_history()
        self.user_settings = self._load_user_settings()
        
        # Initialize with built-in templates if none exist
        if not self.templates:
            self._create_builtin_templates()
    
    def _load_templates(self) -> Dict[str, ProjectTemplate]:
        """Load project templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    templates = {}
                    for name, template_data in data.items():
                        # Convert voice profiles
                        voice_profiles = {}
                        for vp_name, vp_data in template_data['voice_profiles'].items():
                            voice_profiles[vp_name] = VoiceProfile(**vp_data)
                        
                        # Convert audio settings
                        audio_settings = AudioProcessingSettings(**template_data['audio_settings'])
                        
                        # Create template
                        template = ProjectTemplate(
                            name=template_data['name'],
                            description=template_data['description'],
                            category=template_data['category'],
                            voice_profiles=voice_profiles,
                            audio_settings=audio_settings,
                            default_output_dir=template_data.get('default_output_dir', "./voice_studio_output"),
                            created_date=template_data.get('created_date', datetime.now().isoformat())
                        )
                        templates[name] = template
                    return templates
        except Exception as e:
            print(f"[WARNING] Error loading templates: {e}")
        return {}
    
    def _load_history(self) -> List[GenerationRecord]:
        """Load generation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [GenerationRecord(**record) for record in data]
        except Exception as e:
            print(f"[WARNING] Error loading history: {e}")
        return []
    
    def _load_user_settings(self) -> Dict[str, Any]:
        """Load user preferences"""
        try:
            if os.path.exists(self.user_settings_file):
                with open(self.user_settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[WARNING] Error loading user settings: {e}")
        return {
            'default_template': 'YouTube_Standard',
            'auto_save_history': True,
            'backup_settings': True,
            'theme': 'light',
            'language': 'vi'
        }
    
    def _create_builtin_templates(self):
        """Create built-in professional templates"""
        
        # YouTube Standard Template
        youtube_template = ProjectTemplate(
            name="YouTube_Standard",
            description="Optimized cho YouTube videos - natural và engaging",
            category="youtube",
            voice_profiles={
                "narrator": VoiceProfile(
                    name="YouTube Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="friendly",
                    default_speed=1.1,
                    description="Energetic narrator cho YouTube content"
                ),
                "character1": VoiceProfile(
                    name="Main Character",
                    voice_id="character1", 
                    gender="male",
                    language="vietnamese",
                    default_emotion="confident",
                    default_speed=1.0,
                    description="Confident male voice cho main character"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-16.0,  # YouTube recommended
                remove_silence=True,
                silence_threshold=0.15,
                apply_compression=True,
                compression_ratio=2.5,
                export_formats=['mp3', 'wav']
            )
        )
        
        # Podcast Professional Template  
        podcast_template = ProjectTemplate(
            name="Podcast_Professional",
            description="Professional podcast quality - clear và consistent",
            category="podcast",
            voice_profiles={
                "host": VoiceProfile(
                    name="Podcast Host",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese", 
                    default_emotion="professional",
                    default_speed=0.95,
                    description="Clear và authoritative host voice"
                ),
                "guest": VoiceProfile(
                    name="Podcast Guest",
                    voice_id="character1",
                    gender="female", 
                    language="vietnamese",
                    default_emotion="friendly",
                    default_speed=1.0,
                    description="Warm guest voice"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-23.0,  # Broadcast standard
                remove_silence=True,
                silence_threshold=0.1,
                apply_compression=True,
                compression_ratio=3.0,
                export_formats=['mp3', 'wav', 'flac']
            )
        )
        
        # Audiobook Premium Template
        audiobook_template = ProjectTemplate(
            name="Audiobook_Premium", 
            description="Premium audiobook quality - immersive storytelling",
            category="audiobook",
            voice_profiles={
                "narrator": VoiceProfile(
                    name="Audiobook Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="storytelling",
                    default_speed=0.9,
                    description="Rich storytelling voice"
                ),
                "character_male": VoiceProfile(
                    name="Male Character",
                    voice_id="character1",
                    gender="male",
                    language="vietnamese", 
                    default_emotion="dramatic",
                    default_speed=0.95,
                    description="Expressive male character"
                ),
                "character_female": VoiceProfile(
                    name="Female Character", 
                    voice_id="character2",
                    gender="female",
                    language="vietnamese",
                    default_emotion="emotional",
                    default_speed=1.0,
                    description="Emotional female character"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-20.0,  # Audiobook standard
                remove_silence=False,  # Keep dramatic pauses
                silence_threshold=0.05,
                apply_compression=False,  # Natural dynamics
                export_formats=['mp3', 'flac']
            )
        )
        
        # Gaming Character Template
        gaming_template = ProjectTemplate(
            name="Gaming_Character",
            description="Dynamic gaming characters - expressive và dramatic", 
            category="gaming",
            voice_profiles={
                "hero": VoiceProfile(
                    name="Hero Voice",
                    voice_id="character1",
                    gender="male",
                    language="vietnamese",
                    default_emotion="heroic",
                    default_speed=1.1,
                    description="Strong heroic voice"
                ),
                "villain": VoiceProfile(
                    name="Villain Voice",
                    voice_id="character2", 
                    gender="male",
                    language="vietnamese",
                    default_emotion="sinister",
                    default_speed=0.9,
                    description="Dark villainous voice"
                ),
                "narrator": VoiceProfile(
                    name="Game Narrator",
                    voice_id="narrator",
                    gender="neutral",
                    language="vietnamese",
                    default_emotion="epic",
                    default_speed=1.0,
                    description="Epic gaming narrator"
                )
            },
            audio_settings=AudioProcessingSettings(
                normalize_volume=True,
                target_lufs=-18.0,  # Gaming standard
                remove_silence=True,
                silence_threshold=0.2,
                apply_compression=True,
                compression_ratio=2.0,
                export_formats=['mp3', 'wav']
            )
        )
        
        # Add to templates
        self.templates = {
            "YouTube_Standard": youtube_template,
            "Podcast_Professional": podcast_template, 
            "Audiobook_Premium": audiobook_template,
            "Gaming_Character": gaming_template
        }
        
        # Save templates
        self.save_templates()
    
    def save_templates(self):
        """Save templates to file"""
        try:
            # Convert to JSON-serializable format
            templates_data = {}
            for name, template in self.templates.items():
                # Convert voice profiles to dict
                voice_profiles_data = {}
                for vp_name, vp in template.voice_profiles.items():
                    voice_profiles_data[vp_name] = asdict(vp)
                
                templates_data[name] = {
                    'name': template.name,
                    'description': template.description,
                    'category': template.category,
                    'voice_profiles': voice_profiles_data,
                    'audio_settings': asdict(template.audio_settings),
                    'default_output_dir': template.default_output_dir,
                    'created_date': template.created_date
                }
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates_data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Templates saved to {self.templates_file}")
        except Exception as e:
            print(f"[EMOJI] Error saving templates: {e}")
    
    def save_history(self):
        """Save generation history to file"""
        try:
            history_data = [asdict(record) for record in self.history]
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[EMOJI] Error saving history: {e}")
    
    def save_user_settings(self):
        """Save user settings to file"""
        try:
            with open(self.user_settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[EMOJI] Error saving user settings: {e}")
    
    def get_template(self, name: str) -> Optional[ProjectTemplate]:
        """Get template by name"""
        return self.templates.get(name)
    
    def get_templates_by_category(self, category: str) -> List[ProjectTemplate]:
        """Get all templates in a category"""
        return [t for t in self.templates.values() if t.category == category]
    
    def add_template(self, template: ProjectTemplate) -> bool:
        """Add new template"""
        try:
            self.templates[template.name] = template
            self.save_templates()
            return True
        except Exception as e:
            print(f"[EMOJI] Error adding template: {e}")
            return False
    
    def delete_template(self, name: str) -> bool:
        """Delete template"""
        try:
            if name in self.templates:
                del self.templates[name]
                self.save_templates()
                return True
            return False
        except Exception as e:
            print(f"[EMOJI] Error deleting template: {e}")
            return False
    
    def record_generation(self, record: GenerationRecord):
        """Record a voice generation session"""
        self.history.append(record)
        
        # Keep only last 100 records
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        if self.user_settings.get('auto_save_history', True):
            self.save_history()
    
    def get_recent_history(self, limit: int = 10) -> List[GenerationRecord]:
        """Get recent generation history"""
        return sorted(self.history, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        if not self.history:
            return {
                'total_generations': 0,
                'avg_success_rate': 0.0,
                'most_used_template': 'None',
                'total_audio_time': 0.0
            }
        
        total_generations = len(self.history)
        avg_success_rate = sum(r.success_rate for r in self.history) / total_generations
        total_audio_time = sum(r.total_duration for r in self.history)
        
        # Most used template
        template_usage = {}
        for record in self.history:
            template_usage[record.template_used] = template_usage.get(record.template_used, 0) + 1
        most_used_template = max(template_usage.items(), key=lambda x: x[1])[0] if template_usage else 'None'
        
        return {
            'total_generations': total_generations,
            'avg_success_rate': avg_success_rate,
            'most_used_template': most_used_template, 
            'total_audio_time': total_audio_time,
            'template_usage': template_usage
        }
    
    def export_settings(self, filepath: str) -> bool:
        """Export all settings to file"""
        try:
            export_data = {
                'templates': {},
                'user_settings': self.user_settings,
                'export_date': datetime.now().isoformat()
            }
            
            # Export templates
            for name, template in self.templates.items():
                voice_profiles_data = {}
                for vp_name, vp in template.voice_profiles.items():
                    voice_profiles_data[vp_name] = asdict(vp)
                
                export_data['templates'][name] = {
                    'name': template.name,
                    'description': template.description,
                    'category': template.category,
                    'voice_profiles': voice_profiles_data,
                    'audio_settings': asdict(template.audio_settings),
                    'default_output_dir': template.default_output_dir,
                    'created_date': template.created_date
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Settings exported to {filepath}")
            return True
        except Exception as e:
            print(f"[EMOJI] Error exporting settings: {e}")
            return False
    
    def import_settings(self, filepath: str) -> bool:
        """Import settings from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Import templates
            if 'templates' in import_data:
                for name, template_data in import_data['templates'].items():
                    # Convert voice profiles
                    voice_profiles = {}
                    for vp_name, vp_data in template_data['voice_profiles'].items():
                        voice_profiles[vp_name] = VoiceProfile(**vp_data)
                    
                    # Convert audio settings
                    audio_settings = AudioProcessingSettings(**template_data['audio_settings'])
                    
                    # Create template
                    template = ProjectTemplate(
                        name=template_data['name'],
                        description=template_data['description'],
                        category=template_data['category'],
                        voice_profiles=voice_profiles,
                        audio_settings=audio_settings,
                        default_output_dir=template_data.get('default_output_dir', "./voice_studio_output"),
                        created_date=template_data.get('created_date', datetime.now().isoformat())
                    )
                    self.templates[name] = template
            
            # Import user settings
            if 'user_settings' in import_data:
                self.user_settings.update(import_data['user_settings'])
            
            # Save imported data
            self.save_templates()
            self.save_user_settings()
            
            print(f"[OK] Settings imported from {filepath}")
            return True
        except Exception as e:
            print(f"[EMOJI] Error importing settings: {e}")
            return False


# Usage example
if __name__ == "__main__":
    # Initialize settings manager
    settings = SettingsManager()
    
    # Get YouTube template
    youtube_template = settings.get_template("YouTube_Standard")
    if youtube_template:
        print(f"[CLIPBOARD] Template: {youtube_template.name}")
        print(f"[EDIT] Description: {youtube_template.description}")
        print(f"[MUSIC] Voice Profiles: {list(youtube_template.voice_profiles.keys())}")
        print(f"[SOUND] Target LUFS: {youtube_template.audio_settings.target_lufs}")
    
    # Record a generation session
    record = GenerationRecord(
        timestamp=datetime.now().isoformat(),
        project_name="Test Project",
        template_used="YouTube_Standard",
        segments_generated=5,
        success_rate=0.95,
        total_duration=120.5,
        output_files=["segment_1.mp3", "segment_2.mp3"],
        settings_snapshot={"template": "YouTube_Standard"},
        quality_score=0.92
    )
    settings.record_generation(record)
    
    # Get statistics
    stats = settings.get_statistics()
    print(f"[STATS] Statistics: {stats}") 
>>>>>>> Stashed changes
