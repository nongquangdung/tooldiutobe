# Format JSON Chuẩn Cho AI Models - Tạo Script Video (Enhanced Version 2.0)

## 🎯 Mục đích
File này cung cấp format JSON chuẩn được nâng cấp để yêu cầu các AI models (DeepSeek, Claude, ChatGPT) xuất ra script video có thể sử dụng trực tiếp trong hệ thống với khả năng quản lý cảm xúc, giới tính và metadata dự án tốt hơn.

## 🚀 TEMPLATE MODES - TOKEN OPTIMIZATION

### 🏃‍♂️ RAPID Mode (~150 tokens) - Ultra Compact

**Sử dụng khi**: Story đơn giản, cần token tối đa cho content

```json
{
  "segments": [
    {"id": 1, "dialogues": [
      {"speaker": "narrator", "text": "...", "emotion": "friendly"},
      {"speaker": "character1", "text": "...", "emotion": "excited"}
    ]}
  ],
  "characters": [
    {"id": "narrator", "name": "Narrator", "gender": "neutral"},
    {"id": "character1", "name": "Character", "gender": "female"}
  ]
}
```

**Rules**: segments[].dialogues[]: speaker, text, emotion. characters[]: id, name, gender. Available emotions: neutral, happy, sad, excited, calm, dramatic.

---

### 📝 STANDARD Mode (~400 tokens) - Balanced

**Sử dụng khi**: Story trung bình, cần balance giữa format và content

```json
{
  "project": {"title": "Story Title", "duration": 60},
  "segments": [
    {
      "id": 1,
      "title": "Scene name",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Content here with proper Vietnamese punctuation",
          "emotion": "friendly",
          "pause_after": 1.0,
          "emphasis": ["từ khóa 1", "từ khóa 2"]
        }
      ]
    }
  ],
  "characters": [
    {
      "id": "narrator", 
      "name": "Character Name",
      "gender": "neutral|female|male",
      "default_emotion": "friendly",
      "personality": "professional, warm"
    }
  ]
}
```

**Enhanced emotions**: neutral, gentle, contemplative, cheerful, excited, surprised, sorrowful, angry, friendly, happy, sad, mysterious, dramatic, confident, worried, calm, energetic, serious.

**Intensity**: 0.5-2.0 (1.0 default). **Speed**: 0.5-1.5 (1.0 default).

---

### 📚 DETAILED Mode (~800 tokens) - Full Features

**Sử dụng khi**: Story phức tạp, nhiều characters, cần advanced features

## 📝 Format JSON Bắt Buộc (Enhanced)

