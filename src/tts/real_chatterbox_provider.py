"""
Real Chatterbox TTS Provider
Chế độ thật sử dụng chatterbox-tts package chính thức
macOS Compatible - Auto fallback to demo mode
OPTIMIZED VERSION: 2-4x faster với torch compilation & mixed precision
"""
import os
import tempfile
import uuid
from typing import Optional, Dict, Any, List
import logging
import traceback
import threading
import platform

# Import optimized provider
try:
    from .optimized_chatterbox_provider import OptimizedChatterboxProvider
    OPTIMIZED_PROVIDER_AVAILABLE = True
    print("✅ OptimizedChatterboxProvider imported successfully")
except ImportError as e:
    OPTIMIZED_PROVIDER_AVAILABLE = False
    print(f"⚠️ OptimizedChatterboxProvider not available: {e}")

# Safe imports với fallbacks
try:
    import torch
    import torchaudio  # Required by ChatterboxTTS
    TORCH_AVAILABLE = True
    print(f"✅ PyTorch {torch.__version__} & torchaudio available")
    
    # Kiểm tra CUDA chi tiết
    if torch.cuda.is_available():
        print(f"✅ CUDA available: {torch.version.cuda}")
        print(f"✅ GPU count: {torch.cuda.device_count()}")
        print(f"✅ GPU name: {torch.cuda.get_device_name(0)}")
        print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory // (1024**3)}GB")
    else:
        print(f"❌ CUDA not available. Checking for CUDA installation...")
        print(f"   PyTorch built with CUDA: {torch.version.cuda is not None}")
        print(f"   Checking CUDA driver issues...")
        try:
            # Thử chạy CUDA init để xem lỗi chi tiết
            torch.cuda.init()
        except Exception as cuda_err:
            print(f"   CUDA initialization error: {cuda_err}")
            print(f"   Possible solutions:")
            print(f"   1. Install NVIDIA drivers: https://www.nvidia.com/Download/index.aspx")
            print(f"   2. Ensure PyTorch CUDA version matches installed CUDA")
            print(f"   3. Try: pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118")
except ImportError as e:
    TORCH_AVAILABLE = False
    print(f"⚠️ PyTorch/torchaudio not available: {e}")
    print("   Install with: pip install torch torchaudio")

# macOS Detection
IS_MACOS = platform.system() == "Darwin"
if IS_MACOS:
    print("🍎 macOS detected - will use CPU mode or demo fallback")

# Conditional import with proper error handling for cross-platform compatibility
ChatterboxTTS = None
CHATTERBOX_AVAILABLE = False

def _import_chatterbox_safely():
    """Safely import ChatterboxTTS với detailed error handling"""
    global ChatterboxTTS, CHATTERBOX_AVAILABLE
    
    if CHATTERBOX_AVAILABLE:
        return True  # Already imported successfully
    
    try:
        # Check Python version first 
        import sys
        python_version = sys.version_info
        
        if python_version < (3, 11):
            print(f"⚠️ Python {python_version.major}.{python_version.minor} detected")
            print(f"   ChatterboxTTS requires Python 3.11+ for typing.Self support")
            if IS_MACOS:
                print("🍎 macOS: Falling back to demo mode for compatibility")
            return False
            
        # Try to import from local chatterbox clone first (Windows dev environment)
        if not IS_MACOS:  # Only try local path on non-macOS
            chatterbox_path = r"D:\LearnCusor\BOTAY.COM\chatterbox\src"
            if chatterbox_path not in sys.path:
                sys.path.insert(0, chatterbox_path)
        
        from chatterbox.tts import ChatterboxTTS as _ChatterboxTTS
        ChatterboxTTS = _ChatterboxTTS
        CHATTERBOX_AVAILABLE = True
        print("✅ Real Chatterbox TTS imported successfully")
        return True
        
    except ImportError as e:
        try:
            # Fallback to installed package
            from chatterbox.tts import ChatterboxTTS as _ChatterboxTTS
            ChatterboxTTS = _ChatterboxTTS
            CHATTERBOX_AVAILABLE = True
            print("✅ Real Chatterbox TTS imported from installed package")
            return True
        except ImportError as e2:
            CHATTERBOX_AVAILABLE = False
            print(f"❌ Real Chatterbox TTS import failed: {e2}")
            if IS_MACOS:
                print("🍎 macOS: Will use demo mode instead")
                print("   💡 For real TTS: upgrade to Python 3.11+ or use demo mode")
            else:
                print(f"   💡 Try: pip install chatterbox-tts torch")
            return False
    except Exception as e:
        CHATTERBOX_AVAILABLE = False
        print(f"❌ Unexpected error importing ChatterboxTTS: {e}")
        return False

# Don't import at module level - defer to actual usage

logger = logging.getLogger(__name__)

