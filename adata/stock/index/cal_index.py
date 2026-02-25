# -*- coding: utf-8 -*-
"""
@desc: 指标计算
@author: 1nchaos
@time: 2023/5/23
@log: change log
"""
import pandas as pd


class CalIndex(object):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def weekday_stats(df):
        """
        分析周一到周五每个交易日的平均收益率、平均成交量和上涨概率
        :param df: 包含 trade_date, close, volume 字段的日K数据DataFrame
        :return: DataFrame，行为星期（周一到周五），列为统计指标
        """
        if df.empty:
            return pd.DataFrame()

        data = df.copy()
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data['daily_return'] = data['close'] / data['close'].shift(1) - 1
        data['is_up'] = (data['daily_return'] > 0).astype(int)
        data['weekday'] = data['trade_date'].dt.dayofweek
        data = data.dropna(subset=['daily_return'])

        weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五'}
        data['weekday_name'] = data['weekday'].map(weekday_map)

        result = data.groupby('weekday').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('is_up', 'mean'),
            sample_count=('daily_return', 'count')
        ).reset_index()

        result['weekday_name'] = result['weekday'].map(weekday_map)
        result = result.set_index('weekday_name')
        result = result.reindex(['周一', '周二', '周三', '周四', '周五'])
        result = result.drop(columns=['weekday'])

        result['avg_return'] = result['avg_return'].round(4)
        result['avg_volume'] = result['avg_volume'].round(0).astype(int)
        result['up_prob'] = (result['up_prob'] * 100).round(2)

        result = result.rename(columns={
            'avg_return': '平均收益率',
            'avg_volume': '平均成交量',
            'up_prob': '上涨概率(%)',
            'sample_count': '样本数量'
        })
        result.index.name = '星期'

        return result

    @staticmethod
    def month_period_stats(df):
        """
        分析每月月初（1-10）、月中（11-20）、月末（21-月最后一天）的平均收益率、平均成交量和上涨概率
        :param df: 包含 trade_date, close, volume 字段的日K数据DataFrame
        :return: DataFrame，行为月份区间，列为统计指标
        """
        if df.empty:
            return pd.DataFrame()

        data = df.copy()
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data['daily_return'] = data['close'] / data['close'].shift(1) - 1
        data['is_up'] = (data['daily_return'] > 0).astype(int)
        data['day'] = data['trade_date'].dt.day
        data = data.dropna(subset=['daily_return'])

        def get_month_period(day):
            if day <= 10:
                return '月初(1-10)'
            elif day <= 20:
                return '月中(11-20)'
            else:
                return '月末(21-月末)'

        data['month_period'] = data['day'].apply(get_month_period)

        result = data.groupby('month_period').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('is_up', 'mean'),
            sample_count=('daily_return', 'count')
        ).reset_index()

        period_order = ['月初(1-10)', '月中(11-20)', '月末(21-月末)']
        result = result.set_index('month_period')
        result = result.reindex(period_order)

        result['avg_return'] = result['avg_return'].round(4)
        result['avg_volume'] = result['avg_volume'].round(0).astype(int)
        result['up_prob'] = (result['up_prob'] * 100).round(2)

        result = result.rename(columns={
            'avg_return': '平均收益率',
            'avg_volume': '平均成交量',
            'up_prob': '上涨概率(%)',
            'sample_count': '样本数量'
        })
        result.index.name = '月份区间'

        return result
