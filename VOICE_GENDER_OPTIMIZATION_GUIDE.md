# VOICE GENDER OPTIMIZATION GUIDE

## 🎭 Hệ thống AI Gender Analysis & Voice Optimization

### 📋 Tổng quan
Hệ thống AI Gender Analysis được tích hợp vào Manual Voice Setup Dialog để:
- **Tự động phân tích giới tính** từ text sample (max 300 ký tự)
- **Gợi ý voice phù hợp** cho từng nhân vật
- **Tối ưu thông số voice** theo giới tính (emotion, speed, cfg_weight)
- **Quick Apply** kết quả cho toàn bộ characters

---

## 🎚️ Thông số Voice có thể điều chỉnh cho Giới tính

### 👩 **Female Voice Optimization**
```json
{
  "emotion_exaggeration": 1.2,
  "speed": 0.95,
  "cfg_weight": 0.6,
  "suggested_voices": ["vi-VN-Wavenet-A", "vi-VN-Wavenet-C"],
  "description": "Nhẹ nhàng, dịu dàng, biểu cảm phong phú"
}
```

**Giải thích:**
- `emotion_exaggeration: 1.2` - Tăng biểu cảm 20% (nhẹ nhàng hơn)
- `speed: 0.95` - Chậm hơn 5% (tạo cảm giác dịu dàng)
- `cfg_weight: 0.6` - Guidance weight cao hơn (voice quality tốt hơn)

### 👨 **Male Voice Optimization**
```json
{
  "emotion_exaggeration": 0.8,
  "speed": 1.05,
  "cfg_weight": 0.4,
  "suggested_voices": ["vi-VN-Wavenet-B", "vi-VN-Wavenet-D"],
  "description": "Mạnh mẽ, rõ ràng, ít biểu cảm"
}
```

**Giải thích:**
- `emotion_exaggeration: 0.8` - Giảm biểu cảm 20% (mạnh mẽ hơn)
- `speed: 1.05` - Nhanh hơn 5% (tạo cảm giác quyết đoán)
- `cfg_weight: 0.4` - Guidance weight thấp hơn (tự nhiên hơn)

### 🗣️ **Neutral Voice Optimization**
```json
{
  "emotion_exaggeration": 1.0,
  "speed": 1.0,
  "cfg_weight": 0.5,
  "suggested_voices": ["vi-VN-Standard-C", "vi-VN-Standard-A"],
  "description": "Cân bằng, tự nhiên, phù hợp mọi context"
}
```

**Giải thích:**
- `emotion_exaggeration: 1.0` - Mức biểu cảm chuẩn
- `speed: 1.0` - Tốc độ bình thường
- `cfg_weight: 0.5` - Cân bằng giữa quality và naturalness

---

## 📝 Text Sample Templates (max 300 chars)

### Fairy Tale / Truyện cổ tích:
```
"Ngày xưa có một cô bé tên Anna, cô ấy sống với anh trai Peter trong một ngôi nhà nhỏ. Anna rất thích đọc sách còn Peter thì thích chơi bóng."
```

### Family Story / Chuyện gia đình:
```
"Mẹ Maria đang nấu ăn trong bếp, bố John đi làm về. Con gái Emma và con trai Tommy đang chơi ngoài sân."
```

### Professional Setting / Môi trường công việc:
```
"Chị Sarah là giám đốc công ty, anh David là trưởng phòng kế toán. Họ đang họp với bà Linh về dự án mới."
```

### Generic Characters / Nhân vật chung:
```
"Một người phụ nữ đang đi bộ trên đường, cô ấy gặp một người đàn ông đang đứng chờ xe bus."
```

---

## 🤖 AI Gender Detection Patterns

### Vietnamese Language Patterns:
1. **Title-based detection:**
   - Female: `cô`, `chị`, `bà`, `mẹ`, `con gái`, `công chúa`, `nữ hoàng`, `cô bé`
   - Male: `anh`, `chú`, `ông`, `bố`, `con trai`, `hoàng tử`, `nhà vua`, `cậu bé`

2. **Pronoun-based detection:**
   - Female: `cô ấy`, `chị ấy`, `bà ấy`
   - Male: `anh ấy`, `chú ấy`, `ông ấy`

3. **Name ending patterns:**
   - Female tendency: `a`, `i`, `y`, `nh` (Anna, Linh, Jenny)
   - Male tendency: `ng`, `n`, `c`, `t` (Dung, An, Duc, Dat)

### Confidence Scoring:
- **80-95%** 🟢 High confidence (name + context match)
- **60-79%** 🟡 Medium confidence (partial indicators)
- **<60%** 🔴 Low confidence (ambiguous)

---

## 🚀 Cách sử dụng trong UI

### Bước 1: Mở AI Analysis Panel
- Mở Manual Voice Setup Dialog
- Tìm panel "🤖 AI Gender Analysis & Voice Optimization" (màu tím)

