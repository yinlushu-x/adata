#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多线程装饰器功能
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
from adata.stock.market.stock_market.stock_market import StockMarket

def test_single_stock():
    """测试单个股票获取"""
    print("\n=== 测试单个股票获取 ===")
    start_time = time.time()
    df = StockMarket().get_market(stock_code='000001', start_date='2024-07-01', k_type=1)
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f}秒")
    print(f"返回数据行数: {len(df)}")
    if len(df) > 0:
        print(df.head(3))
    return len(df) > 0

def test_batch_stocks():
    """测试批量股票获取"""
    print("\n=== 测试批量股票获取（多线程） ===")
    start_time = time.time()
    df = StockMarket().get_market(stock_code=['000001', '000002', '000004'], start_date='2024-07-01', k_type=1)
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f}秒")
    print(f"返回数据总行数: {len(df)}")
    
    # 统计每个股票的数据行数
    if len(df) > 0:
        stock_counts = df['stock_code'].value_counts()
        print(f"各股票数据行数: {stock_counts.to_dict()}")
        print(df.head(5))
    
    return len(df) > 0

if __name__ == '__main__':
    print("测试多线程装饰器功能")
    print("=" * 50)
    
    # 测试单个股票
    if not test_single_stock():
        print("\n单个股票获取测试失败!")
    else:
        print("\n单个股票获取测试成功!")
    
    # 测试批量股票
    if not test_batch_stocks():
        print("\n批量股票获取测试失败!")
    else:
        print("\n批量股票获取测试成功!")
    
    print("\n" + "=" * 50)
    print("所有测试完成!")
