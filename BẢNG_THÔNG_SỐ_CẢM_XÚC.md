# 🎭 BẢNG THÔNG SỐ CẢM XÚC - VOICE STUDIO

## 📋 **Tổng Quan**

Voice Studio hiện có **hệ thống quản lý cảm xúc hoàn chỉnh** với 21+ cảm xúc có thể điều chỉnh và lưu cấu hình. Đây là bảng thông số chi tiết cho từng cảm xúc.

---

## 🎛️ **BẢNG THÔNG SỐ CẢM XÚC**

### **📊 Thông Số Chính**
- **Exaggeration**: 0.0-2.5 (Cường độ cảm xúc)
- **CFG Weight**: 0.0-1.0 (Độ mạnh điều khiển giọng)
- **Temperature**: 0.1-1.5 (Tính sáng tạo/biến đổi)
- **Speed**: 0.5-2.0 (Tốc độ nói)

---

## 🏷️ **NEUTRAL EMOTIONS (Cảm Xúc Trung Tính)**

| Cảm Xúc | Exaggeration | CFG Weight | Temperature | Speed | Mô Tả | Sử Dụng |
|----------|-------------|------------|-------------|-------|-------|---------|
| `neutral` | 0.50 | 0.50 | 0.70 | 1.00 | Kể chuyện khách quan, cân bằng | Narration |
| `calm` | 0.50 | 0.50 | 0.50 | 0.90 | Bình tĩnh, điềm đạm | General |
| `contemplative` | 0.40 | 0.40 | 0.60 | 0.80 | Suy tư sâu sắc, trầm ngâm | Narration |

---

## 💚 **POSITIVE EMOTIONS (Cảm Xúc Tích Cực)**

| Cảm Xúc | Exaggeration | CFG Weight | Temperature | Speed | Mô Tả | Sử Dụng |
|----------|-------------|------------|-------------|-------|-------|---------|
| `happy` | 1.35 | 0.55 | 0.80 | 1.10 | Vui vẻ, tích cực chung | Dialogue |
| `excited` | 1.60 | 0.60 | 0.90 | 1.30 | Phấn khích, năng lượng cao | Character |
| `friendly` | 1.20 | 0.50 | 0.80 | 1.00 | Thân thiện, chào đón | General |
| `gentle` | 0.35 | 0.35 | 0.60 | 0.90 | Dịu dàng, nhẹ nhàng | Character |
| `confident` | 1.50 | 0.60 | 0.80 | 1.00 | Tự tin, quyết đoán | Character |
| `persuasive` | 1.35 | 0.55 | 0.80 | 1.00 | Thuyết phục, lôi cuốn | Dialogue |

---

## ❤️ **NEGATIVE EMOTIONS (Cảm Xúc Tiêu Cực)**

| Cảm Xúc | Exaggeration | CFG Weight | Temperature | Speed | Mô Tả | Sử Dụng |
|----------|-------------|------------|-------------|-------|-------|---------|
| `sad` | 0.40 | 0.35 | 0.60 | 0.80 | Buồn bã chung | Character |
| `angry` | 2.00 | 0.70 | 0.90 | 1.20 | Tức giận, mạnh mẽ | Character |
| `sarcastic` | 0.85 | 0.45 | 0.80 | 1.10 | Mỉa mai, châm biếm | Dialogue |

---

## 🎭 **DRAMATIC EMOTIONS (Cảm Xúc Kịch Tính)**

| Cảm Xúc | Exaggeration | CFG Weight | Temperature | Speed | Mô Tả | Sử Dụng |
|----------|-------------|------------|-------------|-------|-------|---------|
| `dramatic` | 1.80 | 0.60 | 1.00 | 1.00 | Kịch tính, ấn tượng | Character |
| `mysterious` | 1.40 | 0.45 | 0.70 | 0.90 | Bí ẩn, huyền bí | Narration |
| `determined` | 1.70 | 0.65 | 0.80 | 1.10 | Quyết tâm, mạnh mẽ | Character |

---

## ✨ **SPECIAL EMOTIONS (Cảm Xúc Đặc Biệt)**

| Cảm Xúc | Exaggeration | CFG Weight | Temperature | Speed | Mô Tả | Sử Dụng |
|----------|-------------|------------|-------------|-------|-------|---------|
| `whisper` | 0.30 | 0.30 | 0.40 | 0.70 | Thì thầm, bí mật | Character |
| `innocent` | 1.20 | 0.50 | 0.70 | 1.00 | Ngây thơ, trẻ con | Character |
| `cold` | 0.35 | 0.65 | 0.50 | 1.00 | Lạnh lùng, xa cách | Character |

---

## 🔧 **CÁCH SỬ DỤNG VÀ ĐIỀU CHỈNH**

### **1. 📱 Giao Diện Điều Chỉnh**
```python
# Mở Emotion Configuration Tab
emotion_tab = EmotionConfigTab()

# Điều chỉnh parameters trực tiếp
emotion_manager.modify_emotion(
    "happy",
    exaggeration=1.8,    # Tăng cường độ cảm xúc
    speed=1.2,           # Tăng tốc độ nói
    temperature=0.9      # Tăng tính biến đổi
)
```

