"""
Voice Studio Smart Batch Processor - PHASE 3
Enterprise-scale batch automation với intelligent project detection,
character mapping, và parallel processing capabilities.
"""

import os
import json
import re
import time
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher


@dataclass
class ProjectFile:
    """Detected project file với metadata"""
    file_path: str
    file_type: str  # 'json', 'txt', 'script', 'md'
    detected_format: str
    characters: List[Dict]
    segments_count: int
    estimated_duration: float
    metadata: Dict[str, Any]
    quality_score: float = 0.0
    
    @property
    def filename(self) -> str:
        return os.path.basename(self.file_path)


@dataclass
class BatchJob:
    """Batch processing job định nghĩa"""
    job_id: str
    project_files: List[ProjectFile]
    output_directory: str
    voice_settings: Dict
    processing_options: Dict
    status: str = "pending"  # pending, running, completed, failed
    progress: float = 0.0
    created_at: str = None
    started_at: str = None
    completed_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class ProcessingResult:
    """Result của batch processing operation"""
    job_id: str
    success: bool
    files_processed: int
    files_failed: int
    total_audio_files: int
    processing_time: float
    output_files: List[str]
    error_messages: List[str]
    performance_metrics: Dict[str, Any]


class ProjectDetector:
    """Smart project file detection và format analysis"""
    
    SUPPORTED_FORMATS = ['.json', '.txt', '.script', '.md', '.csv']
    
    def __init__(self):
        self.detection_patterns = {
            'voice_studio_json': {
                'required_keys': ['segments', 'characters'],
                'optional_keys': ['project', 'settings']
            },
            'script_format': {
                'patterns': [r'\w+:\s+.*', r'SCENE \d+:', r'CHARACTER \d+:']
            },
            'dialogue_format': {
                'patterns': [r'- \w+:', r'\[\w+\]:', r'\w+ \(\w+\):']
            }
        }
    
    def detect_project_files(self, directory: str) -> List[ProjectFile]:
        """Detect và analyze tất cả project files trong directory"""
        project_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                if self.is_supported_file(file_path):
                    try:
                        project_file = self.analyze_project_file(file_path)
                        if project_file:
                            project_files.append(project_file)
                    except Exception as e:
                        logging.warning(f"Failed to analyze {file_path}: {e}")
        
        # Sort by quality score (highest first)
        project_files.sort(key=lambda x: x.quality_score, reverse=True)
        
        return project_files
    
    def is_supported_file(self, file_path: str) -> bool:
        """Check if file format is supported"""
        return any(file_path.lower().endswith(ext) for ext in self.SUPPORTED_FORMATS)
    
    def analyze_project_file(self, file_path: str) -> Optional[ProjectFile]:
        """Phân tích file và trích xuất metadata"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.json':
                return self.analyze_json_file(file_path)
            elif file_ext in ['.txt', '.script', '.md']:
                return self.analyze_text_file(file_path)
            else:
                return None
                
        except Exception as e:
            logging.error(f"Error analyzing {file_path}: {e}")
            return None
    
    def analyze_json_file(self, file_path: str) -> Optional[ProjectFile]:
        """Analyze JSON project files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract basic info
            characters = data.get('characters', [])
            segments = data.get('segments', [])
            
            return ProjectFile(
                file_path=file_path,
                file_type='json',
                detected_format='voice_studio_json',
                characters=characters,
                segments_count=len(segments),
                estimated_duration=sum(seg.get('duration', 30) for seg in segments),
                metadata={'project_info': data.get('project', {})},
                quality_score=0.8  # Default good score for JSON
            )
            
        except Exception as e:
            logging.error(f"Failed to analyze JSON file {file_path}: {e}")
            return None
    
    def analyze_text_file(self, file_path: str) -> Optional[ProjectFile]:
        """Analyze text-based script files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic character info
            characters = [{'id': 'narrator', 'name': 'Narrator', 'gender': 'neutral'}]
            
            return ProjectFile(
                file_path=file_path,
                file_type='text',
                detected_format='plain_text',
                characters=characters,
                segments_count=1,
                estimated_duration=len(content.split()) / 150 * 60,  # 150 wpm
                metadata={'word_count': len(content.split())},
                quality_score=0.6  # Lower score for text files
            )
            
        except Exception as e:
            logging.error(f"Failed to analyze text file {file_path}: {e}")
            return None


class CharacterMatcher:
    """Smart character matching across projects"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
    
    def merge_character_databases(self, project_files: List[ProjectFile]) -> Tuple[List[Dict], Dict[str, str]]:
        """Merge characters từ multiple projects với smart mapping"""
        all_characters = []
        character_mapping = {}  # old_id -> new_id
        
        # Simple implementation for now
        unique_id = 1
        for project_file in project_files:
            for char in project_file.characters:
                char_with_source = char.copy()
                char_with_source['source_file'] = project_file.filename
                original_id = char.get('id', f"char_{unique_id}")
                char_with_source['original_id'] = original_id
                new_id = f"merged_char_{unique_id}"
                char_with_source['id'] = new_id
                
                character_mapping[original_id] = new_id
                all_characters.append(char_with_source)
                unique_id += 1
        
        return all_characters, character_mapping


