# -*- coding: utf-8 -*-
"""
@desc: 股票市场数据分析测试
@author: 1nchaos
@time: 2026/01/16
@log: change log
"""

import sys
sys.path.insert(0, '/Users/mars/disk/test_back/adata_g4')

from adata.stock.market.stock_market_analysis import StockMarketAnalysis
from adata.stock.market.stock_market.stock_market import StockMarket


def test_analyze_by_weekday():
    """
    测试按星期维度分析功能
    """
    stock_code = '000001'
    start_date = '2020-01-01'
    end_date = '2024-12-31'

    market = StockMarket()
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)

    analysis = StockMarketAnalysis()
    result = analysis.analyze_by_weekday(df)

    print("按星期维度分析：")
    print(result)
    print()

    assert result is not None, "结果不能为空"
    assert result.shape[0] == 5, "应该有5个星期"
    assert '平均收益率' in result.columns, "应该包含平均收益率列"
    assert '平均成交量' in result.columns, "应该包含平均成交量列"
    assert '上涨概率' in result.columns, "应该包含上涨概率列"

    print("按星期维度分析测试通过！")
    return result


def test_analyze_by_month_period():
    """
    测试按月份区间分析功能
    """
    stock_code = '000001'
    start_date = '2020-01-01'
    end_date = '2024-12-31'

    market = StockMarket()
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)

    analysis = StockMarketAnalysis()
    result = analysis.analyze_by_month_period(df)

    print("按月份区间分析：")
    print(result)
    print()

    assert result is not None, "结果不能为空"
    assert result.shape[0] == 3, "应该有3个月份区间"
    assert '平均收益率' in result.columns, "应该包含平均收益率列"
    assert '平均成交量' in result.columns, "应该包含平均成交量列"
    assert '上涨概率' in result.columns, "应该包含上涨概率列"

    print("按月份区间分析测试通过！")
    return result


def test_empty_dataframe():
    """
    测试空DataFrame的情况
    """
    import pandas as pd

    analysis = StockMarketAnalysis()

    empty_df = pd.DataFrame()
    weekday_result = analysis.analyze_by_weekday(empty_df)
    month_period_result = analysis.analyze_by_month_period(empty_df)

    assert weekday_result.empty, "空DataFrame应该返回空结果"
    assert month_period_result.empty, "空DataFrame应该返回空结果"

    print("空DataFrame测试通过！")


if __name__ == '__main__':
    test_analyze_by_weekday()
    test_analyze_by_month_period()
    test_empty_dataframe()

    print("\n所有测试通过！")
