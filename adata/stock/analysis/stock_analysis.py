# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析
@author: adata
@time: 2026/01/30
@log: change log
"""
import pandas as pd


class StockAnalysis(object):
    """
    股票数据分析类，提供基于日K数据的各种统计分析功能
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def _calculate_daily_return(df):
        """
        计算日收益率
        :param df: 包含trade_date, close字段的DataFrame
        :return: 添加了daily_return字段的DataFrame
        """
        df = df.sort_values('trade_date').copy()
        df['prev_close'] = df['close'].shift(1)
        df['daily_return'] = df['close'] / df['prev_close'] - 1
        return df

    def analysis_by_weekday(self, df):
        """
        分析周一到周五每个交易日的平均收益率、平均成交量和上涨概率
        
        :param df: 包含trade_date, close, volume字段的DataFrame
        :return: DataFrame，行为星期维度，列为统计指标
            索引：星期一、星期二、星期三、星期四、星期五
            列：avg_return(平均收益率)、avg_volume(平均成交量)、up_prob(上涨概率)
        """
        if df.empty:
            return pd.DataFrame()
        
        required_columns = ['trade_date', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame必须包含{col}字段")
        
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        df = self._calculate_daily_return(df)
        
        df['weekday'] = df['trade_date'].dt.dayofweek
        df = df[df['weekday'] < 5]
        
        weekday_names = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五'}
        df['weekday_name'] = df['weekday'].map(weekday_names)
        
        result = df.groupby('weekday').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('daily_return', lambda x: (x > 0).sum() / len(x)),
            count=('daily_return', 'count')
        ).reset_index()
        
        result['weekday_name'] = result['weekday'].map(weekday_names)
        result = result.set_index('weekday_name')
        result = result[['avg_return', 'avg_volume', 'up_prob', 'count']]
        result = result.reindex(['星期一', '星期二', '星期三', '星期四', '星期五'])
        
        result.index.name = '星期'
        
        return result

    def analysis_by_month_period(self, df):
        """
        分析每月月初（1-10）、月中（11-20）、月末（21-月末）三个区间的统计数据
        
        :param df: 包含trade_date, close, volume字段的DataFrame
        :return: DataFrame，行为月度区间，列为统计指标
            索引：月初(1-10)、月中(11-20)、月末(21-)
            列：avg_return(平均收益率)、avg_volume(平均成交量)、up_prob(上涨概率)
        """
        if df.empty:
            return pd.DataFrame()
        
        required_columns = ['trade_date', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame必须包含{col}字段")
        
        df = df.copy()
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        df = self._calculate_daily_return(df)
        
        df['day_of_month'] = df['trade_date'].dt.day
        
        def get_month_period(day):
            if day <= 10:
                return '月初(1-10)'
            elif day <= 20:
                return '月中(11-20)'
            else:
                return '月末(21-)'
        
        df['month_period'] = df['day_of_month'].apply(get_month_period)
        
        result = df.groupby('month_period').agg(
            avg_return=('daily_return', 'mean'),
            avg_volume=('volume', 'mean'),
            up_prob=('daily_return', lambda x: (x > 0).sum() / len(x)),
            count=('daily_return', 'count')
        ).reset_index()
        
        period_order = ['月初(1-10)', '月中(11-20)', '月末(21-)']
        result = result.set_index('month_period')
        result = result.reindex(period_order)
        
        result.index.name = '月度区间'
        result = result[['avg_return', 'avg_volume', 'up_prob', 'count']]
        
        return result


if __name__ == '__main__':
    import numpy as np
    
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='B')
    test_data = pd.DataFrame({
        'trade_date': dates,
        'close': np.random.uniform(10, 20, len(dates)),
        'volume': np.random.randint(1000000, 10000000, len(dates))
    })
    test_data['open'] = test_data['close'] * np.random.uniform(0.95, 1.05, len(dates))
    
    analysis = StockAnalysis()
    
    print("=" * 50)
    print("按星期分析结果：")
    print("=" * 50)
    weekday_result = analysis.analysis_by_weekday(test_data)
    print(weekday_result)
    print("\n")
    
    print("=" * 50)
    print("按月度区间分析结果：")
    print("=" * 50)
    month_result = analysis.analysis_by_month_period(test_data)
    print(month_result)
