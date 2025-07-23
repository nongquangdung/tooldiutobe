#!/usr/bin/env python3
"""
[THEATER] Unified Emotion System Helpers
"""

from typing import Dict
from core.unified_emotion_system import get_emotion_parameters


def get_unified_emotion_default(emotion_name: str) -> Dict[str, float]:
    """
    [TARGET] Get default parameters for emotion từ Unified Emotion System
    Dùng cho reset functionality
    """
    from core.unified_emotion_system import unified_emotion_system
    
    emotion = unified_emotion_system.unified_emotions.get(emotion_name)
    if emotion:
        return {
            "temperature": emotion.temperature,
            "exaggeration": emotion.exaggeration, 
            "cfg_weight": emotion.cfg_weight,
            "speed": emotion.speed
        }
    
    # Fallback to neutral
    return get_emotion_parameters("neutral")

def preview_unified_emotion(emotion_name: str, text: str = "Test preview") -> str:
    """
    [MUSIC] Preview emotion với Unified Emotion System parameters
    """
    params = get_emotion_parameters(emotion_name)
    
    # Generate preview audio với unified parameters
    # (Implementation sẽ tương tự như preview cũ nhưng dùng unified params)
    return f"Preview for {emotion_name} with params: {params}"
