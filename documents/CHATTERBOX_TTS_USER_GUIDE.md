# 🎭 Hướng dẫn sử dụng Chatterbox TTS trong AI Video Generator

## 📖 Tổng quan
Manual Voice Setup Dialog hiện đã được nâng cấp với **Chatterbox TTS integration** - cho phép bạn tạo giọng đọc AI chất lượng cao với khả năng:

- 🎯 **Voice Cloning**: Clone giọng từ audio samples
- 🎭 **Emotion Control**: Điều chỉnh cảm xúc trong giọng nói
- ⚡ **Speed Control**: Tùy chỉnh tốc độ đọc
- 🤖 **Auto Provider Selection**: Tự động chọn TTS provider tốt nhất

## 🚀 Cách truy cập

### Từ Video Creation Tab:
1. 📝 Nhập prompt và tạo story
2. 🎵 Click **"🎵 Tạo Audio"**
3. 🎭 Click **"🎭 Cấu hình giọng thủ công"**

### Từ Settings Tab:
1. ⚙️ Mở **Settings tab**
2. 📱 Click **"📱 Kiểm tra Device"** để xem Chatterbox status
3. 🧹 Click **"🧹 Xóa Cache"** để quản lý memory

## 🎮 Giao diện Manual Voice Setup

### 📱 Layout Responsive
```
┌─────────────────────────────────────────────────────────────┐
│ 🎭 Cấu hình giọng đọc theo nhân vật                        │
├─────────────────────────────────────────────────────────────┤
│ 👥 Cấu hình nhân vật (70%)    │ 📋 Thông tin & Controls (30%) │
│                               │                              │
│ ┌─ Nhân vật 1 ─────────────┐  │ 🤖 CHATTERBOX TTS:           │
│ │ ✅ Sử dụng               │  │ Status: ✅ Available          │
│ │ Tên: [Narrator]          │  │ Device: Apple MPS (M2 chip)  │
│ │ ID: [narrator]           │  │                              │
│ │ Giới tính: [Trung tính]  │  │ 🇻🇳 GOOGLE TTS (Vietnamese): │
│ │ TTS Provider: [🔄 Auto]  │  │ • Standard A/B/C/D           │
│ │ Giọng: [Auto-select]     │  │ • Wavenet A/B/C/D            │
│ │ 🔊                       │  │                              │
│ │                          │  │ ⚡ Thao tác nhanh:           │
│ │ [Chatterbox Controls]    │  │ ⚙️ Load Preset               │
│ │ 🎭 Emotion: [1.0] ████   │  │ 🎵 Test tất cả giọng         │
│ │ ⚡ Speed: [1.0] ████     │  │ 🔄 Reset về mặc định         │
│ │ 🎤 Clone: [📁 Upload]    │  │ 📱 Chatterbox Device Info    │
│ └─────────────────────────┘  │ 🧹 Clear Chatterbox Cache    │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Cấu hình từng nhân vật

### 1. Thông tin cơ bản
- **✅ Sử dụng**: Bật/tắt nhân vật này
- **Tên**: Tên hiển thị của nhân vật
- **ID**: Mã định danh unique (không trùng lặp)
- **Giới tính**: Nữ/Nam/Trung tính (auto-select voice phù hợp)

### 2. TTS Provider Selection
Chọn provider phù hợp với nhu cầu:

#### 🔄 Auto-select (Recommended)
```
✅ Tự động chọn provider tốt nhất
🇻🇳 Vietnamese text → Google TTS
🇺🇸 English text → Chatterbox TTS
```

#### 🇻🇳 Google TTS (Vietnamese)
```
✅ Hỗ trợ tiếng Việt tốt nhất
🎵 8 giọng: Standard A/B/C/D, Wavenet A/B/C/D
💰 Free (có giới hạn) + Cloud (trả phí)
```

#### 🤖 Chatterbox TTS (English)
```
✅ SoTA AI voice cloning
🎭 Emotion control (0.0-2.0)
⚡ Speed control (0.5-2.0)
🎤 Voice cloning từ audio samples
```

#### 🎭 ElevenLabs (English)
```
✅ High-quality English voices
🎵 8 giọng: Rachel, Drew, Clyde, Paul, etc.
💰 Requires API key
```

## 🤖 Chatterbox TTS Controls

### 🎭 Emotion Control
Điều chỉnh cảm xúc trong giọng nói:

| Slider Value | Emotion Level | Sử dụng cho |
|-------------|---------------|-------------|
| 0.0 - 0.5   | 😐 Neutral, flat | Tài liệu, formal |
| 0.6 - 1.0   | 🙂 Natural | Hội thoại bình thường |
| 1.1 - 1.5   | 😊 Expressive | Kể chuyện, nhân vật |
| 1.6 - 2.0   | 🤩 Very emotional | Kịch, hoạt hình |

### ⚡ Speed Control
Điều chỉnh tốc độ đọc:

| Slider Value | Speed | Sử dụng cho |
|-------------|-------|-------------|
| 0.5 - 0.7   | 🐌 Slow | Giải thích, học tập |
| 0.8 - 1.2   | 🚶 Normal | Hội thoại thường |
| 1.3 - 1.7   | 🏃 Fast | Hành động, phấn khích |
| 1.8 - 2.0   | 🚀 Very fast | Hiệu ứng đặc biệt |

### 🎤 Voice Cloning
Clone giọng từ audio samples:

#### Chuẩn bị Audio Sample:
- ✅ **Thời lượng**: 3-30 giây
- ✅ **Chất lượng**: Rõ ràng, không tạp âm
- ✅ **Format**: .wav, .mp3, .flac, .m4a
- ✅ **Nội dung**: 1 người nói, tự nhiên
- ✅ **Ngôn ngữ**: English (hiện tại)

#### Workflow:
1. 📁 Click **"📁 Upload Voice Sample"**
2. 🎵 Chọn file audio (3-30s)
3. ✅ Thấy **"✅ filename.wav"** → Upload thành công
4. 🎙️ Voice sẽ được clone khi generate audio

## ⚡ Thao tác nhanh

### ⚙️ Load Preset
Nạp cấu hình mẫu cho các thể loại:

#### 🏰 Câu chuyện cổ tích
```
1. Người kể chuyện (Trung tính)
2. Công chúa (Nữ)
3. Hoàng tử (Nam)
4. Phù thủy (Nữ)
```

#### 🌟 Phiêu lưu trẻ em
```
1. Người kể chuyện (Trung tính)
2. Cô bé (Nữ)
3. Cậu bé (Nam)
4. Thú cưng (Nam)
5. Người bạn (Nữ)
```

#### 👨‍👩‍👧‍👦 Gia đình
```
1. Người kể chuyện (Trung tính)
2. Mẹ (Nữ)
3. Bố (Nam)
4. Con gái (Nữ)
5. Con trai (Nam)
6. Ông bà (Trung tính)
```

#### 🎭 Kịch sân khấu
```
1. Người dẫn chuyện (Trung tính)
2. Nhân vật A (Nữ)
3. Nhân vật B (Nam)
4. Phản diện (Nam)
5. Anh hùng (Nữ)
```

### 🎵 Test tất cả giọng
- Tạo audio test cho tất cả nhân vật đã kích hoạt
- Mỗi nhân vật sẽ nói: "Test giọng số X: Tôi là [Tên]"
- Audio test sẽ được phát tự động

### 🔄 Reset về mặc định
- Khôi phục cấu hình ban đầu
- Chỉ 2 nhân vật đầu được kích hoạt
- Tất cả settings về default

## 📱 Chatterbox Device Management

### 📱 Chatterbox Device Info
Xem thông tin chi tiết về hardware:

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

📊 Current Memory Usage:
• CPU Memory: 256 MB (2.1%)
```

