@echo off
title CampusBot - College AI Chatbot Project
color 0b

echo ========================================================
echo         CampusBot - College AI Assistant Website
echo ========================================================
echo.

:: Detect Python executable
set PYTHON_EXE=
if exist "C:\ProgramData\anaconda3\python.exe" (
    set "PYTHON_EXE=C:\ProgramData\anaconda3\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=python"
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python was not detected on your system.
    echo Please install Python or Anaconda to run the project.
    pause
    exit /b 1
)

echo [OK] Using Python: %PYTHON_EXE%
echo [INFO] Starting Flask Server...
echo [INFO] Once started, open your web browser and navigate to:
echo.
echo        http://127.0.0.1:5000
echo.
echo Press Ctrl+C in this terminal window to stop the server anytime.
echo ========================================================
echo.

"%PYTHON_EXE%" app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The server terminated with an error.
    pause
)
