#!/usr/bin/env python3
"""
[EMOJI] WHISPER MANAGER
==================

Advanced Whisper management system tái tạo từ Chatterbox TTS Extended:
- Model selection: OpenAI Whisper và faster-whisper
- VRAM estimation và display trong UI
- Auto-disable khi không cần thiết
- VRAM management để tránh memory leaks
- Performance monitoring
- Integrated with Model Registry for singleton pattern
"""

import os
import sys
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import json

# Add src directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Optional import for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("WARNING: psutil not available, system monitoring features will be limited")

try:
    from core.model_registry import model_registry
except ImportError:
    print("WARNING: model_registry not available, using fallback")
    model_registry = None

logger = logging.getLogger(__name__)

@dataclass
class WhisperModelInfo:
    """Thông tin về Whisper model"""
    name: str
    size: str  # "tiny", "base", "small", "medium", "large", "large-v2", "large-v3"
    parameters: str  # "39M", "74M", "244M", "769M", "1550M"
    vram_requirement: float  # GB
    relative_speed: float  # Relative speed (1.0 = base model)
    accuracy: str  # "Good", "Better", "Best"
    recommended_use: str
    multilingual: bool = True

@dataclass 
class WhisperBackendInfo:
    """Thông tin về Whisper backend"""
    name: str
    display_name: str
    description: str
    installation_cmd: str
    pros: List[str]
    cons: List[str]
    available: bool = False

@dataclass
class WhisperConfig:
    """Cấu hình Whisper system"""
    backend: str = "openai"  # "openai" or "faster-whisper"
    model_size: str = "base"
    device: str = "auto"  # "auto", "cpu", "cuda", "mps"
    compute_type: str = "float16"  # For faster-whisper
    enable_vad: bool = True  # Voice Activity Detection
    beam_size: int = 5
    temperature: float = 0.0
    
    # Memory management
    auto_cleanup: bool = True
    cleanup_timeout: float = 300.0  # 5 minutes
    max_memory_usage: float = 8.0  # GB
    
    # UI settings
    show_vram_info: bool = True
    auto_disable_if_low_memory: bool = True
    memory_warning_threshold: float = 0.8  # 80% memory usage

