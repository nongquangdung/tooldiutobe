"""

Audio Post-Processing Pipeline - PHASE 2 Implementation

Broadcast-quality audio processing với EBU R128 normalization

"""



import os

import subprocess

import tempfile

from typing import List, Optional, Dict, Any

from dataclasses import dataclass

import json





@dataclass

class AudioQualitySettings:

    """Settings cho audio quality processing"""

    target_lufs: float = -23.0  # EBU R128 broadcast standard

    peak_limit: float = -1.0    # True peak limiter

    lra_range: float = 7.0      # Loudness range

    remove_silence: bool = True

    silence_threshold: float = 0.1

    apply_compression: bool = True

    compression_ratio: float = 2.5

    apply_noise_gate: bool = True

    noise_gate_threshold: float = -40.0





class AudioProcessor:

    """Professional audio post-processing pipeline"""

    

    def __init__(self, quality_settings: AudioQualitySettings = None):

        self.settings = quality_settings or AudioQualitySettings()

        self.temp_dir = tempfile.mkdtemp(prefix="voice_studio_audio_")

        self.processing_log = []

        self.ffmpeg_available = self._check_ffmpeg_availability()
        
        if not self.ffmpeg_available:
            self.processing_log.append("⚠️ FFmpeg not available - using fallback mode")

        

    def _check_ffmpeg_availability(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def process_audio_file(self, input_path: str, output_path: str, 

                          export_formats: List[str] = None) -> Dict[str, Any]:

        """

        Process single audio file với full pipeline

        

        Returns:

            Dict với processing results và metrics

        """

        if export_formats is None:

            export_formats = ['mp3']

            

        results = {

            'success': False,

            'input_path': input_path,

            'output_files': {},

            'processing_log': [],

            'audio_metrics': {},

            'error': None

        }

        

        try:

            # Validate input

            if not os.path.exists(input_path):

                raise FileNotFoundError(f"Input file not found: {input_path}")

            

            # Create temp file for processing

            temp_processed = os.path.join(self.temp_dir, f"processed_{os.path.basename(input_path)}")

            

            # Apply processing pipeline

            processed_file = self._apply_processing_pipeline(input_path, temp_processed)

            results['processing_log'].extend(self.processing_log)

            

            # Export to requested formats

            for format_type in export_formats:

                output_file = f"{output_path}.{format_type}"

                success = self._export_format(processed_file, output_file, format_type)

                if success:

                    results['output_files'][format_type] = output_file

            

            results['success'] = len(results['output_files']) > 0

            

        except Exception as e:

            results['error'] = str(e)

            self.processing_log.append(f"❌ Error: {str(e)}")

            

        return results

    

    def _apply_processing_pipeline(self, input_path: str, output_path: str) -> str:

        """Apply complete audio processing pipeline"""

        current_file = input_path

        pipeline_steps = []

        

        if not self.ffmpeg_available:

            # Fallback mode: simple file copy with logging

            import shutil

            shutil.copy2(input_path, output_path)

            pipeline_steps.append("📋 Fallback mode: File copied without processing")

            pipeline_steps.append("💡 Install FFmpeg for full audio processing capabilities")

            self.processing_log.extend(pipeline_steps)

            return output_path

        

        # FFmpeg available - full processing pipeline

        # Step 1: Remove silence (if enabled)

        if self.settings.remove_silence:

            step1_file = os.path.join(self.temp_dir, "step1_silence_removed.wav")

            current_file = self._remove_silence(current_file, step1_file)

            pipeline_steps.append("✅ Silence removal")

        

        # Step 2: Apply compression (if enabled)

        if self.settings.apply_compression:

            step2_file = os.path.join(self.temp_dir, "step2_compressed.wav")

            current_file = self._apply_compression(current_file, step2_file)

            pipeline_steps.append("✅ Dynamic compression")

        

        # Step 3: EBU R128 Normalization (always applied)

        current_file = self._normalize_ebu_r128(current_file, output_path)

        pipeline_steps.append(f"✅ EBU R128 normalization to {self.settings.target_lufs} LUFS")

        

        self.processing_log.extend(pipeline_steps)

        return current_file

    

    def _remove_silence(self, input_path: str, output_path: str) -> str:

        """Remove silence using FFmpeg silenceremove filter"""

        cmd = [

            'ffmpeg', '-i', input_path,

            '-af', f'silenceremove=start_periods=1:start_silence={self.settings.silence_threshold}:start_threshold=-40dB',

            '-y', output_path

        ]

        

        result = subprocess.run(cmd, capture_output=True, text=True)

        return output_path if os.path.exists(output_path) else input_path

    

    def _apply_compression(self, input_path: str, output_path: str) -> str:

        """Apply dynamic range compression"""

        cmd = [

            'ffmpeg', '-i', input_path,

            '-af', f'acompressor=ratio={self.settings.compression_ratio}:threshold=-20dB:attack=5:release=50',

            '-y', output_path

        ]

        

        result = subprocess.run(cmd, capture_output=True, text=True)

        return output_path if os.path.exists(output_path) else input_path

    

    def _normalize_ebu_r128(self, input_path: str, output_path: str) -> str:

        """Normalize audio to EBU R128 broadcast standard"""

        cmd = [

            'ffmpeg', '-i', input_path,

            '-af', f'loudnorm=I={self.settings.target_lufs}:TP={self.settings.peak_limit}:LRA={self.settings.lra_range}',

            '-ar', '48000',  # Broadcast sample rate

            '-y', output_path

        ]

        

        result = subprocess.run(cmd, capture_output=True, text=True)

        return output_path if os.path.exists(output_path) else input_path

    

    def _export_format(self, input_path: str, output_path: str, format_type: str) -> bool:

        """Export audio to specific format với quality presets"""

        if not self.ffmpeg_available:
            # Fallback mode: simple file copy for MP3, skip others
            if format_type == 'mp3':
                import shutil
                try:
                    shutil.copy2(input_path, output_path)
                    self.processing_log.append(f"📋 Fallback copy: {os.path.basename(output_path)}")
                    return True
                except Exception as e:
                    self.processing_log.append(f"❌ Fallback copy failed: {e}")
                    return False
            else:
                self.processing_log.append(f"⚠️ {format_type.upper()} export requires FFmpeg")
                return False
        
        # FFmpeg available - full export pipeline
        format_configs = {
            'mp3': ['-codec:a', 'libmp3lame', '-b:a', '320k', '-ar', '44100'],
            'wav': ['-codec:a', 'pcm_s24le', '-ar', '48000'],  # 24-bit WAV
            'flac': ['-codec:a', 'flac', '-compression_level', '8', '-ar', '48000']
        }
        
        if format_type not in format_configs:
            return False
        
        cmd = ['ffmpeg', '-i', input_path] + format_configs[format_type] + ['-y', output_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = result.returncode == 0 and os.path.exists(output_path)
        
        if success:
            self.processing_log.append(f"✅ Exported {format_type.upper()}: {os.path.basename(output_path)}")
        else:
            self.processing_log.append(f"❌ Export failed for {format_type}")
        
        return success





# Test function

def test_audio_processor():

    """Test audio processor với sample settings"""

    processor = AudioProcessor()

    

    print("🎵 Audio Processor PHASE 2 Test")

    print(f"Target LUFS: {processor.settings.target_lufs}")

    print(f"Remove Silence: {processor.settings.remove_silence}")

    print(f"Apply Compression: {processor.settings.apply_compression}")

    

    return processor





if __name__ == "__main__":

    test_audio_processor()

