@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo === 游戏组队服务器 APK 编译脚本 (Windows) ===
echo.

REM 检查WSL是否可用
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: WSL未安装或不可用
    echo 请安装WSL2和Ubuntu，然后重试
    echo 安装指南: https://docs.microsoft.com/zh-cn/windows/wsl/install
    pause
    exit /b 1
)

echo 检测到WSL，准备在Linux环境中编译APK...
echo.

REM 获取当前目录的WSL路径
for /f "tokens=*" %%i in ('wsl pwd') do set WSL_PWD=%%i
echo 当前WSL路径: %WSL_PWD%
echo.

REM 检查必要文件
if not exist "main.py" (
    echo 错误: 未找到main.py文件
    echo 请确保在tcp_apk目录下运行此脚本
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo 错误: 未找到buildozer.spec文件
    echo 请确保在tcp_apk目录下运行此脚本
    pause
    exit /b 1
)

echo 准备编译环境...
echo.

REM 在WSL中安装依赖和编译
wsl bash -c "
set -e
echo '安装系统依赖...'
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

echo '安装Python依赖...'
pip3 install --user buildozer cython kivy

echo '开始编译APK...'
echo '注意: 首次编译可能需要30-60分钟下载依赖'
buildozer android debug

echo '编译完成!'
if [ -f bin/*.apk ]; then
    echo 'APK文件:'
    ls -la bin/*.apk
else
    echo '警告: 未找到APK文件'
fi
"

if %errorlevel% equ 0 (
    echo.
    echo === 编译成功! ===
    echo APK文件已生成在 bin\ 目录下
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