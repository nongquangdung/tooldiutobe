#!/usr/bin/env python3
"""
🎯 VOICE GENERATION COMPLETE TEST
===============================

Test toàn bộ voice generation workflow với real data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_complete_voice_workflow():
    """Test complete voice generation workflow"""
    print("🎯 TESTING COMPLETE VOICE GENERATION WORKFLOW")
    print("=" * 60)
    
    try:
        from src.tts.real_chatterbox_provider import RealChatterboxProvider  
        from src.core.unified_emotion_system import unified_emotion_system
        
        provider = RealChatterboxProvider()
        
        # Test cases từ original log
        test_cases = [
            {
                "character": "narrator",
                "voice": "jeremiah", 
                "emotion": "dramatic",
                "text": "As the last train passed by, Lan stood at the edge..."
            },
            {
                "character": "character1", 
                "voice": "cora",
                "emotion": "sad", 
                "text": "Every time I come here, I think of that day..."
            },
            {
                "character": "character2",
                "voice": "eli",
                "emotion": "serious",
                "text": "Lan, I didn't forget. I couldn't come back..."
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n🎬 Test Case {i}: {case['character']}")
            print(f"   🎙️ Voice: {case['voice']}")
            print(f"   🎭 Emotion: {case['emotion']}")
            print(f"   📝 Text: {case['text'][:40]}...")
            
            # Test emotion parameters
            emotion_params = unified_emotion_system.get_emotion_parameters(case['emotion'])
            if emotion_params:
                print(f"   ✅ Emotion found: exaggeration={emotion_params.get('exaggeration', 1.0)}, cfg_weight={emotion_params.get('cfg_weight', 0.6)}")
            else:
                print(f"   ⚠️ Emotion '{case['emotion']}' not found")
            
            # Test voice resolution  
            resolved_voice = provider._resolve_voice_selection(case['voice'])
            expected_voice = case['voice']
            actual_voice = resolved_voice['id']
            
            if actual_voice == expected_voice:
                print(f"   ✅ Voice assignment correct: {expected_voice} → {resolved_voice['name']}")
            else:
                print(f"   ❌ Voice assignment WRONG: expected {expected_voice}, got {actual_voice}")
            
            # Test file path
            if 'file_path' in resolved_voice:
                file_path = resolved_voice['file_path']
                if os.path.exists(file_path):
                    print(f"   ✅ Voice file exists: {file_path}")
                else:
                    print(f"   ❌ Voice file missing: {file_path}")
            
            # Simulate generation (without actual audio)
            print(f"   🎵 Would generate audio with:")
            print(f"      - Voice: {resolved_voice['name']} ({resolved_voice['gender']})")
            print(f"      - Emotion: {case['emotion']} ({emotion_params})")
            
        print("\n" + "=" * 60)
        print("✅ Complete voice workflow test finished!")
        
    except Exception as e:
        print(f"❌ Complete workflow test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_voice_workflow() 