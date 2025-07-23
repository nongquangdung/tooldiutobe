"""
Hybrid TTS Manager
Integrates optimized provider with existing system

Features:
- Dual-mode processing (Fast/Compatible)
- Automatic fallback system
- Performance monitoring
- Seamless integration with existing UI
"""

import logging
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class TtsMode(Enum):
    """TTS Processing modes"""
    MAXIMUM_PERFORMANCE = "maximum_performance"  # Use optimized provider only
    HYBRID = "hybrid"  # Try optimized first, fallback to compatible
    MAXIMUM_COMPATIBILITY = "maximum_compatibility"  # Use existing provider only

@dataclass
class HybridConfig:
    """Configuration for hybrid TTS manager"""
    mode: TtsMode = TtsMode.HYBRID
    enable_performance_monitoring: bool = True
    fallback_timeout: float = 10.0  # Seconds before fallback
    cache_enabled: bool = True
    parallel_processing: bool = True

class HybridTtsManager:
    """
    Hybrid TTS Manager
    
    Manages both optimized and compatible TTS providers
    Provides automatic fallback and performance optimization
    """
    
    def __init__(self, config: Optional[HybridConfig] = None):
        self.config = config or HybridConfig()
        
        # Initialize providers
        self._optimized_provider = None
        self._compatible_provider = None
        
        # Performance tracking
        self.performance_metrics = {
            'total_requests': 0,
            'optimized_success': 0,
            'optimized_failures': 0,
            'fallback_usage': 0,
            'average_optimized_time': 0.0,
            'average_fallback_time': 0.0,
            'total_time_saved': 0.0
        }
        
        logger.info("[EMOJI] Hybrid TTS Manager initialized")
        logger.info(f"   Mode: {self.config.mode.value}")
        logger.info(f"   Performance monitoring: {self.config.enable_performance_monitoring}")
    
    def _get_optimized_provider(self):
        """Lazy load optimized provider"""
        if self._optimized_provider is None:
            try:
                from tts.optimized_chatterbox_provider import OptimizedChatterboxProvider, OptimizedGenerationConfig
                
                opt_config = OptimizedGenerationConfig(
                    bypass_validation=True,
                    use_model_cache=self.config.cache_enabled,
                    parallel_processing=self.config.parallel_processing
                )
                
                self._optimized_provider = OptimizedChatterboxProvider(opt_config)
                logger.info("Optimized provider loaded successfully")
                
            except Exception as e:
                logger.error(f"Failed to load optimized provider: {e}")
                self._optimized_provider = None
        
        return self._optimized_provider
    
    def _get_compatible_provider(self):
        """Lazy load compatible provider"""
        if self._compatible_provider is None:
            try:
                from tts.real_chatterbox_provider import RealChatterboxProvider
                self._compatible_provider = RealChatterboxProvider()
                logger.info("Compatible provider loaded successfully")
                
            except Exception as e:
                logger.error(f"Failed to load compatible provider: {e}")
                self._compatible_provider = None
        
        return self._compatible_provider
    
    def generate_voice(self, 
                      text: str,
                      save_path: str,
                      voice_name: Optional[str] = None,
                      emotion: str = "neutral",
                      speed: float = 1.0,
                      cfg_weight: float = 0.5,
                      **kwargs) -> Dict[str, Any]:
        """
        Generate voice using hybrid approach
        
        Process:
        1. Try optimized provider if enabled
        2. Fallback to compatible provider if needed
        3. Track performance metrics
        """
        start_time = time.time()
        self.performance_metrics['total_requests'] += 1
        
        result = None
        used_optimized = False
        
        # Try optimized provider first (if enabled)
        if self.config.mode in [TtsMode.MAXIMUM_PERFORMANCE, TtsMode.HYBRID]:
            optimized_provider = self._get_optimized_provider()
            
            if optimized_provider:
                try:
                    logger.debug("Attempting optimized generation...")
                    
                    # Generate using optimized provider
                    audio_tensor, gen_time = optimized_provider.generate_direct(
                        text=text,
                        voice=voice_name or "neutral",
                        emotion=emotion,
                        speed=speed,
                        cfg_weight=cfg_weight
                    )
                    
                    # Save audio
                    optimized_provider._save_audio_optimized(audio_tensor, save_path)
                    
                    # Success with optimized provider
                    self.performance_metrics['optimized_success'] += 1
                    self.performance_metrics['average_optimized_time'] = (
                        (self.performance_metrics['average_optimized_time'] * 
                         (self.performance_metrics['optimized_success'] - 1) + gen_time) /
                        self.performance_metrics['optimized_success']
                    )
                    
                    result = {
                        "success": True,
                        "audio_path": save_path,
                        "provider": "Optimized",
                        "generation_time": gen_time,
                        "cache_hit": gen_time < 0.01,
                        "performance_boost": True
                    }
                    
                    used_optimized = True
                    logger.info(f"[OK] Optimized generation successful: {gen_time:.3f}s")
                    
                except Exception as e:
                    logger.warning(f"Optimized generation failed: {e}")
                    self.performance_metrics['optimized_failures'] += 1
                    
                    # Continue to fallback if hybrid mode
                    if self.config.mode == TtsMode.MAXIMUM_PERFORMANCE:
                        # No fallback in max performance mode
                        return {
                            "success": False,
                            "error": f"Optimized generation failed: {str(e)}",
                            "provider": "Optimized (failed)"
                        }
        
        # Fallback to compatible provider
        if not used_optimized and self.config.mode in [TtsMode.HYBRID, TtsMode.MAXIMUM_COMPATIBILITY]:
            compatible_provider = self._get_compatible_provider()
            
            if compatible_provider:
                try:
                    logger.debug("Using compatible provider...")
                    self.performance_metrics['fallback_usage'] += 1
                    
                    fallback_start = time.time()
                    
                    # Use existing provider interface
                    result = compatible_provider.generate_voice(
                        text=text,
                        save_path=save_path,
                        voice_name=voice_name,
                        emotion=emotion,
                        speed=speed,
                        cfg_weight=cfg_weight,
                        **kwargs
                    )
                    
                    fallback_time = time.time() - fallback_start
                    self.performance_metrics['average_fallback_time'] = (
                        (self.performance_metrics['average_fallback_time'] * 
                         (self.performance_metrics['fallback_usage'] - 1) + fallback_time) /
                        self.performance_metrics['fallback_usage']
                    )
                    
                    if result.get("success"):
                        result["provider"] = "Compatible (fallback)"
                        result["generation_time"] = fallback_time
                        result["performance_boost"] = False
                        logger.info(f"[OK] Compatible generation successful: {fallback_time:.3f}s")
                    
                except Exception as e:
                    logger.error(f"Compatible generation failed: {e}")
                    result = {
                        "success": False,
                        "error": f"All providers failed. Last error: {str(e)}",
                        "provider": "None (all failed)"
                    }
        
        # Update total time saved metric
        total_time = time.time() - start_time
        if used_optimized and self.performance_metrics['average_fallback_time'] > 0:
            time_saved = max(0, self.performance_metrics['average_fallback_time'] - total_time)
            self.performance_metrics['total_time_saved'] += time_saved
        
        return result or {
            "success": False,
            "error": "No providers available",
            "provider": "None"
        }
    
    def generate_batch(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate batch of audio using optimal provider
        """
        logger.info(f"[HOT] Hybrid batch generation: {len(requests)} requests")
        
        # Try optimized batch processing first
        if self.config.mode in [TtsMode.MAXIMUM_PERFORMANCE, TtsMode.HYBRID]:
            optimized_provider = self._get_optimized_provider()
            
            if optimized_provider:
                try:
                    results = optimized_provider.generate_batch_optimized(requests)
                    
                    # Check if all succeeded
                    successful = sum(1 for r in results if r.get('success', False))
                    if successful == len(requests) or self.config.mode == TtsMode.MAXIMUM_PERFORMANCE:
                        logger.info(f"[OK] Optimized batch complete: {successful}/{len(requests)}")
                        return results
                    else:
                        logger.warning(f"Optimized batch partial success: {successful}/{len(requests)}")
                        
                except Exception as e:
                    logger.warning(f"Optimized batch failed: {e}")
        
        # Fallback to sequential processing with compatible provider
        if self.config.mode in [TtsMode.HYBRID, TtsMode.MAXIMUM_COMPATIBILITY]:
            logger.info("Using compatible provider for batch processing...")
            results = []
            
            for request in requests:
                result = self.generate_voice(**request)
                results.append(result)
            
            return results
        
        # No fallback in maximum performance mode
        return [{"success": False, "error": "Batch processing failed"} for _ in requests]
    
    def set_mode(self, mode: TtsMode):
        """Change TTS processing mode"""
        self.config.mode = mode
        logger.info(f"TTS mode changed to: {mode.value}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report"""
        total_optimized = self.performance_metrics['optimized_success'] + self.performance_metrics['optimized_failures']
        optimized_success_rate = (
            (self.performance_metrics['optimized_success'] / max(1, total_optimized)) * 100
        )
        
        fallback_rate = (
            (self.performance_metrics['fallback_usage'] / max(1, self.performance_metrics['total_requests'])) * 100
        )
        
        # Calculate performance improvement
        if self.performance_metrics['average_fallback_time'] > 0 and self.performance_metrics['average_optimized_time'] > 0:
            speedup_factor = self.performance_metrics['average_fallback_time'] / self.performance_metrics['average_optimized_time']
        else:
            speedup_factor = 1.0
        
        return {
            "total_requests": self.performance_metrics['total_requests'],
            "optimized_success_rate": optimized_success_rate,
            "fallback_rate": fallback_rate,
            "average_optimized_time": self.performance_metrics['average_optimized_time'],
            "average_fallback_time": self.performance_metrics['average_fallback_time'],
            "speedup_factor": speedup_factor,
            "total_time_saved": self.performance_metrics['total_time_saved'],
            "current_mode": self.config.mode.value,
            "recommendations": self._get_performance_recommendations()
        }
    
    def _get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        
        if self.performance_metrics['optimized_failures'] > self.performance_metrics['optimized_success']:
            recommendations.append("Consider using Maximum Compatibility mode for stability")
        
        if self.performance_metrics['fallback_usage'] == 0 and self.performance_metrics['optimized_success'] > 5:
            recommendations.append("Optimized provider working well - consider Maximum Performance mode")
        
        if self.performance_metrics['total_time_saved'] > 60:  # 1 minute saved
            recommendations.append(f"Optimizations saved {self.performance_metrics['total_time_saved']:.1f} seconds total")
        
        if not self.config.cache_enabled:
            recommendations.append("Enable caching for better performance")
        
        return recommendations
    
    def clear_cache(self):
        """Clear all provider caches"""
        if self._optimized_provider:
            self._optimized_provider.clear_cache()
        
        logger.info("All caches cleared")
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        return {
            "optimized_available": self._get_optimized_provider() is not None,
            "compatible_available": self._get_compatible_provider() is not None,
            "current_mode": self.config.mode.value,
            "performance_monitoring": self.config.enable_performance_monitoring,
            "cache_enabled": self.config.cache_enabled
        } 