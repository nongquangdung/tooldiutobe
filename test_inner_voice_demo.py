#!/usr/bin/env python3
"""
🎭 TEST INNER VOICE DEMO
========================

Test script để demo Inner Voice feature với các echo effects khác nhau.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_inner_voice_processor():
    """Test Inner Voice Processor standalone"""
    print("🎭 === INNER VOICE PROCESSOR TEST ===")
    print("=" * 50)
    
    try:
        from core.inner_voice_processor import InnerVoiceProcessor
        
        processor = InnerVoiceProcessor()
        
        if not processor.ffmpeg_available:
            print("❌ FFmpeg not available")
            print("💡 Please install FFmpeg to test Inner Voice effects")
            return False
        
        print("✅ InnerVoiceProcessor initialized successfully")
        
        # Show available types
        types = processor.get_available_types()
        print(f"\n📋 Available Inner Voice Types: {len(types)}")
        
        for type_id, info in types.items():
            print(f"\n🎪 {type_id.upper()}:")
            print(f"   📝 Name: {info['name']}")
            print(f"   📖 Description: {info['description']}")
            print(f"   🎛️ Filter: {info['filter']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import InnerVoiceProcessor: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing InnerVoiceProcessor: {e}")
        return False

def test_voice_generator_integration():
    """Test Voice Generator với Inner Voice integration"""
    print("\n🎙️ === VOICE GENERATOR INTEGRATION TEST ===")
    print("=" * 55)
    
    try:
        from tts.voice_generator import VoiceGenerator
        
        generator = VoiceGenerator()
        
        if generator.inner_voice_processor:
            print("✅ VoiceGenerator with Inner Voice Processor initialized")
            
            # Test với demo JSON
            demo_file = "voice_studio_inner_voice_demo.json"
            if os.path.exists(demo_file):
                print(f"📁 Found demo file: {demo_file}")
                
                with open(demo_file, 'r', encoding='utf-8') as f:
                    demo_data = json.load(f)
                
                # Analyze demo data
                total_dialogues = 0
                inner_voice_dialogues = 0
                
                for segment in demo_data.get('segments', []):
                    for dialogue in segment.get('dialogues', []):
                        total_dialogues += 1
                        if dialogue.get('inner_voice', False):
                            inner_voice_dialogues += 1
                
                print(f"📊 Demo Data Analysis:")
                print(f"   📝 Total dialogues: {total_dialogues}")
                print(f"   🎭 Inner voice dialogues: {inner_voice_dialogues}")
                print(f"   📈 Inner voice ratio: {inner_voice_dialogues/total_dialogues*100:.1f}%")
                
                # Show inner voice types usage
                inner_voice_types = {}
                for segment in demo_data.get('segments', []):
                    for dialogue in segment.get('dialogues', []):
                        if dialogue.get('inner_voice', False):
                            iv_type = dialogue.get('inner_voice_type', 'auto')
                            inner_voice_types[iv_type] = inner_voice_types.get(iv_type, 0) + 1
                
                print(f"\n🎪 Inner Voice Types Usage:")
                for iv_type, count in inner_voice_types.items():
                    print(f"   {iv_type}: {count} dialogues")
                
            else:
                print(f"⚠️ Demo file not found: {demo_file}")
                print("💡 Creating demo JSON...")
                
        else:
            print("⚠️ VoiceGenerator initialized but Inner Voice Processor not available")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import VoiceGenerator: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing VoiceGenerator: {e}")
        return False

def test_audio_processing():
    """Test actual audio processing với inner voice"""
    print("\n🎵 === AUDIO PROCESSING TEST ===")
    print("=" * 40)
    
    # Find test audio files
    test_files = [
        "./test_audio_output/emotion_preview_neutral.wav",
        "./test_audio_output/emotion_preview_contemplative.wav",
        "./test_audio_output/emotion_preview_soft.wav"
    ]
    
    found_files = [f for f in test_files if os.path.exists(f)]
    
    if not found_files:
        print("📁 No test audio files found")
        print("💡 Generate some emotion previews first to test inner voice processing")
        return False
    
    try:
        from core.inner_voice_processor import InnerVoiceProcessor, InnerVoiceType
        
        processor = InnerVoiceProcessor()
        
        if not processor.ffmpeg_available:
            print("❌ FFmpeg not available - cannot test audio processing")
            return False
        
        print(f"📁 Found {len(found_files)} test audio files")
        
        # Test với từng file
        for test_file in found_files[:1]:  # Chỉ test 1 file để tiết kiệm thời gian
            print(f"\n🧪 Testing với: {os.path.basename(test_file)}")
            
            for inner_type in InnerVoiceType:
                output_file = f"./test_inner_voice_{inner_type.value}_{os.path.basename(test_file).replace('.wav', '.mp3')}"
                
                print(f"   🎭 Processing {inner_type.value}...")
                result = processor.process_inner_voice(test_file, output_file, inner_type)
                
                if result["success"]:
                    print(f"   ✅ {inner_type.value}: {result['preset_name']}")
                    print(f"      📁 Output: {os.path.basename(result['output_path'])}")
                    print(f"      📊 Size: {result['original_size']} → {result['processed_size']} bytes")
                else:
                    print(f"   ❌ {inner_type.value}: {result.get('error', 'Unknown error')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import InnerVoiceProcessor: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in audio processing test: {e}")
        return False

def test_json_schema_validation():
    """Test JSON schema với inner voice fields"""
    print("\n📋 === JSON SCHEMA VALIDATION ===")
    print("=" * 40)
    
    demo_file = "voice_studio_inner_voice_demo.json"
    if not os.path.exists(demo_file):
        print(f"⚠️ Demo file not found: {demo_file}")
        return False
    
    try:
        with open(demo_file, 'r', encoding='utf-8') as f:
            demo_data = json.load(f)
        
        print("✅ JSON file loaded successfully")
        
        # Validate structure
        required_keys = ['title', 'characters', 'segments', 'voice_mapping']
        missing_keys = [key for key in required_keys if key not in demo_data]
        
        if missing_keys:
            print(f"❌ Missing required keys: {missing_keys}")
            return False
        
        print("✅ Basic structure validation passed")
        
        # Validate inner voice fields
        inner_voice_count = 0
        invalid_inner_voice = []
        
        for segment_idx, segment in enumerate(demo_data.get('segments', [])):
            for dialogue_idx, dialogue in enumerate(segment.get('dialogues', [])):
                if dialogue.get('inner_voice', False):
                    inner_voice_count += 1
                    
                    # Validate inner_voice_type if specified
                    iv_type = dialogue.get('inner_voice_type')
                    if iv_type and iv_type not in ['light', 'deep', 'dreamy']:
                        invalid_inner_voice.append({
                            'segment': segment_idx + 1,
                            'dialogue': dialogue_idx + 1,
                            'invalid_type': iv_type
                        })
        
        print(f"📊 Inner Voice Validation:")
        print(f"   🎭 Total inner voice dialogues: {inner_voice_count}")
        
        if invalid_inner_voice:
            print(f"   ❌ Invalid inner voice types found: {len(invalid_inner_voice)}")
            for invalid in invalid_inner_voice:
                print(f"      Segment {invalid['segment']}, Dialogue {invalid['dialogue']}: {invalid['invalid_type']}")
            return False
        else:
            print(f"   ✅ All inner voice types are valid")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in JSON validation: {e}")
        return False

def main():
    """Main test function"""
    print("🎭 INNER VOICE FEATURE - COMPREHENSIVE TEST")
    print("=" * 60)
    print()
    
    test_results = []
    
    # 1. Test Inner Voice Processor
    result1 = test_inner_voice_processor()
    test_results.append(("InnerVoiceProcessor", result1))
    
    # 2. Test Voice Generator Integration
    result2 = test_voice_generator_integration()
    test_results.append(("VoiceGenerator Integration", result2))
    
    # 3. Test JSON Schema
    result3 = test_json_schema_validation()
    test_results.append(("JSON Schema Validation", result3))
    
    # 4. Test Audio Processing (optional)
    result4 = test_audio_processing()
    test_results.append(("Audio Processing", result4))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Inner Voice feature is ready to use!")
        print("\n💡 Usage:")
        print("   1. Add 'inner_voice': true to dialogue in JSON")
        print("   2. Optionally specify 'inner_voice_type': 'light'/'deep'/'dreamy'")
        print("   3. Run voice generation - inner voice will be applied automatically")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")

if __name__ == '__main__':
    main() 