# 🎭 INNER VOICE FEATURE GUIDE

## Tổng Quan

**Inner Voice** (Thoại Nội Tâm) là tính năng mới của Voice Studio cho phép tạo hiệu ứng âm thanh đặc biệt cho những đoạn dialogue thể hiện suy tư, hồi tưởng, hoặc mơ mộng của nhân vật.

## ✨ Tính Năng Chính

### 🎪 3 Loại Inner Voice Effects

#### 1. **Nội Tâm Nhẹ** (`light`)
- **Mô tả**: Tự sự, tâm sự nhẹ nhàng
- **Phù hợp**: Nữ trẻ, nhân vật suy tư, độc thoại ngắn
- **Filter**: `aecho=0.6:0.5:500:0.3`
- **Đặc điểm**: Echo nhẹ nhàng, êm, không chi phối giọng chính

#### 2. **Nội Tâm Sâu** (`deep`)  
- **Mô tả**: Căng thẳng, hồi tưởng, ấn tượng mạnh
- **Phù hợp**: Độc thoại nam, giọng nặng trĩu, nhớ lại quá khứ
- **Filter**: `aecho=0.7:0.6:700|900:0.4|0.3`
- **Đặc điểm**: Vọng dài hơn, nhiều tầng, gợi chiều sâu tâm lý

#### 3. **Nội Tâm Cách Âm** (`dreamy`)
- **Mô tả**: Xa thực tại, mơ hồ, không gian khác biệt
- **Phù hợp**: Cảnh mộng, mất phương hướng, tâm trí rối loạn
- **Filter**: `volume=0.8,aecho=0.5:0.6:800:0.4,lowpass=f=3000`
- **Đặc điểm**: Kết hợp giảm volume + lowpass, như nói trong giấc mơ

## 📋 Cách Sử Dụng

### 1. **Cấu Trúc JSON Cơ Bản**

```json
{
  "segments": [
    {
      "dialogues": [
        {
          "speaker": "alice",
          "text": "Mình có nên làm điều này không nhỉ?",
          "emotion": "contemplative",
          "inner_voice": true,
          "inner_voice_type": "light"
        }
      ]
    }
  ]
}
```

### 2. **Các Field Inner Voice**

| Field | Bắt Buộc | Mô Tả | Giá Trị |
|-------|----------|-------|---------|
| `inner_voice` | ✅ | Bật/tắt inner voice | `true`/`false` |
| `inner_voice_type` | ❌ | Loại effect cụ thể | `light`, `deep`, `dreamy` |

### 3. **Auto-Detection**

Nếu không chỉ định `inner_voice_type`, hệ thống sẽ tự động chọn dựa trên `emotion`:

- **Light**: `contemplative`, `thoughtful`, `hopeful`, `curious`
- **Deep**: `anxious`, `worried`, `determined`, `angry`, `sad`, `commanding`  
- **Dreamy**: `dreamy`, `gentle`, `romantic`, `whisper`, `soft`, `innocent`

## 🎯 Ví Dụ Thực Tế

### Đoạn Dialogue Hoàn Chỉnh

```json
{
  "title": "Nội Tâm Của Alice",
  "characters": [
    {
      "id": "alice",
      "name": "Alice",
      "voice_id": "vi-VN-Standard-C"
    }
  ],
  "segments": [
    {
      "dialogues": [
        {
          "speaker": "alice",
          "text": "Sáng nay Alice ngồi bên cửa sổ.",
          "emotion": "neutral"
        },
        {
          "speaker": "alice", 
          "text": "Mình có nên nhận công việc này không nhỉ?",
          "emotion": "contemplative",
          "inner_voice": true,
          "inner_voice_type": "light"
        },
        {
          "speaker": "alice",
          "text": "Nhớ lại công ty cũ, làm việc từ tối đến sáng...",
          "emotion": "anxious",
          "inner_voice": true,
          "inner_voice_type": "deep" 
        },
        {
          "speaker": "alice",
          "text": "Giá như mình có thể đi du lịch khắp nơi...",
          "emotion": "dreamy",
          "inner_voice": true,
          "inner_voice_type": "dreamy"
        }
      ]
    }
  ]
}
```

## 🔧 Yêu Cầu Kỹ Thuật

### Dependencies

- **FFmpeg**: Bắt buộc để xử lý audio effects
- **Voice Studio**: Version có inner voice support
- **Python 3.8+**: Môi trường runtime

### Cài Đặt FFmpeg

