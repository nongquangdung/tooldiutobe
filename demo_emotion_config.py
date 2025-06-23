#!/usr/bin/env python3
"""
🎭 DEMO EMOTION CONFIGURATION SYSTEM
====================================

Demo script để test emotion configuration manager và UI.
Hiển thị khả năng điều chỉnh và lưu cấu hình cảm xúc.

Features được test:
- Load default emotions (25+ emotions)
- Tạo custom emotions
- Modify emotion parameters
- Create emotion presets
- Export/import configurations
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.emotion_config_manager import EmotionConfigManager, EmotionParameters
import json
from pathlib import Path

def demo_emotion_manager():
    """Demo emotion configuration manager"""
    print("🎭 === EMOTION CONFIGURATION MANAGER DEMO ===\n")
    
    # Initialize manager
    manager = EmotionConfigManager()
    
    # 1. Show default emotions
    print("📋 DEFAULT EMOTIONS:")
    default_emotions = manager.default_emotions
    print(f"   Total: {len(default_emotions)} emotions")
    
    for name, emotion in list(default_emotions.items())[:5]:  # Show first 5
        print(f"   🎭 {name}: exag={emotion.exaggeration:.2f}, cfg={emotion.cfg_weight:.2f}, "
              f"temp={emotion.temperature:.2f}, speed={emotion.speed:.2f}")
    
    print(f"   ... and {len(default_emotions)-5} more emotions\n")
    
    # 2. Show emotions by category
    print("🏷️ EMOTIONS BY CATEGORY:")
    categories = manager.get_emotion_categories()
    for category in categories:
        emotions = manager.get_emotions_by_category(category)
        print(f"   {category.title()}: {len(emotions)} emotions")
        
        # Show examples
        for name in list(emotions.keys())[:2]:  # Show 2 examples
            emotion = emotions[name]
            print(f"     • {name}: {emotion.description}")
    print()
    
    # 3. Create custom emotion
    print("✨ CREATING CUSTOM EMOTIONS:")
    
    custom_emotions = [
        {
            "name": "epic_battle",
            "exaggeration": 2.3,
            "cfg_weight": 0.8,
            "temperature": 1.2,
            "speed": 1.4,
            "description": "Epic battle scene with intense drama",
            "category": "dramatic",
            "voice_tone": "intense"
        },
        {
            "name": "gentle_lullaby",
            "exaggeration": 0.2,
            "cfg_weight": 0.2,
            "temperature": 0.3,
            "speed": 0.6,
            "description": "Soft lullaby for peaceful sleep",
            "category": "special",
            "voice_tone": "soft"
        },
        {
            "name": "corporate_presentation",
            "exaggeration": 0.7,
            "cfg_weight": 0.6,
            "temperature": 0.6,
            "speed": 1.0,
            "description": "Professional corporate presentation",
            "category": "neutral",
            "voice_tone": "balanced"
        }
    ]
    
    for custom in custom_emotions:
        emotion = manager.create_custom_emotion(**custom)
        print(f"   ✅ Created: {emotion.name}")
        print(f"      Parameters: exag={emotion.exaggeration:.2f}, cfg={emotion.cfg_weight:.2f}")
        print(f"      Category: {emotion.category}, Voice Tone: {emotion.voice_tone}")
    print()
    
    # 4. Modify existing emotion
    print("🔧 MODIFYING EMOTIONS:")
    
    # Modify happy emotion to be more intense
    original_happy = manager.get_all_emotions()["happy"]
    print(f"   Original 'happy': exag={original_happy.exaggeration:.2f}")
    
    modified_happy = manager.modify_emotion(
        "happy",
        exaggeration=1.8,  # More intense
        speed=1.3,         # Faster
        description="Super enthusiastic happiness"
    )
    
    if modified_happy:
        print(f"   Modified 'happy': exag={modified_happy.exaggeration:.2f}, speed={modified_happy.speed:.2f}")
    print()
    
    # 5. Get emotion parameters for TTS
    print("🎙️ TTS PARAMETERS:")
    
    test_emotions = ["neutral", "epic_battle", "gentle_lullaby", "happy"]
    for emotion_name in test_emotions:
        params = manager.get_emotion_parameters(emotion_name)
        print(f"   {emotion_name}:")
        print(f"     exaggeration: {params['exaggeration']:.2f}")
        print(f"     cfg_weight: {params['cfg_weight']:.2f}")
        print(f"     temperature: {params['temperature']:.2f}")
        print(f"     speed: {params['speed']:.2f}")
    print()
    
    # 6. Create emotion preset
    print("📋 CREATING EMOTION PRESET:")
    
    preset_emotions = ["neutral", "happy", "sad", "dramatic", "epic_battle"]
    preset = manager.create_emotion_preset(
        preset_name="story_narration",
        emotions=preset_emotions,
        description="Optimal emotions for story narration"
    )
    
    print(f"   ✅ Created preset: {preset.name}")
    print(f"      Emotions: {len(preset.emotions)}")
    print(f"      Description: {preset.description}")
    print()
    
    # 7. Statistics
    print("📊 EMOTION STATISTICS:")
    stats = manager.get_emotion_statistics()
    
    print(f"   Total Emotions: {stats['total_emotions']}")
    print(f"   Default: {stats['default_emotions']}")
    print(f"   Custom: {stats['custom_emotions']}")
    print(f"   Presets: {stats['total_presets']}")
    
    print("\n   Category Distribution:")
    for category, count in stats['categories'].items():
        print(f"     {category.title()}: {count}")
    
    print("\n   Voice Tone Distribution:")
    for tone, count in stats['voice_tones'].items():
        print(f"     {tone.title()}: {count}")
    print()
    
    # 8. Export configuration
    print("💾 EXPORTING CONFIGURATION:")
    
    export_path = "demo_emotion_export.json"
    manager.export_emotion_config(export_path)
    
    if os.path.exists(export_path):
        file_size = os.path.getsize(export_path)
        print(f"   ✅ Exported to: {export_path}")
        print(f"      File size: {file_size} bytes")
        
        # Show preview of exported data
        with open(export_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"      Default emotions: {len(data['default_emotions'])}")
        print(f"      Custom emotions: {len(data['custom_emotions'])}")
        print(f"      Presets: {len(data['emotion_presets'])}")
    print()
    
    return manager

def demo_emotion_usage_scenarios():
    """Demo các scenario sử dụng emotion configurations"""
    print("🎬 === EMOTION USAGE SCENARIOS ===\n")
    
    manager = EmotionConfigManager()
    
    # Scenario 1: Audio book narration
    print("📚 SCENARIO 1: AUDIOBOOK NARRATION")
    audiobook_emotions = ["neutral", "contemplative", "gentle", "dramatic", "mysterious"]
    
    print("   Optimal emotions for audiobook:")
    for emotion_name in audiobook_emotions:
        params = manager.get_emotion_parameters(emotion_name)
        emotion = manager.get_all_emotions()[emotion_name]
        print(f"     🎭 {emotion_name}: {emotion.description}")
        print(f"        → exag={params['exaggeration']:.2f}, speed={params['speed']:.2f}")
    print()
    
    # Scenario 2: Character dialogue
    print("🎭 SCENARIO 2: CHARACTER DIALOGUE")
    
    characters = {
        "hero": ["confident", "friendly", "determined"],
        "villain": ["angry", "sarcastic", "cold"],
        "narrator": ["neutral", "mysterious", "dramatic"],
        "child": ["excited", "happy", "innocent"]
    }
    
    for character, emotions in characters.items():
        print(f"   {character.title()} character emotions:")
        for emotion_name in emotions:
            if emotion_name in manager.get_all_emotions():
                params = manager.get_emotion_parameters(emotion_name)
                print(f"     • {emotion_name}: exag={params['exaggeration']:.2f}")
            else:
                print(f"     • {emotion_name}: (not available)")
    print()
    
    # Scenario 3: Commercial/advertisement
    print("📺 SCENARIO 3: COMMERCIAL/ADVERTISEMENT")
    commercial_emotions = ["friendly", "excited", "persuasive", "confident"]
    
    print("   Commercial voice emotions:")
    for emotion_name in commercial_emotions:
        if emotion_name in manager.get_all_emotions():
            params = manager.get_emotion_parameters(emotion_name)
            emotion = manager.get_all_emotions()[emotion_name]
            print(f"     🎙️ {emotion_name}: {emotion.description}")
            print(f"        → cfg={params['cfg_weight']:.2f}, temp={params['temperature']:.2f}")
        else:
            print(f"     🎙️ {emotion_name}: (custom emotion needed)")
    print()

def demo_emotion_table_format():
    """Demo format bảng emotion parameters"""
    print("📊 === EMOTION PARAMETERS TABLE ===\n")
    
    manager = EmotionConfigManager()
    all_emotions = manager.get_all_emotions()
    
    # Table header
    print("| Emotion | Exaggeration | CFG Weight | Temperature | Speed | Category | Voice Tone | Description |")
    print("|---------|-------------|------------|-------------|-------|----------|------------|-------------|")
    
    # Show emotions by category
    categories = ["neutral", "positive", "negative", "dramatic", "special"]
    
    for category in categories:
        category_emotions = manager.get_emotions_by_category(category)
        if category_emotions:
            print(f"| **{category.upper()}** | | | | | | | |")
            
            for emotion_name, emotion in category_emotions.items():
                print(f"| {emotion_name} | {emotion.exaggeration:.2f} | {emotion.cfg_weight:.2f} | "
                      f"{emotion.temperature:.2f} | {emotion.speed:.2f} | {emotion.category} | "
                      f"{emotion.voice_tone} | {emotion.description[:30]}... |")
    
    print(f"\n📋 Total: {len(all_emotions)} emotions available")
    print()

def create_emotion_configuration_summary():
    """Tạo summary file cho emotion configuration"""
    print("📝 === CREATING CONFIGURATION SUMMARY ===\n")
    
    manager = EmotionConfigManager()
    
    summary = {
        "title": "Voice Studio - Emotion Configuration System",
        "version": "1.0",
        "description": "Comprehensive emotion parameter management for TTS voice generation",
        "features": [
            "25+ predefined emotions with optimized parameters",
            "Custom emotion creation and modification",
            "Emotion presets for different use cases",
            "Real-time parameter adjustment",
            "Export/import configuration files",
            "Statistics and analytics"
        ],
        "emotion_categories": {},
        "parameter_ranges": {
            "exaggeration": "0.0 - 2.5 (emotion intensity)",
            "cfg_weight": "0.0 - 1.0 (voice guidance strength)",
            "temperature": "0.1 - 1.5 (creativity/variability)",
            "speed": "0.5 - 2.0 (speaking speed)"
        },
        "use_cases": [
            "Audiobook narration",
            "Character dialogue",
            "Commercial/advertisement",
            "Educational content",
            "Entertainment/gaming",
            "Professional presentations"
        ]
    }
    
    # Add category details
    categories = manager.get_emotion_categories()
    for category in categories:
        emotions = manager.get_emotions_by_category(category)
        summary["emotion_categories"][category] = {
            "count": len(emotions),
            "emotions": list(emotions.keys()),
            "description": f"{category.title()} emotions for various voice expressions"
        }
    
    # Save summary
    summary_path = "EMOTION_CONFIGURATION_SUMMARY.md"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# 🎭 Voice Studio - Emotion Configuration System\n\n")
        f.write(f"**Version:** {summary['version']}\n\n")
        f.write(f"**Description:** {summary['description']}\n\n")
        
        f.write("## ✨ Features\n\n")
        for feature in summary['features']:
            f.write(f"- ✅ {feature}\n")
        f.write("\n")
        
        f.write("## 🎛️ Parameter Ranges\n\n")
        for param, desc in summary['parameter_ranges'].items():
            f.write(f"- **{param.title()}**: {desc}\n")
        f.write("\n")
        
        f.write("## 🏷️ Emotion Categories\n\n")
        for category, info in summary['emotion_categories'].items():
            f.write(f"### {category.title()}\n")
            f.write(f"**Count:** {info['count']} emotions\n\n")
            f.write(f"**Emotions:** {', '.join(info['emotions'][:5])}{'...' if len(info['emotions']) > 5 else ''}\n\n")
        
        f.write("## 🎬 Use Cases\n\n")
        for use_case in summary['use_cases']:
            f.write(f"- 🎯 {use_case}\n")
        f.write("\n")
        
        f.write("## 📊 Statistics\n\n")
        stats = manager.get_emotion_statistics()
        f.write(f"- **Total Emotions:** {stats['total_emotions']}\n")
        f.write(f"- **Default Emotions:** {stats['default_emotions']}\n")
        f.write(f"- **Custom Emotions:** {stats['custom_emotions']}\n")
        f.write(f"- **Emotion Presets:** {stats['total_presets']}\n")
    
    print(f"   ✅ Created: {summary_path}")
    print()

if __name__ == "__main__":
    print("🎭 VOICE STUDIO EMOTION CONFIGURATION DEMO")
    print("=" * 50)
    print()
    
    try:
        # Run demos
        manager = demo_emotion_manager()
        demo_emotion_usage_scenarios()
        demo_emotion_table_format()
        create_emotion_configuration_summary()
        
        print("🎉 === DEMO COMPLETED SUCCESSFULLY ===")
        print()
        print("📋 Files created:")
        print("   • demo_emotion_export.json - Exported emotion configuration")
        print("   • EMOTION_CONFIGURATION_SUMMARY.md - System documentation")
        print("   • configs/emotions/ - Custom emotions and presets")
        print()
        print("🚀 Next steps:")
        print("   1. Integrate EmotionConfigTab into main Voice Studio UI")
        print("   2. Connect emotion system to TTS generation")
        print("   3. Add real-time preview functionality")
        print("   4. Implement emotion presets loading")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc() 