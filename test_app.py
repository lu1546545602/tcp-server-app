#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏组队服务器 - 测试脚本
用于在开发环境中测试Kivy应用

使用方法:
1. 安装依赖: pip install kivy
2. 运行测试: python test_app.py
"""

import sys
import os

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import kivy
        print(f"✓ Kivy版本: {kivy.__version__}")
    except ImportError:
        print("✗ Kivy未安装")
        print("请运行: pip install kivy")
        return False
    
    return True

def test_app():
    """测试应用"""
    print("=== 游戏组队服务器 - 测试模式 ===")
    print()
    
    if not check_dependencies():
        return False
    
    print("启动Kivy应用...")
    print("注意: 这是桌面测试版本，用于验证功能")
    print()
    
    try:
        # 导入并运行主应用
        from main import TCPServerApp
        app = TCPServerApp()
        app.run()
        return True
    except Exception as e:
        print(f"启动应用失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print(__doc__)
        return
    
    # 检查是否在正确目录
    if not os.path.exists('main.py'):
        print("错误: 请在tcp_apk目录下运行此脚本")
        sys.exit(1)
    
    success = test_app()
    
    if success:
        print("\n测试完成!")
    else:
        print("\n测试失败!")
        sys.exit(1)

if __name__ == '__main__':
    main()