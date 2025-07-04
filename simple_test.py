#!/usr/bin/env python3
"""
Simple test for OptimizedChatterboxProvider
"""

import sys
import time
sys.path.append('./src')

def test_basic():
    print("🧪 Testing OptimizedChatterboxProvider...")
    
    try:
        from tts.optimized_chatterbox_provider import OptimizedChatterboxProvider
        print("✅ Import successful")
        
        # Test với float16 optimization
        provider = OptimizedChatterboxProvider(
            device="cuda",
            dtype="float16", 
            use_compilation=False,  # Disable compilation for now
            cpu_offload=False
        )
        print("✅ Provider initialized")
        
        # Get status
        status = provider.get_status()
        print("\n📋 Provider Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test generation
        print("\n🎤 Testing generation...")
        start_time = time.time()
        
        result = provider.generate(
            text="Hello, this is a test of the optimized ChatterboxTTS provider.",
            voice_path=None,  # Use default voice
            emotion="neutral"
        )
        
        generation_time = time.time() - start_time
        
        if result:
            print(f"✅ Generation successful!")
            print(f"   ⏱️ Time: {generation_time:.2f}s")
            print(f"   📁 Output: {result}")
        else:
            print("❌ Generation failed")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic() 