### 🧹 Clear Chatterbox Cache
Giải phóng memory khi cần:

```
🧹 Chatterbox TTS Cache Cleared

Memory Usage Before/After:
• CPU: 512 → 256 MB (freed: 256 MB)
✅ Voice cloning cache cleared
✅ GPU cache cleared (if applicable)
✅ Memory resources freed
```

## 🎯 Workflow hoàn chỉnh

### Bước 1: Chuẩn bị
1. 🔧 Mở Settings → Click **"📱 Kiểm tra Device"**
2. ✅ Verify Chatterbox status
3. 🧹 Clear cache nếu cần thiết

### Bước 2: Cấu hình nhân vật
1. 🎭 Mở Manual Voice Setup Dialog
2. ⚙️ Load preset phù hợp hoặc cấu hình manual
3. 🤖 Chọn Chatterbox TTS cho English characters
4. 🎭 Điều chỉnh emotion và speed
5. 🎤 Upload voice samples nếu muốn clone

### Bước 3: Test và fine-tune
1. 🔊 Click preview cho từng nhân vật
2. 🎵 Test tất cả giọng cùng lúc
3. 🔧 Điều chỉnh parameters nếu cần
4. ✅ Confirm khi hài lòng

### Bước 4: Generate audio
1. ✅ Click **"✅ Áp dụng"**
2. ⏳ Chờ audio generation
3. 🎵 Enjoy high-quality AI voices!

