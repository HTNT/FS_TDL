@echo off
echo ====================================
echo Git Push to GitHub
echo ====================================
echo.

REM Kiem tra xem da co remote chua
git remote -v | find "origin" >nul
if errorlevel 1 (
    echo [!] Chua co remote origin!
    echo.
    echo Hay chay lenh sau voi thong tin cua ban:
    echo git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    pause
    exit /b 1
)

echo [1/3] Dang add files...
git add .

echo.
set /p commit_msg="Nhap commit message: "

echo.
echo [2/3] Dang commit...
git commit -m "%commit_msg%"

echo.
echo [3/3] Dang push len GitHub...
git push

echo.
echo ====================================
echo HOAN TAT!
echo ====================================
echo.
pause
