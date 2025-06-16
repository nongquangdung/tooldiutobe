# Hướng dẫn Setup và Test trên MacOS 13 inch

## 🎯 Tối ưu hóa cho MacOS
Ứng dụng đã được tối ưu đặc biệt cho màn hình MacBook 13 inch với:
- Kích thước cửa sổ: 1200x800 (tối thiểu 1000x700)
- Design system native MacOS với màu sắc và font chuẩn Apple
- Layout responsive với scroll areas
- Giao diện compact và hiện đại

## 🚀 Khởi chạy nhanh

### 1. Chạy ứng dụng
```bash
cd /path/to/toolytb
python3 src/main.py
```

### 2. Cấu hình API Keys (tùy chọn)
Vào tab **⚙️ Cài đặt** và nhập:
- **OpenAI API Key**: Để tạo ảnh và nội dung (khuyến nghị)
- **DeepSeek API Key**: Đã có sẵn, có thể thay đổi
- **ElevenLabs API Key**: Để có giọng đọc chất lượng cao

### 3. Test tạo video cơ bản

#### Bước 1: Tạo câu chuyện
1. Vào tab **🎬 Tạo Video**
2. Chọn danh mục prompt từ dropdown (ví dụ: "Du lịch")
3. Chọn một prompt mẫu hoặc nhập prompt tùy chỉnh
4. Nhấn **📝 Tạo câu chuyện**
5. Xem preview nội dung trong phần "📄 Xem trước nội dung"

#### Bước 2: Tạo video hoàn chỉnh
1. Sau khi có câu chuyện, nhấn **🎬 Tạo video hoàn chỉnh**
2. Theo dõi tiến trình trong phần "📊 Tiến trình"
3. Video sẽ được lưu trong thư mục `projects/`

## 🎨 Tính năng UI/UX mới

### Layout tối ưu
- **Scroll Areas**: Tất cả nội dung dài đều có scroll, không bao giờ tràn màn hình
- **Group Boxes**: Nội dung được tổ chức thành các nhóm logic
- **Compact Design**: Tối đa hóa thông tin hiển thị trên màn hình 13"

### Tab Navigation
- **🎬 Tạo Video**: Giao diện chính với 6 nhóm chức năng
- **📁 Dự án**: Splitter layout 40%-60% để quản lý projects
- **⚙️ Cài đặt**: 6 nhóm cài đặt được tổ chức rõ ràng

### Visual Improvements
- **Native MacOS Colors**: Sử dụng #007AFF (iOS Blue)
- **Rounded Corners**: Border radius 8px
- **Hover Effects**: Smooth transitions
- **Icon Integration**: Emoji icons cho dễ nhận diện

## 🔧 Troubleshooting

### Lỗi thường gặp
1. **"pydub không available"**: 
   ```bash
   pip3 install pydub
   ```

2. **Lỗi OpenAI API**: Cấu hình API key trong tab Cài đặt

3. **Lỗi font**: MacOS sẽ tự động fallback sang system font

### Performance Tips
- Đóng các ứng dụng khác để tối ưu RAM
- Sử dụng preset "Minimal" cho video nhanh
- Kiểm tra kết nối internet cho API calls

## 📱 Responsive Design

### Kích thước cửa sổ
- **Default**: 1200x800 (tối ưu cho MacBook 13")
- **Minimum**: 1000x700 (vẫn sử dụng được)
- **Maximum**: 1400x900 (cho màn hình lớn hơn)

### Adaptive Layout
- Tự động điều chỉnh theo kích thước cửa sổ
- Scroll bars xuất hiện khi cần thiết
- Splitter có thể resize theo ý muốn

## 🎯 Test Cases

### Test 1: Tạo video cơ bản
1. Prompt: "Tạo video giới thiệu về cà phê Việt Nam"
2. Preset: "Năng động"
3. Kiểm tra: Câu chuyện → Audio → Video

### Test 2: Sử dụng ảnh thủ công
1. Chọn "Chọn ảnh thủ công"
2. Chọn thư mục chứa ảnh
3. Tạo video với ảnh có sẵn

### Test 3: Quản lý projects
1. Tạo nhiều projects
2. Test chức năng xóa, mở thư mục
3. Kiểm tra splitter resize

## 📊 Performance Metrics

### Thời gian tạo video (ước tính)
- **Tạo câu chuyện**: 10-30 giây
- **Tạo ảnh AI**: 30-60 giây (5 ảnh)
- **Tạo audio**: 20-40 giây
- **Render video**: 30-60 giây
- **Tổng**: 2-4 phút cho video 30-60 giây

### Yêu cầu hệ thống
- **RAM**: Tối thiểu 4GB, khuyến nghị 8GB+
- **Storage**: 1GB trống cho temp files
- **Network**: Ổn định cho API calls
- **macOS**: 10.14+ (Mojave trở lên) 