# -*- coding: utf-8 -*-
"""
股票K线图绘制工具
使用adata.stock.market.get_market获取数据，使用mplfinance绘制K线图
"""

import sys
import argparse
import pandas as pd
import mplfinance as mpf
from adata.stock.market.stock_market.stock_market import StockMarket

def get_stock_data(stock_code, start_date, end_date, k_type=1, adjust_type=1):
    """
    获取股票行情数据
    :param stock_code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param k_type: K线类型（1:日, 2:周, 3:月, 4:季度, 5:5min, 15:15min, 30:30min, 60:60min）
    :param adjust_type: 复权类型（0:不复权, 1:前复权, 2:后复权）
    :return: 处理后的DataFrame
    """
    market = StockMarket()
    df = market.get_market(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        k_type=k_type,
        adjust_type=adjust_type
    )
    
    if df.empty:
        print(f"未获取到股票{stock_code}的数据")
        return None
    
    # 转换日期为datetime格式
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    
    # 选择需要的列并重命名为mplfinance需要的格式
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    return df

def plot_kline_chart(data, stock_code, title):
    """
    绘制K线图
    :param data: 包含OHLCV数据的DataFrame
    :param stock_code: 股票代码
    :param title: 图表标题
    """
    # 设置图表样式
    mc = mpf.make_marketcolors(
        up='red', down='green', wick='inherit', edge='inherit', volume='inherit'
    )
    s = mpf.make_mpf_style(marketcolors=mc, figcolor='#f0f0f0', facecolor='#f0f0f0')
    
    # 绘制图表
    fig, axes = mpf.plot(
        data,
        type='candle',
        volume=True,
        style=s,
        title=title,
        ylabel='价格(元)',
        ylabel_lower='成交量(股)',
        figratio=(16, 9),
        figscale=1.2,
        returnfig=True
    )
    
    # 显示图表
    mpf.show()

def main():
    """
    主函数，处理命令行参数并执行
    """
    parser = argparse.ArgumentParser(description='股票K线图绘制工具')
    parser.add_argument('stock_code', help='股票代码（如：000001）')
    parser.add_argument('start_date', help='开始日期（格式：YYYY-MM-DD）')
    parser.add_argument('end_date', help='结束日期（格式：YYYY-MM-DD）')
    parser.add_argument('--k_type', type=int, default=1, help='K线类型（1:日, 2:周, 3:月, 4:季度, 5:5min, 15:15min, 30:30min, 60:60min）')
    parser.add_argument('--adjust_type', type=int, default=1, help='复权类型（0:不复权, 1:前复权, 2:后复权）')
    
    args = parser.parse_args()
    
    # 获取数据
    print(f"正在获取股票{args.stock_code}的行情数据...")
    data = get_stock_data(
        stock_code=args.stock_code,
        start_date=args.start_date,
        end_date=args.end_date,
        k_type=args.k_type,
        adjust_type=args.adjust_type
    )
    
    if data is None:
        sys.exit(1)
    
    # 绘制图表
    title = f"股票{args.stock_code} K线图 ({args.start_date} 至 {args.end_date})"
    print(f"正在绘制K线图...")
    plot_kline_chart(data, args.stock_code, title)

if __name__ == '__main__':
    main()