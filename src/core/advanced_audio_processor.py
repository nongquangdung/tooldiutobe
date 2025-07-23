#!/usr/bin/env python3
"""
[MUSIC] ADVANCED AUDIO PROCESSOR
============================

Advanced audio post-processing module tái tạo tính năng từ Chatterbox TTS Extended:
- Tích hợp Auto-editor: Cắt bỏ im lặng/giật hình/rối loạn
- Chuẩn hóa FFmpeg: EBU R128 và Peak normalization
- Multiple audio formats: WAV, MP3, FLAC
- Advanced file naming với timestamp và metadata
"""

import os
import subprocess
import tempfile
import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import time
from datetime import datetime
import shutil

logger = logging.getLogger(__name__)

@dataclass
class AudioProcessingConfig:
    """Cấu hình cho audio post-processing"""
    # Auto-editor settings
    enable_auto_editor: bool = True
    silence_threshold: float = 0.05  # Threshold for silence detection (0.0-1.0)
    min_silence_duration: float = 0.5  # Minimum silence duration to cut (seconds)
    margin: float = 0.1  # Margin to keep around speech (seconds)
    preserve_original: bool = True  # Keep original WAV before cleanup
    
    # FFmpeg normalization
    enable_ffmpeg_normalization: bool = True
    normalization_type: str = "ebu"  # "ebu" or "peak"
    
    # EBU R128 settings
    target_loudness: float = -23.0  # LUFS
    target_peak: float = -2.0  # dBFS
    target_range: float = 7.0  # LU (Loudness Units)
    
    # Peak normalization settings
    peak_target: float = -1.0  # dBFS
    
    # Output formats
    output_formats: List[str] = field(default_factory=lambda: ["wav", "mp3"])  # "wav", "mp3", "flac"
    mp3_bitrate: str = "320k"
    flac_compression: int = 5  # 0-8, higher = more compression
    
    # File naming
    include_timestamp: bool = True
    include_generation_id: bool = True
    include_seed: bool = True
    base_name: str = "generated"

@dataclass
class AudioProcessingResult:
    """Kết quả audio processing"""
    original_file: str
    processed_files: Dict[str, str]  # format -> file_path
    processing_stats: Dict[str, Any]
    processing_time: float
    metadata: Dict[str, Any]

