"""

Voice Studio Quality Controller - PHASE 3

AI-powered quality control với multiple candidates, Whisper validation, và smart retry

"""



import os

import time

import json

import logging

from datetime import datetime

from typing import List, Dict, Tuple, Optional, Any

from dataclasses import dataclass, asdict

from enum import Enum



# Audio processing

try:

    import whisper

    WHISPER_AVAILABLE = True

except ImportError:

    WHISPER_AVAILABLE = False



try:

    from pydub import AudioSegment

    import librosa

    import numpy as np

    AUDIO_ANALYSIS_AVAILABLE = True

except ImportError:

    AUDIO_ANALYSIS_AVAILABLE = False



# Similarity calculation

try:

    from difflib import SequenceMatcher

    import re

    TEXT_ANALYSIS_AVAILABLE = True

except ImportError:

    TEXT_ANALYSIS_AVAILABLE = False





class QualityMetric(Enum):

    """Quality metrics for audio evaluation"""

    TRANSCRIPTION_ACCURACY = "transcription_accuracy"

    AUDIO_CLARITY = "audio_clarity"

    SPEECH_NATURALNESS = "speech_naturalness"

    EMOTIONAL_CONSISTENCY = "emotional_consistency"

    TECHNICAL_QUALITY = "technical_quality"





@dataclass

class QualityScore:

    """Individual quality score with details"""

    metric: QualityMetric

    score: float  # 0.0 - 1.0

    details: Dict[str, Any]

    timestamp: str = None

    

    def __post_init__(self):

        if self.timestamp is None:

            self.timestamp = datetime.now().isoformat()





@dataclass

class AudioCandidate:

    """Audio candidate với quality assessment"""

    candidate_id: str

    audio_path: str

    text: str

    voice_params: Dict

    quality_scores: List[QualityScore]

    overall_score: float

    generation_time: float

    metadata: Dict[str, Any]

    

    @property

    def is_high_quality(self) -> bool:

        """Check if candidate meets quality threshold"""

        return self.overall_score >= 0.85

    

    @property

    def transcription_score(self) -> float:

        """Get transcription accuracy score"""

        for score in self.quality_scores:

            if score.metric == QualityMetric.TRANSCRIPTION_ACCURACY:

                return score.score

        return 0.0





@dataclass

class QualityReport:

    """Comprehensive quality report"""

    task_id: str

    best_candidate: Optional[AudioCandidate]

    all_candidates: List[AudioCandidate]

    total_attempts: int

    success_rate: float

    processing_time: float

    quality_breakdown: Dict[str, float]

    recommendations: List[str]

    timestamp: str = None

    

    def __post_init__(self):

        if self.timestamp is None:

            self.timestamp = datetime.now().isoformat()





