@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo === 游戏组队服务器 APK Docker编译脚本 ===
echo.

REM 检查Docker是否可用
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker未安装或不可用
    echo 请安装Docker Desktop，然后重试
    echo 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo 检测到Docker，准备构建编译环境...
echo.

REM 检查必要文件
if not exist "main.py" (
    echo 错误: 未找到main.py文件
    echo 请确保在tcp_apk目录下运行此脚本
    pause
    exit /b 1
)

if not exist "Dockerfile" (
    echo 错误: 未找到Dockerfile文件
    echo 请确保在tcp_apk目录下运行此脚本
    pause
    exit /b 1
)

echo 构建Docker镜像...
echo 注意: 首次构建可能需要10-20分钟下载依赖
echo.

docker build -t tcp-server-builder .
if %errorlevel% neq 0 (
    echo 错误: Docker镜像构建失败
    pause
    exit /b 1
)

echo.
echo Docker镜像构建成功！
echo 开始编译APK...
echo 注意: 编译过程可能需要30-60分钟
echo.

REM 创建输出目录
if not exist "bin" mkdir bin

REM 运行Docker容器编译APK
docker run --rm -v "%cd%\bin:/app/bin" tcp-server-builder

if %errorlevel% equ 0 (
    echo.
    echo === 编译成功! ===
    echo APK文件已生成在 bin\ 目录下
    dir bin\*.apk
    echo.
    echo 后续步骤:
    echo 1. 将APK文件传输到安卓设备
    echo 2. 在设备上启用"未知来源"应用安装
    echo 3. 安装APK文件
    echo 4. 启动应用并配置服务器
) else (
    echo.
    echo === 编译失败! ===
    echo 请检查错误信息并解决问题后重试
)

echo.
pause