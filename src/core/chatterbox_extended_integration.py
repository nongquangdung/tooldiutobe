#!/usr/bin/env python3
"""
[ROCKET] CHATTERBOX EXTENDED INTEGRATION
===================================

Integration manager kết nối tất cả advanced modules với Voice Studio:
- AdvancedTextProcessor: Text preprocessing
- AdvancedAudioProcessor: Audio post-processing  
- GenerationController: Quality control & multiple takes
- WhisperManager: STT validation
- Seamless integration với existing Voice Studio workflow
"""

import os
import sys
import time
import asyncio
import logging
import tempfile
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from pathlib import Path
import json

# Add src directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import our advanced modules
from core.advanced_text_processor import AdvancedTextProcessor, TextProcessingConfig, create_standard_processor, create_conservative_processor, create_aggressive_processor
from core.advanced_audio_processor import AdvancedAudioProcessor, AudioProcessingConfig, create_default_processor as create_audio_processor, create_quality_processor, create_fast_processor
from core.generation_controller import GenerationController, GenerationConfig, create_default_controller, create_quality_controller, create_fast_controller
from core.whisper_manager import WhisperManager, WhisperConfig, create_default_manager

# Import parallel whisper validator
try:
    from core.parallel_whisper_validator import ParallelWhisperValidator, WhisperValidationConfig
    PARALLEL_WHISPER_AVAILABLE = True
except ImportError:
    PARALLEL_WHISPER_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ExtendedGenerationConfig:
    """Cấu hình tổng thể cho extended generation system"""
    # Text processing
    enable_advanced_text_processing: bool = True
    text_processing_mode: str = "default"  # "default", "conservative", "aggressive"
    
    # Audio processing  
    enable_advanced_audio_processing: bool = True
    audio_processing_mode: str = "quality"  # "default", "quality", "fast"
    
    # Generation control
    enable_quality_control: bool = True
    generation_mode: str = "balanced"  # "fast", "balanced", "quality"
    
    # Whisper validation
    enable_whisper_validation: bool = True
    whisper_mode: str = "performance"  # "performance", "quality"
    
    # Integration settings
    preserve_original_files: bool = True
    output_detailed_reports: bool = True
    enable_parallel_processing: bool = True
    
    # Performance tuning
    max_concurrent_generations: int = 4
    generation_timeout: float = 120.0
    
    # Output formats
    output_formats: List[str] = field(default_factory=lambda: ["wav", "mp3"])

@dataclass
class ExtendedGenerationResult:
    """Kết quả extended generation"""
    original_request: Dict[str, Any]
    text_processing_result: Any
    generation_results: List[Any]
    audio_processing_results: List[Any]
    final_outputs: Dict[str, List[str]]  # format -> list of file paths
    processing_stats: Dict[str, Any]
    total_processing_time: float
    success: bool
    error_message: Optional[str] = None

