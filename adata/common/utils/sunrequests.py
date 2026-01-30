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
from urllib.parse import urlparse

import requests


class RateLimiter(object):
    _instance = None
    _lock = threading.Lock()
    _default_limit = 30
    _domain_limits = {}
    _request_times = {}

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_default_limit(cls, limit: int):
        cls._default_limit = limit

    @classmethod
    def set_domain_limit(cls, domain: str, limit: int):
        cls._domain_limits[domain] = limit

    @classmethod
    def get_limit(cls, domain: str) -> int:
        return cls._domain_limits.get(domain, cls._default_limit)

    @classmethod
    def _get_domain(cls, url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc

    @classmethod
    def wait_if_needed(cls, url: str):
        domain = cls._get_domain(url)
        limit = cls.get_limit(domain)

        with cls._lock:
            if domain not in cls._request_times:
                cls._request_times[domain] = []

            now = time.time()
            one_minute_ago = now - 60
            cls._request_times[domain] = [t for t in cls._request_times[domain] if t > one_minute_ago]

            if len(cls._request_times[domain]) >= limit:
                oldest_time = cls._request_times[domain][0]
                wait_time = oldest_time + 60 - now
                if wait_time > 0:
                    time.sleep(wait_time)
                    cls._request_times[domain] = [t for t in cls._request_times[domain] if t > time.time() - 60]

            cls._request_times[domain].append(time.time())


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
        RateLimiter.wait_if_needed(url)
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
rate_limiter = RateLimiter()
