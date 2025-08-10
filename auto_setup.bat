@echo off
chcp 65001 >nul
echo ========================================
echo TCP Server APK - Auto Setup Script
echo ========================================
echo.

echo [1/4] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git is ready
echo.

echo [2/4] Checking repository status...
if exist ".git" (
    echo ✓ Git repository exists
) else (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "TCP Server Android App - Ready for APK compilation"
    echo ✓ Repository initialized
)
echo.

echo [3/4] Opening GitHub in browser...
start https://github.com/new
echo ✓ GitHub opened in browser
echo.

echo [4/4] Preparing upload commands...
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. In the opened browser:
echo    - Repository name: tcp-server-android
echo    - Set as PUBLIC (important for free Actions)
echo    - Click "Create repository"
echo.
echo 2. Copy your GitHub username and paste below:
set /p username="Enter your GitHub username: "
echo.
echo 3. Copy and run these commands:
echo.
echo git remote add origin https://github.com/%username%/tcp-server-android.git
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
echo Auto-executing upload commands...
echo ========================================
echo.

if "%username%"=="" (
    echo Username not provided. Please run commands manually.
    pause
    exit /b 1
)

echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/tcp-server-android.git
if errorlevel 1 (
    echo Warning: Could not add remote. Please check username.
)

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
echo Note: You may need to enter your GitHub credentials
git push -u origin main
if errorlevel 1 (
    echo.
    echo Push failed. Please check:
    echo 1. GitHub repository exists
    echo 2. Username is correct
    echo 3. You have push permissions
    echo.
    echo Manual commands:
    echo git remote add origin https://github.com/%username%/tcp-server-android.git
    echo git branch -M main
    echo git push -u origin main
) else (
    echo.
    echo ========================================
    echo SUCCESS! Code uploaded to GitHub
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Go to: https://github.com/%username%/tcp-server-android
    echo 2. Click "Actions" tab
    echo 3. Wait for APK compilation (10-15 minutes)
    echo 4. Download APK from completed workflow
    echo.
    echo Opening repository in browser...
    start https://github.com/%username%/tcp-server-android
)

echo.
pause