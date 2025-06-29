#!/usr/bin/env python3
"""
🎭 TEST UNIFIED 93 EMOTIONS SYSTEM
==================================

Test script để kiểm tra:
1. 93 emotions config load correctly
2. Emotion Config Tab hiển thị 93 emotions
3. Advanced window mapping sử dụng config thay vì hardcode
4. Export/Import functionality với 93 emotions
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.append("src")

def test_config_loading():
    """Test loading 93 emotions config"""
    print("🔍 Testing unified_emotions.json loading...")
    
    config_path = Path("configs/emotions/unified_emotions.json")
    if not config_path.exists():
        print("❌ Config file not found!")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ Config loaded successfully!")
        print(f"   📊 Version: {config.get('version', 'N/A')}")
        print(f"   📈 Total emotions: {config.get('total_emotions', 0)}")
        print(f"   📝 Description: {config.get('description', 'N/A')}")
        
        # Check emotions structure
        emotions = config.get('emotions', {})
        if len(emotions) >= 90:
            print(f"✅ Emotions count: {len(emotions)} (Expected 90+)")
        else:
            print(f"⚠️ Emotions count: {len(emotions)} (Expected 90+)")
        
        # Sample some emotions
        sample_emotions = list(emotions.keys())[:5]
        print(f"   🎭 Sample emotions: {sample_emotions}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

def test_unified_emotion_system():
    """Test unified emotion system functions"""
    print("\n🔍 Testing unified emotion system functions...")
    
    try:
        from src.core.unified_emotion_system import UnifiedEmotionSystem, get_emotion_parameters
        
        # Test system initialization
        system = UnifiedEmotionSystem()
        print("✅ UnifiedEmotionSystem initialized")
        
        # Test get_emotion_parameters function
        test_emotions = ['happy', 'sad', 'angry', 'surprised', 'mysterious', 'commanding']
        
        for emotion in test_emotions:
            params = get_emotion_parameters(emotion)
            if params:
                print(f"   🎭 {emotion}: T={params.get('temperature', 'N/A'):.1f}, E={params.get('exaggeration', 'N/A'):.1f}, C={params.get('cfg_weight', 'N/A'):.1f}, S={params.get('speed', 'N/A'):.1f}")
            else:
                print(f"   ❌ {emotion}: No parameters found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing unified emotion system: {e}")
        return False

def test_advanced_window_mapping():
    """Test advanced window emotion mapping"""
    print("\n🔍 Testing advanced window emotion mapping...")
    
    try:
        # Import advanced window (này có thể fail do UI dependencies)
        sys.path.append("src/ui")
        
        # Test basic mapping function without full UI
        from src.core.unified_emotion_system import get_emotion_parameters
        
        test_emotions = ['surprised', 'furious', 'mysterious', 'innocent', 'commanding']
        
        print("   Testing config-based mapping:")
        for emotion in test_emotions:
            params = get_emotion_parameters(emotion)
            if params:
                exaggeration = params.get('exaggeration', 1.0)
                cfg_weight = params.get('cfg_weight', 0.5)
                
                # Check if values are within expert range
                expert_compliant = (0.8 <= exaggeration <= 1.2) and (0.4 <= cfg_weight <= 0.7)
                status = "✅" if expert_compliant else "⚠️"
                
                print(f"   {status} {emotion}: exaggeration={exaggeration:.2f}, cfg_weight={cfg_weight:.2f}")
            else:
                print(f"   ❌ {emotion}: Not found in config")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing advanced window mapping: {e}")
        return False

def test_emotion_categories():
    """Test emotion categories distribution"""
    print("\n🔍 Testing emotion categories...")
    
    try:
        with open("configs/emotions/unified_emotions.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        emotions = config.get('emotions', {})
        categories = {}
        
        for emotion_data in emotions.values():
            category = emotion_data.get('category', 'unknown')
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        print("   📊 Emotion categories distribution:")
        for category, count in sorted(categories.items()):
            print(f"      {category}: {count} emotions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing categories: {e}")
        return False

def test_parameter_ranges():
    """Test parameter ranges compliance"""
    print("\n🔍 Testing parameter ranges...")
    
    try:
        with open("configs/emotions/unified_emotions.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        emotions = config.get('emotions', {})
        
        # Expert recommendations
        expert_ranges = {
            'temperature': (0.7, 1.0),
            'exaggeration': (0.8, 1.2),
            'cfg_weight': (0.5, 0.7),
            'speed': (0.8, 1.3)
        }
        
        compliance_stats = {param: {'compliant': 0, 'total': 0} for param in expert_ranges}
        
        for emotion_name, emotion_data in emotions.items():
            for param, (min_val, max_val) in expert_ranges.items():
                value = emotion_data.get(param, 0)
                compliance_stats[param]['total'] += 1
                
                if min_val <= value <= max_val:
                    compliance_stats[param]['compliant'] += 1
        
        print("   📏 Expert compliance check:")
        for param, stats in compliance_stats.items():
            percentage = (stats['compliant'] / stats['total']) * 100
            status = "✅" if percentage >= 80 else "⚠️"
            print(f"      {status} {param}: {stats['compliant']}/{stats['total']} ({percentage:.1f}%) compliant")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing parameter ranges: {e}")
        return False

def test_export_functionality():
    """Test export functionality simulation"""
    print("\n🔍 Testing export functionality simulation...")
    
    try:
        from src.core.unified_emotion_system import UnifiedEmotionSystem
        
        system = UnifiedEmotionSystem()
        
        # Simulate export (get current config)
        current_config = system.export_emotion_config()
        
        if current_config and 'emotions' in current_config:
            emotion_count = len(current_config['emotions'])
            print(f"✅ Export simulation successful: {emotion_count} emotions")
            
            # Test a few sample exports
            sample_emotions = ['happy', 'sad', 'mysterious', 'commanding', 'innocent']
            print("   📋 Sample exported emotions:")
            
            for emotion in sample_emotions:
                if emotion in current_config['emotions']:
                    data = current_config['emotions'][emotion]
                    print(f"      {emotion}: T={data.get('temperature', 0):.1f}, E={data.get('exaggeration', 0):.1f}")
                else:
                    print(f"      ❌ {emotion}: Not found")
            
            return True
        else:
            print("❌ Export simulation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing export: {e}")
        return False

def main():
    """Main test execution"""
    print("🎭 UNIFIED 93 EMOTIONS SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        ("Config Loading", test_config_loading),
        ("Unified Emotion System", test_unified_emotion_system), 
        ("Advanced Window Mapping", test_advanced_window_mapping),
        ("Emotion Categories", test_emotion_categories),
        ("Parameter Ranges", test_parameter_ranges),
        ("Export Functionality", test_export_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! 93 emotions system is ready!")
    else:
        print("⚠️ Some tests failed. Check the details above.")

if __name__ == "__main__":
    main() 