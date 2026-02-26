# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
"""

import threading
import time
from collections import defaultdict
from urllib.parse import urlparse

import requests


class RateLimiter:
    """
    基于令牌桶算法的频率限制器
    支持每个域名独立的请求频率控制
    """
    _instance_lock = threading.Lock()

    def __init__(self, default_rate: int = 30):
        self._default_rate = default_rate
        self._domain_rates = {}
        self._domain_buckets = defaultdict(self._create_bucket)
        self._lock = threading.Lock()

    def _create_bucket(self):
        return {'tokens': self._default_rate, 'last_update': time.time()}

    def set_rate_limit(self, domain: str, requests_per_minute: int):
        """设置特定域名的请求频率限制"""
        with self._lock:
            self._domain_rates[domain] = requests_per_minute
            self._domain_buckets[domain] = {'tokens': requests_per_minute, 'last_update': time.time()}

    def set_default_rate(self, requests_per_minute: int):
        """设置默认请求频率限制"""
        with self._lock:
            self._default_rate = requests_per_minute

    def get_rate(self, domain: str) -> int:
        """获取域名的请求频率限制"""
        return self._domain_rates.get(domain, self._default_rate)

    def acquire(self, domain: str):
        """获取请求许可，如果超过限制则等待"""
        with self._lock:
            bucket = self._domain_buckets[domain]
            rate = self._domain_rates.get(domain, self._default_rate)
            now = time.time()
            elapsed = now - bucket['last_update']
            bucket['tokens'] = min(rate, bucket['tokens'] + elapsed * (rate / 60.0))
            bucket['last_update'] = now
            if bucket['tokens'] < 1:
                wait_time = (1 - bucket['tokens']) * (60.0 / rate)
                time.sleep(wait_time)
                bucket['tokens'] = 0
                bucket['last_update'] = time.time()
            else:
                bucket['tokens'] -= 1


_rate_limiter = RateLimiter()


class SunProxy(object):
    _data = {}
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SunProxy, "_instance"):
            with SunProxy._instance_lock:
                if not hasattr(SunProxy, "_instance"):
                    SunProxy._instance = object.__new__(cls)

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def delete(cls, key):
        if key in cls._data:
            del cls._data[key]


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy

    @staticmethod
    def set_rate_limit(domain: str, requests_per_minute: int):
        """
        设置特定域名的请求频率限制
        :param domain: 域名，如 'eastmoney.com' 或 '10jqka.com.cn'
        :param requests_per_minute: 每分钟最大请求数
        """
        _rate_limiter.set_rate_limit(domain, requests_per_minute)

    @staticmethod
    def set_default_rate(requests_per_minute: int):
        """
        设置默认请求频率限制
        :param requests_per_minute: 每分钟最大请求数，默认30
        """
        _rate_limiter.set_default_rate(requests_per_minute)

    @staticmethod
    def get_rate(domain: str) -> int:
        """
        获取域名的请求频率限制
        :param domain: 域名
        :return: 每分钟最大请求数
        """
        return _rate_limiter.get_rate(domain)

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 0. 频率限制
        domain = urlparse(url).netloc
        if domain:
            _rate_limiter.acquire(domain)
        # 1. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 2. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(retry_wait_time / 1000)
            if i == times - 1:
                return res
        return res

    def __get_proxies(self, proxies):
        """
        获取代理配置
        """
        if proxies is None:
            proxies = {}
        is_proxy = SunProxy.get('is_proxy')
        ip = SunProxy.get('ip')
        proxy_url = SunProxy.get('proxy_url')
        if not ip and is_proxy and proxy_url:
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
