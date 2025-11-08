#!/usr/bin/env python3
"""
网页截图和录屏工具 - 启动脚本
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import flask
        import playwright
        print("✓ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"✗ 依赖缺失: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def install_playwright_browsers():
    """安装Playwright浏览器"""
    print("正在安装Playwright浏览器...")
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✓ Playwright浏览器安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 浏览器安装失败: {e}")
        return False

def main():
    """主函数"""
    print("🌐 网页截图和录屏工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 安装浏览器
    if not install_playwright_browsers():
        print("警告: 浏览器安装失败，可能会影响功能")
    
    # 创建必要目录
    os.makedirs('output/screenshots', exist_ok=True)
    os.makedirs('output/videos', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("\n🚀 启动服务...")
    print("服务地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    # 启动Flask应用
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"\n✗ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()