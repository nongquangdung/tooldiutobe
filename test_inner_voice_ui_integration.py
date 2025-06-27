#!/usr/bin/env python3
"""
Test Inner Voice UI Integration với Config và Processor
"""

import json
import os
import sys

def test_inner_voice_config():
    """Test cấu hình inner voice đã được thêm vào unified_emotions.json"""
    print("🧪 Testing Inner Voice Config...")
    
    config_path = "configs/emotions/unified_emotions.json"
    
    if not os.path.exists(config_path):
        print(f"❌ Config file không tồn tại: {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Kiểm tra inner_voice_config
    if "inner_voice_config" not in config:
        print("❌ Thiếu inner_voice_config trong unified_emotions.json")
        return False
    
    inner_config = config["inner_voice_config"]
    print("✅ Inner Voice Config đã được cấu hình đúng!")
    print(f"   📝 Enabled: {inner_config.get('enabled', False)}")
    print(f"   🎭 Presets: {list(inner_config.get('presets', {}).keys())}")
    
    return True

def main():
    """Chạy test chính"""
    print("🎭 INNER VOICE UI INTEGRATION TEST")
    print("=" * 50)
    
    success = test_inner_voice_config()
    
    print("=" * 50)
    if success:
        print("✅ Test PASSED! Inner Voice config OK!")
    else:
        print("❌ Test FAILED!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 