from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Voice Studio API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class EmotionCfg(BaseModel):
    exaggeration: float = 1.0
    cfg: float = 0.5
    temperature: float = 0.8
    speed: float = 1.0

class TtsRequest(BaseModel):
    text: str
    emotion: EmotionCfg

@app.post("/tts/generate", response_class=None)
async def generate_tts(req: TtsRequest):
    """Stub endpoint – returns 501 Not Implemented. Replace with real generation (RealChatterboxProvider)."""
    raise HTTPException(status_code=501, detail="TTS generation not implemented yet") 