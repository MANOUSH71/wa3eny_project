@echo off
REM Development startup script (Windows)

echo 🚀 Starting Aegis AI Development Environment...

REM Start backend
echo 📦 Starting FastAPI backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

REM Wait a bit
timeout /t 3 /nobreak > nul

REM Start frontend
echo 🌐 Starting frontend server...
start "Frontend" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo ✅ Development servers running:
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo    Frontend: http://localhost:8080
echo.
echo Close the command windows to stop servers
pause
