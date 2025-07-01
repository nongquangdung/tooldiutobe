#!/usr/bin/env python3
"""
🎙️ VOICE STUDIO TTS API SERVER
==============================

FastAPI server providing TTS endpoints for Voice Studio V2
Supports both Manual mode and JSON mode with multi-provider voice generation
"""

import os
import sys
import uuid
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiofiles
import uvicorn

# Add proper Python path setup
CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
SRC_DIR = PROJECT_ROOT / "src"

# Add to Python path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_DIR))

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Try to import with fallback for missing dependencies
try:
    from tts.enhanced_voice_generator import EnhancedVoiceGenerator, VoiceGenerationRequest, VoiceGenerationResult
    from tts.chatterbox_voices_integration import ChatterboxConfig
    TTS_AVAILABLE = True
    print("✅ TTS imports successful - using REAL TTS!")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"TTS imports failed: {e}. Running in mock mode.")
    TTS_AVAILABLE = False
    print("❌ TTS imports failed - using mock mode")
    
    # Mock classes for development
    class VoiceGenerationRequest:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class VoiceGenerationResult:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class MockEnhancedVoiceGenerator:
        def get_available_voices(self):
            return {
                "olivia": {"name": "Olivia", "gender": "female", "provider": "chatterbox", "quality": 9.2, "description": "Warm, professional female voice"},
                "gabriel": {"name": "Gabriel", "gender": "male", "provider": "chatterbox", "quality": 9.0, "description": "Deep, authoritative male voice"},
                "emily": {"name": "Emily", "gender": "female", "provider": "chatterbox", "quality": 8.8, "description": "Young, energetic female voice"},
                "alexander": {"name": "Alexander", "gender": "male", "provider": "chatterbox", "quality": 8.9, "description": "Sophisticated male voice"},
                "aaron": {"name": "Aaron", "gender": "male", "provider": "chatterbox", "quality": 8.7, "description": "Friendly male voice"},
                "alice": {"name": "Alice", "gender": "female", "provider": "chatterbox", "quality": 8.6, "description": "Clear, articulate female voice"}
            }
        
        def get_best_voice_for_character(self, character_type: str, gender_preference: Optional[str] = None, quality_threshold: float = 8.0):
            if gender_preference == "male":
                return "gabriel"
            elif gender_preference == "female":
                return "olivia"
            else:
                return "olivia"
        
        @property
        def voice_quality_map(self):
            return self.get_available_voices()
        
        def generate_voice(self, request: VoiceGenerationRequest):
            # Mock generation - create empty file for testing
            import time
            time.sleep(2)  # Simulate processing time
            Path(request.output_path).touch()
            return VoiceGenerationResult(
                success=True,
                output_path=request.output_path,
                voice_used=getattr(request, 'voice_id', 'olivia'),
                provider_used="mock",
                generation_time=2.0,
                quality_score=8.5,
                error_message=""
            )

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Voice Studio TTS API",
    description="Advanced TTS API with multi-provider support",
    version="2.0.0"
)

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TTS system
if TTS_AVAILABLE:
    # Use real TTS if available
    tts_generator = EnhancedVoiceGenerator()
    print("🎤 Using REAL Enhanced Voice Generator!")
else:
    # Use mock class if imports failed
    tts_generator = MockEnhancedVoiceGenerator()
    print("🤖 Using MOCK Voice Generator for testing")

