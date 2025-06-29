#!/usr/bin/env python3
"""
Test script để debug inner voice preview
"""

import os
import sys
import traceback

# Add src to path
sys.path.insert(0, 'src')

def test_inner_voice_preview():
    """Test inner voice preview với debug logs"""
    
    print("🎭 Testing Inner Voice Preview...")
    
    try:
        # Import TTS provider
        from tts.real_chatterbox_provider import RealChatterboxProvider
        print("✅ RealChatterboxProvider imported")
        
        # Import Inner Voice Processor
        from core.inner_voice_processor import InnerVoiceProcessor, InnerVoiceType
        print("✅ InnerVoiceProcessor imported")
        
        # Test parameters cho light inner voice
        test_parameters = {
            'delay': 130.0,
            'decay': 0.3, 
            'gain': 0.5,
            'filter': 'aecho=0.5:0.3:130.0:0.3'
        }
        
        print(f"🔧 Test parameters: {test_parameters}")
        
        # Step 1: Generate base audio
        provider = RealChatterboxProvider()
        test_text = "Tôi đang suy nghĩ về những gì sẽ xảy ra tiếp theo. Có lẽ nên thử cách khác?"
        
        preview_dir = "test_inner_voice_output"
        os.makedirs(preview_dir, exist_ok=True)
        
        base_audio_path = os.path.join(preview_dir, "debug_base_light.wav")
        
        print(f"📝 Generating base audio: {test_text}")
        print(f"💾 Save path: {base_audio_path}")
        
        base_result = provider.generate_voice(
            text=test_text,
            save_path=base_audio_path,
            emotion_exaggeration=1.0,
            cfg_weight=0.5,
            speed=1.0
        )
        
        print(f"🔍 Base result: {base_result}")
        
        if not base_result.get('success', False):
            print(f"❌ Base TTS generation failed")
            return False
        
        if not os.path.exists(base_audio_path):
            print(f"❌ Base audio file not created: {base_audio_path}")
            return False
        
        print(f"✅ Base audio created: {base_audio_path}")
        
        # Step 2: Apply inner voice effects
        print(f"🎚️ Applying inner voice effects...")
        
        processor = InnerVoiceProcessor()
        print("✅ InnerVoiceProcessor created")
        
        # Set custom preset
        print(f"🔧 Setting custom preset for 'light'")
        processor.set_custom_preset('light', test_parameters)
        
        # Output path
        output_path = os.path.join(preview_dir, "debug_inner_voice_light.wav")
        
        # Convert to enum
        inner_voice_type = InnerVoiceType.LIGHT
        print(f"🔄 Using InnerVoiceType: {inner_voice_type}")
        
        # Process inner voice
        print(f"🎵 Processing: {base_audio_path} -> {output_path}")
        
        process_result = processor.process_inner_voice(
            input_path=base_audio_path,
            output_path=output_path,
            inner_voice_type=inner_voice_type
        )
        
        print(f"🔍 Process result: {process_result}")
        
        if process_result.get('success', False):
            print(f"✅ Inner voice processing successful!")
            print(f"📁 Output file: {output_path}")
            
            if os.path.exists(output_path):
                print(f"📊 Output file size: {os.path.getsize(output_path)} bytes")
                return True
            else:
                print(f"❌ Output file not found: {output_path}")
                return False
        else:
            error_msg = process_result.get('error', 'Unknown error')
            print(f"❌ Inner voice processing failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_inner_voice_preview()
    print(f"\n{'='*50}")
    if success:
        print("🎉 Inner Voice Preview Test: SUCCESS")
    else:
        print("💥 Inner Voice Preview Test: FAILED")
    print(f"{'='*50}") 