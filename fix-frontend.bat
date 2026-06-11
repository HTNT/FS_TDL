@echo off
echo ====================================
echo Fix loi Frontend TypeScript/VS Code
echo ====================================
echo.

cd frontend

echo [1/3] Dang cai dat dependencies...
call npm install

echo.
echo [2/3] Dang tao cau hinh VS Code...
if not exist ".vscode" mkdir .vscode

echo { > .vscode\settings.json
echo   "typescript.tsdk": "node_modules/typescript/lib", >> .vscode\settings.json
echo   "typescript.enablePromptUseWorkspaceTsdk": true >> .vscode\settings.json
echo } >> .vscode\settings.json

echo.
echo [3/3] Kiem tra TypeScript config...
type tsconfig.json | find "baseUrl" >nul
if errorlevel 1 (
    echo   [!] Canh bao: tsconfig.json co the chua dung
) else (
    echo   [OK] tsconfig.json hop le
)

echo.
echo ====================================
echo HOAN TAT!
echo ====================================
echo.
echo Cac buoc tiep theo trong VS Code:
echo 1. Ctrl + Shift + P
echo 2. Go: "TypeScript: Restart TS Server"
echo 3. Ctrl + Shift + P
echo 4. Go: "Developer: Reload Window"
echo.
echo Neu van loi, xem huong dan: FIX-VSCODE-ERRORS.md
echo.
pause
