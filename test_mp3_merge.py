#!/usr/bin/env python3
"""
Test script để merge MP3 files với proper duration
"""
import os
import glob

def merge_mp3_files_with_proper_headers(output_dir):
    """Merge MP3 files với proper header handling"""
    
    # Find all segment files
    pattern = os.path.join(output_dir, "segment_*.mp3")
    files = glob.glob(pattern)
    
    if not files:
        print(f"❌ No segment files found in {output_dir}")
        return None
        
    # Sort files properly
    def extract_numbers(filename):
        import re
        basename = os.path.basename(filename)
        match = re.search(r'segment_(\d+)_dialogue_(\d+)', basename)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (0, 0)
    
    sorted_files = sorted(files, key=extract_numbers)
    
    print(f"🎵 Found {len(sorted_files)} MP3 files to merge:")
    for i, file in enumerate(sorted_files[:5]):
        print(f"   {i+1}. {os.path.basename(file)}")
    if len(sorted_files) > 5:
        print(f"   ... and {len(sorted_files) - 5} more")
    
    # Output file
    output_path = os.path.join(output_dir, "test_proper_merge.mp3")
    
    print(f"\n🔧 Merging using MP3 frame-level concatenation...")
    
    try:
        with open(output_path, 'wb') as outfile:
            first_file = True
            
            for file_path in sorted_files:
                if os.path.exists(file_path):
                    print(f"   📎 Processing: {os.path.basename(file_path)}")
                    
                    with open(file_path, 'rb') as infile:
                        data = infile.read()
                        
                        if first_file:
                            # Keep full first file including headers
                            outfile.write(data)
                            first_file = False
                            print(f"      ✅ Wrote full file with headers ({len(data)} bytes)")
                        else:
                            # Skip ID3 headers for subsequent files
                            # Find MP3 sync frame (0xFF 0xFB or 0xFF 0xFA)
                            sync_pos = 0
                            for i in range(min(1024, len(data) - 1)):
                                if data[i] == 0xFF and data[i+1] in [0xFB, 0xFA, 0xF3, 0xF2]:
                                    sync_pos = i
                                    break
                            
                            # Write from sync frame onwards
                            audio_data = data[sync_pos:]
                            outfile.write(audio_data)
                            print(f"      ✅ Wrote audio data only ({len(audio_data)} bytes, skipped {sync_pos} header bytes)")
        
        print(f"\n✅ MP3 FRAME MERGE SUCCESS!")
        print(f"📁 Output: {output_path}")
        
        # Check file size
        file_size = os.path.getsize(output_path)
        print(f"📏 File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error during merge: {e}")
        return None

if __name__ == "__main__":
    output_dir = "./voice_studio_output"
    result = merge_mp3_files_with_proper_headers(output_dir)
    
    if result:
        print(f"\n🎯 Test completed! Check the merged file:")
        print(f"   {result}")
        print(f"\n💡 Compare duration with the original problematic file:")
        print(f"   {os.path.join(output_dir, 'complete_merged_audio.mp3')}")
    else:
        print("❌ Test failed!") 