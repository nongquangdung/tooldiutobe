# ⚡ Voice Studio Web V2.0 - Quick Start

## 🚀 Khởi chạy siêu nhanh (1 lệnh)

```bash
./start_voice_studio.sh
```

**✅ Xong! Web sẽ tự động mở tại:** `http://localhost:8080`

---

## 🛑 Dừng services

```bash
./stop_voice_studio.sh
```

---

## 📋 Khởi chạy thủ công (nếu script không hoạt động)

### Bước 1: Backend
```bash
cd chatterbox-web-reference
python3 -m venv chatterbox_env
source chatterbox_env/bin/activate
pip install -r requirements.txt
python download_model.py  # Chỉ lần đầu
python server.py
```
**Backend chạy tại:** `http://localhost:8005`

### Bước 2: Frontend (terminal mới)
```bash
cd web-v2
python3 -m http.server 8080
```
**Frontend chạy tại:** `http://localhost:8080`

---

## 🎯 Test Features

1. **Basic TTS:** 
   - Nhập text → Chọn voice → Generate
   
2. **Emotion System:**
   - Tab "Emotion Control" → Chọn preset → Adjust sliders
   
3. **Character Mapping:** 
   - Tab "Character Mapping" → Add character → Test dialogue
   
4. **Inner Voice Effects:**
   - Tab "Inner Voice Effects" → Chọn effect → Test "(thinking: ...)"
   
5. **Full Demo:**
   - Truy cập: `http://localhost:8080/demo-test.html`

---

## 🔧 Troubleshooting

### ❌ Lỗi phổ biến:

**Backend không chạy:**
```bash
# Kiểm tra Python
python3 --version  # Cần >= 3.8

# Reinstall
pip install --upgrade -r requirements.txt
```

**Frontend không load:**
```bash
# Thử port khác
python3 -m http.server 8081
```

**Audio không play:**
- Dùng Chrome/Firefox/Safari
- Enable audio autoplay
- Test với headphones

---

## 📱 Mobile Access

1. Tìm IP máy tính:
   ```bash
   ifconfig | grep inet  # macOS/Linux
   ipconfig             # Windows
   ```

2. Truy cập từ phone: `http://[YOUR_IP]:8080`

---

## 🎵 Tính năng chính

- ✅ **28 AI Voices**: Nam/nữ chất lượng cao
- ✅ **8 Emotion Presets**: Happy, Sad, Excited, etc.
- ✅ **3 Inner Voice Effects**: Light, Deep, Dreamy
- ✅ **Character Mapping**: Multi-character dialogue
- ✅ **Analytics System**: Session tracking & export
- ✅ **Voice Cloning**: Upload và clone giọng nói
- ✅ **Mobile Friendly**: Responsive design
- ✅ **Real-time Processing**: Instant audio generation

---

## 📞 Support

**Files quan trọng:**
- `VOICE_STUDIO_WEB_V2_SETUP_GUIDE.md` - Hướng dẫn chi tiết
- `web-v2/README.md` - Technical documentation
- `backend.log` & `frontend.log` - Debug logs

**Quick commands:**
```bash
# Khởi chạy
./start_voice_studio.sh

# Dừng
./stop_voice_studio.sh

# Kiểm tra processes
ps aux | grep -E '(server.py|http.server)'

# Kiểm tra ports
lsof -i:8005  # Backend
lsof -i:8080  # Frontend
```

**🎉 Happy Voice Generation! ✨** 