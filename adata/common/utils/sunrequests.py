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
        # 域名请求频率限制配置: {domain: limit_per_minute}
        self._domain_limits = {}
        # 域名请求计数: {domain: {'count': int, 'current_time': int}}
        self._domain_requests = {}
        # 默认每分钟请求次数限制
        self._default_limit = 30
        # 线程锁
        self._lock = threading.Lock()

    def set_rate_limit(self, domain, limit):
        """
        设置域名的请求频率限制
        :param domain: 域名，例如 'hq.sinajs.cn'
        :param limit: 每分钟请求次数
        """
        with self._lock:
            self._domain_limits[domain] = limit

    def set_default_rate_limit(self, limit):
        """
        设置默认的请求频率限制（所有未单独设置的域名）
        :param limit: 每分钟请求次数，默认30
        """
        with self._lock:
            self._default_limit = limit

    def get_rate_limit(self, domain=None):
        """
        获取域名的请求频率限制
        :param domain: 域名，如果为None则返回默认限制
        :return: 每分钟请求次数
        """
        with self._lock:
            if domain is None:
                return self._default_limit
            return self._domain_limits.get(domain, self._default_limit)

    def _check_rate_limit(self, url):
        """
        检查并处理请求频率限制
        :param url: 请求URL
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        while True:
            with self._lock:
                # 获取该域名的限制次数
                limit = self._domain_limits.get(domain, self._default_limit)
                current_time = int(time.time() // 60)  # 当前分钟
                
                # 初始化或更新域名的请求记录
                if domain not in self._domain_requests:
                    self._domain_requests[domain] = {
                        'count': 0,
                        'current_time': current_time
                    }
                
                requests_record = self._domain_requests[domain]
                
                # 如果时间已经过了一分钟，重置计数器
                if requests_record['current_time'] != current_time:
                    requests_record['count'] = 0
                    requests_record['current_time'] = current_time
                
                # 检查是否超过限制
                if requests_record['count'] < limit:
                    # 未超过限制，增加计数器并返回
                    requests_record['count'] += 1
                    return
                
                # 超过限制，计算需要等待的时间
                wait_time = 60 - (time.time() % 60) + 0.1
            
            # 在锁外等待，避免阻塞其他线程
            time.sleep(wait_time)

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
        # 1. 检查频率限制
        self._check_rate_limit(url)
        
        # 2. 获取设置代理
        proxies = self.__get_proxies(proxies)
        
        # 3. 请求数据结果
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
            # 使用原始requests获取代理IP，避免频率限制影响代理获取
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()