#!/usr/bin/env python3
"""
[TARGET] MODEL REGISTRY
================

Global singleton registry để quản lý tất cả heavy AI models:
- Prevent duplicate model loading
- Centralized cleanup
- Memory monitoring
- Thread-safe operations
"""

import threading
import gc
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ModelInfo:
    """Information about a loaded model"""
    name: str
    model_type: str  # "chatterbox", "whisper", "other"
    instance: Any
    memory_usage: float  # GB
    loaded_at: datetime
    last_used: datetime
    reference_count: int = 1

class ModelRegistry:
    """
    [TARGET] GLOBAL MODEL REGISTRY
    ========================
    
    Singleton registry để quản lý tất cả heavy models:
    - Prevents duplicate loading
    - Centralized cleanup
    - Memory monitoring
    - Reference counting
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self._models: Dict[str, ModelInfo] = {}
        self._lock = threading.Lock()
        
        logger.info("[TARGET] Model Registry initialized")
    
    def register_model(self, key: str, model: Any, model_type: str, 
                      memory_usage: float = 0.0) -> Any:
        """
        Register a model in the registry
        Returns existing model if already registered, or registers new one
        """
        with self._lock:
            if key in self._models:
                # Model already exists, increment reference count
                self._models[key].reference_count += 1
                self._models[key].last_used = datetime.now()
                logger.info(f"[EMOJI] Reusing existing model: {key} (refs: {self._models[key].reference_count})")
                return self._models[key].instance
            
            # Register new model
            model_info = ModelInfo(
                name=key,
                model_type=model_type,
                instance=model,
                memory_usage=memory_usage,
                loaded_at=datetime.now(),
                last_used=datetime.now()
            )
            
            self._models[key] = model_info
            logger.info(f"[OK] Registered new model: {key} ({model_type}, {memory_usage:.1f}GB)")
            return model
    
    def get_model(self, key: str) -> Optional[Any]:
        """Get a model from registry if it exists"""
        with self._lock:
            if key in self._models:
                self._models[key].last_used = datetime.now()
                return self._models[key].instance
            return None
    
    def unregister_model(self, key: str) -> bool:
        """
        Decrease reference count and unregister model if no more references
        Returns True if model was completely removed
        """
        with self._lock:
            if key not in self._models:
                return False
            
            self._models[key].reference_count -= 1
            
            if self._models[key].reference_count <= 0:
                # No more references, cleanup model
                model_info = self._models.pop(key)
                try:
                    # Try to cleanup the model
                    if hasattr(model_info.instance, 'cleanup'):
                        model_info.instance.cleanup()
                    elif hasattr(model_info.instance, '__del__'):
                        del model_info.instance
                except Exception as e:
                    logger.warning(f"[WARNING] Cleanup error for {key}: {e}")
                
                logger.info(f"[DELETE] Removed model: {key}")
                return True
            else:
                logger.info(f"[EMOJI] Decreased ref count for {key}: {self._models[key].reference_count}")
                return False
    
    def cleanup_all(self):
        """Cleanup all models - for application shutdown"""
        with self._lock:
            logger.info("[CLEAN] Cleaning up all models...")
            
            for key, model_info in list(self._models.items()):
                try:
                    if hasattr(model_info.instance, 'cleanup'):
                        model_info.instance.cleanup()
                    elif hasattr(model_info.instance, '__del__'):
                        del model_info.instance
                except Exception as e:
                    logger.warning(f"[WARNING] Cleanup error for {key}: {e}")
            
            self._models.clear()
            
            # Clear CUDA cache
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    logger.info("[OK] CUDA cache cleared")
            except ImportError:
                pass
            except Exception as e:
                logger.warning(f"[WARNING] CUDA cleanup error: {e}")
            
            # Force garbage collection
            gc.collect()
            logger.info("[OK] All models cleaned up")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        with self._lock:
            total_memory = sum(model.memory_usage for model in self._models.values())
            model_count = len(self._models)
            
            models_by_type = {}
            for model in self._models.values():
                if model.model_type not in models_by_type:
                    models_by_type[model.model_type] = {'count': 0, 'memory': 0.0}
                models_by_type[model.model_type]['count'] += 1
                models_by_type[model.model_type]['memory'] += model.memory_usage
            
            return {
                'total_memory_gb': total_memory,
                'model_count': model_count,
                'models_by_type': models_by_type,
                'models': {k: {
                    'type': v.model_type,
                    'memory_gb': v.memory_usage,
                    'refs': v.reference_count,
                    'loaded_at': v.loaded_at.isoformat(),
                    'last_used': v.last_used.isoformat()
                } for k, v in self._models.items()}
            }
    
    def get_loaded_models(self) -> List[str]:
        """Get list of currently loaded model keys"""
        with self._lock:
            return list(self._models.keys())
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        return cls()

# Global registry instance
model_registry = ModelRegistry()