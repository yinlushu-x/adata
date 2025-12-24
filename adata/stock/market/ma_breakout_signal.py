# -*- coding: utf-8 -*-
"""
@desc: 均线突破 + 成交量确认信号检测模块
@author: AI Assistant
@time: 2025-12-24
@log: change log
"""
import pandas as pd
import matplotlib.pyplot as plt
from adata.stock.market.stock_market.stock_market import StockMarket

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Hiragino Sans GB', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def detect_ma_breakout_signal(
    stock_code: str,
    start_date: str,
    end_date: str
):
    """
    检测均线突破 + 成交量确认信号
    :param stock_code: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 信号检测结果
    """
    # 1. 获取股票行情数据
    market = StockMarket()
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date)
    
    if df.empty:
        print("未获取到有效行情数据")
        return
    
    # 2. 计算技术指标
    # 计算均线
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    
    # 计算成交量10日均值
    df['VOL_MA10'] = df['volume'].rolling(window=10).mean()
    
    # 3. 检测信号
    # 均线突破条件：当日close > MA20，前一日close <= MA20
    df['ma_breakout'] = (df['close'] > df['MA20']) & (df['close'].shift(1) <= df['MA20'].shift(1))
    
    # 成交量确认条件：当日volume > VOL_MA10
    df['volume_confirm'] = df['volume'] > df['VOL_MA10']
    
    # 有效买入信号：同时满足均线突破和成交量确认
    df['buy_signal'] = df['ma_breakout'] & df['volume_confirm']
    
    # 4. 输出信号
    signal_df = df[df['buy_signal']][['trade_time', 'close', 'volume']].copy()
    signal_df = signal_df.rename(columns={'trade_time': '日期', 'close': '收盘价', 'volume': '成交量'})
    
    print("=== 均线突破 + 成交量确认信号检测结果 ===")
    if not signal_df.empty:
        print(signal_df.to_string(index=False))
    else:
        print("区间内未检测到有效信号")
    
    # 5. 可视化
    plt.figure(figsize=(14, 8))
    
    # 绘制收盘价
    plt.plot(df['trade_time'], df['close'], label='收盘价', color='blue', alpha=0.5)
    
    # 绘制均线
    plt.plot(df['trade_time'], df['MA5'], label='MA5', color='green')
    plt.plot(df['trade_time'], df['MA10'], label='MA10', color='orange')
    plt.plot(df['trade_time'], df['MA20'], label='MA20', color='red')
    
    # 绘制信号点
    signal_points = df[df['buy_signal']]
    if not signal_points.empty:
        plt.scatter(signal_points['trade_time'], signal_points['close'], marker='^', color='red', s=100, label='买入信号')
    
    # 设置图表属性
    plt.title(f'{stock_code} 均线突破 + 成交量确认信号检测')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    return signal_df


if __name__ == '__main__':
    # 测试示例
    detect_ma_breakout_signal('000001', '2024-01-01', '2024-12-31')