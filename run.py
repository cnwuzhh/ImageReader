#!/usr/bin/env python3
"""
ImageReader 快速启动脚本
"""

import sys
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'PIL', 'requests', 'tkinter'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'requests':
                import requests
            elif package == 'tkinter':
                import tkinter
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("错误: 缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行: pip install -r requirements.txt")
        return False

    return True

def check_config():
    """检查配置文件"""
    try:
        from config import CHATGLM_API_KEY
        if CHATGLM_API_KEY == "YOUR_API_KEY_HERE":
            print("警告: 请先配置ChatGLM API密钥")
            print("方法1: 运行程序后点击'设置'按钮进行配置")
            print("方法2: 编辑config.py文件中的CHATGLM_API_KEY")
            return False
    except ImportError:
        print("错误: 无法导入配置文件")
        return False

    return True

def main():
    print("=== ImageReader 智能表格识别器 ===")
    print("正在检查环境...")

    # 检查Python版本
    if not check_python_version():
        input("按回车键退出...")
        return

    # 检查依赖包
    if not check_dependencies():
        input("按回车键退出...")
        return

    # 检查配置
    # if not check_config():
    #     print("注意: 程序仍可运行，但需要配置API密钥才能使用识别功能")

    print("环境检查完成，正在启动程序...")

    try:
        from main import main as app_main
        app_main()
    except Exception as e:
        print(f"启动失败: {str(e)}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()