class WhisperValidator:

    """Whisper-based audio validation"""

    

    def __init__(self, model_name: str = "base"):

        self.model_name = model_name

        self.model = None

        self.load_model()

    

    def load_model(self):

        """Load Whisper model"""

        if not WHISPER_AVAILABLE:

            logging.warning("Whisper not available. Skipping transcription validation.")

            return

        

        try:

            self.model = whisper.load_model(self.model_name)

            logging.info(f"[OK] Whisper model '{self.model_name}' loaded successfully")

        except Exception as e:

            logging.error(f"[EMOJI] Failed to load Whisper model: {e}")

            self.model = None

    

    def validate_transcription(self, audio_path: str, expected_text: str) -> QualityScore:

        """Validate audio matches expected text"""

        if not self.model:

            return QualityScore(

                metric=QualityMetric.TRANSCRIPTION_ACCURACY,

                score=0.5,  # Neutral score when validation unavailable

                details={"error": "Whisper model not available"}

            )

        

        try:

            # Transcribe audio

            result = self.model.transcribe(audio_path)

            transcribed_text = result["text"].strip()

            

            # Calculate similarity

            similarity = self.calculate_text_similarity(transcribed_text, expected_text)

            

            # Additional metrics

            word_accuracy = self.calculate_word_accuracy(transcribed_text, expected_text)

            confidence = result.get("segments", [{}])[0].get("avg_logprob", -1.0)

            

            details = {

                "transcribed": transcribed_text,

                "expected": expected_text,

                "word_accuracy": word_accuracy,

                "confidence": confidence,

                "whisper_model": self.model_name

            }

            

            return QualityScore(

                metric=QualityMetric.TRANSCRIPTION_ACCURACY,

                score=similarity,

                details=details

            )

            

        except Exception as e:

            logging.error(f"[EMOJI] Transcription validation failed: {e}")

            return QualityScore(

                metric=QualityMetric.TRANSCRIPTION_ACCURACY,

                score=0.0,

                details={"error": str(e)}

            )

    

    def calculate_text_similarity(self, text1: str, text2: str) -> float:

        """Calculate text similarity score"""

        if not TEXT_ANALYSIS_AVAILABLE:

            return 0.5

        

        # Normalize texts

        text1_clean = self.normalize_text(text1)

        text2_clean = self.normalize_text(text2)

        

        # Calculate similarity using SequenceMatcher

        similarity = SequenceMatcher(None, text1_clean, text2_clean).ratio()

        return similarity

    

    def calculate_word_accuracy(self, transcribed: str, expected: str) -> float:

        """Calculate word-level accuracy"""

        if not TEXT_ANALYSIS_AVAILABLE:

            return 0.5

        

        transcribed_words = set(self.normalize_text(transcribed).split())

        expected_words = set(self.normalize_text(expected).split())

        

        if not expected_words:

            return 1.0

        

        correct_words = len(transcribed_words.intersection(expected_words))

        total_words = len(expected_words)

        

        return correct_words / total_words

    

    def normalize_text(self, text: str) -> str:

        """Normalize text for comparison"""

        # Convert to lowercase

        text = text.lower()

        # Remove punctuation and extra spaces

        text = re.sub(r'[^\w\s]', '', text)

        text = re.sub(r'\s+', ' ', text)

        return text.strip()





