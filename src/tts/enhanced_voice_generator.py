#!/usr/bin/env python3
"""
[ROCKET] ENHANCED VOICE GENERATOR
===========================

Enhanced TTS system integrating Chatterbox TTS Server với Real Chatterbox provider.
Combines 28 high-quality Chatterbox voices với existing Voice Studio capabilities.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path

# Add src directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import existing providers
from .real_chatterbox_provider import RealChatterboxProvider
from .chatterbox_voices_integration import ChatterboxVoicesManager, ChatterboxConfig

logger = logging.getLogger(__name__)

@dataclass
class VoiceGenerationRequest:
    """Enhanced voice generation request"""
    text: str
    character_id: str
    voice_provider: str = "auto"  # "chatterbox", "real_chatterbox", "auto"
    voice_id: str = "olivia"
    emotion: str = "neutral"
    speed: float = 1.0
    quality: str = "high"
    output_path: str = ""
    
    # Advanced parameters
    temperature: float = 0.7
    exaggeration: float = 1.0
    cfg_weight: float = 3.0
    seed: int = -1

    # Multi-character and inner voice support
    inner_voice: bool = False
    inner_voice_type: Optional[str] = None  # "light", "deep", "dreamy"

@dataclass
class VoiceGenerationResult:
    """Voice generation result with metadata"""
    success: bool
    output_path: str = ""
    voice_used: str = ""
    provider_used: str = ""
    generation_time: float = 0.0
    quality_score: float = 0.0
    error_message: str = ""
    metadata: Dict[str, Any] = None

class EnhancedVoiceGenerator:
    """
    [MIC] ENHANCED VOICE GENERATOR
    
    Multi-provider TTS system combining:
    - Chatterbox TTS Server (28 premium voices)
    - Real Chatterbox Provider (local TTS)
    - Smart provider selection
    - Voice quality optimization
    """
    
    def __init__(self, chatterbox_config: ChatterboxConfig = None):
        self.chatterbox_manager = ChatterboxVoicesManager(chatterbox_config)
        self.real_chatterbox = RealChatterboxProvider()
        
        # Provider priorities
        self.provider_priorities = {
            "chatterbox": 1,      # Highest quality, requires server
            "real_chatterbox": 2  # Fallback, local processing
        }
        
        # Voice quality mappings
        self.voice_quality_map = {}
        self.initialize_voice_mappings()
        
    def initialize_voice_mappings(self):
        """Initialize voice quality and availability mappings"""
        
        # Chatterbox TTS Server voices (high quality)
        chatterbox_voices = self.chatterbox_manager.get_available_voices()
        for voice_id, voice in chatterbox_voices.items():
            self.voice_quality_map[voice_id] = {
                "provider": "chatterbox",
                "quality": voice.quality_rating,
                "gender": voice.gender,
                "name": voice.name,
                "description": voice.description
            }
        
        # Real Chatterbox voices - Load từ ChatterboxVoicesManager (voices/ folder)
        try:
            # Import ChatterboxVoicesManager để load voices từ voices/ folder
            from .chatterbox_voices_integration import ChatterboxVoicesManager
            voices_manager = ChatterboxVoicesManager()
            real_chatterbox_voices = voices_manager.get_available_voices()
            
            # Add voices từ voices/ folder
            for voice_id, voice_obj in real_chatterbox_voices.items():
                if voice_id not in self.voice_quality_map:
                    self.voice_quality_map[voice_id] = {
                        "provider": "real_chatterbox", 
                        "quality": 8.0,  # High quality for local voices
                        "gender": voice_obj.gender,
                        "name": voice_obj.name,
                        "description": "Local voice from voices/ folder",
                        "file_path": voice_obj.file_path
                    }
            
            print(f"[OK] Loaded {len(real_chatterbox_voices)} voices from voices/ folder for Real Chatterbox")
            
        except Exception as e:
            print(f"[WARNING] Could not load voices from ChatterboxVoicesManager: {e}")
            print("   [EMOJI] No fallback mock voices will be added. Voice list remains empty if loading failed.")
    
    def get_available_voices(self) -> Dict[str, Dict[str, Any]]:
        """Get all available voices from all providers"""
        return self.voice_quality_map.copy()
    
    def get_voices_by_provider(self, provider: str) -> Dict[str, Dict[str, Any]]:
        """Get voices filtered by provider"""
        return {
            voice_id: info for voice_id, info in self.voice_quality_map.items()
            if info["provider"] == provider
        }
    
    def get_best_voice_for_character(
        self, 
        character_type: str = "narrator",
        gender_preference: str = None,
        quality_threshold: float = 8.0
    ) -> str:
        """
        Get best voice recommendation for character type
        
        Args:
            character_type: Type of character (narrator, hero, villain, etc.)
            gender_preference: "male", "female", or None
            quality_threshold: Minimum quality score required
        
        Returns:
            Best voice ID
        """
        
        # Get recommendations từ Chatterbox manager
        recommended_voices = self.chatterbox_manager.get_voice_recommendations(character_type)
        
        # Filter by quality and gender
        candidates = []
        for voice_id in recommended_voices:
            if voice_id in self.voice_quality_map:
                voice_info = self.voice_quality_map[voice_id]
                
                # Check quality threshold
                if voice_info["quality"] < quality_threshold:
                    continue
                
                # Check gender preference
                if gender_preference and voice_info["gender"] != gender_preference:
                    continue
                
                candidates.append((voice_id, voice_info["quality"]))
        
        # Sort by quality and return best
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        # Fallback to default high-quality voices
        fallback_voices = ["olivia", "gabriel", "alexander", "emily"]
        for voice_id in fallback_voices:
            if voice_id in self.voice_quality_map:
                return voice_id
        
        # Ultimate fallback
        return "narrator"
    
    def select_best_provider(self, voice_id: str, prefer_quality: bool = True) -> str:
        """
        Select best provider for given voice
        
        Args:
            voice_id: Requested voice ID
            prefer_quality: Whether to prefer quality over availability
        
        Returns:
            Provider name ("chatterbox" or "real_chatterbox")
        """
        
        # Cache connection status để không phải check mỗi lần
        if not hasattr(self, '_chatterbox_available'):
            self._chatterbox_available = None
            self._last_check_time = 0
        
        # Check connection mỗi 30 giây một lần (cache)
        import time
        current_time = time.time()
        if (self._chatterbox_available is None or 
            current_time - self._last_check_time > 30):
            
            connection_test = self.chatterbox_manager.test_chatterbox_connection()
            self._chatterbox_available = connection_test.get("success", False)
            self._last_check_time = current_time
            
            if not self._chatterbox_available:
                logger.info("Chatterbox TTS Server not available, using Real Chatterbox")
        
        # Return appropriate provider
        if self._chatterbox_available:
            return "chatterbox"
        else:
            return "real_chatterbox"
    
    def generate_voice(self, request: VoiceGenerationRequest) -> VoiceGenerationResult:
        """
        Generate voice with enhanced multi-provider system
        
        Args:
            request: Voice generation request
        
        Returns:
            Voice generation result with metadata
        """
        
        import time
        start_time = time.time()
        
        try:
            # Auto-select provider if not specified
            if request.voice_provider == "auto":
                selected_provider = self.select_best_provider(request.voice_id)
            else:
                selected_provider = request.voice_provider
            
            # Auto-select voice if needed
            if request.voice_id == "auto":
                request.voice_id = self.get_best_voice_for_character("narrator")
            
            # Ensure output directory exists
            if request.output_path:
                os.makedirs(os.path.dirname(request.output_path), exist_ok=True)
            else:
                request.output_path = f"./voice_studio_output/{request.character_id}_{int(time.time())}.wav"
                os.makedirs(os.path.dirname(request.output_path), exist_ok=True)
            
            # Generate based on provider
            if selected_provider == "chatterbox":
                result = self._generate_with_chatterbox(request)
            else:
                result = self._generate_with_real_chatterbox(request)
            
            # Calculate generation time
            generation_time = time.time() - start_time
            
            if result.get("success"):
                return VoiceGenerationResult(
                    success=True,
                    output_path=result["output_path"],
                    voice_used=result.get("voice_used", request.voice_id),
                    provider_used=selected_provider,
                    generation_time=generation_time,
                    quality_score=result.get("quality_rating", 8.0),
                    metadata=result
                )
            else:
                # Try fallback provider if primary failed
                if selected_provider == "chatterbox":
                    logger.warning("Chatterbox failed, trying Real Chatterbox fallback")
                    fallback_result = self._generate_with_real_chatterbox(request)
                    
                    if fallback_result.get("success"):
                        return VoiceGenerationResult(
                            success=True,
                            output_path=fallback_result["output_path"],
                            voice_used=fallback_result.get("voice_used", request.voice_id),
                            provider_used="real_chatterbox",
                            generation_time=time.time() - start_time,
                            quality_score=7.5,
                            metadata=fallback_result
                        )
                
                return VoiceGenerationResult(
                    success=False,
                    error_message=result.get("error", "Unknown generation error"),
                    provider_used=selected_provider,
                    generation_time=generation_time
                )
                
        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Voice generation failed: {str(e)}")
            return VoiceGenerationResult(
                success=False,
                error_message=str(e),
                generation_time=generation_time
            )
    
    def generate_voice_batch(self, requests: List[VoiceGenerationRequest]) -> List[VoiceGenerationResult]:
        """
        Generate a batch of voice audio files.
        Currently optimized for the RealChatterboxProvider.
        """
        import time
        start_time = time.time()
        
        if not requests:
            return []

        print(f"EnhancedVoiceGenerator: Received batch request for {len(requests)} segments.")
        
        # TODO: Implement provider routing for batches (e.g., group by provider).
        # For now, we assume all will be processed by the most efficient batch provider.
        
        provider_to_use = "real_chatterbox" # Hardcoded for now
        
        try:
            if provider_to_use == "real_chatterbox":
                # Prepare the list of dicts for the provider's batch method
                batch_for_provider = []
                for req in requests:
                    # Ensure output path is set
                    if not req.output_path:
                        # Use UUID to prevent filename collisions in batch
                        req.output_path = f"./voice_studio_output/{req.character_id}_{int(time.time())}_{uuid.uuid4().hex[:6]}.wav"
                    os.makedirs(os.path.dirname(req.output_path), exist_ok=True)
                    
                    batch_for_provider.append({
                        "text": req.text,
                        "save_path": req.output_path,
                        "emotion": req.emotion,  # NEW: Include emotion
                        "emotion_exaggeration": req.exaggeration,
                        "speed": req.speed,
                        "cfg_weight": req.cfg_weight,
                        "voice_name": req.voice_id,
                        "inner_voice": req.inner_voice,  # NEW: Include inner voice
                        "inner_voice_type": req.inner_voice_type
                    })

                # Call the provider's batch generation method
                provider_results = self.real_chatterbox.generate_voice_batch(batch_for_provider)

                # Convert results back to VoiceGenerationResult objects
                final_results = []
                total_generation_time = time.time() - start_time
                
                for i, req in enumerate(requests):
                    provider_res = provider_results[i]
                    if provider_res.get("success"):
                        final_results.append(VoiceGenerationResult(
                            success=True,
                            output_path=provider_res["audio_path"],
                            voice_used=req.voice_id,
                            provider_used=provider_to_use,
                            generation_time=total_generation_time / len(requests), # Approximate time per segment
                            metadata=provider_res
                        ))
                    else:
                        final_results.append(VoiceGenerationResult(
                            success=False,
                            error_message=provider_res.get("error", "Unknown batch error"),
                            provider_used=provider_to_use
                        ))
                return final_results
            else:
                # Fallback for other providers: generate one by one
                print("Batch processing not implemented for this provider, generating sequentially.")
                results = [self.generate_voice(req) for req in requests]
                return results

        except Exception as e:
            print(f"[EMOJI] ERROR: Enhanced batch generation failed: {e}")
            logger.error(traceback.format_exc())
            return [VoiceGenerationResult(success=False, error_message=str(e)) for _ in requests]

    def _generate_with_chatterbox(self, request: VoiceGenerationRequest) -> Dict[str, Any]:
        """Generate using Chatterbox TTS Server"""
        return self.chatterbox_manager.generate_audio_chatterbox(
            text=request.text,
            voice_id=request.voice_id,
            output_path=request.output_path,
            temperature=request.temperature,
            speed=request.speed,
            exaggeration=request.exaggeration,
            cfg_weight=request.cfg_weight,
            seed=request.seed
        )
    
    def _generate_with_real_chatterbox(self, request: VoiceGenerationRequest) -> Dict[str, Any]:
        """Generate using Real Chatterbox provider"""
        try:
            # Use voice_id directly instead of hardcoded mapping
            voice_id = request.voice_id
            
            # Log voice assignment for debugging
            print(f"   [EMOJI] Enhanced Voice Generator: Using voice_id='{voice_id}' for character '{request.character_id}'")
            
            # Generate with Real Chatterbox - now including emotion parameter
            result = self.real_chatterbox.generate_voice(
                text=request.text,
                save_path=request.output_path,
                voice_sample_path=None,  # Use predefined voice
                emotion=request.emotion,  # NEW: Pass emotion parameter
                emotion_exaggeration=request.exaggeration,
                speed=request.speed,
                cfg_weight=request.cfg_weight,
                voice_name=voice_id,  # Pass voice_id directly
                inner_voice=request.inner_voice,
                inner_voice_type=request.inner_voice_type
            )
            
            if result.get("success") and os.path.exists(request.output_path):
                return {
                    "success": True,
                    "output_path": request.output_path,
                    "voice_used": voice_id,
                    "quality_rating": 7.5,
                    "provider": "real_chatterbox"
                }
            else:
                # Propagate the actual error message from real_chatterbox.generate_voice
                return {
                    "success": False,
                    "error": result.get("error", "Real Chatterbox generation failed (unknown error)")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Real Chatterbox error: {str(e)}"
            }
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers"""
        status = {}
        
        # Chatterbox TTS Server status
        chatterbox_test = self.chatterbox_manager.test_chatterbox_connection()
        status["chatterbox"] = {
            "available": chatterbox_test.get("success", False),
            "server_url": self.chatterbox_manager.config.server_url,
            "response_time": chatterbox_test.get("response_time", 0),
            "voices_count": len(self.chatterbox_manager.voices_cache)
        }
        
        # Real Chatterbox status
        real_status = self.real_chatterbox.get_provider_status()
        status["real_chatterbox"] = {
            "available": real_status.get("available", False),
            "device": real_status.get("device", "Unknown"),
            "initialized": real_status.get("initialized", False)
        }
        
        return status
    
    def get_chatterbox_device_info(self) -> Dict[str, Any]:
        """Get Chatterbox device information for UI compatibility"""
        real_status = self.real_chatterbox.get_provider_status()
        chatterbox_test = self.chatterbox_manager.test_chatterbox_connection()
        
        return {
            "available": real_status.get("available", False) or chatterbox_test.get("success", False),
            "device_name": real_status.get("device_name", "Unknown"),
            "initialized": real_status.get("initialized", False),
            "voices_count": len(self.chatterbox_manager.voices_cache),
            "server_available": chatterbox_test.get("success", False)
        }
    
    def export_voice_config(self, output_path: str):
        """Export comprehensive voice configuration"""
        config_data = {
            "enhanced_voice_generator": {
                "total_voices": len(self.voice_quality_map),
                "providers": list(self.provider_priorities.keys()),
                "provider_status": self.get_provider_status()
            },
            "voice_mappings": self.voice_quality_map,
            "export_timestamp": "2025-06-20",
            "version": "1.0"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported enhanced voice config to {output_path}")


# Demo function
def demo_enhanced_voice_generator():
    """Demo enhanced voice generator capabilities"""
    print("[ROCKET] ENHANCED VOICE GENERATOR DEMO")
    print("=" * 50)
    
    # Initialize generator
    generator = EnhancedVoiceGenerator()
    
    # Show provider status
    print("\n[STATS] Provider Status:")
    status = generator.get_provider_status()
    for provider, info in status.items():
        availability = "[OK] Online" if info["available"] else "[EMOJI] Offline"
        print(f"   {provider}: {availability} | {info['voices_count']} voices | Quality: {info['quality_rating']}/10")
    
    # Show available voices
    all_voices = generator.get_available_voices()
    print(f"\n[MIC] Total Available Voices: {len(all_voices)}")
    
    # Show by provider
    for provider in ["chatterbox", "real_chatterbox"]:
        provider_voices = generator.get_voices_by_provider(provider)
        print(f"\n   {provider.title()}: {len(provider_voices)} voices")
        for voice_id, info in list(provider_voices.items())[:3]:
            print(f"      • {info['name']} ({voice_id}): Quality {info['quality']}/10")
    
    # Test voice recommendations
    print(f"\n[TARGET] Smart Voice Recommendations:")
    test_characters = [
        ("narrator", None),
        ("hero", "male"), 
        ("villain", "female")
    ]
    
    for char_type, gender in test_characters:
        best_voice = generator.get_best_voice_for_character(char_type, gender)
        voice_info = all_voices.get(best_voice, {})
        print(f"   {char_type.title()} ({gender or 'any'}): {voice_info.get('name', best_voice)} (Quality: {voice_info.get('quality', 'N/A')}/10)")
    
    print(f"\n[OK] Enhanced Voice Generator Demo Complete!")


if __name__ == "__main__":
    demo_enhanced_voice_generator() 