### **2. 💾 Lưu Cấu Hình Tùy Chỉnh**
```python
# Tạo emotion mới
emotion_manager.create_custom_emotion(
    name="epic_hero",
    exaggeration=2.2,
    cfg_weight=0.8,
    temperature=1.1,
    speed=1.3,
    description="Anh hùng sử thi",
    category="dramatic"
)

# Lưu tất cả thay đổi
emotion_manager.save_custom_emotions()
```

### **3. 📋 Tạo Emotion Presets**
```python
# Preset cho kể chuyện
audiobook_preset = emotion_manager.create_emotion_preset(
    preset_name="audiobook_narration",
    emotions=["neutral", "contemplative", "gentle", "dramatic", "mysterious"],
    description="Tối ưu cho audiobook"
)

# Preset cho nhân vật
character_preset = emotion_manager.create_emotion_preset(
    preset_name="character_dialogue", 
    emotions=["happy", "excited", "angry", "sad", "confident"],
    description="Tối ưu cho dialogue nhân vật"
)
```

---

## 🎬 **CÁC SCENARIO SỬ DỤNG**

### **📚 Audiobook/Narration**
```python
best_emotions = ["neutral", "contemplative", "gentle", "dramatic", "mysterious"]
# → Phù hợp cho kể chuyện, có chiều sâu cảm xúc
```

### **🎭 Character Dialogue**
```python
hero_emotions = ["confident", "friendly", "determined"]
villain_emotions = ["angry", "sarcastic", "cold"] 
child_emotions = ["excited", "happy", "innocent"]
# → Phân biệt rõ ràng từng loại nhân vật
```

### **📺 Commercial/Advertisement**
```python
commercial_emotions = ["friendly", "excited", "persuasive", "confident"]
# → Tạo sức hút và thuyết phục khách hàng
```

---

## 📊 **THỐNG KÊ HỆ THỐNG**

```
📈 EMOTION STATISTICS:
   • Tổng số cảm xúc: 21+
   • Default emotions: 18
   • Custom emotions: Không giới hạn
   • Emotion presets: Không giới hạn

📂 PHÂN LOẠI:
   • Neutral: 4 cảm xúc  
   • Positive: 6 cảm xúc
   • Negative: 3 cảm xúc
   • Dramatic: 4 cảm xúc  
   • Special: 4 cảm xúc

🎵 VOICE TONE:
   • Soft: 7 cảm xúc
   • Balanced: 8 cảm xúc
   • Strong: 3 cảm xúc
   • Intense: 3 cảm xúc
```

---

## 🚀 **TÍNH NĂNG NÂNG CAO**

### **✨ Live Parameter Adjustment**
- Điều chỉnh real-time bằng sliders
- Preview emotion effects
- Auto-save configurations

### **🎛️ Advanced Controls**
- Voice tone mapping
- Use case optimization  
- Category-based filtering
- Custom parameter ranges

### **💾 Import/Export**
- Export toàn bộ config thành JSON
- Import presets từ community
- Backup/restore settings
- Version control

### **📊 Analytics & Monitoring**
- Emotion usage statistics
- Performance metrics
- Quality assessments
- User behavior tracking

---

## 🔄 **WORKFLOW INTEGRATION**

### **1. Script Processing**
```python
# Auto-detect emotion từ text
detected_emotion = analyze_text_emotion(dialogue_text)

# Apply emotion parameters
emotion_params = emotion_manager.get_emotion_parameters(detected_emotion)

# Generate voice với emotion
result = voice_generator.generate_voice(
    text=dialogue_text,
    emotion=detected_emotion,
    **emotion_params
)
```

### **2. Character-Specific Settings**
```python
# Per-character emotion mapping
character_emotions = {
    "narrator": ["neutral", "contemplative", "mysterious"],
    "hero": ["confident", "determined", "friendly"], 
    "villain": ["angry", "cold", "sarcastic"],
    "child": ["excited", "happy", "innocent"]
}

# Auto-apply based on character
for character, emotions in character_emotions.items():
    character_voice_config[character]["available_emotions"] = emotions
```

---

## 💡 **BEST PRACTICES**

### **🎯 Emotion Selection**
1. **Narration**: Dùng neutral, contemplative, gentle
2. **Action scenes**: Dùng dramatic, determined, excited  
3. **Emotional scenes**: Dùng sad, happy, angry theo context
4. **Mystery/Thriller**: Dùng mysterious, cold, whisper

### **⚙️ Parameter Tuning**
1. **Low Exaggeration (0.3-0.6)**: Tinh tế, tự nhiên
2. **Medium Exaggeration (0.8-1.5)**: Biểu cảm rõ ràng
3. **High Exaggeration (1.8-2.5)**: Kịch tính, mạnh mẽ

### **🎵 Voice Tone Matching**
1. **Soft tones**: Female characters, children, gentle scenes
2. **Strong/Intense tones**: Action heroes, villains, dramatic moments
3. **Balanced tones**: Narrators, general dialogue

---

## 🎉 **KẾT LUẬN**

Hệ thống **Emotion Configuration Manager** của Voice Studio cung cấp:

✅ **21+ cảm xúc predefined** với parameters tối ưu  
✅ **Unlimited custom emotions** có thể tạo và điều chỉnh  
✅ **Emotion presets** cho các use cases khác nhau  
✅ **Real-time adjustment** với UI trực quan  
✅ **Export/Import** để chia sẻ configurations  
✅ **Advanced analytics** để theo dõi hiệu suất  

**→ Tạo ra giọng đọc có cảm xúc phong phú và tự nhiên cho mọi dự án!** 🎭✨ 