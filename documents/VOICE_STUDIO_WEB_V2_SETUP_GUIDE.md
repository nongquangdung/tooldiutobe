# 🚀 Voice Studio Web V2.0 - Hướng Dẫn Khởi Chạy

## 📋 Tổng quan
Voice Studio Web V2.0 bao gồm:
- **Backend**: Chatterbox-TTS-Server (cổng 8005)
- **Frontend**: Web interface với tất cả advanced features (cổng 8080)

## 🔧 Yêu cầu hệ thống
- **Python**: 3.8+ (khuyến nghị 3.10+)
- **Node.js**: 16+ (nếu dùng build tools)
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB+)
- **GPU**: NVIDIA GPU với CUDA support (tùy chọn, để tăng tốc)

---

## 🎯 BƯỚC 1: Setup Backend (Chatterbox-TTS-Server)

### 1.1 Di chuyển vào thư mục backend
```bash
cd chatterbox-web-reference
```

### 1.2 Tạo môi trường ảo Python
```bash
# macOS/Linux
python3 -m venv chatterbox_env
source chatterbox_env/bin/activate

# Windows
python -m venv chatterbox_env
chatterbox_env\Scripts\activate
```

### 1.3 Cài đặt dependencies
```bash
# Cơ bản (CPU only)
pip install -r requirements.txt

# Nếu có NVIDIA GPU
pip install -r requirements-nvidia.txt

# Nếu có AMD GPU (ROCm)
pip install -r requirements-rocm.txt
```

### 1.4 Download models (lần đầu tiên)
```bash
python download_model.py
```

### 1.5 Khởi chạy backend server
```bash
python server.py
```

**✅ Backend sẽ chạy tại:** `http://localhost:8005`

---

## 🎨 BƯỚC 2: Setup Frontend (Web V2.0)

### 2.1 Mở terminal mới (giữ backend chạy)
```bash
# Di chuyển về thư mục gốc
cd ..
```

### 2.2 Di chuyển vào thư mục web-v2
```bash
cd web-v2
```

### 2.3 Khởi chạy web server
```bash
# Phương pháp 1: Python HTTP Server (đơn giản)
python3 -m http.server 8080

# Phương pháp 2: Node.js HTTP Server (nếu có Node.js)
npx http-server -p 8080 -c-1

# Phương pháp 3: Live Server (VS Code extension)
# Chuột phải -> "Open with Live Server"
```

**✅ Frontend sẽ chạy tại:** `http://localhost:8080`

---

## 🔍 BƯỚC 3: Kiểm tra kết nối

### 3.1 Mở trình duyệt
Truy cập: `http://localhost:8080`

### 3.2 Kiểm tra backend connection
- Mở Developer Tools (F12)
- Vào tab Console
- Không có lỗi màu đỏ = thành công kết nối

### 3.3 Test cơ bản
1. Nhập text: "Hello, this is Voice Studio Web V2.0"
2. Chọn voice từ dropdown
3. Click "Generate"
4. Nếu có audio player xuất hiện = thành công!

---

## 🎛️ BƯỚC 4: Test Advanced Features

### 4.1 Test Emotion System
```
1. Chuyển sang tab "Emotion Control"
2. Chọn emotion preset (Happy, Sad, Excited, etc.)
3. Adjust sliders: Exaggeration, Temperature, Speed
4. Generate audio với text: "I am feeling this emotion now"
```

### 4.2 Test Character Mapping
```
1. Chuyển sang tab "Character Mapping"
2. Add character: Name="Alice", Voice="female-voice-1"
3. Input text: "Alice: Hello there! How are you today?"
4. System sẽ tự động detect và apply voice cho Alice
```

### 4.3 Test Inner Voice Effects
```
1. Chuyển sang tab "Inner Voice Effects"
2. Chọn effect: Light/Deep/Dreamy
3. Input text với format: "(thinking: This is my inner voice)"
4. Generate và nghe sự khác biệt
```

### 4.4 Test Analytics System
```
1. Generate vài audio samples
2. Chuyển sang tab "Analytics"
3. View session metrics
4. Export data bằng "Export Analytics"
```

---

## 🐋 BƯỚC 5: Chạy bằng Docker (Tùy chọn)

### 5.1 Backend với Docker
```bash
cd chatterbox-web-reference
docker-compose up -d
```

### 5.2 Frontend với Docker
```bash
# Tạo Dockerfile cho web-v2
cat > web-v2/Dockerfile << EOF
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
EOF

# Build và chạy
cd web-v2
docker build -t voice-studio-web-v2 .
docker run -d -p 8080:80 voice-studio-web-v2
```

---

## 🛠️ Troubleshooting

### ❌ Backend không khởi động
```bash
# Kiểm tra Python version
python --version  # Cần >= 3.8

# Kiểm tra pip packages
pip list | grep torch

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### ❌ Frontend không load
```bash
# Kiểm tra port đã được sử dụng chưa
lsof -i :8080  # macOS/Linux
netstat -an | find "8080"  # Windows

# Thử port khác
python3 -m http.server 8081
```

### ❌ CORS errors
```javascript
// Thêm vào đầu file voice-studio-config.js
window.VOICE_STUDIO_CONFIG.api.headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};
```

### ❌ Audio không play
- Kiểm tra browser support: Chrome/Firefox/Safari
- Enable audio autoplay trong browser settings
- Test với headphones nếu có vấn đề về speakers

---

## 📱 Mobile Testing

### Truy cập từ điện thoại:
1. Tìm IP address của máy tính:
   ```bash
   # macOS/Linux
   ifconfig | grep inet
   
   # Windows
   ipconfig
   ```

2. Truy cập từ phone: `http://[YOUR_IP]:8080`
3. Test touch controls và responsive design

---

## 🎉 Demo Test Suite

### Chạy comprehensive test:
```bash
# Mở: http://localhost:8080/demo-test.html
```

Demo này sẽ test tất cả features:
- ✅ 28 predefined voices
- ✅ 8 emotion presets
- ✅ 3 inner voice effects
- ✅ Character mapping với auto-detection
- ✅ Analytics tracking
- ✅ Project save/load
- ✅ Mobile responsiveness

---

## 📊 Performance Optimization

### Backend optimization:
```bash
# Sử dụng GPU nếu có
export CUDA_VISIBLE_DEVICES=0

# Tăng số threads
export OMP_NUM_THREADS=4
```

### Frontend optimization:
- Enable browser caching
- Use CDN cho external libraries
- Minify CSS/JS files cho production

---

## 🔒 Security Notes

- **Development**: Chỉ chạy localhost
- **Production**: 
  - Use HTTPS
  - Set proper CORS headers
  - Add rate limiting
  - Use authentication nếu cần

---

## 📞 Support

Nếu gặp vấn đề:
1. Check console logs (F12)
2. Check backend logs trong terminal
3. Restart cả backend và frontend
4. Clear browser cache và cookies

**Happy Voice Generation! 🎵✨** 