```json
{
  "project": {
    "title": "Tên dự án hoặc video",
    "description": "Mô tả ngắn gọn về nội dung video",
    "total_duration": 60,
    "target_audience": "Đối tượng mục tiêu (VD: teen, adult, general)",
    "style": "Phong cách video (VD: educational, entertainment, story)",
    "created_date": "2024-01-20"
  },
  "segments": [
    {
      "id": 1,
      "title": "Mở đầu - Giới thiệu chủ đề",
      "script": "Nội dung chính của đoạn này - câu chuyện hoặc thông tin",
      "image_prompt": "Mô tả chi tiết hình ảnh cần tạo cho đoạn này, bao gồm bối cảnh, màu sắc, góc chụp",
      "mood": "Tâm trạng chung của đoạn: upbeat, serious, mysterious, calm, dramatic",
      "background_music": "Loại nhạc nền: energetic, calm, mysterious, dramatic, none",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Lời thoại của người kể chuyện - giữ nguyên dấu câu và ngữ điệu",
          "emotion": "friendly",
          "pause_after": 0.5,
          "emphasis": ["từ", "cần", "nhấn", "mạnh"]
        },
        {
          "speaker": "character1",
          "text": "Lời thoại của nhân vật chính với cảm xúc rõ ràng",
          "emotion": "excited",
          "pause_after": 1.0,
          "emphasis": ["wow", "tuyệt vời"]
        }
      ],
      "duration": 12,
      "transition": "fade",
      "camera_movement": "zoom_in"
    },
    {
      "id": 2,
      "title": "Phát triển - Nội dung chính",
      "script": "Nội dung đoạn 2 với chi tiết và thông tin quan trọng",
      "image_prompt": "Mô tả hình ảnh đoạn 2 với details cụ thể",
      "mood": "serious",
      "background_music": "calm",
      "dialogues": [
        {
          "speaker": "character2",
          "text": "Đây là thông tin quan trọng mà chúng ta cần biết...",
          "emotion": "contemplative",
          "pause_after": 1.5,
          "emphasis": ["quan trọng", "cần biết"]
        },
        {
          "speaker": "narrator",
          "text": "Tiếp tục phát triển câu chuyện với chi tiết thú vị",
          "emotion": "neutral",
          "pause_after": 0.8,
          "emphasis": []
        }
      ],
      "duration": 15,
      "transition": "slide",
      "camera_movement": "pan_right"
    }
  ],
  "characters": [
    {
      "id": "narrator",
      "name": "Người kể chuyện",
      "description": "Giọng dẫn chuyện chính, trung tính và dễ nghe",
      "gender": "neutral",
      "age_range": "adult",
      "personality": "professional, warm, engaging",
      "voice_characteristics": "clear, moderate_pace, authoritative",
      "suggested_voice": "vi-VN-Wavenet-C",
      "default_emotion": "friendly"
    },
    {
      "id": "character1",
      "name": "Nhân vật chính",
      "description": "Nhân vật năng động, tích cực trong câu chuyện",
      "gender": "female",
      "age_range": "young_adult",
      "personality": "energetic, optimistic, curious",
      "voice_characteristics": "bright, expressive, engaging",
      "suggested_voice": "vi-VN-Wavenet-A",
      "default_emotion": "happy"
    },
    {
      "id": "character2",
      "name": "Chuyên gia",
      "description": "Nhân vật truyền đạt kiến thức, đáng tin cậy",
      "gender": "male",
      "age_range": "adult",
      "personality": "knowledgeable, calm, thoughtful",
      "voice_characteristics": "deep, steady, authoritative",
      "suggested_voice": "vi-VN-Wavenet-B",
      "default_emotion": "contemplative"
    }
  ],
  "audio_settings": {
    "merge_order": ["intro", "content", "conclusion"],
    "crossfade_duration": 0.3,
    "normalize_volume": true,
    "background_music_volume": 0.2,
    "voice_volume": 1.0,
    "output_format": "mp3",
    "sample_rate": 44100
  },
  "metadata": {
    "version": "2.0",
    "ai_model": "DeepSeek/Claude/ChatGPT",
    "generation_date": "2024-01-20",
    "language": "vi-VN",
    "content_rating": "G",
    "tags": ["educational", "technology", "tutorial"],
    "keywords": ["học tập", "công nghệ", "hướng dẫn"]
  }
}
```

## 🎭 Danh Sách Characters & Emotions Nâng Cao

### Speaker IDs:
- `narrator` - Người kể chuyện (giọng chính)
- `character1` - Nhân vật chính (tích cực, năng động)
- `character2` - Nhân vật phụ/chuyên gia (uy tín, trầm)
- `character3` - Nhân vật thứ 3 (nếu cần)
- `system` - Thông báo hệ thống
- `announcer` - MC, người dẫn chương trình
- `interviewer` - Người phỏng vấn
- `expert` - Chuyên gia trong lĩnh vực

### Gender Options:
- `neutral` - Giọng trung tính, không thiên về nam/nữ
- `female` - Giọng nữ
- `male` - Giọng nam
- `child` - Giọng trẻ em
- `elderly` - Giọng người lớn tuổi

### Age Range:
- `child` - Trẻ em (6-12 tuổi)
- `teen` - Thiếu niên (13-19 tuổi)
- `young_adult` - Thanh niên (20-35 tuổi)
- `adult` - Người lớn (36-55 tuổi)
- `elderly` - Người cao tuổi (55+ tuổi)

### Enhanced Emotion Options (22 cảm xúc):
- `neutral` - Bình thường, trung tính
- `gentle` - Dịu dàng, nhẹ nhàng
- `contemplative` - Suy tư, trầm ngâm
- `cheerful` - Vui vẻ, phấn khích nhẹ
- `excited` - Phấn khích mạnh
- `surprised` - Ngạc nhiên
- `sorrowful` - Buồn bã, thương cảm
- `angry` - Tức giận
- `fierce` - Dữ dội, mạnh mẽ
- `pleading` - Cầu xin, van nài
- `friendly` - Thân thiện
- `happy` - Hạnh phúc
- `sad` - Buồn
- `mysterious` - Bí ẩn
- `dramatic` - Kịch tính
- `confident` - Tự tin
- `worried` - Lo lắng
- `calm` - Bình tĩnh
- `energetic` - Năng lượng cao
- `romantic` - Lãng mạn
- `serious` - Nghiêm túc
- `playful` - Vui đùa, tinh nghịch

