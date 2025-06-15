# techContext.md

## Công nghệ sử dụng
- Desktop app: PySide6 (Python) hoặc Electron (JS/TS)
- AI: OpenAI GPT-4/Claude (script, image prompt, narration), DALL·E/Midjourney/SD/Kling (image), Google TTS/ElevenLabs (voice)
- Video: FFmpeg

## Setup phát triển
- Python 3.10+ hoặc Node.js 18+
- Cài đặt FFmpeg local
- API key cho OpenAI, Google, ElevenLabs, DALL·E...

## Ràng buộc kỹ thuật
- Mỗi đoạn tối đa ~1024 token (giới hạn AI)
- File-based, dễ backup, dễ chỉnh sửa ngoài

## Dependency chính
- PySide6/Electron, openai, requests, ffmpeg-python hoặc fluent-ffmpeg, dotenv 