# 📁 Voice Mapping Configuration

Thư mục này chứa các file cấu hình voice mapping đã được lưu từ dialog "Cấu hình giọng đọc theo nhân vật".

## 🗂️ Các file được tạo

### `voice_mapping.json`
File cấu hình chính chứa:
- **characters**: Danh sách nhân vật với thông tin chi tiết
- **voice_mapping**: Mapping giữa character ID và voice configuration  
- **last_saved**: Thời gian lưu cuối cùng

## 🔄 Tính năng Auto Save/Load

### Auto Save
- Tự động lưu cấu hình khi bấm "✅ Áp dụng cấu hình"
- Ghi đè file cũ với cấu hình mới nhất
- Backup thời gian lưu để track changes

### Auto Load  
- Tự động nạp cấu hình đã lưu khi mở dialog
- Khôi phục tất cả settings: tên, ID, giới tính, provider, voice
- Bao gồm cả Chatterbox emotion/speed settings và voice cloning

## 🎛️ Thao tác thủ công

### Lưu cấu hình
1. Thiết lập nhân vật như mong muốn
2. Bấm "💾 Lưu cấu hình" 
3. File được lưu tại `./configs/voice_mapping.json`

### Load cấu hình
1. Bấm "📂 Load cấu hình"
2. Tất cả settings được khôi phục từ file đã lưu
3. Hiển thị thời gian lưu cuối cùng

## 📋 Format file JSON

```json
{
  "characters": [
    {
      "id": "narrator",
      "name": "Người kể chuyện", 
      "gender": "neutral",
      "suggested_voice": "vi-VN-Standard-C",
      "provider": "🇻🇳 Google TTS (Vietnamese)"
    }
  ],
  "voice_mapping": {
    "narrator": {
      "provider": "🇻🇳 Google TTS (Vietnamese)",
      "voice": "vi-VN-Standard-C"
    }
  },
  "last_saved": "2025-06-16 12:25:30"
}
```

## ⚠️ Lưu ý

- File được ghi đè mỗi lần save (không có versioning)
- Voice cloning samples được reference theo đường dẫn tuyệt đối
- Nếu voice sample bị xóa, chức năng cloning sẽ không hoạt động 