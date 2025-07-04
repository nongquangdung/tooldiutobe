import sys
from pathlib import Path

# --- Ensure project root is on PYTHONPATH ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from uuid import uuid4
import os

from src.tts.enhanced_voice_generator import (
    EnhancedVoiceGenerator,
    VoiceGenerationRequest,
)
from .emotion_api import router as emotion_router
from .voice_api import router as voice_router


app = FastAPI(title="Voice Studio API", version="0.2.0")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request Schema matching Chatterbox-Server (OpenAI style) ---
class AudioSpeechRequest(BaseModel):
    input: str
    exaggeration: float = 1.0
    cfg_weight: float = 0.5
    temperature: float = 0.8
    speed: float = 1.0
    voice_id: str | None = None
    emotion: str | None = None
    inner: bool = False


# --- Generator instance ---
generator = EnhancedVoiceGenerator()


@app.post("/v1/audio/speech", response_class=StreamingResponse)
async def generate_audio(req: AudioSpeechRequest):
    """Generate TTS audio via EnhancedVoiceGenerator and stream back as WAV."""

    # Load emotion params if provided
    from .emotion_api import _load_emotions

    emotion_params = {}
    if req.emotion:
        emotions_dict = _load_emotions()
        if req.emotion in emotions_dict:
            emo_cfg = emotions_dict[req.emotion]
            emotion_params = {
                "exaggeration": emo_cfg.get("exaggeration", req.exaggeration),
                "cfg_weight": emo_cfg.get("cfg_weight", req.cfg_weight),
                "temperature": emo_cfg.get("temperature", req.temperature),
                "speed": emo_cfg.get("speed", req.speed),
            }
        else:
            emotion_params = {}

    # Whisper detection
    voice_id = req.voice_id or "alice"
    if req.emotion and req.emotion.lower() == "whisper":
        voice_id = "whisper-female" if "female" in voice_id else "whisper-male"

    voice_request = VoiceGenerationRequest(
        text=req.input,
        character_id="narrator",
        voice_id=voice_id,
        emotion=req.emotion or "neutral",
        speed=emotion_params.get("speed", req.speed),
        temperature=emotion_params.get("temperature", req.temperature),
        exaggeration=emotion_params.get("exaggeration", req.exaggeration),
        cfg_weight=emotion_params.get("cfg_weight", req.cfg_weight),
    )

    result = generator.generate_voice(voice_request)

    if not result.success or not os.path.exists(result.output_path):
        raise HTTPException(status_code=500, detail=result.error_message or "Voice generation failed")

    def iterfile():
        with open(result.output_path, "rb") as f:
            yield from f

    filename = os.path.basename(result.output_path)
    return StreamingResponse(
        iterfile(),
        media_type="audio/wav",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"} 

app.include_router(emotion_router)
app.include_router(voice_router) 