class RealChatterboxProvider:
    """
    Real Chatterbox TTS Provider - macOS Compatible
    
    SINGLETON PATTERN: Chỉ có 1 instance duy nhất để tránh lãng phí resources
    
    Features:
    - 🚀 Real Chatterbox voice cloning (NVIDIA/Linux)
    - 🍎 macOS compatible demo mode
    - 🎛️ CFG weight control (real on GPU, simulated on CPU)
    - 🎭 Emotion exaggeration (real on GPU, simulated on CPU)
    - 💾 Auto device detection (CUDA/MPS/CPU)
    - 🔄 Thread-safe operations
    - 🎯 Singleton pattern
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation - thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("🔄 Creating new RealChatterboxProvider instance (Singleton)")
                    cls._instance = super(RealChatterboxProvider, cls).__new__(cls)
                    cls._instance._initialized = False
                else:
                    print("♻️ Reusing existing RealChatterboxProvider instance (Singleton)")
        else:
            print("♻️ Reusing existing RealChatterboxProvider instance (Singleton)")
        return cls._instance
    
    def __init__(self):
        # Chỉ initialize một lần duy nhất
        if self._initialized:
            return
            
        self.device = None
        self.device_name = "Unknown"
        self.is_initialized = False
        self.available = False  # Will be set based on actual capabilities
        self.chatterbox_model = None
        self.demo_mode = False
        
        # NEW: Optimized provider for 2-4x faster generation
        self.optimized_provider = None
        self.use_optimization = True  # Can be disabled via env var
        
        # Always initialize as available for macOS compatibility
        self.available = True
        
        try:
            self._detect_device()
            self._initialize_provider()
            self._initialize_optimized_provider()
        except Exception as e:
            print(f"⚠️ Real Chatterbox TTS initialization failed: {e}")
            print("🎯 Falling back to demo mode...")
            self.demo_mode = True
            self.is_initialized = True
            self.available = True  # Still available in demo mode
        
        self._initialized = True
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance - thread-safe"""
        return cls()
    
    def _initialize_optimized_provider(self):
        """Initialize optimized provider for 2-4x faster generation"""
        if not OPTIMIZED_PROVIDER_AVAILABLE:
            print("⚠️ Optimized provider not available, using standard provider")
            return
        
        # Check if optimization is disabled
        if os.getenv("DISABLE_OPTIMIZATION", "").lower() in ("true", "1", "yes"):
            print("🔄 Optimization disabled via DISABLE_OPTIMIZATION env var")
            self.use_optimization = False
            return
        
        # Only use optimization on CUDA devices for best results
        if self.device != "cuda":
            print(f"⚠️ Optimization works best on CUDA, current device: {self.device}")
            print("   Using standard provider for compatibility")
            self.use_optimization = False
            return
        
        try:
            print("🚀 Initializing OptimizedChatterboxProvider...")
            
            # Try to load settings from UI first, fall back to env vars
            optimization_settings = self._load_optimization_settings()
            
            dtype = optimization_settings.get("dtype", "float16")
            use_compilation = optimization_settings.get("compilation", True)
            cpu_offload = optimization_settings.get("cpu_offload", False)
            
            self.optimized_provider = OptimizedChatterboxProvider(
                device=self.device,
                dtype=dtype,
                use_compilation=use_compilation,
                cpu_offload=cpu_offload
            )
            
            print("✅ OptimizedChatterboxProvider initialized successfully!")
            print(f"   🎯 Optimization enabled: dtype={dtype}, compilation={use_compilation}")
            
        except Exception as e:
            print(f"❌ Failed to initialize OptimizedChatterboxProvider: {e}")
            self.optimized_provider = None
            self.use_optimization = False
    
    def _load_optimization_settings(self):
        """Load optimization settings from UI config file or environment variables"""
        settings = {
            "dtype": "float16",
            "compilation": True,
            "cpu_offload": False,
            "lazy_load": True,
            "chunked_processing": True,
            "chunk_size": 200,
            "voice_cache": True,
            "cache_size": 10
        }
        
        try:
            # Try to load from UI settings file first
            import json
            settings_file = os.path.join(os.getcwd(), "configs", "tts_optimization.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    ui_settings = json.load(f)
                    settings.update(ui_settings)
                    print(f"✅ Loaded UI optimization settings: {settings}")
                    return settings
        except Exception as e:
            print(f"⚠️ Could not load UI settings: {e}")
        
        # Fallback to environment variables
        try:
            env_settings = {
                "dtype": os.getenv("CHATTERBOX_DTYPE", "float16"),
                "compilation": os.getenv("CHATTERBOX_COMPILATION", "true").lower() in ("true", "1", "yes"),
                "cpu_offload": os.getenv("CHATTERBOX_CPU_OFFLOAD", "false").lower() in ("true", "1", "yes"),
                "lazy_load": os.getenv("CHATTERBOX_LAZY_LOAD", "true").lower() in ("true", "1", "yes"),
                "chunked_processing": os.getenv("CHATTERBOX_CHUNKED", "true").lower() in ("true", "1", "yes"),
                "chunk_size": int(os.getenv("CHATTERBOX_CHUNK_SIZE", "200")),
            }
            settings.update({k: v for k, v in env_settings.items() if v is not None})
            print(f"✅ Loaded environment optimization settings: {settings}")
        except Exception as e:
            print(f"⚠️ Error loading environment settings: {e}")
        
        return settings
    
    def _detect_device(self):
        """Auto-detect best available device, with optional FORCE_DEVICE env override"""
        # 1) Check override via env var
        force_device = os.getenv("FORCE_DEVICE", "").lower().strip()
        if force_device in {"cuda", "gpu"}:
            if TORCH_AVAILABLE and torch.cuda.is_available():
                self.device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
                self.device_name = f"GPU ({gpu_name}) - Real Chatterbox (FORCED)"
                print(f"⚡ FORCE_DEVICE override detected -> {self.device_name}")
                return
            else:
                print("⚠️ FORCE_DEVICE=cuda set nhưng không tìm thấy GPU khả dụng, bỏ qua override")
        elif force_device == "mps" and TORCH_AVAILABLE and hasattr(torch.backends, 'mps'):
            if torch.backends.mps.is_available():
                self.device = "mps"
                self.device_name = "Apple MPS - Real Chatterbox (FORCED)"
                print(f"🍎 FORCE_DEVICE override -> {self.device_name}")
                return
        elif force_device == "cpu":
            self.device = "cpu"
            self.device_name = "CPU - Real Chatterbox (FORCED)"
            print(f"💻 FORCE_DEVICE override -> {self.device_name}")
            return

        # 2) Auto detection như trước
        if not TORCH_AVAILABLE:
            self.device = "cpu"
            self.device_name = "CPU (Demo Mode - no PyTorch)"
            self.demo_mode = True
            return
            
        try:
            if torch.cuda.is_available():
                # CUDA GPU (any platform with NVIDIA)
                self.device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
                self.device_name = f"GPU ({gpu_name}) - Real Chatterbox"
                print(f"🎯 Real Chatterbox detected device: {self.device_name}")
                print(f"   🚀 GPU Memory: {torch.cuda.get_device_properties(0).total_memory // (1024**3)}GB")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available() and IS_MACOS:
                # Apple Silicon MPS - TRY REAL FIRST
                self.device = "mps"
                self.device_name = "Apple MPS - Real Chatterbox"
                print(f"🍎 macOS Apple Silicon: {self.device_name}")
                print("   🎯 Attempting real Chatterbox TTS on MPS...")
            else:
                # CPU - TRY REAL FIRST (including macOS Intel)
                self.device = "cpu"
                self.device_name = "CPU - Real Chatterbox"
                print(f"💻 CPU device: {self.device_name}")
                if IS_MACOS:
                    print("🍎 macOS CPU: Attempting real Chatterbox TTS...")
                
        except Exception as e:
            logger.warning(f"Device detection failed: {e}")
            self.device = "cpu"
            self.device_name = "CPU (Fallback)"
    
    def _initialize_provider(self):
        """Initialize provider with real Chatterbox TTS first, demo as fallback"""
        # Try to import ChatterboxTTS safely first
        chatterbox_import_success = _import_chatterbox_safely()
        
        if not chatterbox_import_success:
            print(f"⚠️ Chatterbox TTS not available - using demo mode")
            self.demo_mode = True
            self.is_initialized = True
            self.available = True
            return True
            
        try:
            print(f"🔄 Initializing Real Chatterbox TTS on {self.device_name}...")
            
            # TRY REAL CHATTERBOX ON ALL DEVICES (including macOS CPU)
            self.chatterbox_model = ChatterboxTTS.from_pretrained(device=self.device)
            
            print(f"✅ Real Chatterbox TTS ready on {self.device_name}")
            print("🎤 Real voice cloning available!")
            if IS_MACOS:
                print("🍎 macOS real Chatterbox TTS confirmed working!")
            
            self.is_initialized = True
            self.available = True
            self.demo_mode = False  # Real mode confirmed
            return True
                
        except Exception as e:
            logger.error(f"Real Chatterbox TTS initialization failed: {e}")
            print(f"⚠️ Falling back to demo mode: {e}")
            if IS_MACOS:
                print("🍎 macOS: Real TTS failed, using demo mode")
            
            self.demo_mode = True
            self.is_initialized = True
            self.available = True
            return True
    
    def get_device_info(self) -> Dict[str, Any]:
        """Lấy thông tin device hiện tại"""
        info = {
            "available": self.available,
            "initialized": self.is_initialized,
            "device": self.device,
            "device_name": self.device_name,
            "torch_available": TORCH_AVAILABLE,
            "chatterbox_available": CHATTERBOX_AVAILABLE,
            "provider_type": "Real Chatterbox TTS (Official)"
        }
        
        if TORCH_AVAILABLE and self.device == "cuda":
            try:
                info.update({
                    "cuda_version": torch.version.cuda,
                    "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory // (1024**3),
                    "gpu_memory_available": (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)) // (1024**3)
                })
            except:
                pass
        
        return info
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get comprehensive provider status với device info và optimization status"""
        basic_status = {
            'available': self.available,
            'initialized': self.is_initialized,
            'device': self.device,
            'device_name': self.device_name,
            'torch_available': TORCH_AVAILABLE,
            'chatterbox_available': CHATTERBOX_AVAILABLE,
            'provider_type': 'Real Chatterbox TTS (Official)',
            'cuda_version': torch.version.cuda if TORCH_AVAILABLE else None,
            **self.get_device_info()
        }
        
        # Add optimization status
        if self.optimized_provider:
            opt_status = self.optimized_provider.get_status()
            basic_status.update({
                'optimization_enabled': True,
                'optimization_details': opt_status,
                'provider_type': 'Real Chatterbox TTS (Optimized 2-4x faster)'
            })
        else:
            basic_status.update({
                'optimization_enabled': False,
                'optimization_reason': 'Not available or disabled'
            })
        
        return basic_status
    
<<<<<<< Updated upstream
=======
    def generate_voice_batch(self, batch_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate a batch of TTS audio files using Real Chatterbox.
        This is highly efficient on GPU.
        """
        if not self.is_initialized or self.demo_mode:
            # Fallback to generating one by one if not in real mode or not initialized
            print("Batch processing unavailable, falling back to sequential generation.")
            results = []
            for req in batch_requests:
                result = self.generate_voice(**req)
                results.append(result)
            return results

        print(f"[HOT] Generating batch of {len(batch_requests)} audio files with REAL Chatterbox TTS...")
        
        try:
            # Prepare data for the model
            texts = [req['text'] for req in batch_requests]
            
            # --- Core Batch Generation ---
            # Assuming the model's generate method can handle a list of texts
            wavs = self.chatterbox_model.generate(texts)
            # -----------------------------

            if wavs is None or len(wavs) != len(texts):
                raise RuntimeError("Batch generation did not return the expected number of waveforms.")

            results = []
            for i, req in enumerate(batch_requests):
                try:
                    wav = wavs[i]
                    save_path = req['save_path']
                    
                    import torchaudio as ta
                    save_dir = os.path.dirname(save_path)
                    if save_dir:
                        os.makedirs(save_dir, exist_ok=True)
                    
                    ta.save(save_path, wav, self.chatterbox_model.sr)
                    
                    results.append({
                        "success": True,
                        "audio_path": save_path,
                        "duration": wav.shape[-1] / self.chatterbox_model.sr
                    })
                except Exception as e:
                    print(f"Error saving file for segment {i}: {e}")
                    results.append({"success": False, "error": str(e)})
            
            print(f"[OK] Batch generation complete. {sum(1 for r in results if r['success'])}/{len(results)} files created.")
            return results

        except Exception as e:
            print(f"[EMOJI] ERROR: Real ChatterboxTTS batch generation failed: {e}")
            logger.error(traceback.format_exc())
            # Fallback to individual generation on batch failure
            print("Batch generation failed. Falling back to sequential generation.")
            results = []
            for req in batch_requests:
                result = self.generate_voice(**req)
                results.append(result)
            return results
        