class WhisperManager:
    """Singleton manager cho Whisper system với advanced features"""
    
    _instance = None
    _lock = threading.Lock()
    
    # Model information database
    MODEL_INFO = {
        "tiny": WhisperModelInfo(
            name="tiny", size="tiny", parameters="39M", vram_requirement=0.5,
            relative_speed=4.0, accuracy="Good", 
            recommended_use="Fast transcription, low-resource systems"
        ),
        "base": WhisperModelInfo(
            name="base", size="base", parameters="74M", vram_requirement=1.0,
            relative_speed=2.0, accuracy="Better",
            recommended_use="Balanced speed vs accuracy"
        ),
        "small": WhisperModelInfo(
            name="small", size="small", parameters="244M", vram_requirement=2.0,
            relative_speed=1.0, accuracy="Better",
            recommended_use="Good accuracy, moderate speed"
        ),
        "medium": WhisperModelInfo(
            name="medium", size="medium", parameters="769M", vram_requirement=4.0,
            relative_speed=0.5, accuracy="Best",
            recommended_use="High accuracy, slower speed"
        ),
        "large": WhisperModelInfo(
            name="large", size="large", parameters="1550M", vram_requirement=8.0,
            relative_speed=0.25, accuracy="Best",
            recommended_use="Maximum accuracy, slowest"
        ),
        "large-v2": WhisperModelInfo(
            name="large-v2", size="large-v2", parameters="1550M", vram_requirement=8.0,
            relative_speed=0.25, accuracy="Best",
            recommended_use="Latest large model with improvements"
        ),
        "large-v3": WhisperModelInfo(
            name="large-v3", size="large-v3", parameters="1550M", vram_requirement=8.0,
            relative_speed=0.25, accuracy="Best",
            recommended_use="Newest large model (requires recent whisper)"
        )
    }
    
    BACKEND_INFO = {
        "openai": WhisperBackendInfo(
            name="openai",
            display_name="OpenAI Whisper",
            description="Original OpenAI implementation",
            installation_cmd="pip install openai-whisper",
            pros=["Official implementation", "Well-tested", "Easy to use"],
            cons=["Slower than alternatives", "Higher memory usage"]
        ),
        "faster-whisper": WhisperBackendInfo(
            name="faster-whisper",
            display_name="Faster Whisper (SYSTRAN)",
            description="Optimized implementation with CTranslate2",
            installation_cmd="pip install faster-whisper",
            pros=["2-4x faster", "Lower memory usage", "Better batching"],
            cons=["Additional dependency", "Less tested"]
        )
    }
    
    def __new__(cls, config: Optional[WhisperConfig] = None):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config: Optional[WhisperConfig] = None):
        # Only initialize once
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.config = config or WhisperConfig()
        self.current_model = None
        self.current_backend = None
        self.device_info = None
        self.memory_monitor = None
        self.cleanup_timer = None
        
        # Performance tracking
        self.stats = {
            'total_transcriptions': 0,
            'total_processing_time': 0.0,
            'average_processing_speed': 0.0,
            'memory_usage_peak': 0.0,
            'model_loads': 0,
            'cleanups_performed': 0
        }
        
        # Initialize system
        self._detect_device_capabilities()
        self._check_backend_availability()
        
    def _detect_device_capabilities(self):
        """Detect device capabilities và VRAM"""
        device_info = {
            'cpu': True,
            'cuda': False,
            'mps': False,
            'total_ram': 8.0,  # Default fallback
            'available_ram': 4.0,  # Default fallback
            'gpu_info': []
        }
        
        # Get RAM info if psutil is available
        if PSUTIL_AVAILABLE:
            try:
                device_info['total_ram'] = psutil.virtual_memory().total / (1024**3)  # GB
                device_info['available_ram'] = psutil.virtual_memory().available / (1024**3)  # GB
            except Exception as e:
                logger.warning(f"Failed to get RAM info: {e}")
        else:
            logger.warning("psutil not available, using fallback RAM estimates")
        
        # Check CUDA
        try:
            import torch
            if torch.cuda.is_available():
                device_info['cuda'] = True
                for i in range(torch.cuda.device_count()):
                    gpu_props = torch.cuda.get_device_properties(i)
                    vram_gb = gpu_props.total_memory / (1024**3)
                    device_info['gpu_info'].append({
                        'id': i,
                        'name': gpu_props.name,
                        'vram_total': vram_gb,
                        'vram_available': vram_gb - (torch.cuda.memory_allocated(i) / (1024**3))
                    })
        except:
            pass
        
        # Check MPS (Apple Silicon)
        try:
            import torch
            if torch.backends.mps.is_available():
                device_info['mps'] = True
        except:
            pass
        
        self.device_info = device_info
        logger.info(f"[PC] Device capabilities detected:")
        logger.info(f"   [EMOJI] RAM: {device_info['total_ram']:.1f}GB total, {device_info['available_ram']:.1f}GB available")
        logger.info(f"   [GAME] CUDA: {'[OK]' if device_info['cuda'] else '[EMOJI]'}")
        logger.info(f"   [APPLE] MPS: {'[OK]' if device_info['mps'] else '[EMOJI]'}")
        
        for gpu in device_info['gpu_info']:
            logger.info(f"   [GAME] GPU {gpu['id']}: {gpu['name']} ({gpu['vram_total']:.1f}GB)")
    
    def _check_backend_availability(self):
        """Check availability của các Whisper backends"""
        for backend_name, backend_info in self.BACKEND_INFO.items():
            try:
                if backend_name == "openai":
                    import whisper
                    backend_info.available = True
                elif backend_name == "faster-whisper":
                    import faster_whisper
                    backend_info.available = True
                    
                logger.info(f"[OK] {backend_info.display_name} available")
                
            except ImportError:
                backend_info.available = False
                logger.info(f"[EMOJI] {backend_info.display_name} not available")
                logger.info(f"   Install with: {backend_info.installation_cmd}")
    
    def get_recommended_model(self, target_accuracy: str = "Better", 
                            max_vram: Optional[float] = None) -> str:
        """Get recommended model dựa trên constraints"""
        available_vram = max_vram or self._get_available_vram()
        
        # Filter models by VRAM constraint
        suitable_models = [
            model for name, model in self.MODEL_INFO.items()
            if model.vram_requirement <= available_vram
        ]
        
        if not suitable_models:
            return "tiny"  # Fallback
        
        # Filter by accuracy requirement
        if target_accuracy == "Good":
            accuracy_filter = ["Good", "Better", "Best"]
        elif target_accuracy == "Better":
            accuracy_filter = ["Better", "Best"]
        else:  # "Best"
            accuracy_filter = ["Best"]
        
        suitable_models = [
            model for model in suitable_models
            if model.accuracy in accuracy_filter
        ]
        
        if not suitable_models:
            suitable_models = [
                model for name, model in self.MODEL_INFO.items()
                if model.vram_requirement <= available_vram
            ]
        
        # Select best model (highest accuracy, then fastest)
        best_model = max(suitable_models, 
                        key=lambda m: (accuracy_filter.index(m.accuracy) if m.accuracy in accuracy_filter else 99, 
                                     m.relative_speed))
        
        return best_model.name
    
    def _get_available_vram(self) -> float:
        """Get available VRAM in GB"""
        if self.device_info['cuda'] and self.device_info['gpu_info']:
            return max(gpu['vram_available'] for gpu in self.device_info['gpu_info'])
        else:
            # Use RAM as fallback
            return self.device_info['available_ram']
    
    def load_model(self, model_size: Optional[str] = None, 
                   backend: Optional[str] = None) -> bool:
        """Load Whisper model với memory management"""
        model_size = model_size or self.config.model_size
        backend = backend or self.config.backend
        
        # Check if same model is already loaded
        if (self.current_model and 
            getattr(self.current_model, '_model_size', None) == model_size and
            self.current_backend == backend):
            logger.info(f"[EMOJI] Model {model_size} already loaded")
            return True
        
        # Cleanup existing model
        self.cleanup_model()
        
        logger.info(f"[EMOJI] Loading Whisper model: {model_size} ({backend})")
        
        # Check VRAM requirements
        model_info = self.MODEL_INFO.get(model_size)
        if model_info:
            available_vram = self._get_available_vram()
            if model_info.vram_requirement > available_vram:
                logger.warning(f"[WARNING] Model requires {model_info.vram_requirement:.1f}GB, only {available_vram:.1f}GB available")
                
                if self.config.auto_disable_if_low_memory:
                    logger.info("[REFRESH] Auto-selecting smaller model...")
                    model_size = self.get_recommended_model(max_vram=available_vram)
                    model_info = self.MODEL_INFO.get(model_size)
        
        try:
            start_time = time.time()
            
            # Generate unique model key
            model_key = f"whisper_{backend}_{model_size}_{self._get_optimal_device()}"
            
            # Check if model already exists in registry
            existing_model = model_registry.get_model(model_key)
            if existing_model:
                self.current_model = existing_model
                self.current_backend = backend
                logger.info(f"[EMOJI] Reusing Whisper model from registry: {model_key}")
                return
            
            # Load new model
            if backend == "faster-whisper":
                from faster_whisper import WhisperModel
                
                device = self._get_optimal_device()
                model = WhisperModel(
                    model_size, 
                    device=device,
                    compute_type=self.config.compute_type
                )
                
            else:  # openai
                import whisper
                model = whisper.load_model(model_size)
            
            # Register model in registry
            model_info = self.MODEL_INFO.get(model_size, None)
            memory_usage = model_info.vram_requirement if model_info else 2.0
            
            self.current_model = model_registry.register_model(
                model_key, 
                model, 
                "whisper", 
                memory_usage
            )
                
            load_time = time.time() - start_time
            
            # Store metadata
            self.current_model._model_size = model_size
            self.current_model._backend = backend
            self.current_backend = backend
            
            # Update stats
            self.stats['model_loads'] += 1
            logger.info(f"[OK] Loaded new Whisper model: {model_key} ({load_time:.1f}s)")
            
            # Start cleanup timer
            self._start_cleanup_timer()
            
            logger.info(f"[OK] Model loaded in {load_time:.2f}s")
            
            if model_info:
                logger.info(f"   [STATS] Model info: {model_info.parameters} parameters, {model_info.vram_requirement:.1f}GB VRAM")
                logger.info(f"   [TARGET] Accuracy: {model_info.accuracy}, Speed: {model_info.relative_speed:.1f}x")
            
            return True
            
        except Exception as e:
            logger.error(f"[EMOJI] Failed to load model {model_size}: {e}")
            return False
    
    def transcribe(self, audio_path: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Transcribe audio với performance monitoring"""
        if not self.current_model:
            if not self.load_model():
                raise Exception("Failed to load Whisper model")
        
        logger.debug(f"[EMOJI] Transcribing: {os.path.basename(audio_path)}")
        
        start_time = time.time()
        memory_before = self._get_memory_usage()
        
        try:
            if self.current_backend == "faster-whisper":
                segments, info = self.current_model.transcribe(
                    audio_path,
                    beam_size=self.config.beam_size,
                    temperature=self.config.temperature,
                    vad_filter=self.config.enable_vad,
                    **kwargs
                )
                
                transcription = " ".join([segment.text for segment in segments])
                metadata = {
                    'language': info.language,
                    'language_probability': info.language_probability,
                    'duration': info.duration
                }
                
            else:  # openai
                result = self.current_model.transcribe(
                    audio_path,
                    temperature=self.config.temperature,
                    **kwargs
                )
                
                transcription = result["text"]
                metadata = {
                    'language': result.get("language", "unknown"),
                    'segments': len(result.get("segments", [])),
                    'duration': sum(seg.get("end", 0) - seg.get("start", 0) 
                                  for seg in result.get("segments", []))
                }
            
            processing_time = time.time() - start_time
            memory_after = self._get_memory_usage()
            memory_peak = max(memory_before, memory_after)
            
            # Update stats
            self.stats['total_transcriptions'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['average_processing_speed'] = (
                metadata.get('duration', 0) / processing_time if processing_time > 0 else 0
            )
            self.stats['memory_usage_peak'] = max(self.stats['memory_usage_peak'], memory_peak)
            
            logger.debug(f"[OK] Transcription completed in {processing_time:.2f}s")
            logger.debug(f"   [EDIT] Text: '{transcription[:50]}...'")
            
            # Reset cleanup timer
            self._start_cleanup_timer()
            
            return transcription.strip(), metadata
            
        except Exception as e:
            logger.error(f"[EMOJI] Transcription failed: {e}")
            raise
    
    def _get_optimal_device(self) -> str:
        """Get optimal device cho Whisper"""
        if self.config.device != "auto":
            return self.config.device
            
        if self.device_info['cuda']:
            return "cuda"
        elif self.device_info['mps']:
            return "mps"
        else:
            return "cpu"
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in GB"""
        try:
            import torch
            if torch.cuda.is_available():
                return torch.cuda.memory_allocated() / (1024**3)
        except:
            pass
        
        # Fallback to system memory with psutil
        if PSUTIL_AVAILABLE:
            try:
                return (psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024**3)
            except Exception:
                pass
        
        # Ultimate fallback if psutil not available
        return 2.0  # GB estimate
    
    def _start_cleanup_timer(self):
        """Start/restart cleanup timer"""
        if not self.config.auto_cleanup:
            return
            
        # Cancel existing timer
        if self.cleanup_timer:
            self.cleanup_timer.cancel()
            
        # Start new timer
        self.cleanup_timer = threading.Timer(
            self.config.cleanup_timeout, 
            self.cleanup_model
        )
        self.cleanup_timer.start()
    
    def cleanup_model(self):
        """Cleanup Whisper model via model registry"""
        if not self.current_model:
            return
            
        logger.info("[CLEAN] Cleaning up Whisper model...")
        
        try:
            # Generate model key to unregister from registry
            if hasattr(self.current_model, '_model_size') and hasattr(self.current_model, '_backend'):
                model_size = self.current_model._model_size
                backend = self.current_model._backend
                model_key = f"whisper_{backend}_{model_size}_{self._get_optimal_device()}"
                
                # Unregister from model registry
                model_registry.unregister_model(model_key)
            
            # Clear local reference
            self.current_model = None
            self.current_backend = None
            
            # Cancel timer
            if self.cleanup_timer:
                self.cleanup_timer.cancel()
                self.cleanup_timer = None
            
            self.stats['cleanups_performed'] += 1
            logger.info("[OK] Whisper model cleanup completed")
            
        except Exception as e:
            logger.warning(f"[WARNING] Cleanup failed: {e}")
    
    def get_ui_display_info(self) -> Dict[str, Any]:
        """Get information để display trong UI"""
        current_model_info = None
        if self.current_model:
            model_size = getattr(self.current_model, '_model_size', 'unknown')
            current_model_info = self.MODEL_INFO.get(model_size)
        
        available_vram = self._get_available_vram()
        current_memory = self._get_memory_usage()
        
        return {
            'backend_info': {
                name: {
                    'display_name': info.display_name,
                    'available': info.available,
                    'description': info.description,
                    'pros': info.pros,
                    'cons': info.cons
                }
                for name, info in self.BACKEND_INFO.items()
            },
            'model_info': {
                name: {
                    'parameters': info.parameters,
                    'vram_requirement': info.vram_requirement,
                    'accuracy': info.accuracy,
                    'speed': info.relative_speed,
                    'recommended_use': info.recommended_use,
                    'can_load': info.vram_requirement <= available_vram
                }
                for name, info in self.MODEL_INFO.items()
            },
            'system_info': {
                'available_vram': available_vram,
                'current_memory_usage': current_memory,
                'memory_warning': current_memory > (available_vram * self.config.memory_warning_threshold),
                'device_capabilities': self.device_info
            },
            'current_model': {
                'loaded': self.current_model is not None,
                'model_size': getattr(self.current_model, '_model_size', None) if self.current_model else None,
                'backend': self.current_backend,
                'info': current_model_info.__dict__ if current_model_info else None
            },
            'stats': self.stats,
            'recommendations': {
                'recommended_model': self.get_recommended_model(),
                'can_auto_disable': self.config.auto_disable_if_low_memory,
                'should_show_warning': current_memory > (available_vram * self.config.memory_warning_threshold)
            }
        }
    
    def get_manager_report(self) -> Dict[str, Any]:
        """Get comprehensive report về Whisper manager"""
        return {
            'config': self.config.__dict__,
            'system': self.device_info,
            'backends': {name: info.__dict__ for name, info in self.BACKEND_INFO.items()},
            'models': {name: info.__dict__ for name, info in self.MODEL_INFO.items()},
            'current_state': {
                'model_loaded': self.current_model is not None,
                'current_backend': self.current_backend,
                'memory_usage': self._get_memory_usage()
            },
            'stats': self.stats,
            'ui_info': self.get_ui_display_info()
        }

# Convenience functions
def create_default_manager() -> WhisperManager:
    """Tạo manager với cấu hình mặc định"""
    return WhisperManager()

def create_performance_manager() -> WhisperManager:
    """Tạo manager tối ưu cho performance"""
    config = WhisperConfig(
        backend="faster-whisper",
        model_size="base",
        compute_type="int8",
        enable_vad=True,
        auto_cleanup=True,
        cleanup_timeout=180.0,  # 3 minutes
        show_vram_info=True
    )
    return WhisperManager(config)

def create_quality_manager() -> WhisperManager:
    """Tạo manager tối ưu cho quality"""
    config = WhisperConfig(
        backend="openai",
        model_size="medium",
        beam_size=10,
        temperature=0.0,
        auto_cleanup=False,  # Keep loaded for quality
        show_vram_info=True,
        auto_disable_if_low_memory=False  # Force quality
    )
    return WhisperManager(config)

if __name__ == "__main__":
    # Test the manager
    manager = create_default_manager()
    print("Whisper manager initialized")
    
    # Print UI display info
    ui_info = manager.get_ui_display_info()
    print(json.dumps(ui_info, indent=2, default=str)) 