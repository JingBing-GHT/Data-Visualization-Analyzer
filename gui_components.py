"""
图形用户界面组件模块
Graphical User Interface Components Module
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
from data_analyzer import DataAnalyzer
from visualization_engine import VisualizationEngine
import json
import os
from datetime import datetime

class DataVisualizationApp:
    """数据可视化应用主类"""
    
    def __init__(self, root):
        self.root = root
        self.analyzer = DataAnalyzer()
        self.visualizer = VisualizationEngine()
        self.current_data = None
        self.current_figure = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 设置样式
        self.setup_styles()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.create_title(main_frame)
        
        # 创建主内容区域（左右布局）
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 左侧控制面板
        self.create_control_panel(content_frame)
        
        # 右侧可视化区域
        self.create_visualization_area(content_frame)
        
        # 创建状态栏
        self.create_status_bar(main_frame)
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabelframe.Label', font=('Arial', 10, 'bold'))
        style.configure('Accent.TButton', font=('Arial', 9, 'bold'))
    
    def create_title(self, parent):
        """创建标题区域"""
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            title_frame, 
            text="数据可视化分析工具", 
            style='Title.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="专业的数据分析和可视化平台",
            font=('Arial', 11),
            foreground='#7f8c8d'
        )
        subtitle_label.pack()
    
    def create_control_panel(self, parent):
        """创建左侧控制面板"""
        # 左侧控制面板框架
        control_frame = ttk.Frame(parent, width=350)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # 创建标签页
        notebook = ttk.Notebook(control_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 数据导入标签页
        self.create_data_import_tab(notebook)
        
        # 图表配置标签页
        self.create_chart_config_tab(notebook)
        
        # 数据分析标签页
        self.create_analysis_tab(notebook)
    
    def create_data_import_tab(self, notebook):
        """创建数据导入标签页"""
        tab = ttk.Frame(notebook, padding="10")
        notebook.add(tab, text="📁 数据导入")
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(tab, text="数据文件", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        # 文件格式选择
        format_frame = ttk.Frame(file_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(format_frame, text="文件格式:").pack(side=tk.LEFT)
        self.file_format = ttk.Combobox(format_frame, values=["自动检测", "Excel", "CSV", "JSON"], width=12)
        self.file_format.set("自动检测")
        self.file_format.pack(side=tk.LEFT, padx=5)
        
        # 文件选择按钮
        ttk.Button(file_frame, text="选择数据文件", command=self.load_data_file, 
                  style='Accent.TButton').pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly').pack(fill=tk.X, pady=5)
        
        # CSV选项（条件显示）
        self.csv_frame = ttk.LabelFrame(file_frame, text="CSV选项", padding="5")
        
        ttk.Label(self.csv_frame, text="分隔符:").grid(row=0, column=0, sticky=tk.W)
        self.delimiter = ttk.Entry(self.csv_frame, width=5)
        self.delimiter.insert(0, ",")
        self.delimiter.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.csv_frame, text="编码:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        self.encoding = ttk.Combobox(self.csv_frame, values=["utf-8", "gbk", "gb2312", "latin1"], width=8)
        self.encoding.set("utf-8")
        self.encoding.grid(row=0, column=3, padx=5)
        
        # 数据预览区域
        preview_frame = ttk.LabelFrame(tab, text="数据预览", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=12, font=('Consolas', 9))
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定文件格式变化事件
        self.file_format.bind('<<ComboboxSelected>>', self.on_file_format_change)
    
    def on_file_format_change(self, event=None):
        """文件格式改变时的回调"""
        format_type = self.file_format.get()
        if format_type == "CSV":
            self.csv_frame.pack(fill=tk.X, pady=5)
        else:
            self.csv_frame.pack_forget()
    
    def create_chart_config_tab(self, notebook):
        """创建图表配置标签页"""
        tab = ttk.Frame(notebook, padding="10")
        notebook.add(tab, text="📊 图表配置")
        
        # 图表类型选择
        chart_frame = ttk.LabelFrame(tab, text="图表类型", padding="10")
        chart_frame.pack(fill=tk.X, pady=5)
        
        # 基础图表
        ttk.Label(chart_frame, text="基础图表:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.chart_type = tk.StringVar(value="line")
        
        basic_charts = [
            ("折线图", "line"),
            ("柱状图", "bar"),
            ("散点图", "scatter"),
            ("饼图", "pie"),
            ("面积图", "area")
        ]
        
        for i, (text, value) in enumerate(basic_charts):
            ttk.Radiobutton(chart_frame, text=text, variable=self.chart_type, 
                           value=value).grid(row=1, column=i, sticky=tk.W, padx=5)
        
        # 统计图表
        ttk.Label(chart_frame, text="统计图表:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        
        stat_charts = [
            ("箱线图", "box"),
            ("热力图", "heatmap"),
            ("分布图", "distplot"),
            ("小提琴图", "violin"),
            ("配对图", "pairplot")
        ]
        
        for i, (text, value) in enumerate(stat_charts):
            ttk.Radiobutton(chart_frame, text=text, variable=self.chart_type, 
                           value=value).grid(row=3, column=i, sticky=tk.W, padx=5)
        
        # 坐标轴配置
        axis_frame = ttk.LabelFrame(tab, text="坐标轴配置", padding="10")
        axis_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(axis_frame, text="X轴:").grid(row=0, column=0, sticky=tk.W)
        self.x_axis = ttk.Combobox(axis_frame, state="readonly", width=20)
        self.x_axis.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(axis_frame, text="Y轴:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.y_axis = ttk.Combobox(axis_frame, state="readonly", width=20)
        self.y_axis.grid(row=1, column=1, padx=5, sticky=tk.W, pady=5)
        
        # 分组选项
        ttk.Label(axis_frame, text="分组:").grid(row=2, column=0, sticky=tk.W)
        self.group_by = ttk.Combobox(axis_frame, state="readonly", width=20)
        self.group_by.grid(row=2, column=1, padx=5, sticky=tk.W)
        
        # 样式配置
        style_frame = ttk.LabelFrame(tab, text="图表样式", padding="10")
        style_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(style_frame, text="主题:").grid(row=0, column=0, sticky=tk.W)
        self.theme = ttk.Combobox(style_frame, values=["default", "darkgrid", "whitegrid", "dark", "white"], width=15)
        self.theme.set("default")
        self.theme.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(style_frame, text="颜色方案:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color_palette = ttk.Combobox(style_frame, values=["viridis", "plasma", "Set1", "Set2", "Pastel1", "husl"], width=15)
        self.color_palette.set("viridis")
        self.color_palette.grid(row=1, column=1, padx=5, sticky=tk.W, pady=5)
        
        # 生成图表按钮
        ttk.Button(tab, text="生成图表", command=self.generate_chart, 
                  style='Accent.TButton').pack(fill=tk.X, pady=10)
    
    def create_analysis_tab(self, notebook):
        """创建数据分析标签页"""
        tab = ttk.Frame(notebook, padding="10")
        notebook.add(tab, text="🔍 数据分析")
        
        # 数据概览
        overview_frame = ttk.LabelFrame(tab, text="数据概览", padding="10")
        overview_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(overview_frame, text="显示数据概览", 
                  command=self.show_data_overview).pack(fill=tk.X, pady=2)
        
        ttk.Button(overview_frame, text="显示描述性统计", 
                  command=self.show_descriptive_stats).pack(fill=tk.X, pady=2)
        
        # 统计分析
        stats_frame = ttk.LabelFrame(tab, text="统计分析", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(stats_frame, text="相关性分析", 
                  command=self.analyze_correlations).pack(fill=tk.X, pady=2)
        
        ttk.Button(stats_frame, text="缺失值分析", 
                  command=self.analyze_missing_values).pack(fill=tk.X, pady=2)
        
        ttk.Button(stats_frame, text="异常值检测", 
                  command=self.detect_outliers).pack(fill=tk.X, pady=2)
        
        # 数据操作
        operation_frame = ttk.LabelFrame(tab, text="数据操作", padding="10")
        operation_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(operation_frame, text="数据清洗", 
                  command=self.clean_data).pack(fill=tk.X, pady=2)
        
        ttk.Button(operation_frame, text="数据转换", 
                  command=self.transform_data).pack(fill=tk.X, pady=2)
        
        # 导出功能
        export_frame = ttk.LabelFrame(tab, text="导出功能", padding="10")
        export_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(export_frame, text="导出图表", 
                  command=self.export_chart).pack(fill=tk.X, pady=2)
        
        ttk.Button(export_frame, text="导出数据", 
                  command=self.export_data).pack(fill=tk.X, pady=2)
        
        ttk.Button(export_frame, text="生成报告", 
                  command=self.generate_report).pack(fill=tk.X, pady=2)
    
    def create_visualization_area(self, parent):
        """创建右侧可视化区域"""
        viz_frame = ttk.Frame(parent)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 图表显示区域
        chart_frame = ttk.LabelFrame(viz_frame, text="图表展示", padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Matplotlib图形
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加工具栏
        toolbar_frame = ttk.Frame(chart_frame)
        toolbar_frame.pack(fill=tk.X)
        NavigationToolbar2Tk(self.canvas, toolbar_frame)
        
        # 分析结果显示区域
        analysis_frame = ttk.LabelFrame(viz_frame, text="分析结果", padding="10")
        analysis_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, height=8, font=('Consolas', 9))
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X)
    
    def load_data_file(self):
        """加载数据文件"""
        file_types = [
            ("所有支持格式", "*.xlsx *.xls *.csv *.json"),
            ("Excel文件", "*.xlsx *.xls"),
            ("CSV文件", "*.csv"),
            ("JSON文件", "*.json"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(title="选择数据文件", filetypes=file_types)
        if not filename:
            return
        
        try:
            self.status_var.set("正在加载数据...")
            self.root.update()
            
            file_format = self.file_format.get()
            
            if file_format == "自动检测":
                if filename.endswith(('.xlsx', '.xls')):
                    file_format = "Excel"
                elif filename.endswith('.csv'):
                    file_format = "CSV"
                elif filename.endswith('.json'):
                    file_format = "JSON"
            
            if file_format == "Excel":
                self.current_data = pd.read_excel(filename)
            elif file_format == "CSV":
                delimiter = self.delimiter.get() if self.delimiter.get() else ','
                encoding = self.encoding.get()
                self.current_data = pd.read_csv(filename, delimiter=delimiter, encoding=encoding)
            elif file_format == "JSON":
                with open(filename, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                # 简单处理JSON数据，可根据实际结构调整
                if isinstance(json_data, list):
                    self.current_data = pd.DataFrame(json_data)
                else:
                    self.current_data = pd.DataFrame([json_data])
            else:
                messagebox.showerror("错误", f"不支持的文件格式: {file_format}")
                return
            
            self.file_path_var.set(filename)
            self.update_data_preview()
            self.update_axis_options()
            self.status_var.set(f"数据加载成功: {len(self.current_data)} 行 × {len(self.current_data.columns)} 列")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {str(e)}")
            self.status_var.set("数据加载失败")
    
    def update_data_preview(self):
        """更新数据预览"""
        if self.current_data is not None:
            preview_content = f"数据形状: {self.current_data.shape}\n\n"
            preview_content += f"列名: {list(self.current_data.columns)}\n\n"
            preview_content += "前5行数据:\n"
            preview_content += self.current_data.head().to_string()
            
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', preview_content)
    
    def update_axis_options(self):
        """更新坐标轴选项"""
        if self.current_data is not None:
            columns = list(self.current_data.columns)
            self.x_axis['values'] = columns
            self.y_axis['values'] = columns
            self.group_by['values'] = [""] + columns  # 空字符串表示不分组
            
            if columns:
                self.x_axis.set(columns[0])
                if len(columns) > 1:
                    self.y_axis.set(columns[1])
    
    def generate_chart(self):
        """生成图表"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        try:
            self.status_var.set("正在生成图表...")
            self.root.update()
            
            # 获取配置参数
            chart_type = self.chart_type.get()
            x_col = self.x_axis.get()
            y_col = self.y_axis.get()
            group_col = self.group_by.get() if self.group_by.get() else None
            theme = self.theme.get()
            palette = self.color_palette.get()
            
            # 设置主题
            if theme != "default":
                sns.set_style(theme)
            
            # 清空图形
            self.figure.clear()
            
            # 生成图表
            ax = self.figure.add_subplot(111)
            self.visualizer.create_chart(
                ax, self.current_data, chart_type, x_col, y_col, group_col, palette
            )
            
            # 刷新画布
            self.canvas.draw()
            self.status_var.set("图表生成完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成图表失败: {str(e)}")
            self.status_var.set("图表生成失败")
    
    def show_data_overview(self):
        """显示数据概览"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        overview = self.analyzer.get_data_overview(self.current_data)
        self.display_analysis_result(overview)
    
    def show_descriptive_stats(self):
        """显示描述性统计"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        stats = self.analyzer.get_descriptive_statistics(self.current_data)
        self.display_analysis_result(stats)
    
    def analyze_correlations(self):
        """分析相关性"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        correlations = self.analyzer.analyze_correlations(self.current_data)
        self.display_analysis_result(correlations)
    
    def analyze_missing_values(self):
        """分析缺失值"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        missing_analysis = self.analyzer.analyze_missing_values(self.current_data)
        self.display_analysis_result(missing_analysis)
    
    def detect_outliers(self):
        """检测异常值"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        outliers = self.analyzer.detect_outliers(self.current_data)
        self.display_analysis_result(outliers)
    
    def clean_data(self):
        """数据清洗"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        # 这里可以实现数据清洗对话框
        messagebox.showinfo("信息", "数据清洗功能开发中...")
    
    def transform_data(self):
        """数据转换"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        # 这里可以实现数据转换对话框
        messagebox.showinfo("信息", "数据转换功能开发中...")
    
    def export_chart(self):
        """导出图表"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG图片", "*.png"),
                ("JPEG图片", "*.jpg"),
                ("PDF文档", "*.pdf"),
                ("SVG矢量图", "*.svg")
            ]
        )
        
        if filename:
            try:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"图表已导出到: {filename}")
                self.status_var.set("图表导出完成")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def export_data(self):
        """导出数据"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel文件", "*.xlsx"),
                ("CSV文件", "*.csv"),
                ("JSON文件", "*.json")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.xlsx'):
                    self.current_data.to_excel(filename, index=False)
                elif filename.endswith('.csv'):
                    self.current_data.to_csv(filename, index=False, encoding='utf-8-sig')
                elif filename.endswith('.json'):
                    self.current_data.to_json(filename, orient='records', indent=2)
                
                messagebox.showinfo("成功", f"数据已导出到: {filename}")
                self.status_var.set("数据导出完成")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def generate_report(self):
        """生成分析报告"""
        if self.current_data is None:
            messagebox.showwarning("警告", "请先加载数据文件")
            return
        
        messagebox.showinfo("信息", "分析报告生成功能开发中...")
    
    def display_analysis_result(self, result):
        """显示分析结果"""
        self.analysis_text.delete('1.0', tk.END)
        self.analysis_text.insert('1.0', result)
