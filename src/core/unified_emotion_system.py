#!/usr/bin/env python3
"""
[THEATER] UNIFIED EMOTION SYSTEM
=========================

HỆ THỐNG EMOTION THỐNG NHẤT - Gộp và chuẩn hóa từ 3 hệ thống cũ:
1. 93 UI Mapping Labels (advanced_window.py)
2. 8 Basic Chatterbox Emotions (chatterbox_voices_integration.py)  
3. 28 Core Emotions (emotion_config_manager.py)

THÔNG SỐ CHUẨN (theo khuyến nghị chuyên gia):
- Temperature: 0.7 - 1.0 (cho giọng tự nhiên)
- Exaggeration: 0.8 - 1.2 (cho biểu cảm mạnh)
- CFG Weight: 0.5 - 0.7 (cân bằng trung thành/biểu cảm)
- Speed: 0.8 - 1.3 (tốc độ nói phù hợp)

Author: Voice Studio Team
Version: 2.0 - Unified System
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import copy

logger = logging.getLogger(__name__)

@dataclass
class UnifiedEmotionParameters:
    """Unified emotion parameters - 4 thông số chuẩn"""
    name: str
    temperature: float = 0.8    # 0.7-1.0 (creativity/variability)
    exaggeration: float = 1.0   # 0.8-1.2 (emotion intensity) 
    cfg_weight: float = 0.6     # 0.5-0.7 (voice guidance strength)
    speed: float = 1.0          # 0.8-1.3 (speaking speed)
    description: str = ""
    category: str = "neutral"   # neutral, positive, negative, dramatic, special
    source_system: str = ""     # track nguồn gốc
    aliases: List[str] = None   # các tên khác cho cùng emotion

    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []

class UnifiedEmotionSystem:
    """
    [TARGET] HỆ THỐNG EMOTION THỐNG NHẤT
    
    Gộp tất cả emotions từ 3 hệ thống cũ và chuẩn hóa theo khuyến nghị tối ưu:
    - Loại bỏ duplicate emotions
    - Áp dụng thông số theo expert recommendations  
    - Tạo mapping system cho backward compatibility
    - Cung cấp API thống nhất cho toàn bộ hệ thống
    """
    
    def __init__(self, config_dir: str = "configs/emotions"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.unified_emotions: Dict[str, UnifiedEmotionParameters] = {}
        self.emotion_aliases: Dict[str, str] = {}

        # === Load from file if exists ===
        config_file = self.config_dir / "unified_emotions.json"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # Check if file is not empty
                        data = json.loads(content)
                        for name, params in data.get("emotions", {}).items():
                            self.unified_emotions[name] = UnifiedEmotionParameters(**params)
                        self.emotion_aliases = data.get("aliases", {})
                    else:
                        # File is empty, recreate
                        raise ValueError("Empty config file")
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"[WARNING] Error loading emotion config: {e}")
                print("[INFO] Recreating emotion config...")
                self.create_unified_emotion_database()
                self.generate_backward_compatibility_mapping()
                self.save_unified_config()
        else:
            self.create_unified_emotion_database()
            self.generate_backward_compatibility_mapping()
            self.save_unified_config()
    
    def create_unified_emotion_database(self):
        """Tạo database emotion thống nhất từ 3 hệ thống cũ"""
        
        # ================================================================
        # [THEATER] MASTER EMOTION DATABASE - 101+ Emotions Unified
        # Áp dụng khuyến nghị tối ưu: temp=0.7-1.0, exag=0.8-1.2, cfg=0.5-0.7, speed=0.8-1.3
        # ================================================================
        
        unified_emotions_data = [
            
            # ===== NEUTRAL EMOTIONS (Cảm xúc trung tính) =====
            UnifiedEmotionParameters(
                name="neutral", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.0,
                description="Balanced, objective narration", category="neutral",
                source_system="core+ui+chatterbox", aliases=["normal", "balanced"]
            ),
            UnifiedEmotionParameters(
                name="calm", temperature=0.7, exaggeration=0.9, cfg_weight=0.5, speed=0.9,
                description="Peaceful, composed speech", category="neutral", 
                source_system="core+ui+chatterbox", aliases=["peaceful", "composed"]
            ),
            UnifiedEmotionParameters(
                name="contemplative", temperature=0.8, exaggeration=0.9, cfg_weight=0.5, speed=0.8,
                description="Deep inner thoughts", category="neutral",
                source_system="core+ui", aliases=["thoughtful", "meditative"]
            ),
            UnifiedEmotionParameters(
                name="soft", temperature=0.7, exaggeration=0.8, cfg_weight=0.5, speed=0.9,
                description="Gentle, tender expressions", category="neutral",
                source_system="ui", aliases=["gentle", "tender"]
            ),
            UnifiedEmotionParameters(
                name="whisper", temperature=0.7, exaggeration=0.8, cfg_weight=0.5, speed=0.8,
                description="Intimate, secretive tone", category="neutral",
                source_system="core+ui+chatterbox", aliases=["secret", "intimate"]
            ),
            
            # ===== POSITIVE EMOTIONS (Cảm xúc tích cực) =====
            UnifiedEmotionParameters(
                name="happy", temperature=0.9, exaggeration=1.2, cfg_weight=0.6, speed=1.1,
                description="General joy, positive mood", category="positive",
                source_system="core+ui+chatterbox", aliases=["joyful", "pleased"]
            ),
            UnifiedEmotionParameters(
                name="excited", temperature=1.0, exaggeration=1.2, cfg_weight=0.6, speed=1.3,
                description="High energy, enthusiastic", category="positive",
                source_system="core+ui+chatterbox", aliases=["energetic", "thrilled"]
            ),
            UnifiedEmotionParameters(
                name="cheerful", temperature=0.9, exaggeration=1.1, cfg_weight=0.6, speed=1.1,
                description="Bright, uplifting tone", category="positive",
                source_system="ui", aliases=["bright", "uplifting"]
            ),
            UnifiedEmotionParameters(
                name="friendly", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.0,
                description="Warm, welcoming tone", category="positive",
                source_system="core+ui", aliases=["warm", "welcoming"]
            ),
            UnifiedEmotionParameters(
                name="confident", temperature=0.8, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Self-assured, determined", category="positive",
                source_system="core+ui", aliases=["assured", "determined"]
            ),
            UnifiedEmotionParameters(
                name="encouraging", temperature=0.9, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Inspiring, motivating", category="positive",
                source_system="ui", aliases=["motivating", "inspiring", "enthusiastic"]
            ),
            UnifiedEmotionParameters(
                name="admiring", temperature=0.8, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Genuine praise, impressed", category="positive",
                source_system="ui", aliases=["impressed", "praising"]
            ),
            UnifiedEmotionParameters(
                name="playful", temperature=0.9, exaggeration=1.1, cfg_weight=0.6, speed=1.1,
                description="Fun, teasing tone", category="positive",
                source_system="ui", aliases=["teasing", "mischievous"]
            ),
            UnifiedEmotionParameters(
                name="romantic", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=0.9,
                description="Loving, tender expressions", category="positive",
                source_system="ui", aliases=["loving", "affectionate"]
            ),
            UnifiedEmotionParameters(
                name="innocent", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.0,
                description="Childlike, naive expression", category="positive",
                source_system="core+ui", aliases=["naive", "childlike", "carefree"]
            ),
            
            # ===== NEGATIVE EMOTIONS (Cảm xúc tiêu cực) =====
            UnifiedEmotionParameters(
                name="sad", temperature=0.7, exaggeration=0.9, cfg_weight=0.5, speed=0.8,
                description="General sadness, melancholy", category="negative",
                source_system="core+ui+chatterbox", aliases=["melancholy", "melancholic", "hurt"]
            ),
            UnifiedEmotionParameters(
                name="angry", temperature=0.9, exaggeration=1.2, cfg_weight=0.7, speed=1.2,
                description="General anger, irritation", category="negative",
                source_system="core+ui+chatterbox", aliases=["furious", "irritated", "frustrated"]
            ),
            UnifiedEmotionParameters(
                name="sarcastic", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.1,
                description="Mocking, ironic tone", category="negative",
                source_system="core+ui", aliases=["mocking", "ironic"]
            ),
            UnifiedEmotionParameters(
                name="disappointed", temperature=0.7, exaggeration=0.9, cfg_weight=0.5, speed=0.9,
                description="Let down, dissatisfied", category="negative",
                source_system="ui", aliases=["dissatisfied", "letdown"]
            ),
            UnifiedEmotionParameters(
                name="anxious", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.1,
                description="Worried, underlying tension", category="negative",
                source_system="ui", aliases=["worried", "nervous", "restless"]
            ),
            UnifiedEmotionParameters(
                name="fearful", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.0,
                description="Afraid, scared expressions", category="negative",
                source_system="ui", aliases=["afraid", "scared", "fear"]
            ),
            UnifiedEmotionParameters(
                name="confused", temperature=0.8, exaggeration=0.9, cfg_weight=0.6, speed=0.9,
                description="Hesitant, lacking confidence", category="negative",
                source_system="ui", aliases=["embarrassed", "hesitant", "uncertain"]
            ),
            UnifiedEmotionParameters(
                name="cold", temperature=0.7, exaggeration=0.8, cfg_weight=0.6, speed=1.0,
                description="Emotionless, distant", category="negative",
                source_system="core+ui", aliases=["distant", "indifferent", "detached"]
            ),
            
            # ===== DRAMATIC EMOTIONS (Cảm xúc kịch tính) =====
            UnifiedEmotionParameters(
                name="dramatic", temperature=1.0, exaggeration=1.2, cfg_weight=0.6, speed=1.0,
                description="Theatrical, intense expression", category="dramatic",
                source_system="core+ui+chatterbox", aliases=["theatrical", "intense"]
            ),
            UnifiedEmotionParameters(
                name="mysterious", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=0.9,
                description="Enigmatic, secretive tone", category="dramatic",
                source_system="core+ui", aliases=["enigmatic", "secretive", "ominous", "eerie"]
            ),
            UnifiedEmotionParameters(
                name="surprised", temperature=0.9, exaggeration=1.2, cfg_weight=0.6, speed=1.2,
                description="Shock, disbelief, amazement", category="dramatic",
                source_system="ui", aliases=["shocked", "amazed", "astonished"]
            ),
            UnifiedEmotionParameters(
                name="commanding", temperature=0.8, exaggeration=1.1, cfg_weight=0.7, speed=1.0,
                description="Authoritative, decisive tone", category="dramatic",
                source_system="ui", aliases=["authoritative", "decisive", "firm"]
            ),
            UnifiedEmotionParameters(
                name="urgent", temperature=0.9, exaggeration=1.2, cfg_weight=0.7, speed=1.2,
                description="Emergency, warning calls", category="dramatic",
                source_system="ui", aliases=["warning", "emergency", "alarm"]
            ),
            UnifiedEmotionParameters(
                name="contemptuous", temperature=0.8, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Harsh mockery, clear disdain", category="dramatic",
                source_system="ui", aliases=["scornful", "disdainful", "condescending"]
            ),
            UnifiedEmotionParameters(
                name="bewildered", temperature=0.8, exaggeration=1.1, cfg_weight=0.6, speed=0.9,
                description="Confused, don't understand", category="dramatic",
                source_system="ui", aliases=["lost", "perplexed", "dazed"]
            ),
            UnifiedEmotionParameters(
                name="pleading", temperature=0.8, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Begging, deep emotional appeals", category="dramatic",
                source_system="ui", aliases=["earnest", "desperate"]
            ),
            
            # ===== SPECIAL EMOTIONS (Cảm xúc đặc biệt) =====
            UnifiedEmotionParameters(
                name="persuasive", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=1.0,
                description="Convincing, eloquent argument", category="special",
                source_system="core+ui", aliases=["convincing", "eloquent", "rhetorical"]
            ),
            UnifiedEmotionParameters(
                name="humorous", temperature=0.9, exaggeration=1.1, cfg_weight=0.6, speed=1.1,
                description="Funny, charming, witty", category="special",
                source_system="ui", aliases=["witty", "amusing", "charming"]
            ),
            UnifiedEmotionParameters(
                name="flirtatious", temperature=0.9, exaggeration=1.1, cfg_weight=0.6, speed=1.0,
                description="Playful, suggestive tone", category="special",
                source_system="ui", aliases=["provocative", "seductive"]
            ),
            UnifiedEmotionParameters(
                name="sleepy", temperature=0.7, exaggeration=0.8, cfg_weight=0.5, speed=0.8,
                description="Drowsy, tired expression", category="special",
                source_system="ui", aliases=["drowsy", "tired"]
            ),
            UnifiedEmotionParameters(
                name="shy", temperature=0.7, exaggeration=0.8, cfg_weight=0.5, speed=0.9,
                description="Timid, bashful tone", category="special",
                source_system="ui", aliases=["timid", "bashful"]
            ),
            
            # ===== ADDITIONAL EMOTIONS từ 93 UI Mapping =====
            UnifiedEmotionParameters(
                name="suspenseful", temperature=0.8, exaggeration=1.0, cfg_weight=0.6, speed=0.9,
                description="Tense, anticipatory", category="dramatic",
                source_system="ui", aliases=["tense", "anticipatory"]
            ),
            
        ]
        
        # Store all emotions in unified database
        for emotion in unified_emotions_data:
            self.unified_emotions[emotion.name] = emotion
            
            # Create alias mappings
            for alias in emotion.aliases:
                self.emotion_aliases[alias] = emotion.name
        
        logger.info(f"[OK] Created unified emotion database with {len(self.unified_emotions)} emotions")
        logger.info(f"[CLIPBOARD] Generated {len(self.emotion_aliases)} emotion aliases for backward compatibility")
    
    def generate_backward_compatibility_mapping(self):
        """Tạo mapping cho backward compatibility với 3 hệ thống cũ"""
        
        # ================================================================
        # [REFRESH] BACKWARD COMPATIBILITY MAPPING
        # Đảm bảo các hệ thống cũ vẫn hoạt động bình thường
        # ================================================================
        
        # Legacy emotions không có trong unified system -> map to closest match
        legacy_mappings = {
            # Từ 28 Core Emotions
            "gentle": "soft",
            "determined": "commanding", 
            
            # Từ 93 UI Emotions
            "joyful": "happy",
            "furious": "angry",
            "shocked": "surprised",
            "amazed": "surprised",
            "hurt": "sad",
            "irritated": "angry",
            "frustrated": "angry",
            "earnest": "pleading",
            "desperate": "pleading",
            "worried": "anxious",
            "nervous": "anxious",
            "restless": "anxious",
            "ominous": "mysterious",
            "eerie": "mysterious",
            "urgent": "urgent",
            "emergency": "urgent",
            "alarm": "urgent",
            "mocking": "sarcastic",
            "ironic": "sarcastic",
            "impressed": "admiring",
            "praising": "admiring",
            "embarrassed": "confused",
            "hesitant": "confused",
            "uncertain": "confused",
            "thoughtful": "contemplative",
            "melancholic": "sad",
            "distant": "cold",
            "indifferent": "cold",
            "detached": "cold",
            "enthusiastic": "encouraging",
            "motivating": "encouraging",
            "inspiring": "encouraging",
            "decisive": "commanding",
            "authoritative": "commanding",
            "firm": "commanding",
            "naive": "innocent",
            "childlike": "innocent",
            "carefree": "innocent",
            "lost": "bewildered",
            "perplexed": "bewildered",
            "dazed": "bewildered",
            "teasing": "playful",
            "provocative": "flirtatious",
            "witty": "humorous",
            "amusing": "humorous",
            "charming": "humorous",
            "rhetorical": "persuasive",
            "eloquent": "persuasive",
            "convincing": "persuasive",
            "scornful": "contemptuous",
            "disdainful": "contemptuous",
            "condescending": "contemptuous",
            "fear": "fearful",
            "romantic": "romantic",
            
            # Từ 8 Chatterbox Basic Emotions (tất cả đều có trong unified)
            # -> Không cần mapping thêm
        }
        
        # Add legacy mappings to alias system
        for legacy_name, unified_name in legacy_mappings.items():
            if unified_name in self.unified_emotions:
                self.emotion_aliases[legacy_name] = unified_name
        
        logger.info(f"[REFRESH] Generated {len(legacy_mappings)} legacy emotion mappings")
    
    def get_emotion_parameters(self, emotion_name: str) -> Dict[str, float]:
        """
        Lấy parameters cho emotion (support cả tên chính và aliases)
        
        Returns: Dict với 4 thông số chuẩn
        """
        # Resolve alias to main name
        main_name = self.emotion_aliases.get(emotion_name.lower(), emotion_name.lower())
        
        # Get emotion
        emotion = self.unified_emotions.get(main_name)
        
        if emotion:
            return {
                "temperature": emotion.temperature,
                "exaggeration": emotion.exaggeration,
                "cfg_weight": emotion.cfg_weight,
                "speed": emotion.speed
            }
        
        # Fallback to neutral
        neutral = self.unified_emotions.get("neutral")
        if neutral:
            logger.warning(f"[WARNING] Emotion '{emotion_name}' not found, using neutral")
            return {
                "temperature": neutral.temperature,
                "exaggeration": neutral.exaggeration,
                "cfg_weight": neutral.cfg_weight,
                "speed": neutral.speed
            }
        
        # Ultimate fallback
        logger.error(f"[EMOJI] Neutral emotion not found! Using hardcoded defaults")
        return {
            "temperature": 0.8,
            "exaggeration": 1.0,
            "cfg_weight": 0.6,
            "speed": 1.0
        }
    
    def get_all_emotions(self) -> Dict[str, UnifiedEmotionParameters]:
        """Lấy tất cả emotions trong unified system"""
        return self.unified_emotions.copy()
    
    def get_emotions_by_category(self, category: str) -> Dict[str, UnifiedEmotionParameters]:
        """Lấy emotions theo category"""
        return {
            name: emotion for name, emotion in self.unified_emotions.items()
            if emotion.category == category
        }
    
    def get_emotion_categories(self) -> List[str]:
        """Lấy tất cả categories"""
        categories = set(emotion.category for emotion in self.unified_emotions.values())
        return sorted(list(categories))
    
    def get_all_emotion_names(self) -> List[str]:
        """Lấy tất cả tên emotions (bao gồm aliases)"""
        main_names = list(self.unified_emotions.keys())
        alias_names = list(self.emotion_aliases.keys())
        return sorted(main_names + alias_names)
    
    def search_emotion(self, query: str) -> List[str]:
        """Tìm kiếm emotion theo tên hoặc mô tả"""
        query = query.lower()
        results = []
        
        # Search main names
        for name, emotion in self.unified_emotions.items():
            if query in name.lower() or query in emotion.description.lower():
                results.append(name)
        
        # Search aliases
        for alias, main_name in self.emotion_aliases.items():
            if query in alias.lower() and main_name not in results:
                results.append(main_name)
        
        return sorted(results)
    
    def add_custom_emotion(self, name: str, description: str = "", category: str = "neutral", 
                          temperature: float = 0.8, exaggeration: float = 1.0, 
                          cfg_weight: float = 0.6, speed: float = 1.0, 
                          aliases: List[str] = None) -> bool:
        """Thêm custom emotion mới vào unified system"""
        try:
            # Validate tên emotion
            if not name or not name.strip():
                raise ValueError("Tên emotion không được trống")
            
            name = name.strip().lower()
            
            # Check duplicate  
            if name in self.unified_emotions:
                raise ValueError(f"Emotion '{name}' đã tồn tại")
            
            # Check aliases conflicts
            if aliases:
                for alias in aliases:
                    if alias.lower() in self.emotion_aliases:
                        raise ValueError(f"Alias '{alias}' đã được sử dụng")
            
            # Validate parameters theo expert recommendations
            if not (0.7 <= temperature <= 1.0):
                logger.warning(f"Temperature {temperature} ngoài range khuyến nghị (0.7-1.0)")
            if not (0.8 <= exaggeration <= 1.2):
                logger.warning(f"Exaggeration {exaggeration} ngoài range khuyến nghị (0.8-1.2)")
            if not (0.5 <= cfg_weight <= 0.7):
                logger.warning(f"CFG Weight {cfg_weight} ngoài range khuyến nghị (0.5-0.7)")
            if not (0.8 <= speed <= 1.3):
                logger.warning(f"Speed {speed} ngoài range khuyến nghị (0.8-1.3)")
            
            # Tạo emotion mới
            if aliases is None:
                aliases = []
                
            new_emotion = UnifiedEmotionParameters(
                name=name,
                temperature=temperature,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                speed=speed,
                description=description or f"Custom emotion: {name}",
                category=category,
                source_system="custom",
                aliases=aliases
            )
            
            # Add vào hệ thống
            self.unified_emotions[name] = new_emotion
            
            # Add aliases mappings
            for alias in aliases:
                self.emotion_aliases[alias.lower()] = name
            
            # Save config
            self.save_unified_config()
            
            logger.info(f"[OK] Added custom emotion: {name}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Failed to add custom emotion '{name}': {str(e)}")
            raise e
    
    def delete_custom_emotion(self, emotion_name: str) -> bool:
        """Xóa custom emotion (chỉ được xóa custom, không xóa built-in)"""
        try:
            emotion_name = emotion_name.lower()
            
            if emotion_name not in self.unified_emotions:
                raise ValueError(f"Emotion '{emotion_name}' không tồn tại")
            
            emotion = self.unified_emotions[emotion_name]
            
            # Chỉ cho phép xóa custom emotions
            if emotion.source_system != "custom":
                raise ValueError(f"Không thể xóa built-in emotion '{emotion_name}'. Chỉ custom emotions mới có thể xóa.")
            
            # Remove aliases
            for alias in emotion.aliases:
                if alias.lower() in self.emotion_aliases:
                    del self.emotion_aliases[alias.lower()]
            
            # Remove emotion
            del self.unified_emotions[emotion_name]
            
            # Save config
            self.save_unified_config()
            
            logger.info(f"[OK] Deleted custom emotion: {emotion_name}")
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Failed to delete emotion '{emotion_name}': {str(e)}")
            return False
    
    def get_custom_emotions(self) -> Dict[str, UnifiedEmotionParameters]:
        """Lấy danh sách chỉ custom emotions"""
        return {name: emotion for name, emotion in self.unified_emotions.items() 
                if emotion.source_system == "custom"}
    
    def is_custom_emotion(self, emotion_name: str) -> bool:
        """Check xem emotion có phải custom không"""
        emotion = self.unified_emotions.get(emotion_name.lower())
        return emotion is not None and emotion.source_system == "custom"
    
    def validate_expert_compliance(self) -> Dict[str, Any]:
        """
        Kiểm tra mức độ tuân thủ khuyến nghị chuyên gia
        
        Khuyến nghị:
        - Temperature: 0.7 - 1.0
        - Exaggeration: 0.8 - 1.2  
        - CFG Weight: 0.5 - 0.7
        - Speed: 0.8 - 1.3
        """
        compliance = {
            "temperature": {"compliant": 0, "total": 0, "violations": []},
            "exaggeration": {"compliant": 0, "total": 0, "violations": []},
            "cfg_weight": {"compliant": 0, "total": 0, "violations": []},
            "speed": {"compliant": 0, "total": 0, "violations": []}
        }
        
        # Check ranges
        ranges = {
            "temperature": (0.7, 1.0),
            "exaggeration": (0.8, 1.2),
            "cfg_weight": (0.5, 0.7),
            "speed": (0.8, 1.3)
        }
        
        for name, emotion in self.unified_emotions.items():
            for param, (min_val, max_val) in ranges.items():
                compliance[param]["total"] += 1
                
                value = getattr(emotion, param)
                if min_val <= value <= max_val:
                    compliance[param]["compliant"] += 1
                else:
                    compliance[param]["violations"].append({
                        "emotion": name,
                        "value": value,
                        "recommended": f"{min_val}-{max_val}"
                    })
        
        # Calculate percentages
        summary = {}
        for param, data in compliance.items():
            percentage = (data["compliant"] / data["total"]) * 100 if data["total"] > 0 else 0
            summary[param] = {
                "compliance_rate": round(percentage, 1),
                "compliant": data["compliant"],
                "total": data["total"],
                "violations": len(data["violations"])
            }
        
        return {
            "summary": summary,
            "details": compliance,
            "total_emotions": len(self.unified_emotions)
        }
    
    def save_unified_config(self):
        """Lưu unified configuration vào file"""
        try:
            # Main config
            config_file = self.config_dir / "unified_emotions.json"
            emotions_data = {
                name: asdict(emotion) for name, emotion in self.unified_emotions.items()
            }
            
            config_data = {
                "version": "2.0",
                "description": "Unified Emotion System - Consolidated from 3 legacy systems",
                "total_emotions": len(self.unified_emotions),
                "total_aliases": len(self.emotion_aliases),
                "expert_recommendations": {
                    "temperature": "0.7 - 1.0",
                    "exaggeration": "0.8 - 1.2", 
                    "cfg_weight": "0.5 - 0.7",
                    "speed": "0.8 - 1.3"
                },
                "emotions": emotions_data,
                "aliases": self.emotion_aliases
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Compliance report
            compliance = self.validate_expert_compliance()
            compliance_file = self.config_dir / "unified_emotions_compliance_report.json"
            
            with open(compliance_file, 'w', encoding='utf-8') as f:
                json.dump(compliance, f, indent=2, ensure_ascii=False)
            
            logger.info(f"[OK] Saved unified emotion config to {config_file}")
            logger.info(f"[STATS] Saved compliance report to {compliance_file}")
            
        except Exception as e:
            logger.error(f"[EMOJI] Failed to save unified config: {e}")
    
    def export_legacy_compatibility_layer(self):
        """Export compatibility layer cho 3 hệ thống cũ"""
        
        compatibility_data = {
            "advanced_window_mapping": {},
            "chatterbox_basic_emotions": {},
            "core_emotions": {},
            "migration_guide": {
                "description": "Migration từ legacy systems sang Unified Emotion System",
                "steps": [
                    "1. Import UnifiedEmotionSystem",
                    "2. Replace emotion_manager với unified_emotion_system",
                    "3. Use get_emotion_parameters() cho tất cả emotion lookups",
                    "4. Update UI components để sử dụng unified categories",
                    "5. Test backward compatibility với existing scripts"
                ]
            }
        }
        
        # Generate mappings for each legacy system
        for emotion_name in self.get_all_emotion_names():
            params = self.get_emotion_parameters(emotion_name)
            
            # For advanced_window.py map_emotion_to_parameters()
            compatibility_data["advanced_window_mapping"][emotion_name] = {
                "exaggeration": params["exaggeration"],
                "cfg_weight": params["cfg_weight"]
            }
            
            # For chatterbox basic emotions
            if emotion_name in ["neutral", "happy", "sad", "angry", "excited", "calm", "whisper", "dramatic"]:
                compatibility_data["chatterbox_basic_emotions"][emotion_name] = {
                    "temperature": params["temperature"],
                    "exaggeration": params["exaggeration"]
                }
            
            # For core emotion manager
            compatibility_data["core_emotions"][emotion_name] = params
        
        # Save compatibility layer
        compat_file = self.config_dir / "legacy_compatibility_layer.json"
        with open(compat_file, 'w', encoding='utf-8') as f:
            json.dump(compatibility_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[REFRESH] Exported legacy compatibility layer to {compat_file}")


# ================================================================
# [STAR] GLOBAL UNIFIED EMOTION SYSTEM INSTANCE
# ================================================================

# Singleton instance for entire Voice Studio application
unified_emotion_system = UnifiedEmotionSystem()


# ================================================================
# [ROCKET] CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY
# ================================================================

def get_emotion_parameters(emotion_name: str) -> Dict[str, float]:
    """Convenience function - drop-in replacement cho tất cả legacy systems"""
    return unified_emotion_system.get_emotion_parameters(emotion_name)

def get_all_emotions() -> Dict[str, UnifiedEmotionParameters]:
    """Get all unified emotions"""
    return unified_emotion_system.get_all_emotions()

def get_emotion_categories() -> List[str]:
    """Get all emotion categories"""
    return unified_emotion_system.get_emotion_categories()

def search_emotions(query: str) -> List[str]:
    """Search emotions by name or description"""
    return unified_emotion_system.search_emotion(query)

def validate_expert_compliance() -> Dict[str, Any]:
    """Validate compliance với expert recommendations"""
    return unified_emotion_system.validate_expert_compliance()


# ================================================================
# [TEST] DEMO AND TESTING
# ================================================================

def demo_unified_emotion_system():
    """Demo unified emotion system capabilities"""
    print("[THEATER] === UNIFIED EMOTION SYSTEM DEMO ===")
    print("=" * 50)
    
    # System overview
    emotions = unified_emotion_system.get_all_emotions()
    print(f"[STATS] Total Emotions: {len(emotions)}")
    print(f"[EMOJI] Categories: {', '.join(unified_emotion_system.get_emotion_categories())}")
    print(f"[REFRESH] Aliases: {len(unified_emotion_system.emotion_aliases)}")
    print()
    
    # Test backward compatibility
    print("[REFRESH] BACKWARD COMPATIBILITY TEST:")
    legacy_emotions = ["neutral", "happy", "furious", "joyful", "contemplative", "mysterious"]
    
    for emotion in legacy_emotions:
        params = get_emotion_parameters(emotion)
        print(f"   {emotion}: temp={params['temperature']:.1f}, exag={params['exaggeration']:.1f}, "
              f"cfg={params['cfg_weight']:.1f}, speed={params['speed']:.1f}")
    print()
    
    # Expert compliance
    compliance = validate_expert_compliance()
    print("[CLIPBOARD] EXPERT COMPLIANCE SUMMARY:")
    for param, data in compliance["summary"].items():
        print(f"   {param.title()}: {data['compliance_rate']:.1f}% "
              f"({data['compliant']}/{data['total']} emotions)")
    print()
    
    # Search test
    print("[SEARCH] SEARCH TEST:")
    search_results = search_emotions("happy")
    print(f"   Search 'happy': {', '.join(search_results[:5])}")
    print()
    
    print("[OK] Unified Emotion System Demo Complete!")


if __name__ == "__main__":
    demo_unified_emotion_system()