### Emotion Intensity (Cường độ cảm xúc):
- `0.5` - Rất nhẹ
- `0.8` - Nhẹ
- `1.0` - Bình thường (mặc định)
- `1.2` - Trung bình
- `1.5` - Mạnh
- `2.0` - Rất mạnh
- `2.5` - Cực mạnh

### Voice Speed (Tốc độ nói):
- `0.5` - Rất chậm
- `0.7` - Chậm
- `0.9` - Hơi chậm
- `1.0` - Bình thường (mặc định)
- `1.1` - Hơi nhanh
- `1.3` - Nhanh
- `1.5` - Rất nhanh

### Suggested Voices (Vietnamese - Enhanced):
- `vi-VN-Standard-A` - Nữ, Standard (ấm áp)
- `vi-VN-Standard-B` - Nam, Standard (chuyên nghiệp)
- `vi-VN-Standard-C` - Nữ, Standard (trẻ trung)
- `vi-VN-Standard-D` - Nam, Standard (uy tín)
- `vi-VN-Wavenet-A` - Nữ, Wavenet (chất lượng cao, biểu cảm)
- `vi-VN-Wavenet-B` - Nam, Wavenet (chất lượng cao, trầm ấm)
- `vi-VN-Wavenet-C` - Nữ, Wavenet (tự nhiên, dễ nghe)
- `vi-VN-Wavenet-D` - Nam, Wavenet (mạnh mẽ, rõ ràng)

## 🛡️ Lưu Ý Quan Trọng (Updated)

### 1. JSON Thuần Túy - Không Markdown
```
❌ KHÔNG SỬ DỤNG:
```json
{...}
```

✅ CHỈ XUẤT JSON THUẦN:
{...}
```

### 2. Chuỗi Phải Đầy Đủ & Escaped
- Không được để chuỗi bị cắt giữa chừng
- Tất cả dấu ngoặc kép phải được đóng
- Escape các ký tự đặc biệt: `\"`, `\\`, `\n`
- Kiểm tra syntax JSON trước khi xuất

### 3. Thời Lượng & Timing Hợp Lý
- Mỗi segment: 8-20 giây
- Tổng video: 45-120 giây
- Duration tính bằng giây
- Pause_after: thời gian tạm dừng sau mỗi dialogue (giây)

### 4. Image Prompt Chi Tiết
- Mô tả cụ thể về hình ảnh, bối cảnh
- Bao gồm màu sắc, ánh sáng, góc nhìn
- Phù hợp với mood và nội dung audio
- Tránh nội dung nhạy cảm hoặc bản quyền

### 5. Character Consistency
- Giữ nhất quán tính cách nhân vật qua các segment
- Default settings phải phù hợp với personality
- Voice characteristics phải match với gender và age

## 📋 Template Prompt Cho AI Models (Enhanced)

### Cho DeepSeek:
```
Tạo script video ngắn từ prompt: "[YOUR_PROMPT]"

Yêu cầu Enhanced Format:
1. Chia thành 3-5 đoạn, mỗi đoạn 10-18 giây
2. Có ít nhất 2-3 characters với tính cách rõ ràng
3. Mỗi dialogue có emotion, intensity, speed phù hợp
4. Character descriptions chi tiết (gender, age, personality)
5. Project metadata đầy đủ (title, description, style)
6. Audio settings cho merging files
7. Image_prompt chi tiết cho từng đoạn
8. Xuất CHÍNH XÁC theo Enhanced Format JSON 2.0
9. KHÔNG sử dụng markdown wrapper, chỉ JSON thuần

Đảm bảo:
- Emotion intensity phù hợp với nội dung
- Character consistency qua các segments
- Timing hợp lý cho video ngắn
- JSON syntax hoàn chỉnh không lỗi

Trả về JSON hoàn chỉnh theo Enhanced Format 2.0:
```

### Cho Claude/ChatGPT:
```
Tạo kịch bản video TikTok/YouTube Shorts từ: "[YOUR_PROMPT]"

Sử dụng Enhanced JSON Format 2.0 với:
- Project metadata đầy đủ
- Characters với personality và voice settings
- Dialogues với emotion intensity và speed control
- Audio merging settings
- 3-5 segments, mỗi segment 10-18 giây
- Language: Tiếng Việt

Format: JSON thuần (không markdown wrapper)
Đảm bảo JSON syntax hoàn chỉnh, không cắt chuỗi.
Character consistency và emotion phù hợp nội dung.
```

