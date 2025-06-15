# systemPatterns.md

## Kiến trúc tổng thể
- Ứng dụng desktop PySide6 chia thành các module: UI, AI, Image, TTS, Video, Project, Core.
- Tích hợp đa API providers với fallback system.
- Bộ dựng video nội bộ dùng FFmpeg với effects presets.
- API Manager quản lý tất cả providers và keys.

## API Providers được hỗ trợ

### AI Content Generation
- **OpenAI GPT-4**: Primary content generation
- **Claude (Anthropic)**: Alternative content generation  
- **DeepSeek**: Cost-effective content generation
- **Auto fallback**: Thử theo thứ tự khi provider chính lỗi

### Image Generation
- **DALL-E (OpenAI)**: Sử dụng chung OpenAI API key
- **Midjourney**: Via API integration
- **Stable Diffusion**: Via Stability AI API
- **Manual Upload**: Cho phép tải ảnh thủ công

### Text-to-Speech
- **Google TTS**: Free tier, không cần API key
- **ElevenLabs**: Premium quality voices
- **Azure Speech**: Microsoft cognitive services
- **Auto fallback**: Google TTS → ElevenLabs → Azure

## Pattern chính
- **Modular**: Mỗi chức năng là module riêng biệt
- **Pipeline**: Prompt → Script → Image → TTS → Video → Export
- **File-based**: Mỗi đoạn nội dung lưu thành file riêng
- **Provider Pattern**: Abstraction layer cho multiple APIs
- **Fallback System**: Auto switch khi API không khả dụng
- **Configuration Management**: Centralized API key management

## Mối quan hệ thành phần
- **UI** ↔ **APIManager**: Quản lý providers và keys
- **APIManager** ↔ **AI/Image/TTS modules**: Cung cấp API keys
- **UI** → **Pipeline**: Orchestrate video generation
- **Pipeline** → **AI/Image/TTS/Video**: Execute generation steps
- **Project Manager**: Lưu trạng thái, metadata, settings

## Error Handling & Resilience
- API key validation trước khi sử dụng
- Graceful fallback khi provider không khả dụng
- User-friendly error messages
- Retry logic với exponential backoff
- Offline mode cho manual image selection 