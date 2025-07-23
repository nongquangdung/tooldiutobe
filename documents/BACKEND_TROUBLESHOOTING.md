# 🛠️ BACKEND TROUBLESHOOTING GUIDE

## Vấn đề hiện tại
Frontend UI đang hoạt động hoàn hảo nhưng backend server không start được, dẫn đến lỗi:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
:8000/api/system/status
```

## ✅ Giải pháp đã áp dụng
Frontend đã được update với **Mock Mode** để user vẫn có thể:
- Test toàn bộ UI interface
- Xem voice selection working
- Test progress tracking
- Verify audio player functionality

## 🔧 Cách fix Backend Server

### Method 1: Quick Start
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Check Dependencies
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Debug Mode
```bash
cd backend
python app/main.py
# Xem error messages cụ thể
```

### Method 4: Alternative Port
Nếu port 8000 bị conflict:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Sau đó update `web/src/api/voice-api.ts` line với port mới.

## 🐛 Common Issues

### Issue 1: Port Already in Use
```
ERROR: [Errno 10048] only one usage of each socket address is normally permitted
```
**Solution:** Kill existing processes:
```bash
netstat -ano | findstr :8000
# Kill process by PID
taskkill /PID [PID_NUMBER] /F
```

### Issue 2: Python Dependencies Missing
```
ImportError: No module named 'fastapi'
```
**Solution:**
```bash
pip install fastapi uvicorn[standard]
pip install -r requirements.txt
```

### Issue 3: ChatterboxTTS Issues
```
TTS imports failed: ...
```
**Solution:** Backend sẽ chạy trong mock mode, vẫn functional.

## 🎯 Current Status

✅ **Working:**
- Frontend UI hoàn chỉnh
- Mock mode với 6 voices
- Progress tracking simulation
- Audio player interface
- Voice selection dropdown

❌ **Not Working:**
- Backend TTS server
- Real audio generation
- API endpoints

## 🚀 Next Steps

1. **Immediate:** User có thể test toàn bộ UI với mock mode
2. **Backend Fix:** Troubleshoot Python environment
3. **Production:** Deploy backend to cloud service
4. **Alternative:** Use WebRTC/Browser-based TTS as fallback

## 📝 Frontend Changes Made

File: `web/src/components/VoiceStudioV2Simple.tsx`
- Added `mockMode` state
- Mock voice data when API fails
- Simulated progress animation
- Clear error messages
- Troubleshooting instructions

## 💡 User Experience

Hiện tại user sẽ thấy:
- Orange status: "error - using mock mode"
- Mock warning banner
- Full UI functionality
- Clear instructions để fix backend
- 6 mock voices available

User có thể test toàn bộ interface ngay bây giờ! 🎉 