>>>>>>> Stashed changes
    def generate_voice(self, 
                      text: str, 
                      save_path: str, 
                      voice_sample_path: Optional[str] = None,
                      emotion_exaggeration: float = 1.0,
                      speed: float = 1.0,
                      voice_name: Optional[str] = None,
                      cfg_weight: float = 0.5,
<<<<<<< Updated upstream
                      voice_prompt: Optional[str] = None) -> Dict[str, Any]:
=======
                      temperature: float = 0.7,  # NEW: Temperature parameter
                      voice_prompt: Optional[str] = None,
                      inner_voice: bool = False,  # NEW: Inner voice support
                      inner_voice_type: Optional[str] = None) -> Dict[str, Any]:
>>>>>>> Stashed changes
        """
        Generate TTS audio - Real Chatterbox on CUDA, Demo on macOS/CPU
        
        Args:
            text: Text to synthesize
            save_path: Path to save audio file
            voice_sample_path: Voice cloning sample (3-30s audio)
            emotion_exaggeration: Emotion control (0.0-2.0)
            speed: Speaking speed (0.5-2.0)
            voice_name: Voice name reference
            cfg_weight: CFG guidance weight (0.0-1.0)
            temperature: Temperature for voice variance (0.1-1.5)
            voice_prompt: Text prompt to describe desired voice characteristics
        """
        if not self.is_initialized:
            return {"success": False, "error": "Provider not initialized"}
        
        try:
