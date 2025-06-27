#!/usr/bin/env python3
"""
🎭 REAL INNER VOICE TEST
========================

Test thực tế inner voice feature với Voice Studio app.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_inner_voice_generation():
    """Demo tạo audio với inner voice effects"""
    print("🎭 === REAL INNER VOICE GENERATION TEST ===")
    print("=" * 55)
    
    try:
        from tts.voice_generator import VoiceGenerator
        
        generator = VoiceGenerator()
        print("✅ VoiceGenerator initialized")
        
        # Demo data ngắn gọn
        demo_data = {
            "segments": [
                {
                    "dialogues": [
                        {
                            "speaker": "alice",
                            "text": "Hôm nay trời đẹp quá.",
                            "emotion": "happy"
                        },
                        {
                            "speaker": "alice", 
                            "text": "Mình có nên ra ngoài chơi không nhỉ?",
                            "emotion": "contemplative",
                            "inner_voice": True,
                            "inner_voice_type": "light"
                        },
                        {
                            "speaker": "alice",
                            "text": "Làm việc từ sáng đến giờ, giờ cần thời gian nghỉ ngơi rồi.",
                            "emotion": "thoughtful", 
                            "inner_voice": True,
                            "inner_voice_type": "deep"
                        }
                    ]
                }
            ],
            "characters": [
                {"id": "alice", "name": "Alice"}
            ]
        }
        
        voice_mapping = {"alice": "vi-VN-Standard-C"}
        output_dir = "./test_inner_voice_output"
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"📁 Output directory: {output_dir}")
        print(f"🎭 Testing {len(demo_data['segments'][0]['dialogues'])} dialogues...")
        
        # Test generation
        result = generator.generate_audio_by_characters(demo_data, output_dir, voice_mapping)
        
        if result["success"]:
            print("✅ INNER VOICE GENERATION SUCCESS!")
            print(f"   📁 Final audio: {os.path.basename(result['final_audio_path'])}")
            
            # List generated files
            if os.path.exists(output_dir):
                files = list(Path(output_dir).glob("*.mp3"))
                print(f"\n📋 Generated files: {len(files)}")
                for file in files:
                    size = file.stat().st_size
                    is_inner = "_inner_" in file.name
                    indicator = "🎭" if is_inner else "🎤"
                    print(f"   {indicator} {file.name} ({size:,} bytes)")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in real test: {e}")
        return False

def test_standalone_inner_voice():
    """Test standalone inner voice processor"""
    print("\n🎛️ === STANDALONE INNER VOICE TEST ===")
    print("=" * 45)
    
    try:
        from core.inner_voice_processor import InnerVoiceProcessor
        
        processor = InnerVoiceProcessor()
        
        # Find test file
        test_file = "./test_audio_output/emotion_preview_happy.wav"
        if not os.path.exists(test_file):
            print(f"⚠️ Test file not found: {test_file}")
            return False
        
        output_file = "./test_standalone_inner_voice.mp3"
        
        # Test dialogue data
        dialogue_data = {
            "speaker": "alice",
            "emotion": "contemplative", 
            "inner_voice": True,
            "inner_voice_type": "light"
        }
        
        print(f"🧪 Processing: {os.path.basename(test_file)}")
        result = processor.process_dialogue_with_inner_voice(
            test_file, dialogue_data, "./test_inner_voice_output"
        )
        
        if result["success"]:
            print("✅ STANDALONE PROCESSING SUCCESS!")
            if result.get("inner_voice_applied", False):
                print(f"   🎭 Inner voice applied: {result.get('preset_name', 'Unknown')}")
                print(f"   📁 Output: {os.path.basename(result['output_path'])}")
            else:
                print("   📝 No inner voice applied (flag was false)")
        else:
            print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in standalone test: {e}")
        return False

def demo_json_with_inner_voice():
    """Demo với complete JSON có inner voice"""
    print("\n📋 === COMPLETE JSON DEMO ===")
    print("=" * 35)
    
    json_file = "voice_studio_inner_voice_demo.json"
    if not os.path.exists(json_file):
        print(f"⚠️ Demo JSON not found: {json_file}")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded JSON: {data['title']}")
        
        # Analyze inner voice usage
        inner_voice_stats = {
            "light": 0,
            "deep": 0, 
            "dreamy": 0,
            "auto": 0
        }
        
        total_dialogues = 0
        inner_voice_dialogues = 0
        
        for segment in data.get('segments', []):
            for dialogue in segment.get('dialogues', []):
                total_dialogues += 1
                if dialogue.get('inner_voice', False):
                    inner_voice_dialogues += 1
                    iv_type = dialogue.get('inner_voice_type', 'auto')
                    inner_voice_stats[iv_type] = inner_voice_stats.get(iv_type, 0) + 1
        
        print(f"\n📊 Inner Voice Analysis:")
        print(f"   📝 Total dialogues: {total_dialogues}")
        print(f"   🎭 Inner voice dialogues: {inner_voice_dialogues}")
        print(f"   📈 Coverage: {inner_voice_dialogues/total_dialogues*100:.1f}%")
        
        print(f"\n🎪 Type Distribution:")
        for iv_type, count in inner_voice_stats.items():
            if count > 0:
                print(f"   {iv_type}: {count} dialogues")
        
        # Show example dialogues
        print(f"\n💭 Example Inner Voice Dialogues:")
        count = 0
        for segment in data.get('segments', []):
            for dialogue in segment.get('dialogues', []):
                if dialogue.get('inner_voice', False) and count < 3:
                    count += 1
                    speaker = dialogue['speaker']
                    text = dialogue['text'][:50] + "..." if len(dialogue['text']) > 50 else dialogue['text']
                    iv_type = dialogue.get('inner_voice_type', 'auto')
                    emotion = dialogue.get('emotion', 'neutral')
                    
                    print(f"   {count}. {speaker} ({emotion}, {iv_type}): \"{text}\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing JSON: {e}")
        return False

def main():
    """Main demo function"""
    print("🎭 INNER VOICE FEATURE - REAL WORLD TEST")
    print("=" * 50)
    print()
    
    results = []
    
    # 1. Demo JSON Analysis
    result1 = demo_json_with_inner_voice()
    results.append(("JSON Analysis", result1))
    
    # 2. Standalone processor test
    result2 = test_standalone_inner_voice()
    results.append(("Standalone Processor", result2))
    
    # 3. Real generation test
    result3 = demo_inner_voice_generation()
    results.append(("Real Generation", result3))
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 REAL WORLD TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n📈 Success Rate: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 INNER VOICE FEATURE IS PRODUCTION READY!")
        print("\n📋 How to use:")
        print('   1. Add "inner_voice": true to any dialogue in JSON')
        print('   2. Optionally add "inner_voice_type": "light|deep|dreamy"')
        print('   3. Generate audio - inner voice will be applied automatically')
        print('   4. Files with inner voice will have "_inner_light" etc. suffix')
    else:
        print(f"\n⚠️ Some issues found. Please review the failed tests above.")

if __name__ == '__main__':
    main() 