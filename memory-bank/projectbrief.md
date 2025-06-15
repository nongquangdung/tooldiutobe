# projectbrief.md

## Tên dự án
Công cụ tạo video tự động bằng AI từ prompt

## Mục tiêu
Tự động hóa quá trình sản xuất video ngắn (TikTok, YouTube Shorts, Reels) từ một prompt duy nhất, tích hợp AI sinh kịch bản, tạo ảnh, chuyển văn bản thành giọng nói và dựng video hoàn chỉnh với hiệu ứng.

## Phạm vi
- Nhập prompt, sinh kịch bản, chia đoạn, sinh mô tả ảnh, lời thoại.
- Tạo ảnh AI cho từng đoạn (có thể chọn/tải ảnh).
- Chuyển lời thoại thành giọng nói (Google TTS/ElevenLabs).
- Dựng video từng đoạn (ảnh + audio + hiệu ứng) bằng FFmpeg.
- Gộp các đoạn thành video hoàn chỉnh, cho phép tải từng phần.
- Hỗ trợ hiệu ứng chuyển cảnh, zoom, khớp hình với thoại.
- Giao diện desktop (PySide6 hoặc Electron), kéo thả sắp xếp đoạn, preset hiệu ứng, gợi ý prompt mẫu.

## Yêu cầu bắt buộc
- Tích hợp AI sinh nội dung, tạo ảnh, TTS, dựng video.
- Lưu từng đoạn thành file riêng biệt.
- Cho phép xuất video hoàn chỉnh hoặc tải từng phần.

## Không nằm trong phạm vi
- Phát trực tiếp video đã dựng.

## Kiến trúc tổng thể
- Ứng dụng desktop (UI nhập prompt, chỉnh sửa, preview, xuất video).
- Tích hợp API AI (OpenAI, DALL·E, Google TTS, ElevenLabs...).
- Bộ dựng video nội bộ (FFmpeg). 