#!/usr/bin/env python3
"""
🎭 TEST HIGH-QUALITY EMOTION PROMPTS
===================================

Test emotional prompts với high-quality text để preview emotion tốt hơn.
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.emotion_config_tab import AudioPreviewThread

def test_prompt_coverage():
    """Test coverage của emotion prompts"""
    print("🎭 === HIGH-QUALITY EMOTION PROMPTS TEST ===")
    print()
    
    # Get all emotions từ unified system
    from core.unified_emotion_system import UnifiedEmotionSystem
    unified_system = UnifiedEmotionSystem()
    all_emotions = unified_system.get_all_emotions()
    
    print(f"📊 Total emotions in system: {len(all_emotions)}")
    print(f"📝 Available prompts: {len(AudioPreviewThread.EMOTION_PROMPTS)}")
    print()
    
    # Check coverage
    covered_emotions = []
    missing_emotions = []
    
    for emotion_name in all_emotions.keys():
        if emotion_name.lower() in AudioPreviewThread.EMOTION_PROMPTS:
            covered_emotions.append(emotion_name)
        else:
            missing_emotions.append(emotion_name)
    
    print(f"✅ Emotions WITH high-quality prompts ({len(covered_emotions)}):")
    for emotion in sorted(covered_emotions)[:10]:  # Show first 10
        prompt = AudioPreviewThread.EMOTION_PROMPTS[emotion.lower()]
        print(f"   {emotion}: \"{prompt[:60]}...\"")
    if len(covered_emotions) > 10:
        print(f"   ... và {len(covered_emotions) - 10} emotions khác")
    print()
    
    if missing_emotions:
        print(f"⚠️ Emotions WITHOUT high-quality prompts ({len(missing_emotions)}):")
        for emotion in sorted(missing_emotions):
            print(f"   {emotion}: Will use fallback text")
        print()
    
    # Coverage statistics
    coverage_percent = (len(covered_emotions) / len(all_emotions)) * 100
    print(f"📈 Coverage: {coverage_percent:.1f}% ({len(covered_emotions)}/{len(all_emotions)})")
    print()
    
    # Test specific prompts
    test_emotions = ["happy", "sad", "angry", "neutral", "dramatic", "whisper"]
    print("🎯 Testing specific emotion prompts:")
    
    for emotion in test_emotions:
        if emotion in all_emotions:
            prompt = AudioPreviewThread.EMOTION_PROMPTS.get(
                emotion.lower(),
                f"This is a preview of the {emotion} emotion with custom parameters."
            )
            print(f"   {emotion}: \"{prompt}\"")
            print(f"      📏 Length: {len(prompt)} characters")
            print()
    
    return len(covered_emotions), len(missing_emotions)

def demo_prompt_improvements():
    """Demo cải thiện chất lượng prompts"""
    print("🚀 === PROMPT QUALITY IMPROVEMENTS ===")
    print()
    
    # So sánh old vs new
    test_emotions = ["happy", "sad", "angry", "neutral"]
    
    for emotion in test_emotions:
        old_prompt = f"Đây là preview của emotion {emotion}."
        new_prompt = AudioPreviewThread.EMOTION_PROMPTS.get(
            emotion,
            f"This is a preview of the {emotion} emotion with custom parameters."
        )
        
        print(f"🎭 {emotion.upper()}:")
        print(f"   ❌ Old: \"{old_prompt}\"")
        print(f"   ✅ New: \"{new_prompt}\"")
        print(f"   📈 Improvement: {len(new_prompt)} vs {len(old_prompt)} chars "
              f"({len(new_prompt)/len(old_prompt):.1f}x longer)")
        print()
    
    print("💡 Benefits:")
    print("   ✅ More realistic emotional content")
    print("   ✅ Better TTS emotion detection")
    print("   ✅ Clearer parameter differentiation")
    print("   ✅ Professional voice previews")
    print()

def main():
    print("🎭 Voice Studio - High-Quality Emotion Prompts Test")
    print("=" * 60)
    print()
    
    # Test prompt coverage
    covered, missing = test_prompt_coverage()
    
    # Demo improvements
    demo_prompt_improvements()
    
    # Summary
    print("📋 === TEST SUMMARY ===")
    print(f"✅ High-quality prompts: {covered} emotions")
    print(f"⚠️ Fallback prompts: {missing} emotions")
    print(f"🎯 Coverage: {covered/(covered+missing)*100:.1f}%")
    print()
    print("🚀 Ready for Voice Studio UI testing!")
    print("💡 Run: python demo_complete_emotion_features.py")

if __name__ == '__main__':
    main() 