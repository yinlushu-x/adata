# -*- coding: utf-8 -*-
"""
@desc: 股票时间维度分析模块
@author: adata
@time: 2026/2/25
@log: 提供基于星期维度和月内区间的统计分析功能
"""
import pandas as pd
import numpy as np
from datetime import datetime
from calendar import monthrange


class TimeAnalysis(object):
    """
    股票时间维度分析类
    提供基于星期维度和月内区间的统计分析功能
    """

    def __init__(self) -> None:
        super().__init__()

    def _calc_daily_return(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算日收益率
        :param df: 包含trade_date, open, close, volume的数据框
        :return: 添加了daily_return列的数据框
        """
        df = df.copy()
        df = df.sort_values('trade_date').reset_index(drop=True)
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        return df.dropna(subset=['daily_return'])

    def _add_weekday(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加星期几列
        :param df: 数据框
        :return: 添加了weekday列的数据框
        """
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['weekday'] = df['trade_date'].dt.dayofweek
        df['weekday_name'] = df['trade_date'].dt.day_name()
        return df

    def _add_month_period(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加月内区间列
        :param df: 数据框
        :return: 添加了month_period列的数据框
        """
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['day'] = df['trade_date'].dt.day
        df['days_in_month'] = df['trade_date'].apply(lambda x: monthrange(x.year, x.month)[1])

        def get_period(row):
            if row['day'] <= 10:
                return '月初(1-10日)'
            elif row['day'] <= 20:
                return '月中(11-20日)'
            else:
                return '月末(21日-月底)'

        df['month_period'] = df.apply(get_period, axis=1)
        return df

    def analyze_by_weekday(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        分析周一到周五每个交易日的平均收益率、平均成交量以及上涨概率

        :param df: 股票日K数据，需包含trade_date, open, close, volume字段
        :return: DataFrame，行为星期维度，列为统计指标
                 统计指标包括：平均收益率、平均成交量、上涨概率、交易天数
        """
        if df.empty:
            return pd.DataFrame()

        required_cols = ['trade_date', 'open', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"数据缺少必要字段: {col}")

        df = self._calc_daily_return(df)
        df = self._add_weekday(df)

        weekday_names = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五'}

        result_data = []
        for weekday in range(5):
            weekday_df = df[df['weekday'] == weekday]
            if weekday_df.empty:
                continue

            avg_return = weekday_df['daily_return'].mean()
            avg_volume = weekday_df['volume'].mean()
            up_prob = (weekday_df['daily_return'] > 0).mean()
            trade_days = len(weekday_df)

            result_data.append({
                '星期': weekday_names.get(weekday, f'星期{weekday + 1}'),
                '平均收益率': round(avg_return, 6),
                '平均收益率(%)': round(avg_return * 100, 4),
                '平均成交量': int(avg_volume),
                '上涨概率': round(up_prob, 4),
                '上涨概率(%)': round(up_prob * 100, 2),
                '交易天数': trade_days
            })

        result_df = pd.DataFrame(result_data)
        if not result_df.empty:
            result_df.set_index('星期', inplace=True)

        return result_df

    def analyze_by_month_period(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        分析每月月初、月中、月末三个区间的平均收益率、平均成交量以及上涨概率

        :param df: 股票日K数据，需包含trade_date, open, close, volume字段
        :return: DataFrame，行为月内区间维度，列为统计指标
                 统计指标包括：平均收益率、平均成交量、上涨概率、交易天数
        """
        if df.empty:
            return pd.DataFrame()

        required_cols = ['trade_date', 'open', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"数据缺少必要字段: {col}")

        df = self._calc_daily_return(df)
        df = self._add_month_period(df)

        period_order = ['月初(1-10日)', '月中(11-20日)', '月末(21日-月底)']

        result_data = []
        for period in period_order:
            period_df = df[df['month_period'] == period]
            if period_df.empty:
                continue

            avg_return = period_df['daily_return'].mean()
            avg_volume = period_df['volume'].mean()
            up_prob = (period_df['daily_return'] > 0).mean()
            trade_days = len(period_df)

            result_data.append({
                '月内区间': period,
                '平均收益率': round(avg_return, 6),
                '平均收益率(%)': round(avg_return * 100, 4),
                '平均成交量': int(avg_volume),
                '上涨概率': round(up_prob, 4),
                '上涨概率(%)': round(up_prob * 100, 2),
                '交易天数': trade_days
            })

        result_df = pd.DataFrame(result_data)
        if not result_df.empty:
            result_df.set_index('月内区间', inplace=True)

        return result_df
