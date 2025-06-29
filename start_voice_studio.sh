#!/bin/bash

# 🚀 Voice Studio Web V2.0 - Auto Start Script
# Tự động khởi chạy backend và frontend

echo "🎵 ==================================="
echo "🎵  Voice Studio Web V2.0 Launcher"
echo "🎵 ==================================="
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không tìm thấy. Vui lòng cài đặt Python 3.8+"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Kiểm tra thư mục
if [ ! -d "chatterbox-web-reference" ]; then
    echo "❌ Thư mục chatterbox-web-reference không tồn tại!"
    echo "💡 Hãy chạy script này từ thư mục gốc của project"
    exit 1
fi

if [ ! -d "web-v2" ]; then
    echo "❌ Thư mục web-v2 không tồn tại!"
    echo "💡 Hãy chạy script này từ thư mục gốc của project"
    exit 1
fi

# Tạo môi trường ảo nếu chưa có
echo "🔧 Kiểm tra môi trường Python..."
cd chatterbox-web-reference

if [ ! -d "chatterbox_env" ]; then
    echo "📦 Tạo môi trường ảo Python..."
    python3 -m venv chatterbox_env
    echo "✅ Đã tạo môi trường ảo"
fi

# Kích hoạt môi trường ảo
echo "🔄 Kích hoạt môi trường ảo..."
source chatterbox_env/bin/activate

# Cài đặt dependencies nếu cần
echo "📥 Kiểm tra dependencies..."
if ! pip show torch &> /dev/null; then
    echo "📦 Cài đặt dependencies (có thể mất vài phút)..."
    pip install -r requirements.txt
    echo "✅ Đã cài đặt dependencies"
else
    echo "✅ Dependencies đã có sẵn"
fi

# Download models nếu cần
echo "🤖 Kiểm tra AI models..."
if [ ! -d "voices" ] || [ -z "$(ls -A voices 2>/dev/null)" ]; then
    echo "📥 Download AI models (có thể mất 10-15 phút)..."
    python download_model.py
    echo "✅ Đã download models"
else
    echo "✅ AI models đã có sẵn"
fi

echo ""
echo "🎯 =================================="
echo "🎯  Khởi chạy Voice Studio Web V2.0"
echo "🎯 =================================="
echo ""

# Khởi chạy backend trong background
echo "🚀 Khởi chạy Backend (Chatterbox-TTS-Server)..."
echo "📡 Backend sẽ chạy tại: http://localhost:8005"
nohup python server.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend PID: $BACKEND_PID"

# Chờ backend khởi động
echo "⏱️  Chờ backend khởi động (10 giây)..."
sleep 10

# Kiểm tra backend có chạy không
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend đã khởi động thành công!"
else
    echo "❌ Backend không khởi động được. Kiểm tra backend.log"
    exit 1
fi

# Quay về thư mục gốc
cd ..

# Khởi chạy frontend
echo ""
echo "🎨 Khởi chạy Frontend (Web V2.0)..."
echo "🌐 Frontend sẽ chạy tại: http://localhost:8080"
cd web-v2

# Khởi chạy web server trong background
nohup python3 -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend PID: $FRONTEND_PID"

# Chờ frontend khởi động
sleep 3

# Quay về thư mục gốc
cd ..

echo ""
echo "🎉 =================================="
echo "🎉  Voice Studio Web V2.0 READY!"
echo "🎉 =================================="
echo ""
echo "🌐 Frontend: http://localhost:8080"
echo "📡 Backend:  http://localhost:8005"
echo "🎬 Demo:     http://localhost:8080/demo-test.html"
echo ""
echo "📊 Process IDs:"
echo "   Backend PID:  $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   Backend:  backend.log"
echo "   Frontend: frontend.log"
echo ""
echo "🛑 Để dừng servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Mở trình duyệt tự động (nếu có)
if command -v open &> /dev/null; then
    echo "🔗 Mở trình duyệt tự động..."
    sleep 2
    open http://localhost:8080
elif command -v xdg-open &> /dev/null; then
    echo "🔗 Mở trình duyệt tự động..."
    sleep 2
    xdg-open http://localhost:8080
fi

echo "🎵 Happy Voice Generation! ✨"
echo ""
echo "💡 Tips:"
echo "   - Test với demo-test.html để kiểm tra tất cả features"
echo "   - Sử dụng Developer Tools (F12) để debug"
echo "   - Restart nếu gặp vấn đề: kill $BACKEND_PID $FRONTEND_PID"
echo "" 