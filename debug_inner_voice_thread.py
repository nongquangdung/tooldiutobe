#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

print("🔧 Testing inner voice processing directly...")

# Test Step 1: Generate base TTS
print("🎵 Step 1: Generate base TTS...")
from tts.real_chatterbox_provider import RealChatterboxProvider
provider = RealChatterboxProvider()

preview_dir = "test_inner_voice_output"
os.makedirs(preview_dir, exist_ok=True)

import time
timestamp = str(int(time.time()))
base_audio_path = os.path.join(preview_dir, f"base_light_{timestamp}.wav")

preview_text = "Tôi đang suy nghĩ về những gì sẽ xảy ra tiếp theo. Có lẽ nên thử cách khác?"

base_result = provider.generate_voice(
    text=preview_text,
    save_path=base_audio_path,
    emotion_exaggeration=1.0,
    cfg_weight=0.5,
    speed=1.0
)

print(f"🔍 Base result: {base_result}")

if not base_result.get('success', False):
    print(f"❌ Base TTS failed")
    exit(1)

# Kiểm tra file location
actual_path = base_result.get('file_path', base_audio_path)
print(f"✅ Base audio: {actual_path}")
print(f"📊 File exists: {os.path.exists(actual_path)}")

if actual_path != base_audio_path and os.path.exists(actual_path):
    base_audio_path = actual_path

# Test Step 2: Apply inner voice effects
print("\n🎚️ Step 2: Apply inner voice effects...")

try:
    from core.inner_voice_processor import InnerVoiceProcessor, InnerVoiceType
    processor = InnerVoiceProcessor()
    print("✅ InnerVoiceProcessor imported")
    
    # Set custom preset
    parameters = {
        'delay': 400.0, 
        'decay': 0.3, 
        'gain': 0.5, 
        'filter': 'aecho=0.5:0.3:400.0:0.3'
    }
    processor.set_custom_preset('light', parameters)
    print(f"🔧 Custom preset set: {parameters}")
    
    # Output path
    output_path = os.path.join(preview_dir, f"inner_voice_preview_light_{timestamp}.wav")
    
    # Process
    inner_voice_enum = InnerVoiceType.LIGHT
    print(f"🎵 Processing: {base_audio_path} -> {output_path}")
    
    process_result = processor.process_inner_voice(
        input_path=base_audio_path,
        output_path=output_path,
        inner_voice_type=inner_voice_enum
    )
    
    print(f"🔍 Process result: {process_result}")
    
    if process_result.get('success', False):
        print(f"✅ INNER VOICE SUCCESS: {output_path}")
        print(f"📊 File exists: {os.path.exists(output_path)}")
        if os.path.exists(output_path):
            print(f"📏 File size: {os.path.getsize(output_path)} bytes")
            
        # Compare sizes
        base_size = os.path.getsize(base_audio_path) if os.path.exists(base_audio_path) else 0
        processed_size = os.path.getsize(output_path)
        print(f"📊 Base: {base_size} bytes, Processed: {processed_size} bytes")
    else:
        error_msg = process_result.get('error', 'Unknown error')
        print(f"❌ Inner voice processing failed: {error_msg}")
        
except Exception as e:
    print(f"❌ Step 2 error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Direct test completed!") 