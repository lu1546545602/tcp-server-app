#!/bin/bash

# 游戏组队服务器 - 安卓APK编译脚本
# 使用方法: ./build.sh [debug|release]

set -e

BUILD_TYPE=${1:-debug}

echo "=== 游戏组队服务器 APK 编译脚本 ==="
echo "编译类型: $BUILD_TYPE"
echo

# 检查是否在正确的目录
if [ ! -f "main.py" ] || [ ! -f "buildozer.spec" ]; then
    echo "错误: 请在tcp_apk目录下运行此脚本"
    exit 1
fi

# 检查buildozer是否安装
if ! command -v buildozer &> /dev/null; then
    echo "错误: buildozer未安装"
    echo "请运行: pip install buildozer"
    exit 1
fi

# 检查Python依赖
echo "检查Python依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 清理之前的构建（可选）
read -p "是否清理之前的构建缓存? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "清理构建缓存..."
    buildozer android clean
fi

# 开始编译
echo "开始编译APK..."
echo "注意: 首次编译可能需要较长时间下载依赖"
echo

if [ "$BUILD_TYPE" = "release" ]; then
    echo "编译发布版本..."
    buildozer android release
else
    echo "编译调试版本..."
    buildozer android debug
fi

# 检查编译结果
if [ $? -eq 0 ]; then
    echo
    echo "=== 编译成功! ==="
    echo "APK文件位置:"
    ls -la bin/*.apk 2>/dev/null || echo "未找到APK文件"
    echo
    echo "安装说明:"
    echo "1. 将APK文件传输到安卓设备"
    echo "2. 在设备上启用'未知来源'应用安装"
    echo "3. 安装APK文件"
    echo "4. 启动应用并配置服务器"
else
    echo
    echo "=== 编译失败! ==="
    echo "请检查错误信息并解决问题后重试"
    exit 1
fi