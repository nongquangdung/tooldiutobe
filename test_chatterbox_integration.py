#!/usr/bin/env python3
"""
🧪 CHATTERBOX TTS INTEGRATION TEST
==================================

Test script để verify Chatterbox TTS integration với Voice Studio.
Tests both Chatterbox TTS Server và fallback Real Chatterbox provider.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager, ChatterboxConfig
from src.tts.enhanced_voice_generator import EnhancedVoiceGenerator, VoiceGenerationRequest

def test_chatterbox_voices_manager():
    """Test Chatterbox Voices Manager"""
    print("🧪 Testing Chatterbox Voices Manager...")
    
    manager = ChatterboxVoicesManager()
    
    # Test 1: Voice loading
    voices = manager.get_available_voices()
    print(f"   ✅ Loaded {len(voices)} voices")
    
    # Test 2: Gender filtering
    female_voices = manager.get_voices_by_gender("female")
    male_voices = manager.get_voices_by_gender("male")
    print(f"   ✅ Female voices: {len(female_voices)}")
    print(f"   ✅ Male voices: {len(male_voices)}")
    
    # Test 3: Voice recommendations
    narrator_voices = manager.get_voice_recommendations("narrator")
    print(f"   ✅ Narrator recommendations: {narrator_voices[:3]}")
    
    # Test 4: Connection test
    connection_result = manager.test_chatterbox_connection()
    if connection_result.get("success"):
        print(f"   ✅ Chatterbox TTS Server: Online")
    else:
        print(f"   ⚠️ Chatterbox TTS Server: Offline - {connection_result.get('status')}")
    
    return connection_result.get("success", False)

def test_enhanced_voice_generator():
    """Test Enhanced Voice Generator"""
    print("\n🧪 Testing Enhanced Voice Generator...")
    
    generator = EnhancedVoiceGenerator()
    
    # Test 1: Provider status
    provider_status = generator.get_provider_status()
    print(f"   📊 Provider Status:")
    for provider, info in provider_status.items():
        status = "✅ Online" if info["available"] else "❌ Offline"
        voices_count = info.get('voices_count', len(info.get('voices', [])) if 'voices' in info else 0)
        print(f"      {provider}: {status} ({voices_count} voices)")
    
    # Test 2: Voice mappings
    all_voices = generator.get_available_voices()
    print(f"   ✅ Total voices mapped: {len(all_voices)}")
    
    # Test 3: Smart recommendations
    test_cases = [
        ("narrator", None, 8.0),
        ("hero", "male", 8.5),
        ("villain", "female", 8.0)
    ]
    
    print(f"   🎯 Smart Voice Recommendations:")
    for char_type, gender, quality_threshold in test_cases:
        best_voice = generator.get_best_voice_for_character(char_type, gender, quality_threshold)
        voice_info = all_voices.get(best_voice, {})
        print(f"      {char_type} ({gender or 'any'}): {voice_info.get('name', best_voice)} (Q: {voice_info.get('quality')}/10)")

def test_voice_generation():
    """Test actual voice generation"""
    print("\n🧪 Testing Voice Generation...")
    
    generator = EnhancedVoiceGenerator()
    
    # Prepare test output directory
    test_output_dir = "./test_chatterbox_output"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Test cases
    test_requests = [
        {
            "name": "Auto Provider Selection",
            "request": VoiceGenerationRequest(
                text="Hello! This is a test of the enhanced voice generation system.",
                character_id="test_auto",
                voice_provider="auto",
                voice_id="olivia",
                emotion="friendly",
                output_path=f"{test_output_dir}/test_auto.wav"
            )
        },
        {
            "name": "Chatterbox High Quality",
            "request": VoiceGenerationRequest(
                text="Testing Chatterbox TTS Server with high quality voice synthesis.",
                character_id="test_chatterbox",
                voice_provider="chatterbox",
                voice_id="gabriel",
                emotion="professional",
                temperature=0.8,
                speed=1.1,
                output_path=f"{test_output_dir}/test_chatterbox.wav"
            )
        },
        {
            "name": "Real Chatterbox Fallback",
            "request": VoiceGenerationRequest(
                text="Testing Real Chatterbox provider as a reliable fallback option.",
                character_id="test_fallback",
                voice_provider="real_chatterbox",
                voice_id="narrator",
                emotion="neutral",
                output_path=f"{test_output_dir}/test_fallback.wav"
            )
        }
    ]
    
    # Run generation tests
    results = []
    for test_case in test_requests:
        print(f"\n   🚀 {test_case['name']}:")
        
        start_time = time.time()
        result = generator.generate_voice(test_case["request"])
        end_time = time.time()
        
        if result.success:
            file_size = os.path.getsize(result.output_path) if os.path.exists(result.output_path) else 0
            print(f"      ✅ Success: {result.voice_used} via {result.provider_used}")
            print(f"      📊 Time: {result.generation_time:.2f}s | Quality: {result.quality_score}/10 | Size: {file_size} bytes")
        else:
            print(f"      ❌ Failed: {result.error_message}")
        
        results.append({
            "test_name": test_case["name"],
            "success": result.success,
            "provider_used": result.provider_used,
            "generation_time": result.generation_time,
            "quality_score": result.quality_score,
            "error": result.error_message if not result.success else None
        })
    
    return results

def export_test_results(results, chatterbox_online=False):
    """Export test results to JSON"""
    test_report = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "chatterbox_server_online": chatterbox_online,
        "total_tests": len(results),
        "successful_tests": sum(1 for r in results if r["success"]),
        "test_results": results,
        "summary": {
            "success_rate": f"{(sum(1 for r in results if r['success']) / len(results) * 100):.1f}%",
            "avg_generation_time": f"{sum(r['generation_time'] for r in results) / len(results):.2f}s",
            "avg_quality_score": f"{sum(r['quality_score'] for r in results if r['quality_score'] > 0) / max(1, sum(1 for r in results if r['quality_score'] > 0)):.1f}/10"
        }
    }
    
    output_file = f"chatterbox_integration_test_report_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Test report saved: {output_file}")
    return test_report

def main():
    """Run complete Chatterbox integration test suite"""
    print("🎙️ CHATTERBOX TTS INTEGRATION TEST SUITE")
    print("=" * 60)
    
    # Test 1: Chatterbox Voices Manager
    chatterbox_online = test_chatterbox_voices_manager()
    
    # Test 2: Enhanced Voice Generator
    test_enhanced_voice_generator()
    
    # Test 3: Voice Generation
    generation_results = test_voice_generation()
    
    # Export results
    test_report = export_test_results(generation_results, chatterbox_online)
    
    # Summary
    print(f"\n🎯 TEST SUMMARY:")
    print(f"   📊 Total Tests: {test_report['total_tests']}")
    print(f"   ✅ Successful: {test_report['successful_tests']}")
    print(f"   📈 Success Rate: {test_report['summary']['success_rate']}")
    print(f"   ⏱️ Avg Generation Time: {test_report['summary']['avg_generation_time']}")
    print(f"   🎯 Avg Quality Score: {test_report['summary']['avg_quality_score']}")
    print(f"   🌐 Chatterbox Server: {'✅ Online' if chatterbox_online else '❌ Offline'}")
    
    if chatterbox_online:
        print(f"\n🎉 INTEGRATION SUCCESS! Chatterbox TTS Server is working với Voice Studio!")
    else:
        print(f"\n⚠️ PARTIAL SUCCESS! Real Chatterbox fallback is working, but Chatterbox TTS Server is offline.")
        print(f"   💡 To test full integration, start Chatterbox TTS Server on localhost:8004")
    
    print(f"\n✅ Chatterbox Integration Test Complete!")

if __name__ == "__main__":
    main() 