class AdvancedAudioProcessor:
    """Advanced audio processor với đầy đủ tính năng post-processing"""
    
    def __init__(self, config: Optional[AudioProcessingConfig] = None):
        self.config = config or AudioProcessingConfig()
        self.ffmpeg_available = self._check_ffmpeg()
        self.auto_editor_available = self._check_auto_editor()
        
        # Processing stats
        self.processing_stats = {
            'files_processed': 0,
            'silence_removed_seconds': 0.0,
            'normalization_applied': 0,
            'formats_generated': 0,
            'total_processing_time': 0.0
        }
        
    def _check_ffmpeg(self) -> bool:
        """Kiểm tra FFmpeg availability"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5,
                                  stderr=subprocess.DEVNULL)  # Suppress stderr
            available = result.returncode == 0
            # Reduce logging noise
            if available:
                logger.debug("FFmpeg: [OK] Available")
            return available
        except Exception as e:
            # Suppress FFmpeg check warnings
            logger.debug(f"FFmpeg check failed: {e}")
            return False
    
    def _check_auto_editor(self) -> bool:
        """Kiểm tra Auto-editor availability"""
        try:
            result = subprocess.run(['auto-editor', '--version'], 
                                  capture_output=True, text=True, timeout=5,
                                  stderr=subprocess.DEVNULL)  # Suppress stderr
            available = result.returncode == 0
            # Reduce logging noise
            if available:
                logger.debug("Auto-editor: [OK] Available")
            return available
        except Exception as e:
            # Suppress auto-editor check warnings
            logger.debug(f"Auto-editor not found: {e}")
            return False
    
    def process_audio(self, input_file: str, output_dir: str, 
                     metadata: Optional[Dict[str, Any]] = None) -> AudioProcessingResult:
        """
        Main method để process audio file với tất cả các tính năng
        
        Args:
            input_file: Path to input audio file
            output_dir: Directory for output files
            metadata: Optional metadata (character_id, emotion, etc.)
            
        Returns:
            AudioProcessingResult object với file paths và stats
        """
        start_time = time.time()
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"[MUSIC] Starting advanced audio processing...")
        logger.info(f"   [FOLDER] Input: {os.path.basename(input_file)}")
        logger.info(f"   [FOLDER] Output dir: {output_dir}")
        
        # Initialize result
        processed_files = {}
        current_file = input_file
        processing_metadata = metadata or {}
        
        # Step 1: Auto-editor (silence removal)
        if self.config.enable_auto_editor and self.auto_editor_available:
            current_file = self._apply_auto_editor(current_file, output_dir)
            
        # Step 2: FFmpeg normalization
        if self.config.enable_ffmpeg_normalization and self.ffmpeg_available:
            current_file = self._apply_normalization(current_file, output_dir)
            
        # Step 3: Generate multiple formats
        processed_files = self._generate_output_formats(current_file, output_dir, processing_metadata)
        
        processing_time = time.time() - start_time
        self.processing_stats['total_processing_time'] += processing_time
        self.processing_stats['files_processed'] += 1
        
        logger.info(f"[OK] Audio processing completed in {processing_time:.2f}s")
        logger.info(f"   [STATS] Generated {len(processed_files)} format(s)")
        
        return AudioProcessingResult(
            original_file=input_file,
            processed_files=processed_files,
            processing_stats=self.processing_stats.copy(),
            processing_time=processing_time,
            metadata=processing_metadata
        )
    
    def _apply_auto_editor(self, input_file: str, output_dir: str) -> str:
        """Áp dụng auto-editor để cắt bỏ im lặng và artifacts"""
        logger.info("[THEATER] Applying auto-editor...")
        
        output_file = os.path.join(output_dir, "auto_edited.wav")
        
        # Build auto-editor command
        cmd = [
            'auto-editor', input_file,
            '--output', output_file,
            '--silence-threshold', str(self.config.silence_threshold),
            '--min-silence-duration', str(self.config.min_silence_duration),
            '--margin', str(self.config.margin),
            '--export', 'audio',
            '--audio-codec', 'pcm_s16le'  # High quality WAV
        ]
        
        try:
            logger.debug(f"Auto-editor command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                                  stderr=subprocess.DEVNULL)  # Suppress FFmpeg stderr
            
            if result.returncode == 0:
                logger.info(f"   [OK] Auto-editor completed: {os.path.basename(output_file)}")
                
                # Calculate silence removed (rough estimate)
                original_duration = self._get_audio_duration(input_file)
                edited_duration = self._get_audio_duration(output_file)
                silence_removed = max(0, original_duration - edited_duration)
                
                self.processing_stats['silence_removed_seconds'] += silence_removed
                logger.info(f"   [MUTE] Silence removed: {silence_removed:.2f}s")
                
                return output_file
            else:
                logger.debug(f"Auto-editor failed with return code: {result.returncode}")
                return input_file
                
        except subprocess.TimeoutExpired:
            logger.debug("Auto-editor timeout - using original file")
            return input_file
        except Exception as e:
            logger.debug(f"Auto-editor error: {e}")
            return input_file
    
    def _apply_normalization(self, input_file: str, output_dir: str) -> str:
        """Áp dụng FFmpeg normalization (EBU R128 hoặc Peak)"""
        logger.info(f"[AUDIO] Applying {self.config.normalization_type.upper()} normalization...")
        
        output_file = os.path.join(output_dir, "normalized.wav")
        
        if self.config.normalization_type == "ebu":
            # EBU R128 normalization
            filter_params = (
                f"loudnorm=I={self.config.target_loudness}:"
                f"TP={self.config.target_peak}:"
                f"LRA={self.config.target_range}:print_format=summary"
            )
        else:
            # Peak normalization
            filter_params = f"volume={self.config.peak_target}dB"
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', filter_params,
            '-ar', '44100',  # Standard sample rate
            '-ac', '2',      # Stereo
            '-y',            # Overwrite
            output_file
        ]
        
        try:
            logger.debug(f"FFmpeg normalization command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                                  stderr=subprocess.DEVNULL)  # Suppress FFmpeg stderr
            
            if result.returncode == 0:
                logger.info(f"   [OK] Normalization completed: {os.path.basename(output_file)}")
                self.processing_stats['normalization_applied'] += 1
                return output_file
            else:
                logger.debug(f"Normalization failed with return code: {result.returncode}")
                return input_file
                
        except subprocess.TimeoutExpired:
            logger.debug("Normalization timeout - using original file")
            return input_file
        except Exception as e:
            logger.debug(f"Normalization error: {e}")
            return input_file
    
    def _generate_output_formats(self, input_file: str, output_dir: str, 
                                metadata: Dict[str, Any]) -> Dict[str, str]:
        """Generate multiple output formats với advanced naming"""
        logger.info(f"[EMOJI] Generating {len(self.config.output_formats)} format(s)...")
        
        processed_files = {}
        
        # Generate base filename
        base_filename = self._generate_filename(metadata)
        
        for format_type in self.config.output_formats:
            try:
                output_file = os.path.join(output_dir, f"{base_filename}.{format_type}")
                
                if format_type == "wav":
                    # For WAV, just copy the processed file
                    shutil.copy2(input_file, output_file)
                    
                elif format_type == "mp3":
                    # Convert to MP3
                    self._convert_to_mp3(input_file, output_file)
                    
                elif format_type == "flac":
                    # Convert to FLAC
                    self._convert_to_flac(input_file, output_file)
                    
                if os.path.exists(output_file):
                    processed_files[format_type] = output_file
                    self.processing_stats['formats_generated'] += 1
                    logger.info(f"   [OK] Generated {format_type.upper()}: {os.path.basename(output_file)}")
                    
            except Exception as e:
                logger.error(f"Failed to generate {format_type}: {e}")
        
        return processed_files
    
    def _convert_to_mp3(self, input_file: str, output_file: str):
        """Convert to MP3 với high quality"""
        cmd = [
            'ffmpeg', '-i', input_file,
            '-acodec', 'mp3',
            '-ab', self.config.mp3_bitrate,
            '-ar', '44100',
            '-ac', '2',
            '-y', output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise Exception(f"MP3 conversion failed: {result.stderr}")
    
    def _convert_to_flac(self, input_file: str, output_file: str):
        """Convert to FLAC với compression"""
        cmd = [
            'ffmpeg', '-i', input_file,
            '-acodec', 'flac',
            '-compression_level', str(self.config.flac_compression),
            '-ar', '44100',
            '-ac', '2',
            '-y', output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise Exception(f"FLAC conversion failed: {result.stderr}")
    
    def _generate_filename(self, metadata: Dict[str, Any]) -> str:
        """Generate filename với timestamp, generation ID và seed"""
        parts = [self.config.base_name]
        
        # Add character/context info
        if 'character_id' in metadata:
            parts.append(metadata['character_id'])
        if 'emotion' in metadata:
            parts.append(metadata['emotion'])
            
        # Add timestamp
        if self.config.include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            parts.append(timestamp)
            
        # Add generation ID (hash of content)
        if self.config.include_generation_id:
            content_hash = hashlib.md5(str(metadata).encode()).hexdigest()[:8]
            parts.append(f"gen_{content_hash}")
            
        # Add seed if provided
        if self.config.include_seed and 'seed' in metadata:
            parts.append(f"seed_{metadata['seed']}")
            
        return "_".join(parts)
    
    def _get_audio_duration(self, file_path: str) -> float:
        """Lấy duration của audio file"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries',
                'format=duration', '-of', 'csv=p=0', file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return float(result.stdout.strip())
        except:
            return 0.0
    
    def get_processing_report(self) -> Dict[str, Any]:
        """Lấy báo cáo chi tiết về audio processing"""
        return {
            'config': {
                'auto_editor_enabled': self.config.enable_auto_editor,
                'normalization_enabled': self.config.enable_ffmpeg_normalization,
                'normalization_type': self.config.normalization_type,
                'output_formats': self.config.output_formats,
                'preserve_original': self.config.preserve_original
            },
            'availability': {
                'ffmpeg': self.ffmpeg_available,
                'auto_editor': self.auto_editor_available
            },
            'stats': self.processing_stats,
            'settings': {
                'silence_threshold': self.config.silence_threshold,
                'target_loudness': self.config.target_loudness,
                'mp3_bitrate': self.config.mp3_bitrate,
                'flac_compression': self.config.flac_compression
            }
        }
    
    def batch_process(self, input_files: List[str], output_dir: str, 
                     metadata_list: Optional[List[Dict[str, Any]]] = None) -> List[AudioProcessingResult]:
        """Batch process multiple audio files"""
        logger.info(f"[MUSIC] Starting batch audio processing for {len(input_files)} files...")
        
        results = []
        metadata_list = metadata_list or [{}] * len(input_files)
        
        for i, (input_file, metadata) in enumerate(zip(input_files, metadata_list)):
            logger.info(f"[FOLDER] Processing file {i+1}/{len(input_files)}: {os.path.basename(input_file)}")
            
            try:
                # Create subdirectory for each file
                file_output_dir = os.path.join(output_dir, f"file_{i+1:03d}")
                result = self.process_audio(input_file, file_output_dir, metadata)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to process {input_file}: {e}")
                
        logger.info(f"[OK] Batch processing completed: {len(results)}/{len(input_files)} successful")
        return results