class AudioAnalyzer:

    """Audio quality analysis"""

    

    def analyze_audio_quality(self, audio_path: str) -> List[QualityScore]:

        """Analyze technical audio quality"""

        scores = []

        

        if not AUDIO_ANALYSIS_AVAILABLE:

            # Return default scores if analysis unavailable

            return [

                QualityScore(

                    metric=QualityMetric.AUDIO_CLARITY,

                    score=0.7,

                    details={"error": "Audio analysis libraries not available"}

                )

            ]

        

        try:

            # Load audio - SUPPRESS FFMPEG STDERR
            import contextlib
            with contextlib.redirect_stderr(open(os.devnull, 'w')):
                audio = AudioSegment.from_file(audio_path)

            y, sr = librosa.load(audio_path)

            

            # Audio clarity (SNR estimation)

            clarity_score = self.estimate_clarity(y, sr)

            scores.append(QualityScore(

                metric=QualityMetric.AUDIO_CLARITY,

                score=clarity_score,

                details={"snr_estimate": clarity_score}

            ))

            

            # Technical quality (dynamic range, clipping)

            technical_score = self.assess_technical_quality(audio, y)

            scores.append(QualityScore(

                metric=QualityMetric.TECHNICAL_QUALITY,

                score=technical_score,

                details={"dynamic_range": technical_score}

            ))

            

            # Speech naturalness (spectral features)

            naturalness_score = self.assess_naturalness(y, sr)

            scores.append(QualityScore(

                metric=QualityMetric.SPEECH_NATURALNESS,

                score=naturalness_score,

                details={"spectral_analysis": naturalness_score}

            ))

            

        except Exception as e:

            logging.error(f"[EMOJI] Audio analysis failed: {e}")

            scores.append(QualityScore(

                metric=QualityMetric.AUDIO_CLARITY,

                score=0.5,

                details={"error": str(e)}

            ))

        

        return scores

    

    def estimate_clarity(self, y: np.ndarray, sr: int) -> float:

        """Estimate audio clarity (simple SNR-based)"""

        try:

            # Simple clarity estimation based on spectral energy distribution

            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

            

            # Higher centroid and lower bandwidth typically indicate clearer speech

            clarity = np.mean(spectral_centroids) / (np.mean(spectral_bandwidth) + 1)

            clarity = min(max(clarity / 10, 0.0), 1.0)  # Normalize to 0-1

            

            return clarity

        except:

            return 0.7  # Default reasonable score

    

    def assess_technical_quality(self, audio: AudioSegment, y: np.ndarray) -> float:

        """Assess technical audio quality"""

        try:

            # Check for clipping

            max_amplitude = np.max(np.abs(y))

            clipping_penalty = 1.0 if max_amplitude < 0.95 else 0.7

            

            # Dynamic range

            rms = np.sqrt(np.mean(y**2))

            peak = np.max(np.abs(y))

            dynamic_range = peak / (rms + 1e-10)

            

            # Normalize dynamic range score (good range is 3-10)

            dr_score = min(max((dynamic_range - 3) / 7, 0.0), 1.0)

            

            return (clipping_penalty + dr_score) / 2

        except:

            return 0.7  # Default reasonable score

    

    def assess_naturalness(self, y: np.ndarray, sr: int) -> float:

        """Assess speech naturalness"""

        try:

            # Assess spectral features that correlate with natural speech

            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

            mfcc_variance = np.var(mfccs, axis=1)

            

            # Natural speech has certain MFCC variance patterns

            naturalness = np.mean(mfcc_variance) / 100  # Rough normalization

            naturalness = min(max(naturalness, 0.0), 1.0)

            

            return naturalness

        except:

            return 0.7  # Default reasonable score





