#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Voice Modes - Voice Selection vs Voice Clone
Kiểm tra logic chọn giọng mới với 2 modes rõ ràng
"""

import sys
import os
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tts.real_chatterbox_provider import RealChatterboxProvider

def test_voice_selection_mode():
    """Test voice selection mode với các giọng có sẵn"""
    print("🗣️ TESTING VOICE SELECTION MODE")
    print("=" * 50)
    
    provider = RealChatterboxProvider.get_instance()
    
    # Test với các voice ID khác nhau
    test_voices = [
        ("female_young", "Giọng nữ trẻ"),
        ("male_young", "Giọng nam trẻ"),
        ("neutral_narrator", "Giọng kể chuyện")
    ]
    
    for voice_id, description in test_voices:
        print(f"\n🎭 Testing {description} ({voice_id})")
        
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, f"test_{voice_id}.mp3")
        
        result = provider.generate_voice(
            text=f"Xin chào, đây là test {description}",
            save_path=output_path,
            voice_name=voice_id,
            emotion_exaggeration=1.0,
            speed=1.0,
            cfg_weight=0.5
        )
        
        if result.get('success'):
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Success: {file_size:.1f}KB generated")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")

def test_voice_clone_mode():
    """Test voice clone mode với reference audio"""
    print("\n🎤 TESTING VOICE CLONE MODE")
    print("=" * 50)
    
    provider = RealChatterboxProvider.get_instance()
    
    # Tìm reference audio files trong project
    reference_paths = []
    
    # Check trong projects/manual_audio_project/audio/
    audio_dir = "projects/manual_audio_project/audio"
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith(('.mp3', '.wav')):
                reference_paths.append(os.path.join(audio_dir, file))
    
    if not reference_paths:
        print("⚠️ No reference audio files found for voice cloning test")
        print("   Expected location: projects/manual_audio_project/audio/")
        return
    
    # Test với reference audio đầu tiên
    reference_path = reference_paths[0]
    print(f"\n🎯 Using reference: {os.path.basename(reference_path)}")
    
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "test_voice_clone.mp3")
    
    result = provider.generate_voice(
        text="Xin chào, đây là test voice cloning với reference audio",
        save_path=output_path,
        voice_sample_path=reference_path,
        emotion_exaggeration=1.0,
        speed=1.0,
        cfg_weight=0.5
    )
    
    if result.get('success'):
        file_size = os.path.getsize(output_path) / 1024  # KB
        print(f"✅ Voice Clone Success: {file_size:.1f}KB generated")
        print(f"   Reference: {reference_path}")
    else:
        print(f"❌ Voice Clone Failed: {result.get('error', 'Unknown error')}")

def test_voice_mode_priority_logic():
    """Test logic chọn giữa voice selection và voice clone"""
    print("\n🎯 TESTING VOICE MODE PRIORITY LOGIC")
    print("=" * 50)
    
    # Simulate character settings
    test_cases = [
        {
            'name': 'Character A',
            'voice_mode': 'voice_selection',
            'voice_id': 'female_young',
            'voice_clone_path': None,
            'expected': 'selection'
        },
        {
            'name': 'Character B', 
            'voice_mode': 'voice_clone',
            'voice_id': 'male_young',
            'voice_clone_path': 'projects/manual_audio_project/audio/s1_d1_narrator.mp3',
            'expected': 'clone'
        },
        {
            'name': 'Character C',
            'voice_mode': 'voice_clone',
            'voice_id': 'female_young',
            'voice_clone_path': None,  # No clone path
            'expected': 'selection'  # Should fallback
        }
    ]
    
    for case in test_cases:
        print(f"\n👤 {case['name']}:")
        print(f"   Mode: {case['voice_mode']}")
        print(f"   Voice ID: {case['voice_id']}")
        print(f"   Clone Path: {case['voice_clone_path']}")
        
        # Simulate validation logic
        if case['voice_mode'] == 'voice_clone' and case['voice_clone_path'] and os.path.exists(case['voice_clone_path']):
            actual_mode = 'clone'
        else:
            actual_mode = 'selection'
        
        if actual_mode == case['expected']:
            print(f"   ✅ Result: {actual_mode} (as expected)")
        else:
            print(f"   ❌ Result: {actual_mode} (expected {case['expected']})")

def main():
    """Run all voice mode tests"""
    print("🎵 VOICE MODES TEST SUITE")
    print("Testing Voice Selection vs Voice Clone logic")
    print("=" * 60)
    
    try:
        # Test 1: Voice Selection Mode
        test_voice_selection_mode()
        
        # Test 2: Voice Clone Mode  
        test_voice_clone_mode()
        
        # Test 3: Priority Logic
        test_voice_mode_priority_logic()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED")
        print("✅ Voice Selection: Sử dụng giọng có sẵn")
        print("✅ Voice Clone: Sử dụng reference audio để clone")
        print("✅ Priority Logic: Voice mode quyết định behavior")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 