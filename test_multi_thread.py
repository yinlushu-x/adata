#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多线程获取股票行情数据的效果
"""

import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adata.stock.market.stock_market.stock_market import StockMarket

def test_single_thread(stock_codes, start_date, k_type):
    """测试单线程获取多个股票数据"""
    print("=== 单线程测试 ===")
    market = StockMarket()
    start_time = time.time()
    
    results = []
    for code in stock_codes:
        result = market.get_market(stock_code=code, start_date=start_date, k_type=k_type)
        results.append(result)
    
    # 合并结果
    if results:
        df = pd.concat(results, ignore_index=True)
    else:
        df = pd.DataFrame()
    
    end_time = time.time()
    print(f"单线程获取 {len(stock_codes)} 只股票数据耗时: {end_time - start_time:.2f} 秒")
    print(f"获取数据行数: {len(df)}")
    return df, end_time - start_time

def test_multi_thread(stock_codes, start_date, k_type):
    """测试多线程获取多个股票数据"""
    print("\n=== 多线程测试 ===")
    market = StockMarket()
    start_time = time.time()
    
    df = market.get_market(stock_code=stock_codes, start_date=start_date, k_type=k_type)
    
    end_time = time.time()
    print(f"多线程获取 {len(stock_codes)} 只股票数据耗时: {end_time - start_time:.2f} 秒")
    print(f"获取数据行数: {len(df)}")
    return df, end_time - start_time

if __name__ == '__main__':
    import pandas as pd
    
    # 测试参数
    stock_codes = ['000001', '000002', '000858', '002415', '600036', '600519', '000725', '002230']
    start_date = '2024-07-01'
    k_type = 1  # 日K线
    
    print(f"测试股票代码: {stock_codes}")
    print(f"测试时间范围: {start_date} 至今")
    print(f"K线类型: 日K线")
    
    # 单线程测试
    _, single_time = test_single_thread(stock_codes, start_date, k_type)
    
    # 多线程测试
    _, multi_time = test_multi_thread(stock_codes, start_date, k_type)
    
    # 性能对比
    print(f"\n=== 性能对比 ===")
    if multi_time > 0:
        speedup = single_time / multi_time
        print(f"多线程相比单线程加速比: {speedup:.2f}x")
        print(f"时间节省: {(single_time - multi_time):.2f} 秒 ({(1 - multi_time/single_time)*100:.1f}%)")
    else:
        print("无法计算性能比，多线程时间为0")