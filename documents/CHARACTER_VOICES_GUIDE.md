# 🎭 Hướng dẫn sử dụng Character Voices System

## Tổng quan

System Character Voices cho phép tạo audio với nhiều giọng đọc khác nhau theo từng nhân vật trong câu chuyện. Hệ thống tự động:

- ✅ Phân tách kịch bản theo nhân vật (speaker)
- ✅ Chọn giọng đọc (voice) cho từng nhân vật
- ✅ Gọi Google TTS API theo từng đoạn, từng voice
- ✅ Ghép các file .mp3 thành một file thoại hoàn chỉnh

## 🚀 Cách sử dụng

### Bước 1: Tạo câu chuyện
1. Mở ứng dụng `python src/main.py`
2. Nhập prompt ví dụ: "Tạo câu chuyện về cuộc phiêu lưu của cô bé Linh và chú gấu Bông"
3. Bấm **📝 Tạo câu chuyện**
4. Hệ thống sẽ tự động phân tích và tạo nhân vật

### Bước 2: Chọn giọng đọc cho từng nhân vật
1. Sau khi tạo câu chuyện xong, nút **🎵 Tạo Audio** sẽ được kích hoạt
2. Bấm **🎵 Tạo Audio**
3. Dialog "Chọn giọng đọc cho từng nhân vật" sẽ hiện ra

### Bước 3: Cấu hình giọng đọc
Trong dialog Character Voice:

| Cột | Mô tả |
|-----|-------|
| **Nhân vật** | Tên nhân vật (ví dụ: Cô bé Linh, Chú gấu Bông) |
| **Giới tính** | Nam/Nữ/Trung tính |
| **Giọng gợi ý** | AI tự động đề xuất giọng phù hợp |
| **Giọng chọn** | Dropdown chọn giọng cuối cùng |
| **Preview** | Nút 🔊 để nghe thử giọng |

### Bước 4: Test và áp dụng
- Bấm **🔊** để nghe thử giọng của từng nhân vật
- Bấm **🎵 Test tất cả** để test toàn bộ giọng
- Bấm **✅ Áp dụng** để bắt đầu tạo audio

### Bước 5: Nghe kết quả
- Sau khi tạo xong, bấm **📁 Mở thư mục Audio** để xem files
- Bấm **▶️ Nghe Audio hoàn chỉnh** để phát file cuối cùng

## 🎤 Giọng đọc có sẵn

### Giọng Nam
- `vi-VN-Standard-B` - Giọng nam chuẩn
- `vi-VN-Standard-D` - Giọng nam chuẩn 2
- `vi-VN-Wavenet-B` - Giọng nam chất lượng cao
- `vi-VN-Wavenet-D` - Giọng nam chất lượng cao 2

### Giọng Nữ
- `vi-VN-Standard-A` - Giọng nữ chuẩn
- `vi-VN-Standard-C` - Giọng nữ chuẩn 2
- `vi-VN-Wavenet-A` - Giọng nữ chất lượng cao
- `vi-VN-Wavenet-C` - Giọng nữ chất lượng cao 2

💡 **Gợi ý:** Wavenet có chất lượng âm thanh tốt hơn Standard

## 📁 Cấu trúc file được tạo

```
project_name/
├── audio/
│   ├── s1_d1_narrator.mp3      # Segment 1, Dialogue 1, Narrator
│   ├── s1_d2_character1.mp3    # Segment 1, Dialogue 2, Character 1
│   ├── s1_d3_character2.mp3    # Segment 1, Dialogue 3, Character 2
│   ├── segment_1_complete.mp3  # Segment 1 hoàn chỉnh
│   ├── segment_2_complete.mp3  # Segment 2 hoàn chỉnh
│   └── final_complete_audio.mp3 # File audio cuối cùng hoàn chỉnh
```

## 🎯 Ví dụ sử dụng

### Input Prompt:
```
Tạo câu chuyện về cuộc phiêu lưu của cô bé Linh và chú gấu Bông đi tìm kho báu
```

### AI sẽ tạo:
```json
{
  "characters": [
    {
      "id": "narrator",
      "name": "Người kể chuyện",
      "gender": "neutral",
      "suggested_voice": "vi-VN-Standard-C"
    },
    {
      "id": "linh",
      "name": "Cô bé Linh", 
      "gender": "female",
      "suggested_voice": "vi-VN-Wavenet-A"
    },
    {
      "id": "bong",
      "name": "Chú gấu Bông",
      "gender": "male", 
      "suggested_voice": "vi-VN-Wavenet-B"
    }
  ],
  "segments": [
    {
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Trong một ngày nắng đẹp...",
          "emotion": "neutral"
        },
        {
          "speaker": "linh", 
          "text": "Bông ơi, chúng ta đi tìm kho báu nhé!",
          "emotion": "excited"
        },
        {
          "speaker": "bong",
          "text": "Grrr... Bông sẵn sàng bảo vệ Linh!",
          "emotion": "determined"
        }
      ]
    }
  ]
}
```

### Kết quả:
- ✅ Audio cho Người kể chuyện: giọng trung tính
- ✅ Audio cho Cô bé Linh: giọng nữ trong sáng
- ✅ Audio cho Chú gấu Bông: giọng nam ấm áp
- ✅ File tổng hợp hoàn chỉnh với dialogue tự nhiên

## 🔧 Tính năng nâng cao

### Character Voice Dialog

| Nút | Chức năng |
|-----|-----------|
| **🎵 Test tất cả** | Tạo sample audio cho tất cả nhân vật |
| **🔄 Reset** | Reset về giọng AI gợi ý |
| **🔊 Preview** | Nghe thử giọng từng nhân vật |

### Audio Controls

| Nút | Chức năng |
|-----|-----------|
| **📁 Mở thư mục Audio** | Mở folder chứa tất cả audio files |
| **▶️ Nghe Audio hoàn chỉnh** | Phát file audio cuối cùng |

## ⚙️ Cấu hình

### API Keys cần thiết:
- **Google Cloud TTS API Key** - Cho tạo giọng chất lượng cao
- **DeepSeek/OpenAI/Claude API Key** - Cho tạo nội dung

### Setup Google TTS:
1. Vào Google Cloud Console
2. Enable Text-to-Speech API  
3. Tạo Service Account và download JSON key
4. Set environment variable `GOOGLE_TTS_API_KEY`

## 🐛 Troubleshooting

### Lỗi thường gặp:

**"Không tìm thấy thông tin nhân vật"**
- Đảm bảo đã tạo câu chuyện trước khi tạo audio
- Thử tạo lại câu chuyện với prompt rõ ràng hơn

**"Lỗi tạo audio"**
- Kiểm tra Google TTS API key
- Đảm bảo có kết nối internet
- Thử lại với giọng Standard thay vì Wavenet

**"Preview không hoạt động"**
- Kiểm tra Windows Media Player hoặc audio player mặc định
- Thử mở file audio thủ công từ thư mục

## 📊 Performance

### Thời gian tạo audio:
- **1 nhân vật, 1 segment**: ~5-10 giây
- **3 nhân vật, 5 segments**: ~30-60 giây  
- **Phụ thuộc**: Độ dài text, số lượng characters, voice quality

### File size ước tính:
- **Standard voices**: ~50KB/phút
- **Wavenet voices**: ~100KB/phút

## 🎉 Kết luận

Character Voices System cho phép tạo ra những câu chuyện audio sống động với nhiều giọng đọc khác nhau, mang lại trải nghiệm nghe thú vị và chuyên nghiệp. Hệ thống hoàn toàn tự động hóa từ việc phân tích nhân vật đến tạo audio cuối cùng! 