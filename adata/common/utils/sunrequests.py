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
    # 频率限制存储：{domain: (max_requests_per_minute, request_timestamps_list)}
    _rate_limit_config = {}
    _rate_limit_lock = threading.Lock()
    _default_max_requests = 30  # 默认每分钟30次请求

    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy

    @classmethod
    def set_rate_limit(cls, domain, max_requests_per_minute):
        """
        设置指定域名的请求频率限制
        :param domain: 域名，例如: "finance.pae.baidu.com"
        :param max_requests_per_minute: 每分钟最大请求次数
        """
        with cls._rate_limit_lock:
            cls._rate_limit_config[domain] = (max_requests_per_minute, [])

    def _check_rate_limit(self, url):
        """
        检查请求频率限制，如果超过限制则等待
        :param url: 请求的URL
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        with SunRequests._rate_limit_lock:
            # 获取该域名的限制配置，如果没有则使用默认值
            if domain not in SunRequests._rate_limit_config:
                SunRequests._rate_limit_config[domain] = (SunRequests._default_max_requests, [])

            max_requests, timestamps = SunRequests._rate_limit_config[domain]

            # 清理1分钟前的时间戳
            current_time = time.time()
            one_minute_ago = current_time - 60
            timestamps = [t for t in timestamps if t > one_minute_ago]

            # 如果超过限制则等待
            if len(timestamps) >= max_requests:
                # 计算需要等待的时间（等待到最早的时间戳过期）
                wait_time = 60 - (current_time - timestamps[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                # 再次清理时间戳
                current_time = time.time()
                one_minute_ago = current_time - 60
                timestamps = [t for t in timestamps if t > one_minute_ago]

            # 记录当前请求时间
            timestamps.append(current_time)
            SunRequests._rate_limit_config[domain] = (max_requests, timestamps)

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
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
