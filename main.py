#!/usr/bin/env python3
"""
数据可视化分析工具 - 主程序入口
Data Visualization Analyzer - Main Entry Point
"""

import tkinter as tk
from gui_components import DataVisualizationApp

def main():
    """主程序入口函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口标题
        root.title("数据可视化分析工具 v2.0")
        root.geometry("1200x800")
        
        # 设置窗口最小尺寸
        root.minsize(1000, 700)
        
        # 创建主应用程序
        app = DataVisualizationApp(root)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
