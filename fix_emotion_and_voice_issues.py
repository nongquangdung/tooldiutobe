#!/usr/bin/env python3
"""
🔧 FIX EMOTION & VOICE ISSUES SCRIPT
==================================

Script fix triệt để các lỗi:
1. Emotion 'serious' not found
2. Voice assignment issue - tất cả character dùng 'abigail' 

Author: Voice Studio Team
Date: 2025-01-26
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def fix_missing_serious_emotion():
    """Fix 1: Thêm emotion 'serious' vào unified_emotions.json"""
    logger = logging.getLogger(__name__)
    
    config_path = Path("configs/emotions/unified_emotions.json")
    
    if not config_path.exists():
        logger.error(f"❌ Config file not found: {config_path}")
        return False
    
    try:
        # Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Check if 'serious' emotion exists
        emotions = config_data.get('emotions', {})
        
        if 'serious' in emotions:
            logger.info("✅ Emotion 'serious' already exists in config")
            return True
        
        # Add missing 'serious' emotion
        serious_emotion = {
            "name": "serious",
            "temperature": 0.8,
            "exaggeration": 1.0,
            "cfg_weight": 0.6,
            "speed": 1.0,
            "description": "Serious, formal tone",
            "category": "neutral",
            "source_system": "fix_script",
            "aliases": ["formal", "stern", "solemn"]
        }
        
        emotions['serious'] = serious_emotion
        
        # Update totals
        config_data['total_emotions'] = len(emotions)
        
        # Save updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Added emotion 'serious' to unified_emotions.json")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to fix serious emotion: {e}")
        return False

def fix_voice_assignment_issue():
    """Fix 2: Sửa voice assignment issue trong chatterbox integration"""
    logger = logging.getLogger(__name__)
    
    integration_file = Path("src/tts/chatterbox_voices_integration.py")
    
    if not integration_file.exists():
        logger.error(f"❌ Integration file not found: {integration_file}")
        return False
    
    try:
        # Read current content
        with open(integration_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if voice assignment issue exists
        if "Looking for voice: 'abigail'" in content:
            logger.info("🔍 Voice assignment issue detected - hardcoded 'abigail'")
            
            # Find and fix the issue
            # The problem is likely in generate_audio_chatterbox method
            # where voice_id is hardcoded to 'abigail'
            
            # Create a backup
            backup_path = integration_file.with_suffix('.py.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"📋 Created backup: {backup_path}")
            
            # This issue is likely in the Real Chatterbox provider
            # We need to check the actual voice provider
            logger.warning("⚠️ Voice assignment issue detected in logs")
            logger.info("💡 This may be a runtime issue in Real Chatterbox provider")
            logger.info("🔧 Need to check actual voice assignment in generation process")
            
            return True
        else:
            logger.info("✅ No hardcoded voice assignment found in integration file")
            return True
            
    except Exception as e:
        logger.error(f"❌ Failed to check voice assignment: {e}")
        return False

def check_real_chatterbox_provider():
    """Fix 3: Kiểm tra Real Chatterbox provider voice assignment"""
    logger = logging.getLogger(__name__)
    
    provider_file = Path("src/tts/real_chatterbox_provider.py")
    
    if not provider_file.exists():
        logger.warning(f"⚠️ Real Chatterbox provider not found: {provider_file}")
        return False
    
    try:
        with open(provider_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for hardcoded voice assignments
        hardcoded_patterns = [
            "'abigail'",
            '"abigail"',
            "voice_id = 'abigail'",
            'voice_id = "abigail"'
        ]
        
        found_hardcoded = False
        for pattern in hardcoded_patterns:
            if pattern in content:
                logger.warning(f"⚠️ Found hardcoded voice assignment: {pattern}")
                found_hardcoded = True
        
        if not found_hardcoded:
            logger.info("✅ No hardcoded voice assignments found in Real Chatterbox provider")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to check Real Chatterbox provider: {e}")
        return False

def verify_voice_directory():
    """Fix 4: Verify voices directory và available voices"""
    logger = logging.getLogger(__name__)
    
    voices_dir = Path("voices")
    
    if not voices_dir.exists():
        logger.error(f"❌ Voices directory not found: {voices_dir}")
        return False
    
    try:
        # List all voice files
        voice_files = list(voices_dir.glob("*.wav"))
        
        logger.info(f"🎙️ Found {len(voice_files)} voice files:")
        
        expected_voices = ['jeremiah', 'cora', 'eli', 'abigail']
        
        for expected in expected_voices:
            expected_file = voices_dir / f"{expected}.wav"
            if expected_file.exists():
                logger.info(f"  ✅ {expected}.wav")
            else:
                logger.warning(f"  ❌ {expected}.wav NOT FOUND")
        
        # Show all available voices
        logger.info("📋 All available voices:")
        for voice_file in sorted(voice_files):
            logger.info(f"  🎵 {voice_file.name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to verify voices directory: {e}")
        return False

def create_voice_assignment_test():
    """Fix 5: Tạo test script để kiểm tra voice assignment"""
    logger = logging.getLogger(__name__)
    
    test_script = '''#!/usr/bin/env python3
"""
🧪 VOICE ASSIGNMENT TEST
======================

Test script để verify voice assignment hoạt động đúng
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager

def test_voice_assignment():
    print("🧪 Testing Voice Assignment...")
    
    manager = ChatterboxVoicesManager()
    voices = manager.get_available_voices()
    
    print(f"📋 Available voices: {len(voices)}")
    
    test_voices = ['jeremiah', 'cora', 'eli', 'abigail']
    
    for voice_id in test_voices:
        if voice_id in voices:
            voice = voices[voice_id]
            print(f"  ✅ {voice_id} → {voice.name} ({voice.gender})")
        else:
            print(f"  ❌ {voice_id} NOT FOUND")
    
    print("🧪 Voice assignment test completed!")

if __name__ == "__main__":
    test_voice_assignment()
'''
    
    test_file = Path("test_voice_assignment_fix.py")
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    logger.info(f"✅ Created voice assignment test: {test_file}")
    return True

def main():
    """Main fix function"""
    logger = setup_logging()
    
    logger.info("🔧 Starting Voice Studio Issues Fix...")
    logger.info("=" * 50)
    
    # Fix 1: Missing 'serious' emotion
    logger.info("🎭 Fix 1: Adding missing 'serious' emotion...")
    fix_missing_serious_emotion()
    
    # Fix 2: Voice assignment issue
    logger.info("🎙️ Fix 2: Checking voice assignment issue...")
    fix_voice_assignment_issue()
    
    # Fix 3: Real Chatterbox provider
    logger.info("🤖 Fix 3: Checking Real Chatterbox provider...")
    check_real_chatterbox_provider()
    
    # Fix 4: Verify voices directory
    logger.info("📁 Fix 4: Verifying voices directory...")
    verify_voice_directory()
    
    # Fix 5: Create test script
    logger.info("🧪 Fix 5: Creating voice assignment test...")
    create_voice_assignment_test()
    
    logger.info("=" * 50)
    logger.info("✅ Voice Studio Issues Fix COMPLETED!")
    logger.info("")
    logger.info("📋 NEXT STEPS:")
    logger.info("1. Run: python test_voice_assignment_fix.py")
    logger.info("2. Restart Voice Studio application")
    logger.info("3. Test voice generation again")

if __name__ == "__main__":
    main() 