# 🎭 **Emotion Auto-Mapping trong Voice Studio**

## 🎯 **TÍNH NĂNG MỚI: TỰ ĐỘNG ĐIỀU CHỈNH CẢM XÚC**

Voice Studio hiện có thể **tự động map emotion labels** từ script JSON thành **emotion exaggeration values** cho Chatterbox TTS, tạo ra giọng đọc tự nhiên và sinh động hơn!

## 🔧 **CÁCH HOẠT ĐỘNG**

### **1. 📝 Input: Emotion Labels trong JSON**
```json
{
  "speaker": "alice",
  "text": "Tôi rất vui mừng!",
  "emotion": "happy"    ← Emotion label từ AI model
}
```

### **2. 🎛️ Mapping: Tự động chuyển đổi**
```
happy → x1.3 multiplier → emotion_exaggeration = 1.3
```

### **3. 🎙️ Output: Giọng đọc có cảm xúc**
Chatterbox TTS sử dụng emotion exaggeration để tạo giọng vui vẻ, tích cực

## 📊 **ENHANCED EMOTION MAPPING TABLE**

**Mỗi emotion label được map thành 2 parameters:**

| Emotion Label | Exaggeration | CFG Weight | Mô tả | Phân loại |
|---------------|-------------|------------|--------|-----------|
| `neutral` | 0.4x | 0.5 | Tự nhiên, giọng kể chuyện | Trung tính |
| **GIỌNG MẠNH MẼ** |||||
| `angry` | 1.2x | 0.35 | Tức giận, mạnh mẽ | Nam tính |
| `threatening` | 1.2x | 0.35 | Đe dọa, hung dữ | Nam tính |
| `confident` | 1.1x | 0.35 | Tự tin, quyết đoán | Nam tính |
| `proud` | 1.1x | 0.35 | Tự hào, kiêu hãnh | Nam tính |
| `dramatic` | 1.3x | 0.35 | Kịch tính, ấn tượng | Nam tính |
| `shout` | 1.3x | 0.30 | Hét to, mạnh mẽ | Nam tính |
| `sarcastic` | 1.0x | 0.35 | Mỉa mai, châm biếm | Nam tính |
| **GIỌNG NHẸ NHÀNG** |||||
| `happy` | 0.7x | 0.45 | Vui vẻ, tích cực | Nữ tính |
| `excited` | 0.8x | 0.45 | Phấn khích, năng động | Nữ tính |
| `friendly` | 0.7x | 0.45 | Thân thiện, gần gũi | Nữ tính |
| `romantic` | 0.7x | 0.45 | Lãng mạn, ngọt ngào | Nữ tính |
| `surprised` | 0.7x | 0.45 | Ngạc nhiên, bất ngờ | Nữ tính |
| `pleading` | 0.8x | 0.45 | Cầu xin, van nài | Nữ tính |
| **GIỌNG ĐẶC BIỆT** |||||
| `sad` | 0.6x | 0.45 | Buồn, trầm lắng | Trung tính |
| `fear` | 0.7x | 0.40 | Sợ hãi, lo lắng | Trung tính |
| `calm` | 0.4x | 0.50 | Bình tĩnh, điềm tĩnh | Trung tính |
| `whisper` | 0.3x | 0.50 | Thì thầm, khẽ khàng | Trung tính |
| `shy` | 0.4x | 0.45 | Nhút nhát, rụt rè | Nữ tính |
| `mysterious` | 0.5x | 0.40 | Bí ẩn, huyền bí | Trung tính |

## 🎛️ **CÁCH SỬ DỤNG**

### **1. Bật Emotion Mapping**
1. Vào tab **🎙️ Voice Studio**
2. Trong phần **"🎛️ Cấu hình Chatterbox TTS chi tiết"**
3. ✅ **Bật checkbox**: **"🎭 Tự động điều chỉnh cảm xúc theo script"**

### **2. Load Script với Emotions**
1. Import file JSON có emotion labels
2. Hoặc sử dụng generated data từ tab Tạo Video
3. Đảm bảo script có emotion fields trong dialogues

### **3. Chọn Chatterbox TTS**
1. **TTS Provider** → **"🤖 Chatterbox TTS"**
2. Chỉ Chatterbox TTS mới hỗ trợ emotion exaggeration

### **4. Generate & Observe**
1. Click **"🎭 Tạo voice cho tất cả nhân vật"**
2. Trong terminal log, bạn sẽ thấy:
```
🎭 Emotion Auto-Mapping: 'happy' → exaggeration=0.70, cfg_weight=0.45
🎭 Emotion Auto-Mapping: 'excited' → exaggeration=0.80, cfg_weight=0.45
🎭 Emotion Auto-Mapping: 'angry' → exaggeration=1.20, cfg_weight=0.35
🎚️ CFG Weight: 0.45
```

## 🔀 **INTERACTION VỚI MANUAL CONTROLS**

### **Khi Manual Controls ENABLED:**
```
Final Value = Base Manual Setting × Emotion Multiplier
```

**Ví dụ:**
- Manual emotion slider: 1.5
- Script emotion: "happy" (x1.3)
- **Final result**: 1.5 × 1.3 = 1.95

### **Khi Manual Controls DISABLED:**
```
Final Value = 1.0 × Emotion Multiplier
```

**Ví dụ:**
- Default: 1.0
- Script emotion: "excited" (x1.8)  
- **Final result**: 1.0 × 1.8 = 1.8

## 🎚️ **VALUE CLAMPING**

Tất cả emotion values được **clamp** vào range **0.0 - 2.0** để:
- ❌ Tránh giọng quá extreme hoặc không tự nhiên
- ✅ Đảm bảo chất lượng audio consistency
- 🎯 Giữ trong range optimal của Chatterbox TTS

## 🚀 **LỢI ÍCH**

### **✅ Tự động hóa**
- KHÔNG cần manually setting emotion cho từng câu
- AI model tự sinh emotion labels → Auto mapping

### **✅ Tự nhiên hơn**
- Mỗi câu thoại có emotion phù hợp
- Không còn giọng đọc đều đều, máy móc

### **✅ Consistency**
- Cùng emotion label → cùng exaggeration value  
- Predictable và consistent behavior

### **✅ Flexibility**
- Có thể tắt mapping để sử dụng manual values
- Combine được với manual controls cho fine-tuning

## 🧪 **TEST FILE DEMO**

File `emotion_mapping_demo.json` chứa:
- 8 emotions khác nhau: `neutral`, `happy`, `excited`, `sad`, `angry`, `surprised`, `calm`, `dramatic`
- 3 nhân vật với Vietnamese voices khác nhau
- Perfect để test và demo emotion mapping functionality

## 🎯 **KẾT QUẢ MONG ĐỢI**

**Trước khi có emotion mapping:**
- Tất cả câu thoại đều có cùng emotion level
- Giọng đọc đều đều, thiếu cảm xúc

**Sau khi có emotion mapping:**
- Câu vui → giọng vui vẻ (higher exaggeration)  
- Câu buồn → giọng trầm lắng (lower exaggeration)
- Câu phấn khích → giọng sôi nổi (much higher exaggeration)
- **→ Tự nhiên và sinh động hơn rất nhiều!** 🎉 