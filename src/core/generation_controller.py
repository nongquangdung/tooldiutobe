#!/usr/bin/env python3
"""
[TARGET] GENERATION CONTROLLER
=========================

Advanced generation logic & quality control tái tạo từ Chatterbox TTS Extended:
- Số lượng thế hệ: Multiple takes cùng lúc
- Ứng viên cho mỗi khối: Multiple variants per block
- Retry logic: Max retries per candidate
- Whisper validation: STT verification
- Fallback strategy: Best candidate selection
"""

import os
import time
import asyncio
import logging
import tempfile
import statistics
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class GenerationConfig:
    """Cấu hình cho generation logic"""
    # Multiple generations
    num_generations: int = 3  # Số lượng "takes" khác nhau
    
    # Candidates per block
    candidates_per_block: int = 2  # Số ứng viên cho mỗi block
    
    # Retry logic
    max_retries_per_candidate: int = 3  # Max retries nếu validation fail
    
    # Whisper validation
    enable_whisper_validation: bool = True
    whisper_model: str = "base"  # tiny, base, small, medium, large
    whisper_backend: str = "openai"  # "openai" or "faster-whisper"
    similarity_threshold: float = 0.7  # Minimum similarity score (0.0-1.0)
    
    # Fallback strategy
    fallback_strategy: str = "longest"  # "longest", "highest_similarity", "first_success"
    
    # Performance
    enable_parallel_generation: bool = True
    max_workers: int = 4
    generation_timeout: float = 60.0  # seconds per generation
    
    # Quality control
    min_audio_length: float = 0.5  # Minimum audio length (seconds)
    max_audio_length: float = 300.0  # Maximum audio length (seconds)

@dataclass
class GenerationCandidate:
    """Một ứng viên generation"""
    id: str
    text: str
    audio_path: str
    metadata: Dict[str, Any]
    validation_score: Optional[float] = None
    transcription: Optional[str] = None
    duration: Optional[float] = None
    generation_time: Optional[float] = None
    attempt_number: int = 1

@dataclass
class GenerationResult:
    """Kết quả generation cho một block"""
    original_text: str
    best_candidate: Optional[GenerationCandidate]
    all_candidates: List[GenerationCandidate]
    generation_stats: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

@dataclass
class BatchGenerationResult:
    """Kết quả generation cho toàn bộ batch"""
    results: List[GenerationResult]
    total_stats: Dict[str, Any]
    processing_time: float
    success_rate: float

