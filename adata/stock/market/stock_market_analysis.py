# -*- coding: utf-8 -*-
"""
@desc: 股票市场数据分析
@author: 1nchaos
@time: 2026/01/16
@log: change log
"""

import pandas as pd


class StockMarketAnalysis(object):
    """
    股票市场数据分析
    """

    def __init__(self) -> None:
        super().__init__()

    def analyze_by_weekday(self, df: pd.DataFrame):
        """
        按星期维度分析股票数据
        :param df: 股票日K数据，包含字段：trade_date, open, close, volume
        :return: DataFrame，行为星期维度，列为统计指标（平均收益率、平均成交量、上涨概率）
        """
        if df.empty:
            return pd.DataFrame()

        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')

        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['is_up'] = df['daily_return'] > 0
        df['weekday'] = df['trade_date'].dt.dayofweek

        df = df.dropna(subset=['daily_return'])

        weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五'}
        df['weekday_name'] = df['weekday'].map(weekday_map)

        result = df.groupby('weekday_name').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('is_up', 'mean')
        ).reindex(['周一', '周二', '周三', '周四', '周五'])

        result['avg_return'] = result['avg_return'].apply(lambda x: f'{x:.4f}')
        result['avg_volume'] = result['avg_volume'].apply(lambda x: f'{x:.0f}')
        result['up_prob'] = result['up_prob'].apply(lambda x: f'{x:.4f}')

        result.columns = ['平均收益率', '平均成交量', '上涨概率']

        return result

    def analyze_by_month_period(self, df: pd.DataFrame):
        """
        按月份区间分析股票数据
        :param df: 股票日K数据，包含字段：trade_date, open, close, volume
        :return: DataFrame，行为月份区间维度，列为统计指标（平均收益率、平均成交量、上涨概率）
        """
        if df.empty:
            return pd.DataFrame()

        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')

        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['is_up'] = df['daily_return'] > 0
        df['day'] = df['trade_date'].dt.day

        def get_month_period(day):
            if day <= 10:
                return '月初(1-10日)'
            elif day <= 20:
                return '月中(11-20日)'
            else:
                return '月末(21-月底)'

        df['month_period'] = df['day'].apply(get_month_period)

        df = df.dropna(subset=['daily_return'])

        result = df.groupby('month_period').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('is_up', 'mean')
        ).reindex(['月初(1-10日)', '月中(11-20日)', '月末(21-月底)'])

        result['avg_return'] = result['avg_return'].apply(lambda x: f'{x:.4f}')
        result['avg_volume'] = result['avg_volume'].apply(lambda x: f'{x:.0f}')
        result['up_prob'] = result['up_prob'].apply(lambda x: f'{x:.4f}')

        result.columns = ['平均收益率', '平均成交量', '上涨概率']

        return result


if __name__ == '__main__':
    from adata.stock.market.stock_market.stock_market import StockMarket

    stock_code = '000001'
    start_date = '2020-01-01'
    end_date = '2024-12-31'

    market = StockMarket()
    df = market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date, k_type=1)

    analysis = StockMarketAnalysis()

    print("按星期维度分析：")
    weekday_result = analysis.analyze_by_weekday(df)
    print(weekday_result)

    print("\n按月份区间分析：")
    month_period_result = analysis.analyze_by_month_period(df)
    print(month_period_result)
