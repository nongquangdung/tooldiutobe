#!/usr/bin/env python3
"""
[TOOL] AUDIO METADATA FIXER
======================

Fix MP3 metadata duration cho merged audio files.
Vấn đề: Binary concatenation không update metadata duration đúng.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

class AudioMetadataFixer:
    """Fix audio metadata issues cho merged files"""
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
        
    def _check_ffmpeg(self) -> bool:
        """Check nếu FFmpeg available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            return True
        except FileNotFoundError:
            return False
    
    def get_actual_duration(self, audio_path: str) -> Optional[float]:
        """Get duration thực tế của audio file bằng FFmpeg"""
        if not self.ffmpeg_available:
            return None
            
        try:
            cmd = [
                'ffmpeg', '-i', audio_path,
                '-f', 'null', '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse duration từ FFmpeg output
            for line in result.stderr.split('\n'):
                if 'Duration:' in line:
                    # Extract "Duration: 00:02:35.42"
                    duration_str = line.split('Duration:')[1].split(',')[0].strip()
                    return self._parse_duration_string(duration_str)
                    
        except Exception as e:
            print(f"[EMOJI] Error getting duration: {e}")
            
        return None
    
    def _parse_duration_string(self, duration_str: str) -> float:
        """Parse duration string "00:02:35.42" thành seconds"""
        try:
            parts = duration_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
            
        except Exception:
            return 0.0
    
    def fix_metadata(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Fix metadata cho audio file"""
        if not self.ffmpeg_available:
            return {
                "success": False,
                "error": "FFmpeg not available - cannot fix metadata"
            }
        
        if not os.path.exists(input_path):
            return {
                "success": False,
                "error": f"Input file not found: {input_path}"
            }
        
        # Output path default = input + "_fixed"
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_fixed{ext}"
        
        try:
            # Get original duration info
            original_duration = self.get_actual_duration(input_path)
            
            print(f"[TOOL] FIXING METADATA: {os.path.basename(input_path)}")
            print(f"   [STATS] Actual duration: {original_duration:.2f}s" if original_duration else "   [STATS] Duration: Unknown")
            
            # Re-encode với FFmpeg để fix metadata
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:a', 'mp3',           # Re-encode to MP3
                '-b:a', '192k',          # 192kbps bitrate
                '-write_id3v2', '1',     # Write ID3v2 tags
                '-y',                    # Overwrite output
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Verify fixed duration
                fixed_duration = self.get_actual_duration(output_path)
                
                print(f"[OK] METADATA FIXED!")
                print(f"   [FOLDER] Fixed file: {os.path.basename(output_path)}")
                print(f"   ⏱ Duration: {fixed_duration:.2f}s" if fixed_duration else "   ⏱ Duration: Fixed")
                
                # Get file sizes
                original_size = os.path.getsize(input_path)
                fixed_size = os.path.getsize(output_path)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "original_duration": original_duration,
                    "fixed_duration": fixed_duration,
                    "original_size": original_size,
                    "fixed_size": fixed_size
                }
            else:
                return {
                    "success": False,
                    "error": f"FFmpeg failed: {result.stderr}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fixing metadata: {str(e)}"
            }
    
    def fix_all_merged_files(self, directory: str) -> Dict[str, Any]:
        """Fix metadata cho tất cả merged files trong directory"""
        if not os.path.exists(directory):
            return {
                "success": False,
                "error": f"Directory not found: {directory}"
            }
        
        # Find merged files (có pattern đặc biệt)
        merged_patterns = [
            "*merged*.mp3",
            "*complete*.mp3", 
            "*conversation*.mp3",
            "*final*.mp3"
        ]
        
        merged_files = []
        for pattern in merged_patterns:
            merged_files.extend(Path(directory).glob(pattern))
        
        if not merged_files:
            return {
                "success": False,
                "error": "No merged audio files found in directory"
            }
        
        print(f"\n[TOOL] BATCH METADATA FIX")
        print(f"[FOLDER] Directory: {directory}")
        print(f"[MUSIC] Found {len(merged_files)} merged files")
        
        results = []
        success_count = 0
        
        for file_path in merged_files:
            print(f"\n[EDIT] Processing: {file_path.name}")
            
            result = self.fix_metadata(str(file_path))
            results.append({
                "file": file_path.name,
                "result": result
            })
            
            if result["success"]:
                success_count += 1
        
        print(f"\n[SUCCESS] BATCH FIX COMPLETE!")
        print(f"   [OK] Success: {success_count}/{len(merged_files)} files")
        
        return {
            "success": True,
            "total_files": len(merged_files),
            "success_count": success_count,
            "results": results
        }

def main():
    """Test metadata fixer"""
    fixer = AudioMetadataFixer()
    
    if not fixer.ffmpeg_available:
        print("[EMOJI] FFmpeg not available - cannot fix metadata")
        print("[IDEA] Install FFmpeg to use this tool")
        return
    
    # Example usage
    test_dir = "./voice_studio_output"
    if os.path.exists(test_dir):
        result = fixer.fix_all_merged_files(test_dir)
        print(f"\n[CLIPBOARD] Result: {result}")
    else:
        print(f"[FOLDER] Test directory not found: {test_dir}")

if __name__ == '__main__':
    main() 