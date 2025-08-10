@echo off
chcp 65001 >nul
echo ========================================
echo TCP Server - GitHub Upload Script
echo ========================================
echo.

echo Step 1: Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please download and install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git is installed
echo.

echo Step 2: Initialize git repository
if not exist ".git" (
    git init
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already exists
)
echo.

echo Step 3: Add all files
git add .
echo ✓ Files added to git
echo.

echo Step 4: Create commit
git commit -m "TCP Server Android App - Ready for APK compilation"
echo ✓ Commit created
echo.

echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Repository name: tcp-server-android
echo    Make it PUBLIC (for free Actions)
echo.
echo 3. Copy the repository URL and run:
echo    git remote add origin YOUR_REPO_URL
echo    git push -u origin main
echo.
echo 4. GitHub will automatically compile APK!
echo    Check Actions tab after upload.
echo.
echo ========================================
echo Current directory ready for upload!
echo ========================================
pause