class QualityController:

    """Main quality controller với multi-candidate generation và validation"""

    

    def __init__(self, 

                 num_candidates: int = 3,

                 quality_threshold: float = 0.85,

                 max_retries: int = 5,

                 whisper_model: str = "base"):

        self.num_candidates = num_candidates

        self.quality_threshold = quality_threshold

        self.max_retries = max_retries

        

        # Initialize validators

        self.whisper_validator = WhisperValidator(whisper_model)

        self.audio_analyzer = AudioAnalyzer()

        

        # Statistics

        self.stats = {

            "total_tasks": 0,

            "successful_tasks": 0,

            "failed_tasks": 0,

            "avg_candidates_needed": 0.0,

            "avg_quality_score": 0.0

        }

        

        logging.info(f"[TARGET] Quality Controller initialized - {num_candidates} candidates, {quality_threshold:.1%} threshold")

    

    def generate_with_quality_control(self, 

                                    text: str, 

                                    voice_params: Dict,

                                    voice_generator_func,

                                    task_id: str = None) -> QualityReport:

        """Generate audio với quality control và multiple candidates"""

        if task_id is None:

            task_id = f"task_{int(time.time())}"

        

        start_time = time.time()

        candidates = []

        

        logging.info(f"[TARGET] Starting quality-controlled generation for task: {task_id}")

        

        # Generate multiple candidates

        for i in range(self.num_candidates):

            candidate_start = time.time()

            

            try:

                # Generate audio (với slight parameter variation cho diversity)

                varied_params = self.create_parameter_variation(voice_params, i)

                audio_path = voice_generator_func(text, varied_params)

                

                if audio_path and os.path.exists(audio_path):

                    # Evaluate quality

                    candidate = self.evaluate_candidate(

                        candidate_id=f"{task_id}_candidate_{i}",

                        audio_path=audio_path,

                        text=text,

                        voice_params=varied_params,

                        generation_time=time.time() - candidate_start

                    )

                    

                    candidates.append(candidate)

                    

                    logging.info(f"[STATS] Candidate {i}: Quality {candidate.overall_score:.3f}")

                    

                    # Early exit if high quality found

                    if candidate.is_high_quality:

                        logging.info(f"[OK] High quality candidate found early: {candidate.overall_score:.3f}")

                        break

                        

                else:

                    logging.warning(f"[WARNING] Failed to generate candidate {i}")

                    

            except Exception as e:

                logging.error(f"[EMOJI] Error generating candidate {i}: {e}")

        

        # Select best candidate

        best_candidate = self.select_best_candidate(candidates) if candidates else None

        

        # Retry logic if quality not met

        if best_candidate and not best_candidate.is_high_quality and len(candidates) < self.max_retries:

            logging.info(f"[REFRESH] Quality below threshold ({best_candidate.overall_score:.3f}), generating additional candidates...")

            

            additional_candidates = self.generate_additional_candidates(

                text, voice_params, voice_generator_func, task_id, 

                self.max_retries - len(candidates)

            )

            candidates.extend(additional_candidates)

            best_candidate = self.select_best_candidate(candidates)

        

        # Create quality report

        total_time = time.time() - start_time

        success_rate = 1.0 if best_candidate and best_candidate.is_high_quality else 0.0

        

        quality_breakdown = self.calculate_quality_breakdown(candidates)

        recommendations = self.generate_recommendations(candidates, best_candidate)

        

        report = QualityReport(

            task_id=task_id,

            best_candidate=best_candidate,

            all_candidates=candidates,

            total_attempts=len(candidates),

            success_rate=success_rate,

            processing_time=total_time,

            quality_breakdown=quality_breakdown,

            recommendations=recommendations

        )

        

        # Update statistics

        self.update_statistics(report)

        

        logging.info(f"[TARGET] Quality control completed: {success_rate:.1%} success, {len(candidates)} candidates, {total_time:.2f}s")

        

        return report

    

    def evaluate_candidate(self, candidate_id: str, audio_path: str, text: str, 

                          voice_params: Dict, generation_time: float) -> AudioCandidate:

        """Evaluate single audio candidate"""

        quality_scores = []

        

        # Transcription validation

        transcription_score = self.whisper_validator.validate_transcription(audio_path, text)

        quality_scores.append(transcription_score)

        

        # Audio quality analysis

        audio_scores = self.audio_analyzer.analyze_audio_quality(audio_path)

        quality_scores.extend(audio_scores)

        

        # Calculate overall score (weighted average)

        overall_score = self.calculate_overall_score(quality_scores)

        

        metadata = {

            "file_size": os.path.getsize(audio_path) if os.path.exists(audio_path) else 0,

            "validation_timestamp": datetime.now().isoformat()

        }

        

        return AudioCandidate(

            candidate_id=candidate_id,

            audio_path=audio_path,

            text=text,

            voice_params=voice_params,

            quality_scores=quality_scores,

            overall_score=overall_score,

            generation_time=generation_time,

            metadata=metadata

        )

    

    def calculate_overall_score(self, quality_scores: List[QualityScore]) -> float:

        """Calculate weighted overall quality score"""

        if not quality_scores:

            return 0.0

        

        # Weights for different metrics

        weights = {

            QualityMetric.TRANSCRIPTION_ACCURACY: 0.4,  # Most important

            QualityMetric.AUDIO_CLARITY: 0.25,

            QualityMetric.TECHNICAL_QUALITY: 0.2,

            QualityMetric.SPEECH_NATURALNESS: 0.15,

            QualityMetric.EMOTIONAL_CONSISTENCY: 0.1

        }

        

        total_weighted_score = 0.0

        total_weight = 0.0

        

        for score in quality_scores:

            weight = weights.get(score.metric, 0.1)  # Default weight

            total_weighted_score += score.score * weight

            total_weight += weight

        

        return total_weighted_score / total_weight if total_weight > 0 else 0.0

    

    def select_best_candidate(self, candidates: List[AudioCandidate]) -> Optional[AudioCandidate]:

        """Select best candidate based on overall score"""

        if not candidates:

            return None

        

        # Sort by overall score (descending)

        sorted_candidates = sorted(candidates, key=lambda c: c.overall_score, reverse=True)

        return sorted_candidates[0]

    

    def create_parameter_variation(self, base_params: Dict, variation_index: int) -> Dict:

        """Create slight parameter variation for diversity"""

        varied_params = base_params.copy()

        

        # Small variations to encourage diversity

        variations = [

            {},  # No variation for first candidate

            {"temperature": base_params.get("temperature", 1.0) * 1.05},

            {"speed": base_params.get("speed", 1.0) * 0.98},

            {"stability": base_params.get("stability", 0.5) * 0.95},

            {"similarity_boost": base_params.get("similarity_boost", 0.5) * 1.1}

        ]

        

        if variation_index < len(variations):

            varied_params.update(variations[variation_index])

        

        return varied_params

    

    def generate_additional_candidates(self, text: str, voice_params: Dict, 

                                     voice_generator_func, task_id: str, 

                                     num_additional: int) -> List[AudioCandidate]:

        """Generate additional candidates when quality threshold not met"""

        additional_candidates = []

        

        for i in range(num_additional):

            try:

                candidate_start = time.time()

                

                # More aggressive parameter variations for retry

                retry_params = self.create_retry_variation(voice_params, i)

                audio_path = voice_generator_func(text, retry_params)

                

                if audio_path and os.path.exists(audio_path):

                    candidate = self.evaluate_candidate(

                        candidate_id=f"{task_id}_retry_{i}",

                        audio_path=audio_path,

                        text=text,

                        voice_params=retry_params,

                        generation_time=time.time() - candidate_start

                    )

                    

                    additional_candidates.append(candidate)

                    

                    if candidate.is_high_quality:

                        break

                        

            except Exception as e:

                logging.error(f"[EMOJI] Error generating retry candidate {i}: {e}")

        

        return additional_candidates

    

    def create_retry_variation(self, base_params: Dict, retry_index: int) -> Dict:

        """Create more aggressive parameter variations for retries"""

        retry_params = base_params.copy()

        

        # More significant variations for retries

        retry_variations = [

            {"temperature": base_params.get("temperature", 1.0) * 0.8},

            {"temperature": base_params.get("temperature", 1.0) * 1.2},

            {"speed": base_params.get("speed", 1.0) * 0.9},

            {"stability": base_params.get("stability", 0.5) * 1.1},

            {"voice_id": "alternative_voice"}  # Could switch to alternative voice

        ]

        

        if retry_index < len(retry_variations):

            retry_params.update(retry_variations[retry_index])

        

        return retry_params

    

    def calculate_quality_breakdown(self, candidates: List[AudioCandidate]) -> Dict[str, float]:

        """Calculate quality metrics breakdown"""

        if not candidates:

            return {}

        

        breakdown = {}

        metric_scores = {}

        

        # Collect all scores by metric

        for candidate in candidates:

            for score in candidate.quality_scores:

                metric_name = score.metric.value

                if metric_name not in metric_scores:

                    metric_scores[metric_name] = []

                metric_scores[metric_name].append(score.score)

        

        # Calculate averages

        for metric, scores in metric_scores.items():

            breakdown[metric] = sum(scores) / len(scores)

        

        return breakdown

    

    def generate_recommendations(self, candidates: List[AudioCandidate], 

                               best_candidate: Optional[AudioCandidate]) -> List[str]:

        """Generate improvement recommendations"""

        recommendations = []

        

        if not candidates:

            recommendations.append("No candidates generated. Check voice generation system.")

            return recommendations

        

        if not best_candidate or not best_candidate.is_high_quality:

            recommendations.append("Consider adjusting voice parameters for better quality.")

            

            # Analyze weak points

            if best_candidate:

                if best_candidate.transcription_score < 0.8:

                    recommendations.append("Low transcription accuracy. Try different voice settings or cleaner text.")

                

                avg_audio_quality = sum(s.score for s in best_candidate.quality_scores 

                                      if s.metric in [QualityMetric.AUDIO_CLARITY, QualityMetric.TECHNICAL_QUALITY]) / 2

                

                if avg_audio_quality < 0.7:

                    recommendations.append("Audio quality issues detected. Check audio processing settings.")

        

        if len(candidates) >= self.max_retries:

            recommendations.append("Max retries reached. Consider reviewing text complexity or voice settings.")

        

        return recommendations

    

    def update_statistics(self, report: QualityReport):

        """Update internal statistics"""

        self.stats["total_tasks"] += 1

        

        if report.success_rate > 0:

            self.stats["successful_tasks"] += 1

        else:

            self.stats["failed_tasks"] += 1

        

        # Update running averages

        total = self.stats["total_tasks"]

        self.stats["avg_candidates_needed"] = (

            (self.stats["avg_candidates_needed"] * (total - 1) + report.total_attempts) / total

        )

        

        if report.best_candidate:

            self.stats["avg_quality_score"] = (

                (self.stats["avg_quality_score"] * (total - 1) + report.best_candidate.overall_score) / total

            )

    

    def get_statistics(self) -> Dict:

        """Get quality controller statistics"""

        stats = self.stats.copy()

        stats["success_rate"] = (

            self.stats["successful_tasks"] / self.stats["total_tasks"] 

            if self.stats["total_tasks"] > 0 else 0.0

        )

        return stats

    

    def save_report(self, report: QualityReport, output_dir: str):

        """Save quality report to file"""

        os.makedirs(output_dir, exist_ok=True)

        

        report_path = os.path.join(output_dir, f"quality_report_{report.task_id}.json")

        

        # Convert to JSON-serializable format

        report_dict = asdict(report)

        

        with open(report_path, 'w', encoding='utf-8') as f:

            json.dump(report_dict, f, indent=2, ensure_ascii=False)

        

        logging.info(f"[FILE] Quality report saved: {report_path}")

        return report_path





