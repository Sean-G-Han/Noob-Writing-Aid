@echo off
echo Launching Noob Writing Aid Development Environment...

start cmd /k "cd backend && .venv\Scripts\activate && uvicorn main:app --reload --port 8000"

start cmd /k "cd frontend && npm run dev"

echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
pause