<<<<<<< Updated upstream
=======
            # Apply emotion-to-parameter mapping if emotion provided
            if emotion and emotion != "neutral":
                mapped_exaggeration, mapped_cfg = self._map_emotion_to_parameters(emotion, emotion_exaggeration)
                print(f"   [THEATER] Emotion mapping: '{emotion}' -> exag={mapped_exaggeration:.2f}, cfg={mapped_cfg:.2f}")
                
                # Check if user has customized parameters (different from defaults)
                # If exaggeration is close to 1.0 (neutral) or exactly the mapped value, use mapping
                # Otherwise, assume user has customized and keep their values
                user_customized_exag = abs(emotion_exaggeration - 1.0) > 0.05 and abs(emotion_exaggeration - mapped_exaggeration) > 0.05
                user_customized_cfg = abs(cfg_weight - 0.6) > 0.05 and abs(cfg_weight - mapped_cfg) > 0.05
                
                if not user_customized_exag:
                    emotion_exaggeration = mapped_exaggeration
                    print(f"   [AUTO] Using mapped exaggeration: {mapped_exaggeration:.2f}")
                else:
                    print(f"   [USER] Keeping user exaggeration: {emotion_exaggeration:.2f} (customized)")
                    
                if not user_customized_cfg:
                    cfg_weight = mapped_cfg  
                    print(f"   [AUTO] Using mapped cfg_weight: {mapped_cfg:.2f}")
                else:
                    print(f"   [USER] Keeping user cfg_weight: {cfg_weight:.2f} (customized)")
            
>>>>>>> Stashed changes
            # Validate parameters
            emotion_exaggeration = max(0.0, min(2.0, emotion_exaggeration))
            speed = max(0.5, min(2.0, speed))
            cfg_weight = max(0.0, min(1.0, cfg_weight))
            temperature = max(0.1, min(1.5, temperature))
            
<<<<<<< Updated upstream
            if self.demo_mode:
                print(f"🎯 Generating with Demo Mode...")
                print(f"   📱 Device: {self.device_name}")
                print(f"   🎭 Emotion: {emotion_exaggeration} (simulated)")
                print(f"   ⚡ Speed: {speed}")
                print(f"   🎚️ CFG Weight: {cfg_weight} (simulated)")
=======
            # Apply inner voice effects if enabled
            if inner_voice and inner_voice_type:
                text = self._apply_inner_voice_effects(text, inner_voice_type)
                print(f"   [EMOJI] Inner voice: {inner_voice_type}")
            
            if self.demo_mode:
                print(f"Generating with Demo Mode...")
                print(f"   Device: {self.device_name}")
                print(f"   Emotion: {emotion} -> {emotion_exaggeration} (simulated)")
                print(f"   Speed: {speed}")
                print(f"   CFG Weight: {cfg_weight} (simulated)")
                print(f"   Temperature: {temperature} (simulated)")
>>>>>>> Stashed changes
                if IS_MACOS:
                    print(f"   🍎 macOS compatibility mode")
                
                # Create demo audio file for macOS compatibility
                return self._generate_demo_audio(
                    text=text,
                    save_path=save_path,
                    voice_name=voice_name,
                    emotion_exaggeration=emotion_exaggeration,
                    speed=speed,
                    cfg_weight=cfg_weight,
                    temperature=temperature,
                    voice_prompt=voice_prompt
                )
            
            else:
<<<<<<< Updated upstream
                print(f"🎙️ Generating with REAL Chatterbox TTS...")
                print(f"   📱 Device: {self.device_name}")
                print(f"   🎭 Emotion: {emotion_exaggeration} (REAL control)")
                print(f"   ⚡ Speed: {speed}")
                print(f"   🎚️ CFG Weight: {cfg_weight} (REAL cfg_weight!)")
=======
                print(f"Generating with REAL Chatterbox TTS...")
                print(f"   Device: {self.device_name}")
                print(f"   Emotion: {emotion} -> {emotion_exaggeration} (REAL control)")
                print(f"   Speed: {speed}")
                print(f"   CFG Weight: {cfg_weight} (REAL cfg_weight!)")
                print(f"   Temperature: {temperature} (REAL temperature!)")
>>>>>>> Stashed changes
                
                # Voice selection and setup
                selected_voice = self._resolve_voice_selection(voice_name)
                print(f"   🗣️ Voice: {selected_voice['name']} ({selected_voice['gender']})")
                
                # Voice cloning setup
                reference_audio = None
                if voice_sample_path and os.path.exists(voice_sample_path):
                    reference_audio = voice_sample_path
                    print(f"   🎤 Voice cloning: {os.path.basename(voice_sample_path)} (User-provided)")
                elif selected_voice.get('file_path') and os.path.exists(selected_voice['file_path']):
                    reference_audio = selected_voice['file_path']
                    print(f"   🎤 Voice cloning: {os.path.basename(reference_audio)} (Predefined voice)")
                
                # Generate real audio
                success = self._generate_real_chatterbox_audio(
                    text=text,
                    save_path=save_path,
                    reference_audio=reference_audio,
                    emotion_exaggeration=emotion_exaggeration,
                    speed=speed,
                    cfg_weight=cfg_weight,
                    temperature=temperature,
                    voice_prompt=voice_prompt
                )
                
                if success:
                    return {"success": True, "audio_path": save_path}
                else:
                    # Fallback to demo
