#!/usr/bin/env python3
"""
🎯 TEST TTS TRỰC TIẾP - BỎ QUA FRONTEND
Kiểm tra ChatterboxTTS hoạt động hay không
"""

import sys
import os
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_direct_tts():
    """Test TTS trực tiếp không qua API"""
    try:
        print("🔄 Testing Direct ChatterboxTTS...")
        
        # Import TTS
        from tts.enhanced_voice_generator import EnhancedVoiceGenerator, VoiceGenerationRequest
        
        print("✅ Import successful")
        
        # Create generator
        generator = EnhancedVoiceGenerator()
        print("✅ Generator created")
        
        # Test request
        output_file = str(Path(__file__).parent / "test_direct_output.mp3")
        request = VoiceGenerationRequest(
            text="Test trực tiếp ChatterboxTTS",
            character_id="narrator",
            voice_id="olivia", 
            emotion="neutral",
            output_path=output_file
        )
        
        print("🎤 Generating audio...")
        result = generator.generate_voice(request)
        
        if result.success:
            file_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
            print(f"✅ SUCCESS! File: {output_file}")
            print(f"📁 Size: {file_size:,} bytes")
            print(f"🎯 Voice: {result.voice_used}")
            print(f"⚡ Provider: {result.provider_used}")
            print(f"⏱️ Time: {result.generation_time:.1f}s")
            
            # Kiểm tra file size
            if file_size > 50000:  # > 50KB = real audio
                print("🎉 REAL TTS WORKING! Audio có nội dung thật!")
                return True
            else:
                print("❌ File quá nhỏ - có thể mock mode")
                return False
        else:
            print(f"❌ FAILED: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_tts()
    sys.exit(0 if success else 1) 