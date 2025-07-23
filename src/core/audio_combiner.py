"""
Audio Combiner - Theo cách Chatterbox-Audiobook implement
Đơn giản: chỉ numpy concatenate, không có audio processing phức tạp
"""

import numpy as np
import wave
import os
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AudioCombiner:
    """
    Simple audio combiner theo cách Chatterbox-Audiobook
    Chỉ numpy concatenate, không có audio processing phức tạp
    """
    
    def __init__(self, sample_rate: int = 22050):
        """
        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        logger.info(f"AudioCombiner initialized with sample rate: {sample_rate}")
    
    def save_audio_chunks(self, audio_chunks: List[np.ndarray], 
                         project_name: str, output_dir: str = "audiobook_projects") -> List[str]:
        """
        Save audio chunks to individual files.
        
        Args:
            audio_chunks: List of audio numpy arrays
            project_name: Name of the project
            output_dir: Output directory
            
        Returns:
            List of saved file paths
        """
        if not audio_chunks:
            logger.warning("No audio chunks to save")
            return []
        
        # Create output directory
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        saved_files = []
        
        for i, chunk in enumerate(audio_chunks):
            if chunk is None or len(chunk) == 0:
                logger.warning(f"Skipping empty chunk {i}")
                continue
            
            # Create filename
            chunk_filename = f"chunk_{i:03d}.wav"
            chunk_path = os.path.join(project_dir, chunk_filename)
            
            try:
                # Save chunk as WAV
                with wave.open(chunk_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(self.sample_rate)
                    
                    # Convert to int16 if needed
                    if chunk.dtype != np.int16:
                        if chunk.dtype == np.float32 or chunk.dtype == np.float64:
                            chunk = (chunk * 32767).astype(np.int16)
                        else:
                            chunk = chunk.astype(np.int16)
                    
                    wav_file.writeframes(chunk.tobytes())
                
                saved_files.append(chunk_path)
                logger.debug(f"Saved chunk {i} to {chunk_path}")
                
            except Exception as e:
                logger.error(f"Error saving chunk {i}: {e}")
        
        logger.info(f"Saved {len(saved_files)} audio chunks to {project_dir}")
        return saved_files
    
    def combine_audio_files(self, file_paths: List[str], output_path: str, 
                           output_format: str = "wav") -> str:
        """
        Combine multiple audio files into one.
        
        Args:
            file_paths: List of audio file paths
            output_path: Output file path
            output_format: Output format (wav only supported)
            
        Returns:
            Status message
        """
        if not file_paths:
            return "[EMOJI] No audio files provided"
        
        try:
            combined_audio = []
            
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    logger.warning(f"File not found: {file_path}")
                    continue
                
                # Read WAV file
                with wave.open(file_path, 'rb') as wav_file:
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                    combined_audio.append(audio_data)
            
            if not combined_audio:
                return "[EMOJI] No valid audio files found"
            
            # Concatenate all audio - đây là cách họ làm
            final_audio = np.concatenate(combined_audio)
            
            # Save combined audio
            if output_format.lower() == "wav":
                with wave.open(output_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(final_audio.tobytes())
            else:
                return "[EMOJI] Only WAV format supported"
            
            logger.info(f"Combined {len(file_paths)} files into {output_path}")
            return f"[OK] Combined {len(file_paths)} files into {output_path}"
            
        except Exception as e:
            logger.error(f"Error combining audio files: {e}")
            return f"[EMOJI] Error combining audio files: {str(e)}"
    
    def combine_audio_arrays(self, audio_arrays: List[np.ndarray], 
                            output_path: str) -> str:
        """
        Combine numpy audio arrays directly.
        
        Args:
            audio_arrays: List of numpy audio arrays
            output_path: Output file path
            
        Returns:
            Status message
        """
        if not audio_arrays:
            return "[EMOJI] No audio arrays provided"
        
        try:
            # Filter out empty arrays
            valid_arrays = [arr for arr in audio_arrays if arr is not None and len(arr) > 0]
            
            if not valid_arrays:
                return "[EMOJI] No valid audio arrays found"
            
            # Simple concatenation - theo cách Chatterbox-Audiobook
            final_audio = np.concatenate(valid_arrays)
            
            # Save as WAV
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                
                # Convert to int16 if needed
                if final_audio.dtype != np.int16:
                    if final_audio.dtype == np.float32 or final_audio.dtype == np.float64:
                        final_audio = (final_audio * 32767).astype(np.int16)
                    else:
                        final_audio = final_audio.astype(np.int16)
                
                wav_file.writeframes(final_audio.tobytes())
            
            logger.info(f"Combined {len(valid_arrays)} arrays into {output_path}")
            return f"[OK] Combined {len(valid_arrays)} audio segments"
            
        except Exception as e:
            logger.error(f"Error combining audio arrays: {e}")
            return f"[EMOJI] Error combining audio arrays: {str(e)}"
    
    def save_trimmed_audio(self, audio_data: Tuple[int, np.ndarray], 
                          original_file_path: str, chunk_num: int) -> Tuple[str, str]:
        """
        Save trimmed audio data to a new file.
        
        Args:
            audio_data: Audio data tuple (sample_rate, audio_array)
            original_file_path: Original audio file path
            chunk_num: Chunk number
            
        Returns:
            tuple: (success_message, file_path)
        """
        if audio_data is None:
            return "[EMOJI] No audio data provided", ""
        
        try:
            # Extract sample rate and audio array
            if isinstance(audio_data, tuple) and len(audio_data) == 2:
                sample_rate, audio_array = audio_data
            else:
                return "[EMOJI] Invalid audio data format", ""
            
            # Create trimmed file path
            base_dir = os.path.dirname(original_file_path)
            base_name = os.path.splitext(os.path.basename(original_file_path))[0]
            trimmed_path = os.path.join(base_dir, f"{base_name}_trimmed.wav")
            
            # Save trimmed audio
            with wave.open(trimmed_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                
                # Convert to int16 if needed
                if audio_array.dtype != np.int16:
                    if audio_array.dtype == np.float32 or audio_array.dtype == np.float64:
                        audio_array = (audio_array * 32767).astype(np.int16)
                    else:
                        audio_array = audio_array.astype(np.int16)
                
                wav_file.writeframes(audio_array.tobytes())
            
            logger.info(f"Saved trimmed audio for chunk {chunk_num}")
            return f"[OK] Trimmed audio saved for chunk {chunk_num}", trimmed_path
            
        except Exception as e:
            logger.error(f"Error saving trimmed audio: {e}")
            return f"[EMOJI] Error saving trimmed audio: {str(e)}", ""
    
    def cleanup_temp_files(self, file_paths: List[str]) -> None:
        """
        Clean up temporary files.
        
        Args:
            file_paths: List of file paths to delete
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.debug(f"Deleted temp file: {file_path}")
            except Exception as e:
                logger.warning(f"Could not delete {file_path}: {e}")
    
    def insert_silence(self, duration: float) -> np.ndarray:
        """
        Create silence audio array.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Silence audio array
        """
        if duration <= 0:
            return np.array([])
        
        samples = int(duration * self.sample_rate)
        silence = np.zeros(samples, dtype=np.int16)
        
        logger.debug(f"Created {duration}s silence ({samples} samples)")
        return silence
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        Get basic audio file information.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                duration = frames / sample_rate
                
                return {
                    'duration': duration,
                    'sample_rate': sample_rate,
                    'channels': channels,
                    'sample_width': sample_width,
                    'frames': frames,
                    'file_path': file_path
                }
        except Exception as e:
            logger.error(f"Error getting audio info for {file_path}: {e}")
            return {}

# Convenience function
def create_audio_combiner(sample_rate: int = 22050) -> AudioCombiner:
    """
    Create an AudioCombiner instance.
    
    Args:
        sample_rate: Audio sample rate
        
    Returns:
        AudioCombiner instance
    """
    return AudioCombiner(sample_rate) 