**Windows:**
```bash
# Download từ https://ffmpeg.org/download.html
# Hoặc dùng chocolatey:
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

## 📁 File Output

### Naming Convention

Files với inner voice sẽ có suffix đặc biệt:

- `dialogue_inner_light.mp3` - Nội tâm nhẹ
- `dialogue_inner_deep.mp3` - Nội tâm sâu  
- `dialogue_inner_dreamy.mp3` - Nội tâm cách âm

### File Structure

```
voice_studio_output/
├── s1_d1_alice.mp3                    # 🎤 Voice bình thường
├── s1_d2_alice_inner_light.mp3        # 🎭 Nội tâm nhẹ
├── s1_d3_alice_inner_deep.mp3         # 🎭 Nội tâm sâu
├── s1_d4_alice_inner_dreamy.mp3       # 🎭 Nội tâm cách âm
└── final_complete_audio.mp3           # File ghép hoàn chỉnh
```

## 🎨 Best Practices

### 1. **Khi Nào Dùng Inner Voice**

✅ **Nên dùng:**
- Suy tư, tự vấn của nhân vật
- Hồi tưởng về quá khứ
- Tưởng tượng về tương lai
- Nội tâm đang phân vân
- Cảnh mộng, ảo giác

❌ **Không nên dùng:**
- Dialogue bình thường giữa nhân vật
- Tường thuật trực tiếp
- Hành động cụ thể
- Thông tin quan trọng cần nghe rõ

### 2. **Chọn Loại Effect**

| Tình Huống | Emotion | Type | Ví Dụ |
|------------|---------|------|-------|
| Suy tư nhẹ | `contemplative` | `light` | "Mình nên làm gì đây?" |
| Hồi tưởng đau | `anxious` | `deep` | "Ngày hôm đó..." |
| Tưởng tượng | `dreamy` | `dreamy` | "Giá như mình có thể..." |

### 3. **Tỷ Lệ Sử Dụng**

- **10-30%** dialogues có inner voice - Hợp lý
- **>50%** dialogues có inner voice - Quá nhiều, mất hiệu quả
- **<5%** dialogues có inner voice - Có thể thiếu chiều sâu

## 🧪 Testing & Debug

### Test Commands

```bash
# Test inner voice processor
python src/core/inner_voice_processor.py

# Test với demo JSON
python demo_inner_voice_real_test.py

# Test comprehensive
python test_inner_voice_demo.py
```

### Troubleshooting

**❌ "FFmpeg not available"**
```bash
# Kiểm tra FFmpeg installation
ffmpeg -version

# Cài đặt nếu chưa có
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg  
# Linux: sudo apt install ffmpeg
```

**❌ "Inner voice failed"**
- Kiểm tra input file tồn tại
- Kiểm tra output directory có quyền write
- Kiểm tra FFmpeg command syntax

**❌ "No inner voice applied"**
- Đảm bảo `inner_voice: true` trong JSON
- Kiểm tra InnerVoiceProcessor được khởi tạo
- Xem log để debug

## 📈 Performance

### File Size Impact

Inner voice processing thường:
- **Tăng file size**: 10-50% so với original
- **Chất lượng**: Giữ nguyên quality, chỉ thêm effects
- **Processing time**: Thêm 2-5 giây per file

### Example Comparison

| File | Type | Size | Effect |
|------|------|------|--------|
| original.mp3 | Normal | 15.9 KB | Không |
| inner_light.mp3 | Light | 12.8 KB | Echo nhẹ |
| inner_deep.mp3 | Deep | 23.5 KB | Echo sâu |
| inner_dreamy.mp3 | Dreamy | 20.1 KB | Echo + filter |

## 🚀 Advanced Usage

### Custom Filter Parameters

Có thể tùy chỉnh filter trong code:

```python
from core.inner_voice_processor import InnerVoiceProcessor

processor = InnerVoiceProcessor()

# Custom echo settings
custom_filter = "aecho=0.8:0.7:600:0.4"
processor.echo_presets[InnerVoiceType.LIGHT]["filter"] = custom_filter
```

### Batch Processing

```python
# Process multiple files
for dialogue in dialogues:
    if dialogue.get('inner_voice', False):
        result = processor.process_dialogue_with_inner_voice(
            input_path, dialogue, output_dir
        )
```

## 📞 Support

Nếu gặp vấn đề:

1. **Kiểm tra requirements**: FFmpeg, Python dependencies
2. **Xem logs**: Console output có thông tin debug chi tiết
3. **Test files**: Dùng demo files để verify setup
4. **File report**: Báo cáo với sample JSON và error logs

---

## 🎯 Tóm Tắt

**Inner Voice** là tính năng mạnh mẽ giúp:
- ✅ **Tăng chiều sâu** cho nội dung audio
- ✅ **Phân biệt rõ ràng** dialogue thường vs nội tâm  
- ✅ **3 loại effects** phù hợp mọi tình huống
- ✅ **Tự động hóa** với emotion detection
- ✅ **Production ready** với Voice Studio

🎭 **Chỉ cần thêm `"inner_voice": true` vào JSON là có thể tạo hiệu ứng thoại nội tâm chuyên nghiệp!** 