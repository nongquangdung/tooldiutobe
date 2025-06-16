# activeContext.md

## Trạng thái hiện tại - MAJOR UPDATE: Advanced TTS Integration
- ✅ Đã hoàn thành toàn bộ implementation theo SPEC-001
- ✅ Tất cả module core đã được tạo và tích hợp
- ✅ Giao diện nâng cao với đầy đủ tính năng
- ✅ Pipeline hoàn chỉnh từ prompt → video
- ✅ **Giao diện đã được tối ưu hoàn toàn cho MacOS 13 inch**
- 🆕 **CHATTERBOX TTS INTEGRATION**: Advanced AI TTS với device auto-detection

## Mới nhất: Chatterbox TTS Integration (2025-06-16)
### 🤖 Features được thêm:
- **ChatterboxTTSProvider**: Provider mới với SoTA zero-shot TTS
- **Device Auto-Detection**: CUDA (GTX 1080) → Apple MPS (M2) → CPU fallback  
- **Emotion Control**: Slider điều chỉnh emotion exaggeration (0.0-2.0)
- **Voice Cloning**: Upload audio samples để clone giọng nói
- **Memory Management**: GPU/CPU memory tracking và cleanup
- **Provider Selection**: Auto-select provider dựa trên ngôn ngữ và hardware

### 🛠️ Technical Implementation:
```python
# Auto device detection logic
if torch.cuda.is_available():
    device = "cuda:0"  # GTX 1080
elif torch.backends.mps.is_available():
    device = "mps"     # Apple M2
else:
    device = "cpu"     # Fallback
```

### 🎯 Provider Logic:
- **Vietnamese text** → Google Cloud TTS (ưu tiên) → Google Free TTS
- **English text** → Chatterbox TTS (nếu có) → ElevenLabs → Google Free TTS
- **Language Auto-detect**: Dựa trên Vietnamese characters

### 📱 UI Integration:
- **Settings Tab**: Device info button + cache clear button
- **Device Info Dialog**: Chi tiết GPU/CPU/memory usage  
- **Real-time Status**: Provider availability tracking
- **Memory Monitoring**: GPU allocated/cached memory display

## Thay đổi gần đây (MacOS Optimization)
- **Responsive Design**: Tối ưu kích thước cửa sổ cho MacBook 13" (1200x800, min 1000x700)
- **MacOS Native Styling**: Áp dụng design system của Apple với màu sắc, font, và spacing chuẩn
- **Scroll Areas**: Thêm scroll cho tất cả nội dung dài, tránh tràn màn hình
- **Group Layout**: Tổ chức UI thành các nhóm logic với QGroupBox
- **Compact Layout**: Sử dụng GridLayout thay vì VBoxLayout để tiết kiệm không gian
- **Splitter Interface**: Tab Projects sử dụng splitter 40%-60% cho tối ưu không gian
- **Progress Tracking**: Nhóm riêng cho progress với preview nội dung compact
- **MacOS Stylesheet**: File riêng `macos_styles.py` với stylesheet hoàn chỉn

## Cải tiến UI/UX
- **Tab Icons**: Thêm emoji icons cho các tab (🎬, 📁, ⚙️)
- **Button Icons**: Thêm emoji cho các nút chức năng
- **Compact Controls**: Giảm kích thước các control, tăng mật độ thông tin
- **Native Colors**: Sử dụng màu #007AFF (iOS Blue) làm màu chủ đạo
- **Rounded Corners**: Border radius 8px cho modern look
- **Hover Effects**: Smooth transitions cho tất cả interactive elements
- 🆕 **TTS Controls**: Device monitoring buttons trong Settings tab

## Cấu trúc file mới
```
src/
├── tts/
│   ├── voice_generator.py (enhanced với dual TTS)
│   └── chatterbox_tts_provider.py (mới)
├── ui/
│   ├── advanced_window.py (thêm Chatterbox UI)
│   ├── macos_styles.py
│   └── manual_voice_setup_dialog.py (enhanced)
├── install_chatterbox.py (installation script)
└── requirements.txt (updated)
```

## Technical Status
### ✅ Working Components:
- Google TTS (Free + Cloud): Vietnamese support
- ElevenLabs TTS: English high-quality
- Chatterbox TTS Integration: Framework complete
- Device Auto-Detection: CUDA/MPS/CPU
- Fallback System: Graceful degradation

### ⚠️ Known Issues:
- Chatterbox TTS: Compatibility với Python 3.9 (transformers version conflict)
- Fallback activated: App hoạt động tốt với Google TTS + ElevenLabs
- Future: Upgrade to Python 3.11+ for full Chatterbox support

## Kiến trúc Provider System
```
VoiceGenerator
├── Google TTS (Free) ✅
├── Google Cloud TTS ✅  
├── ElevenLabs TTS ✅
└── Chatterbox TTS ⚠️ (fallback ready)
```

## Test Results
- ✅ **MacOS M2**: MPS detected, PyTorch 2.0.1 installed
- ✅ **App Launch**: Graceful fallback khi Chatterbox unavailable  
- ✅ **UI Integration**: Device buttons hoạt động
- ✅ **Provider Selection**: Auto-detect working
- ✅ **Memory Management**: Safe cleanup implementation

## Bước tiếp theo
### Immediate:
- 🔄 **Test CUDA on PC**: Test với GTX 1080 để verify CUDA detection
- 📝 **Documentation**: Update user guide với TTS options
- 🧪 **Voice Cloning Test**: Test voice cloning workflow khi Chatterbox available

### Future Enhancement:
- 🐍 **Python 3.11+ Migration**: For full Chatterbox TTS support
- 🎭 **Emotion Presets**: UI presets cho các emotion levels
- 🎵 **Batch Voice Cloning**: Multiple voice samples support
- 🔄 **Real-time TTS**: Live preview of voice generation
- 📊 **Performance Monitoring**: TTS generation speed metrics 