# Convenience functions
def create_default_processor() -> AdvancedAudioProcessor:
    """Tạo processor với cấu hình mặc định"""
    return AdvancedAudioProcessor()

def create_quality_processor() -> AdvancedAudioProcessor:
    """Tạo processor tối ưu cho chất lượng"""
    config = AudioProcessingConfig(
        enable_auto_editor=True,
        silence_threshold=0.03,  # More sensitive
        min_silence_duration=0.3,  # Shorter minimum
        margin=0.15,  # More margin for safety
        enable_ffmpeg_normalization=True,
        normalization_type="ebu",
        target_loudness=-16.0,  # Louder for better quality
        output_formats=["wav", "mp3", "flac"],
        mp3_bitrate="320k",
        flac_compression=8,  # Maximum compression
        preserve_original=True
    )
    return AdvancedAudioProcessor(config)

def create_fast_processor() -> AdvancedAudioProcessor:
    """Tạo processor tối ưu cho tốc độ"""
    config = AudioProcessingConfig(
        enable_auto_editor=False,  # Skip for speed
        enable_ffmpeg_normalization=True,
        normalization_type="peak",  # Faster than EBU
        output_formats=["mp3"],  # Only MP3
        mp3_bitrate="192k",  # Lower bitrate
        preserve_original=False,
        include_timestamp=False,
        include_generation_id=False
    )
    return AdvancedAudioProcessor(config)

if __name__ == "__main__":
    # Test the processor
    processor = create_default_processor()
    print("Audio processor initialized")
    print(f"FFmpeg available: {processor.ffmpeg_available}")
    print(f"Auto-editor available: {processor.auto_editor_available}")
    
    # Print configuration
    report = processor.get_processing_report()
    print(json.dumps(report, indent=2)) 