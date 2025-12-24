# -*- coding: utf-8 -*-
"""
测试股票K线图绘制功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_kline_chart import get_stock_data, plot_kline_chart

def test_get_stock_data():
    """
    测试获取股票数据功能
    """
    print("测试获取股票数据功能...")
    data = get_stock_data(stock_code='000001', start_date='2024-01-01', end_date='2024-12-31')
    print(f"获取到的数据形状: {data.shape}")
    print(f"数据前5行:\n{data.head()}")
    print(f"数据后5行:\n{data.tail()}")
    return data

def test_plot_kline_chart(data):
    """
    测试绘制K线图功能
    """
    print("\n测试绘制K线图功能...")
    plot_kline_chart(data, stock_code='000001', title='测试K线图')

def main():
    """
    主测试函数
    """
    print("=== 开始测试股票K线图绘制功能 ===")
    
    # 测试获取数据
    data = test_get_stock_data()
    
    if data is not None:
        # 测试绘制图表
        test_plot_kline_chart(data)
        print("\n=== 测试完成 ===")
    else:
        print("\n=== 测试失败：未获取到数据 ===")

if __name__ == '__main__':
    main()