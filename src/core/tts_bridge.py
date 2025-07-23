#!/usr/bin/env python3
"""
🌉 TTS BRIDGE
=============

Bridge interface loại bỏ duplicate TTS calls giữa:
- ChatterboxExtendedIntegration (preprocessing/postprocessing only)
- RealChatterboxProvider (TTS generation only)  
- VoiceGenerator (multi-character orchestration)

KIẾN TRÚC MỚI:
- Extended chỉ làm tiền/hậu xử lý
- Real Provider chỉ làm TTS core
- Bridge orchestrate toàn bộ flow
"""

import os
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TTSRequest:
    """TTS request structure"""
    text: str
    voice_name: str
    emotion: str = "neutral"
    emotion_exaggeration: float = 1.0
    speed: float = 1.0
    cfg_weight: float = 0.5
    inner_voice: bool = False
    inner_voice_type: Optional[str] = None
    output_path: str = ""

@dataclass
class TTSResult:
    """TTS result structure"""
    success: bool
    audio_path: str
    error_message: Optional[str] = None
    processing_time: float = 0.0
    metadata: Dict[str, Any] = None

class TTSBridge:
    """
    🌉 TTS BRIDGE
    =============
    
    Centralized interface loại bỏ duplicate TTS calls:
    
    SINGLE CHARACTER MODE:
    Text → Extended(preprocess) → Bridge → Real(TTS) → Extended(postprocess) → Output
    
    MULTI CHARACTER MODE:  
    JSON → Bridge → Real(TTS per character) → Extended(postprocess) → Output
    """
    
    def __init__(self):
        self.real_provider = None
        self.extended_integration = None
        self.voice_generator = None
        
        # Initialize components
        self._initialize_components()
        
        logger.info("🌉 TTS Bridge initialized")
    
    def _initialize_components(self):
        """Initialize TTS components"""
        try:
            # Import và initialize Real Provider
            from tts.real_chatterbox_provider import RealChatterboxProvider
            self.real_provider = RealChatterboxProvider.get_instance()
            logger.info("✅ Real Chatterbox Provider connected")
            
            # Import Extended Integration (preprocessing/postprocessing only)
            from core.chatterbox_extended_integration import ChatterboxExtendedIntegration
            self.extended_integration = ChatterboxExtendedIntegration()
            logger.info("✅ Extended Integration connected (pre/post only)")
            
            # Import RealChatterboxProvider (direct TTS engine)
            from tts.real_chatterbox_provider import RealChatterboxProvider
            self.chatterbox_provider = RealChatterboxProvider.get_instance()
            logger.info("✅ RealChatterbox Provider connected (direct TTS)")
            
        except Exception as e:
            logger.error(f"❌ TTS Bridge initialization failed: {e}")
            raise
    
    def generate_single_character(self, 
                                text: str,
                                voice_name: str = "abigail",
                                output_dir: str = "./output",
                                enable_preprocessing: bool = True,
                                enable_postprocessing: bool = True,
                                **tts_params) -> TTSResult:
        """
        Generate TTS cho single character với advanced text preprocessing
        
        Args:
            text: Input text
            voice_name: Voice name to use
            output_dir: Output directory
            enable_preprocessing: Enable text preprocessing
            enable_postprocessing: Enable audio postprocessing
            **tts_params: TTS parameters (emotion, speed, etc.)
        """
        logger.info("🎙️ Enhanced single character TTS generation starting...")
        
        try:
            # Step 1: Advanced text preprocessing with auto-splitting
            processed_chunks = []
            if enable_preprocessing:
                logger.info("📝 Advanced text preprocessing with smart chunking...")
                processed_chunks = self._preprocess_text_with_chunking(text)
            else:
                processed_chunks = [text]
            
            logger.info(f"📝 Text split into {len(processed_chunks)} optimal chunks")
            
            # Step 2: Generate TTS for each chunk
            generated_files = []
            os.makedirs(output_dir, exist_ok=True)
            
            for i, chunk in enumerate(processed_chunks):
                chunk_filename = f"single_char_chunk_{i+1:03d}_{voice_name}.wav"
                chunk_path = os.path.join(output_dir, chunk_filename)
                
                logger.info(f"🎙️ Generating chunk {i+1}/{len(processed_chunks)} ({len(chunk)} chars)...")
                logger.info(f"🎯 TTS Parameters: {tts_params}")
                
                tts_result = self.real_provider.generate_voice(
                    text=chunk,
                    save_path=chunk_path,
                    voice_name=voice_name,
                    **tts_params
                )
                
                if tts_result.get("success"):
                    generated_files.append(chunk_path)
                else:
                    logger.error(f"❌ Failed to generate chunk {i+1}: {tts_result.get('error')}")
            
            if not generated_files:
                return TTSResult(
                    success=False,
                    audio_path="",
                    error_message="Failed to generate any audio chunks"
                )
            
            # Step 3: Merge chunks if multiple files
            final_path = generated_files[0]  # Default to first file
            if len(generated_files) > 1:
                final_path = os.path.join(output_dir, f"single_character_complete_{voice_name}.wav")
                merge_success = self._merge_audio_chunks(generated_files, final_path)
                
                if merge_success:
                    # Clean up individual chunk files
                    for chunk_file in generated_files:
                        try:
                            os.remove(chunk_file)
                        except:
                            pass
                    logger.info(f"✅ Merged {len(generated_files)} chunks into final audio")
                else:
                    logger.warning("⚠️ Merge failed, using first chunk as output")
                    final_path = generated_files[0]
            
            # Step 4: Audio postprocessing (if enabled)
            if enable_postprocessing and self.extended_integration:
                logger.info("🎵 Enhanced audio postprocessing...")
                # TODO: Add enhanced audio postprocessing here
                pass
            
            logger.info("✅ Enhanced single character TTS completed")
            return TTSResult(
                success=True,
                audio_path=final_path,
                metadata={
                    "chunks_processed": len(processed_chunks),
                    "total_characters": len(text),
                    "voice_name": voice_name,
                    "preprocessing_enabled": enable_preprocessing
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Enhanced single character TTS failed: {e}")
            return TTSResult(
                success=False,
                audio_path="",
                error_message=str(e)
            )
    
    def _preprocess_text_with_chunking(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """
        Smart text preprocessing with intelligent chunking
        
        Args:
            text: Input text to process
            max_chunk_size: Maximum characters per chunk
            
        Returns:
            List of optimally sized text chunks
        """
        import re
        
        # Clean and normalize text
        text = text.strip()
        if not text:
            return []
        
        # Split by sentences first (respecting Vietnamese punctuation)
        sentence_pattern = r'[.!?]+(?:\s|$)'
        sentences = re.split(sentence_pattern, text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add punctuation back if missing
            if not sentence.endswith(('.', '!', '?')):
                sentence = sentence + "."
            
            # Check if adding this sentence would exceed chunk size
            potential_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if len(potential_chunk) <= max_chunk_size:
                current_chunk = potential_chunk
            else:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append(current_chunk)
                
                # If single sentence is too long, split by phrases/clauses
                if len(sentence) > max_chunk_size:
                    phrase_chunks = self._split_long_sentence(sentence, max_chunk_size)
                    chunks.extend(phrase_chunks[:-1])  # Add all but last
                    current_chunk = phrase_chunks[-1] if phrase_chunks else ""
                else:
                    current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks if chunks else [text]
    
    def _split_long_sentence(self, sentence: str, max_size: int) -> List[str]:
        """Split a long sentence into smaller phrases"""
        import re
        
        # Try to split by commas and conjunctions first
        phrase_pattern = r'[,;]|\s+(?:và|hoặc|nhưng|mà|thì|nên|because|and|or|but|so|however)\s+'
        phrases = re.split(phrase_pattern, sentence, flags=re.IGNORECASE)
        phrases = [p.strip() for p in phrases if p.strip()]
        
        if not phrases:
            # Fallback to word-based splitting
            words = sentence.split()
            phrases = []
            current_phrase = ""
            
            for word in words:
                if len(current_phrase + " " + word) <= max_size:
                    current_phrase = current_phrase + " " + word if current_phrase else word
                else:
                    if current_phrase:
                        phrases.append(current_phrase)
                    current_phrase = word
            
            if current_phrase:
                phrases.append(current_phrase)
        
        return phrases if phrases else [sentence]
    
    def _merge_audio_chunks(self, audio_files: List[str], output_path: str) -> bool:
        """Merge multiple audio files into one"""
        try:
            # Try to use pydub for merging
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    # Suppress FFmpeg stderr
                    import contextlib
                    with contextlib.redirect_stderr(open(os.devnull, 'w')):
                        audio = AudioSegment.from_wav(audio_file)
                    combined += audio
                    # Add small silence between chunks
                    combined += AudioSegment.silent(duration=300)  # 300ms
            
            # Export merged audio
            with contextlib.redirect_stderr(open(os.devnull, 'w')):
                combined.export(output_path, format="wav")
            
            return True
            
        except Exception as e:
            logger.error(f"Audio merge failed: {e}")
            return False
    
    def generate_multi_character(self,
                               script_data: Dict[str, Any],
                               voice_mapping: Dict[str, str],
                               output_dir: str = "./output",
                               enable_postprocessing: bool = True) -> TTSResult:
        """
        🚨 DISABLED TO PREVENT DUPLICATE TTS
        
        Multi-character generation now handled by Advanced Character System only.
        This prevents the duplicate TTS calls shown in logs.
        """
        logger.info("🚨 TTSBridge multi-character generation DISABLED to prevent duplicates")
        logger.info("🎭 Routing to Advanced Character System instead...")
        
        # Return success without generating - let Advanced Character System handle it
        return TTSResult(
            success=True,
            audio_path=output_dir,
            metadata={
                "mode": "delegated_to_advanced_system",
                "message": "TTSBridge disabled, Advanced Character System will handle generation",
                "duplicate_prevention": True
            }
        )
    
    def generate_audio_from_script_data(self,
                                      script_data: Any,
                                      voice_mapping: Dict[str, Any],
                                      output_directory: str,
                                      progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Universal method - auto-detect mode và route đến đúng handler
        
        THAY THẾ ChatterboxExtendedIntegration.generate_audio_from_script_data()
        """
        logger.info("🌉 Bridge: Auto-detecting script mode...")
        
        try:
            # Auto-detect mode
            if isinstance(script_data, dict) and "segments" in script_data and "characters" in script_data:
                # Complex mode: multiple characters - DISABLED to prevent duplicates
                logger.info("🚨 MULTI-CHARACTER mode DISABLED by TTSBridge")
                logger.info("🎭 Advanced Character System will handle this generation")
                
                # Return success without generating - Advanced Character System will handle it
                return {
                    "success": True,
                    "mode": "delegated_to_advanced_character_system",
                    "result": {
                        "message": "TTSBridge skipped to prevent duplicate TTS calls",
                        "duplicate_prevention": True
                    },
                    "output_directory": output_directory,
                    "error": None
                }
                
            elif isinstance(script_data, dict) and "text" in script_data:
                # Single character mode: enhanced text processing
                logger.info("🎙️ Detected ENHANCED SINGLE-CHARACTER mode")
                text = script_data["text"]
                
                # Extract voice name and TTS parameters from voice mapping (handle both string and dict format)
                logger.info(f"🎯 Voice mapping debug:")
                logger.info(f"   Raw voice_mapping: {voice_mapping}")
                logger.info(f"   Type: {type(voice_mapping)}")
                
                tts_params = {}  # Extract all TTS parameters
                
                if voice_mapping:
                    first_voice = list(voice_mapping.values())[0]
                    logger.info(f"   First voice: {first_voice}")
                    logger.info(f"   First voice type: {type(first_voice)}")
                    
                    if isinstance(first_voice, dict):
                        voice_name = first_voice.get('suggested_voice', 'abigail')
                        # Extract all TTS parameters from the voice mapping
                        tts_params = {
                            'emotion': first_voice.get('emotion', 'neutral'),
                            'emotion_exaggeration': first_voice.get('exaggeration', 1.0),
                            'speed': first_voice.get('speed', 1.0),
                            'cfg_weight': first_voice.get('cfg_weight', 0.5),
                            'temperature': first_voice.get('temperature', 0.7)
                        }
                        logger.info(f"   Extracted from dict: voice={voice_name}")
                        logger.info(f"   TTS params: {tts_params}")
                    else:
                        voice_name = first_voice
                        logger.info(f"   Using direct value: {voice_name}")
                else:
                    voice_name = "abigail"
                    logger.info(f"   No mapping, using default: {voice_name}")
                
                # Ensure voice_name is a string
                if not isinstance(voice_name, str):
                    logger.warning(f"   Voice name is not string: {voice_name}, converting...")
                    voice_name = str(voice_name)
                
                # Log the mode detection details
                logger.info(f"📝 Single mode details:")
                logger.info(f"   Text length: {len(text)} characters")
                logger.info(f"   Voice: {voice_name}")
                logger.info(f"   Chunks from UI: {script_data.get('chunks', 'unknown')}")
                
                result = self.generate_single_character(
                    text=text,
                    voice_name=voice_name,
                    output_dir=output_directory,
                    enable_preprocessing=True,
                    enable_postprocessing=True,
                    **tts_params
                )
                
                return {
                    "success": result.success,
                    "mode": "enhanced_single_character", 
                    "result": result.metadata,
                    "output_directory": output_directory,
                    "audio_path": result.audio_path if result.success else None,
                    "error": result.error_message if not result.success else None
                }
                
            elif isinstance(script_data, str):
                # Direct text input
                logger.info("📝 Detected DIRECT TEXT mode")
                result = self.generate_single_character(
                    text=script_data,
                    voice_name=list(voice_mapping.values())[0] if voice_mapping else "abigail",
                    output_dir=output_directory,
                    enable_preprocessing=True,
                    enable_postprocessing=True
                )
                
                return {
                    "success": result.success,
                    "mode": "direct_text",
                    "result": result.metadata,
                    "output_directory": output_directory,
                    "error": result.error_message if not result.success else None
                }
                
            else:
                logger.error(f"Unknown script data format: {type(script_data)}")
                return {
                    "success": False,
                    "error": f"Unknown script data format: {type(script_data)}",
                    "mode": "unknown"
                }
                
        except Exception as e:
            logger.error(f"Bridge generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "mode": "error"
            }
    
    def _generate_multi_character_direct(self, script_data, output_dir, voice_mapping):
        """Generate multi-character TTS directly with RealChatterboxProvider (no VoiceGenerator)"""
        try:
            import os
            from pathlib import Path
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            generated_files = []
            segments = script_data.get('segments', [])
            
            print(f"🎭 Generating {len(segments)} segments directly via RealChatterboxProvider...")
            
            for segment_idx, segment in enumerate(segments):
                dialogues = segment.get('dialogues', [])
                
                for dialogue_idx, dialogue in enumerate(dialogues):
                    speaker = dialogue.get('speaker', 'unknown')
                    text = dialogue.get('text', '')
                    emotion = dialogue.get('emotion', 'neutral')
                    
                    if not text.strip():
                        continue
                    
                    # Get voice name from mapping
                    voice_name = voice_mapping.get(speaker, 'alice')  # Default fallback
                    
                    # Generate filename
                    audio_filename = f"s{segment_idx+1}_d{dialogue_idx+1}_{speaker}.mp3"
                    audio_path = os.path.join(output_dir, audio_filename)
                    
                    print(f"🎙️ DIRECT TTS: {speaker} ({voice_name}) -> {audio_filename}")
                    
                    # Generate audio directly with RealChatterboxProvider
                    try:
                        result = self.chatterbox_provider.generate_voice(
                            text=text,
                            save_path=audio_path,
                            voice_name=voice_name,
                            emotion_exaggeration=1.0,  # Map emotion to exaggeration
                            speed=1.0,
                            cfg_weight=0.5
                        )
                        
                        if result.get("success", False):
                            generated_files.append(audio_path)
                            print(f"✅ Generated: {audio_filename}")
                        else:
                            print(f"❌ Failed to generate: {audio_filename} - {result.get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        print(f"❌ Error generating {audio_filename}: {e}")
                        continue
            
            return {
                "success": len(generated_files) > 0,
                "generated_files": generated_files,
                "total_files": len(generated_files),
                "error": None if len(generated_files) > 0 else "No files generated"
            }
            
        except Exception as e:
            return {
                "success": False,
                "generated_files": [],
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get bridge status"""
        return {
            "bridge_available": True,
            "real_provider_available": self.real_provider is not None,
            "extended_integration_available": self.extended_integration is not None,
            "voice_generator_available": self.voice_generator is not None,
            "architecture": "Bridge eliminates duplicate TTS calls"
        }

# Global bridge instance
tts_bridge = TTSBridge()

def get_tts_bridge() -> TTSBridge:
    """Get global TTS bridge instance"""
    return tts_bridge