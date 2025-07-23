#!/usr/bin/env python3
"""
Advanced Text Processor
Enhanced text preprocessing với sophisticated patterns

Features:
- Smart sound word removal (50+ patterns)
- Advanced regex processing
- Dialogue tag detection
- Emotional cue extraction
- Punctuation normalization
- Text quality scoring
"""

import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ProcessingMode(Enum):
    """Text processing modes"""
    CONSERVATIVE = "conservative"
    STANDARD = "standard"
    AGGRESSIVE = "aggressive"

@dataclass
class TextProcessingConfig:
    """Configuration for text processing"""
    mode: ProcessingMode = ProcessingMode.STANDARD
    remove_sound_words: bool = True
    normalize_punctuation: bool = True
    detect_dialogue_tags: bool = True
    extract_emotional_cues: bool = True
    fix_abbreviations: bool = True
    remove_references: bool = True
    smart_joining: bool = True
    recursive_splitting: bool = True
    max_sentence_length: int = 200
    quality_threshold: float = 0.7

class AdvancedTextProcessor:
    """
    Advanced Text Processor với sophisticated patterns
    
    Copy từ original Chatterbox Extended với enhancements:
    - 50+ regex patterns cho sound word removal
    - Intelligent punctuation handling
    - Advanced dialogue detection
    - Quality scoring system
    """
    
    def __init__(self, config: Optional[TextProcessingConfig] = None):
        self.config = config or TextProcessingConfig()
        
        # Initialize pattern collections
        self._sound_word_patterns = self._build_sound_word_patterns()
        self._punctuation_patterns = self._build_punctuation_patterns()
        self._dialogue_patterns = self._build_dialogue_patterns()
        self._emotional_patterns = self._build_emotional_patterns()
        self._abbreviation_patterns = self._build_abbreviation_patterns()
        
        # Processing statistics
        self.processing_stats = {
            'total_processed': 0,
            'sound_words_removed': 0,
            'punctuation_fixes': 0,
            'dialogue_tags_detected': 0,
            'emotional_cues_extracted': 0,
            'quality_improvements': 0
        }
        
        logger.info(f"Advanced Text Processor initialized with {self.config.mode.value} mode")
    
    def _build_sound_word_patterns(self) -> List[re.Pattern]:
        """Build comprehensive sound word removal patterns"""
        patterns = [
            # Basic filler sounds
            r'\b(?:um+h*|uh+m*|er+|ah+|oh+|mm+|hmm+)\b',
            r'\b(?:umm+|uhh+|err+|ahh+|ohh+|mmm+)\b',
            
            # Extended filler words
            r'\b(?:like|you know|basically|literally|actually|sort of|kind of)\b',
            r'\b(?:I mean|well|so|anyway|whatever|somehow|somewhere)\b',
            
            # Verbal pauses and hesitations
            r'\b(?:uh-oh|oh-oh|oops|whoops|oopsie)\b',
            r'\b(?:let me see|let\'s see|how do I say|what\'s the word)\b',
            
            # Action descriptions in brackets/parentheses
            r'\*[^*]*\*',           # *action*
            r'\([^)]*\)',           # (aside)
            r'\[[^\]]*\]',          # [stage direction]
            r'\{[^}]*\}',           # {sound effect}
            
            # Vietnamese filler words
            r'\b(?:à|ờ|ừ|ư|ể|ô|ơ|eh|ah|oh)\b',
            r'\b(?:thì|là|mà|thế|này|kia|đó|đây)\b(?=\s+(?:thì|là|mà))',
            
            # Repetitive words (more than 2 consecutive)
            r'\b(\w+)(?:\s+\1){2,}\b',
            
            # False starts and corrections
            r'\b\w+--\w+\b',        # word--correction
            r'\b\w+\s*-\s*\w+\b',   # word - correction
            
            # Incomplete words with dashes
            r'\b\w+-\s',            # word- (incomplete)
            r'\s-\w+\b',            # -word (incomplete start)
            
            # Multiple punctuation cleanup
            r'[.]{3,}',             # Multiple periods
            r'[!]{2,}',             # Multiple exclamation
            r'[?]{2,}',             # Multiple question marks
            r'[,]{2,}',             # Multiple commas
            
            # Stuttering patterns
            r'\b(\w)\1{2,}\b',      # Repeated letters (aaa, bbb)
            r'\b(\w+)-\1\b',        # word-word repetition
            
            # Common speech disfluencies
            r'\b(?:well well|okay okay|yes yes|no no)\b',
            r'\b(?:and and|but but|or or|so so)\b',
            
            # Placeholder words
            r'\b(?:something|somewhere|someone|somehow|anything|whatever)\b(?=\s+(?:like|or))',
            
            # Excessive whitespace patterns
            r'\s{3,}',              # Multiple spaces
            r'\t+',                 # Tabs
            r'\n{3,}',              # Multiple newlines
            
            # Email/URL artifacts
            r'https?://[^\s]+',     # URLs
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
            
            # Social media artifacts  
            r'#\w+',                # Hashtags
            r'@\w+',                # Mentions
            r'\b(?:RT|DM|PM|LOL|OMG|WTF|BRB|TTYL)\b',  # Internet slang
            
            # Markdown artifacts
            r'\*\*([^*]+)\*\*',     # **bold**
            r'\*([^*]+)\*',         # *italic*
            r'`([^`]+)`',           # `code`
            r'~~([^~]+)~~',         # ~~strikethrough~~
        ]
        
        # Compile all patterns
        compiled_patterns = []
        for pattern in patterns:
            try:
                compiled_patterns.append(re.compile(pattern, re.IGNORECASE | re.MULTILINE))
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{pattern}': {e}")
        
        logger.info(f"Built {len(compiled_patterns)} sound word patterns")
        return compiled_patterns
    
    def _build_punctuation_patterns(self) -> Dict[str, re.Pattern]:
        """Build punctuation normalization patterns"""
        return {
            'ellipsis': re.compile(r'\.{3,}'),           # Multiple periods → …
            'exclamation': re.compile(r'!{2,}'),         # Multiple ! → !
            'question': re.compile(r'\?{2,}'),           # Multiple ? → ?
            'comma_space': re.compile(r',(?=\S)'),       # Missing space after comma
            'period_space': re.compile(r'\.(?=[A-Z])'),  # Missing space after period
            'quote_normalize': re.compile(r'["""]'),     # Smart quotes → "
            'apostrophe': re.compile(r"[''']"),          # Smart apostrophe → '
            'dash_normalize': re.compile(r'[–—]'),       # Em/en dash → -
            'space_punctuation': re.compile(r'\s+([.!?,:;])'),  # Space before punctuation
        }
    
    def _build_dialogue_patterns(self) -> Dict[str, re.Pattern]:
        """Build dialogue tag detection patterns"""
        return {
            'dialogue_tags': re.compile(r'(he said|she said|they said|said \w+|whispered|shouted|asked|replied|answered)', re.IGNORECASE),
            'quoted_speech': re.compile(r'"([^"]*)"'),
            'narrative_breaks': re.compile(r'\b(suddenly|meanwhile|later|then|next|finally)\b', re.IGNORECASE),
            'character_names': re.compile(r'^[A-Z][a-z]+:'),  # Character: dialogue format
        }
    
    def _build_emotional_patterns(self) -> Dict[str, re.Pattern]:
        """Build emotional cue extraction patterns"""
        return {
            'laughter': re.compile(r'\b(haha|hehe|lol|laughs?|chuckles?|giggles?)\b', re.IGNORECASE),
            'crying': re.compile(r'\b(sobs?|cries|weeps?|tears?|boo-hoo)\b', re.IGNORECASE),
            'surprise': re.compile(r'\b(wow|whoa|oh my|amazing|incredible|unbelievable)\b', re.IGNORECASE),
            'anger': re.compile(r'\b(damn|hell|angry|furious|mad|rage)\b', re.IGNORECASE),
            'joy': re.compile(r'\b(happy|joy|excited|thrilled|delighted|wonderful)\b', re.IGNORECASE),
            'sadness': re.compile(r'\b(sad|depressed|miserable|heartbroken|devastated)\b', re.IGNORECASE),
        }
    
    def _build_abbreviation_patterns(self) -> Dict[str, str]:
        """Build abbreviation expansion patterns"""
        return {
            r'\bdr\.': 'doctor',
            r'\bmr\.': 'mister', 
            r'\bmrs\.': 'missus',
            r'\bms\.': 'miss',
            r'\bprof\.': 'professor',
            r'\betc\.': 'etcetera',
            r'\bvs\.': 'versus',
            r'\be\.g\.': 'for example',
            r'\bi\.e\.': 'that is',
            r'\bco\.': 'company',
            r'\binc\.': 'incorporated',
            r'\bllc\.': 'limited liability company',
            r'\bst\.': 'street',
            r'\bave\.': 'avenue',
            r'\brd\.': 'road',
            r'\bblvd\.': 'boulevard',
        }
    
    def smart_remove_sound_words(self, text: str) -> Tuple[str, int]:
        """
        Remove sound words using sophisticated patterns
        Returns: (cleaned_text, removed_count)
        """
        removed_count = 0
        processed_text = text
        
        for pattern in self._sound_word_patterns:
            matches = pattern.findall(processed_text)
            if matches:
                removed_count += len(matches)
                processed_text = pattern.sub(' ', processed_text)
        
        # Clean up extra whitespace
        processed_text = re.sub(r'\s+', ' ', processed_text).strip()
        
        return processed_text, removed_count
    
    def normalize_punctuation(self, text: str) -> Tuple[str, int]:
        """
        Normalize punctuation using advanced patterns
        Returns: (normalized_text, fixes_count)
        """
        fixes_count = 0
        processed_text = text
        
        for name, pattern in self._punctuation_patterns.items():
            original_text = processed_text
            
            if name == 'ellipsis':
                processed_text = pattern.sub('…', processed_text)
            elif name == 'exclamation':
                processed_text = pattern.sub('!', processed_text)
            elif name == 'question':
                processed_text = pattern.sub('?', processed_text)
            elif name == 'comma_space':
                processed_text = pattern.sub(', ', processed_text)
            elif name == 'period_space':
                processed_text = pattern.sub('. ', processed_text)
            elif name == 'quote_normalize':
                processed_text = pattern.sub('"', processed_text)
            elif name == 'apostrophe':
                processed_text = pattern.sub("'", processed_text)
            elif name == 'dash_normalize':
                processed_text = pattern.sub('-', processed_text)
            elif name == 'space_punctuation':
                processed_text = pattern.sub(r'\1', processed_text)
            
            if processed_text != original_text:
                fixes_count += 1
        
        return processed_text, fixes_count
    
    def detect_dialogue_tags(self, text: str) -> Dict[str, List[str]]:
        """Detect and extract dialogue-related elements"""
        dialogue_info = {
            'dialogue_tags': [],
            'quoted_speech': [],
            'narrative_breaks': [],
            'character_names': []
        }
        
        for tag_type, pattern in self._dialogue_patterns.items():
            matches = pattern.findall(text)
            dialogue_info[tag_type] = matches
        
        return dialogue_info
    
    def extract_emotional_cues(self, text: str) -> Dict[str, List[str]]:
        """Extract emotional indicators from text"""
        emotional_cues = {}
        
        for emotion, pattern in self._emotional_patterns.items():
            matches = pattern.findall(text)
            if matches:
                emotional_cues[emotion] = matches
        
        return emotional_cues
    
    def expand_abbreviations(self, text: str) -> Tuple[str, int]:
        """Expand common abbreviations"""
        expansions_count = 0
        processed_text = text
        
        for abbrev_pattern, expansion in self._abbreviation_patterns.items():
            original_text = processed_text
            processed_text = re.sub(abbrev_pattern, expansion, processed_text, flags=re.IGNORECASE)
            
            if processed_text != original_text:
                expansions_count += 1
        
        return processed_text, expansions_count
    
    def calculate_text_quality_score(self, original_text: str, processed_text: str) -> float:
        """
        Calculate text quality improvement score
        Returns: score between 0.0 and 1.0
        """
        factors = {
            'length_reduction': 0.3,    # Shorter is often better for TTS
            'punctuation_ratio': 0.2,   # Good punctuation improves flow
            'word_variety': 0.2,        # Less repetition is better
            'sentence_structure': 0.3   # Balanced sentence lengths
        }
        
        scores = {}
        
        # Length reduction factor (removing filler improves quality)
        len_original = len(original_text)
        len_processed = len(processed_text)
        if len_original > 0:
            reduction_ratio = (len_original - len_processed) / len_original
            scores['length_reduction'] = min(1.0, reduction_ratio * 2)  # Cap at 50% reduction
        else:
            scores['length_reduction'] = 0.0
        
        # Punctuation ratio
        punct_chars = sum(1 for c in processed_text if c in '.!?,:;')
        word_count = len(processed_text.split())
        if word_count > 0:
            punct_ratio = punct_chars / word_count
            scores['punctuation_ratio'] = min(1.0, punct_ratio * 5)  # Ideal ~0.2 ratio
        else:
            scores['punctuation_ratio'] = 0.0
        
        # Word variety (unique words / total words)
        words = processed_text.lower().split()
        if words:
            unique_words = len(set(words))
            variety_ratio = unique_words / len(words)
            scores['word_variety'] = variety_ratio
        else:
            scores['word_variety'] = 0.0
        
        # Sentence structure (balance of sentence lengths)
        sentences = re.split(r'[.!?]+', processed_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            avg_length = sum(lengths) / len(lengths)
            # Ideal sentence length for TTS: 8-15 words
            ideal_score = 1.0 - abs(avg_length - 11.5) / 11.5
            scores['sentence_structure'] = max(0.0, ideal_score)
        else:
            scores['sentence_structure'] = 0.0
        
        # Calculate weighted average
        total_score = sum(scores[factor] * weight for factor, weight in factors.items())
        
        return total_score
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Complete text processing pipeline
        Returns comprehensive processing results
        """
        if not text or not text.strip():
            return {
                'original_text': text,
                'processed_text': text,
                'quality_score': 0.0,
                'improvements': {},
                'dialogue_info': {},
                'emotional_cues': {},
                'processing_stats': {}
            }
        
        self.processing_stats['total_processed'] += 1
        
        processed_text = text
        improvements = {}
        
        # Step 1: Remove sound words (if enabled)
        if self.config.remove_sound_words:
            processed_text, removed_count = self.smart_remove_sound_words(processed_text)
            improvements['sound_words_removed'] = removed_count
            self.processing_stats['sound_words_removed'] += removed_count
        
        # Step 2: Normalize punctuation (if enabled)
        if self.config.normalize_punctuation:
            processed_text, fixes_count = self.normalize_punctuation(processed_text)
            improvements['punctuation_fixes'] = fixes_count
            self.processing_stats['punctuation_fixes'] += fixes_count
        
        # Step 3: Expand abbreviations (if enabled)
        if self.config.fix_abbreviations:
            processed_text, expansions_count = self.expand_abbreviations(processed_text)
            improvements['abbreviations_expanded'] = expansions_count
        
        # Step 4: Detect dialogue elements (if enabled)
        dialogue_info = {}
        if self.config.detect_dialogue_tags:
            dialogue_info = self.detect_dialogue_tags(processed_text)
            self.processing_stats['dialogue_tags_detected'] += len(dialogue_info.get('dialogue_tags', []))
        
        # Step 5: Extract emotional cues (if enabled)
        emotional_cues = {}
        if self.config.extract_emotional_cues:
            emotional_cues = self.extract_emotional_cues(processed_text)
            self.processing_stats['emotional_cues_extracted'] += len(emotional_cues)
        
        # Step 6: Calculate quality score
        quality_score = self.calculate_text_quality_score(text, processed_text)
        
        if quality_score > self.config.quality_threshold:
            self.processing_stats['quality_improvements'] += 1
        
        return {
            'original_text': text,
            'processed_text': processed_text,
            'quality_score': quality_score,
            'improvements': improvements,
            'dialogue_info': dialogue_info,
            'emotional_cues': emotional_cues,
            'processing_stats': dict(self.processing_stats)
        }
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        stats = dict(self.processing_stats)
        
        if stats['total_processed'] > 0:
            stats['average_sound_words_per_text'] = stats['sound_words_removed'] / stats['total_processed']
            stats['average_punctuation_fixes_per_text'] = stats['punctuation_fixes'] / stats['total_processed']
            stats['quality_improvement_rate'] = (stats['quality_improvements'] / stats['total_processed']) * 100
        
        return stats

# Factory functions for different processing modes
def create_conservative_processor() -> AdvancedTextProcessor:
    """Create conservative text processor (minimal changes)"""
    config = TextProcessingConfig(
        mode=ProcessingMode.CONSERVATIVE,
        remove_sound_words=False,
        normalize_punctuation=True,
        detect_dialogue_tags=False,
        extract_emotional_cues=False,
        fix_abbreviations=True,
        smart_joining=False,
        quality_threshold=0.5
    )
    return AdvancedTextProcessor(config)

def create_standard_processor() -> AdvancedTextProcessor:
    """Create standard text processor (balanced processing)"""
    config = TextProcessingConfig(
        mode=ProcessingMode.STANDARD,
        remove_sound_words=True,
        normalize_punctuation=True,
        detect_dialogue_tags=True,
        extract_emotional_cues=True,
        fix_abbreviations=True,
        smart_joining=True,
        quality_threshold=0.7
    )
    return AdvancedTextProcessor(config)

def create_aggressive_processor() -> AdvancedTextProcessor:
    """Create aggressive text processor (maximum cleaning)"""
    config = TextProcessingConfig(
        mode=ProcessingMode.AGGRESSIVE,
        remove_sound_words=True,
        normalize_punctuation=True,
        detect_dialogue_tags=True,
        extract_emotional_cues=True,
        fix_abbreviations=True,
        smart_joining=True,
        recursive_splitting=True,
        max_sentence_length=150,
        quality_threshold=0.8
    )
    return AdvancedTextProcessor(config) 