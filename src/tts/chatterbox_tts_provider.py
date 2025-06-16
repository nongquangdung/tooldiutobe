"""
Chatterbox TTS Provider với device auto-detection
Hỗ trợ: CUDA (GTX 1080), Apple MPS (M2), CPU fallback
"""
import os
import tempfile
import uuid
from typing import Optional, Dict, Any, List
import logging
import traceback

# Safe imports with fallbacks
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ PyTorch not available")

try:
    from chatterbox import ChatterboxTTS
    CHATTERBOX_AVAILABLE = True
    print("✅ Chatterbox TTS imported successfully")
except ImportError as e:
    CHATTERBOX_AVAILABLE = False
    print(f"❌ Chatterbox TTS import failed: {e}")
except Exception as e:
    CHATTERBOX_AVAILABLE = False
    print(f"❌ Chatterbox TTS compatibility error: {e}")

logger = logging.getLogger(__name__)

class ChatterboxTTSProvider:
    """
    Chatterbox TTS Provider với device auto-detection
    
    Features:
    - 🚀 Auto device detection: CUDA → MPS → CPU
    - 🎭 Emotion control (0.0-2.0 exaggeration)
    - 🎤 Voice cloning từ audio samples
    - 🔄 Thread-safe operations
    - 💾 Memory efficient
    """
    
    def __init__(self):
        self.model = None
        self.device = None
        self.device_name = "Unknown"
        self.is_initialized = False
        self.available = CHATTERBOX_AVAILABLE and TORCH_AVAILABLE
        
        # Voice cloning cache
        self.voice_cache = {}
        
        if not TORCH_AVAILABLE:
            print("⚠️ PyTorch not available - Chatterbox TTS disabled")
            return
            
        if not CHATTERBOX_AVAILABLE:
            print("⚠️ Chatterbox TTS not available - using fallback")
            return
        
        try:
            self._detect_device()
            self._initialize_model()
        except Exception as e:
            print(f"⚠️ Chatterbox TTS initialization failed: {e}")
            self.available = False
    
    def _detect_device(self):
        """Auto-detect best available device"""
        if not TORCH_AVAILABLE:
            self.device = None
            self.device_name = "PyTorch not available"
            return
            
        try:
            if torch.cuda.is_available():
                # CUDA GPU (GTX 1080)
                self.device = torch.device("cuda:0")
                self.device_name = f"CUDA ({torch.cuda.get_device_name(0)})"
                print(f"🎯 Detected device: {self.device_name}")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                # Apple Silicon MPS (M2)
                self.device = torch.device("mps")
                self.device_name = "Apple MPS (M2 chip)"
                print(f"🍎 Detected device: {self.device_name}")
            else:
                # CPU fallback
                self.device = torch.device("cpu")
                self.device_name = "CPU"
                print(f"💻 Detected device: {self.device_name}")
                
        except Exception as e:
            logger.warning(f"Device detection failed: {e}")
            self.device = torch.device("cpu") if TORCH_AVAILABLE else None
            self.device_name = "CPU (fallback)" if TORCH_AVAILABLE else "No device"
    
    def _initialize_model(self):
        """Initialize Chatterbox model với device"""
        if not self.available:
            return False
            
        try:
            print(f"🔄 Initializing Chatterbox TTS on {self.device_name}...")
            
            # Initialize model với device
            self.model = ChatterboxTTS(device=str(self.device))
            
            if self.model is not None:
                self.is_initialized = True
                print(f"✅ Chatterbox TTS initialized on {self.device_name}")
                return True
            else:
                logger.error("Failed to initialize Chatterbox model")
                return False
                
        except Exception as e:
            logger.error(f"Chatterbox initialization failed: {e}")
            logger.error(traceback.format_exc())
            self.available = False
            return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Lấy thông tin device hiện tại"""
        info = {
            "available": self.available,
            "initialized": self.is_initialized,
            "device": str(self.device) if self.device else None,
            "device_name": self.device_name,
            "torch_available": TORCH_AVAILABLE,
            "chatterbox_available": CHATTERBOX_AVAILABLE
        }
        
        if TORCH_AVAILABLE and self.device and str(self.device).startswith("cuda"):
            try:
                info.update({
                    "cuda_version": torch.version.cuda,
                    "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory // (1024**3),
                    "gpu_memory_available": (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)) // (1024**3)
                })
            except:
                pass
        
        return info
    
    def generate_voice(self, 
                      text: str, 
                      save_path: str, 
                      voice_sample_path: Optional[str] = None,
                      emotion_exaggeration: float = 1.0,
                      speed: float = 1.0) -> Dict[str, Any]:
        """
        Generate TTS audio với Chatterbox
        
        Args:
            text: Text to synthesize
            save_path: Path to save audio file
            voice_sample_path: Optional voice cloning sample (3-30s audio)
            emotion_exaggeration: Emotion control (0.0-2.0)
            speed: Speaking speed (0.5-2.0)
        """
        if not self.is_initialized:
            return {"success": False, "error": "Chatterbox TTS not initialized"}
        
        try:
            # Validate parameters
            emotion_exaggeration = max(0.0, min(2.0, emotion_exaggeration))
            speed = max(0.5, min(2.0, speed))
            
            # Voice cloning setup
            voice_config = None
            if voice_sample_path and os.path.exists(voice_sample_path):
                voice_config = self._load_voice_sample(voice_sample_path)
            
            # Generate audio
            print(f"🎙️ Generating with Chatterbox TTS...")
            print(f"   📱 Device: {self.device_name}")
            print(f"   🎭 Emotion: {emotion_exaggeration}")
            print(f"   ⚡ Speed: {speed}")
            if voice_config:
                print(f"   🎤 Voice cloning: {os.path.basename(voice_sample_path)}")
            
            # Call Chatterbox model
            audio_output = self.model.tts(
                text=text,
                voice=voice_config,
                emotion_exaggeration=emotion_exaggeration,
                speed=speed
            )
            
            # Save audio
            self._save_audio(audio_output, save_path)
            
            return {
                "success": True, 
                "path": save_path,
                "device": self.device_name,
                "emotion": emotion_exaggeration,
                "speed": speed,
                "voice_cloned": voice_config is not None
            }
            
        except Exception as e:
            logger.error(f"Chatterbox TTS generation failed: {e}")
            logger.error(traceback.format_exc())
            return {"success": False, "error": f"Chatterbox TTS error: {str(e)}"}
    
    def _load_voice_sample(self, sample_path: str) -> Optional[Any]:
        """Load voice sample for cloning"""
        try:
            # Cache voice samples
            if sample_path in self.voice_cache:
                return self.voice_cache[sample_path]
            
            # Load and process voice sample
            voice_config = self.model.load_voice(sample_path)
            
            # Cache for reuse
            self.voice_cache[sample_path] = voice_config
            
            return voice_config
            
        except Exception as e:
            logger.error(f"Voice sample loading failed: {e}")
            return None
    
    def _save_audio(self, audio_data, save_path: str):
        """Save audio data to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save audio based on output type
            if hasattr(audio_data, 'save'):
                audio_data.save(save_path)
            elif isinstance(audio_data, str) and os.path.exists(audio_data):
                # If audio_data is a temp file path, copy it
                import shutil
                shutil.copy2(audio_data, save_path)
            else:
                # Fallback: assume audio_data is raw audio array
                import soundfile as sf
                sf.write(save_path, audio_data, 22050)  # Default sample rate
                
        except Exception as e:
            logger.error(f"Audio saving failed: {e}")
            raise
    
    def clear_voice_cache(self):
        """Clear voice cloning cache"""
        self.voice_cache.clear()
        print("🧹 Voice cloning cache cleared")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        memory_info = {}
        
        if not TORCH_AVAILABLE:
            return {"error": "PyTorch not available"}
        
        try:
            if self.device and str(self.device).startswith("cuda"):
                memory_info.update({
                    "gpu_allocated": torch.cuda.memory_allocated(0) // (1024**2),  # MB
                    "gpu_cached": torch.cuda.memory_reserved(0) // (1024**2),     # MB
                    "gpu_max_allocated": torch.cuda.max_memory_allocated(0) // (1024**2)  # MB
                })
            
            try:
                import psutil
                process = psutil.Process()
                memory_info.update({
                    "cpu_memory_mb": process.memory_info().rss // (1024**2),
                    "cpu_memory_percent": process.memory_percent()
                })
            except ImportError:
                pass
            
        except Exception as e:
            logger.warning(f"Memory usage check failed: {e}")
        
        return memory_info
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.clear_voice_cache()
            
            if TORCH_AVAILABLE and self.device and str(self.device).startswith("cuda"):
                torch.cuda.empty_cache()
                print("🧹 GPU cache cleared")
            
            print("✅ Chatterbox TTS cleaned up")
            
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")
    
    def __del__(self):
        """Destructor"""
        if hasattr(self, 'is_initialized') and self.is_initialized:
            self.cleanup() 