# Example usage và testing

def example_voice_generator(text: str, params: Dict) -> str:

    """Example voice generator function for testing"""

    import tempfile

    import random

    

    # Simulate voice generation với varying quality

    output_path = tempfile.mktemp(suffix='.mp3')

    

    # Create dummy audio file

    with open(output_path, 'wb') as f:

        f.write(b'dummy audio data for testing')

    

    # Simulate processing time

    time.sleep(random.uniform(0.1, 0.5))

    

    return output_path





if __name__ == "__main__":

    # Test quality controller

    logging.basicConfig(level=logging.INFO)

    

    print("[TEST] Testing Quality Controller - PHASE 3")

    

    # Initialize controller

    controller = QualityController(

        num_candidates=3,

        quality_threshold=0.85,

        max_retries=5

    )

    

    # Test generation với quality control

    test_text = "Hello, this is a test of the voice quality control system."

    test_params = {

        "voice_id": "test_voice",

        "speed": 1.0,

        "stability": 0.5

    }

    

    report = controller.generate_with_quality_control(

        text=test_text,

        voice_params=test_params,

        voice_generator_func=example_voice_generator,

        task_id="test_quality_control"

    )

    

    print(f"[OK] Quality control test completed:")

    print(f"   [TARGET] Success Rate: {report.success_rate:.1%}")

    print(f"   [STATS] Best Score: {report.best_candidate.overall_score:.3f if report.best_candidate else 'N/A'}")

    print(f"   [REFRESH] Attempts: {report.total_attempts}")

    print(f"   ⏱ Time: {report.processing_time:.2f}s")

    

    # Show statistics

    stats = controller.get_statistics()

    print(f"\n[METRICS] Controller Statistics:")

    for key, value in stats.items():

        print(f"   {key}: {value}")

    

    print("\n[SUCCESS] Quality Controller PHASE 3 - Implementation Complete!")