class GenerationController:
    """Controller chính cho advanced generation logic"""
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        self.config = config or GenerationConfig()
        self.whisper_model = None
        self.whisper_available = False
        
        # Stats tracking
        self.stats = {
            'total_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'total_candidates': 0,
            'whisper_validations': 0,
            'retries_performed': 0,
            'average_similarity': 0.0,
            'average_generation_time': 0.0
        }
        
        # Initialize Whisper if enabled
        if self.config.enable_whisper_validation:
            self._initialize_whisper()
    
    def _initialize_whisper(self):
        """Initialize Whisper model cho validation"""
        try:
            if self.config.whisper_backend == "faster-whisper":
                from faster_whisper import WhisperModel
                logger.info(f"Loading faster-whisper model: {self.config.whisper_model}")
                self.whisper_model = WhisperModel(self.config.whisper_model)
            else:
                import whisper
                logger.info(f"Loading OpenAI Whisper model: {self.config.whisper_model}")
                self.whisper_model = whisper.load_model(self.config.whisper_model)
            
            self.whisper_available = True
            logger.info("[OK] Whisper model loaded successfully")
            
        except Exception as e:
            logger.warning(f"[EMOJI] Failed to load Whisper model: {e}")
            self.whisper_available = False
    
    async def generate_with_quality_control(self, 
                                          text_blocks: List[str],
                                          generation_function: Callable,
                                          generation_params: Dict[str, Any]) -> BatchGenerationResult:
        """
        Main method cho generation với quality control
        
        Args:
            text_blocks: List of text blocks to generate
            generation_function: Function để generate audio (async)
            generation_params: Parameters for generation function
            
        Returns:
            BatchGenerationResult với tất cả kết quả
        """
        start_time = time.time()
        
        logger.info(f"[TARGET] Starting quality-controlled generation...")
        logger.info(f"   [EDIT] Text blocks: {len(text_blocks)}")
        logger.info(f"   [THEATER] Generations per block: {self.config.num_generations}")
        logger.info(f"   [TARGET] Candidates per generation: {self.config.candidates_per_block}")
        logger.info(f"   [SEARCH] Whisper validation: {'[OK]' if self.config.enable_whisper_validation else '[EMOJI]'}")
        
        results = []
        
        if self.config.enable_parallel_generation and len(text_blocks) > 1:
            # Parallel processing
            results = await self._generate_parallel(text_blocks, generation_function, generation_params)
        else:
            # Sequential processing
            results = await self._generate_sequential(text_blocks, generation_function, generation_params)
        
        processing_time = time.time() - start_time
        
        # Calculate success rate
        successful_results = sum(1 for r in results if r.success)
        success_rate = successful_results / len(results) if results else 0.0
        
        # Update global stats
        self.stats['total_generations'] += len(results)
        self.stats['successful_generations'] += successful_results
        self.stats['failed_generations'] += len(results) - successful_results
        
        logger.info(f"[OK] Generation completed in {processing_time:.2f}s")
        logger.info(f"   [STATS] Success rate: {success_rate:.1%} ({successful_results}/{len(results)})")
        
        return BatchGenerationResult(
            results=results,
            total_stats=self.stats.copy(),
            processing_time=processing_time,
            success_rate=success_rate
        )
    
    async def _generate_sequential(self, text_blocks: List[str], 
                                 generation_function: Callable,
                                 generation_params: Dict[str, Any]) -> List[GenerationResult]:
        """Sequential generation cho từng block"""
        results = []
        
        for i, text_block in enumerate(text_blocks):
            logger.info(f"[EDIT] Processing block {i+1}/{len(text_blocks)}")
            result = await self._generate_single_block(text_block, generation_function, generation_params)
            results.append(result)
            
        return results
    
    async def _generate_parallel(self, text_blocks: List[str],
                               generation_function: Callable,
                               generation_params: Dict[str, Any]) -> List[GenerationResult]:
        """Parallel generation cho multiple blocks"""
        logger.info(f"[FAST] Using parallel generation with {self.config.max_workers} workers")
        
        # Create semaphore to limit concurrent generations
        semaphore = asyncio.Semaphore(self.config.max_workers)
        
        async def generate_with_semaphore(text_block):
            async with semaphore:
                return await self._generate_single_block(text_block, generation_function, generation_params)
        
        # Start all generations
        tasks = [generate_with_semaphore(text_block) for text_block in text_blocks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Block {i+1} failed: {result}")
                processed_results.append(GenerationResult(
                    original_text=text_blocks[i],
                    best_candidate=None,
                    all_candidates=[],
                    generation_stats={},
                    success=False,
                    error_message=str(result)
                ))
            else:
                processed_results.append(result)
                
        return processed_results
    
    async def _generate_single_block(self, text: str,
                                   generation_function: Callable,
                                   generation_params: Dict[str, Any]) -> GenerationResult:
        """Generate audio cho một text block với multiple candidates và validation"""
        logger.debug(f"[TARGET] Generating for text: '{text[:50]}...'")
        
        all_candidates = []
        
        # Generate multiple takes
        for generation_id in range(self.config.num_generations):
            logger.debug(f"   [THEATER] Generation {generation_id + 1}/{self.config.num_generations}")
            
            # Generate multiple candidates per take
            generation_candidates = await self._generate_candidates_for_take(
                text, generation_function, generation_params, generation_id
            )
            
            all_candidates.extend(generation_candidates)
        
        # Select best candidate
        best_candidate = self._select_best_candidate(all_candidates)
        
        # Generate stats
        generation_stats = self._calculate_generation_stats(all_candidates)
        
        success = best_candidate is not None
        if success:
            logger.debug(f"   [OK] Best candidate: score={best_candidate.validation_score:.3f}")
        else:
            logger.warning(f"   [EMOJI] No successful candidates found")
        
        return GenerationResult(
            original_text=text,
            best_candidate=best_candidate,
            all_candidates=all_candidates,
            generation_stats=generation_stats,
            success=success
        )
    
    async def _generate_candidates_for_take(self, text: str,
                                          generation_function: Callable,
                                          generation_params: Dict[str, Any],
                                          generation_id: int) -> List[GenerationCandidate]:
        """Generate multiple candidates cho một take"""
        candidates = []
        
        for candidate_id in range(self.config.candidates_per_block):
            candidate = await self._generate_single_candidate(
                text, generation_function, generation_params, 
                generation_id, candidate_id
            )
            
            if candidate:
                candidates.append(candidate)
                
        return candidates
    
    async def _generate_single_candidate(self, text: str,
                                       generation_function: Callable,
                                       generation_params: Dict[str, Any],
                                       generation_id: int,
                                       candidate_id: int) -> Optional[GenerationCandidate]:
        """Generate một candidate với retry logic"""
        
        for attempt in range(self.config.max_retries_per_candidate + 1):
            try:
                logger.debug(f"      [TARGET] Candidate {candidate_id+1}, attempt {attempt+1}")
                
                # Generate unique ID
                unique_id = f"gen_{generation_id}_cand_{candidate_id}_att_{attempt}"
                
                # Create temporary output file
                temp_dir = tempfile.mkdtemp()
                output_path = os.path.join(temp_dir, f"{unique_id}.wav")
                
                # Start generation timer
                gen_start_time = time.time()
                
                # Call generation function
                generation_result = await asyncio.wait_for(
                    generation_function(text=text, output_path=output_path, **generation_params),
                    timeout=self.config.generation_timeout
                )
                
                generation_time = time.time() - gen_start_time
                
                # Check if generation succeeded
                if not os.path.exists(output_path):
                    raise Exception("Generation function didn't create output file")
                
                # Get audio duration
                duration = self._get_audio_duration(output_path)
                
                # Validate audio length
                if duration < self.config.min_audio_length:
                    raise Exception(f"Audio too short: {duration:.2f}s < {self.config.min_audio_length}s")
                    
                if duration > self.config.max_audio_length:
                    raise Exception(f"Audio too long: {duration:.2f}s > {self.config.max_audio_length}s")
                
                # Create candidate
                candidate = GenerationCandidate(
                    id=unique_id,
                    text=text,
                    audio_path=output_path,
                    metadata=generation_result if isinstance(generation_result, dict) else {},
                    duration=duration,
                    generation_time=generation_time,
                    attempt_number=attempt + 1
                )
                
                # Validate with Whisper if enabled
                if self.config.enable_whisper_validation and self.whisper_available:
                    validation_score, transcription = await self._validate_with_whisper(candidate)
                    candidate.validation_score = validation_score
                    candidate.transcription = transcription
                    
                    # Check if validation passed
                    if validation_score >= self.config.similarity_threshold:
                        logger.debug(f"         [OK] Validation passed: {validation_score:.3f}")
                        self.stats['total_candidates'] += 1
                        return candidate
                    else:
                        logger.debug(f"         [REFRESH] Validation failed: {validation_score:.3f}, retrying...")
                        if attempt < self.config.max_retries_per_candidate:
                            self.stats['retries_performed'] += 1
                            continue
                else:
                    # No validation - accept candidate
                    candidate.validation_score = 1.0  # Assume perfect if no validation
                    self.stats['total_candidates'] += 1
                    return candidate
                    
            except asyncio.TimeoutError:
                logger.warning(f"         ⏰ Generation timeout for candidate {candidate_id+1}")
                if attempt < self.config.max_retries_per_candidate:
                    self.stats['retries_performed'] += 1
                    continue
                    
            except Exception as e:
                logger.warning(f"         [EMOJI] Generation failed for candidate {candidate_id+1}: {e}")
                if attempt < self.config.max_retries_per_candidate:
                    self.stats['retries_performed'] += 1
                    continue
        
        # All attempts failed
        logger.warning(f"      [EMOJI] All attempts failed for candidate {candidate_id+1}")
        return None
    
    async def _validate_with_whisper(self, candidate: GenerationCandidate) -> Tuple[float, str]:
        """Validate candidate bằng Whisper STT"""
        try:
            # Transcribe audio
            if self.config.whisper_backend == "faster-whisper":
                segments, _ = self.whisper_model.transcribe(candidate.audio_path)
                transcription = " ".join([segment.text for segment in segments])
            else:
                result = self.whisper_model.transcribe(candidate.audio_path)
                transcription = result["text"]
            
            transcription = transcription.strip()
            
            # Calculate similarity
            similarity = self._calculate_text_similarity(candidate.text, transcription)
            
            self.stats['whisper_validations'] += 1
            self.stats['average_similarity'] = (
                (self.stats['average_similarity'] * (self.stats['whisper_validations'] - 1) + similarity) /
                self.stats['whisper_validations']
            )
            
            logger.debug(f"         [EMOJI] Whisper: '{transcription[:30]}...' (similarity: {similarity:.3f})")
            
            return similarity, transcription
            
        except Exception as e:
            logger.warning(f"Whisper validation failed: {e}")
            return 0.0, ""
    
    def _calculate_text_similarity(self, original: str, transcription: str) -> float:
        """Calculate similarity between original text và transcription"""
        from difflib import SequenceMatcher
        
        # Normalize text
        orig_normalized = original.lower().strip()
        trans_normalized = transcription.lower().strip()
        
        # Calculate similarity using SequenceMatcher
        similarity = SequenceMatcher(None, orig_normalized, trans_normalized).ratio()
        
        return similarity
    
    def _select_best_candidate(self, candidates: List[GenerationCandidate]) -> Optional[GenerationCandidate]:
        """Select best candidate dựa trên fallback strategy"""
        if not candidates:
            return None
        
        # Filter out candidates with validation scores if available
        valid_candidates = [c for c in candidates if c.validation_score is not None]
        
        if not valid_candidates:
            valid_candidates = candidates
        
        if self.config.fallback_strategy == "highest_similarity":
            # Select candidate with highest validation score
            return max(valid_candidates, key=lambda c: c.validation_score or 0.0)
            
        elif self.config.fallback_strategy == "longest":
            # Select candidate with longest duration
            return max(valid_candidates, key=lambda c: c.duration or 0.0)
            
        elif self.config.fallback_strategy == "first_success":
            # Select first successful candidate
            return valid_candidates[0]
            
        else:
            # Default: highest similarity
            return max(valid_candidates, key=lambda c: c.validation_score or 0.0)
    
    def _calculate_generation_stats(self, candidates: List[GenerationCandidate]) -> Dict[str, Any]:
        """Calculate stats cho generation"""
        if not candidates:
            return {}
        
        valid_candidates = [c for c in candidates if c.validation_score is not None]
        
        stats = {
            'total_candidates': len(candidates),
            'valid_candidates': len(valid_candidates),
            'average_duration': statistics.mean([c.duration for c in candidates if c.duration]),
            'average_generation_time': statistics.mean([c.generation_time for c in candidates if c.generation_time])
        }
        
        if valid_candidates:
            stats.update({
                'average_similarity': statistics.mean([c.validation_score for c in valid_candidates]),
                'best_similarity': max([c.validation_score for c in valid_candidates]),
                'worst_similarity': min([c.validation_score for c in valid_candidates])
            })
        
        return stats
    
    def _get_audio_duration(self, file_path: str) -> float:
        """Get duration of audio file"""
        try:
            import wave
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                duration = frames / float(sample_rate)
                return duration
        except:
            # Fallback to ffprobe if wave fails
            try:
                import subprocess
                cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                       '-of', 'csv=p=0', file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                return float(result.stdout.strip())
            except:
                return 0.0
    
    def get_controller_report(self) -> Dict[str, Any]:
        """Get detailed report về controller performance"""
        return {
            'config': {
                'num_generations': self.config.num_generations,
                'candidates_per_block': self.config.candidates_per_block,
                'max_retries': self.config.max_retries_per_candidate,
                'whisper_validation': self.config.enable_whisper_validation,
                'whisper_model': self.config.whisper_model,
                'similarity_threshold': self.config.similarity_threshold,
                'fallback_strategy': self.config.fallback_strategy
            },
            'availability': {
                'whisper_available': self.whisper_available,
                'parallel_processing': self.config.enable_parallel_generation
            },
            'stats': self.stats,
            'performance': {
                'success_rate': (self.stats['successful_generations'] / 
                               max(1, self.stats['total_generations'])),
                'average_similarity': self.stats['average_similarity'],
                'average_generation_time': self.stats['average_generation_time']
            }
        }

# Convenience functions
def create_default_controller() -> GenerationController:
    """Tạo controller với cấu hình mặc định"""
    return GenerationController()

def create_quality_controller() -> GenerationController:
    """Tạo controller tối ưu cho chất lượng"""
    config = GenerationConfig(
        num_generations=5,  # More takes
        candidates_per_block=3,  # More candidates
        max_retries_per_candidate=5,  # More retries
        enable_whisper_validation=True,
        whisper_model="base",  # Better model
        similarity_threshold=0.8,  # Higher threshold
        fallback_strategy="highest_similarity",
        enable_parallel_generation=True,
        max_workers=6
    )
    return GenerationController(config)

def create_fast_controller() -> GenerationController:
    """Tạo controller tối ưu cho tốc độ"""
    config = GenerationConfig(
        num_generations=1,  # Single take
        candidates_per_block=1,  # Single candidate
        max_retries_per_candidate=1,  # Minimal retries
        enable_whisper_validation=False,  # No validation
        fallback_strategy="first_success",
        enable_parallel_generation=True,
        max_workers=8,
        generation_timeout=30.0  # Shorter timeout
    )
    return GenerationController(config)

if __name__ == "__main__":
    # Test the controller
    controller = create_default_controller()
    print("Generation controller initialized")
    print(f"Whisper available: {controller.whisper_available}")
    
    # Print configuration
    report = controller.get_controller_report()
    print(json.dumps(report, indent=2)) 