# -*- coding: utf-8 -*-
from adata.common.utils import requests as adata_requests
from adata.common.utils.date_utils import get_cur_time

# 测试adata的requests工具
def test_adata_requests():
    stock_code = '000333'
    se_cid = 1 if stock_code.startswith('6') else 0
    start_date = '20240101'
    end_date = get_cur_time("%Y%m%d")
    k_type = 1
    k_type = f"10{k_type}" if int(k_type) < 5 else k_type
    adjust_type = 1
    
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "klt": k_type, 
        "fqt": adjust_type,
        "secid": f"{se_cid}.{stock_code}",
        "beg": start_date, 
        "end": end_date,
        "_": "1623766962675",
    }
    
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    print(f"请求URL: {url}")
    print(f"请求参数: {params}")
    
    # 使用adata的requests工具请求
    try:
        r = adata_requests.request(method='get', url=url, params=params)
        print(f"状态码: {r.status_code}")
        print(f"响应头: {r.headers}")
        print(f"响应内容: {r.text[:1000]}...")
        
        data_json = r.json()
        print(f"JSON解析结果: {data_json}")
        if data_json.get('data'):
            print(f"klines长度: {len(data_json['data'].get('klines', []))}")
            # 测试数据处理逻辑
            lines = data_json["data"]["klines"]
            data = [item.split(",") for item in lines]
            print(f"数据长度: {len(data)}")
            print(f"第一条数据: {data[0]}")
            print(f"最后一条数据: {data[-1]}")
    except Exception as e:
        print(f"请求错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_adata_requests()
