#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple TTS Server Demo for Voice Studio Web V2.0
Tạo server demo đơn giản để test frontend trước khi setup đầy đủ
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import tempfile
import wave
import numpy as np
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Voice Studio Web V2.0 - Demo Server",
    description="Simple TTS demo server for testing",
    version="2.0.0"
)

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TTSRequest(BaseModel):
    input: str
    model: Optional[str] = "demo-voice"
    voice: Optional[str] = "default"
    response_format: Optional[str] = "wav"
    speed: Optional[float] = 1.0
    exaggeration: Optional[float] = 1.0
    cfg_weight: Optional[float] = 1.0
    temperature: Optional[float] = 1.0

# Predefined voices list (matching Chatterbox format)
DEMO_VOICES = {
    "female-voice-1": {"name": "Emma", "gender": "female", "language": "en"},
    "female-voice-2": {"name": "Olivia", "gender": "female", "language": "en"},
    "female-voice-3": {"name": "Ava", "gender": "female", "language": "en"},
    "female-voice-4": {"name": "Isabella", "gender": "female", "language": "en"},
    "female-voice-5": {"name": "Sophia", "gender": "female", "language": "en"},
    "male-voice-1": {"name": "Liam", "gender": "male", "language": "en"},
    "male-voice-2": {"name": "Noah", "gender": "male", "language": "en"},
    "male-voice-3": {"name": "Oliver", "gender": "male", "language": "en"},
    "male-voice-4": {"name": "William", "gender": "male", "language": "en"},
    "male-voice-5": {"name": "James", "gender": "male", "language": "en"},
}

def generate_demo_audio(text: str, duration: float = 2.0, sample_rate: int = 22050):
    """
    Generate a simple sine wave audio as demo
    Tạo audio demo đơn giản để test
    """
    # Generate a sine wave based on text length
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create different frequencies for different voices
    base_freq = 440  # A4 note
    text_hash = hash(text) % 1000
    frequency = base_freq + (text_hash / 10)  # Vary frequency based on text
    
    # Generate sine wave
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Add some variation to make it more interesting
    audio_data += np.sin(2 * np.pi * frequency * 1.5 * t) * 0.1
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    return audio_data

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Voice Studio Web V2.0 - Demo Server",
        "version": "2.0.0",
        "status": "running",
        "demo": True,
        "endpoints": {
            "tts": "/v1/audio/speech",
            "voices": "/v1/voices",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Voice Studio Web V2.0 Demo",
        "demo_mode": True
    }

@app.get("/v1/voices")
async def get_voices():
    """Get available voices (demo)"""
    return {
        "voices": DEMO_VOICES,
        "total": len(DEMO_VOICES),
        "demo_mode": True
    }

@app.post("/v1/audio/speech")
async def text_to_speech(request: TTSRequest):
    """
    OpenAI-compatible TTS endpoint (demo)
    Generates demo audio for testing frontend
    """
    try:
        text = request.input.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text input is required")
        
        if len(text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
        
        # Generate demo audio
        duration = min(max(len(text) / 20, 1.0), 10.0)  # 1-10 seconds based on text length
        audio_data = generate_demo_audio(text, duration)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            # Write WAV header and data
            with wave.open(tmp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(22050)  # Sample rate
                wav_file.writeframes(audio_data.tobytes())
            
            # Return the audio file
            return FileResponse(
                tmp_file.name,
                media_type="audio/wav",
                filename=f"demo_tts_{hash(text) % 10000}.wav",
                headers={
                    "X-Demo-Mode": "true",
                    "X-Voice-Studio": "2.0",
                    "Cache-Control": "no-cache"
                }
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@app.get("/demo")
async def demo_info():
    """Demo information"""
    return {
        "title": "Voice Studio Web V2.0 - Demo Mode",
        "description": "This is a demo server generating synthetic audio for testing.",
        "features": {
            "basic_tts": "✅ Generating demo audio",
            "multiple_voices": "✅ 10 demo voices available",
            "emotion_system": "⚠️  Requires full Chatterbox setup",
            "voice_cloning": "⚠️  Requires full Chatterbox setup",
            "real_tts": "⚠️  Requires full Chatterbox TTS engine"
        },
        "next_steps": [
            "1. Test frontend with this demo server",
            "2. Install full Chatterbox TTS dependencies",
            "3. Replace with real TTS engine"
        ],
        "ports": {
            "demo_server": 8005,
            "frontend": 8080
        }
    }

if __name__ == "__main__":
    print("🎵 =================================")
    print("🎵  Voice Studio Web V2.0 Demo")
    print("🎵 =================================")
    print("")
    print("🚀 Starting demo server...")
    print("📡 Server: http://localhost:8005")
    print("🎬 Demo info: http://localhost:8005/demo")
    print("🔧 This is DEMO mode - generates synthetic audio")
    print("")
    print("✅ Ready for frontend testing!")
    print("")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8005,
        log_level="info"
    ) 