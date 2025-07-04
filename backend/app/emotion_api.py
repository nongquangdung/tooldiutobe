from __future__ import annotations

"""Emotion API Router
=======================
CRUD + Import/Export cho Emotion Library (Phase 1)
Lưu trữ đơn giản bằng JSON file trên đĩa (backend/configs/emotions/custom_emotions.json).
"""

import json
import uuid
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# --- File paths ---
EMOTION_DIR = Path(__file__).resolve().parents[1] / "configs" / "emotions"
EMOTION_DIR.mkdir(parents=True, exist_ok=True)
EMOTION_FILE = EMOTION_DIR / "custom_emotions.json"

# If first time, create empty file
if not EMOTION_FILE.exists():
    EMOTION_FILE.write_text("{}", encoding="utf-8")

# --- Pydantic Schema ---
class Emotion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    exaggeration: float = Field(..., ge=0.0, le=3.0)
    cfg_weight: float = Field(..., ge=0.1, le=1.0)
    temperature: float = Field(..., ge=0.0, le=2.0)
    speed: float = Field(..., ge=0.5, le=3.0)
    category: str = Field(default="general", description="Phân loại cảm xúc (tùy chọn)")


# --- Helper functions ---

def _load_93_default_emotions():
    """Load 93 default emotions from unified_emotions.json if custom file is empty"""
    unified_emotions_path = Path(__file__).resolve().parents[2] / "configs" / "emotions" / "unified_emotions.json"
    
    if not unified_emotions_path.exists():
        return {}
    
    try:
        with open(unified_emotions_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        emotions_data = config.get("emotions", {})
        # Convert to API format
        converted = {}
        for name, emotion in emotions_data.items():
            converted[name] = {
                "id": emotion.get("id", name),
                "name": emotion.get("name", name),
                "exaggeration": emotion.get("exaggeration", 1.0),
                "cfg_weight": emotion.get("cfg_weight", 0.5),
                "temperature": emotion.get("temperature", 0.8),
                "speed": emotion.get("speed", 1.0),
                "category": emotion.get("category", "general")
            }
        
        return converted
    except Exception as e:
        print(f"Warning: Could not load default emotions: {e}")
        return {}


def _load_emotions() -> Dict[str, Any]:
    """Load emotions file. If file is list, convert to dict keyed by id."""
    with open(EMOTION_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    # If empty, load 93 default emotions
    if not data:
        default_emotions = _load_93_default_emotions()
        if default_emotions:
            _save_emotions(default_emotions)
            return default_emotions

    # Auto unwrap if wrapped by export_info
    if isinstance(data, dict) and "emotions" in data and len(data) == 2 and "export_info" in data:
        data = data["emotions"]

    # If list, convert to dict keyed by id
    if isinstance(data, list):
        converted = {}
        for item in data:
            if isinstance(item, dict):
                emo_id = item.get("id") or str(uuid.uuid4())
                item["id"] = emo_id
                converted[emo_id] = item
        # Save converted format for future
        _save_emotions(converted)
        return converted
    elif isinstance(data, dict):
        return data
    else:
        return {}


def _save_emotions(data: Dict[str, Any]):
    EMOTION_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# --- Router ---
router = APIRouter(prefix="/v1/emotions", tags=["emotions"])


@router.get("/")
async def list_emotions() -> Dict[str, Any]:
    """Trả về toàn bộ emotion library"""
    return _load_emotions()


@router.post("/")
async def create_emotion(emotion: Emotion):
    data = _load_emotions()
    if emotion.id in data:
        raise HTTPException(status_code=400, detail="Emotion ID already exists")
    data[emotion.id] = emotion.dict()
    _save_emotions(data)
    return {"success": True, "id": emotion.id}


@router.put("/{emotion_id}")
async def update_emotion(emotion_id: str, emotion: Emotion):
    data = _load_emotions()

    existing = data.get(emotion_id, {})
    # Preserve existing category if not provided in payload
    updated_fields = emotion.dict(exclude_unset=True, exclude_defaults=True)
    merged = {**existing, **updated_fields}

    merged["id"] = emotion_id  # ensure correct id
    data[emotion_id] = merged
    _save_emotions(data)
    return {"success": True}


@router.delete("/{emotion_id}")
async def delete_emotion(emotion_id: str):
    emotions = _load_emotions()

    # If data wrapped with 'emotions', work inside it
    container = emotions
    if isinstance(emotions, dict) and "emotions" in emotions and len(emotions) > 1:
        container = emotions["emotions"]

    found = False
    # Direct key match
    if emotion_id in container:
        del container[emotion_id]
        found = True
    else:
        # Search by inner 'id' or 'name'
        for key, val in list(container.items()):
            if (
                isinstance(val, dict)
                and (val.get("id") == emotion_id or val.get("name") == emotion_id)
            ):
                del container[key]
                found = True
                break

    if not found:
        raise HTTPException(status_code=404, detail="Emotion not found")

    # Save outer structure if wrapped
    if container is not emotions and "emotions" in emotions:
        emotions["emotions"] = container

    _save_emotions(emotions)
    return {"message": "Deleted"}


@router.delete("/all")
async def delete_all_emotions():
    """Xóa toàn bộ emotion library"""
    _save_emotions({})
    return {"message": "All emotions deleted", "count": 0}


@router.post("/import")
async def import_emotions(file: UploadFile = File(...)):
    try:
        content = await file.read()
        emotions_json = json.loads(content)
        normalized: Dict[str, Any] = {}
        
        if isinstance(emotions_json, dict) and "emotions" in emotions_json:
            emotions_json = emotions_json["emotions"]

        if isinstance(emotions_json, list):
            # Convert list -> dict; ensure ids
            for item in emotions_json:
                if not isinstance(item, dict):
                    continue
                emo_id = item.get("id") or str(uuid.uuid4())
                item["id"] = emo_id
                normalized[emo_id] = item
        elif isinstance(emotions_json, dict):
            # Giữ nguyên category gốc, chỉ set default nếu thiếu
            for key, val in emotions_json.items():
                if isinstance(val, dict):
                    normalized[key] = val
        else:
            raise ValueError("Invalid format")
        
        _save_emotions(normalized)
        return {"success": True, "count": len(normalized)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/export")
async def export_emotions():
    """Xuất file JSON emotions hiện tại"""
    if not EMOTION_FILE.exists():
        raise HTTPException(status_code=404, detail="Emotion file not found")
    return FileResponse(path=EMOTION_FILE, filename="emotion_library.json", media_type="application/json") 