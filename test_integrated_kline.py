# -*- coding: utf-8 -*-
"""
测试集成后的股票K线图绘制功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import adata

def test_integrated_kline():
    """
    测试集成后的K线图绘制功能
    """
    print("=== 测试集成后的股票K线图绘制功能 ===")
    
    # 绘制股票K线图
    stock_code = '000001'
    start_date = '2024-01-01'
    end_date = '2024-12-31'
    
    print(f"正在绘制股票{stock_code}的K线图...")
    adata.chart.draw_kline(stock_code, start_date, end_date)
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_integrated_kline()