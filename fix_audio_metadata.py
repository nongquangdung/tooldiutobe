#!/usr/bin/env python3
"""
🔧 FIX AUDIO METADATA TOOL
==========================

Tool để fix metadata duration cho merged audio files.
Sử dụng khi file audio đã gộp nhưng duration properties không đúng.

Usage:
  python fix_audio_metadata.py                    # Fix all merged files trong voice_studio_output
  python fix_audio_metadata.py <file_path>        # Fix specific file
  python fix_audio_metadata.py <directory>        # Fix all files trong directory
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.audio_metadata_fixer import AudioMetadataFixer

def main():
    """Main function"""
    print("🔧 Audio Metadata Fixer Tool")
    print("=" * 40)
    
    fixer = AudioMetadataFixer()
    
    if not fixer.ffmpeg_available:
        print("❌ FFmpeg not available!")
        print("💡 Please install FFmpeg để use this tool")
        print("   Windows: Download từ https://ffmpeg.org/download.html")
        print("   Or install với: winget install Gyan.FFmpeg")
        return
    
    # Determine target
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "./voice_studio_output"  # Default directory
    
    print(f"🎯 Target: {target}")
    print()
    
    if os.path.isfile(target):
        # Single file
        print(f"📝 Processing single file: {os.path.basename(target)}")
        result = fixer.fix_metadata(target)
        
        if result["success"]:
            print()
            print("🎉 SUCCESS!")
            print(f"   📁 Original: {os.path.basename(target)}")
            print(f"   📁 Fixed: {os.path.basename(result['output_path'])}")
            if result.get("original_duration") and result.get("fixed_duration"):
                print(f"   ⏱️ Duration: {result['original_duration']:.1f}s → {result['fixed_duration']:.1f}s")
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            
    elif os.path.isdir(target):
        # Directory
        print(f"📁 Processing directory: {target}")
        result = fixer.fix_all_merged_files(target)
        
        if result["success"]:
            print()
            print("🎉 BATCH PROCESSING COMPLETE!")
            print(f"   📊 Total files: {result['total_files']}")
            print(f"   ✅ Success: {result['success_count']}")
            print(f"   ❌ Failed: {result['total_files'] - result['success_count']}")
            
            # Show details
            print()
            print("📋 Details:")
            for item in result["results"]:
                status = "✅" if item["result"]["success"] else "❌"
                print(f"   {status} {item['file']}")
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Target not found: {target}")
        print()
        print("💡 Usage examples:")
        print("   python fix_audio_metadata.py                                    # Fix all trong voice_studio_output")
        print("   python fix_audio_metadata.py merged_audio.mp3                   # Fix specific file")
        print("   python fix_audio_metadata.py ./my_audio_folder                  # Fix all trong folder")

def test_demo():
    """Demo function để test tool"""
    print("\n🧪 DEMO MODE - Testing metadata fixer")
    print("=" * 50)
    
    # Test với voice_studio_output nếu có
    test_dirs = [
        "./voice_studio_output",
        "./test_audio_output", 
        "./outputs"
    ]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            print(f"🎯 Found test directory: {test_dir}")
            
            fixer = AudioMetadataFixer()
            result = fixer.fix_all_merged_files(test_dir)
            
            print(f"📋 Result: {result}")
            return
    
    print("📁 No test directories found")
    print("💡 Create some merged audio files first!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        test_demo()
    else:
        main() 