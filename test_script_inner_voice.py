#!/usr/bin/env python3
"""
Test Script Generation với Inner Voice - SIMPLE VERSION
"""

import sys
import os
import json
sys.path.insert(0, os.path.abspath('.'))

def test_script_generation():
    """Test voice generation với inner voice trong scripts"""
    print("🎬 TESTING SCRIPT GENERATION WITH INNER VOICE")
    print("=" * 55)
    
    try:
        from src.tts.voice_generator import VoiceGenerator
        
        # Create generator
        generator = VoiceGenerator()
        print("✅ VoiceGenerator created")
        
        # Demo script data với inner voice
        script_data = {
            "segments": [
                {
                    "dialogues": [
                        {
                            "speaker": "narrator",
                            "text": "Hôm nay trời đẹp quá.",
                            "emotion": "happy"
                        },
                        {
                            "speaker": "narrator", 
                            "text": "Mình có nên ra ngoài chơi không nhỉ?",
                            "emotion": "contemplative",
                            "inner_voice": True,
                            "inner_voice_type": "light"
                        },
                        {
                            "speaker": "narrator",
                            "text": "Nhớ lại hôm qua mình làm việc từ sáng đến tối...",
                            "emotion": "thoughtful",
                            "inner_voice": True,
                            "inner_voice_type": "deep"
                        },
                        {
                            "speaker": "narrator",
                            "text": "Giá như mình có thể bay đi khắp nơi...",
                            "emotion": "dreamy",
                            "inner_voice": True,
                            "inner_voice_type": "dreamy"
                        }
                    ]
                }
            ],
            "characters": [
                {
                    "id": "narrator",
                    "name": "Narrator",
                    "gender": "female"
                }
            ]
        }
        
        voice_mapping = {"narrator": "Abigail"}
        output_dir = "./test_script_output"
        
        # Ensure output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"📁 Output directory: {output_dir}")
        print(f"🎭 Testing {len(script_data['segments'][0]['dialogues'])} dialogues...")
        print("   - 1 normal dialogue")
        print("   - 3 inner voice dialogues (light, deep, dreamy)")
        
        # Generate audio
        result = generator.generate_audio_by_characters(script_data, output_dir, voice_mapping)
        
        if result["success"]:
            print("\n✅ SCRIPT GENERATION SUCCESS!")
            print(f"   📁 Final audio: {os.path.basename(result['final_audio_path'])}")
            
            # Check generated files
            import glob
            audio_files = glob.glob(os.path.join(output_dir, "*.mp3"))
            print(f"\n📋 Generated files: {len(audio_files)}")
            
            inner_voice_files = 0
            normal_files = 0
            
            for file_path in audio_files:
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                
                if "_inner_" in filename:
                    inner_voice_files += 1
                    # Extract inner voice type
                    if "_inner_light" in filename:
                        iv_type = "light"
                    elif "_inner_deep" in filename:
                        iv_type = "deep"
                    elif "_inner_dreamy" in filename:
                        iv_type = "dreamy"
                    else:
                        iv_type = "unknown"
                    print(f"   🎭 {filename} ({size:,} bytes) - Inner Voice: {iv_type}")
                else:
                    if filename != os.path.basename(result['final_audio_path']):
                        normal_files += 1
                        print(f"   🎤 {filename} ({size:,} bytes) - Normal")
            
            print(f"\n📊 File Analysis:")
            print(f"   🎤 Normal dialogues: {normal_files}")
            print(f"   🎭 Inner voice dialogues: {inner_voice_files}")
            
            # Expected: 1 normal + 3 inner voice = 4 individual files + 1 final
            expected_individual = 4
            actual_individual = normal_files + inner_voice_files
            
            if actual_individual == expected_individual:
                print(f"   ✅ Expected {expected_individual} files, got {actual_individual}")
                
                if inner_voice_files == 3:
                    print("   ✅ All 3 inner voice effects applied successfully!")
                    return True
                else:
                    print(f"   ⚠️ Expected 3 inner voice files, got {inner_voice_files}")
            else:
                print(f"   ⚠️ Expected {expected_individual} individual files, got {actual_individual}")
                
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

if __name__ == "__main__":
    success = test_script_generation()
    if success:
        print("\n🎉 INNER VOICE SCRIPT GENERATION SUCCESS!")
        print("✅ Tính năng Inner Voice hoạt động hoàn hảo trong script generation")
    else:
        print("\n❌ Inner voice script generation có vấn đề") 