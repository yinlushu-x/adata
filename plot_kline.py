# -*- coding: utf-8 -*-
"""
@desc: 股票K线图绘制工具
@author: 1nchaos
@time: 2024/07/23
"""

import argparse
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from adata.stock.market import market

def plot_kline(stock_code, start_date, end_date, k_type=1, adjust_type=1):
    """
    绘制股票K线图
    :param stock_code: 股票代码
    :param start_date: 开始日期，格式YYYY-MM-DD
    :param end_date: 结束日期，格式YYYY-MM-DD
    :param k_type: k线类型：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min 默认：1 日k
    :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
    """
    # 获取数据
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=k_type, adjust_type=adjust_type)
    
    if df.empty:
        print(f"没有找到股票{stock_code}在{start_date}至{end_date}期间的行情数据")
        return
    
    # 数据处理：提取时间、开盘价、收盘价、最高价、最低价等OHLC信息
    # 转换时间列
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    
    # 重命名列以匹配mplfinance要求
    df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)
    
    # 设置K线图样式
    mc = mpf.make_marketcolors(up='red', down='green', wick='inherit', volume='inherit')
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle='-', rc={'font.family': 'SimHei'})
    
    # 绘制K线图
    fig, axes = mpf.plot(df, type='candle', style=s, volume=True, returnfig=True, figsize=(16, 8))
    
    # 设置标题和标签
    axes[0].set_title(f'{stock_code} 股票K线图 ({start_date} - {end_date})', fontsize=14)
    axes[0].set_xlabel('时间', fontsize=12)
    axes[0].set_ylabel('价格', fontsize=12)
    axes[2].set_xlabel('时间', fontsize=12)
    axes[2].set_ylabel('成交量', fontsize=12)
    
    # 显示图表
    plt.show()

def main():
    """
    命令行入口
    """
    parser = argparse.ArgumentParser(description='绘制股票K线图')
    parser.add_argument('stock_code', type=str, help='股票代码，如000001')
    parser.add_argument('start_date', type=str, help='开始日期，格式YYYY-MM-DD')
    parser.add_argument('end_date', type=str, help='结束日期，格式YYYY-MM-DD')
    parser.add_argument('--k_type', type=int, default=1, help='k线类型：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min')
    parser.add_argument('--adjust_type', type=int, default=1, help='复权类型：0.不复权；1.前复权；2.后复权')
    
    args = parser.parse_args()
    
    plot_kline(args.stock_code, args.start_date, args.end_date, args.k_type, args.adjust_type)

if __name__ == '__main__':
    main()