## 🐛 Troubleshooting

### ❌ Chatterbox Not Available
**Triệu chứng**: Device info hiển thị "❌ Not available"

**Giải pháp**:
1. 🐍 Upgrade Python to 3.11+ (hiện tại 3.9 có compatibility issue)
2. 📦 Run: `python3 install_chatterbox.py`
3. 🔧 Check PyTorch installation
4. 💾 Ensure sufficient memory

### 🔊 Preview không hoạt động
**Giải pháp**:
1. ✅ Check provider selection
2. 🎤 Verify voice sample format
3. 🔧 Try different emotion/speed values
4. 🧹 Clear cache và retry

### 💾 Memory issues
**Giải pháp**:
1. 🧹 Clear Chatterbox cache thường xuyên
2. 📱 Monitor device info
3. 🔄 Restart app nếu cần
4. 💻 Close other memory-intensive apps

## 💡 Tips & Best Practices

### 🎭 Emotion Settings
- **Narrator**: 0.8-1.0 (natural, không quá dramatic)
- **Characters**: 1.2-1.5 (expressive cho personality)
- **Action scenes**: 1.5-1.8 (high energy)
- **Formal content**: 0.5-0.7 (professional)

### ⚡ Speed Settings
- **Storytelling**: 0.9-1.1 (comfortable pace)
- **Dialogue**: 1.0-1.3 (natural conversation)
- **Explanations**: 0.7-0.9 (clear understanding)
- **Excitement**: 1.3-1.6 (energetic)

### 🎤 Voice Cloning Tips
- 📱 Record với smartphone quality là đủ
- 🎙️ Nói tự nhiên, không đọc máy móc
- 🔇 Tránh background noise
- ⏱️ 10-15 giây là optimal length
- 🗣️ Include variety trong intonation

### 🔄 Provider Strategy
- 🇻🇳 **Vietnamese content**: Luôn dùng Google TTS
- 🇺🇸 **English content**: Chatterbox TTS (nếu có) > ElevenLabs > Google
- 🔄 **Mixed content**: Auto-select để tối ưu
- 💰 **Budget conscious**: Google TTS free tier

---

## 🎉 Kết luận

Với Chatterbox TTS integration, bạn giờ có thể tạo ra những video với chất lượng giọng đọc professional-grade. Hãy thử nghiệm với các settings khác nhau để tìm ra combination hoàn hảo cho nội dung của bạn!

**Happy voice generating! 🎙️✨** 