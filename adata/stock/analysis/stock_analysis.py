# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析
@author: adata
@time: 2026/2/3
@log: change log
"""

import pandas as pd
import numpy as np
from datetime import datetime


class StockAnalysis(object):
    """
    股票数据分析
    """

    def __init__(self) -> None:
        super().__init__()

    def get_weekday_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        分析周一到周五每个交易日的平均收益率、平均成交量以及上涨概率
        
        :param df: 日K数据DataFrame，必须包含 trade_date、open、close、volume 字段
        :return: DataFrame，行为星期维度（周一到周五），列为统计指标
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
        
        df = df[df['weekday'] < 5]
        
        weekday_names = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五'}
        df['weekday_name'] = df['weekday'].map(weekday_names)
        
        stats = df.groupby('weekday_name').agg({
            'daily_return': 'mean',
            'volume': 'mean',
            'is_up': 'mean'
        }).reset_index()
        
        stats.columns = ['星期', '平均收益率', '平均成交量', '上涨概率']
        
        stats['平均收益率'] = stats['平均收益率'].round(6)
        stats['平均成交量'] = stats['平均成交量'].round(2)
        stats['上涨概率'] = stats['上涨概率'].round(4)
        
        weekday_order = ['周一', '周二', '周三', '周四', '周五']
        stats['sort_key'] = stats['星期'].map({name: i for i, name in enumerate(weekday_order)})
        stats = stats.sort_values('sort_key').drop('sort_key', axis=1).reset_index(drop=True)
        
        return stats

    def get_month_period_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        分析每月月初（1-10）、月中（11-20）、月末（21-月最后一天）三个区间的
        平均收益率、平均成交量以及上涨概率
        
        :param df: 日K数据DataFrame，必须包含 trade_date、open、close、volume 字段
        :return: DataFrame，行为月份区间维度，列为统计指标
        """
        if df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        df['is_up'] = df['daily_return'] > 0
        
        df['day_of_month'] = df['trade_date'].dt.day
        
        def get_period(day):
            if 1 <= day <= 10:
                return '月初(1-10日)'
            elif 11 <= day <= 20:
                return '月中(11-20日)'
            else:
                return '月末(21日-月底)'
        
        df['period'] = df['day_of_month'].apply(get_period)
        
        stats = df.groupby('period').agg({
            'daily_return': 'mean',
            'volume': 'mean',
            'is_up': 'mean'
        }).reset_index()
        
        stats.columns = ['月份区间', '平均收益率', '平均成交量', '上涨概率']
        
        stats['平均收益率'] = stats['平均收益率'].round(6)
        stats['平均成交量'] = stats['平均成交量'].round(2)
        stats['上涨概率'] = stats['上涨概率'].round(4)
        
        period_order = {'月初(1-10日)': 0, '月中(11-20日)': 1, '月末(21日-月底)': 2}
        stats['sort_key'] = stats['月份区间'].map(period_order)
        stats = stats.sort_values('sort_key').drop('sort_key', axis=1).reset_index(drop=True)
        
        return stats
