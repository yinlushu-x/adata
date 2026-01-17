#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""

import time
from adata.common.utils import requests

def test_rate_limit():
    """
    测试频率限制功能
    """
    print("测试频率限制功能...")
    
    # 设置测试域名的频率限制为每分钟5次
    test_domain = "httpbin.org"
    requests.set_rate_limit(test_domain, 5)
    print(f"设置 {test_domain} 的频率限制为每分钟5次")
    
    # 发送6个请求，看看是否会被限制
    start_time = time.time()
    for i in range(6):
        request_start = time.time()
        print(f"\n请求 {i+1} 开始时间: {time.strftime('%H:%M:%S')}")
        
        try:
            # 使用httpbin.org的延迟接口
            url = f"https://httpbin.org/delay/1"
            response = requests.request('get', url, timeout=10)
            print(f"请求 {i+1} 完成，状态码: {response.status_code}")
        except Exception as e:
            print(f"请求 {i+1} 失败: {e}")
        
        request_end = time.time()
        print(f"请求 {i+1} 耗时: {request_end - request_start:.2f} 秒")
    
    total_time = time.time() - start_time
    print(f"\n总耗时: {total_time:.2f} 秒")
    print(f"平均请求间隔: {total_time / 6:.2f} 秒")
    
    # 如果频率限制生效，第6个请求应该会等待大约12秒（因为每分钟5次，平均12秒一次）
    # 所以总耗时应该在 6（请求延迟） + 12（等待时间）= 18秒左右
    if total_time > 15:
        print("\n✓ 频率限制功能正常工作！")
    else:
        print("\n✗ 频率限制功能可能没有正常工作")

if __name__ == "__main__":
    test_rate_limit()