<<<<<<< Updated upstream
                    print("⚠️ Real generation failed, falling back to demo")
                    return self._generate_demo_audio(text, save_path, voice_name, emotion_exaggeration, speed, cfg_weight, voice_prompt)
=======
                    print("WARNING: Real generation failed, falling back to demo")
                    return self._generate_demo_audio(text, save_path, voice_name, emotion, emotion_exaggeration, speed, cfg_weight, temperature, voice_prompt)
>>>>>>> Stashed changes
            
            # Return actual path (might be MP3 instead of WAV)
            actual_path = save_path
            if save_path.endswith('.wav') and os.path.exists(save_path.replace('.wav', '.mp3')):
                actual_path = save_path.replace('.wav', '.mp3')
                
            return {
                "success": True, 
                "path": actual_path,
                "device": self.device_name,
                "emotion": emotion_exaggeration,
                "speed": speed,
                "cfg_weight": cfg_weight,
                "voice_cloned": reference_audio is not None,
                "voice_id": selected_voice['id'],
                "voice_name": selected_voice['name'],
                "voice_gender": selected_voice['gender'],
                "provider": "Real Chatterbox TTS",
                "format": "MP3 (fallback - WAV requires ffmpeg)",
                "note": "Temporary fallback - parameters logged for real implementation"
            }
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            # Final fallback to demo
<<<<<<< Updated upstream
            print("⚠️ Generation failed, creating demo file...")
            return self._generate_demo_audio(text, save_path, voice_name, emotion_exaggeration, speed, cfg_weight, voice_prompt)
    
    def _generate_demo_audio(self, text: str, save_path: str, voice_name: Optional[str] = None,
                           emotion_exaggeration: float = 1.0, speed: float = 1.0, 
                           cfg_weight: float = 0.5, voice_prompt: Optional[str] = None) -> Dict[str, Any]:
=======
            print("WARNING: Generation failed, creating demo file...")
            return self._generate_demo_audio(text, save_path, voice_name, emotion, emotion_exaggeration, speed, cfg_weight, temperature, voice_prompt)
    
    def _generate_demo_audio(self, text: str, save_path: str, voice_name: Optional[str] = None,
                           emotion: str = "neutral", emotion_exaggeration: float = 1.0, speed: float = 1.0, 
                           cfg_weight: float = 0.5, temperature: float = 0.7, voice_prompt: Optional[str] = None) -> Dict[str, Any]:
>>>>>>> Stashed changes
        """Generate demo audio file for macOS compatibility"""
        try:
            # Normalize path and create directory if needed
            normalized_path = os.path.normpath(os.path.abspath(save_path))
            save_dir = os.path.dirname(normalized_path)
            os.makedirs(save_dir, exist_ok=True)
            
            # Create demo text file using normalized path
            demo_path = normalized_path.replace('.wav', '_real_chatterbox_demo.txt')
            with open(demo_path, 'w', encoding='utf-8') as f:
                f.write(f"🎯 Chatterbox TTS Demo Mode\n")
                f.write(f"{'='*50}\n")
                f.write(f"📱 Device: {self.device_name}\n")
                f.write(f"🍎 Platform: {'macOS' if IS_MACOS else 'Other'}\n")
                f.write(f"{'='*50}\n")
<<<<<<< Updated upstream
                f.write(f"📝 Text: {text}\n")
                f.write(f"🗣️ Voice: {voice_name or 'Default'}\n")
                f.write(f"🎭 Emotion: {emotion_exaggeration} (simulated)\n")
                f.write(f"⚡ Speed: {speed}\n")
                f.write(f"🎚️ CFG Weight: {cfg_weight} (simulated)\n")
=======
                f.write(f"Text: {text}\n")
                f.write(f"Voice: {voice_name or 'Default'}\n")
                f.write(f"Emotion: {emotion} (simulated)\n")
                f.write(f"Emotion Exaggeration: {emotion_exaggeration} (simulated)\n")
                f.write(f"Speed: {speed}\n")
                f.write(f"CFG Weight: {cfg_weight} (simulated)\n")
                f.write(f"Temperature: {temperature} (simulated)\n")
>>>>>>> Stashed changes
                if voice_prompt:
                    f.write(f"💬 Voice Prompt: {voice_prompt}\n")
                f.write(f"{'='*50}\n")
                f.write(f"ℹ️ This is a demo file created because:\n")
                if IS_MACOS:
                    f.write(f"   • Running on macOS (limited Chatterbox support)\n")
                if not CHATTERBOX_AVAILABLE:
                    f.write(f"   • Chatterbox TTS not installed\n")
                if not TORCH_AVAILABLE:
                    f.write(f"   • PyTorch not available\n")
                f.write(f"\n🎯 To get real TTS on GPU:\n")
                f.write(f"   1. Use Linux/Windows with NVIDIA GPU\n")
                f.write(f"   2. Install: pip install chatterbox-tts torch[cuda]\n")
                f.write(f"   3. Configure proper GPU drivers\n")
            
            print(f"✅ Demo file created: {demo_path}")
            
            # Also try to create a simple WAV file if possible
            try:
                import numpy as np
                import wave
                
                # Generate simple sine wave as placeholder
                sample_rate = 22050
                duration = min(3.0, len(text) * 0.1)  # Rough duration estimate
                t = np.linspace(0, duration, int(sample_rate * duration))
                frequency = 440  # A4 note
                audio_data = np.sin(2 * np.pi * frequency * t) * 0.1  # Low volume
                
                # Apply speed effect
                if speed != 1.0:
                    new_length = int(len(audio_data) / speed)
                    audio_data = np.interp(np.linspace(0, len(audio_data), new_length), 
                                         np.arange(len(audio_data)), audio_data)
                
                # Convert to 16-bit integers
                audio_data = (audio_data * 32767).astype(np.int16)
                
                # Save as WAV using normalized path
                with wave.open(normalized_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data.tobytes())
                
