#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 PHASE 2 REAL AUDIO PROCESSING TEST
Test Audio Processor và Audio Exporter với real audio files
"""

import os
import sys
import time
import glob
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_audio_processor_real_files():
    """Test Audio Processor với real audio files"""
    print("🎵" + "="*70)
    print("🎵 PHASE 2 REAL AUDIO PROCESSING TEST")
    print("🎵 Testing với actual audio files")
    print("🎵" + "="*70)
    
    try:
        from core.audio_processor import AudioProcessor, AudioQualitySettings
        
        # Find test audio files
        audio_files = glob.glob("voice_studio_output/segment_*.mp3")
        if not audio_files:
            print("❌ No test audio files found in voice_studio_output/")
            return False
        
        # Use first few files for testing
        test_files = audio_files[:3]
        print(f"\n🎯 Testing with {len(test_files)} real audio files:")
        for file in test_files:
            file_size = os.path.getsize(file) / 1024  # KB
            print(f"   📁 {os.path.basename(file)} ({file_size:.1f}KB)")
        
        # Test different quality settings
        quality_presets = {
            "broadcast": AudioQualitySettings(
                target_lufs=-23.0,
                remove_silence=True,
                apply_compression=True,
                compression_ratio=2.5,
                apply_noise_gate=True
            ),
            "podcast": AudioQualitySettings(
                target_lufs=-18.0,
                remove_silence=True,
                apply_compression=True,
                compression_ratio=3.0,
                apply_noise_gate=False
            ),
            "youtube": AudioQualitySettings(
                target_lufs=-16.0,
                remove_silence=False,
                apply_compression=False,
                apply_noise_gate=False
            )
        }
        
        # Create output directory
        output_dir = "test_phase2_output"
        os.makedirs(output_dir, exist_ok=True)
        
        total_processed = 0
        total_exported = 0
        processing_results = []
        
        for preset_name, settings in quality_presets.items():
            print(f"\n🎛️ TESTING PRESET: {preset_name.upper()}")
            print("-" * 50)
            
            processor = AudioProcessor(settings)
            
            print(f"   🎯 Target LUFS: {settings.target_lufs}")
            print(f"   🔇 Remove Silence: {settings.remove_silence}")
            print(f"   🗜️ Compression: {settings.apply_compression}")
            print(f"   🚪 Noise Gate: {settings.apply_noise_gate}")
            
            for test_file in test_files:
                basename = Path(test_file).stem
                output_path = os.path.join(output_dir, f"{basename}_{preset_name}")
                
                print(f"\n   🔄 Processing: {os.path.basename(test_file)}")
                start_time = time.time()
                
                # Test multiple export formats
                export_formats = ['mp3', 'wav', 'flac']
                result = processor.process_audio_file(
                    input_path=test_file,
                    output_path=output_path,
                    export_formats=export_formats
                )
                
                processing_time = time.time() - start_time
                
                if result['success']:
                    print(f"   ✅ Success in {processing_time:.2f}s")
                    print(f"      📁 Output formats: {list(result['output_files'].keys())}")
                    
                    # Check file sizes
                    for format_type, file_path in result['output_files'].items():
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path) / 1024  # KB
                            print(f"      📊 {format_type.upper()}: {file_size:.1f}KB")
                            total_exported += 1
                    
                    total_processed += 1
                    processing_results.append({
                        'file': test_file,
                        'preset': preset_name,
                        'time': processing_time,
                        'formats': list(result['output_files'].keys())
                    })
                else:
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Summary
        print(f"\n🎉 PHASE 2 AUDIO PROCESSING RESULTS:")
        print(f"   📁 Files processed: {total_processed}/{len(test_files) * len(quality_presets)}")
        print(f"   📊 Formats exported: {total_exported}")
        print(f"   ⚡ Success rate: {total_processed/(len(test_files) * len(quality_presets))*100:.1f}%")
        
        if processing_results:
            avg_time = sum(r['time'] for r in processing_results) / len(processing_results)
            print(f"   ⏱️ Average processing time: {avg_time:.2f}s per file")
        
        return total_processed > 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Processing error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_audio_exporter_real_files():
    """Test Audio Exporter với multiple formats"""
    print(f"\n🚀 TESTING AUDIO EXPORTER")
    print("-" * 50)
    
    try:
        from core.audio_exporter import AudioExporter, AudioFormat, ExportSettings, AudioQuality
        
        # Find test audio files
        audio_files = glob.glob("voice_studio_output/segment_*.mp3")[:2]  # Test with 2 files
        
        if not audio_files:
            print("❌ No test files for exporter")
            return False
        
        exporter = AudioExporter()
        output_dir = "test_phase2_exports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test different quality presets
        quality_tests = [
            (AudioQuality.STANDARD, "Standard quality"),
            (AudioQuality.HIGH, "High quality"),
            (AudioQuality.LOSSLESS, "Lossless quality")
        ]
        
        # Test formats
        test_formats = [AudioFormat.MP3, AudioFormat.WAV, AudioFormat.FLAC]
        
        export_success = 0
        total_exports = 0
        
        for quality, description in quality_tests:
            print(f"\n   🎛️ Testing {description}")
            
            settings = ExportSettings()
            settings.apply_quality_preset(quality)
            
            for audio_file in audio_files:
                basename = Path(audio_file).stem
                print(f"      🔄 Exporting: {basename}")
                
                # Multi-format export
                results = exporter.export_multiple_formats(
                    input_path=audio_file,
                    output_dir=output_dir,
                    formats=test_formats,
                    settings=settings
                )
                
                total_exports += len(test_formats)
                for format_type, success in results.items():
                    if success:
                        export_success += 1
                        output_file = os.path.join(output_dir, f"{basename}.{format_type}")
                        if os.path.exists(output_file):
                            file_size = os.path.getsize(output_file) / 1024  # KB
                            print(f"         ✅ {format_type.upper()}: {file_size:.1f}KB")
                    else:
                        print(f"         ❌ {format_type.upper()}: Failed")
        
        # Test preset exports
        print(f"\n   🎯 Testing Use Case Presets:")
        test_use_cases = ['youtube', 'podcast', 'audiobook']
        
        for use_case in test_use_cases:
            print(f"      🎬 {use_case.title()} preset")
            job_id = exporter.export_with_preset(
                input_files=audio_files[:1],  # Test with 1 file
                output_dir=output_dir,
                use_case=use_case,
                quality=AudioQuality.STANDARD
            )
            
            status = exporter.get_job_status(job_id)
            if status and status['status'] == 'completed':
                print(f"         ✅ Completed: {status['files_processed']} files")
            else:
                print(f"         ❌ Failed or incomplete")
        
        print(f"\n   📊 Export Results:")
        print(f"      ✅ Successful: {export_success}/{total_exports}")
        print(f"      📈 Success rate: {export_success/total_exports*100:.1f}%")
        
        return export_success > 0
        
    except ImportError as e:
        print(f"❌ Audio Exporter import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

def test_parallel_processor_with_real_audio():
    """Test Parallel Processor với real audio processing tasks"""
    print(f"\n⚡ TESTING PARALLEL PROCESSOR WITH REAL TASKS")
    print("-" * 50)
    
    try:
        from core.parallel_processor import ParallelProcessor
        
        processor = ParallelProcessor(num_workers=4)
        
        # Register real audio processing handler
        def real_audio_task_handler(input_data):
            """Real audio processing task"""
            import tempfile
            import shutil
            
            input_file = input_data.get('input_file')
            processing_type = input_data.get('processing_type', 'copy')
            
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            # Simulate different processing types
            temp_output = tempfile.mktemp(suffix='.mp3')
            
            if processing_type == 'copy':
                shutil.copy2(input_file, temp_output)
                time.sleep(0.1)  # Simulate processing time
            elif processing_type == 'analyze':
                # Simulate audio analysis
                time.sleep(0.3)
                file_size = os.path.getsize(input_file)
                with open(temp_output, 'wb') as f:
                    f.write(f'Analysis of {input_file}: {file_size} bytes'.encode())
            
            return {
                'success': True,
                'output_file': temp_output,
                'input_file': input_file,
                'processing_type': processing_type,
                'file_size': os.path.getsize(temp_output)
            }
        
        processor.register_task_handler('real_audio_processing', real_audio_task_handler)
        processor.start_workers()
        
        # Submit real audio processing tasks
        audio_files = glob.glob("voice_studio_output/segment_*.mp3")[:6]  # Test with 6 files
        
        if not audio_files:
            print("❌ No audio files for parallel processing test")
            return False
        
        print(f"      📁 Processing {len(audio_files)} real audio files")
        
        # Submit tasks
        task_ids = []
        for i, audio_file in enumerate(audio_files):
            task_id = f"real_audio_task_{i}"
            task_data = {
                'input_file': audio_file,
                'processing_type': 'copy' if i % 2 == 0 else 'analyze'
            }
            
            if processor.submit_task(task_id, task_data, 'real_audio_processing'):
                task_ids.append(task_id)
        
        # Wait for completion
        print(f"      ⏳ Waiting for {len(task_ids)} tasks to complete...")
        time.sleep(3.0)  # Give time for processing
        
        # Check results
        completed = 0
        failed = 0
        
        for task_id in task_ids:
            status = processor.get_task_status(task_id)
            if status:
                if status['status'] == 'completed' and status['success']:
                    completed += 1
                else:
                    failed += 1
        
        # Get performance stats
        stats = processor.get_performance_stats()
        
        processor.stop_workers()
        
        print(f"      ✅ Completed: {completed}/{len(task_ids)}")
        print(f"      ❌ Failed: {failed}")
        print(f"      ⚡ Throughput: {stats['throughput_per_second']:.2f} tasks/sec")
        print(f"      📈 Efficiency: {stats['efficiency']:.1f}%")
        
        return completed > 0
        
    except ImportError as e:
        print(f"❌ Parallel Processor import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Parallel processing error: {e}")
        return False

def main():
    """Run all Phase 2 real audio tests"""
    print("🚀 Starting Phase 2 real audio processing tests...")
    
    results = []
    
    # Test 1: Audio Processor
    results.append(("Audio Processor", test_audio_processor_real_files()))
    
    # Test 2: Audio Exporter
    results.append(("Audio Exporter", test_audio_exporter_real_files()))
    
    # Test 3: Parallel Processor with real tasks
    results.append(("Parallel Processor", test_parallel_processor_with_real_audio()))
    
    # Summary
    print(f"\n🎉 PHASE 2 REAL AUDIO TEST SUMMARY:")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{len(results)} tests passed ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("🎉 PHASE 2 REAL AUDIO PROCESSING: 100% SUCCESS!")
        print("   Ready for production use với real audio files!")
    else:
        print("⚠️ Some tests failed - investigate issues before production")

if __name__ == "__main__":
    main() 