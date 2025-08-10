@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    GitHub仓库名称修复工具
echo ========================================
echo.

echo [1/4] 检查Git状态...
git status
if errorlevel 1 (
    echo 错误: Git仓库未初始化
    pause
    exit /b 1
)

echo.
echo [2/4] 移除旧的远程仓库配置...
git remote remove origin 2>nul
echo 已清理旧配置

echo.
echo [3/4] 打开GitHub创建仓库页面...
start https://github.com/new
echo.
echo ========================================
echo 请在浏览器中创建新仓库:
echo.
echo 推荐仓库名称: tcp-server-app
echo 其他选项: tcp-server-mobile, xunqin-tcp-server
echo.
echo 设置:
echo - Repository name: tcp-server-app
echo - 选择 Public
echo - 不要勾选任何初始化选项
echo - 点击 "Create repository"
echo ========================================
echo.
set /p username="请输入您的GitHub用户名: "
if "%username%"=="" (
    echo 错误: 用户名不能为空
    pause
    exit /b 1
)

set /p reponame="请输入您创建的仓库名称 [默认: tcp-server-app]: "
if "%reponame%"=="" set reponame=tcp-server-app

echo.
echo [4/4] 配置新的远程仓库...
echo 添加远程仓库: https://github.com/%username%/%reponame%.git
git remote add origin https://github.com/%username%/%reponame%.git

echo.
echo 验证远程仓库配置:
git remote -v

echo.
echo 推送代码到GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo 推送失败! 可能的原因:
    echo 1. 仓库名称仍然不合法
    echo 2. 用户名输入错误
    echo 3. 仓库未创建或设置错误
    echo 4. 需要身份验证
    echo ========================================
    echo.
    echo 解决方案:
    echo 1. 检查GitHub仓库是否已创建
    echo 2. 确认用户名和仓库名称正确
    echo 3. 尝试使用GitHub Desktop进行推送
    echo 4. 或使用Personal Access Token
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 代码推送成功!
echo ========================================
echo.
echo 下一步操作:
echo 1. 访问您的仓库: https://github.com/%username%/%reponame%
echo 2. 点击 "Actions" 标签页
echo 3. 等待APK编译完成 (约5-10分钟)
echo 4. 下载编译好的APK文件
echo.
echo APK功能:
echo - TCP服务器 (端口8888)
echo - 接收脚本指令
echo - 返回执行结果
echo - 支持多客户端连接
echo.
start https://github.com/%username%/%reponame%
echo 已打开您的GitHub仓库页面
echo.
pause