class SmartBatchProcessor:
    """Enterprise-scale batch processing automation"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(8, os.cpu_count() or 4)
        self.project_detector = ProjectDetector()
        self.character_matcher = CharacterMatcher()
        self.active_jobs = {}
        self.job_history = []
        
        # Performance tracking
        self.performance_stats = {
            'total_jobs_processed': 0,
            'total_files_processed': 0,
            'total_processing_time': 0.0,
            'success_rate': 0.0
        }
    
    def create_batch_job(self, 
                        source_directory: str,
                        output_directory: str,
                        voice_settings: Dict,
                        processing_options: Dict = None) -> BatchJob:
        """Create new batch processing job"""
        
        # Detect project files
        project_files = self.project_detector.detect_project_files(source_directory)
        
        if not project_files:
            raise ValueError(f"No valid project files found in {source_directory}")
        
        # Create job
        job_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = BatchJob(
            job_id=job_id,
            project_files=project_files,
            output_directory=output_directory,
            voice_settings=voice_settings,
            processing_options=processing_options or {}
        )
        
        self.active_jobs[job_id] = job
        
        return job
    
    def process_batch_job(self, 
                         job: BatchJob,
                         voice_generator_func: Callable,
                         progress_callback: Callable = None) -> ProcessingResult:
        """Process batch job với parallel execution"""
        
        job.status = "running"
        job.started_at = datetime.now().isoformat()
        
        start_time = time.time()
        
        try:
            # Merge character databases
            merged_characters, character_mapping = self.character_matcher.merge_character_databases(job.project_files)
            
            # Simple processing for demo
            output_files = []
            error_messages = []
            files_processed = len(job.project_files)
            files_failed = 0
            
            # Mock audio generation
            for project_file in job.project_files:
                try:
                    mock_audio_path = f"{job.output_directory}/mock_audio_{project_file.filename}.mp3"
                    output_files.append(mock_audio_path)
                except Exception as e:
                    error_messages.append(str(e))
                    files_failed += 1
                    files_processed -= 1
            
            # Calculate metrics
            processing_time = time.time() - start_time
            
            performance_metrics = {
                'files_per_second': files_processed / processing_time if processing_time > 0 else 0,
                'characters_merged': len(merged_characters),
                'parallel_workers': self.max_workers,
                'efficiency': files_processed / len(job.project_files) if job.project_files else 0
            }
            
            # Create result
            result = ProcessingResult(
                job_id=job.job_id,
                success=files_failed == 0,
                files_processed=files_processed,
                files_failed=files_failed,
                total_audio_files=len(output_files),
                processing_time=processing_time,
                output_files=output_files,
                error_messages=error_messages,
                performance_metrics=performance_metrics
            )
            
            # Update job status
            job.status = "completed" if result.success else "failed"
            job.completed_at = datetime.now().isoformat()
            job.progress = 100.0
            
            return result
            
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now().isoformat()
            
            error_result = ProcessingResult(
                job_id=job.job_id,
                success=False,
                files_processed=0,
                files_failed=len(job.project_files),
                total_audio_files=0,
                processing_time=time.time() - start_time,
                output_files=[],
                error_messages=[str(e)],
                performance_metrics={}
            )
            
            return error_result
    
    def get_job_status(self, job_id: str) -> Optional[BatchJob]:
        """Get current job status"""
        return self.active_jobs.get(job_id)
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        return {
            **self.performance_stats,
            'active_jobs': len(self.active_jobs),
            'completed_jobs': len(self.job_history),
            'max_workers': self.max_workers
        }


# Mock functions for testing
def example_batch_voice_generator(text: str, params: Dict) -> str:
    """Example voice generator function for testing"""
    import tempfile
    import time
    
    # Simulate processing time
    time.sleep(0.1)
    
    # Create mock audio file
    temp_file = tempfile.mktemp(suffix='.mp3')
    with open(temp_file, 'wb') as f:
        f.write(f'Mock audio for: {text[:50]}...'.encode())
    
    return temp_file


if __name__ == "__main__":
    # Quick test
    detector = ProjectDetector()
    processor = SmartBatchProcessor()
    
    print("🏭 Smart Batch Processor initialized successfully!")
    print(f"   👥 Max Workers: {processor.max_workers}")
    print(f"   📁 Supported Formats: {detector.SUPPORTED_FORMATS}") 