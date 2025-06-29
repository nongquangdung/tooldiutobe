#!/usr/bin/env python3
"""
🎭 FORCE APPLY 93 EMOTIONS
==========================

Script force apply 93 emotions trực tiếp vào unified_emotions.json
để đảm bảo Emotion Config Tab có đầy đủ 93 emotions.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_37_emotions():
    """Load 37 emotions từ backup"""
    backup_path = "configs/emotions/unified_emotions_37_backup.json"
    
    if os.path.exists(backup_path):
        with open(backup_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Fallback to current config
    config_path = "configs/emotions/unified_emotions.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_56_additional_emotions():
    """Get 56 emotions bổ sung để lên 93 total"""
    
    additional_emotions = {
        # Surprise emotions
        'shocked': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Intense surprise, stunned reaction', 'category': 'surprise'
        },
        'amazed': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Wonder, awe, impressed', 'category': 'surprise'
        },
        'stunned': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Completely surprised, speechless', 'category': 'surprise'
        },
        
        # Negative emotions
        'hurt': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Emotional pain, heartache', 'category': 'negative'
        },
        'melancholy': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Deep sadness, pensiveness', 'category': 'negative'
        },
        'melancholic': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Reflective sadness, wistful', 'category': 'negative'
        },
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
        'disgusted': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Strong distaste, revulsion', 'category': 'negative'
        },
        
        # Desperate emotions
        'earnest': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Sincere, serious appeal', 'category': 'desperate'
        },
        'desperate': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Last resort, urgent need', 'category': 'desperate'
        },
        'begging': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Imploring, asking desperately', 'category': 'desperate'
        },
        
        # Nervous emotions
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
        'paranoid': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Suspicious, fearful of threats', 'category': 'nervous'
        },
        
        # Mysterious emotions
        'ominous': {
            'temperature': 0.7, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Threatening, foreboding', 'category': 'mysterious'
        },
        'eerie': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Strange, unsettling', 'category': 'mysterious'
        },
        'cryptic': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Hidden meaning, puzzling', 'category': 'mysterious'
        },
        
        # Urgent emotions
        'warning': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.2,
            'description': 'Alert, caution signal', 'category': 'urgent'
        },
        'emergency': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.3,
            'description': 'Crisis situation, alarm', 'category': 'urgent'
        },
        'alarm': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.2,
            'description': 'Warning signal, alert', 'category': 'urgent'
        },
        'critical': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.7, 'speed': 1.3,
            'description': 'Extremely important, crucial', 'category': 'urgent'
        },
        
        # Sarcastic emotions
        'mocking': {
            'temperature': 0.8, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Ridiculing, derisive', 'category': 'sarcastic'
        },
        'ironic': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Contrary to expectation', 'category': 'sarcastic'
        },
        'cynical': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Skeptical, distrusting', 'category': 'sarcastic'
        },
        
        # Positive emotions
        'impressed': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Favorably affected, amazed', 'category': 'positive'
        },
        'praising': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Expressing approval, commending', 'category': 'positive'
        },
        'enthusiastic': {
            'temperature': 1.0, 'exaggeration': 1.2, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Highly excited, passionate', 'category': 'positive'
        },
        'delighted': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Greatly pleased, joyful', 'category': 'positive'
        },
        'grateful': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Thankful, appreciative', 'category': 'positive'
        },
        'optimistic': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Hopeful, positive outlook', 'category': 'positive'
        },
        'proud': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Feeling satisfied with achievement', 'category': 'positive'
        },
        
        # Confused emotions
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
        'perplexed': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Completely puzzled, baffled', 'category': 'confused'
        },
        'doubtful': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Questioning, uncertain', 'category': 'confused'
        },
        'puzzled': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Confused, trying to understand', 'category': 'confused'
        },
        
        # Authoritative emotions
        'commanding': {
            'temperature': 0.8, 'exaggeration': 1.1, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Authoritative, in control', 'category': 'authoritative'
        },
        'dominant': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.7, 'speed': 1.0,
            'description': 'Controlling, assertive', 'category': 'authoritative'
        },
        'demanding': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.7, 'speed': 1.1,
            'description': 'Insisting, requiring', 'category': 'authoritative'
        },
        'stern': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 0.9,
            'description': 'Serious, strict', 'category': 'authoritative'
        },
        'firm': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 0.9,
            'description': 'Resolute, determined', 'category': 'authoritative'
        },
        'assertive': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 1.0,
            'description': 'Confident, direct', 'category': 'authoritative'
        },
        
        # Innocent emotions
        'naive': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Simple, unsophisticated', 'category': 'innocent'
        },
        'childlike': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Pure, simple wonder', 'category': 'innocent'
        },
        
        # Special emotions
        'dreamy': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Ethereal, otherworldly', 'category': 'special'
        },
        'mystical': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Spiritual, transcendent', 'category': 'special'
        },
        'ethereal': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.4, 'speed': 0.8,
            'description': 'Heavenly, otherworldly', 'category': 'special'
        },
        'hypnotic': {
            'temperature': 0.7, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 0.8,
            'description': 'Mesmerizing, entrancing', 'category': 'special'
        },
        'seductive': {
            'temperature': 0.8, 'exaggeration': 1.0, 'cfg_weight': 0.6, 'speed': 0.9,
            'description': 'Alluring, enticing', 'category': 'special'
        },
        
        # Fear-based emotions  
        'fear': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Basic fear emotion', 'category': 'negative'
        },
        'terrified': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.2,
            'description': 'Extremely frightened', 'category': 'negative'
        },
        'horrified': {
            'temperature': 0.9, 'exaggeration': 1.1, 'cfg_weight': 0.6, 'speed': 1.1,
            'description': 'Filled with horror', 'category': 'negative'
        },
        
        # Neutral variants
        'matter_of_fact': {
            'temperature': 0.7, 'exaggeration': 0.8, 'cfg_weight': 0.5, 'speed': 0.9,
            'description': 'Straightforward, factual', 'category': 'neutral'
        },
        'informative': {
            'temperature': 0.8, 'exaggeration': 0.9, 'cfg_weight': 0.5, 'speed': 1.0,
            'description': 'Educational, explaining', 'category': 'neutral'
        }
    }
    
    return additional_emotions

def create_93_emotions_config():
    """Tạo config với đầy đủ 93 emotions"""
    
    print("🔄 Creating 93 emotions config...")
    
    # Load 37 base emotions
    base_config = load_37_emotions()
    print(f"✅ Loaded {len(base_config['emotions'])} base emotions")
    
    # Get 56 additional emotions
    additional_emotions = get_56_additional_emotions()
    print(f"✅ Prepared {len(additional_emotions)} additional emotions")
    
    # Create new config
    new_config = {
        "version": "3.0",
        "description": "Unified Emotion System - 93 Emotions (37 original + 56 advanced)",
        "total_emotions": 93,
        "total_aliases": base_config.get("total_aliases", 93) + len(additional_emotions) * 2,
        "expansion_date": datetime.now().isoformat(),
        "expert_recommendations": {
            "temperature": "0.7 - 1.0",
            "exaggeration": "0.8 - 1.2",
            "cfg_weight": "0.5 - 0.7", 
            "speed": "0.8 - 1.3"
        },
        "emotions": base_config["emotions"].copy()
    }
    
    # Add additional emotions
    for emotion_name, params in additional_emotions.items():
        new_config["emotions"][emotion_name] = {
            "name": emotion_name,
            "temperature": params["temperature"],
            "exaggeration": params["exaggeration"],
            "cfg_weight": params["cfg_weight"], 
            "speed": params["speed"],
            "description": params["description"],
            "category": params["category"],
            "source_system": "expansion_93",
            "aliases": []
        }
        print(f"   ✅ Added: {emotion_name}")
    
    # Verify count
    actual_count = len(new_config["emotions"])
    new_config["total_emotions"] = actual_count
    
    print(f"✅ Created config with {actual_count} emotions")
    return new_config

def save_93_emotions_config(config):
    """Save config với 93 emotions"""
    
    # Backup current config
    config_path = "configs/emotions/unified_emotions.json"
    backup_path = f"configs/emotions/backup/unified_emotions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Backup saved: {backup_path}")
    
    # Save new config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ New config saved: {config_path}")
    
    return True

def main():
    """Main execution"""
    
    print("🎭 FORCE APPLY 93 EMOTIONS")
    print("=" * 50)
    
    try:
        # Create 93 emotions config
        config = create_93_emotions_config()
        
        # Save config
        save_93_emotions_config(config)
        
        print(f"\n🎉 SUCCESS! 93 EMOTIONS APPLIED!")
        print(f"   📊 Total emotions: {config['total_emotions']}")
        print(f"   📊 Actual count: {len(config['emotions'])}")
        print(f"   📅 Updated: {config['expansion_date']}")
        
        print(f"\n🎯 EMOTION CONFIG TAB SẴN SÀNG!")
        print(f"   ✅ Bảng sẽ hiển thị đầy đủ 93 emotions")
        print(f"   ✅ Có thể tùy chỉnh tất cả parameters")
        print(f"   ✅ Export/Import với 93 emotions")
        print(f"   ✅ Add custom emotions mới")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 