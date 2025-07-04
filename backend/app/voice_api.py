from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4
import os

# Thư viện quản lý voices có sẵn
from src.tts.chatterbox_voices_integration import ChatterboxVoicesManager

router = APIRouter(prefix="/v1/voices", tags=["voices"])

# Singleton VoicesManager cho toàn bộ app
voices_manager = ChatterboxVoicesManager()

# Đường dẫn thư mục lưu voice mẫu (.wav)
VOICES_DIR: Path = voices_manager.voices_directory


@router.get("/")
async def list_voices():
    """Trả về danh sách tất cả giọng đọc sẵn có (28 giọng mặc định + giọng upload)."""
    voices = voices_manager.get_available_voices()
    return {
        "count": len(voices),
        "voices": [
            {
                "id": vid,
                "name": v.name,
                "gender": v.gender,
                "description": v.description,
            }
            for vid, v in voices.items()
        ],
    }


@router.post("/upload")
async def upload_voice(file: UploadFile = File(...), name: str | None = None):
    """Upload một file .wav và lưu làm giọng đọc tuỳ chỉnh."""
    # Chỉ cho phép WAV
    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ tệp WAV")

    # Xác định tên voice_id
    base_name = name or Path(file.filename).stem
    # Loại bỏ ký tự không hợp lệ
    safe_name = "".join(ch for ch in base_name.lower() if ch.isalnum() or ch in ("_", "-"))
    if not safe_name:
        safe_name = f"custom_{uuid4().hex[:8]}"

    target_path = VOICES_DIR / f"{safe_name}.wav"

    # Tránh ghi đè
    if target_path.exists():
        raise HTTPException(status_code=400, detail="Voice ID đã tồn tại, chọn tên khác")

    # Đảm bảo thư mục tồn tại
    os.makedirs(VOICES_DIR, exist_ok=True)

    # Ghi file
    with open(target_path, "wb") as out_f:
        data = await file.read()
        out_f.write(data)

    # Reload voices cache để nhận giọng mới
    voices_manager.voices_cache.clear()
    voices_manager.setup_predefined_voices()

    return {"success": True, "voice_id": safe_name} 