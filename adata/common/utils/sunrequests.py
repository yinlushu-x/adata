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
from collections import defaultdict

import requests


class RateLimiter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._lock = threading.Lock()
        self._default_limit = 30
        self._domain_limits = {}
        self._requests = defaultdict(list)

    def set_limit(self, domain, limit):
        with self._lock:
            if limit <= 0:
                self._domain_limits[domain] = None
            else:
                self._domain_limits[domain] = limit

    def set_default_limit(self, limit):
        with self._lock:
            self._default_limit = max(1, limit)

    def get_limit(self, domain):
        with self._lock:
            if domain in self._domain_limits:
                return self._domain_limits[domain]
            return self._default_limit

    def _get_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc

    def wait(self, url):
        domain = self._get_domain(url)
        limit = self.get_limit(domain)
        if limit is None:
            return

        now = time.time()
        window_start = now - 60

        with self._lock:
            timestamps = self._requests[domain]
            timestamps = [t for t in timestamps if t > window_start]

            while len(timestamps) >= limit:
                window_start = timestamps[0]
                wait_time = 60 - (now - window_start)
                if wait_time > 0:
                    time.sleep(wait_time)
                now = time.time()
                window_start = now - 60
                timestamps = [t for t in timestamps if t > window_start]

            timestamps.append(now)
            self._requests[domain] = timestamps


_rate_limiter = RateLimiter()


def set_rate_limit(domain, limit):
    _rate_limiter.set_limit(domain, limit)


def set_default_rate_limit(limit):
    _rate_limiter.set_default_limit(limit)


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
        # 0. 频率限制
        _rate_limiter.wait(url)
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
