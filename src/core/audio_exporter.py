<<<<<<< Updated upstream
"""
Voice Studio Audio Exporter - Multi-Format Professional Export System
Support cho WAV, MP3, FLAC với quality optimization
"""

import os
import subprocess
import shutil
from typing import List, Dict, Optional, Tuple
from enum import Enum
from pathlib import Path
import json
from datetime import datetime


class AudioFormat(Enum):
    """Supported audio formats"""
    MP3 = "mp3"
    WAV = "wav" 
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"


class AudioQuality(Enum):
    """Audio quality presets"""
    DRAFT = "draft"         # Fast export, lower quality
    STANDARD = "standard"   # Balanced quality/size
    HIGH = "high"           # High quality
    LOSSLESS = "lossless"   # Maximum quality


class ExportSettings:
    """Audio export configuration"""
    
    def __init__(self):
        # Format-specific settings
        self.mp3_bitrate = 320      # kbps
        self.mp3_vbr = False        # Use CBR by default
        
        self.wav_sample_rate = 48000  # Hz
        self.wav_bit_depth = 24       # bits
        
        self.flac_compression = 5     # 0-8, higher = smaller file
        
        # Universal settings
        self.normalize_volume = True
        self.target_lufs = -23.0     # EBU R128 broadcast standard
        self.remove_silence = False  # Preserve artistic intent
        self.fade_in_ms = 0         # Fade in duration
        self.fade_out_ms = 0        # Fade out duration
        
    def get_quality_preset(self, quality: AudioQuality) -> Dict:
        """Get preset settings for quality level"""
        presets = {
            AudioQuality.DRAFT: {
                'mp3_bitrate': 128,
                'wav_sample_rate': 44100,
                'wav_bit_depth': 16,
                'flac_compression': 8,
                'normalize_volume': False
            },
            AudioQuality.STANDARD: {
                'mp3_bitrate': 192, 
                'wav_sample_rate': 44100,
                'wav_bit_depth': 16,
                'flac_compression': 5,
                'normalize_volume': True
            },
            AudioQuality.HIGH: {
                'mp3_bitrate': 320,
                'wav_sample_rate': 48000, 
                'wav_bit_depth': 24,
                'flac_compression': 3,
                'normalize_volume': True
            },
            AudioQuality.LOSSLESS: {
                'mp3_bitrate': 320,
                'wav_sample_rate': 96000,
                'wav_bit_depth': 24, 
                'flac_compression': 0,
                'normalize_volume': True
            }
        }
        return presets.get(quality, presets[AudioQuality.STANDARD])
    
    def apply_quality_preset(self, quality: AudioQuality):
        """Apply quality preset to current settings"""
        preset = self.get_quality_preset(quality)
        for key, value in preset.items():
            if hasattr(self, key):
                setattr(self, key, value)


class BatchExportJob:
    """Batch export job configuration"""
    
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.input_files: List[str] = []
        self.output_dir = ""
        self.formats: List[AudioFormat] = []
        self.settings = ExportSettings()
        self.status = "pending"  # pending, running, completed, failed
        self.progress = 0.0      # 0.0 to 1.0
        self.results: List[Dict] = []
        self.errors: List[str] = []


