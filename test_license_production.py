#!/usr/bin/env python3
"""
Test Voice Studio License Integration với Production Server
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.license_manager import LicenseManager

def test_production_license():
    """Test kết nối tới license server production"""
    
    print("🧪 Testing Voice Studio License Integration")
    print("=" * 50)
    
    # URL production server
    production_url = "https://my-voice-studio-license-74bdfd2609ed.herokuapp.com"
    
    # Tạo license manager và set production URL
    license_manager = LicenseManager()
    license_manager.license_server_url = production_url
    
    # Test licenses (đã tạo ở bước trước)
    test_licenses = [
        {
            "name": "Basic Plan",
            "key": "VS-T1OJRBRE-M2PKKRWY-F24KXLRU",
            "plan": "basic"
        },
        {
            "name": "Pro Plan", 
            "key": "VS-Z14AD804-CYGIEQIT-W6J6QW62",
            "plan": "pro"
        },
        {
            "name": "Enterprise Plan",
            "key": "VS-14PPPKQH-E3DO41WQ-9G1S44VL", 
            "plan": "enterprise"
        }
    ]
    
    print(f"🌐 Testing connection to: {production_url}")
    print()
    
    # Test từng license
    for i, license_info in enumerate(test_licenses, 1):
        print(f"📋 Test {i}: {license_info['name']}")
        print(f"   Key: {license_info['key']}")
        
        try:
            # Verify license
            result = license_manager.verify_license_online(license_info['key'])
            
            if result.get('status') == 'valid':
                print(f"   ✅ Status: VALID")
                print(f"   📦 Plan: {result.get('plan_type', 'N/A')}")
                print(f"   📅 Expires: {result.get('expiry_date', 'N/A')}")
                print(f"   🔧 Features: {len(result.get('features', {}))}")
                
                # Test specific features
                features_to_test = ['basic_tts', 'emotion_config', 'inner_voice', 'batch_processing']
                available_features = result.get('features', {})
                
                print(f"   🧩 Feature Check:")
                for feature in features_to_test:
                    status = "✅" if feature in available_features else "❌"
                    print(f"      {status} {feature}")
                    
            else:
                print(f"   ❌ Status: {result.get('status', 'INVALID')}")
                print(f"   🚫 Reason: {result.get('reason', 'Unknown')}")
                
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
            
        print()
    
    # Test cache functionality
    print("💾 Testing Cache Performance...")
    print("   First call (should hit server)...")
    
    import time
    start_time = time.time()
    result1 = license_manager.verify_license_online(test_licenses[1]['key'])
    first_call_time = time.time() - start_time
    
    print(f"   ⏱️  First call: {first_call_time:.3f}s")
    
    print("   Second call (should use cache)...")
    start_time = time.time()
    result2 = license_manager.verify_license_offline(test_licenses[1]['key'])
    second_call_time = time.time() - start_time
    
    print(f"   ⏱️  Second call: {second_call_time:.3f}s")
    
    if second_call_time < first_call_time:
        print("   ✅ Cache working! Second call is faster.")
    else:
        print("   ⚠️  Cache may not be working optimally.")
    
    print()
    print("🎉 Production License Test Complete!")
    print(f"📊 Results Summary:")
    print(f"   - Server URL: {production_url}")
    print(f"   - Licenses Tested: {len(test_licenses)}")
    print(f"   - Cache Performance: {'✅ Good' if second_call_time < first_call_time else '⚠️ Check needed'}")

if __name__ == "__main__":
    test_production_license() 