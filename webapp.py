# -*- coding: utf-8 -*-
"""
股票行情Web应用
展示昨日成交量前十名股票的实时行情数据
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
from adata.stock.market.stock_market.stock_market import StockMarket
from adata.stock.info.stock_code import StockCode

app = Flask(__name__)

# 获取昨日成交量前十的股票代码
def get_top_volume_stocks():
    """
    获取昨日成交量前十的股票代码
    """
    try:
        # 获取所有股票代码
        stock_code = StockCode()
        all_stocks = stock_code.all_code()
        print(f"获取到 {len(all_stocks)} 只股票")
        
        # 获取昨日日期
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"昨日日期: {yesterday}")
        
        # 获取股票市场数据
        top_stocks = []
        
        # 这里简化处理，实际应用中可能需要分批获取数据
        # 取前100只股票作为示例，实际应用中可能需要获取更多
        if not all_stocks.empty:
            sample_stocks = all_stocks['stock_code'].head(100).tolist()
            print(f"获取前100只股票的行情数据")
            print(f"股票代码示例: {sample_stocks[:5]}")
            
            # 直接使用新浪API获取数据
            import requests
            from adata.common.headers import sina_headers
            from adata.common.utils import code_utils
            
            # 构建API URL
            api_url = 'https://hq.sinajs.cn/list='
            for code in sample_stocks:
                api_url += f's_{code_utils.get_exchange_by_stock_code(code).lower()}{code},'
            
            # 请求接口
            res = requests.request('get', api_url, headers=sina_headers.c_headers)
            
            # 解析数据
            data_list = res.text.split(';')
            data = []
            for data_str in data_list:
                if len(data_str) < 8 or '=' not in data_str:
                    continue
                idx = data_str.index('=')
                code = [data_str[idx - 6:idx]]
                code.extend(data_str[idx + 2:-1].split(','))
                if len(code) == 7:
                    data.append(code)
            
            # 转换为DataFrame
            columns = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']
            market_data = pd.DataFrame(data=data, columns=columns)
            
            # 转换数据类型
            market_data['price'] = pd.to_numeric(market_data['price'], errors='coerce')
            market_data['change'] = pd.to_numeric(market_data['change'], errors='coerce')
            market_data['change_pct'] = pd.to_numeric(market_data['change_pct'], errors='coerce')
            market_data['volume'] = pd.to_numeric(market_data['volume'], errors='coerce')
            market_data['amount'] = pd.to_numeric(market_data['amount'], errors='coerce')
            
            print(f"获取到 {len(market_data)} 只股票的行情数据")
            
            if not market_data.empty:
                # 按成交量排序，取前10
                top_stocks = market_data.nlargest(10, 'volume')['stock_code'].tolist()
                print(f"成交量前十的股票: {top_stocks}")
            else:
                print("未获取到行情数据，使用默认股票代码")
                top_stocks = ['000001', '000002', '600000', '600036', '000858', '002415', '000725', '600519', '002594', '600276']
        
        return top_stocks
    except Exception as e:
        print(f"获取热门股票失败: {e}")
        import traceback
        traceback.print_exc()
        # 返回一些默认股票代码
        return ['000001', '000002', '600000', '600036', '000858', '002415', '000725', '600519', '002594', '600276']

# 获取股票实时行情数据
def get_stock_market_data(stock_codes):
    """
    获取指定股票的实时行情数据
    """
    try:
        # 直接使用新浪API获取数据
        import requests
        from adata.common.headers import sina_headers
        from adata.common.utils import code_utils
        
        # 构建API URL
        api_url = 'https://hq.sinajs.cn/list='
        for code in stock_codes:
            api_url += f's_{code_utils.get_exchange_by_stock_code(code).lower()}{code},'
        
        # 请求接口
        res = requests.request('get', api_url, headers=sina_headers.c_headers)
        
        # 解析数据
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8 or '=' not in data_str:
                continue
            idx = data_str.index('=')
            code = [data_str[idx - 6:idx]]
            code.extend(data_str[idx + 2:-1].split(','))
            if len(code) == 7:
                data.append(code)
        
        # 转换为DataFrame
        columns = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']
        market_data = pd.DataFrame(data=data, columns=columns)
        
        # 转换数据类型
        market_data['price'] = pd.to_numeric(market_data['price'], errors='coerce')
        market_data['change'] = pd.to_numeric(market_data['change'], errors='coerce')
        market_data['change_pct'] = pd.to_numeric(market_data['change_pct'], errors='coerce')
        market_data['volume'] = pd.to_numeric(market_data['volume'], errors='coerce')
        market_data['amount'] = pd.to_numeric(market_data['amount'], errors='coerce')
        
        if market_data.empty:
            return []
        
        # 转换为字典列表，便于前端处理
        result = []
        for _, row in market_data.iterrows():
            # 格式化涨跌幅，添加颜色标识
            change_pct = float(row['change_pct'])
            change_class = 'positive' if change_pct > 0 else 'negative' if change_pct < 0 else 'neutral'
            
            # 格式化成交量和成交额
            volume = int(row['volume'])
            amount = float(row['amount'])
            
            # 格式化成交量为万手或亿手
            if volume >= 100000000:
                volume_str = f"{volume/100000000:.2f}亿手"
            elif volume >= 10000:
                volume_str = f"{volume/10000:.2f}万手"
            else:
                volume_str = f"{volume}手"
            
            # 格式化成交额为亿元或万元
            if amount >= 100000000:
                amount_str = f"{amount/100000000:.2f}亿元"
            elif amount >= 10000:
                amount_str = f"{amount/10000:.2f}万元"
            else:
                amount_str = f"{amount:.2f}元"
            
            stock_info = {
                'code': row['stock_code'],
                'name': row['short_name'],
                'price': f"{float(row['price']):.2f}",
                'change': f"{float(row['change']):.2f}",
                'change_pct': f"{change_pct:.2f}%",
                'change_class': change_class,
                'volume': volume_str,
                'amount': amount_str,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            result.append(stock_info)
        
        return result
    except Exception as e:
        print(f"获取行情数据失败: {e}")
        import traceback
        traceback.print_exc()
        return []

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/top_stocks')
def api_top_stocks():
    """获取昨日成交量前十的股票实时行情API"""
    # 获取昨日成交量前十的股票代码
    top_stocks = get_top_volume_stocks()
    
    # 获取这些股票的实时行情数据
    market_data = get_stock_market_data(top_stocks)
    
    return jsonify({
        'status': 'success',
        'data': market_data,
        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 确保static目录存在
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=8080)