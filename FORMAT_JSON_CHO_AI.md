# Format JSON Chuẩn Cho AI Models - Tạo Script Video

## 🎯 Mục đích
File này cung cấp format JSON chuẩn để yêu cầu các AI models (DeepSeek, Claude, ChatGPT) xuất ra script video có thể sử dụng trực tiếp trong hệ thống.

## 📝 Format JSON Bắt Buộc

```json
{
  "segments": [
    {
      "id": 1,
      "script": "Tiêu đề hoặc nội dung chính của đoạn này",
      "image_prompt": "Mô tả chi tiết hình ảnh cần tạo cho đoạn này",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Lời thoại của người kể chuyện",
          "emotion": "neutral"
        },
        {
          "speaker": "character1",
          "text": "Lời thoại của nhân vật chính",
          "emotion": "happy"
        }
      ],
      "duration": 12
    },
    {
      "id": 2,
      "script": "Nội dung đoạn 2",
      "image_prompt": "Mô tả hình ảnh đoạn 2",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Tiếp tục câu chuyện...",
          "emotion": "excited"
        }
      ],
      "duration": 15
    }
  ],
  "characters": [
    {
      "id": "narrator",
      "name": "Người kể chuyện",
      "gender": "neutral",
      "suggested_voice": "vi-VN-Standard-C"
    },
    {
      "id": "character1",
      "name": "Nhân vật chính",
      "gender": "female",
      "suggested_voice": "vi-VN-Standard-A"
    }
  ]
}
```

## 🎭 Danh Sách Characters Hỗ Trợ

### Speaker IDs:
- `narrator` - Người kể chuyện (giọng trung tính)
- `character1` - Nhân vật chính
- `character2` - Nhân vật phụ
- `character3` - Nhân vật thứ 3 (nếu cần)
- `system` - Thông báo hệ thống

### Gender Options:
- `neutral` - Giọng trung tính
- `female` - Giọng nữ
- `male` - Giọng nam

### Emotion Options:
- `neutral` - Bình thường
- `happy` - Vui vẻ
- `excited` - Phấn khích
- `sad` - Buồn
- `angry` - Tức giận
- `surprised` - Ngạc nhiên
- `friendly` - Thân thiện

### Suggested Voices (Vietnamese):
- `vi-VN-Standard-A` - Nữ, Standard
- `vi-VN-Standard-B` - Nam, Standard  
- `vi-VN-Standard-C` - Nữ, Standard
- `vi-VN-Standard-D` - Nam, Standard
- `vi-VN-Wavenet-A` - Nữ, Wavenet (chất lượng cao)
- `vi-VN-Wavenet-B` - Nam, Wavenet (chất lượng cao)
- `vi-VN-Wavenet-C` - Nữ, Wavenet (chất lượng cao)
- `vi-VN-Wavenet-D` - Nam, Wavenet (chất lượng cao)

## 🛡️ Lưu Ý Quan Trọng

### 1. JSON Thuần Túy
```
❌ KHÔNG SỬ DỤNG:
```json
{...}
```

✅ CHỈ XUẤT JSON THUẦN:
{...}
```

### 2. Chuỗi Phải Đầy Đủ
- Không được để chuỗi bị cắt giữa chừng
- Tất cả dấu ngoặc kép phải được đóng
- Kiểm tra syntax JSON trước khi xuất

### 3. Thời Lượng Hợp Lý
- Mỗi segment: 10-20 giây
- Tổng video: 60-120 giây
- Duration tính bằng giây

### 4. Image Prompt Chi Tiết
- Mô tả cụ thể về hình ảnh
- Bao gồm màu sắc, bối cảnh, góc nhìn
- Phù hợp với nội dung audio

## 📋 Template Prompt Cho AI Models

### Cho DeepSeek:
```
Tạo script video ngắn từ prompt: "[YOUR_PROMPT]"

Yêu cầu:
1. Chia thành 3-5 đoạn, mỗi đoạn 10-15 giây
2. Có ít nhất 2 characters: narrator và character1
3. Mỗi dialogue phải có emotion phù hợp
4. Image_prompt chi tiết cho từng đoạn
5. Xuất CHÍNH XÁC theo format JSON trong file FORMAT_JSON_CHO_AI.md
6. KHÔNG sử dụng markdown wrapper, chỉ JSON thuần

Trả về JSON hoàn chỉnh, đảm bảo syntax đúng:
```

### Cho Claude/ChatGPT:
```
Tạo kịch bản video TikTok từ: "[YOUR_PROMPT]"

Format: JSON thuần (không markdown)
Segments: 3-5 đoạn
Characters: narrator + character1 (tối thiểu)
Duration: 10-15s mỗi đoạn
Language: Tiếng Việt

Đảm bảo JSON syntax hoàn chỉnh, không cắt chuỗi giữa chừng.
```

## 🔧 Test Script Có Sẵn

Nếu muốn test TTS với script có sẵn, sử dụng format này:

```json
{
  "segments": [
    {
      "id": 1,
      "script": "Giới thiệu chủ đề",
      "image_prompt": "Hình ảnh thu hút sự chú ý",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Xin chào mọi người!",
          "emotion": "friendly"
        },
        {
          "speaker": "character1", 
          "text": "Hôm nay chúng ta sẽ cùng khám phá...",
          "emotion": "excited"
        }
      ],
      "duration": 10
    }
  ],
  "characters": [
    {
      "id": "narrator",
      "name": "Người dẫn chương trình",
      "gender": "neutral",
      "suggested_voice": "vi-VN-Wavenet-C"
    },
    {
      "id": "character1",
      "name": "Chuyên gia",
      "gender": "female", 
      "suggested_voice": "vi-VN-Wavenet-A"
    }
  ]
}
```

## 🎯 Sử Dụng Trong Ứng Dụng

1. **Copy JSON** từ AI model
2. **Paste vào** ứng dụng (tab Create Video)
3. **Click** "Generate Audio & Video"
4. **Kiểm tra** preview trong tab Projects

Hệ thống sẽ tự động:
- ✅ Parse JSON
- ✅ Tạo audio cho từng dialogue  
- ✅ Gộp audio theo timeline
- ✅ Tạo video với ảnh + audio 