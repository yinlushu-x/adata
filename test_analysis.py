# -*- coding: utf-8 -*-
"""
测试股票时间维度分析功能
"""
import adata

# 获取股票日K数据
print("=" * 60)
print("获取股票日K数据: 000001 平安银行")
print("=" * 60)
df = adata.stock.market.get_market(stock_code='000001', start_date='2023-01-01', k_type=1)
print(f"数据条数: {len(df)}")
print("\n数据预览:")
print(df.head(10))
print("\n数据列:", df.columns.tolist())

# 测试1: 星期维度分析
print("\n" + "=" * 60)
print("功能1: 星期维度统计分析")
print("=" * 60)
weekday_stats = adata.stock.analysis.analyze_by_weekday(df)
print("\n星期维度统计结果:")
print(weekday_stats)

# 测试2: 月内区间分析
print("\n" + "=" * 60)
print("功能2: 月内区间统计分析")
print("=" * 60)
month_period_stats = adata.stock.analysis.analyze_by_month_period(df)
print("\n月内区间统计结果:")
print(month_period_stats)

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
