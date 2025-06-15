# AI Video Generator

Công cụ tạo video tự động bằng AI từ prompt - tích hợp sinh kịch bản, tạo ảnh, chuyển văn bản thành giọng nói và dựng video hoàn chỉnh.

## Tính năng

- ✅ Sinh kịch bản từ prompt bằng AI (OpenAI GPT-4)
- ✅ Tạo ảnh AI cho từng đoạn (DALL-E)
- ✅ Chuyển văn bản thành giọng nói (Google TTS/ElevenLabs)
- ✅ Dựng video với hiệu ứng zoom, chuyển cảnh (FFmpeg)
- ✅ Giao diện desktop với tabs: tạo video, quản lý project, cài đặt
- ✅ Lưu/tải project, quản lý file tự động
- ✅ Progress tracking và xử lý lỗi

## Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.10+
- FFmpeg (cài đặt local)

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cài đặt FFmpeg
**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Tải từ https://ffmpeg.org/download.html
- Thêm vào PATH

**Linux:**
```bash
sudo apt install ffmpeg
```

### 4. Cấu hình API Keys
1. Copy `config.env.example` thành `config.env`
2. Điền API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_TTS_API_KEY=your_google_tts_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

## Sử dụng

### Chạy ứng dụng
```bash
python src/main.py
```

### Tạo video
1. Mở tab "Tạo Video"
2. Nhập prompt mô tả nội dung video
3. Đặt tên project
4. Chọn hiệu ứng (zoom, chuyển cảnh)
5. Bấm "Tạo video"
6. Đợi quá trình hoàn thành (có progress bar)

### Quản lý projects
1. Mở tab "Projects"
2. Xem danh sách projects đã tạo
3. Click vào project để xem chi tiết
4. Mở thư mục hoặc xóa project

### Cài đặt
1. Mở tab "Cài đặt"
2. Nhập API keys
3. Chọn độ phân giải, FPS
4. Lưu cài đặt

## Cấu trúc thư mục

```
src/
├── ai/                 # Module AI sinh nội dung
├── image/              # Module tạo ảnh AI
├── tts/                # Module chuyển văn bản thành giọng nói
├── video/              # Module dựng video FFmpeg
├── project/            # Module quản lý project
├── core/               # Pipeline tích hợp tất cả
├── ui/                 # Giao diện PySide6
└── main.py             # Entry point

projects/               # Thư mục lưu projects
├── project_name_timestamp/
│   ├── images/         # Ảnh AI đã tạo
│   ├── audio/          # File giọng nói
│   ├── segments/       # Video từng đoạn
│   ├── videos/         # Video hoàn chỉnh
│   └── project.json    # Metadata project
```

## API Keys được hỗ trợ

### 📝 AI Sinh nội dung
- **OpenAI GPT-4**: Sinh kịch bản và prompt ảnh
  - Lấy tại: https://platform.openai.com/api-keys
- **Claude (Anthropic)**: Alternative AI content generation
  - Lấy tại: https://console.anthropic.com/
- **DeepSeek**: Cost-effective AI từ DeepSeek
  - Lấy tại: https://platform.deepseek.com/

### 🎨 AI Tạo ảnh
- **DALL-E (OpenAI)**: Sử dụng chung OpenAI API key
- **Midjourney**: Tạo ảnh qua API
  - Lấy tại: https://docs.midjourney.com/
- **Stable Diffusion**: Via Stability AI
  - Lấy tại: https://platform.stability.ai/

### 🎤 Text-to-Speech
- **Google TTS**: Miễn phí, không cần API key
- **ElevenLabs**: Giọng nói chất lượng cao
  - Lấy tại: https://elevenlabs.io/
- **Azure Speech**: Microsoft cognitive services
  - Lấy tại: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/

> **Lưu ý**: Ứng dụng có hệ thống fallback tự động. Chỉ cần cấu hình ít nhất 1 API cho mỗi loại service.

## Troubleshooting

### Lỗi "command not found: pip"
```bash
# macOS/Linux
python3 -m ensurepip --upgrade
python3 -m pip install -r requirements.txt
python3 src/main.py
```

### Lỗi FFmpeg
- Đảm bảo FFmpeg đã được cài đặt và thêm vào PATH
- Test: `ffmpeg -version`

### Lỗi API
- Kiểm tra API keys trong `config.env`
- Đảm bảo có credit trong tài khoản API

## Phát triển

### Thêm tính năng mới
1. Tạo module trong thư mục tương ứng
2. Import vào `core/video_pipeline.py`
3. Cập nhật UI nếu cần

### Test
```bash
# Test từng module
python -m src.ai.content_generator
python -m src.image.image_generator
python -m src.tts.voice_generator
```

## License

MIT License - xem file LICENSE để biết chi tiết. 