# Output directory for generated audio
OUTPUT_DIR = Path("voice_studio_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Static files for serving audio
app.mount("/audio", StaticFiles(directory=str(OUTPUT_DIR)), name="audio")

# Job tracking
job_status = {}

# ========================
# PYDANTIC MODELS
# ========================

class ManualTTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice: str = "olivia"
    emotion: str = "neutral"
    inner_voice: bool = False
    inner_voice_type: str = "light"
    speed: float = 1.0
    temperature: float = 0.7
    exaggeration: float = 1.0

class Character(BaseModel):
    id: str
    name: str
    gender: str
    voice: Optional[str] = None

class Dialogue(BaseModel):
    speaker: str
    text: str
    emotion: str = "neutral"
    inner_voice: bool = False
    inner_voice_type: str = "light"

class Segment(BaseModel):
    id: int
    dialogues: List[Dialogue]

class JSONTTSRequest(BaseModel):
    segments: List[Segment]
    characters: List[Character]
    language: str = "en"
    speed: float = 1.0
    temperature: float = 0.7

class TTSResponse(BaseModel):
    success: bool
    job_id: str
    audio_url: Optional[str] = None
    message: str
    metadata: Optional[Dict[str, Any]] = None

# ========================
# VOICE MANAGEMENT
# ========================

@app.get("/api/voices/available")
async def get_available_voices():
    """Get all available voices from all providers"""
    try:
        voices = tts_generator.get_available_voices()
        
        # Format for frontend
        formatted_voices = []
        for voice_id, info in voices.items():
            formatted_voices.append({
                "id": voice_id,
                "name": info["name"],
                "gender": info["gender"],
                "provider": info["provider"],
                "quality": info["quality"],
                "description": info["description"]
            })
        
        return {
            "success": True,
            "voices": formatted_voices,
            "total_count": len(formatted_voices)
        }
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/voices/by-language/{language}")
async def get_voices_by_language(language: str):
    """Get voices filtered by language (future enhancement)"""
    # For now, return all voices - will be enhanced with language-specific filtering
    return await get_available_voices()

@app.get("/api/voices/recommend/{character_type}")
async def recommend_voice(character_type: str, gender: Optional[str] = None):
    """Get voice recommendation for character type"""
    try:
        recommended_voice = tts_generator.get_best_voice_for_character(
            character_type=character_type,
            gender_preference=gender,
            quality_threshold=8.0
        )
        
        voice_info = tts_generator.voice_quality_map.get(recommended_voice, {})
        
        return {
            "success": True,
            "recommended_voice": recommended_voice,
            "voice_info": voice_info
        }
    except Exception as e:
        logger.error(f"Error recommending voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# MANUAL MODE TTS
# ========================

@app.post("/api/tts/manual", response_model=TTSResponse)
async def generate_manual_tts(request: ManualTTSRequest, background_tasks: BackgroundTasks):
    """Generate TTS for manual mode (single narrator)"""
    try:
        job_id = str(uuid.uuid4())
        
        # Create output filename
        output_filename = f"manual_{job_id}.mp3"
        output_path = OUTPUT_DIR / output_filename
        
        # Create voice generation request
        voice_request = VoiceGenerationRequest(
            text=request.text,
            character_id="narrator",
            voice_id=request.voice,
            emotion=request.emotion,
            speed=request.speed,
            temperature=request.temperature,
            exaggeration=request.exaggeration,
            output_path=str(output_path)
        )
        
        # Add background task for generation
        background_tasks.add_task(generate_audio_task, voice_request, job_id)
        
        return TTSResponse(
            success=True,
            job_id=job_id,
            message="Manual TTS generation started",
            metadata={
                "mode": "manual",
                "voice": request.voice,
                "language": request.language,
                "text_length": len(request.text)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in manual TTS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# JSON MODE TTS
# ========================

@app.post("/api/tts/json", response_model=TTSResponse)
async def generate_json_tts(request: JSONTTSRequest, background_tasks: BackgroundTasks):
    """Generate TTS for JSON mode (multi-character)"""
    try:
        job_id = str(uuid.uuid4())
        
        # Create output directory for this job
        job_output_dir = OUTPUT_DIR / f"json_{job_id}"
        job_output_dir.mkdir(exist_ok=True)
        
        # Add background task for generation
        background_tasks.add_task(generate_json_audio_task, request, job_id)
        
        return TTSResponse(
            success=True,
            job_id=job_id,
            message="JSON TTS generation started",
            metadata={
                "mode": "json",
                "segments_count": len(request.segments),
                "characters_count": len(request.characters),
                "language": request.language
            }
        )
        
    except Exception as e:
        logger.error(f"Error in JSON TTS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# FILE UPLOAD & PROCESSING
# ========================

@app.post("/api/upload/json-script")
async def upload_json_script(file: UploadFile = File(...)):
    """Upload and parse JSON script file"""
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="File must be a JSON file")
        
        # Read and parse JSON
        content = await file.read()
        script_data = json.loads(content.decode('utf-8'))
        
        # Extract characters and segments
        characters = []
        segments = []
        
        # Auto-detect characters from script
        if "characters" in script_data:
            characters = script_data["characters"]
        elif "segments" in script_data:
            # Extract characters from dialogues
            character_names = set()
            for segment in script_data["segments"]:
                for dialogue in segment.get("dialogues", []):
                    character_names.add(dialogue.get("speaker", ""))
            
            # Create character objects
            characters = [
                {
                    "id": name.lower().replace(" ", "_"),
                    "name": name,
                    "gender": "neutral",
                    "voice": None
                }
                for name in character_names if name
            ]
        
        segments = script_data.get("segments", [])
        
        return {
            "success": True,
            "script_data": {
                "characters": characters,
                "segments": segments
            },
            "message": f"Successfully parsed script with {len(characters)} characters and {len(segments)} segments"
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Error processing JSON script: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# JOB STATUS & RESULTS
# ========================

@app.get("/api/job/{job_id}/status")
async def get_job_status(job_id: str):
    """Get job generation status"""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status[job_id]

@app.get("/api/job/{job_id}/download")
async def download_audio(job_id: str):
    """Download generated audio file"""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_info = job_status[job_id]
    if not job_info.get("completed", False):
        raise HTTPException(status_code=202, detail="Job still processing")
    
    if not job_info.get("success", False):
        raise HTTPException(status_code=500, detail=job_info.get("error", "Generation failed"))
    
    audio_path = job_info.get("output_path")
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=f"voice_studio_{job_id}.mp3"
    )

# ========================
# BACKGROUND TASKS
# ========================

async def generate_audio_task(voice_request: VoiceGenerationRequest, job_id: str):
    """Background task for manual audio generation"""
    try:
        # Update job status
        job_status[job_id] = {
            "status": "processing",
            "progress": 0,
            "completed": False,
            "success": False
        }
        
        # Generate audio
        result = tts_generator.generate_voice(voice_request)
        
        # Update final status
        job_status[job_id] = {
            "status": "completed" if result.success else "failed",
            "progress": 100,
            "completed": True,
            "success": result.success,
            "output_path": result.output_path if result.success else None,
            "error": result.error_message if not result.success else None,
            "metadata": {
                "voice_used": result.voice_used,
                "provider_used": result.provider_used,
                "generation_time": result.generation_time,
                "quality_score": result.quality_score
            }
        }
        
        logger.info(f"Manual TTS job {job_id} completed: {result.success}")
        
    except Exception as e:
        logger.error(f"Error in manual TTS generation: {e}")
        job_status[job_id] = {
            "status": "failed",
            "progress": 0,
            "completed": True,
            "success": False,
            "error": str(e)
        }

async def generate_json_audio_task(request: JSONTTSRequest, job_id: str):
    """Background task for JSON mode audio generation"""
    try:
        # Update job status
        job_status[job_id] = {
            "status": "processing",
            "progress": 0,
            "completed": False,
            "success": False
        }
        
        job_output_dir = OUTPUT_DIR / f"json_{job_id}"
        generated_files = []
        
        total_dialogues = sum(len(segment.dialogues) for segment in request.segments)
        processed_dialogues = 0
        
        # Generate audio for each dialogue
        for segment in request.segments:
            for dialogue_idx, dialogue in enumerate(segment.dialogues):
                # Find character voice
                character_voice = "olivia"  # Default
                for char in request.characters:
                    if char.id == dialogue.speaker or char.name == dialogue.speaker:
                        character_voice = char.voice or character_voice
                        break
                
                # Create voice request
                output_filename = f"s{segment.id}_d{dialogue_idx + 1}_{dialogue.speaker}.mp3"
                output_path = job_output_dir / output_filename
                
                voice_request = VoiceGenerationRequest(
                    text=dialogue.text,
                    character_id=dialogue.speaker,
                    voice_id=character_voice,
                    emotion=dialogue.emotion,
                    speed=request.speed,
                    temperature=request.temperature,
                    output_path=str(output_path)
                )
                
                # Generate audio
                result = tts_generator.generate_voice(voice_request)
                
                if result.success:
                    generated_files.append({
                        "segment_id": segment.id,
                        "dialogue_index": dialogue_idx,
                        "speaker": dialogue.speaker,
                        "file_path": str(output_path),
                        "file_url": f"/audio/json_{job_id}/{output_filename}"
                    })
                
                processed_dialogues += 1
                progress = int((processed_dialogues / total_dialogues) * 100)
                
                # Update progress
                job_status[job_id]["progress"] = progress
        
        # Create combined audio file (optional)
        combined_path = job_output_dir / "complete_audio.mp3"
        
        # Update final status
        job_status[job_id] = {
            "status": "completed",
            "progress": 100,
            "completed": True,
            "success": True,
            "output_path": str(combined_path),
            "generated_files": generated_files,
            "metadata": {
                "total_dialogues": total_dialogues,
                "successful_generations": len(generated_files),
                "language": request.language
            }
        }
        
        logger.info(f"JSON TTS job {job_id} completed with {len(generated_files)} files")
        
    except Exception as e:
        logger.error(f"Error in JSON TTS generation: {e}")
        job_status[job_id] = {
            "status": "failed",
            "progress": 0,
            "completed": True,
            "success": False,
            "error": str(e)
        }

# ========================
# SYSTEM STATUS
# ========================

@app.get("/api/system/status")
async def get_system_status():
    """Get system status and provider availability"""
    try:
        provider_status = tts_generator.get_provider_status()
        
        return {
            "success": True,
            "providers": provider_status,
            "total_voices": len(tts_generator.get_available_voices()),
            "system_ready": True
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {
            "success": False,
            "error": str(e),
            "system_ready": False
        }

# ========================
# STARTUP
# ========================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("🎙️ Voice Studio TTS API Server starting...")
    logger.info(f"📁 Output directory: {OUTPUT_DIR}")
    logger.info("🚀 Voice Studio TTS API ready!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 