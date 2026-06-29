#!/bin/bash
# Development startup script (Mac/Linux)

echo "🚀 Starting Aegis AI Development Environment..."

# Start backend
echo "📦 Starting FastAPI backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo "🌐 Starting frontend server..."
cd ../frontend
python3 -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "✅ Development servers running:"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all servers"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# Wait
wait
