@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo === TCP Server APK Build Script (Direct) ===
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not installed or not available
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python detected, preparing build dependencies...
echo.

REM Check required files
if not exist "main.py" (
    echo Error: main.py file not found
    echo Please run this script in tcp_apk directory
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo Error: buildozer.spec file not found
    echo Please run this script in tcp_apk directory
    pause
    exit /b 1
)

echo Installing buildozer and dependencies...
echo Note: This may take several minutes
echo.

REM Install buildozer
pip install buildozer cython
if %errorlevel% neq 0 (
    echo Warning: buildozer installation may fail on Windows
    echo buildozer is primarily designed for Linux environments
    echo.
)

echo.
echo === Build Options ===
echo Due to buildozer limitations on Windows, recommend alternatives:
echo.
echo 1. Use GitHub Actions online build (Recommended)
echo 2. Use Docker container build
echo 3. Use Linux virtual machine
echo 4. Use current Kivy app for development/testing
echo.
echo Current Kivy app is working and ready for development
echo For APK files, please use the alternative methods above
echo.
pause