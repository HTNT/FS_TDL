@echo off
echo ====================================
echo Khoi dong Backend (FastAPI)
echo ====================================
echo.

cd backend

REM Kiem tra xem virtual environment da ton tai chua
if not exist "venv" (
    echo Tao virtual environment...
    python -m venv venv
)

REM Kich hoat virtual environment
echo Kich hoat virtual environment...
call venv\Scripts\activate.bat

REM Kiem tra file .env
if not exist ".env" (
    echo Tao file .env tu .env.example...
    copy .env.example .env
    echo.
    echo QUAN TRONG: Hay chinh sua file backend\.env voi thong tin database cua ban!
    echo.
    pause
)

REM Cai dat dependencies
echo Cai dat Python dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo Backend dang chay tai: http://localhost:8000
echo API Docs tai: http://localhost:8000/docs
echo ====================================
echo.

REM Chay backend
uvicorn app.main:app --reload
