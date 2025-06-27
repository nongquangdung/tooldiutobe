#!/usr/bin/env python3
"""
Test script cho license server
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Server config
SERVER_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def create_test_license(email, plan="pro", days=30, max_devices=2):
    """Tạo license test"""
    try:
        data = {
            "customer_email": email,
            "plan_type": plan,
            "duration_days": days,
            "max_activations": max_devices
        }
        
        response = requests.post(f"{SERVER_URL}/api/create_license", 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            license_data = response.json()
            print(f"✅ License created: {license_data['license_key']}")
            print(f"   Plan: {license_data['plan_type']}")
            print(f"   Expires: {license_data['expiry_date']}")
            return license_data
        else:
            print(f"❌ License creation failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ License creation error: {e}")
        return None

def test_license_verification(license_key, hardware_id="TEST-HARDWARE-12345"):
    """Test license verification"""
    try:
        data = {
            "license_key": license_key,
            "hardware_id": hardware_id,
            "app_version": "1.0.0"
        }
        
        response = requests.post(f"{SERVER_URL}/api/verify", 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"✅ License verification: {verify_data['status']}")
            print(f"   Plan: {verify_data.get('plan_type', 'N/A')}")
            print(f"   Features: {list(verify_data.get('features', {}).keys())}")
            return verify_data
        else:
            print(f"❌ License verification failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ License verification error: {e}")
        return None

def test_license_status(license_key):
    """Test license status endpoint"""
    try:
        response = requests.get(f"{SERVER_URL}/api/status/{license_key}", timeout=10)
        
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ License status: {status_data['status']}")
            print(f"   Email: {status_data['customer_email']}")
            print(f"   Activations: {status_data['current_activations']}/{status_data['max_activations']}")
            return status_data
        else:
            print(f"❌ License status failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ License status error: {e}")
        return None

def main():
    """Main test function"""
    print("🔧 Testing License Server...")
    print("=" * 50)
    
    # 1. Test health
    if not test_health():
        print("❌ Server không chạy. Hãy start server trước!")
        return
    
    print("\n📝 Creating test licenses...")
    
    # 2. Tạo license test
    demo_licenses = []
    
    # Basic license
    basic_license = create_test_license("test-basic@example.com", "basic", 7, 1)
    if basic_license:
        demo_licenses.append(basic_license)
    
    # Pro license  
    pro_license = create_test_license("test-pro@example.com", "pro", 30, 2)
    if pro_license:
        demo_licenses.append(pro_license)
    
    # Enterprise license
    enterprise_license = create_test_license("test-enterprise@example.com", "enterprise", 365, 5)
    if enterprise_license:
        demo_licenses.append(enterprise_license)
    
    print(f"\n✅ Created {len(demo_licenses)} demo licenses")
    
    # 3. Test verification
    print("\n🔐 Testing license verification...")
    for license_data in demo_licenses:
        license_key = license_data['license_key']
        print(f"\nTesting {license_key}...")
        
        # Verify license
        verify_result = test_license_verification(license_key)
        
        # Check status
        status_result = test_license_status(license_key)
    
    print("\n🎉 License server test completed!")
    print("\n📋 Demo License Keys:")
    for i, license_data in enumerate(demo_licenses):
        plan_names = {"basic": "Basic", "pro": "Pro", "enterprise": "Enterprise"}
        plan_name = plan_names.get(license_data['plan_type'], license_data['plan_type'])
        print(f"   {i+1}. {plan_name}: {license_data['license_key']}")

if __name__ == "__main__":
    main() 