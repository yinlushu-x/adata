# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析模块
@author: adata
@time: 2026/2/25
@log: 提供股票日K数据的统计分析功能
"""
from adata.stock.analysis.time_analysis import TimeAnalysis


class Analysis(TimeAnalysis):

    def __init__(self) -> None:
        super().__init__()


analysis = Analysis()
