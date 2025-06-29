#!/bin/bash

# 🔍 Voice Studio Web V2.0 - Status Checker

echo "🔍 =================================="
echo "🔍  Voice Studio Web V2.0 Status"
echo "🔍 =================================="
echo ""

# Check Backend
echo "📡 Checking Backend (port 8005)..."
if curl -s http://localhost:8005 > /dev/null; then
    echo "✅ Backend: RUNNING"
    BACKEND_INFO=$(curl -s http://localhost:8005 | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    echo "   Info: $BACKEND_INFO"
else
    echo "❌ Backend: NOT RUNNING"
fi

echo ""

# Check Frontend  
echo "🌐 Checking Frontend (port 8080)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 | grep -q "200"; then
    echo "✅ Frontend: RUNNING"
    echo "   URL: http://localhost:8080"
else
    echo "❌ Frontend: NOT RUNNING"
fi

echo ""

# Check Processes
echo "🔧 Running Processes:"
PYTHON_PROCS=$(ps aux | grep python | grep -v grep | wc -l | tr -d ' ')
HTTP_PROCS=$(ps aux | grep "http.server" | grep -v grep | wc -l | tr -d ' ')

echo "   Python processes: $PYTHON_PROCS"
echo "   HTTP server processes: $HTTP_PROCS"

echo ""

# URLs
echo "🔗 Quick Links:"
echo "   🏠 Main Interface: http://localhost:8080"
echo "   🎬 Demo Test: http://localhost:8080/demo-test.html"
echo "   📡 Backend API: http://localhost:8005"
echo "   ℹ️  Demo Info: http://localhost:8005/demo"

echo ""

# Test Backend API
echo "🧪 Quick Backend Test:"
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ Health endpoint working"
else
    echo "❌ Health endpoint not responding"
fi

if curl -s http://localhost:8005/v1/voices > /dev/null; then
    VOICE_COUNT=$(curl -s http://localhost:8005/v1/voices | grep -o '"total":[0-9]*' | cut -d':' -f2)
    echo "✅ Voices endpoint: $VOICE_COUNT voices available"
else
    echo "❌ Voices endpoint not responding"
fi

echo ""
echo "🎵 Voice Studio Web V2.0 Status Check Complete! ✨" 