# 🎭 Hướng dẫn Emotion Configuration UI - Table Format

## Tổng quan

Voice Studio đã được nâng cấp với UI emotion configuration hoàn toàn mới, sử dụng **table format** giống như bảng "cấu hình riêng cho từng nhân vật" để dễ dàng quản lý và tùy chỉnh emotions.

## ✨ Tính năng chính

### 📊 Table Format Layout
- **Bảng 9 cột** hiển thị đầy đủ thông tin emotions
- **Tùy chỉnh trực tiếp** trong bảng với spinboxes và comboboxes
- **Color coding**: Custom emotions (màu xanh lá), Default emotions (màu xanh da trời)
- **Responsive design** với column widths tối ưu

### 🎵 Real Audio Preview
- **Preview âm thanh thật** với TTS engine
- **Progress tracking** với progress bar
- **Auto-play** audio file sau khi generate
- **Error handling** và fallback simulation

### ➕ Custom Emotion Management
- **Thêm emotions mới** với dialog form
- **Xóa custom emotions** (bảo vệ default emotions)
- **Validation** tên emotions và parameters
- **Auto-refresh** table sau khi thay đổi

### 🔍 Advanced Filtering
- **Filter theo category**: neutral, positive, negative, dramatic, special
- **Custom-only filter**: Chỉ hiện custom emotions
- **Live statistics**: Hiển thị số lượng emotions theo loại

### 📤 Import/Export
- **Export config** thành JSON file
- **Import config** từ file có sẵn
- **Backup/restore** toàn bộ emotion settings

## 🏗️ Cấu trúc Table

| Cột | Tên | Chức năng |
|-----|-----|-----------|
| 0 | 🎭 Emotion Name | Tên emotion (read-only) |
| 1 | 📝 Description | Mô tả emotion (editable cho custom) |
| 2 | 🏷️ Category | Category dropdown |
| 3 | 🎯 Exaggeration | SpinBox (0.0-2.5) |
| 4 | ⚖️ CFG Weight | SpinBox (0.0-1.0) |
| 5 | 🌡️ Temperature | SpinBox (0.1-1.5) |
| 6 | ⚡ Speed | SpinBox (0.5-2.0) |
| 7 | 🎵 Preview | Button + ProgressBar |
| 8 | 🗑️ Actions | Delete cho custom emotions |

## 🎮 Hướng dẫn sử dụng

### 1. Khởi chạy UI
```bash
python demo_table_emotion_ui.py
```

### 2. Tùy chỉnh Emotions
- **Chỉnh parameters**: Click trực tiếp vào spinbox/combobox trong table
- **Tự động lưu**: Thay đổi được lưu ngay lập tức
- **Visual feedback**: Status bar hiển thị kết quả

### 3. Preview Âm thanh
- **Click nút "🎵 Nghe"** để tạo preview
- **Progress bar** hiển thị tiến trình
- **Audio tự động phát** sau khi hoàn thành
- **Error handling** cho các trường hợp lỗi

### 4. Thêm Custom Emotion
- **Click "➕ Thêm Emotion"**
- **Điền form**: Tên, mô tả, category, parameters
- **Validation**: Kiểm tra tên trùng và thông tin hợp lệ
- **Auto-reload**: Table tự động cập nhật

### 5. Xóa Custom Emotion
- **Click nút "🗑️"** ở custom emotion
- **Confirmation dialog** để xác nhận
- **Safe delete**: Chỉ xóa được custom emotions

### 6. Filter & Search
- **Category filter**: Dropdown chọn category
- **Custom filter**: Checkbox "Chỉ hiện custom emotions"
- **Live filtering**: Kết quả hiển thị ngay lập tức

### 7. Import/Export
- **Export**: Click "📤 Export" → Chọn nơi lưu file JSON
- **Import**: Click "📥 Import" → Chọn file JSON
- **Backup**: Tự động tạo backup trước khi import

## 🎨 UI Components

### AudioPreviewThread
- **Background processing** cho TTS generation
- **Signal/slot communication** với UI
- **Error handling** và cleanup

### Table Widgets
- **QDoubleSpinBox**: Cho parameters có decimal
- **QComboBox**: Cho category selection  
- **QProgressBar**: Cho preview progress
- **Custom styling**: Theo Voice Studio theme

### Color Scheme
```css
Custom Emotions: #E8F5E8 (Light Green)
Default Emotions: #F0F8FF (Light Blue)
Preview Button: #5856D6 (Purple)
Add Button: #28CD41 (Green)
Delete Button: #FF3B30 (Red)
```

## 📝 Technical Implementation

### Files Modified
- `src/ui/emotion_config_tab.py` - Main UI implementation
- `demo_table_emotion_ui.py` - Demo script

### Key Features
- **Singleton TTS Provider**: Prevent multiple instances
- **Thread-safe Preview**: Background audio generation
- **Responsive Layout**: Auto-resize columns
- **Error Recovery**: Graceful fallbacks

### Memory Management
- **Thread cleanup**: Automatic cleanup sau preview
- **Widget reuse**: Efficient table cell widgets
- **Signal disconnection**: Prevent memory leaks

## 🐛 Troubleshooting

### TTS Preview Không hoạt động
- **Check TTS provider**: Cần Real Chatterbox được setup
- **GPU Memory**: Cần đủ VRAM cho TTS model
- **Fallback mode**: Sẽ hiển thị simulation dialog

### Table Performance
- **Large datasets**: Table handle được hàng trăm emotions
- **Memory usage**: Efficient widget reuse
- **Responsive**: Smooth scrolling và filtering

### Import/Export Issues
- **File format**: Chỉ hỗ trợ JSON format
- **Validation**: Auto-validate trước khi import
- **Backup**: Tự động backup trước modifications

## 🎯 Kết luận

UI emotion configuration mới với **table format** mang lại:

✅ **Trải nghiệm tốt hơn** - Giống character settings table  
✅ **Preview thật** - Nghe âm thanh emotions  
✅ **Quản lý dễ dàng** - Thêm/xóa/edit trực tiếp  
✅ **Professional UI** - Responsive và modern  
✅ **Error-free** - Robust error handling  

Thiết kế này hoàn toàn thay thế UI compact cũ và mang lại workflow tự nhiên hơn cho users! 🎊 