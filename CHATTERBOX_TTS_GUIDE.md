# 🤖 Chatterbox TTS Integration Guide

## Tổng quan
AI Video Generator hiện đã tích hợp **Chatterbox TTS** - một AI TTS state-of-the-art với khả năng:
- 🎯 **Zero-shot voice cloning** từ audio samples
- 🎭 **Emotion control** với fine-tuning
- 🚀 **Device auto-detection**: CUDA/MPS/CPU
- 🌟 **SoTA quality** outperform ElevenLabs theo benchmark

## 📱 Hardware Support

### 🎯 NVIDIA GPU (GTX 1080, RTX series)
```
✅ CUDA acceleration
⚡ Fastest generation speed
💾 Requires 4GB+ VRAM
🔧 Auto-detected: "CUDA (GeForce GTX 1080)"
```

### 🍎 Apple Silicon (M1, M2, M3)
```
✅ MPS acceleration  
⚡ Fast generation on Metal
💾 Unified memory usage
🔧 Auto-detected: "Apple MPS (M2 chip)"
```

### 💻 CPU Fallback
```
✅ Compatible với mọi system
⚡ Slower nhưng vẫn functional
💾 Uses system RAM
🔧 Auto-detected: "CPU"
```

## 🛠️ Installation

### Tự động (Recommended)
```bash
python3 install_chatterbox.py
```

Script sẽ:
1. 🔍 **Detect hardware** (CUDA/MPS/CPU)
2. 📦 **Install PyTorch** phù hợp cho system
3. 🤖 **Install Chatterbox TTS** từ GitHub
4. 🧪 **Test installation** và report status
5. 🔄 **Install fallback TTS** nếu cần

### Manual Installation
```bash
# For Apple M2
pip3 install torch==2.0.1 torchaudio==2.0.2

# For CUDA GPU
pip3 install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# Install Chatterbox
pip3 install git+https://github.com/resemble-ai/chatterbox.git
```

## 🎮 Sử dụng trong App

### 1. Kiểm tra Device Status
1. 🔧 Mở **Settings tab**
2. 📱 Click **"📱 Kiểm tra Device"** trong TTS section
3. 📊 Xem device info:
   ```
   🤖 Chatterbox TTS Device Information
   
   ✅ Status: Initialized
   📱 Device: Apple MPS (M2 chip)
   🔧 Device Type: mps
   
   🌍 Languages: English
   ✨ Features:
   • SoTA quality
   • Emotion control  
   • Voice cloning
   • Device: Apple MPS (M2 chip)
   
   📊 Current Memory Usage:
   • CPU Memory: 256 MB (2.1%)
   ```

### 2. Provider Selection
TTS providers được auto-select dựa trên:

#### Vietnamese Text
```
1st choice: Google Cloud TTS (nếu có API key)
2nd choice: Google Free TTS
```

#### English Text  
```
1st choice: Chatterbox TTS (nếu available)
2nd choice: ElevenLabs (nếu có API key)
3rd choice: Google Free TTS
```

### 3. Voice Generation Options

#### Basic TTS
```python
# Trong app - tự động detect language và provider
voice_generator.generate_voice_auto_v2(
    text="Hello, this is a test",
    save_path="output.mp3",
    provider="auto",  # auto-select
    language="auto"   # auto-detect
)
```

#### Advanced Chatterbox Features
```python
# Direct Chatterbox với emotion control
voice_generator.generate_voice_chatterbox(
    text="Hello world!",
    save_path="output.mp3",
    emotion_exaggeration=1.5,  # 0.0-2.0
    speed=1.2,                 # 0.5-2.0
    voice_sample_path="clone_voice.wav"  # Optional
)
```

## 🎭 Emotion Control

Chatterbox TTS hỗ trợ emotion exaggeration từ 0.0-2.0:

| Value | Effect | Use Case |
|-------|---------|----------|
| 0.0-0.5 | Neutral, flat | Documentation, formal |
| 0.8-1.0 | Natural | Normal conversation |
| 1.2-1.5 | Expressive | Storytelling, character |
| 1.6-2.0 | Very emotional | Drama, cartoon |

## 🎤 Voice Cloning

