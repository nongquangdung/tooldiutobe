<<<<<<< Updated upstream
"""
SIMPLE Inner Voice Effects Processor
Applies echo/reverb effects to audio files using FFmpeg
"""

import os
import subprocess
import json
from pathlib import Path
import time

class SimpleInnerVoiceProcessor:
    """Simplified Inner Voice processor using FFmpeg"""
    
    def __init__(self):
        self.config_file = "configs/emotions/unified_emotions.json"
        self.default_configs = {
            'light': {
                'delay': 400.0,
                'decay': 0.3,
                'gain': 0.5,
                'filter': 'aecho=0.5:0.3:400.0:0.3'
            },
            'deep': {
                'delay': 800.0,
                'decay': 0.6,
                'gain': 0.7,
                'filter': 'aecho=0.7:0.6:800.0:0.6,lowpass=f=3000'
            },
            'dreamy': {
                'delay': 1900.0,
                'decay': 0.8,
                'gain': 0.6,
                'filter': 'volume=0.8,aecho=0.6:0.8:1900.0:0.8,lowpass=f=3000'
            }
        }
        self.load_config()
    
    def load_config(self):
        """Load inner voice config from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Get inner voice config from unified emotions file
                inner_voice_config = data.get('inner_voice_config', {})
                if inner_voice_config and 'presets' in inner_voice_config:
                    presets = inner_voice_config['presets']
                    
                    # Update configs with loaded values
                    for voice_type in ['light', 'deep', 'dreamy']:
                        if voice_type in presets:
                            config = presets[voice_type]
                            print(f"🔍 Loading {voice_type}: filter='{config.get('filter', 'missing')}'")
                            self.default_configs[voice_type].update({
                                'delay': config.get('delay', self.default_configs[voice_type]['delay']),
                                'decay': config.get('decay', self.default_configs[voice_type]['decay']),
                                'gain': config.get('gain', self.default_configs[voice_type]['gain']),
                                'filter': config.get('filter', self.default_configs[voice_type]['filter'])
                            })
                            print(f"   ✅ Updated {voice_type}: filter='{self.default_configs[voice_type]['filter']}'")
                    print(f"✅ Loaded inner voice config from {self.config_file}")
                else:
                    print(f"⚠️ No inner voice config found, using defaults")
            else:
                print(f"⚠️ Config file not found: {self.config_file}, using defaults")
                
        except Exception as e:
            print(f"❌ Error loading config: {e}, using defaults")
    
    def apply_effects(self, input_file: str, output_file: str, voice_type: str = 'light', custom_params: dict = None) -> bool:
        """
        Apply inner voice effects to audio file
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output file
            voice_type: Type of effect ('light', 'deep', 'dreamy')
            custom_params: Custom parameters {delay, decay, gain}
            
        Returns:
            bool: Success status
        """
        try:
            if not os.path.exists(input_file):
                print(f"❌ Input file not found: {input_file}")
                return False
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir:  # Only create if directory is not empty (not root)
                os.makedirs(output_dir, exist_ok=True)
            
            # Get effect parameters
            if custom_params:
                delay = custom_params.get('delay', 400.0)
                decay = custom_params.get('decay', 0.3)
                gain = custom_params.get('gain', 0.5)
            else:
                config = self.default_configs.get(voice_type, self.default_configs['light'])
                delay = config['delay']
                decay = config['decay']
                gain = config['gain']
            
            # Build FFmpeg filter - use config filter if available
            config = self.default_configs.get(voice_type, self.default_configs['light'])
            
            if custom_params:
                # Build custom filter for custom params
                if voice_type == 'light':
                    filter_complex = f"aecho={gain}:{decay}:{delay}:0.3"
                elif voice_type == 'deep':
                    filter_complex = f"aecho={gain}:{decay}:{delay}:{decay},lowpass=f=3000"
                elif voice_type == 'dreamy':
                    filter_complex = f"volume=0.8,aecho={gain}:{decay}:{delay}:{decay},lowpass=f=3000"
                else:
                    filter_complex = f"aecho={gain}:{decay}:{delay}:0.3"
            else:
                # Use filter from config
                filter_complex = config['filter']
            
            # FFmpeg command - try local first, then system
            ffmpeg_exe = None
            
            # Try local FFmpeg first
            local_ffmpeg = os.path.join("tools", "ffmpeg", "ffmpeg.exe")
            if os.path.exists(local_ffmpeg):
                ffmpeg_exe = local_ffmpeg
            else:
                # Fall back to system FFmpeg
                ffmpeg_exe = "ffmpeg"
            
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_file,
                "-af", filter_complex,
                output_file
            ]
            
            print(f"🔄 Applying {voice_type} inner voice effects...")
            print(f"   Input: {input_file}")
            print(f"   Output: {output_file}")
            print(f"   Filter: {filter_complex}")
            
            # Execute FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                # Verify file sizes
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                
                print(f"✅ Inner voice effects applied successfully!")
                print(f"   📊 Size: {input_size//1024}KB → {output_size//1024}KB")
                return True
            else:
                print(f"❌ FFmpeg failed with error:")
                print(f"   Return code: {result.returncode}")
                print(f"   STDERR: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error applying inner voice effects: {e}")
            return False
    
    def process_audio_with_inner_voice(self, input_file: str, voice_type: str = 'light', custom_params: dict = None) -> str:
        """
        Process audio file and return processed file path
        
        Args:
            input_file: Path to input audio file
            voice_type: Type of effect ('light', 'deep', 'dreamy')
            custom_params: Custom parameters {delay, decay, gain}
            
        Returns:
            str: Path to processed file or None if failed
        """
        try:
            # Generate output filename
            input_path = Path(input_file)
            timestamp = int(time.time())
            output_file = f"voice_studio_output/{input_path.stem}_inner_voice_{voice_type}_{timestamp}.mp3"
            
            success = self.apply_effects(input_file, output_file, voice_type, custom_params)
            
            if success:
                return output_file
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error processing audio with inner voice: {e}")
            return None
    
    def get_available_types(self):
        """Get available inner voice types"""
        return list(self.default_configs.keys())
    
    def get_config(self, voice_type: str):
        """Get configuration for a voice type"""
        return self.default_configs.get(voice_type, self.default_configs['light'])

# Global instance
_processor = None

def get_inner_voice_processor():
    """Get global SimpleInnerVoiceProcessor instance"""
    global _processor
    if _processor is None:
        _processor = SimpleInnerVoiceProcessor()
    return _processor

# Convenience functions
def apply_inner_voice_effects(input_file: str, output_file: str, voice_type: str = 'light', custom_params: dict = None) -> bool:
    """Apply inner voice effects to audio file"""
    processor = get_inner_voice_processor()
    return processor.apply_effects(input_file, output_file, voice_type, custom_params)

def process_audio_with_inner_voice(input_file: str, voice_type: str = 'light', custom_params: dict = None) -> str:
    """Process audio file and return processed file path"""
    processor = get_inner_voice_processor()
=======
"""
SIMPLE Inner Voice Effects Processor
Applies echo/reverb effects to audio files using FFmpeg
"""

import os
import subprocess
import json
from pathlib import Path
import time

class SimpleInnerVoiceProcessor:
    """Simplified Inner Voice processor using FFmpeg"""
    
    def __init__(self):
        self.config_file = "configs/emotions/unified_emotions.json"
        self.default_configs = {
            'light': {
                'delay': 400.0,
                'decay': 0.3,
                'gain': 0.5,
                'filter': 'aecho=0.5:0.3:400.0:0.3'
            },
            'deep': {
                'delay': 800.0,
                'decay': 0.6,
                'gain': 0.7,
                'filter': 'aecho=0.7:0.6:800.0:0.6,lowpass=f=3000'
            },
            'dreamy': {
                'delay': 1900.0,
                'decay': 0.8,
                'gain': 0.6,
                'filter': 'volume=0.8,aecho=0.6:0.8:1900.0:0.8,lowpass=f=3000'
            }
        }
        self.load_config()
    
    def load_config(self):
        """Load inner voice config from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Get inner voice config from unified emotions file
                inner_voice_config = data.get('inner_voice_config', {})
                if inner_voice_config and 'presets' in inner_voice_config:
                    presets = inner_voice_config['presets']
                    
                    # Update configs with loaded values
                    for voice_type in ['light', 'deep', 'dreamy']:
                        if voice_type in presets:
                            config = presets[voice_type]
                            print(f"[SEARCH] Loading {voice_type}: filter='{config.get('filter', 'missing')}'")
                            self.default_configs[voice_type].update({
                                'delay': config.get('delay', self.default_configs[voice_type]['delay']),
                                'decay': config.get('decay', self.default_configs[voice_type]['decay']),
                                'gain': config.get('gain', self.default_configs[voice_type]['gain']),
                                'filter': config.get('filter', self.default_configs[voice_type]['filter'])
                            })
                            print(f"   [OK] Updated {voice_type}: filter='{self.default_configs[voice_type]['filter']}'")
                    print(f"[OK] Loaded inner voice config from {self.config_file}")
                else:
                    print(f"[WARNING] No inner voice config found, using defaults")
            else:
                print(f"[WARNING] Config file not found: {self.config_file}, using defaults")
                
        except Exception as e:
            print(f"[EMOJI] Error loading config: {e}, using defaults")
    
    def apply_effects(self, input_file: str, output_file: str, voice_type: str = 'light', custom_params: dict = None) -> bool:
        """
        Apply inner voice effects to audio file
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output file
            voice_type: Type of effect ('light', 'deep', 'dreamy')
            custom_params: Custom parameters {delay, decay, gain}
            
        Returns:
            bool: Success status
        """
        try:
            if not os.path.exists(input_file):
                print(f"[EMOJI] Input file not found: {input_file}")
                return False
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir:  # Only create if directory is not empty (not root)
                os.makedirs(output_dir, exist_ok=True)
            
            # Get effect parameters
            if custom_params:
                delay = custom_params.get('delay', 400.0)
                decay = custom_params.get('decay', 0.3)
                gain = custom_params.get('gain', 0.5)
            else:
                config = self.default_configs.get(voice_type, self.default_configs['light'])
                delay = config['delay']
                decay = config['decay']
                gain = config['gain']
            
            # Build FFmpeg filter - use config filter if available
            config = self.default_configs.get(voice_type, self.default_configs['light'])
            
            if custom_params:
                # Build custom filter for custom params
                if voice_type == 'light':
                    filter_complex = f"aecho={gain}:{decay}:{delay}:0.3"
                elif voice_type == 'deep':
                    filter_complex = f"aecho={gain}:{decay}:{delay}:{decay},lowpass=f=3000"
                elif voice_type == 'dreamy':
                    filter_complex = f"volume=0.8,aecho={gain}:{decay}:{delay}:{decay},lowpass=f=3000"
                else:
                    filter_complex = f"aecho={gain}:{decay}:{delay}:0.3"
            else:
                # Use filter from config
                filter_complex = config['filter']
            
            # FFmpeg command - try local first, then system
            ffmpeg_exe = None
            
            # Try local FFmpeg first
            local_ffmpeg = os.path.join("tools", "ffmpeg", "ffmpeg.exe")
            if os.path.exists(local_ffmpeg):
                ffmpeg_exe = local_ffmpeg
            else:
                # Fall back to system FFmpeg
                ffmpeg_exe = "ffmpeg"
            
            cmd = [
                ffmpeg_exe, "-y",
                "-i", input_file,
                "-af", filter_complex,
                output_file
            ]
            
            print(f"[REFRESH] Applying {voice_type} inner voice effects...")
            print(f"   Input: {input_file}")
            print(f"   Output: {output_file}")
            print(f"   Filter: {filter_complex}")
            
            # Execute FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                # Verify file sizes
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                
                print(f"[OK] Inner voice effects applied successfully!")
                print(f"   [STATS] Size: {input_size//1024}KB → {output_size//1024}KB")
                return True
            else:
                print(f"[EMOJI] FFmpeg failed with error:")
                print(f"   Return code: {result.returncode}")
                print(f"   STDERR: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[EMOJI] Error applying inner voice effects: {e}")
            return False
    
    def process_audio_with_inner_voice(self, input_file: str, voice_type: str = 'light', custom_params: dict = None) -> str:
        """
        Process audio file and return processed file path
        
        Args:
            input_file: Path to input audio file
            voice_type: Type of effect ('light', 'deep', 'dreamy')
            custom_params: Custom parameters {delay, decay, gain}
            
        Returns:
            str: Path to processed file or None if failed
        """
        try:
            # Generate output filename
            input_path = Path(input_file)
            timestamp = int(time.time())
            output_file = f"voice_studio_output/{input_path.stem}_inner_voice_{voice_type}_{timestamp}.mp3"
            
            success = self.apply_effects(input_file, output_file, voice_type, custom_params)
            
            if success:
                return output_file
            else:
                return None
                
        except Exception as e:
            print(f"[EMOJI] Error processing audio with inner voice: {e}")
            return None
    
    def get_available_types(self):
        """Get available inner voice types"""
        return list(self.default_configs.keys())
    
    def get_config(self, voice_type: str):
        """Get configuration for a voice type"""
        return self.default_configs.get(voice_type, self.default_configs['light'])

# Global instance
_processor = None

def get_inner_voice_processor():
    """Get global SimpleInnerVoiceProcessor instance"""
    global _processor
    if _processor is None:
        _processor = SimpleInnerVoiceProcessor()
    return _processor

# Convenience functions
def apply_inner_voice_effects(input_file: str, output_file: str, voice_type: str = 'light', custom_params: dict = None) -> bool:
    """Apply inner voice effects to audio file"""
    processor = get_inner_voice_processor()
    return processor.apply_effects(input_file, output_file, voice_type, custom_params)

def process_audio_with_inner_voice(input_file: str, voice_type: str = 'light', custom_params: dict = None) -> str:
    """Process audio file and return processed file path"""
    processor = get_inner_voice_processor()
>>>>>>> Stashed changes
    return processor.process_audio_with_inner_voice(input_file, voice_type, custom_params) 