#!/usr/bin/env python3
"""
🧪 DEMO AUDIO METADATA FIXING
=============================

Demo script để test audio metadata fixing tool.
"""

import sys
import os
import glob
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.audio_metadata_fixer import AudioMetadataFixer

def demo_metadata_analysis():
    """Demo phân tích metadata của existing audio files"""
    print("🧪 DEMO: Audio Metadata Analysis")
    print("=" * 50)
    
    # Find audio files
    audio_dirs = [
        "./voice_studio_output",
        "./test_audio_output",
        "./outputs",
        "./projects/manual_audio_project/audio"
    ]
    
    audio_files = []
    for directory in audio_dirs:
        if os.path.exists(directory):
            files = list(Path(directory).glob("*.mp3")) + list(Path(directory).glob("*.wav"))
            audio_files.extend(files)
    
    if not audio_files:
        print("📁 No audio files found for testing")
        return
    
    print(f"🎵 Found {len(audio_files)} audio files")
    
    fixer = AudioMetadataFixer()
    
    if not fixer.ffmpeg_available:
        print("❌ FFmpeg not available - cannot analyze metadata")
        print("💡 Install FFmpeg to test this feature")
        return
    
    print()
    print("📊 METADATA ANALYSIS:")
    print("-" * 40)
    
    for audio_file in audio_files[:5]:  # Analyze first 5 files
        print(f"\n📝 {audio_file.name}")
        
        # Get actual duration
        duration = fixer.get_actual_duration(str(audio_file))
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            print(f"   ⏱️ Duration: {minutes:02d}:{seconds:02d} ({duration:.2f}s)")
        else:
            print(f"   ⏱️ Duration: Unable to detect")
        
        # Check file size
        size_mb = audio_file.stat().st_size / (1024 * 1024)
        print(f"   📊 Size: {size_mb:.2f} MB")
        
        # Check if it's a potentially merged file
        name_lower = audio_file.name.lower()
        is_merged = any(keyword in name_lower for keyword in [
            'merged', 'complete', 'conversation', 'final', 'force'
        ])
        
        if is_merged:
            print(f"   🔧 Type: Likely merged file - candidate for metadata fixing")
        else:
            print(f"   📄 Type: Regular audio file")

def demo_metadata_fixing():
    """Demo metadata fixing process"""
    print("\n🔧 DEMO: Metadata Fixing Process")
    print("=" * 50)
    
    # Find potentially problematic files
    problem_files = []
    
    # Look for files with "merged", "complete", etc in name
    search_dirs = ["./voice_studio_output", "./test_audio_output"]
    
    for directory in search_dirs:
        if os.path.exists(directory):
            for pattern in ["*merged*.mp3", "*complete*.mp3", "*conversation*.mp3", "*final*.mp3"]:
                files = list(Path(directory).glob(pattern))
                problem_files.extend(files)
    
    if not problem_files:
        print("📁 No potentially problematic merged files found")
        print("💡 This is good! It means you don't have metadata issues")
        return
    
    print(f"🎯 Found {len(problem_files)} potentially problematic files")
    
    fixer = AudioMetadataFixer()
    
    if not fixer.ffmpeg_available:
        print("❌ FFmpeg not available - cannot fix metadata")
        return
    
    # Demo fix process (but don't actually modify files)
    for file_path in problem_files[:3]:  # Process first 3 files
        print(f"\n📝 Analyzing: {file_path.name}")
        
        original_duration = fixer.get_actual_duration(str(file_path))
        
        if original_duration:
            print(f"   📊 Current duration: {original_duration:.2f}s")
            print(f"   🔧 Would fix metadata để ensure correct properties")
            print(f"   ✅ After fixing: Duration would show correctly in media players")
        else:
            print(f"   ❌ Cannot read duration - file may be corrupted")

def main():
    """Main demo function"""
    print("🎭 Voice Studio - Audio Metadata Demo")
    print("=" * 60)
    print()
    
    print("💡 VẤN ĐỀ BẠN GẶP:")
    print("   - File sau khi gộp có nội dung đầy đủ")
    print("   - Nhưng properties/metadata hiển thị duration sai")
    print("   - Đây là vấn đề phổ biến với binary MP3 concatenation")
    print()
    
    print("🔧 GIẢI PHÁP:")
    print("   - Sử dụng FFmpeg để re-encode và fix metadata")
    print("   - Giữ nguyên chất lượng audio")
    print("   - Update duration properties chính xác")
    print()
    
    # Run demos
    demo_metadata_analysis()
    demo_metadata_fixing()
    
    print("\n📋 HƯỚNG DẪN SỬ DỤNG:")
    print("=" * 30)
    print("1. Để fix tất cả merged files:")
    print("   python fix_audio_metadata.py")
    print()
    print("2. Để fix file cụ thể:")
    print("   python fix_audio_metadata.py your_file.mp3")
    print()
    print("3. Voice Studio sẽ tự động fix metadata khi merge files mới")
    print()
    print("🎉 Metadata fixing giải quyết hoàn toàn vấn đề duration properties!")

if __name__ == '__main__':
    main() 