### Chuẩn bị Audio Sample
- ✅ **Length**: 3-30 giây
- ✅ **Quality**: Clear, no background noise
- ✅ **Format**: .wav, .mp3, .flac
- ✅ **Content**: Single speaker, natural speech
- ✅ **Language**: English (hiện tại)

### Workflow
1. 📁 Chuẩn bị voice sample file
2. 🎙️ Call API với `voice_sample_path`
3. 🧠 Chatterbox sẽ analyze và clone voice
4. 💾 Voice config được cache để reuse
5. 🎵 Generate TTS với cloned voice

## 🧹 Memory Management

### Monitor Memory Usage
```python
# Get memory stats
memory_info = voice_generator.get_chatterbox_device_info()
print(f"GPU Allocated: {memory_info['gpu_allocated']} MB")
print(f"CPU Memory: {memory_info['cpu_memory_mb']} MB")
```

### Clear Cache
1. 🔧 Settings tab → **"🧹 Xóa Cache"**
2. Hoặc programmatically:
```python
voice_generator.cleanup_chatterbox()
```

## 📊 Provider Status

### Check Available Providers
```python
providers = voice_generator.get_available_tts_providers()
for provider in providers:
    print(f"{provider['name']}: {provider['status']}")
```

### Example Output
```
Google TTS (Free): ✅ Available
Google Cloud TTS: ✅ Available  
ElevenLabs: ✅ Available
Chatterbox TTS: ✅ Available (Apple MPS (M2 chip))
```

## 🐛 Troubleshooting

### Chatterbox Not Available
**Symptoms**: "❌ Chatterbox TTS not available"

**Solutions**:
1. 🐍 **Python Version**: Upgrade to Python 3.11+ (current: 3.9 có compatibility issue)
2. 📦 **Dependencies**: Run `pip3 install --upgrade transformers torch`
3. 💾 **Memory**: Ensure enough RAM/VRAM available
4. 🔧 **Reinstall**: Run `python3 install_chatterbox.py` again

### CUDA Not Detected
**Symptoms**: Fallback to CPU despite having GPU

**Solutions**:
1. 🎯 **CUDA Drivers**: Update NVIDIA drivers
2. 📦 **PyTorch CUDA**: Install CUDA-enabled PyTorch
3. 🔍 **Test**: Run `python3 -c "import torch; print(torch.cuda.is_available())"`

### MPS Not Working (Apple)
**Solutions**:
1. 🍎 **macOS Version**: Requires macOS 12.3+
2. 📦 **PyTorch Version**: Ensure PyTorch 1.12+
3. 🔍 **Test**: Run `python3 -c "import torch; print(torch.backends.mps.is_available())"`

## 🔮 Future Enhancements

### Planned Features
- 🎭 **Emotion Presets**: UI sliders cho emotion control
- 🎵 **Batch Voice Cloning**: Multiple voice samples
- 🌍 **Multi-language**: Expand beyond English
- 🔄 **Real-time Preview**: Live TTS preview
- 📊 **Performance Metrics**: Generation speed tracking

### Integration Points
- Manual Voice Setup Dialog: Add emotion controls
- Video Generation: Include emotion in character mapping
- Project Templates: Save voice + emotion presets

## 📝 Technical Notes

### Architecture
```
VoiceGenerator
├── Google TTS (Free) ✅
├── Google Cloud TTS ✅  
├── ElevenLabs TTS ✅
└── ChatterboxTTSProvider ⚠️
    ├── Device Detection
    ├── Model Loading
    ├── Voice Cloning Cache
    └── Memory Management
```

### Device Detection Logic
```python
if torch.cuda.is_available():
    device = "cuda:0"       # NVIDIA GPU
elif torch.backends.mps.is_available():
    device = "mps"          # Apple Silicon
else:
    device = "cpu"          # Fallback
```

### Fallback Strategy
1. Try Chatterbox TTS
2. If fail → Try ElevenLabs
3. If fail → Use Google TTS
4. Always ensure audio generation succeeds

---

## 🚀 Quick Start

1. **Install**: `python3 install_chatterbox.py`
2. **Launch**: `python3 src/main.py`
3. **Check**: Settings → 📱 Kiểm tra Device
4. **Use**: Create video với auto TTS selection
5. **Monitor**: Settings → 🧹 Xóa Cache khi cần

**Happy voice generating! 🎙️✨** 