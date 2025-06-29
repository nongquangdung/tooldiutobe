#!/usr/bin/env python3
"""
🛡️ SAFE EMOTION CONFIG IMPORT
==============================

Import emotion config an toàn với bảo vệ inner_voice_config.
Tự động phát hiện và bảo vệ thông số inner voice khỏi bị ghi đè.
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def backup_current_config():
    """Backup config hiện tại trước khi import"""
    config_path = Path("configs/emotions/unified_emotions.json")
    if config_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(f"configs/emotions/backup/unified_emotions_backup_{timestamp}.json")
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    return None

def check_inner_voice_quality(inner_voice_config):
    """Kiểm tra chất lượng inner_voice_config"""
    if not inner_voice_config.get("enabled", False):
        return "disabled"
    
    presets = inner_voice_config.get("presets", {})
    if not presets:
        return "empty"
    
    # Kiểm tra thông số có ý nghĩa không
    total_params = 0
    meaningful_params = 0
    
    for preset_name, preset in presets.items():
        for param in ["delay", "decay", "gain"]:
            total_params += 1
            if preset.get(param, 0) > 0:
                meaningful_params += 1
    
    if meaningful_params == 0:
        return "all_zero"
    elif meaningful_params < total_params * 0.5:
        return "mostly_zero"
    else:
        return "good"

def safe_import_emotion_config(import_file_path, output_file_path="configs/emotions/unified_emotions.json"):
    """Import emotion config một cách an toàn"""
    
    print("🛡️ SAFE EMOTION CONFIG IMPORT")
    print("=" * 40)
    
    # 1. Backup config hiện tại
    backup_path = backup_current_config()
    
    # 2. Load file import
    try:
        with open(import_file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        print(f"✅ Loaded import file: {import_file_path}")
    except Exception as e:
        print(f"❌ Error loading import file: {e}")
        return False
    
    # 3. Load config hiện tại
    try:
        with open(output_file_path, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f"✅ Loaded current config: {output_file_path}")
    except Exception as e:
        print(f"❌ Error loading current config: {e}")
        return False
    
    # 4. Kiểm tra inner_voice_config
    import_inner_voice = import_data.get("inner_voice_config", {})
    current_inner_voice = current_data.get("inner_voice_config", {})
    
    import_quality = check_inner_voice_quality(import_inner_voice)
    current_quality = check_inner_voice_quality(current_inner_voice)
    
    print(f"\n🔍 INNER VOICE CONFIG ANALYSIS:")
    print(f"   📁 Import file: {import_quality}")
    print(f"   💾 Current config: {current_quality}")
    
    # 5. Quyết định strategy
    preserve_current_inner_voice = False
    
    if current_quality == "good" and import_quality in ["disabled", "empty", "all_zero", "mostly_zero"]:
        preserve_current_inner_voice = True
        print(f"   🛡️ PROTECTION: Sẽ giữ inner_voice_config hiện tại (tốt hơn)")
    elif current_quality in ["disabled", "empty"] and import_quality == "good":
        print(f"   🔄 UPDATE: Sẽ dùng inner_voice_config từ file import (tốt hơn)")
    else:
        print(f"   ⚖️ NEUTRAL: Cả 2 config có chất lượng tương tự")
    
    # 6. Merge data
    merged_data = import_data.copy()
    
    if preserve_current_inner_voice:
        merged_data["inner_voice_config"] = current_inner_voice
        print(f"   ✅ Đã bảo vệ inner_voice_config hiện tại")
    
    # 7. Merge emotions (nếu có)
    if "emotions" in import_data and "emotions" in current_data:
        # Merge emotions: import + current (import override current)
        combined_emotions = current_data["emotions"].copy()
        combined_emotions.update(import_data["emotions"])
        merged_data["emotions"] = combined_emotions
        
        import_count = len(import_data["emotions"])
        current_count = len(current_data["emotions"])
        total_count = len(combined_emotions)
        
        print(f"\n🎭 EMOTIONS MERGE:")
        print(f"   📁 Import: {import_count} emotions")
        print(f"   💾 Current: {current_count} emotions")
        print(f"   🔀 Merged: {total_count} emotions")
    
    # 8. Save merged config
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved merged config to: {output_file_path}")
        
        # 9. Show summary
        print(f"\n📊 IMPORT SUMMARY:")
        print(f"   🛡️ Inner voice protected: {preserve_current_inner_voice}")
        print(f"   📁 Backup created: {backup_path}")
        print(f"   ✅ Import completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving merged config: {e}")
        
        # Restore backup if save failed
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, output_file_path)
            print(f"🔄 Restored backup due to error")
        
        return False

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python safe_import_emotion_config.py <import_file.json>")
        sys.exit(1)
    
    import_file = sys.argv[1]
    if not os.path.exists(import_file):
        print(f"❌ Import file not found: {import_file}")
        sys.exit(1)
    
    success = safe_import_emotion_config(import_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 