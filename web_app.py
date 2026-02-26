# -*- coding: utf-8 -*-
"""
@desc: Web应用 - 显示昨日成交量前十股票的实时行情
@author: adata
@time: 2025/02/26
"""

import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify

import adata

app = Flask(__name__)


def get_yesterday_top_volume_stocks(top_n=10):
    """
    获取昨日成交量前十的股票代码
    :param top_n: 前N名
    :return: 股票代码列表
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        df = adata.stock.market.get_market(stock_code='000001', start_date=yesterday, end_date=yesterday, k_type=1)
    except Exception:
        pass
    
    all_stocks = adata.stock.info.all_code()
    if all_stocks.empty:
        return []
    
    stock_codes = all_stocks['stock_code'].tolist()
    stock_codes = [code for code in stock_codes if code.startswith(('0', '3', '6'))]
    
    volume_data = []
    batch_size = 100
    
    for i in range(0, min(len(stock_codes), 500), batch_size):
        batch_codes = stock_codes[i:i + batch_size]
        try:
            for code in batch_codes:
                try:
                    df = adata.stock.market.get_market(stock_code=code, start_date=yesterday, end_date=yesterday, k_type=1)
                    if not df.empty and 'volume' in df.columns:
                        volume = float(df['volume'].iloc[-1]) if len(df) > 0 else 0
                        if volume > 0:
                            volume_data.append({
                                'stock_code': code,
                                'volume': volume
                            })
                except Exception:
                    continue
        except Exception:
            continue
    
    volume_data.sort(key=lambda x: x['volume'], reverse=True)
    return [item['stock_code'] for item in volume_data[:top_n]]


def get_realtime_market_data(stock_codes):
    """
    获取股票实时行情数据
    :param stock_codes: 股票代码列表
    :return: 实时行情数据列表
    """
    if not stock_codes:
        return []
    
    try:
        df = adata.stock.market.list_market_current(code_list=stock_codes)
        if df.empty:
            return []
        
        result = []
        for _, row in df.iterrows():
            try:
                change_pct = float(row.get('change_pct', 0)) if row.get('change_pct') else 0
                volume = float(row.get('volume', 0)) if row.get('volume') else 0
                amount = float(row.get('amount', 0)) if row.get('amount') else 0
                price = float(row.get('price', 0)) if row.get('price') else 0
                change = float(row.get('change', 0)) if row.get('change') else 0
                
                result.append({
                    'stock_code': row.get('stock_code', ''),
                    'short_name': row.get('short_name', ''),
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'change_pct': round(change_pct, 2),
                    'volume': format_volume(volume),
                    'amount': format_amount(amount),
                    'is_up': change_pct > 0,
                    'is_down': change_pct < 0
                })
            except Exception:
                continue
        
        return result
    except Exception as e:
        print(f"获取实时行情失败: {e}")
        return []


def format_volume(volume):
    """
    格式化成交量
    """
    try:
        volume = float(volume)
        if volume >= 100000000:
            return f"{volume / 100000000:.2f}亿"
        elif volume >= 10000:
            return f"{volume / 10000:.2f}万"
        else:
            return f"{volume:.0f}"
    except Exception:
        return "0"


def format_amount(amount):
    """
    格式化成交额
    """
    try:
        amount = float(amount)
        if amount >= 100000000:
            return f"{amount / 100000000:.2f}亿"
        elif amount >= 10000:
            return f"{amount / 10000:.2f}万"
        else:
            return f"{amount:.2f}"
    except Exception:
        return "0"


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/realtime')
def api_realtime():
    """获取实时行情API"""
    stock_codes = get_yesterday_top_volume_stocks(10)
    data = get_realtime_market_data(stock_codes)
    return jsonify({
        'success': True,
        'data': data,
        'update_time': datetime.now().strftime('%H:%M:%S')
    })


@app.route('/api/demo')
def api_demo():
    """演示数据API（用于测试）"""
    demo_data = [
        {'stock_code': '000001', 'short_name': '平安银行', 'price': 15.68, 'change': 0.35, 'change_pct': 2.28, 'volume': '1.25亿', 'amount': '19.52亿', 'is_up': True, 'is_down': False},
        {'stock_code': '600519', 'short_name': '贵州茅台', 'price': 1856.00, 'change': -12.50, 'change_pct': -0.67, 'volume': '856万', 'amount': '158.92亿', 'is_up': False, 'is_down': True},
        {'stock_code': '000858', 'short_name': '五粮液', 'price': 168.50, 'change': 3.20, 'change_pct': 1.94, 'volume': '3256万', 'amount': '54.78亿', 'is_up': True, 'is_down': False},
        {'stock_code': '601318', 'short_name': '中国平安', 'price': 48.65, 'change': 0.85, 'change_pct': 1.78, 'volume': '8956万', 'amount': '43.52亿', 'is_up': True, 'is_down': False},
        {'stock_code': '600036', 'short_name': '招商银行', 'price': 35.28, 'change': -0.42, 'change_pct': -1.18, 'volume': '5621万', 'amount': '19.86亿', 'is_up': False, 'is_down': True},
        {'stock_code': '000333', 'short_name': '美的集团', 'price': 68.90, 'change': 1.25, 'change_pct': 1.85, 'volume': '2890万', 'amount': '19.92亿', 'is_up': True, 'is_down': False},
        {'stock_code': '601888', 'short_name': '中国中免', 'price': 98.50, 'change': -2.30, 'change_pct': -2.28, 'volume': '4521万', 'amount': '44.52亿', 'is_up': False, 'is_down': True},
        {'stock_code': '002594', 'short_name': '比亚迪', 'price': 268.50, 'change': 5.80, 'change_pct': 2.21, 'volume': '1890万', 'amount': '50.78亿', 'is_up': True, 'is_down': False},
        {'stock_code': '300750', 'short_name': '宁德时代', 'price': 198.60, 'change': 4.50, 'change_pct': 2.32, 'volume': '2156万', 'amount': '42.78亿', 'is_up': True, 'is_down': False},
        {'stock_code': '600900', 'short_name': '长江电力', 'price': 28.95, 'change': 0.25, 'change_pct': 0.87, 'volume': '6852万', 'amount': '19.85亿', 'is_up': True, 'is_down': False},
    ]
    return jsonify({
        'success': True,
        'data': demo_data,
        'update_time': datetime.now().strftime('%H:%M:%S')
    })


if __name__ == '__main__':
    print("启动股票实时行情Web服务...")
    print("请访问: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5001, debug=True)
