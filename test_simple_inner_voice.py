#!/usr/bin/env python3
"""
Test Script cho Simple Inner Voice Effects
Demonstrates the simplified inner voice processing workflow
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Import ONLY the new simple processor, not the old one
from src.core.inner_voice_simple import SimpleInnerVoiceProcessor, apply_inner_voice_effects
from src.tts.voice_generator import get_voice_generator
import time

def test_simple_inner_voice():
    """Test simple inner voice workflow: TTS → FFmpeg effects"""
    
    print("🎵 TESTING SIMPLE INNER VOICE WORKFLOW")
    print("=" * 50)
    
    # Step 1: Generate base TTS audio
    print("\n📝 Step 1: Generating base TTS audio...")
    
    voice_gen = get_voice_generator()
    timestamp = int(time.time())
    base_file = f"test_audio_output/simple_test_base_{timestamp}.wav"
    
    # Ensure directory exists
    os.makedirs("test_audio_output", exist_ok=True)
    
    test_text = "This is a simple test of the inner voice effects. Let's see how it sounds with different processing."
    
    success = voice_gen.generate_voice(
        text=test_text,
        output_path=base_file,
        voice_name="Abigail",
        emotion_intensity=1.0,
        speed=1.0,
        cfg_weight=0.5
    )
    
    if not success or not os.path.exists(base_file):
        print("❌ Failed to generate base TTS")
        return False
    
    print(f"✅ Base TTS generated: {base_file}")
    input_size = os.path.getsize(base_file)
    print(f"   📊 Base file size: {input_size//1024}KB")
    
    # Step 2: Test all inner voice types
    processor = SimpleInnerVoiceProcessor()
    voice_types = ['light', 'deep', 'dreamy']
    
    results = {}
    
    for voice_type in voice_types:
        print(f"\n🎭 Step 2.{voice_types.index(voice_type)+1}: Testing {voice_type} inner voice...")
        
        # Output file for this type
        output_file = f"test_inner_voice_output/simple_test_{voice_type}_{timestamp}.wav"
        
        # Apply effects
        success = apply_inner_voice_effects(
            input_file=base_file,
            output_file=output_file,
            voice_type=voice_type
        )
        
        if success and os.path.exists(output_file):
            output_size = os.path.getsize(output_file)
            print(f"✅ {voice_type.title()} effects applied successfully!")
            print(f"   📊 Output size: {output_size//1024}KB")
            print(f"   📁 File: {output_file}")
            
            results[voice_type] = {
                'success': True,
                'file': output_file,
                'size': output_size
            }
        else:
            print(f"❌ Failed to apply {voice_type} effects")
            results[voice_type] = {
                'success': False,
                'file': None,
                'size': 0
            }
    
    # Step 3: Test custom parameters
    print(f"\n🔧 Step 3: Testing custom parameters...")
    
    custom_params = {
        'delay': 600.0,
        'decay': 0.5,
        'gain': 0.8
    }
    
    custom_output = f"test_inner_voice_output/simple_test_custom_{timestamp}.wav"
    
    success = apply_inner_voice_effects(
        input_file=base_file,
        output_file=custom_output,
        voice_type='light',
        custom_params=custom_params
    )
    
    if success and os.path.exists(custom_output):
        custom_size = os.path.getsize(custom_output)
        print(f"✅ Custom parameters applied successfully!")
        print(f"   📊 Output size: {custom_size//1024}KB")
        print(f"   📁 File: {custom_output}")
        print(f"   🎛️ Params: delay={custom_params['delay']}, decay={custom_params['decay']}, gain={custom_params['gain']}")
        
        results['custom'] = {
            'success': True,
            'file': custom_output,
            'size': custom_size,
            'params': custom_params
        }
    else:
        print(f"❌ Failed to apply custom parameters")
        results['custom'] = {'success': False}
    
    # Step 4: Summary
    print(f"\n📊 SUMMARY RESULTS")
    print("=" * 30)
    print(f"✅ Base TTS: {base_file} ({input_size//1024}KB)")
    
    for voice_type, result in results.items():
        if result['success']:
            print(f"✅ {voice_type.title()}: {result['file']} ({result['size']//1024}KB)")
        else:
            print(f"❌ {voice_type.title()}: Failed")
    
    # Cleanup base file
    try:
        os.remove(base_file)
        print(f"\n🗑️ Cleaned up base file: {base_file}")
    except:
        pass
    
    # Test processor methods
    print(f"\n🔍 PROCESSOR METHODS TEST")
    print("=" * 30)
    
    available_types = processor.get_available_types()
    print(f"📋 Available types: {available_types}")
    
    for voice_type in available_types:
        config = processor.get_config(voice_type)
        print(f"⚙️ {voice_type.title()} config: delay={config['delay']}, decay={config['decay']}, gain={config['gain']}")
    
    print(f"\n🎉 SIMPLE INNER VOICE TEST COMPLETED!")
    
    # Count successful results
    success_count = sum(1 for r in results.values() if r['success'])
    total_count = len(results)
    
    print(f"   📊 Success rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    return success_count == total_count

if __name__ == "__main__":
    try:
        success = test_simple_inner_voice()
        
        if success:
            print(f"\n✅ ALL TESTS PASSED - Simple Inner Voice working correctly!")
            sys.exit(0)
        else:
            print(f"\n❌ SOME TESTS FAILED - Check the output above")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 