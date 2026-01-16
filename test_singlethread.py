from adata.stock.market.stock_market.stock_market import StockMarket
import time
import pandas as pd

start = time.time()
df1 = StockMarket().get_market(stock_code='000001', start_date='2024-07-22')
df2 = StockMarket().get_market(stock_code='600000', start_date='2024-07-22')
df3 = StockMarket().get_market(stock_code='000795', start_date='2024-07-22')
df = pd.concat([df1, df2, df3], ignore_index=True)
print(f'获取数据耗时: {time.time() - start}秒')
print(df)