<<<<<<< Updated upstream
                print(f"✅ Placeholder audio created: {save_path}")
=======
                print(f"Placeholder audio created: {normalized_path}")
>>>>>>> Stashed changes
                
            except Exception as wav_error:
                print(f"⚠️ Could not create placeholder audio: {wav_error}")
            
            return {
                "success": True,
                "audio_path": normalized_path,
                "demo_mode": True,
                "demo_file": demo_path,
                "message": f"Demo mode active on {self.device_name}"
            }
            
        except Exception as e:
            logger.error(f"Demo audio generation failed: {e}")
            return {"success": False, "error": f"Demo generation failed: {str(e)}"}
    
    def _resolve_voice_selection(self, voice_name: Optional[str]) -> Dict[str, str]:
        """
        Resolve voice selection from voice_name parameter
        Returns voice info including file path for voice cloning
        """
        available_voices = self.get_available_voices()
        
<<<<<<< Updated upstream
        # If no voice specified, use default
        if not voice_name:
            return available_voices[0]  # Default to first voice
        
        # Direct voice ID match - THÊM VOICE FILE PATH
=======
        # Loại bỏ mọi path và extension để tránh mismatch (e.g., "voices/Alice.wav" → "alice")
        voice_name_clean = voice_name.strip().lower() if voice_name else ""

        # Nếu bao gồm path, lấy basename
        if voice_name_clean and ("/" in voice_name_clean or "\\" in voice_name_clean):
            voice_name_clean = os.path.basename(voice_name_clean)

        # Loại bỏ đuôi .wav nếu có
        if voice_name_clean.endswith('.wav'):
            voice_name_clean = voice_name_clean[:-4]

        # Debug log để quan sát kết quả làm sạch
        print(f"Resolving voice for requested name: '{voice_name}' -> cleaned: '{voice_name_clean}'")

        # Nếu user không chỉ định, dùng giọng đầu tiên
        if not voice_name_clean:
            return available_voices[0]

        # 1) Khớp chính xác (case-insensitive) – sử dụng dict mapping để tránh bỏ sót
        try:
            from tts.chatterbox_voices_integration import ChatterboxVoicesManager
            voices_manager = ChatterboxVoicesManager()
            voices_map = voices_manager.get_available_voices()  # key: id (lowercase)
            if voice_name_clean in voices_map:
                voice_info_obj = voices_map[voice_name_clean]
                # Chuyển về dict để đồng bộ với available_voices format
                selected_voice = {
                    "id": voice_info_obj.voice_id,
                    "name": voice_info_obj.name,
                    "gender": voice_info_obj.gender,
                    "description": voice_info_obj.description,
                }

                # Tìm file wav theo 3 biến thể tên
                variations = [
                    f"{voice_name_clean}.wav",
                    f"{voice_name_clean.capitalize()}.wav",
                    f"{voice_name_clean.upper()}.wav",
                ]
                for var in variations:
                    candidate = voices_manager.voices_directory / var
                    if candidate.exists():
                        selected_voice["file_path"] = str(candidate)
                        print(f"Voice found: {selected_voice['name']} -> {candidate}")
                        break
                else:
                    print(f"WARNING: Voice file not found for '{voice_name_clean}', tried {variations}")

                return selected_voice
            else:
                print(f"WARNING: Voice '{voice_name_clean}' NOT found in predefined voices. Available IDs: {', '.join(sorted(voices_map.keys()))}")

        except Exception as e:
            print(f"WARNING: Voice lookup error: {e}")

        # 2) Khớp một phần (contains) – ví dụ user gõ "alex" vẫn ra "alexander"
>>>>>>> Stashed changes
        for voice in available_voices:
            if voice['id'] == voice_name:
                # Load voice file path từ ChatterboxVoicesManager
                try:
                    import sys
                    import os
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
                    
                    from .chatterbox_voices_integration import ChatterboxVoicesManager
                    voices_manager = ChatterboxVoicesManager()
                    available_voices = voices_manager.get_available_voices()
                    
                    if voice_name in available_voices:
                        voice_info = available_voices[voice_name]
                        # Try both lowercase and capitalize case for file name
                        voice_file_path_lower = str(voices_manager.voices_directory / f"{voice_name}.wav")
                        voice_file_path_capital = str(voices_manager.voices_directory / f"{voice_name.capitalize()}.wav")
                        
                        if os.path.exists(voice_file_path_lower):
                            voice['file_path'] = voice_file_path_lower
                            print(f"🎤 Voice found: {voice['name']} → {voice_file_path_lower}")
                        elif os.path.exists(voice_file_path_capital):
                            voice['file_path'] = voice_file_path_capital
                            print(f"🎤 Voice found: {voice['name']} → {voice_file_path_capital}")
                        else:
                            print(f"⚠️ Voice file not found for: {voice_name} (tried {voice_file_path_lower} and {voice_file_path_capital})")
                    else:
                        print(f"⚠️ Voice file not found for: {voice_name}")
                        
                except Exception as e:
                    print(f"⚠️ Error loading voice file for {voice_name}: {e}")
                
                return voice
        
        # Gender-based matching (for integration with other TTS providers)
        voice_lower = voice_name.lower()
        
        if any(keyword in voice_lower for keyword in ['female', 'nữ', 'woman', 'girl']):
            # Find female voice
            female_voices = [v for v in available_voices if v['gender'] == 'female']
            if female_voices:
                return female_voices[0]  # Use first female voice
                
        elif any(keyword in voice_lower for keyword in ['male', 'nam', 'man', 'boy']):
            # Find male voice
            male_voices = [v for v in available_voices if v['gender'] == 'male']
            if male_voices:
                return male_voices[0]  # Use first male voice
                
        elif any(keyword in voice_lower for keyword in ['neutral', 'narrator', 'trung tính']):
            # Find neutral voice
            neutral_voices = [v for v in available_voices if v['gender'] == 'neutral']
            if neutral_voices:
                return neutral_voices[0]  # Use first neutral voice
        
        # Vietnamese voice mapping (for compatibility with Google TTS voices)
        vietnamese_voice_mapping = {
            'vi-vn-standard-a': 'female_young',
            'vi-vn-standard-b': 'male_young', 
            'vi-vn-standard-c': 'female_mature',
            'vi-vn-standard-d': 'male_mature',
            'vi-vn-wavenet-a': 'female_gentle',
            'vi-vn-wavenet-b': 'male_deep',
            'vi-vn-wavenet-c': 'female_mature',
            'vi-vn-wavenet-d': 'male_mature'
        }
        
        # Try Vietnamese voice mapping
        voice_clean = voice_name.lower().replace('-', '').replace('_', '')
        for vn_voice, chatterbox_voice in vietnamese_voice_mapping.items():
            if vn_voice.replace('-', '') in voice_clean:
                for voice in available_voices:
                    if voice['id'] == chatterbox_voice:
                        return voice
        
        # Fallback to first available voice
        print(f"⚠️ Voice '{voice_name}' không tìm thấy, dùng default")
        return available_voices[0]
    
