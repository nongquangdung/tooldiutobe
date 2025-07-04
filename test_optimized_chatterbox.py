#!/usr/bin/env python3
"""
Test OptimizedChatterboxProvider với benchmarks
So sánh tốc độ generation giữa optimized và standard provider
"""

import os
import sys
import time
sys.path.append('./src')

from tts.optimized_chatterbox_provider import OptimizedChatterboxProvider

def test_optimized_provider():
    """Test basic functionality of OptimizedChatterboxProvider"""
    print("🧪 Testing OptimizedChatterboxProvider...")
    print("="*60)
    
    # Initialize provider với different optimization levels
    configs = [
        {
            "name": "Standard (float32, no compilation)",
            "device": "cuda",
            "dtype": "float32", 
            "use_compilation": False,
            "cpu_offload": False
        },
        {
            "name": "Mixed Precision (float16)",
            "device": "cuda",
            "dtype": "float16",
            "use_compilation": False,
            "cpu_offload": False
        },
        {
            "name": "Full Optimization (float16 + compilation)",
            "device": "cuda",
            "dtype": "float16",
            "use_compilation": True,
            "cpu_offload": False
        }
    ]
    
    test_text = "Hello world! This is a test of the optimized ChatterboxTTS provider. It should be significantly faster than the standard implementation."
    voice_path = "./voices/Abigail.wav"  # Use predefined voice
    
    if not os.path.exists(voice_path):
        print(f"❌ Voice file not found: {voice_path}")
        print("   Using None voice path for default voice")
        voice_path = None
    
    results = []
    
    for config in configs:
        print(f"\n🔧 Testing: {config['name']}")
        print("-" * 40)
        
        try:
            # Initialize provider
            provider = OptimizedChatterboxProvider(
                device=config["device"],
                dtype=config["dtype"],
                use_compilation=config["use_compilation"],
                cpu_offload=config["cpu_offload"]
            )
            
            # Load model
            if not provider.load_model():
                print(f"❌ Failed to load model for {config['name']}")
                continue
            
            # Warm up (especially important for compilation)
            print("🔥 Warming up...")
            provider.generate(
                text="Warm up generation",
                voice_path=voice_path,
                emotion="neutral"
            )
            
            # Benchmark generation
            print("⏱️ Benchmarking...")
            start_time = time.time()
            
            output_path = provider.generate(
                text=test_text,
                voice_path=voice_path,
                emotion="neutral",
                exaggeration=0.5,
                cfg_weight=0.5
            )
            
            generation_time = time.time() - start_time
            
            if output_path and os.path.exists(output_path):
                # Calculate audio duration
                try:
                    import librosa
                    audio, sr = librosa.load(output_path)
                    audio_duration = len(audio) / sr
                    rtf = audio_duration / generation_time  # Real-time factor
                    
                    result = {
                        "config": config["name"],
                        "generation_time": generation_time,
                        "audio_duration": audio_duration,
                        "rtf": rtf,
                        "success": True
                    }
                    results.append(result)
                    
                    print(f"✅ Success!")
                    print(f"   ⏱️ Generation time: {generation_time:.2f}s")
                    print(f"   🎵 Audio duration: {audio_duration:.2f}s")
                    print(f"   🚀 Real-time factor: {rtf:.2f}x")
                    print(f"   📁 Output: {output_path}")
                    
                except Exception as e:
                    print(f"⚠️ Could not analyze audio: {e}")
                    results.append({
                        "config": config["name"],
                        "generation_time": generation_time,
                        "success": True,
                        "note": "Could not analyze audio duration"
                    })
            else:
                print(f"❌ Generation failed for {config['name']}")
                results.append({
                    "config": config["name"],
                    "success": False
                })
            
        except Exception as e:
            print(f"❌ Error testing {config['name']}: {e}")
            results.append({
                "config": config["name"],
                "success": False,
                "error": str(e)
            })
    
    # Print comparison results
    print("\n📊 BENCHMARK RESULTS")
    print("="*60)
    
    successful_results = [r for r in results if r.get("success", False) and "rtf" in r]
    
    if successful_results:
        # Sort by generation time (fastest first)
        successful_results.sort(key=lambda x: x["generation_time"])
        
        print(f"{'Configuration':<35} {'Time (s)':<10} {'RTF':<8} {'Speedup'}")
        print("-" * 65)
        
        baseline_time = None
        for result in successful_results:
            if baseline_time is None:
                baseline_time = result["generation_time"]
                speedup = "1.00x (baseline)"
            else:
                speedup = f"{baseline_time / result['generation_time']:.2f}x"
            
            print(f"{result['config']:<35} {result['generation_time']:<10.2f} {result['rtf']:<8.2f} {speedup}")
        
        # Find best result
        best_result = successful_results[0]
        print(f"\n🏆 FASTEST: {best_result['config']}")
        print(f"   ⚡ Time: {best_result['generation_time']:.2f}s")
        print(f"   🚀 RTF: {best_result['rtf']:.2f}x")
        
        if len(successful_results) > 1:
            slowest_result = successful_results[-1]
            speedup = slowest_result["generation_time"] / best_result["generation_time"]
            print(f"   📈 Speedup vs slowest: {speedup:.2f}x")
    
    else:
        print("❌ No successful benchmark results")
    
    return results

def test_provider_status():
    """Test provider status and capabilities"""
    print("\n🔍 Testing Provider Status...")
    print("-" * 40)
    
    try:
        provider = OptimizedChatterboxProvider()
        status = provider.get_status()
        
        print("📋 Provider Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Status test failed: {e}")

if __name__ == "__main__":
    print("🚀 OptimizedChatterboxProvider Benchmark")
    print("Testing các optimization techniques cho ChatterboxTTS")
    print("="*60)
    
    # Test basic functionality
    test_provider_status()
    
    # Run benchmarks
    results = test_optimized_provider()
    
    print("\n✅ Testing completed!")
    print("\n💡 Optimization Tips:")
    print("   1. Use float16 for 2x memory reduction + speed boost")
    print("   2. Enable compilation for 2-4x speedup (CUDA only)")  
    print("   3. Use voice caching for repeated generations")
    print("   4. Consider CPU offloading for limited VRAM")
    
    print("\n🔧 Environment Variables:")
    print("   CHATTERBOX_DTYPE=float16|float32|bfloat16")
    print("   CHATTERBOX_COMPILATION=true|false")
    print("   CHATTERBOX_CPU_OFFLOAD=true|false")
    print("   DISABLE_OPTIMIZATION=true|false") 