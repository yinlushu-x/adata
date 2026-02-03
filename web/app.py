# -*- coding: utf-8 -*-
"""
@desc: 股票实时行情Web服务 - 东方财富数据源
@author: AI Assistant
@time: 2025/02/03
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adata.stock.market.stock_market.stock_market_east import StockMarketEast

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

east_market = StockMarketEast()

# 默认热门股票代码（用于演示）
DEFAULT_STOCKS = [
    {'stock_code': '000001', 'stock_name': '平安银行'},
    {'stock_code': '000002', 'stock_name': '万科A'},
    {'stock_code': '000333', 'stock_name': '美的集团'},
    {'stock_code': '000858', 'stock_name': '五粮液'},
    {'stock_code': '002230', 'stock_name': '科大讯飞'},
    {'stock_code': '002594', 'stock_name': '比亚迪'},
    {'stock_code': '300750', 'stock_name': '宁德时代'},
    {'stock_code': '600000', 'stock_name': '浦发银行'},
    {'stock_code': '600036', 'stock_name': '招商银行'},
    {'stock_code': '600519', 'stock_name': '贵州茅台'},
]


def get_current_market_data(stock_codes):
    """获取当前实时行情数据 - 使用东方财富数据源"""
    result = []
    
    # 东方财富接口需要逐个获取，获取最新分时数据的最后一条
    for code in stock_codes:
        try:
            df = east_market.get_market_min(stock_code=code)
            if not df.empty:
                # 获取最新的一条数据
                latest = df.iloc[-1]
                result.append({
                    'stock_code': code,
                    'stock_name': get_stock_name(code),
                    'price': float(latest['price']),
                    'change': float(latest['change']),
                    'change_pct': float(latest['change_pct']),
                    'volume': int(latest['volume']),
                    'amount': float(latest['amount'])
                })
        except Exception as e:
            print(f"获取股票 {code} 行情失败: {e}")
            continue
    
    return result


def get_stock_name(code):
    """根据代码获取股票名称"""
    stock_map = {item['stock_code']: item['stock_name'] for item in DEFAULT_STOCKS}
    return stock_map.get(code, code)


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/top10')
def get_top10():
    """获取热门股票实时行情"""
    try:
        # 获取默认热门股票的实时行情
        stock_codes = [item['stock_code'] for item in DEFAULT_STOCKS]
        current_data = get_current_market_data(stock_codes)

        # 按成交量排序
        current_data.sort(key=lambda x: x['volume'], reverse=True)

        return jsonify({
            'success': True,
            'data': current_data,
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/refresh')
def refresh_data():
    """刷新实时行情数据"""
    return get_top10()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