<<<<<<< Updated upstream
=======
    def clear_voice_embedding_cache(self):
        """Xóa bộ đệm embedding giọng nói trong bộ nhớ."""
        count = len(self.voice_embedding_cache)
        self.voice_embedding_cache.clear()
        print(f"[OK] Đã xóa {count} mục khỏi bộ đệm embedding giọng nói.")

>>>>>>> Stashed changes
    def _generate_real_chatterbox_audio(self, 
                                       text: str, 
                                       save_path: str,
                                       reference_audio: Optional[str] = None,
                                       emotion_exaggeration: float = 1.0,
                                       speed: float = 1.0,
                                       cfg_weight: float = 0.5,
                                       temperature: float = 0.7,
                                       voice_prompt: Optional[str] = None) -> bool:
        """Generate audio using REAL ChatterboxTTS"""
        try:
            print(f"🎤 Real ChatterboxTTS generation starting...")
            print(f"   📝 Text: '{text[:50]}...'")
            print(f"   🎭 Emotion (exaggeration): {emotion_exaggeration}")
            print(f"   ⚡ Speed: {speed}")
            print(f"   🎚️ CFG Weight: {cfg_weight}")
            
            # NOTE: ChatterboxTTS không hỗ trợ voice_prompt text trực tiếp
            # Chỉ hỗ trợ: 1) Default voice, 2) Voice cloning với audio file
            if voice_prompt:
                print(f"⚠️ Voice prompt '{voice_prompt}' được bỏ qua - ChatterboxTTS không hỗ trợ text prompt")
                print(f"   💡 Gợi ý: Sử dụng Voice Clone mode với audio mẫu thay thế")
            
<<<<<<< Updated upstream
            # Generate audio với real ChatterboxTTS API
            if reference_audio and os.path.exists(reference_audio):
                print(f"🎤 Using voice cloning: {os.path.basename(reference_audio)}")
                # Voice cloning mode với parameters
=======
            # === Voice selection logic ===
            if reference_audio and os.path.exists(reference_audio):
                # Voice cloning mode
                print(f"Using voice cloning: {os.path.basename(reference_audio)}")

                # --- VOICE EMBEDDING CACHE LOGIC (placeholder) ---
                # TODO: implement embedding cache to avoid recomputation

>>>>>>> Stashed changes
                wav = self.chatterbox_model.generate(
                    text, 
                    audio_prompt_path=reference_audio,
                    exaggeration=emotion_exaggeration,
<<<<<<< Updated upstream
                    cfg_weight=cfg_weight
=======
                    cfg_weight=cfg_weight,
                    temperature=temperature
>>>>>>> Stashed changes
                )
            else:
                print(f"🗣️ Using default voice")
                # Default voice mode với parameters
                wav = self.chatterbox_model.generate(
                    text,
                    exaggeration=emotion_exaggeration,
                    cfg_weight=cfg_weight,
                    temperature=temperature
                )
            
            # Save audio file using torchaudio
            if wav is not None:
                try:
                    import torchaudio as ta
                    # Ensure directory exists và normalize path
                    normalized_path = os.path.normpath(os.path.abspath(save_path))
                    save_dir = os.path.dirname(normalized_path)
                    if save_dir:
                        os.makedirs(save_dir, exist_ok=True)
                    
                    # Save audio với sample rate từ model
<<<<<<< Updated upstream
                    ta.save(save_path, wav, self.chatterbox_model.sr)
                    print(f"✅ Real ChatterboxTTS audio saved: {save_path}")
                    print(f"   📊 Sample rate: {self.chatterbox_model.sr}")
                    print(f"   📏 Duration: {wav.shape[-1] / self.chatterbox_model.sr:.2f}s")
=======
                    ta.save(normalized_path, wav, self.chatterbox_model.sr)
                    print(f"Real ChatterboxTTS audio saved: {save_path}")
                    print(f"   Sample rate: {self.chatterbox_model.sr}")
                    print(f"   Duration: {wav.shape[-1] / self.chatterbox_model.sr:.2f}s")