class ChatterboxExtendedIntegration:
    """Main integration class cho extended Chatterbox features"""
    
    def __init__(self, config: Optional[ExtendedGenerationConfig] = None):
        self.config = config or ExtendedGenerationConfig()
        
        # Initialize components based on config
        self.text_processor = self._create_text_processor()
        self.audio_processor = self._create_audio_processor()
        self.generation_controller = self._create_generation_controller()
        self.whisper_manager = self._create_whisper_manager()
        
        # Integration stats
        self.integration_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_processing_time': 0.0,
            'average_request_time': 0.0,
            'text_blocks_processed': 0,
            'audio_files_processed': 0,
            'whisper_validations': 0
        }
        
        logger.info("[ROCKET] Chatterbox Extended Integration initialized")
        self._log_component_status()
    
    def _create_text_processor(self):
        """Create text processor based on config"""
        try:
            if hasattr(self.config, 'text_processing_mode'):
                mode = self.config.text_processing_mode
            else:
                mode = "standard"  # Default fallback
            
            if mode == "conservative":
                return create_conservative_processor()
            elif mode == "aggressive":
                return create_aggressive_processor()
            else:
                return create_standard_processor()
                
        except Exception as e:
            logger.warning(f"Advanced text processor not available: {e}")
            return None
    
    def _create_audio_processor(self) -> AdvancedAudioProcessor:
        """Create audio processor based on config"""
        if self.config.audio_processing_mode == "quality":
            return create_quality_processor()
        elif self.config.audio_processing_mode == "fast":
            return create_fast_processor()
        else:
            return create_audio_processor()
    
    def _create_generation_controller(self) -> GenerationController:
        """Create generation controller based on config"""
        if self.config.generation_mode == "quality":
            return create_quality_controller()
        elif self.config.generation_mode == "fast":
            return create_fast_controller()
        else:
            return create_default_controller()
    
    def _create_whisper_manager(self):
        """Create optimized Whisper manager"""
        try:
            if PARALLEL_WHISPER_AVAILABLE:
                # Create config from extended config
                whisper_config = WhisperValidationConfig(
                    model_name=getattr(self.config, 'whisper_model', 'base'),
                    max_workers=getattr(self.config, 'max_workers', 4),
                    similarity_threshold=getattr(self.config, 'similarity_threshold', 0.8),
                    enable_retry=getattr(self.config, 'auto_retry_failed', True)
                )
                
                return ParallelWhisperValidator(whisper_config)
            else:
                logger.warning("Parallel Whisper validator not available")
                return None
            
        except Exception as e:
            logger.warning(f"Whisper manager creation failed: {e}")
            return None
    
    def _log_component_status(self):
        """Log status của tất cả components"""
        logger.info("[STATS] Component Status:")
        logger.info(f"   [EDIT] Text Processor: {self.config.text_processing_mode} mode")
        logger.info(f"   [MUSIC] Audio Processor: {self.config.audio_processing_mode} mode") 
        logger.info(f"   [TARGET] Generation Controller: {self.config.generation_mode} mode")
        logger.info(f"   [AUDIO] Whisper Manager: {self.config.whisper_mode} mode")
        logger.info(f"   [FAST] Parallel Processing: {'[OK]' if self.config.enable_parallel_processing else '[OFF]'}")
        logger.info(f"   [SEARCH] Whisper Validation: {'[OK]' if self.config.enable_whisper_validation else '[OFF]'}")
    
    async def generate_extended(self, 
                              text: str,
                              generation_function: Callable,
                              generation_params: Dict[str, Any],
                              output_dir: str,
                              metadata: Optional[Dict[str, Any]] = None) -> ExtendedGenerationResult:
        """
        EXTENDED GENERATION METHOD
        
        Provides advanced text preprocessing and audio postprocessing capabilities.
        Can work with or without actual TTS generation.
        
        Args:
            text: Input text to process
            generation_function: TTS generation function
            generation_params: TTS generation parameters
            output_dir: Output directory for files
            metadata: Optional metadata for processing
            
        Returns:
            ExtendedGenerationResult with processing results
        """
        start_time = time.time()
        request_metadata = metadata or {}
        
        logger.info(f"[ROCKET] Starting extended generation...")
        logger.info(f"   [EDIT] Text length: {len(text)} characters")
        logger.info(f"   [FOLDER] Output dir: {output_dir}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Step 1: Advanced text preprocessing
            text_processing_result = None
            processed_text_blocks = [text]  # Default fallback
            
            if self.config.enable_advanced_text_processing:
                logger.info("[EDIT] Step 1: Advanced text preprocessing...")
                text_processing_result = self.text_processor.process_text(text)
                processed_text_blocks = text_processing_result.segments
                
                logger.info(f"   [OK] Text processed: {len(processed_text_blocks)} segments")
                self.integration_stats['text_blocks_processed'] += len(processed_text_blocks)
            
            # Step 2: Quality-controlled generation
            logger.info("[TARGET] Step 2: Quality-controlled generation...")
            generation_results = None
            
            if self.config.enable_quality_control:
                # Use generation controller for quality control
                generation_results = await self.generation_controller.generate_with_quality_control(
                    text_blocks=processed_text_blocks,
                    generation_function=generation_function,
                    generation_params=generation_params
                )
                
                logger.info(f"   [OK] Generation completed: {generation_results.success_rate:.1%} success rate")
                
                # Extract successful audio files
                raw_audio_files = []
                for result in generation_results.results:
                    if result.success and result.best_candidate:
                        raw_audio_files.append(result.best_candidate.audio_path)
            else:
                # Fallback to simple generation
                raw_audio_files = []
                for i, text_block in enumerate(processed_text_blocks):
                    temp_file = os.path.join(output_dir, f"temp_gen_{i}.wav")
                    await generation_function(text=text_block, output_path=temp_file, **generation_params)
                    if os.path.exists(temp_file):
                        raw_audio_files.append(temp_file)
            
            # Step 3: Advanced audio post-processing
            audio_processing_results = []
            final_outputs = {format_type: [] for format_type in self.config.output_formats}
            
            if self.config.enable_advanced_audio_processing and raw_audio_files:
                logger.info("[MUSIC] Step 3: Advanced audio post-processing...")
                
                for i, raw_audio_file in enumerate(raw_audio_files):
                    # Create metadata for this file
                    file_metadata = {
                        **request_metadata,
                        'segment_id': i,
                        'original_text': processed_text_blocks[i] if i < len(processed_text_blocks) else text,
                        'generation_id': f"extended_{int(time.time())}_{i}",
                        'seed': generation_params.get('seed', -1)
                    }
                    
                    # Process audio
                    audio_result = self.audio_processor.process_audio(
                        input_file=raw_audio_file,
                        output_dir=os.path.join(output_dir, f"segment_{i:03d}"),
                        metadata=file_metadata
                    )
                    
                    audio_processing_results.append(audio_result)
                    
                    # Collect final outputs by format
                    for format_type, file_path in audio_result.processed_files.items():
                        final_outputs[format_type].append(file_path)
                    
                    self.integration_stats['audio_files_processed'] += 1
                
                logger.info(f"   [OK] Audio processing completed: {len(audio_processing_results)} files")
            else:
                # Simple copy for no processing
                for i, raw_audio_file in enumerate(raw_audio_files):
                    if "wav" in self.config.output_formats:
                        final_outputs["wav"].append(raw_audio_file)
            
            processing_time = time.time() - start_time
            
            # Update integration stats
            self.integration_stats['total_requests'] += 1
            self.integration_stats['successful_requests'] += 1
            self.integration_stats['total_processing_time'] += processing_time
            self.integration_stats['average_request_time'] = (
                self.integration_stats['total_processing_time'] / 
                self.integration_stats['total_requests']
            )
            
            logger.info(f"[OK] Extended generation completed in {processing_time:.2f}s")
            logger.info(f"   [STATS] Final outputs: {sum(len(files) for files in final_outputs.values())} files")
            
            return ExtendedGenerationResult(
                original_request={
                    'text': text,
                    'generation_params': generation_params,
                    'metadata': request_metadata
                },
                text_processing_result=text_processing_result,
                generation_results=generation_results,
                audio_processing_results=audio_processing_results,
                final_outputs=final_outputs,
                processing_stats=self._compile_processing_stats(),
                total_processing_time=processing_time,
                success=True
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            # Update failure stats
            self.integration_stats['total_requests'] += 1
            self.integration_stats['failed_requests'] += 1
            self.integration_stats['total_processing_time'] += processing_time
            
            logger.error(f"[ERROR] Extended generation failed after {processing_time:.2f}s: {e}")
            
            return ExtendedGenerationResult(
                original_request={
                    'text': text,
                    'generation_params': generation_params,
                    'metadata': request_metadata
                },
                text_processing_result=None,
                generation_results=None,
                audio_processing_results=[],
                final_outputs={},
                processing_stats=self._compile_processing_stats(),
                total_processing_time=processing_time,
                success=False,
                error_message=str(e)
            )
    
    def _compile_processing_stats(self) -> Dict[str, Any]:
        """Compile stats từ tất cả components"""
        stats = {
            'integration': self.integration_stats.copy(),
            'text_processor': self.text_processor.get_processing_report(),
            'audio_processor': self.audio_processor.get_processing_report(),
            'generation_controller': self.generation_controller.get_controller_report(),
            'whisper_manager': self.whisper_manager.get_manager_report()
        }
        
        return stats
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'config': self.config.__dict__,
            'components': {
                'text_processor': {
                    'available': self.text_processor is not None,
                    'mode': self.config.text_processing_mode
                },
                'audio_processor': {
                    'available': self.audio_processor is not None,
                    'mode': self.config.audio_processing_mode,
                    'ffmpeg': self.audio_processor.ffmpeg_available,
                    'auto_editor': self.audio_processor.auto_editor_available
                },
                'generation_controller': {
                    'available': self.generation_controller is not None,
                    'mode': self.config.generation_mode,
                    'whisper_validation': self.generation_controller.whisper_available
                },
                'whisper_manager': {
                    'available': self.whisper_manager is not None,
                    'mode': self.config.whisper_mode,
                    'model_loaded': hasattr(self.whisper_manager, 'current_model') and self.whisper_manager.current_model is not None
                }
            },
            'stats': self.integration_stats,
            'ui_info': self._get_ui_info()
        }
    
    def _get_ui_info(self) -> Dict[str, Any]:
        """Get information for UI display"""
        whisper_ui = {}
        if self.whisper_manager and hasattr(self.whisper_manager, 'get_ui_display_info'):
            whisper_ui = self.whisper_manager.get_ui_display_info()
        else:
            whisper_ui = {'system_info': {'memory_warning': False}}
        
        return {
            'whisper_info': whisper_ui,
            'processing_modes': {
                'text_processing': {
                    'current': self.config.text_processing_mode,
                    'options': ['conservative', 'default', 'aggressive'],
                    'descriptions': {
                        'conservative': 'Minimal processing, preserve original text',
                        'default': 'Balanced processing with smart optimizations',
                        'aggressive': 'Maximum processing for optimal TTS'
                    }
                },
                'audio_processing': {
                    'current': self.config.audio_processing_mode,
                    'options': ['fast', 'default', 'quality'],
                    'descriptions': {
                        'fast': 'Quick processing, minimal post-processing',
                        'default': 'Balanced quality and speed',
                        'quality': 'Maximum quality with full post-processing'
                    }
                },
                'generation': {
                    'current': self.config.generation_mode,
                    'options': ['fast', 'balanced', 'quality'],
                    'descriptions': {
                        'fast': 'Single generation, no validation',
                        'balanced': 'Multiple candidates with basic validation',
                        'quality': 'Maximum candidates with full validation'
                    }
                }
            },
            'feature_status': {
                'text_processing': self.config.enable_advanced_text_processing,
                'audio_processing': self.config.enable_advanced_audio_processing,
                'quality_control': self.config.enable_quality_control,
                'whisper_validation': self.config.enable_whisper_validation,
                'parallel_processing': self.config.enable_parallel_processing
            },
            'recommendations': {
                'optimal_workers': min(self.config.max_concurrent_generations, 4),
                'memory_warnings': whisper_ui['system_info']['memory_warning'],
                'suggested_whisper_model': 'base'  # fallback value
            }
        }
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update configuration và reinitialize components if needed"""
        logger.info("[REFRESH] Updating extended configuration...")
        
        # Store old config for comparison
        old_config = self.config.__dict__.copy()
        
        # Update config
        for key, value in new_config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # Check if components need reinitialization
        if old_config['text_processing_mode'] != self.config.text_processing_mode:
            logger.info("   [EDIT] Reinitializing text processor...")
            self.text_processor = self._create_text_processor()
        
        if old_config['audio_processing_mode'] != self.config.audio_processing_mode:
            logger.info("   [MUSIC] Reinitializing audio processor...")
            self.audio_processor = self._create_audio_processor()
        
        if old_config['generation_mode'] != self.config.generation_mode:
            logger.info("   [TARGET] Reinitializing generation controller...")
            self.generation_controller = self._create_generation_controller()
        
        if old_config['whisper_mode'] != self.config.whisper_mode:
            logger.info("   [AUDIO] Reinitializing Whisper manager...")
            self.whisper_manager = self._create_whisper_manager()
        
        logger.info("[OK] Configuration updated successfully")
    
    def generate_audio_from_script_data(self, script_data, voice_mapping, output_directory, progress_callback=None):
        """
        🚨 DEPRECATED METHOD - USE TTSBridge INSTEAD
        
        This method is deprecated to eliminate duplicate TTS calls.
        Use tts_bridge.generate_audio_from_script_data() instead.
        
        Args:
            script_data: Dict containing script data
            voice_mapping: Dict mapping characters to voices
            output_directory: Output directory path
            progress_callback: Optional progress callback function
            
        Returns:
            Dict with success status and results
        """
        # Bridge method - delegates to TTSBridge for UI compatibility
        logger.debug("ChatterboxExtended delegating to TTSBridge for audio generation")
        
        try:
            # Import TTSBridge
            from core.tts_bridge import get_tts_bridge
            bridge = get_tts_bridge()
            
            # Delegate to TTSBridge (no duplicate TTS)
            return bridge.generate_audio_from_script_data(
                script_data=script_data,
                voice_mapping=voice_mapping,
                output_directory=output_directory,
                progress_callback=progress_callback
            )
            
        except Exception as e:
            logger.error(f"Bridge delegation failed: {e}")
            return {
                "success": False,
                "error": f"Bridge delegation failed: {str(e)}",
                "mode": "error"
            }
    
    def _generate_complex_audio(self, script_data, voice_mapping, output_directory, progress_callback=None):
        """🚨 DEPRECATED - Complex audio generation moved to TTSBridge"""
        logger.warning("🚨 DEPRECATED: _generate_complex_audio() moved to TTSBridge")
        
        # Delegate to TTSBridge
        from core.tts_bridge import get_tts_bridge
        bridge = get_tts_bridge()
        return bridge.generate_multi_character(
            script_data=script_data,
            voice_mapping=voice_mapping,
            output_dir=output_directory,
            enable_postprocessing=True
        )
    
    async def _generate_simple_audio(self, script_data, output_directory, progress_callback=None):
        """🚨 DEPRECATED - Simple audio generation moved to TTSBridge"""
        logger.warning("🚨 DEPRECATED: _generate_simple_audio() moved to TTSBridge")
        
        # Delegate to TTSBridge
        from core.tts_bridge import get_tts_bridge
        bridge = get_tts_bridge()
        
        # Extract text
        text = script_data.get("text", "") if isinstance(script_data, dict) else str(script_data)
        
        result = bridge.generate_single_character(
            text=text,
            voice_name="abigail",  # Default voice
            output_dir=output_directory,
            enable_preprocessing=True,
            enable_postprocessing=True
        )
        
        return {
            "success": result.success,
            "mode": "simple",
            "result": result.metadata,
            "output_directory": output_directory,
            "error": result.error_message if not result.success else None
        }
    
    def cleanup(self):
        """Cleanup tất cả resources"""
        logger.info("[CLEAN] Cleaning up extended integration...")
        
        try:
            if self.whisper_manager:
                self.whisper_manager.cleanup_model()
            
            # Clear stats
            self.integration_stats = {key: 0 for key in self.integration_stats}
            
            logger.info("[OK] Cleanup completed")
            
        except Exception as e:
            logger.warning(f"[WARNING] Cleanup warning: {e}")

# Convenience functions
def create_default_integration() -> ChatterboxExtendedIntegration:
    """Tạo integration với cấu hình mặc định"""
    return ChatterboxExtendedIntegration()

def create_performance_integration() -> ChatterboxExtendedIntegration:
    """Tạo integration tối ưu cho performance"""
    config = ExtendedGenerationConfig(
        text_processing_mode="conservative",
        audio_processing_mode="fast", 
        generation_mode="fast",
        whisper_mode="performance",
        enable_whisper_validation=False,
        enable_parallel_processing=True,
        max_concurrent_generations=8,
        output_formats=["mp3"]
    )
    return ChatterboxExtendedIntegration(config)

def create_quality_integration() -> ChatterboxExtendedIntegration:
    """Tạo integration tối ưu cho quality"""
    config = ExtendedGenerationConfig(
        text_processing_mode="aggressive",
        audio_processing_mode="quality",
        generation_mode="quality", 
        whisper_mode="quality",
        enable_whisper_validation=True,
        enable_parallel_processing=True,
        preserve_original_files=True,
        output_detailed_reports=True,
        output_formats=["wav", "mp3", "flac"]
    )
    return ChatterboxExtendedIntegration(config)

if __name__ == "__main__":
    # Test the integration
    integration = create_default_integration()
    print("Extended integration initialized")
    
    # Print system status
    status = integration.get_system_status()
    print(json.dumps(status, indent=2, default=str)) 