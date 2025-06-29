#!/usr/bin/env python3
"""
🔇 SUPPRESS ML LIBRARY WARNINGS
==============================
Script để suppress các deprecation warnings từ PyTorch và Transformers
"""

import warnings
import os

def suppress_all_ml_warnings():
    """Suppress tất cả ML library warnings"""
    
    # PyTorch warnings
    warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
    warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="torch")
    
    # Specific warning messages
    warnings.filterwarnings("ignore", message=".*sdp_kernel.*deprecated.*")
    warnings.filterwarnings("ignore", message=".*LlamaSdpaAttention.*")
    warnings.filterwarnings("ignore", message=".*past_key_values.*tuple.*deprecated.*")
    warnings.filterwarnings("ignore", message=".*TOKENIZERS_PARALLELISM.*")
    
    # Environment variables
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["PYTORCH_DISABLE_DEPRECATED_WARNING"] = "1"
    
    print("🔇 All ML library warnings suppressed!")

if __name__ == "__main__":
    suppress_all_ml_warnings()
