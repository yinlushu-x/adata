# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析模块
@author: adata
@time: 2026/2/3
@log: change log
"""
from adata.stock.analysis.stock_analysis import StockAnalysis


class Analysis(StockAnalysis):

    def __init__(self) -> None:
        super().__init__()


analysis = Analysis()
