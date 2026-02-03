# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析功能测试
@author: adata
@time: 2026/2/3
"""
import adata
import pandas as pd


def test_weekday_analysis():
    """测试周一到周五统计分析功能"""
    print("=" * 60)
    print("测试1: 获取股票日K数据并进行星期维度统计分析")
    print("=" * 60)
    
    # 获取平安银行(000001)的日K数据
    df = adata.stock.market.get_market(stock_code='000001', start_date='2023-01-01', end_date='2025-01-01', k_type=1)
    print(f"获取到 {len(df)} 条日K数据")
    print("\n数据预览:")
    print(df[['trade_date', 'open', 'close', 'volume']].head(10))
    
    # 进行星期维度统计分析
    weekday_stats = adata.stock.analysis.get_weekday_stats(df)
    print("\n星期维度统计分析结果:")
    print(weekday_stats)
    print()


def test_month_period_analysis():
    """测试月初、月中、月末区间统计分析功能"""
    print("=" * 60)
    print("测试2: 获取股票日K数据并进行月份区间统计分析")
    print("=" * 60)
    
    # 获取平安银行(000001)的日K数据
    df = adata.stock.market.get_market(stock_code='000001', start_date='2023-01-01', end_date='2025-01-01', k_type=1)
    print(f"获取到 {len(df)} 条日K数据")
    
    # 进行月份区间统计分析
    period_stats = adata.stock.analysis.get_month_period_stats(df)
    print("\n月份区间统计分析结果:")
    print(period_stats)
    print()


def test_with_custom_data():
    """使用自定义数据测试"""
    print("=" * 60)
    print("测试3: 使用自定义数据进行测试")
    print("=" * 60)
    
    # 创建测试数据
    test_data = {
        'trade_date': [
            '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',  # 周二到周五
            '2024-01-08', '2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12',  # 周一到周五
            '2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19',  # 周一到周五
            '2024-01-22', '2024-01-23', '2024-01-24', '2024-01-25', '2024-01-26',  # 周一到周五
            '2024-01-29', '2024-01-30', '2024-01-31',  # 周一到周三
            '2024-02-01', '2024-02-02',  # 周四、周五
        ],
        'open': [10.0, 10.2, 10.1, 10.3, 10.2, 10.4, 10.3, 10.5, 10.4,
                 10.3, 10.2, 10.1, 10.0, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4,
                 10.5, 10.6, 10.7, 10.8, 10.9],
        'close': [10.2, 10.1, 10.3, 10.2, 10.4, 10.3, 10.5, 10.4, 10.3,
                  10.2, 10.1, 10.0, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5,
                  10.6, 10.7, 10.8, 10.9, 11.0],
        'volume': [10000, 12000, 11000, 13000, 10500, 12500, 11500, 13500, 11000,
                   10000, 9500, 9000, 8500, 8800, 9200, 9800, 10200, 10800, 11200,
                   12000, 12500, 13000, 14000, 15000]
    }
    df = pd.DataFrame(test_data)
    
    print("自定义测试数据:")
    print(df)
    
    # 星期统计
    weekday_stats = adata.stock.analysis.get_weekday_stats(df)
    print("\n星期维度统计分析结果:")
    print(weekday_stats)
    
    # 月份区间统计
    period_stats = adata.stock.analysis.get_month_period_stats(df)
    print("\n月份区间统计分析结果:")
    print(period_stats)


if __name__ == '__main__':
    test_weekday_analysis()
    test_month_period_analysis()
    test_with_custom_data()
