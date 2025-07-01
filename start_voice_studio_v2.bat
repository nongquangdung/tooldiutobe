@echo off
echo ============================================
echo    🎵 VOICE STUDIO V2 - KHỞI ĐỘNG DEBUG
echo ============================================
echo.

echo 📡 Khởi động Backend API (Port 8000)...
start "Voice Studio Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Đợi backend khởi động...
timeout /t 5 /nobreak >nul

echo 🌐 Khởi động Frontend UI (Port 5173)...
start "Voice Studio Frontend" cmd /k "cd web && npm run dev"

echo ⏳ Đợi frontend khởi động...
timeout /t 5 /nobreak >nul

echo.
echo ✅ KHỞI ĐỘNG HOÀN TẤT!
echo.
echo 🔗 Các URL quan trọng:
echo    Frontend UI: http://localhost:5173
echo    Backend API: http://localhost:8000
echo    API Docs:    http://localhost:8000/docs
echo.
echo 🐛 DEBUG MODE:
echo    - UI hiện đang chạy với VoiceStudioV2Simple component
echo    - Sẽ hiển thị API status và available voices
echo    - Check browser console để xem chi tiết
echo.
echo 📝 Troubleshooting:
echo    - Nếu UI trắng: Check console.log trong browser
echo    - Nếu Backend lỗi: Check Backend terminal window
echo    - Nếu API không connect: Đảm bảo cả 2 server đang chạy
echo.
echo 💡 Next Steps:
echo    - Test với Simple UI trước
echo    - Nếu OK, switch back sang VoiceStudioV2 full
echo    - Import VoiceStudioV2 trong App.tsx thay vì VoiceStudioV2Simple
echo.
pause 