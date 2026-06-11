@echo off
echo ====================================
echo Khoi dong Frontend (React + Vite)
echo ====================================
echo.

cd frontend

REM Kiem tra file .env
if not exist ".env" (
    echo Tao file .env tu .env.example...
    copy .env.example .env
)

REM Kiem tra node_modules
if not exist "node_modules" (
    echo Cai dat npm dependencies...
    npm install
)

echo.
echo ====================================
echo Frontend dang chay tai: http://localhost:5173
echo ====================================
echo.

REM Chay frontend
npm run dev
