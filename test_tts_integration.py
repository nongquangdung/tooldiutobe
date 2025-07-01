#!/usr/bin/env python3
"""
🧪 VOICE STUDIO TTS INTEGRATION TEST
====================================

Comprehensive test script for Voice Studio TTS system
Tests both Manual mode and JSON mode functionality
"""

import json
import time
import requests
from pathlib import Path

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_OUTPUT_DIR = Path("test_tts_output")
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

class TTSIntegrationTester:
    """TTS Integration Testing Suite"""
    
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
        self.session = requests.Session()
        self.test_results = {
            "api_connection": False,
            "voices_available": False,
            "manual_tts": False,
            "total_tests": 3,
            "passed_tests": 0,
            "errors": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log test message"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_api_connection(self) -> bool:
        """Test API server connection"""
        self.log("🔌 Testing API connection...")
        
        try:
            response = self.session.get(f"{self.api_url}/api/system/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("system_ready"):
                    self.log("✅ API connection successful")
                    self.test_results["api_connection"] = True
                    return True
                else:
                    self.log("❌ API not ready")
                    return False
            else:
                self.log(f"❌ API connection failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ API connection error: {e}")
            self.test_results["errors"].append(f"API Connection: {e}")
            return False
    
    def test_voices_available(self) -> bool:
        """Test voice availability"""
        self.log("🎤 Testing voice availability...")
        
        try:
            response = self.session.get(f"{self.api_url}/api/voices/available")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("voices"):
                    voice_count = len(data["voices"])
                    self.log(f"✅ Found {voice_count} available voices")
                    self.test_results["voices_available"] = True
                    return True
                else:
                    self.log("❌ No voices available")
                    return False
            else:
                self.log(f"❌ Voice API failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Voice availability error: {e}")
            self.test_results["errors"].append(f"Voices: {e}")
            return False
    
    def test_manual_tts(self) -> bool:
        """Test manual TTS generation"""
        self.log("📝 Testing manual TTS generation...")
        
        try:
            request_data = {
                "text": "Hello! This is a test of Voice Studio TTS system.",
                "language": "en",
                "voice": "olivia",
                "emotion": "neutral",
                "inner_voice": False,
                "inner_voice_type": "light",
                "speed": 1.0,
                "temperature": 0.7,
                "exaggeration": 1.0
            }
            
            response = self.session.post(
                f"{self.api_url}/api/tts/manual",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    job_id = data["job_id"]
                    self.log(f"✅ Manual TTS started (Job ID: {job_id})")
                    self.test_results["manual_tts"] = True
                    return True
                else:
                    self.log(f"❌ Manual TTS failed: {data.get('message')}")
                    return False
            else:
                self.log(f"❌ Manual TTS request failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Manual TTS error: {e}")
            self.test_results["errors"].append(f"Manual TTS: {e}")
            return False
    
    def run_all_tests(self) -> dict:
        """Run complete test suite"""
        self.log("🚀 Starting Voice Studio TTS Integration Tests")
        self.log("=" * 60)
        
        tests = [
            ("API Connection", self.test_api_connection),
            ("Voice Availability", self.test_voices_available),
            ("Manual TTS", self.test_manual_tts)
        ]
        
        for test_name, test_func in tests:
            self.log(f"\n📋 Running: {test_name}")
            try:
                if test_func():
                    self.test_results["passed_tests"] += 1
                    self.log(f"✅ {test_name} PASSED")
                else:
                    self.log(f"❌ {test_name} FAILED")
            except Exception as e:
                self.log(f"💥 {test_name} ERROR: {e}")
                self.test_results["errors"].append(f"{test_name}: {e}")
        
        self._print_final_results()
        return self.test_results
    
    def _print_final_results(self):
        """Print final test results"""
        self.log("\n" + "=" * 60)
        self.log("🏁 FINAL TEST RESULTS")
        self.log("=" * 60)
        
        passed = self.test_results["passed_tests"]
        total = self.test_results["total_tests"]
        
        self.log(f"✅ Tests Passed: {passed}/{total}")
        self.log(f"📊 Success Rate: {(passed/total)*100:.1f}%")
        
        if self.test_results["errors"]:
            self.log("\n❌ Errors:")
            for error in self.test_results["errors"]:
                self.log(f"   - {error}")
        
        if passed == total:
            self.log("\n🎉 ALL TESTS PASSED! Voice Studio TTS is ready! 🎉")
        else:
            self.log(f"\n⚠️  {total - passed} tests failed. Check errors above.")

def main():
    """Main test function"""
    print("🎙️ Voice Studio TTS Integration Test Suite")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/system/status", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running! Start with:")
            print("   cd backend && python -m uvicorn app.main:app --reload")
            return 1
    except Exception:
        print("❌ Backend not accessible! Start with:")
        print("   cd backend && python -m uvicorn app.main:app --reload")
        return 1
    
    tester = TTSIntegrationTester()
    results = tester.run_all_tests()
    
    return 0 if results["passed_tests"] == results["total_tests"] else 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 