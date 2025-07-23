"""
Pause Processor - Theo cách Chatterbox-Audiobook implement
Đơn giản: đếm line breaks, 0.1s per break
"""

import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)

class PauseProcessor:
    """
    Simple pause processor theo cách Chatterbox-Audiobook
    Chỉ đếm line breaks và tạo pause duration
    """
    
    def __init__(self, pause_duration: float = 0.1):
        """
        Args:
            pause_duration: Thời gian pause cho mỗi line break (giây)
        """
        self.pause_duration = pause_duration
        logger.info(f"PauseProcessor initialized with {pause_duration}s per line break")
    
    def process_text_for_pauses(self, text: str) -> Tuple[str, float]:
        """
        Process text to count returns and calculate total pause time.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (cleaned_text, total_pause_duration)
        """
        # Count line breaks (both \n and \r\n)
        return_count = text.count('\n') + text.count('\r')
        total_pause_duration = return_count * self.pause_duration
        
        # Clean up text for TTS (normalize line breaks but keep structure)
        cleaned_text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        logger.debug(f"Found {return_count} line breaks, total pause: {total_pause_duration}s")
        
        return cleaned_text, total_pause_duration
    
    def create_pause_audio(self, duration: float, sample_rate: int = 22050) -> np.ndarray:
        """
        Create silence audio for pause duration.
        
        Args:
            duration: Pause duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            numpy array of silence
        """
        if duration <= 0:
            return np.array([])
        
        samples = int(duration * sample_rate)
        silence = np.zeros(samples, dtype=np.float32)
        
        logger.debug(f"Created {duration}s pause audio ({samples} samples)")
        return silence
    
    def insert_pauses_in_segments(self, segments: List[np.ndarray], 
                                 pause_positions: List[int]) -> List[np.ndarray]:
        """
        Insert pause audio between segments at specified positions.
        
        Args:
            segments: List of audio segments
            pause_positions: List of positions where to insert pauses
            
        Returns:
            List of segments with pauses inserted
        """
        if not pause_positions:
            return segments
        
        result = []
        pause_audio = self.create_pause_audio(self.pause_duration)
        
        for i, segment in enumerate(segments):
            result.append(segment)
            
            # Insert pause if this position is in pause_positions
            if i in pause_positions and i < len(segments) - 1:  # Don't add pause after last segment
                result.append(pause_audio)
        
        logger.info(f"Inserted {len(pause_positions)} pauses between {len(segments)} segments")
        return result
    
    def process_multiline_text(self, text: str) -> List[Tuple[str, bool]]:
        """
        Split text by lines and mark which lines should have pauses after them.
        
        Args:
            text: Input text with line breaks
            
        Returns:
            List of (line_text, needs_pause_after) tuples
        """
        lines = text.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line:  # Only process non-empty lines
                # Add pause after line if it's not the last line
                needs_pause = i < len(lines) - 1
                result.append((line, needs_pause))
        
        logger.debug(f"Processed {len(lines)} lines, {sum(1 for _, needs_pause in result if needs_pause)} will have pauses")
        return result
    
    def get_pause_info(self, text: str) -> dict:
        """
        Get detailed pause information for text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with pause statistics
        """
        cleaned_text, total_pause_duration = self.process_text_for_pauses(text)
        lines = self.process_multiline_text(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'total_lines': len(lines),
            'lines_with_pauses': sum(1 for _, needs_pause in lines if needs_pause),
            'total_pause_duration': total_pause_duration,
            'pause_duration_per_break': self.pause_duration,
            'lines': lines
        }

# Convenience function
def create_pause_processor(pause_duration: float = 0.1) -> PauseProcessor:
    """
    Create a PauseProcessor instance.
    
    Args:
        pause_duration: Pause duration per line break in seconds
        
    Returns:
        PauseProcessor instance
    """
    return PauseProcessor(pause_duration) 