### Bước 2: Nhập Text Sample
- Paste text từ script hoặc prompt vào text box
- Maximum 300 ký tự (tự động cắt nếu dài hơn)
- Sử dụng placeholder examples làm tham khảo

### Bước 3: Phân tích AI
- Click "🔍 Phân tích giới tính"
- AI sẽ analyze và hiển thị:
  - Character names detected
  - Gender confidence (%)
  - Suggested voice
  - Recommended emotion & speed settings

### Bước 4: Apply Results
Choose một trong các options:

#### 🎯 Tự động gán giọng:
- Apply toàn bộ AI suggestions cho all enabled characters
- Tự động set name, gender, voice, emotion, speed

#### 👩 Tối ưu giọng nữ:
- Apply female optimization cho characters có gender = "Nữ"
- emotion: 1.2, speed: 0.95

#### 👨 Tối ưu giọng nam:
- Apply male optimization cho characters có gender = "Nam"  
- emotion: 0.8, speed: 1.05

#### 🗣️ Tối ưu giọng trung tính:
- Apply neutral settings cho tất cả characters
- emotion: 1.0, speed: 1.0

---

## 🎛️ Advanced Parameter Tuning

### Chatterbox TTS Parameters:
```python
def generate_voice(
    text: str,
    voice_sample_path: Optional[str] = None,
    emotion_exaggeration: float = 1.0,  # 0.0-2.0
    speed: float = 1.0,                 # 0.5-2.0
    cfg_weight: float = 0.5             # 0.0-1.0
):
```

### Emotion Exaggeration Range:
- **0.0-0.5**: Monotone, robotic (good for narrator)
- **0.6-0.9**: Subtle emotions (good for male voices)
- **1.0**: Default emotional range
- **1.1-1.5**: Enhanced emotions (good for female voices)
- **1.6-2.0**: Very expressive (good for children, cartoon)

### Speed Range:
- **0.5-0.8**: Very slow (meditation, audiobook)
- **0.8-0.95**: Slightly slow (female gentle voices)
- **1.0**: Normal speed
- **1.05-1.2**: Slightly fast (male confident voices)
- **1.3-2.0**: Very fast (energetic, urgent)

### CFG Weight Impact:
- **0.0-0.3**: Very natural, may lose some quality
- **0.4-0.6**: Balanced quality & naturalness
- **0.7-1.0**: High quality, may sound less natural

---

## 📊 Testing & Validation

### Test Script Usage:
```bash
python test_gender_analysis_demo.py
```

### Expected Output:
```
🤖 GENDER ANALYSIS DEMO
============================================================

📝 Test Case 1: Fairy Tale Vietnamese
📄 Text: Ngày xưa có một cô bé tên Anna, cô ấy sống với anh trai Peter...
🎯 Analysis Results:
   👩 Anna: Female (85%)
      🎵 Voice: vi-VN-Wavenet-A (Nữ)
      🎭 Emotion: 1.2 | ⚡ Speed: 0.95
   👨 Peter: Male (82%)
      🎵 Voice: vi-VN-Wavenet-B (Nam)
      🎭 Emotion: 0.8 | ⚡ Speed: 1.05
```

---

## 💡 Best Practices

### Text Sample Guidelines:
1. **Include character names** explicitly ("cô Anna", "anh Peter")
2. **Use Vietnamese titles** for better detection
3. **Provide context** about character interactions
4. **Keep under 300 chars** for optimal processing

### Voice Selection Strategy:
1. **Wavenet voices** for higher quality (if available)
2. **Standard voices** for backup/cost efficiency
3. **Match gender** with voice recommendation
4. **Test preview** before final generation

### Parameter Optimization:
1. **Start with AI suggestions** as baseline
2. **Fine-tune based on content type**:
   - Documentary: Lower emotion, normal speed
   - Children story: Higher emotion, varied speed
   - Professional: Balanced settings
3. **Consider voice cloning** for consistent character voices

---

## 🔧 Integration với Video Pipeline

### Saved Configuration:
- AI analysis results được save trong `configs/voice_mapping.json`
- Auto-load khi mở lại dialog
- Export/import settings between projects

### Script Integration:
- AI analysis có thể apply trực tiếp cho script characters
- Consistency check across multiple segments
- Batch processing cho large scripts

### Quality Assurance:
- Preview individual character voices
- Test full script with selected settings
- Export audio samples for review

---

## ⚠️ Limitations & Considerations

### Current Limitations:
- Vietnamese language focus (English patterns in development)
- Text-based analysis only (no audio input analysis)
- Max 300 characters per analysis session
- Requires manual review for ambiguous cases

### Accuracy Expectations:
- **High accuracy** (80%+) for clear Vietnamese patterns
- **Medium accuracy** (60-79%) for mixed/ambiguous text
- **Manual override** always available for corrections

### Performance Notes:
- Real-time analysis (< 1 second processing)
- No network calls (all local processing)
- Memory efficient pattern matching
- UI responsive during analysis

---

*Generated by AI Video Generator - Voice Gender Optimization System* 