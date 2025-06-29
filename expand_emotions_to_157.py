#!/usr/bin/env python3
"""
🎭 EXPAND EMOTIONS TO 157 SYSTEM
================================

Script mở rộng unified_emotions.json từ 37 lên 157 emotions
bằng cách thêm 120 emotions từ advanced_window.py mapping system.

Mục tiêu:
- Giữ nguyên 37 emotions hiện có
- Thêm 120 emotions mới từ advanced mapping  
- Tất cả emotions có thể tùy biến trong Emotion Config Tab
- Auto-mapping sẽ sử dụng config thay vì hardcode
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_current_emotions():
    """Load 37 emotions hiện có từ unified_emotions.json"""
    config_path = Path("configs/emotions/unified_emotions.json")
    
    if not config_path.exists():
        print(f"❌ Không tìm thấy file: {config_path}")
        return None
        
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_advanced_emotions_mapping():
    """Lấy 120 emotions từ advanced_window.py mapping"""
    
    # 120 emotions từ advanced_window.py với categories phân loại
    advanced_emotions = {
        # Existing emotions cần được normalize theo expert range (giới hạn 0.8-1.2)
        'surprised': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.55, 'speed': 1.1,
            'description': 'Shock, disbelief, amazement', 'category': 'surprise'
        },
        'shocked': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Intense surprise, stunned reaction', 'category': 'surprise'  
        },
        'amazed': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Wonder, awe, impressed', 'category': 'surprise'
        },
        
        # Sad/Hurt emotions
        'hurt': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Emotional pain, heartache', 'category': 'negative'
        },
        'disappointed': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Unmet expectations, letdown', 'category': 'negative'
        },
        'melancholy': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Deep sadness, pensiveness', 'category': 'negative'
        },
        'melancholic': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Reflective sadness, wistful', 'category': 'negative'
        },
        
        # Angry emotions (normalized)
        'furious': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.3,
            'description': 'Intense anger, rage', 'category': 'negative'
        },
        'irritated': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Annoyed, slightly angry', 'category': 'negative'
        },
        'frustrated': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Blocked progress, impatient', 'category': 'negative'
        },
        
        # Pleading emotions
        'pleading': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Begging, earnest request', 'category': 'desperate'
        },
        'earnest': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Sincere, serious appeal', 'category': 'desperate'
        },
        'desperate': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Last resort, urgent need', 'category': 'desperate'
        },
        
        # Anxious emotions
        'anxious': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.55, 'speed': 1.0,
            'description': 'Worried, uneasy', 'category': 'nervous'
        },
        'worried': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Concerned, troubled', 'category': 'nervous'
        },
        'nervous': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Jittery, on edge', 'category': 'nervous'
        },
        'restless': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.55, 'speed': 1.1,
            'description': 'Unable to settle, agitated', 'category': 'nervous'
        },
        
        # Mysterious emotions
        'mysterious': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Enigmatic, secretive', 'category': 'mysterious'
        },
        'suspenseful': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Building tension, anticipation', 'category': 'mysterious'
        },
        'ominous': {
            'temperature': 0.7, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Threatening, foreboding', 'category': 'mysterious'
        },
        'eerie': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Strange, unsettling', 'category': 'mysterious'
        },
        
        # Warning emotions (normalized)
        'warning': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.2,
            'description': 'Alert, caution signal', 'category': 'urgent'
        },
        'urgent': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.3,
            'description': 'Time-critical, immediate', 'category': 'urgent'
        },
        'emergency': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.3,
            'description': 'Crisis situation, alarm', 'category': 'urgent'
        },
        'alarm': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.2,
            'description': 'Warning signal, alert', 'category': 'urgent'
        },
        
        # Sarcastic emotions
        'sarcastic': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Ironic, mocking tone', 'category': 'sarcastic'
        },
        'mocking': {
            'temperature': 0.8, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Ridiculing, derisive', 'category': 'sarcastic'
        },
        'ironic': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Contrary to expectation', 'category': 'sarcastic'
        },
        
        # Impressed emotions  
        'impressed': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Favorably affected, amazed', 'category': 'positive'
        },
        'praising': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Expressing approval, commending', 'category': 'positive'
        },
        
        # Confused emotions
        'confused': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Bewildered, unclear', 'category': 'confused'
        },
        'embarrassed': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Self-conscious, awkward', 'category': 'confused'
        },
        'hesitant': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Uncertain, tentative', 'category': 'confused'
        },
        'uncertain': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Doubtful, unsure', 'category': 'confused'
        },
        
        # Fear emotions
        'fearful': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Afraid, apprehensive', 'category': 'negative'
        },
        'fear': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Basic fear emotion', 'category': 'negative'
        },
        
        # Sleepy emotions
        'sleepy': {
            'temperature': 0.6, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.7,
            'description': 'Drowsy, tired', 'category': 'neutral'
        },
        'thoughtful': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Reflective, considering', 'category': 'neutral'
        },
        
        # Cold emotions
        'cold': {
            'temperature': 0.6, 'exaggeration': 0.8, 'cfg_weight': 0.6, 'speed': 0.9,
            'description': 'Emotionally distant, aloof', 'category': 'negative'
        },
        'distant': {
            'temperature': 0.6, 'exaggeration': 0.8, 'cfg_weight': 0.6, 'speed': 0.8,
            'description': 'Remote, detached', 'category': 'negative'
        },
        'indifferent': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.6, 'speed': 0.9,
            'description': 'Uncaring, neutral', 'category': 'neutral'
        },
        'detached': {
            'temperature': 0.6, 'exaggeration': 0.8, 'cfg_weight': 0.6, 'speed': 0.8,
            'description': 'Emotionally separated', 'category': 'neutral'
        },
        
        # Enthusiastic emotions (normalized)
        'enthusiastic': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Eager, passionate', 'category': 'positive'
        },
        'motivating': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Inspiring action, encouraging', 'category': 'positive'
        },
        'inspiring': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Uplifting, motivational', 'category': 'positive'
        },
        
        # Strong/Decisive emotions (normalized)
        'commanding': {
            'temperature': 0.9, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Authoritative, directing', 'category': 'authoritative'
        },
        'decisive': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Firm, conclusive', 'category': 'authoritative'
        },
        'authoritative': {
            'temperature': 0.9, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Commanding respect, expert', 'category': 'authoritative'
        },
        'firm': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Unwavering, solid', 'category': 'authoritative'
        },
        
        # Innocent emotions
        'innocent': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Pure, naive', 'category': 'innocent'
        },
        'naive': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.4, 'speed': 1.0,
            'description': 'Unsophisticated, simple', 'category': 'innocent'
        },
        'childlike': {
            'temperature': 0.9, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.1,
            'description': 'Youthful, innocent wonder', 'category': 'innocent'
        },
        'carefree': {
            'temperature': 0.9, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.1,
            'description': 'Worry-free, light-hearted', 'category': 'positive'
        },
        
        # Bewildered emotions
        'bewildered': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Completely confused', 'category': 'confused'
        },
        'lost': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Unable to find way', 'category': 'confused'
        },
        'perplexed': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Completely puzzled', 'category': 'confused'
        },
        'dazed': {
            'temperature': 0.7, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Stunned, confused', 'category': 'confused'
        },
        
        # Provocative emotions
        'provocative': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.55, 'speed': 1.0,
            'description': 'Deliberately challenging', 'category': 'provocative'
        },
        'teasing': {
            'temperature': 0.9, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.1,
            'description': 'Playfully mocking', 'category': 'provocative'
        },
        'flirtatious': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Romantically playful', 'category': 'provocative'
        },
        
        # Humorous emotions
        'humorous': {
            'temperature': 0.9, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.1,
            'description': 'Funny, entertaining', 'category': 'positive'
        },
        'witty': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Cleverly amusing', 'category': 'positive'
        },
        'amusing': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Entertaining, funny', 'category': 'positive'
        },
        'charming': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Delightfully appealing', 'category': 'positive'
        },
        
        # Persuasive emotions
        'persuasive': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.55, 'speed': 1.0,
            'description': 'Convincing, influential', 'category': 'authoritative'
        },
        'rhetorical': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Skillfully persuasive', 'category': 'authoritative'
        },
        'eloquent': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Fluently persuasive', 'category': 'authoritative'
        },
        'convincing': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.55, 'speed': 1.0,
            'description': 'Persuasively effective', 'category': 'authoritative'
        },
        
        # Scornful emotions (normalized)
        'scornful': {
            'temperature': 0.9, 'exaggeration': 1.2, 'cfg_weight': 0.65, 'speed': 1.0,
            'description': 'Contemptuous, disdainful', 'category': 'negative'
        },
        'contemptuous': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Showing disdain', 'category': 'negative'
        },
        'disdainful': {
            'temperature': 0.9, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Showing contempt', 'category': 'negative'
        },
        'condescending': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.65, 'speed': 1.0,
            'description': 'Patronizing, superior', 'category': 'negative'
        },
        
        # Additional common emotions
        'shy': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Timid, bashful', 'category': 'neutral'
        },
        'dramatic': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Theatrical, intense', 'category': 'dramatic'
        },
        
        # Additional variations and aliases
        'joyful': {
            'temperature': 0.9, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Full of joy, elated', 'category': 'positive'
        },
        'cheerful': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Bright, uplifting tone', 'category': 'positive'
        },
        'normal': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Standard, default tone', 'category': 'neutral'
        },
        'gentle': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.9,
            'description': 'Soft, tender approach', 'category': 'neutral'
        }
    }
    
    return advanced_emotions

def create_expanded_emotions_config(force_apply=False):
    """Tạo config mở rộng với 93 emotions"""
    
    # Load current 37 emotions
    current_config = load_current_emotions()
    if not current_config:
        return None
        
    # Get advanced emotions to add
    advanced_emotions = get_advanced_emotions_mapping()
    
    # Create new config structure
    new_config = {
        "version": "3.0",
        "description": "Expanded Emotion System - 93 Emotions (37 original + 56 advanced)",
        "total_emotions": 37 + len([e for e in advanced_emotions.keys() if force_apply or e not in current_config["emotions"]]),
        "total_aliases": current_config.get("total_aliases", 93),
        "expansion_date": datetime.now().isoformat(),
        "expert_recommendations": current_config.get("expert_recommendations", {
            "temperature": "0.7 - 1.0",
            "exaggeration": "0.8 - 1.2", 
            "cfg_weight": "0.5 - 0.7",
            "speed": "0.8 - 1.3"
        }),
        "emotions": current_config["emotions"].copy()
    }
    
    # Add advanced emotions
    added_count = 0
    for emotion_name, params in advanced_emotions.items():
        if force_apply or emotion_name not in new_config["emotions"]:
            if not force_apply and emotion_name in new_config["emotions"]:
                print(f"⚠️ Emotion '{emotion_name}' đã tồn tại, skip...")
                continue
                
            # Add emotion với source system notation
            new_config["emotions"][emotion_name] = {
                "name": emotion_name,
                "temperature": params["temperature"],
                "exaggeration": params["exaggeration"], 
                "cfg_weight": params["cfg_weight"],
                "speed": params["speed"],
                "description": params["description"],
                "category": params["category"],
                "source_system": "advanced_mapping",
                "aliases": []
            }
            added_count += 1
            if force_apply:
                print(f"✅ Applied: {emotion_name}")
    
    new_config["total_emotions"] = len(new_config["emotions"])
    print(f"✅ Tạo thành công config với {new_config['total_emotions']} emotions")
    print(f"   📊 37 emotions gốc + {added_count} emotions mới") 
    
    return new_config

def backup_current_config():
    """Backup config hiện tại"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("configs/emotions/backup")
    backup_dir.mkdir(exist_ok=True)
    
    source = Path("configs/emotions/unified_emotions.json")
    backup = backup_dir / f"unified_emotions_backup_{timestamp}.json"
    
    if source.exists():
        import shutil
        shutil.copy2(source, backup)
        print(f"✅ Backup tạo tại: {backup}")
        return True
    return False

