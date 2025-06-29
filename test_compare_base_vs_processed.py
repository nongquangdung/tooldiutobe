#!/usr/bin/env python3
"""
So sánh Base TTS vs Processed Inner Voice
"""

import os
import sys
import time
import subprocess
import platform
sys.path.insert(0, 'src')

def play_audio(file_path, label):
    """Play audio with label"""
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return False
    
    print(f"\n🎵 Playing {label}: {file_path}")
    print(f"📊 File size: {os.path.getsize(file_path)} bytes")
    
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", file_path], check=True)
        return True
    except Exception as e:
        print(f"❌ Lỗi play audio: {e}")
        return False

def create_test_files():
    """Tạo base và processed files để so sánh"""
    
    print("🎭 Creating test files để so sánh...")
    
    try:
        from tts.real_chatterbox_provider import RealChatterboxProvider
        from core.inner_voice_processor import InnerVoiceProcessor, InnerVoiceType
        
        # Text để test
        test_text = "Tôi đang suy nghĩ về những gì sẽ xảy ra tiếp theo. Có lẽ nên thử cách khác?"
        
        # Tạo thư mục output
        output_dir = "test_comparison_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Tạo base TTS
        provider = RealChatterboxProvider()
        base_path = os.path.join(output_dir, "base_audio.wav")
        
        print(f"📝 Generating base audio...")
        base_result = provider.generate_voice(
            text=test_text,
            save_path=base_path,
            emotion_exaggeration=1.0,
            cfg_weight=0.5,
            speed=1.0
        )
        
        if not base_result.get('success', False):
            print(f"❌ Base TTS generation failed")
            return None, None
        
        print(f"✅ Base audio created: {base_path}")
        
        # Step 2: Apply inner voice effects
        processor = InnerVoiceProcessor()
        
        # Test với light inner voice
        light_params = {
            'delay': 130.0,
            'decay': 0.3,
            'gain': 0.5,
            'filter': 'aecho=0.5:0.3:130.0:0.3'
        }
        
        processor.set_custom_preset('light', light_params)
        
        processed_path = os.path.join(output_dir, "inner_voice_light.wav")
        
        print(f"🎚️ Applying light inner voice effects...")
        process_result = processor.process_inner_voice(
            input_path=base_path,
            output_path=processed_path,
            inner_voice_type=InnerVoiceType.LIGHT
        )
        
        if process_result.get('success', False):
            print(f"✅ Inner voice processing successful: {processed_path}")
            return base_path, processed_path
        else:
            error_msg = process_result.get('error', 'Unknown error')
            print(f"❌ Inner voice processing failed: {error_msg}")
            return base_path, None
            
    except Exception as e:
        print(f"❌ Error creating test files: {e}")
        return None, None

def main():
    """Main comparison function"""
    
    print("🔊 COMPARISON TEST: Base TTS vs Inner Voice Processed")
    print("=" * 60)
    
    # Tạo test files
    base_path, processed_path = create_test_files()
    
    if not base_path:
        print("❌ Không thể tạo base audio")
        return
    
    if not processed_path:
        print("❌ Không thể tạo processed audio")
        return
    
    # So sánh thông tin files
    base_size = os.path.getsize(base_path)
    processed_size = os.path.getsize(processed_path)
    
    print(f"\n📊 FILE COMPARISON:")
    print(f"   Base TTS: {base_size} bytes")
    print(f"   Inner Voice: {processed_size} bytes")
    print(f"   Size ratio: {processed_size/base_size:.2%}")
    
    if processed_size < base_size:
        print("✅ Processed file nhỏ hơn - có áp dụng effects!")
    else:
        print("⚠️ Processed file không nhỏ hơn - effects có thể chưa được áp dụng")
    
    # Play audio để so sánh
    print(f"\n🎵 AUDIO COMPARISON:")
    print("Bạn sẽ nghe 2 files liên tiếp để so sánh:")
    
    input("\n👂 Press Enter để nghe BASE AUDIO (original TTS)...")
    play_audio(base_path, "BASE AUDIO")
    
    time.sleep(2)
    
    input("\n👂 Press Enter để nghe INNER VOICE (processed với effects)...")
    play_audio(processed_path, "INNER VOICE")
    
    print(f"\n💡 EXPECTED DIFFERENCES:")
    print("   - Inner voice sẽ có echo/reverb effect")
    print("   - Âm thanh sẽ có cảm giác xa hơn, như thoại nội tâm")
    print("   - Có thể có lowpass filter làm âm thanh mềm hơn")
    
    print(f"\n📁 Test files saved in: test_comparison_output/")
    print(f"   Base: {base_path}")
    print(f"   Processed: {processed_path}")

if __name__ == "__main__":
    main() 