## 🔧 Test Script Có Sẵn (Enhanced)

```json
{
  "project": {
    "title": "Hướng dẫn học tiếng Anh hiệu quả",
    "description": "Video ngắn hướng dẫn phương pháp học tiếng Anh cho người mới bắt đầu",
    "total_duration": 45,
    "target_audience": "young_adult",
    "style": "educational",
    "created_date": "2024-01-20"
  },
  "segments": [
    {
      "id": 1,
      "title": "Mở đầu thu hút",
      "script": "Giới thiệu phương pháp học tiếng Anh độc đáo",
      "image_prompt": "Một người trẻ tự tin đứng trước màn hình laptop, background hiện đại với sách và cờ các nước",
      "mood": "upbeat",
      "background_music": "energetic",
      "dialogues": [
        {
          "speaker": "narrator",
          "text": "Bạn có muốn học tiếng Anh nhanh chóng và hiệu quả không?",
          "emotion": "excited",
          "pause_after": 1.0,
          "emphasis": ["nhanh chóng", "hiệu quả"]
        },
        {
          "speaker": "character1",
          "text": "Hôm nay mình sẽ chia sẻ 3 bí quyết tuyệt vời!",
          "emotion": "cheerful",
          "pause_after": 0.8,
          "emphasis": ["3 bí quyết", "tuyệt vời"]
        }
      ],
      "duration": 12,
      "transition": "fade",
      "camera_movement": "zoom_in"
    }
  ],
  "characters": [
    {
      "id": "narrator",
      "name": "MC chính",
      "description": "Người dẫn chương trình năng động, tạo cảm hứng học tập",
      "gender": "female",
      "age_range": "young_adult",
      "personality": "energetic, inspiring, professional",
      "voice_characteristics": "clear, engaging, motivational",
      "suggested_voice": "vi-VN-Wavenet-A",
      "default_emotion": "friendly"
    },
    {
      "id": "character1",
      "name": "Học viên tiêu biểu",
      "description": "Đại diện cho người học, nhiệt huyết và tò mò",
      "gender": "female",
      "age_range": "young_adult",
      "personality": "curious, enthusiastic, relatable",
      "voice_characteristics": "bright, expressive, youthful",
      "suggested_voice": "vi-VN-Wavenet-C",
      "default_emotion": "excited"
    }
  ],
  "audio_settings": {
    "merge_order": ["intro", "content", "conclusion"],
    "crossfade_duration": 0.3,
    "normalize_volume": true,
    "background_music_volume": 0.15,
    "voice_volume": 1.0,
    "output_format": "mp3",
    "sample_rate": 44100
  },
  "metadata": {
    "version": "2.0",
    "ai_model": "DeepSeek",
    "generation_date": "2024-01-20",
    "language": "vi-VN",
    "content_rating": "G",
    "tags": ["educational", "language_learning", "tutorial"],
    "keywords": ["học tiếng Anh", "phương pháp học", "hiệu quả"]
  }
}
```

## 🎯 Sử Dụng Trong Ứng Dụng (Enhanced Workflow)

1. **Generate JSON** từ AI model với Enhanced Format 2.0
2. **Validate JSON** syntax trước khi import
3. **Import vào** Voice Studio tab
4. **Review Characters** và adjust voice settings nếu cần
5. **Preview Audio** với emotion và speed settings
6. **Generate All Voices** với real-time progress
7. **Auto-merge** thành complete conversation
8. **Export & Share** final audio/video

## 🔍 Validation Checklist

### ✅ JSON Structure:
- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] All required fields present
- [ ] Character IDs consistent across segments và characters array
- [ ] Duration values are reasonable numbers

### ✅ Content Quality:
- [ ] Character personalities consistent
- [ ] Emotion intensity matches content tone
- [ ] Dialogue text natural và engaging
- [ ] Image prompts detailed và relevant
- [ ] Total duration appropriate for target platform

### ✅ Audio Settings:
- [ ] Emotion values trong range 0.5-2.5
- [ ] Speed values trong range 0.5-1.5  
- [ ] Voice assignments match character genders
- [ ] Pause timing reasonable (0.3-2.0 seconds)