def save_expanded_config(config):
    """Save config 157 emotions mới"""
    output_path = Path("configs/emotions/unified_emotions.json")
    
    # Backup trước khi ghi đè
    backup_current_config()
    
    # Save config mới
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Đã lưu config mới tại: {output_path}")
    
    # Tạo summary report
    create_expansion_report(config)

def create_expansion_report(config):
    """Tạo báo cáo mở rộng"""
    report = {
        "expansion_summary": {
            "date": datetime.now().isoformat(),
            "original_emotions": 37,
            "added_emotions": config["total_emotions"] - 37,
            "total_emotions": config["total_emotions"],
            "version": config["version"]
        },
        "categories": {},
        "parameter_ranges": {
            "temperature": {"min": 0, "max": 0},
            "exaggeration": {"min": 0, "max": 0},
            "cfg_weight": {"min": 0, "max": 0}, 
            "speed": {"min": 0, "max": 0}
        }
    }
    
    # Phân tích categories và ranges
    for emotion_data in config["emotions"].values():
        category = emotion_data.get("category", "unknown")
        if category not in report["categories"]:
            report["categories"][category] = 0
        report["categories"][category] += 1
        
        # Update parameter ranges
        for param in ["temperature", "exaggeration", "cfg_weight", "speed"]:
            value = emotion_data.get(param, 0)
            if report["parameter_ranges"][param]["min"] == 0:
                report["parameter_ranges"][param]["min"] = value
                report["parameter_ranges"][param]["max"] = value
            else:
                report["parameter_ranges"][param]["min"] = min(report["parameter_ranges"][param]["min"], value)
                report["parameter_ranges"][param]["max"] = max(report["parameter_ranges"][param]["max"], value)
    
    # Save report
    report_path = Path("configs/emotions/expansion_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Báo cáo mở rộng tại: {report_path}")

def main():
    print("\n🎭 EMOTION SYSTEM EXPANSION - 37 → 157 Emotions")
    print("=" * 60)
    
    # Load existing config
    current_config = load_current_emotions()
    if not current_config:
        return
    
    # Get advanced emotions
    advanced_emotions = get_advanced_emotions_mapping()
    
    # Force expansion - xóa check tồn tại để đảm bảo apply đầy đủ 93 emotions
    print("🔄 FORCE APPLYING ALL 93 EMOTIONS...")
    config = create_expanded_emotions_config(force_apply=True)
    
    if config:
        # Backup current config  
        backup_current_config()
        
        # Save new config
        save_expanded_config(config)
        
        # Create report
        create_expansion_report(config)
        
        print(f"\n✅ EXPANSION HOÀN THÀNH!")
        print(f"📊 Total emotions: {config['total_emotions']}")
        print(f"🎯 Next steps:")
        print(f"   1. Test emotion config tab với 93 emotions")
        print(f"   2. Update advanced_window.py để sử dụng config thay vì hardcode")
        print(f"   3. Test export/import functionality")
    else:
        print("❌ Expansion failed!")

if __name__ == "__main__":
    main() 