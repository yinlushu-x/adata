# -*- coding: utf-8 -*-
"""
测试均线突破 + 成交量确认信号检测模块
"""
from adata.stock.market import detect_ma_breakout_signal

if __name__ == '__main__':
    # 测试示例1：平安银行(000001)
    print("=== 测试1：平安银行(000001) ===")
    detect_ma_breakout_signal('000001', '2024-01-01', '2024-06-30')
    
    # 测试示例2：贵州茅台(600519)
    print("\n=== 测试2：贵州茅台(600519) ===")
    detect_ma_breakout_signal('600519', '2024-01-01', '2024-06-30')
    
    # 测试示例3：腾讯控股(0700.HK)
    print("\n=== 测试3：腾讯控股(0700.HK) ===")
    detect_ma_breakout_signal('0700.HK', '2024-01-01', '2024-06-30')