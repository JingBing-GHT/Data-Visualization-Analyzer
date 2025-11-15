"""
数据分析核心逻辑模块
Data Analysis Core Logic Module
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings

class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self):
        pass
    
    def get_data_overview(self, data):
        """获取数据概览"""
        overview = "=== 数据概览 ===\n\n"
        overview += f"数据形状: {data.shape} (行数: {data.shape[0]}, 列数: {data.shape[1]})\n\n"
        
        overview += "列信息:\n"
        for col in data.columns:
            dtype = data[col].dtype
            non_null = data[col].count()
            null_count = data[col].isnull().sum()
            overview += f"  {col}: {dtype} (非空值: {non_null}, 空值: {null_count})\n"
        
        overview += f"\n内存使用: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n"
        
        return overview
    
    def get_descriptive_statistics(self, data):
        """获取描述性统计"""
        stats_text = "=== 描述性统计 ===\n\n"
        
        # 数值型数据统计
        numeric_data = data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            stats_text += "数值型变量统计:\n"
            stats_text += numeric_data.describe().to_string()
            stats_text += "\n\n"
        
        # 分类型数据统计
        categorical_data = data.select_dtypes(include=['object', 'category'])
        if not categorical_data.empty:
            stats_text += "分类型变量统计:\n"
            for col in categorical_data.columns:
                stats_text += f"\n{col}:\n"
                value_counts = data[col].value_counts()
                stats_text += value_counts.head(10).to_string()  # 只显示前10个
                if len(value_counts) > 10:
                    stats_text += f"\n... 和其他 {len(value_counts) - 10} 个类别"
            stats_text += "\n"
        
        return stats_text
    
    def analyze_correlations(self, data):
        """分析相关性"""
        corr_text = "=== 相关性分析 ===\n\n"
        
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return "没有数值型数据可用于相关性分析"
        
        if len(numeric_data.columns) < 2:
            return "需要至少两个数值型变量进行相关性分析"
        
        # 计算相关系数矩阵
        correlation_matrix = numeric_data.corr()
        
        corr_text += "相关系数矩阵:\n"
        corr_text += correlation_matrix.round(3).to_string()
        corr_text += "\n\n"
        
        # 找出强相关性
        corr_text += "强相关性 (|r| > 0.7):\n"
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr = correlation_matrix.iloc[i, j]
                if abs(corr) > 0.7:
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    strong_correlations.append((col1, col2, corr))
        
        if strong_correlations:
            for col1, col2, corr in strong_correlations:
                corr_text += f"  {col1} - {col2}: {corr:.3f}\n"
        else:
            corr_text += "  未发现强相关性\n"
        
        return corr_text
    
    def analyze_missing_values(self, data):
        """分析缺失值"""
        missing_text = "=== 缺失值分析 ===\n\n"
        
        total_cells = np.product(data.shape)
        total_missing = data.isnull().sum().sum()
        
        missing_text += f"总数据点: {total_cells}\n"
        missing_text += f"总缺失值: {total_missing}\n"
        missing_text += f"缺失值比例: {total_missing/total_cells*100:.2f}%\n\n"
        
        missing_text += "各列缺失值统计:\n"
        missing_count = data.isnull().sum()
        missing_percent = (missing_count / len(data)) * 100
        
        missing_df = pd.DataFrame({
            '缺失数量': missing_count,
            '缺失比例%': missing_percent.round(2)
        })
        
        # 只显示有缺失值的列
        missing_df = missing_df[missing_df['缺失数量'] > 0]
        
        if not missing_df.empty:
            missing_text += missing_df.to_string()
        else:
            missing_text += "  没有缺失值"
        
        return missing_text
    
    def detect_outliers(self, data):
        """检测异常值"""
        outlier_text = "=== 异常值检测 ===\n\n"
        
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return "没有数值型数据可用于异常值检测"
        
        outlier_text += "使用IQR方法检测异常值:\n\n"
        
        for col in numeric_data.columns:
            Q1 = numeric_data[col].quantile(0.25)
            Q3 = numeric_data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = numeric_data[(numeric_data[col] < lower_bound) | (numeric_data[col] > upper_bound)]
            outlier_count = len(outliers)
            
            outlier_text += f"{col}:\n"
            outlier_text += f"  正常值范围: [{lower_bound:.3f}, {upper_bound:.3f}]\n"
            outlier_text += f"  异常值数量: {outlier_count}
