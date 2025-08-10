@echo off
chcp 65001 >nul
echo ========================================
echo 修复GitHub推送问题
echo ========================================
echo.

echo 当前状态: 错误的远程仓库已移除
echo.

echo 请按照以下步骤操作:
echo.
echo 第1步: 创建GitHub仓库
echo ----------------------------------------
echo 1. 打开浏览器访问: https://github.com/new
echo 2. Repository name: tcp-server-android
echo 3. 设置为 Public (重要!)
echo 4. 点击 "Create repository"
echo.

echo 正在为您打开GitHub...
start https://github.com/new
echo.

echo 第2步: 获取您的GitHub用户名
echo ----------------------------------------
set /p username="请输入您的GitHub用户名: "

if "%username%"=="" (
    echo 错误: 用户名不能为空
    pause
    exit /b 1
)

echo.
echo 第3步: 添加正确的远程仓库
echo ----------------------------------------
echo 执行命令: git remote add origin https://github.com/%username%/tcp-server-android.git
git remote add origin https://github.com/%username%/tcp-server-android.git

if errorlevel 1 (
    echo 警告: 添加远程仓库可能失败
    echo 请确认仓库地址正确
) else (
    echo ✓ 远程仓库添加成功
)

echo.
echo 第4步: 验证远程仓库
echo ----------------------------------------
git remote -v
echo.

echo 第5步: 推送代码
echo ----------------------------------------
echo 注意: 如果出现认证对话框，请输入您的GitHub凭据
echo 用户名: %username%
echo 密码: 您的GitHub密码或Personal Access Token
echo.
echo 开始推送...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo 推送失败 - 可能的解决方案:
    echo ========================================
    echo.
    echo 1. 确认GitHub仓库已创建:
    echo    https://github.com/%username%/tcp-server-android
    echo.
    echo 2. 检查认证信息:
    echo    - 用户名: %username%
    echo    - 密码: GitHub密码或Token
    echo.
    echo 3. 使用Personal Access Token:
    echo    - 访问: https://github.com/settings/tokens
    echo    - 生成新token
    echo    - 用token替代密码
    echo.
    echo 4. 手动重试:
    echo    git push -u origin main
    echo.
) else (
    echo.
    echo ========================================
    echo 🎉 推送成功!
    echo ========================================
    echo.
    echo 下一步:
    echo 1. 访问: https://github.com/%username%/tcp-server-android
    echo 2. 点击 "Actions" 标签
    echo 3. 等待APK编译完成 (10-15分钟)
    echo 4. 下载编译好的APK文件
    echo.
    echo 正在打开您的仓库...
    start https://github.com/%username%/tcp-server-android
)

echo.
pause