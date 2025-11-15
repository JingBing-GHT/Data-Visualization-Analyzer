"""
可视化引擎模块
Visualization Engine Module
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats

class VisualizationEngine:
    """可视化引擎"""
    
    def __init__(self):
        # 设置默认样式
        plt.style.use('default')
        sns.set_palette("viridis")
    
    def create_chart(self, ax, data, chart_type, x_col, y_col=None, group_col=None, palette="viridis"):
        """
        创建图表
        
        Args:
            ax: matplotlib轴对象
            data: 数据框
            chart_type: 图表类型
            x_col: X轴列名
            y_col: Y轴列名
            group_col: 分组列名
            palette: 颜色方案
        """
        try:
            if chart_type == "line":
                self.create_line_chart(ax, data, x_col, y_col, group_col, palette)
            elif chart_type == "bar":
                self.create_bar_chart(ax, data, x_col, y_col, group_col, palette)
            elif chart_type == "scatter":
                self.create_scatter_chart(ax, data, x_col, y_col, group_col, palette)
            elif chart_type == "pie":
                self.create_pie_chart(ax, data, x_col, palette)
            elif chart_type == "area":
                self.create_area_chart(ax, data, x_col, y_col, group_col, palette)
            elif chart_type == "box":
                self.create_box_plot(ax, data, x_col, y_col, palette)
            elif chart_type == "heatmap":
                self.create_heatmap(ax, data, palette)
            elif chart_type == "distplot":
                self.create_distribution_plot(ax, data, x_col, palette)
            elif chart_type == "violin":
                self.create_violin_plot(ax, data, x_col, y_col, palette)
            elif chart_type == "pairplot":
                self.create_pair_plot(ax, data, group_col, palette)
            else:
                raise ValueError(f"不支持的图表类型: {chart_type}")
                
            # 设置标题和标签
            self.set_chart_labels(ax, chart_type, x_col, y_col)
            
        except Exception as e:
            raise Exception(f"创建图表失败: {str(e)}")
    
    def create_line_chart(self, ax, data, x_col, y_col, group_col, palette):
        """创建折线图"""
        if group_col and group_col in data.columns:
            # 分组折线图
            groups = data.groupby(group_col)
            for name, group in groups:
                ax.plot(group[x_col], group[y_col], marker='o', label=name, linewidth=2)
            ax.legend()
        else:
            # 简单折线图
            ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, color=sns.color_palette(palette)[0])
    
    def create_bar_chart(self, ax, data, x_col, y_col, group_col, palette):
        """创建柱状图"""
        if group_col and group_col in data.columns:
            # 分组柱状图
            pivot_data = data.pivot_table(values=y_col, index=x_col, columns=group_col, aggfunc='mean')
            pivot_data.plot(kind='bar', ax=ax, color=sns.color_palette(palette, len(pivot_data.columns)))
            ax.legend(title=group_col)
        else:
            # 简单柱状图
            ax.bar(data[x_col], data[y_col], color=sns.color_palette(palette))
    
    def create_scatter_chart(self, ax, data, x_col, y_col, group_col, palette):
        """创建散点图"""
        if group_col and group_col in data.columns:
            # 分组散点图
            groups = data.groupby(group_col)
            colors = sns.color_palette(palette, len(groups))
            for (name, group), color in zip(groups, colors):
                ax.scatter(group[x_col], group[y_col], label=name, color=color, alpha=0.7)
            ax.legend()
        else:
            # 简单散点图
            ax.scatter(data[x_col], data[y_col], color=sns.color_palette(palette)[0], alpha=0.7)
    
    def create_pie_chart(self, ax, data, x_col, palette):
        """创建饼图"""
        value_counts = data[x_col].value_counts()
        colors = sns.color_palette(palette, len(value_counts))
        ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', colors=colors)
        ax.set_ylabel('')  # 移除Y轴标签
    
    def create_area_chart(self, ax, data, x_col, y_col, group_col, palette):
        """创建面积图"""
        if group_col and group_col in data.columns:
            # 分组面积图
            pivot_data = data.pivot_table(values=y_col, index=x_col, columns=group_col, aggfunc='sum')
            pivot_data.plot(kind='area', ax=ax, color=sns.color_palette(palette, len(pivot_data.columns)))
            ax.legend(title=group_col)
        else:
            # 简单面积图
            ax.fill_between(data[x_col], data[y_col], color=sns.color_palette(palette)[0], alpha=0.4)
            ax.plot(data[x_col], data[y_col], color=sns.color_palette(palette)[0], linewidth=2)
    
    def create_box_plot(self, ax, data, x_col, y_col, palette):
        """创建箱线图"""
        if x_col and y_col:
            # 分组箱线图
            sns.boxplot(data=data, x=x_col, y=y_col, ax=ax, palette=palette)
        else:
            # 单变量箱线图
            column = x_col if x_col else y_col
            sns.boxplot(data=data[column], ax=ax, color=sns.color_palette(palette)[0])
    
    def create_heatmap(self, ax, data, palette):
        """创建热力图"""
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            raise ValueError("没有数值型数据可用于热力图")
        
        correlation_matrix = numeric_data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap=palette, ax=ax, center=0,
                   fmt='.2f', linewidths=0.5)
    
    def create_distribution_plot(self, ax, data, x_col, palette):
        """创建分布图"""
        sns.histplot(data=data, x=x_col, kde=True, ax=ax, color=sns.color_palette(palette)[0])
    
    def create_violin_plot(self, ax, data, x_col, y_col, palette):
        """创建小提琴图"""
        if x_col and y_col:
            sns.violinplot(data=data, x=x_col, y=y_col, ax=ax, palette=palette)
        else:
            column = x_col if x_col else y_col
            sns.violinplot(data=data[column], ax=ax, color=sns.color_palette(palette)[0])
    
    def create_pair_plot(self, ax, data, group_col, palette):
        """创建配对图（简化版）"""
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            raise ValueError("没有数值型数据可用于配对图")
        
        # 简化版：显示第一个数值变量对第二个数值变量的散点图
        if len(numeric_data.columns) >= 2:
            col1, col2 = numeric_data.columns[0], numeric_data.columns[1]
            if group_col and group_col in data.columns:
                sns.scatterplot(data=data, x=col1, y=col2, hue=group_col, ax=ax, palette=palette)
            else:
                sns.scatterplot(data=data, x=col1, y=col2, ax=ax, color=sns.color_palette(palette)[0])
        else:
            raise ValueError("需要至少两个数值型变量用于配对图")
    
    def set_chart_labels(self, ax, chart_type, x_col, y_col):
        """设置图表标签"""
        if x_col:
            ax.set_xlabel(x_col, fontsize=12)
        if y_col:
            ax.set_ylabel(y_col, fontsize=12)
        
        # 设置标题
        chart_names = {
            "line": "折线图",
            "bar": "柱状图", 
            "scatter": "散点图",
            "pie": "饼图",
            "area": "面积图",
            "box": "箱线图",
            "heatmap": "热力图",
            "distplot": "分布图",
            "violin": "小提琴图",
            "pairplot": "散点图"
        }
        
        title = chart_names.get(chart_type, "图表")
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # 美化图表
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        # 自动调整X轴标签角度（如果标签太长）
        if x_col and hasattr(ax, 'get_xticklabels'):
            labels = ax.get_xticklabels()
            if labels:
                max_label_length = max(len(label.get_text()) for label in labels)
                if max_label_length > 10:
                    plt.setp(labels, rotation=45, ha='right')
