# -*- coding: utf-8 -*-
"""
@desc: 股票分析工具
@author: AI Assistant
@time: 2025-12-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adata.stock import stock

def calculate_max_drawdown(prices):
    """
    计算最大回撤
    :param prices: 价格序列
    :return: 最大回撤值（百分比）
    """
    if len(prices) < 2:
        return 0.0
    
    peak = prices[0]
    max_dd = 0.0
    
    for price in prices[1:]:
        if price > peak:
            peak = price
        else:
            dd = (peak - price) / peak
            if dd > max_dd:
                max_dd = dd
    
    return max_dd * 100

def analyze_stock(stock_code, start_date, end_date):
    """
    分析指定股票在给定日期区间内的行情数据
    :param stock_code: 股票代码
    :param start_date: 开始日期，格式如 '2024-01-01'
    :param end_date: 结束日期，格式如 '2024-12-31'
    """
    # 1. 获取股票行情数据
    df = stock.market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)
    
    if df.empty:
        print(f"错误：未能获取股票 {stock_code} 的行情数据")
        return
    
    # 2. 计算指标
    # 确保数据按日期排序
    df = df.sort_values('trade_date')
    
    # 区间涨跌幅
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    price_change = (end_price / start_price - 1) * 100
    
    # 区间最大回撤
    max_drawdown = calculate_max_drawdown(df['close'].values)
    
    # 区间最高价和最低价
    highest_price = df['high'].max()
    lowest_price = df['low'].min()
    
    # 3. 打印结果
    print("=" * 50)
    print(f"股票分析报告：{stock_code}")
    print(f"分析区间：{start_date} 至 {end_date}")
    print("=" * 50)
    print(f"期初价格：{start_price:.2f} 元")
    print(f"期末价格：{end_price:.2f} 元")
    print(f"区间涨跌幅：{price_change:.2f}%")
    print(f"区间最大回撤：{max_drawdown:.2f}%")
    print(f"区间最高价：{highest_price:.2f} 元")
    print(f"区间最低价：{lowest_price:.2f} 元")
    print(f"交易日数量：{len(df)} 天")
    print("=" * 50)
    
    # 4. 绘制收益曲线图
    plt.figure(figsize=(12, 6))
    
    # 绘制收盘价曲线
    plt.plot(df['trade_date'], df['close'], label='收盘价', color='#1f77b4', linewidth=2)
    
    # 绘制归一化收益曲线（便于观察相对收益）
    normalized_price = df['close'] / start_price
    plt.plot(df['trade_date'], normalized_price, label='归一化收益', color='#ff7f0e', linewidth=2)
    
    # 设置图表属性
    plt.title(f'股票 {stock_code} 收益曲线图 ({start_date} - {end_date})', fontsize=14, pad=20)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('价格/归一化收益', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # 显示图表
    plt.tight_layout()
    plt.show()

import argparse

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='股票分析工具')
    parser.add_argument('stock_code', type=str, help='股票代码，如 000001')
    parser.add_argument('start_date', type=str, help='开始日期，格式为 YYYY-MM-DD')
    parser.add_argument('end_date', type=str, help='结束日期，格式为 YYYY-MM-DD')
    
    args = parser.parse_args()
    
    # 运行分析
    analyze_stock(args.stock_code, args.start_date, args.end_date)