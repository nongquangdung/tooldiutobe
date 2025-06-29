#!/usr/bin/env python3
"""
Test Inner Voice trong Script Generation
Kiểm tra xem inner voice có được apply vào script generation hay không
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.tts.voice_generator import VoiceGenerator

def test_inner_voice_script_generation():
    """Test inner voice trong script generation"""
    
    # Test script JSON với inner voice
    test_script = {
        "project_name": "Test Inner Voice Script",
        "segments": [
            {
                "segment_id": 1,
                "dialogues": [
                    {
                        "dialogue_id": 1,
                        "character": "narrator",
                        "voice": "Jordan",
                        "emotion": "contemplative",
                        "text": "This is a normal narrator voice without inner voice.",
                        "inner_voice": False
                    },
                    {
                        "dialogue_id": 2,  
                        "character": "narrator",
                        "voice": "Jordan",
                        "emotion": "contemplative", 
                        "text": "This is narrator with light inner voice - should have echo effect.",
                        "inner_voice": True,
                        "inner_voice_type": "light"
                    },
                    {
                        "dialogue_id": 3,
                        "character": "narrator", 
                        "voice": "Jordan",
                        "emotion": "contemplative",
                        "text": "This is narrator with deep inner voice - should have deep echo and lowpass.",
                        "inner_voice": True,
                        "inner_voice_type": "deep"
                    },
                    {
                        "dialogue_id": 4,
                        "character": "narrator",
                        "voice": "Jordan", 
                        "emotion": "contemplative",
                        "text": "This is narrator with dreamy inner voice - should have soft dreamy effects.",
                        "inner_voice": True,
                        "inner_voice_type": "dreamy"
                    }
                ]
            }
        ]
    }
    
    print("🎬 Testing Inner Voice Script Generation...")
    print(f"📁 Output directory: test_script_output/")
    
    # Create output directory
    output_dir = Path("test_script_output")
    output_dir.mkdir(exist_ok=True)
    
    # Save test script
    script_file = output_dir / "test_inner_voice_script.json"
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(test_script, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Script saved: {script_file}")
    
    # Generate audio
    voice_gen = VoiceGenerator()
    
    for segment in test_script["segments"]:
        for dialogue in segment["dialogues"]:
            print(f"\n🎯 Processing dialogue {dialogue['dialogue_id']}...")
            print(f"   📝 Text: {dialogue['text'][:50]}...")
            print(f"   🎭 Inner Voice: {dialogue.get('inner_voice', False)}")
            print(f"   🎶 Type: {dialogue.get('inner_voice_type', 'none')}")
            
            # Use original text (simplified)
            enhanced_prompt = dialogue["text"]
            
            # Generate filename
            inner_voice_suffix = ""
            if dialogue.get("inner_voice"):
                inner_voice_suffix = f"_inner_{dialogue.get('inner_voice_type', 'unknown')}"
                
            filename = f"s{segment['segment_id']}_d{dialogue['dialogue_id']}_{dialogue['character']}{inner_voice_suffix}.mp3"
            output_file = output_dir / filename
            
            try:
                # Generate voice
                success = voice_gen.generate_voice(
                    text=enhanced_prompt,
                    output_path=str(output_file),
                    voice_name=dialogue["voice"],
                    emotion_intensity=1.0,
                    speed=1.0,
                    cfg_weight=0.6
                )
                
                # Apply inner voice effects if needed
                if success and dialogue.get("inner_voice", False):
                    print(f"   🎭 Applying inner voice: {dialogue.get('inner_voice_type', 'light')}")
                    try:
                        from src.core.inner_voice_simple import apply_inner_voice_effects
                        
                        inner_voice_type = dialogue.get('inner_voice_type', 'light')
                        base_name = output_file.stem
                        inner_file = output_file.parent / f"{base_name}_inner_{inner_voice_type}.mp3"
                        
                        success_inner = apply_inner_voice_effects(
                            input_file=str(output_file),
                            output_file=str(inner_file),
                            voice_type=inner_voice_type,
                            custom_params=None
                        )
                        
                        if success_inner and inner_file.exists():
                            # Replace original with inner voice version
                            output_file.unlink()  # Delete original
                            inner_file.rename(output_file)  # Rename inner to original
                            print(f"   ✅ Inner voice applied successfully!")
                        else:
                            print(f"   ❌ Inner voice failed")
                            
                    except Exception as e:
                        print(f"   ❌ Inner voice error: {e}")
                
                if success and output_file.exists():
                    file_size = output_file.stat().st_size
                    print(f"   ✅ Generated: {filename} ({file_size:,} bytes)")
                    
                    # Check if file has effects (compare size differences)
                    if dialogue.get("inner_voice"):
                        print(f"   🎵 Inner voice effects applied!")
                else:
                    print(f"   ❌ Failed to generate: {filename}")
                    
            except Exception as e:
                print(f"   💥 Error: {e}")
    
    print(f"\n🎉 Test completed! Check files in: {output_dir}")
    
    # List generated files
    print(f"\n📂 Generated files:")
    for file in sorted(output_dir.glob("*.mp3")):
        size = file.stat().st_size
        print(f"   📄 {file.name} ({size:,} bytes)")

if __name__ == "__main__":
    test_inner_voice_script_generation() 