>>>>>>> Stashed changes
                    return True
                except ImportError:
                    print("❌ torchaudio not available for saving audio")
                    return False
            else:
                print("❌ Real ChatterboxTTS returned no audio data")
                return False
                
        except Exception as e:
            print(f"❌ Real ChatterboxTTS generation failed: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def _generate_fallback_audio(self, text: str, save_path: str, speed: float = 1.0, voice_info: Dict = None) -> bool:
        """
        Generate actual audio using gTTS as fallback while developing real Chatterbox
        Simulates voice selection by adjusting audio parameters
        """
        try:
            from gtts import gTTS
            
            print(f"🎵 Generating fallback audio với gTTS...")
            
            # Voice simulation log
            if voice_info:
                print(f"   🎭 Simulating {voice_info['name']} ({voice_info['gender']})")
                print(f"   📝 Note: Real implementation would use voice model: {voice_info['id']}")
            
            # Detect language
            lang = 'vi' if any(char in text for char in 'àáãạảăắằẳẵặâấầẩẫậđèéẹẻẽêềếểễệìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳýỵỷỹ') else 'en'
            
            # Adjust speed based on voice type (simulation)
            if voice_info:
                # Simulate voice characteristics with speed adjustment
                if voice_info['gender'] == 'male':
                    speed *= 0.95  # Slightly slower for male voices
                elif voice_info['gender'] == 'female' and 'young' in voice_info['id']:
                    speed *= 1.05  # Slightly faster for young female voices
                elif 'child' in voice_info['id']:
                    speed *= 1.1   # Faster for child voices
                elif 'elder' in voice_info['id']:
                    speed *= 0.9   # Slower for elder voices
            
            # Generate TTS (use slow=True if speed < 1.0)
            use_slow = speed < 1.0
            tts = gTTS(text=text, lang=lang, slow=use_slow)
            
            # Save directly as MP3 first, then try to convert to WAV
            if save_path.endswith('.wav'):
                mp3_path = save_path.replace('.wav', '.mp3')
            else:
                mp3_path = save_path
            
            tts.save(mp3_path)
            
            # For now, just use MP3 since ffmpeg not available
            if save_path.endswith('.wav'):
                print(f"⚠️ Saving as MP3 instead of WAV (ffmpeg not available): {mp3_path}")
            print(f"✅ Fallback audio saved as MP3: {mp3_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Fallback audio generation failed: {e}")
            logger.error(f"Fallback audio generation failed: {e}")
            return False
    
    def _save_audio(self, audio_data, save_path: str):
        """Save audio data to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save audio (format depends on chatterbox-tts API)
            if hasattr(audio_data, 'save'):
                audio_data.save(save_path)
            elif hasattr(audio_data, 'export'):
                audio_data.export(save_path, format="wav")
            else:
                # Fallback: assume numpy array
                import soundfile as sf
                sf.write(save_path, audio_data, 22050)  # Standard sample rate
                
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        memory_info = {
            "provider": "Real Chatterbox TTS",
            "available": self.available,
            "initialized": self.is_initialized
        }
        
        if TORCH_AVAILABLE and self.device == "cuda":
            try:
                memory_info.update({
                    "gpu_memory_allocated": torch.cuda.memory_allocated(0) // (1024**2),  # MB
                    "gpu_memory_cached": torch.cuda.memory_reserved(0) // (1024**2),  # MB
                    "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory // (1024**2)  # MB
                })
            except:
                pass
        
        return memory_info
    
    def cleanup(self):
        """
        Cleanup Real Chatterbox TTS resources
        CẢNH BÁO: Với Singleton pattern, cleanup sẽ ảnh hưởng đến tất cả instances
        """
        try:
            if self.chatterbox_model:
                # Clear model from memory
                del self.chatterbox_model
                self.chatterbox_model = None
                
            if TORCH_AVAILABLE and self.device == "cuda":
                torch.cuda.empty_cache()
                
            self.is_initialized = False
            print("🧹 Real Chatterbox TTS cleaned up (Singleton)")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def soft_cleanup(self):
        """
        Soft cleanup - chỉ dọn dẹp cache, không destroy model
        An toàn hơn cho Singleton pattern
        """
        try:
            if TORCH_AVAILABLE and self.device == "cuda":
                torch.cuda.empty_cache()
                print("🧹 Real Chatterbox CUDA cache cleared (Singleton safe)")
        except Exception as e:
            logger.warning(f"Real Chatterbox soft cleanup warning: {e}")
    
    def __del__(self):
        """
        Destructor - không cleanup với Singleton pattern
        Để tránh destroy shared instance
        """
        pass
    
    def clear_voice_cache(self):
        """Clear voice cache"""
        if TORCH_AVAILABLE and self.device == "cuda":
            torch.cuda.empty_cache()
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get available voices - use 28 predefined voices from voices/ directory"""
        try:
            # Load voices từ ChatterboxVoicesManager
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
            
            from tts.chatterbox_voices_integration import ChatterboxVoicesManager
            voices_manager = ChatterboxVoicesManager()
            
            available_chatterbox_voices = voices_manager.get_available_voices()
            
            # Convert to format expected by RealChatterboxProvider
            available_voices = []
            for voice_id, voice_data in available_chatterbox_voices.items():
                available_voices.append({
                    "id": voice_id,
                    "name": voice_data.name,
                    "gender": voice_data.gender,
                    "description": f"Predefined voice: {voice_data.name} ({voice_data.gender})"
                })
            
            print(f"🎙️ Loaded {len(available_voices)} predefined voices từ ChatterboxVoicesManager")
            return available_voices
            
        except Exception as e:
            print(f"⚠️ Failed to load predefined voices: {e}")
            # Fallback to basic voices if loading fails
            return [
                # Female voices
                {"id": "female_young", "name": "Young Female", "gender": "female", "description": "Giọng nữ trẻ, tươi tắn"},
                {"id": "female_mature", "name": "Mature Female", "gender": "female", "description": "Giọng nữ trưởng thành, ấm áp"},
                {"id": "female_gentle", "name": "Gentle Female", "gender": "female", "description": "Giọng nữ dịu dàng"},
                
                # Male voices  
                {"id": "male_young", "name": "Young Male", "gender": "male", "description": "Giọng nam trẻ, năng động"},
                {"id": "male_mature", "name": "Mature Male", "gender": "male", "description": "Giọng nam trưởng thành, uy tín"},
                {"id": "male_deep", "name": "Deep Male", "gender": "male", "description": "Giọng nam trầm, khỏe khoắn"},
                
                # Neutral/Character voices
                {"id": "neutral_narrator", "name": "Narrator", "gender": "neutral", "description": "Giọng kể chuyện trung tính"},
                {"id": "neutral_child", "name": "Child Voice", "gender": "neutral", "description": "Giọng trẻ em"},
                {"id": "neutral_elder", "name": "Elder Voice", "gender": "neutral", "description": "Giọng người lớn tuổi"},
                
                # Voice cloning
                {"id": "cloned", "name": "Voice Cloning", "gender": "variable", "description": "Nhân bản giọng từ mẫu audio"}
            ] 