class AudioExporter:
    """Professional multi-format audio export system"""
    
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.active_jobs: Dict[str, BatchExportJob] = {}
        
    def _find_ffmpeg(self) -> Optional[str]:
        """Find FFmpeg executable"""
        # Try common locations
        common_paths = [
            "ffmpeg",
            "ffmpeg.exe", 
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg"
        ]
        
        for path in common_paths:
            if shutil.which(path):
                return path
                
        print("⚠️ Warning: FFmpeg not found. Install FFmpeg for best quality exports.")
        return None
    
    def _get_audio_info(self, audio_path: str) -> Dict:
        """Get audio file information using FFprobe"""
        if not self.ffmpeg_path:
            return {}
            
        try:
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg', 'ffprobe')
            cmd = [
                ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return info
        except Exception as e:
            print(f"⚠️ Error getting audio info: {e}")
            
        return {}
    
    def _build_ffmpeg_command(self, input_path: str, output_path: str, 
                            audio_format: AudioFormat, settings: ExportSettings) -> List[str]:
        """Build FFmpeg command for specific format"""
        if not self.ffmpeg_path:
            raise Exception("FFmpeg not available")
            
        cmd = [self.ffmpeg_path, '-i', input_path, '-y']  # -y to overwrite
        
        # Audio filters
        filters = []
        
        # Volume normalization
        if settings.normalize_volume:
            filters.append(f'loudnorm=I={settings.target_lufs}:TP=-1:LRA=7')
        
        # Fade effects
        if settings.fade_in_ms > 0:
            filters.append(f'afade=t=in:ss=0:d={settings.fade_in_ms/1000}')
        if settings.fade_out_ms > 0:
            filters.append(f'afade=t=out:st=-{settings.fade_out_ms/1000}:d={settings.fade_out_ms/1000}')
        
        # Silence removal
        if settings.remove_silence:
            filters.append('silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse')
        
        # Apply filters
        if filters:
            cmd.extend(['-af', ','.join(filters)])
        
        # Format-specific settings
        if audio_format == AudioFormat.MP3:
            cmd.extend(['-codec:a', 'libmp3lame'])
            if settings.mp3_vbr:
                cmd.extend(['-q:a', '0'])  # VBR highest quality
            else:
                cmd.extend(['-b:a', f'{settings.mp3_bitrate}k'])
                
        elif audio_format == AudioFormat.WAV:
            cmd.extend(['-codec:a', 'pcm_s24le'])  # 24-bit PCM
            cmd.extend(['-ar', str(settings.wav_sample_rate)])
            
        elif audio_format == AudioFormat.FLAC:
            cmd.extend(['-codec:a', 'flac'])
            cmd.extend(['-compression_level', str(settings.flac_compression)])
            cmd.extend(['-ar', str(settings.wav_sample_rate)])
            
        elif audio_format == AudioFormat.OGG:
            cmd.extend(['-codec:a', 'libvorbis'])
            cmd.extend(['-q:a', '6'])  # Quality level 6 (192kbps equivalent)
            
        elif audio_format == AudioFormat.M4A:
            cmd.extend(['-codec:a', 'aac'])
            cmd.extend(['-b:a', '256k'])
        
        cmd.append(output_path)
        return cmd
    
    def export_single_file(self, input_path: str, output_path: str, 
                          audio_format: AudioFormat, settings: ExportSettings) -> bool:
        """Export single file to specified format"""
        try:
            if not os.path.exists(input_path):
                print(f"❌ Input file not found: {input_path}")
                return False
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Fallback mode if FFmpeg not available
            if not self.ffmpeg_path:
                return self._fallback_export(input_path, output_path, audio_format)
            
            # Get audio info
            audio_info = self._get_audio_info(input_path)
            if audio_info:
                duration = float(audio_info.get('format', {}).get('duration', 0))
                print(f"🎵 Processing: {os.path.basename(input_path)} ({duration:.1f}s)")
            
            # Build and execute FFmpeg command
            cmd = self._build_ffmpeg_command(input_path, output_path, audio_format, settings)
            
            print(f"🔄 Exporting to {audio_format.value.upper()}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"✅ Export successful: {os.path.basename(output_path)} ({file_size:.1f}MB)")
                return True
            else:
                print(f"❌ Export failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
    
    def _fallback_export(self, input_path: str, output_path: str, audio_format: AudioFormat) -> bool:
        """Fallback export using simple file copy for supported formats"""
        try:
            import shutil
            
            # Only support MP3 copy in fallback mode
            if audio_format == AudioFormat.MP3 and input_path.lower().endswith('.mp3'):
                shutil.copy2(input_path, output_path)
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"📋 Fallback copy: {os.path.basename(output_path)} ({file_size:.1f}MB)")
                return True
            else:
                print(f"❌ Export error: FFmpeg not available")
                return False
                
        except Exception as e:
            print(f"❌ Fallback export error: {e}")
            return False
    
    def export_multiple_formats(self, input_path: str, output_dir: str, 
                               formats: List[AudioFormat], settings: ExportSettings) -> Dict[str, bool]:
        """Export single file to multiple formats"""
        results = {}
        base_name = Path(input_path).stem
        
        print(f"🚀 Multi-format export: {base_name}")
        
        for audio_format in formats:
            output_filename = f"{base_name}.{audio_format.value}"
            output_path = os.path.join(output_dir, output_filename)
            
            success = self.export_single_file(input_path, output_path, audio_format, settings)
            results[audio_format.value] = success
            
        return results
    
    def create_batch_job(self, name: str, input_files: List[str], output_dir: str, 
                        formats: List[AudioFormat], settings: ExportSettings) -> str:
        """Create new batch export job"""
        job_id = f"batch_{len(self.active_jobs)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = BatchExportJob(name)
        job.input_files = input_files
        job.output_dir = output_dir
        job.formats = formats
        job.settings = settings
        
        self.active_jobs[job_id] = job
        return job_id
    
    def execute_batch_job(self, job_id: str) -> bool:
        """Execute batch export job"""
        if job_id not in self.active_jobs:
            print(f"❌ Job not found: {job_id}")
            return False
            
        job = self.active_jobs[job_id]
        job.status = "running"
        job.progress = 0.0
        
        print(f"🚀 Starting batch job: {job.name}")
        print(f"📁 Files: {len(job.input_files)}")
        print(f"🎵 Formats: {[f.value for f in job.formats]}")
        
        total_tasks = len(job.input_files) * len(job.formats)
        completed_tasks = 0
        
        try:
            for input_file in job.input_files:
                if not os.path.exists(input_file):
                    error_msg = f"Input file not found: {input_file}"
                    job.errors.append(error_msg)
                    print(f"⚠️ {error_msg}")
                    continue
                
                # Process each format
                file_results = self.export_multiple_formats(
                    input_file, job.output_dir, job.formats, job.settings
                )
                
                # Record results
                result_entry = {
                    'input_file': input_file,
                    'formats': file_results,
                    'timestamp': datetime.now().isoformat()
                }
                job.results.append(result_entry)
                
                # Update progress
                completed_tasks += len(job.formats)
                job.progress = completed_tasks / total_tasks
                print(f"📊 Progress: {job.progress*100:.1f}%")
            
            job.status = "completed"
            print(f"🎉 Batch job completed: {job.name}")
            return True
            
        except Exception as e:
            job.status = "failed"
            job.errors.append(str(e))
            print(f"❌ Batch job failed: {e}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get batch job status"""
        if job_id not in self.active_jobs:
            return None
            
        job = self.active_jobs[job_id]
        return {
            'name': job.name,
            'status': job.status,
            'progress': job.progress,
            'files_processed': len(job.results),
            'total_files': len(job.input_files),
            'errors': job.errors,
            'created_at': job.created_at
        }
    
    def get_format_recommendations(self, use_case: str) -> Dict[str, any]:
        """Get format recommendations for specific use cases"""
        recommendations = {
            'youtube': {
                'primary': AudioFormat.MP3,
                'settings': {'mp3_bitrate': 192, 'target_lufs': -16.0},
                'description': 'Optimized for YouTube upload'
            },
            'podcast': {
                'primary': AudioFormat.MP3,
                'settings': {'mp3_bitrate': 128, 'target_lufs': -23.0},
                'description': 'Podcast distribution standard'
            },
            'audiobook': {
                'primary': AudioFormat.MP3,
                'secondary': AudioFormat.M4A,
                'settings': {'mp3_bitrate': 64, 'target_lufs': -20.0},
                'description': 'Audiobook platforms'
            },
            'music_production': {
                'primary': AudioFormat.WAV,
                'secondary': AudioFormat.FLAC,
                'settings': {'wav_sample_rate': 48000, 'wav_bit_depth': 24},
                'description': 'Professional audio production'
            },
            'archival': {
                'primary': AudioFormat.FLAC,
                'settings': {'flac_compression': 5},
                'description': 'Long-term storage'
            }
        }
        
        return recommendations.get(use_case, recommendations['youtube'])
    
    def export_with_preset(self, input_files: List[str], output_dir: str, 
                          use_case: str, quality: AudioQuality = AudioQuality.STANDARD) -> str:
        """Export with predefined preset for specific use case"""
        # Get recommendations
        rec = self.get_format_recommendations(use_case)
        
        # Setup settings
        settings = ExportSettings()
        settings.apply_quality_preset(quality)
        
        # Apply use case specific settings
        if 'settings' in rec:
            for key, value in rec['settings'].items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
        
        # Determine formats
        formats = [rec['primary']]
        if 'secondary' in rec:
            formats.append(rec['secondary'])
        
        # Create and execute batch job
        job_name = f"{use_case}_{quality.value}_export"
        job_id = self.create_batch_job(job_name, input_files, output_dir, formats, settings)
        
        success = self.execute_batch_job(job_id)
        if success:
            print(f"✅ Preset export completed: {use_case} ({quality.value})")
        
        return job_id


# Usage example
if __name__ == "__main__":
    # Initialize exporter
    exporter = AudioExporter()
    
    # Test single file export
    input_file = "./voice_studio_output/segment_1_complete.mp3"
    output_dir = "./exports"
    
    if os.path.exists(input_file):
        # Multi-format export
        formats = [AudioFormat.MP3, AudioFormat.WAV, AudioFormat.FLAC]
        settings = ExportSettings()
        settings.apply_quality_preset(AudioQuality.HIGH)
        
        results = exporter.export_multiple_formats(input_file, output_dir, formats, settings)
        print(f"Export results: {results}")
        
        # Preset export for YouTube
        job_id = exporter.export_with_preset(
            [input_file], output_dir, "youtube", AudioQuality.STANDARD
        )
        status = exporter.get_job_status(job_id)
        print(f"Job status: {status}")
    else:
        print(f"Test file not found: {input_file}")
        print("Testing format recommendations...")
        
        for use_case in ['youtube', 'podcast', 'audiobook', 'music_production']:
            rec = exporter.get_format_recommendations(use_case)
=======
"""
Voice Studio Audio Exporter - Multi-Format Professional Export System
Support cho WAV, MP3, FLAC với quality optimization
"""

import os
import subprocess
import shutil
from typing import List, Dict, Optional, Tuple
from enum import Enum
from pathlib import Path
import json
from datetime import datetime


class AudioFormat(Enum):
    """Supported audio formats"""
    MP3 = "mp3"
    WAV = "wav" 
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"


class AudioQuality(Enum):
    """Audio quality presets"""
    DRAFT = "draft"         # Fast export, lower quality
    STANDARD = "standard"   # Balanced quality/size
    HIGH = "high"           # High quality
    LOSSLESS = "lossless"   # Maximum quality


class ExportSettings:
    """Audio export configuration"""
    
    def __init__(self):
        # Format-specific settings
        self.mp3_bitrate = 320      # kbps
        self.mp3_vbr = False        # Use CBR by default
        
        self.wav_sample_rate = 48000  # Hz
        self.wav_bit_depth = 24       # bits
        
        self.flac_compression = 5     # 0-8, higher = smaller file
        
        # Universal settings
        self.normalize_volume = True
        self.target_lufs = -23.0     # EBU R128 broadcast standard
        self.remove_silence = False  # Preserve artistic intent
        self.fade_in_ms = 0         # Fade in duration
        self.fade_out_ms = 0        # Fade out duration
        
    def get_quality_preset(self, quality: AudioQuality) -> Dict:
        """Get preset settings for quality level"""
        presets = {
            AudioQuality.DRAFT: {
                'mp3_bitrate': 128,
                'wav_sample_rate': 44100,
                'wav_bit_depth': 16,
                'flac_compression': 8,
                'normalize_volume': False
            },
            AudioQuality.STANDARD: {
                'mp3_bitrate': 192, 
                'wav_sample_rate': 44100,
                'wav_bit_depth': 16,
                'flac_compression': 5,
                'normalize_volume': True
            },
            AudioQuality.HIGH: {
                'mp3_bitrate': 320,
                'wav_sample_rate': 48000, 
                'wav_bit_depth': 24,
                'flac_compression': 3,
                'normalize_volume': True
            },
            AudioQuality.LOSSLESS: {
                'mp3_bitrate': 320,
                'wav_sample_rate': 96000,
                'wav_bit_depth': 24, 
                'flac_compression': 0,
                'normalize_volume': True
            }
        }
        return presets.get(quality, presets[AudioQuality.STANDARD])
    
    def apply_quality_preset(self, quality: AudioQuality):
        """Apply quality preset to current settings"""
        preset = self.get_quality_preset(quality)
        for key, value in preset.items():
            if hasattr(self, key):
                setattr(self, key, value)


class BatchExportJob:
    """Batch export job configuration"""
    
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.input_files: List[str] = []
        self.output_dir = ""
        self.formats: List[AudioFormat] = []
        self.settings = ExportSettings()
        self.status = "pending"  # pending, running, completed, failed
        self.progress = 0.0      # 0.0 to 1.0
        self.results: List[Dict] = []
        self.errors: List[str] = []


class AudioExporter:
    """Professional multi-format audio export system"""
    
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.active_jobs: Dict[str, BatchExportJob] = {}
        
    def _find_ffmpeg(self) -> Optional[str]:
        """Find FFmpeg executable"""
        # Try common locations
        common_paths = [
            "ffmpeg",
            "ffmpeg.exe", 
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg"
        ]
        
        for path in common_paths:
            if shutil.which(path):
                return path
                
        print("[WARNING] Warning: FFmpeg not found. Install FFmpeg for best quality exports.")
        return None
    
    def _get_audio_info(self, audio_path: str) -> Dict:
        """Get audio file information using FFprobe"""
        if not self.ffmpeg_path:
            return {}
            
        try:
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg', 'ffprobe')
            cmd = [
                ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return info
        except Exception as e:
            print(f"[WARNING] Error getting audio info: {e}")
            
        return {}
    
    def _build_ffmpeg_command(self, input_path: str, output_path: str, 
                            audio_format: AudioFormat, settings: ExportSettings) -> List[str]:
        """Build FFmpeg command for specific format"""
        if not self.ffmpeg_path:
            raise Exception("FFmpeg not available")
            
        cmd = [self.ffmpeg_path, '-i', input_path, '-y']  # -y to overwrite
        
        # Audio filters
        filters = []
        
        # Volume normalization
        if settings.normalize_volume:
            filters.append(f'loudnorm=I={settings.target_lufs}:TP=-1:LRA=7')
        
        # Fade effects
        if settings.fade_in_ms > 0:
            filters.append(f'afade=t=in:ss=0:d={settings.fade_in_ms/1000}')
        if settings.fade_out_ms > 0:
            filters.append(f'afade=t=out:st=-{settings.fade_out_ms/1000}:d={settings.fade_out_ms/1000}')
        
        # Silence removal
        if settings.remove_silence:
            filters.append('silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse')
        
        # Apply filters
        if filters:
            cmd.extend(['-af', ','.join(filters)])
        
        # Format-specific settings
        if audio_format == AudioFormat.MP3:
            cmd.extend(['-codec:a', 'libmp3lame'])
            if settings.mp3_vbr:
                cmd.extend(['-q:a', '0'])  # VBR highest quality
            else:
                cmd.extend(['-b:a', f'{settings.mp3_bitrate}k'])
                
        elif audio_format == AudioFormat.WAV:
            cmd.extend(['-codec:a', 'pcm_s24le'])  # 24-bit PCM
            cmd.extend(['-ar', str(settings.wav_sample_rate)])
            
        elif audio_format == AudioFormat.FLAC:
            cmd.extend(['-codec:a', 'flac'])
            cmd.extend(['-compression_level', str(settings.flac_compression)])
            cmd.extend(['-ar', str(settings.wav_sample_rate)])
            
        elif audio_format == AudioFormat.OGG:
            cmd.extend(['-codec:a', 'libvorbis'])
            cmd.extend(['-q:a', '6'])  # Quality level 6 (192kbps equivalent)
            
        elif audio_format == AudioFormat.M4A:
            cmd.extend(['-codec:a', 'aac'])
            cmd.extend(['-b:a', '256k'])
        
        cmd.append(output_path)
        return cmd
    
    def export_single_file(self, input_path: str, output_path: str, 
                          audio_format: AudioFormat, settings: ExportSettings) -> bool:
        """Export single file to specified format"""
        try:
            if not os.path.exists(input_path):
                print(f"[EMOJI] Input file not found: {input_path}")
                return False
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Fallback mode if FFmpeg not available
            if not self.ffmpeg_path:
                return self._fallback_export(input_path, output_path, audio_format)
            
            # Get audio info
            audio_info = self._get_audio_info(input_path)
            if audio_info:
                duration = float(audio_info.get('format', {}).get('duration', 0))
                print(f"[MUSIC] Processing: {os.path.basename(input_path)} ({duration:.1f}s)")
            
            # Build and execute FFmpeg command
            cmd = self._build_ffmpeg_command(input_path, output_path, audio_format, settings)
            
            print(f"[REFRESH] Exporting to {audio_format.value.upper()}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"[OK] Export successful: {os.path.basename(output_path)} ({file_size:.1f}MB)")
                return True
            else:
                print(f"[EMOJI] Export failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[EMOJI] Export error: {e}")
            return False
    
    def _fallback_export(self, input_path: str, output_path: str, audio_format: AudioFormat) -> bool:
        """Fallback export using simple file copy for supported formats"""
        try:
            import shutil
            
            # Only support MP3 copy in fallback mode
            if audio_format == AudioFormat.MP3 and input_path.lower().endswith('.mp3'):
                shutil.copy2(input_path, output_path)
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"[CLIPBOARD] Fallback copy: {os.path.basename(output_path)} ({file_size:.1f}MB)")
                return True
            else:
                print(f"[EMOJI] Export error: FFmpeg not available")
                return False
                
        except Exception as e:
            print(f"[EMOJI] Fallback export error: {e}")
            return False
    
    def export_multiple_formats(self, input_path: str, output_dir: str, 
                               formats: List[AudioFormat], settings: ExportSettings) -> Dict[str, bool]:
        """Export single file to multiple formats"""
        results = {}
        base_name = Path(input_path).stem
        
        print(f"[ROCKET] Multi-format export: {base_name}")
        
        for audio_format in formats:
            output_filename = f"{base_name}.{audio_format.value}"
            output_path = os.path.join(output_dir, output_filename)
            
            success = self.export_single_file(input_path, output_path, audio_format, settings)
            results[audio_format.value] = success
            
        return results
    
    def create_batch_job(self, name: str, input_files: List[str], output_dir: str, 
                        formats: List[AudioFormat], settings: ExportSettings) -> str:
        """Create new batch export job"""
        job_id = f"batch_{len(self.active_jobs)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = BatchExportJob(name)
        job.input_files = input_files
        job.output_dir = output_dir
        job.formats = formats
        job.settings = settings
        
        self.active_jobs[job_id] = job
        return job_id
    
    def execute_batch_job(self, job_id: str) -> bool:
        """Execute batch export job"""
        if job_id not in self.active_jobs:
            print(f"[EMOJI] Job not found: {job_id}")
            return False
            
        job = self.active_jobs[job_id]
        job.status = "running"
        job.progress = 0.0
        
        print(f"[ROCKET] Starting batch job: {job.name}")
        print(f"[FOLDER] Files: {len(job.input_files)}")
        print(f"[MUSIC] Formats: {[f.value for f in job.formats]}")
        
        total_tasks = len(job.input_files) * len(job.formats)
        completed_tasks = 0
        
        try:
            for input_file in job.input_files:
                if not os.path.exists(input_file):
                    error_msg = f"Input file not found: {input_file}"
                    job.errors.append(error_msg)
                    print(f"[WARNING] {error_msg}")
                    continue
                
                # Process each format
                file_results = self.export_multiple_formats(
                    input_file, job.output_dir, job.formats, job.settings
                )
                
                # Record results
                result_entry = {
                    'input_file': input_file,
                    'formats': file_results,
                    'timestamp': datetime.now().isoformat()
                }
                job.results.append(result_entry)
                
                # Update progress
                completed_tasks += len(job.formats)
                job.progress = completed_tasks / total_tasks
                print(f"[STATS] Progress: {job.progress*100:.1f}%")
            
            job.status = "completed"
            print(f"[SUCCESS] Batch job completed: {job.name}")
            return True
            
        except Exception as e:
            job.status = "failed"
            job.errors.append(str(e))
            print(f"[EMOJI] Batch job failed: {e}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get batch job status"""
        if job_id not in self.active_jobs:
            return None
            
        job = self.active_jobs[job_id]
        return {
            'name': job.name,
            'status': job.status,
            'progress': job.progress,
            'files_processed': len(job.results),
            'total_files': len(job.input_files),
            'errors': job.errors,
            'created_at': job.created_at
        }
    
    def get_format_recommendations(self, use_case: str) -> Dict[str, any]:
        """Get format recommendations for specific use cases"""
        recommendations = {
            'youtube': {
                'primary': AudioFormat.MP3,
                'settings': {'mp3_bitrate': 192, 'target_lufs': -16.0},
                'description': 'Optimized for YouTube upload'
            },
            'podcast': {
                'primary': AudioFormat.MP3,
                'settings': {'mp3_bitrate': 128, 'target_lufs': -23.0},
                'description': 'Podcast distribution standard'
            },
            'audiobook': {
                'primary': AudioFormat.MP3,
                'secondary': AudioFormat.M4A,
                'settings': {'mp3_bitrate': 64, 'target_lufs': -20.0},
                'description': 'Audiobook platforms'
            },
            'music_production': {
                'primary': AudioFormat.WAV,
                'secondary': AudioFormat.FLAC,
                'settings': {'wav_sample_rate': 48000, 'wav_bit_depth': 24},
                'description': 'Professional audio production'
            },
            'archival': {
                'primary': AudioFormat.FLAC,
                'settings': {'flac_compression': 5},
                'description': 'Long-term storage'
            }
        }
        
        return recommendations.get(use_case, recommendations['youtube'])
    
    def export_with_preset(self, input_files: List[str], output_dir: str, 
                          use_case: str, quality: AudioQuality = AudioQuality.STANDARD) -> str:
        """Export with predefined preset for specific use case"""
        # Get recommendations
        rec = self.get_format_recommendations(use_case)
        
        # Setup settings
        settings = ExportSettings()
        settings.apply_quality_preset(quality)
        
        # Apply use case specific settings
        if 'settings' in rec:
            for key, value in rec['settings'].items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
        
        # Determine formats
        formats = [rec['primary']]
        if 'secondary' in rec:
            formats.append(rec['secondary'])
        
        # Create and execute batch job
        job_name = f"{use_case}_{quality.value}_export"
        job_id = self.create_batch_job(job_name, input_files, output_dir, formats, settings)
        
        success = self.execute_batch_job(job_id)
        if success:
            print(f"[OK] Preset export completed: {use_case} ({quality.value})")
        
        return job_id


# Usage example
if __name__ == "__main__":
    # Initialize exporter
    exporter = AudioExporter()
    
    # Test single file export
    input_file = "./voice_studio_output/segment_1_complete.mp3"
    output_dir = "./exports"
    
    if os.path.exists(input_file):
        # Multi-format export
        formats = [AudioFormat.MP3, AudioFormat.WAV, AudioFormat.FLAC]
        settings = ExportSettings()
        settings.apply_quality_preset(AudioQuality.HIGH)
        
        results = exporter.export_multiple_formats(input_file, output_dir, formats, settings)
        print(f"Export results: {results}")
        
        # Preset export for YouTube
        job_id = exporter.export_with_preset(
            [input_file], output_dir, "youtube", AudioQuality.STANDARD
        )
        status = exporter.get_job_status(job_id)
        print(f"Job status: {status}")
    else:
        print(f"Test file not found: {input_file}")
        print("Testing format recommendations...")
        
        for use_case in ['youtube', 'podcast', 'audiobook', 'music_production']:
            rec = exporter.get_format_recommendations(use_case)
>>>>>>> Stashed changes
            print(f"  {use_case}: {rec['primary'].value} - {rec['description']}") 