# -*- coding: utf-8 -*-
"""
@desc: 股票数据分析
@author: adata
@time: 2026/01/30
@log: change log
"""
from adata.stock.analysis.stock_analysis import StockAnalysis


class Analysis(object):

    def __init__(self) -> None:
        self.stock_analysis = StockAnalysis()


analysis = Analysis()
