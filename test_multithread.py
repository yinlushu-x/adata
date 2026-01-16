from adata.stock.market.stock_market.stock_market import StockMarket
import time

start = time.time()
df = StockMarket().get_market(stock_code=['000001', '600000', '000795'], start_date='2024-07-22')
print(f'获取数据耗时: {time.time() - start}秒')
print(df)