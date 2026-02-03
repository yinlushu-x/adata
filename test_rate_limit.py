# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""
import time
import adata
from adata.common.utils import requests

# 测试1: 设置频率限制
print("=" * 50)
print("测试1: 设置频率限制")
print("=" * 50)

# 设置所有域名默认每分钟5次请求
adata.set_rate_limit('*', max_requests=5, window_seconds=60)
print("已设置全局默认限制: 每分钟5次请求")

# 设置特定域名每分钟2次
adata.set_rate_limit('httpbin.org', max_requests=2, window_seconds=60)
print("已设置 httpbin.org 限制: 每分钟2次请求")

# 测试2: 验证频率限制
print("\n" + "=" * 50)
print("测试2: 验证频率限制 ( httpbin.org 限制每分钟2次 )")
print("=" * 50)

url = "https://httpbin.org/get"
start_time = time.time()

for i in range(4):
    req_start = time.time()
    try:
        res = requests.request('get', url=url, timeout=10)
        elapsed = time.time() - req_start
        total_elapsed = time.time() - start_time
        print(f"请求 {i+1}: 状态={res.status_code}, 耗时={elapsed:.2f}s, 总耗时={total_elapsed:.2f}s")
    except Exception as e:
        elapsed = time.time() - req_start
        total_elapsed = time.time() - start_time
        print(f"请求 {i+1}: 失败={e}, 耗时={elapsed:.2f}s, 总耗时={total_elapsed:.2f}s")

print("\n测试完成！")
print("如果频率限制生效，前2个请求应该很快，后2个请求应该有明显的等待时间")
