#!/bin/bash

# 🛑 Voice Studio Web V2.0 - Stop Script
# Dừng tất cả services một cách an toàn

echo "🛑 ==================================="
echo "🛑  Voice Studio Web V2.0 Stopper"
echo "🛑 ==================================="
echo ""

# Tìm và dừng tất cả processes liên quan
echo "🔍 Tìm các processes đang chạy..."

# Tìm backend process (Chatterbox server)
BACKEND_PIDS=$(pgrep -f "python.*server.py" || true)
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "📡 Tìm thấy Backend processes: $BACKEND_PIDS"
    for pid in $BACKEND_PIDS; do
        echo "🛑 Dừng Backend PID: $pid"
        kill $pid 2>/dev/null || true
    done
else
    echo "📡 Không tìm thấy Backend processes"
fi

# Tìm frontend process (HTTP server)
FRONTEND_PIDS=$(pgrep -f "python.*http.server.*8080" || true)
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "🌐 Tìm thấy Frontend processes: $FRONTEND_PIDS"
    for pid in $FRONTEND_PIDS; do
        echo "🛑 Dừng Frontend PID: $pid"
        kill $pid 2>/dev/null || true
    done
else
    echo "🌐 Không tìm thấy Frontend processes"
fi

# Tìm các processes khác có thể liên quan
OTHER_PIDS=$(pgrep -f "voice.*studio" || true)
if [ ! -z "$OTHER_PIDS" ]; then
    echo "🔧 Tìm thấy processes khác: $OTHER_PIDS"
    for pid in $OTHER_PIDS; do
        echo "🛑 Dừng process PID: $pid"
        kill $pid 2>/dev/null || true
    done
fi

echo ""
echo "⏱️  Chờ processes dừng hoàn toàn (5 giây)..."
sleep 5

# Kiểm tra lại và force kill nếu cần
echo "🔍 Kiểm tra lại các processes..."

REMAINING_BACKEND=$(pgrep -f "python.*server.py" || true)
if [ ! -z "$REMAINING_BACKEND" ]; then
    echo "⚠️  Backend vẫn chạy, force kill: $REMAINING_BACKEND"
    for pid in $REMAINING_BACKEND; do
        kill -9 $pid 2>/dev/null || true
    done
fi

REMAINING_FRONTEND=$(pgrep -f "python.*http.server.*8080" || true)
if [ ! -z "$REMAINING_FRONTEND" ]; then
    echo "⚠️  Frontend vẫn chạy, force kill: $REMAINING_FRONTEND"
    for pid in $REMAINING_FRONTEND; do
        kill -9 $pid 2>/dev/null || true
    done
fi

# Xóa log files
echo ""
echo "🧹 Dọn dẹp log files..."
if [ -f "backend.log" ]; then
    rm backend.log
    echo "🗑️  Đã xóa backend.log"
fi

if [ -f "frontend.log" ]; then
    rm frontend.log
    echo "🗑️  Đã xóa frontend.log"
fi

# Kiểm tra port còn bị chiếm không
echo ""
echo "🔍 Kiểm tra ports..."

PORT_8005=$(lsof -ti:8005 || true)
if [ ! -z "$PORT_8005" ]; then
    echo "⚠️  Port 8005 vẫn bị chiếm bởi PID: $PORT_8005"
    kill -9 $PORT_8005 2>/dev/null || true
fi

PORT_8080=$(lsof -ti:8080 || true)
if [ ! -z "$PORT_8080" ]; then
    echo "⚠️  Port 8080 vẫn bị chiếm bởi PID: $PORT_8080"
    kill -9 $PORT_8080 2>/dev/null || true
fi

echo ""
echo "✅ ==================================="
echo "✅  Voice Studio Web V2.0 STOPPED!"
echo "✅ ==================================="
echo ""
echo "🔄 Để khởi chạy lại:"
echo "   ./start_voice_studio.sh"
echo ""
echo "🔍 Để kiểm tra processes:"
echo "   ps aux | grep -E '(server.py|http.server)'"
echo ""
echo "🌐 Để kiểm tra ports:"
echo "   lsof -i:8005  # Backend"
echo "   lsof -i:8080  # Frontend"
echo ""

echo "🎵 Services đã dừng thành công! ✨" 