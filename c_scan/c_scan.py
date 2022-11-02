# coding=utf-8
"""
C段扫描
一定要拿下一个服务器之后，我们就可以知道服务器的内网IP
1. 直接双穿NMAP，安装，扫描
2. 上传，自己写的工具也可以进行扫描

思路：
1. 利用我们的IPy进行C段的IP生成
2. 将IP和我们的端口进行结合，生成访问链接
3. 利用requests进行请求，然后判断相应的结果
4. 来判断这个服务是否开启
"""
import os
import re
import sys

import requests
import threading
from queue import Queue
sys.path.append("../")
from config import *
from common import do_get, progress, save


class C_scan(object):
    def __init__(self, ip_name, thread_count):
        self._ip_name = ip_name
        self._queue = Queue()
        self._thread_count = thread_count
        self._threads = []
        self._ips = []
        self._total_count = 0
        self._result = []

    def _active_ip(self):
        with open(nmap_xml_path, "r") as f:
            ip_data = f.read()
            # 书写正则表达式取xml文件的ip
            pattern = r'<address addr="(.*?)" addrtype="ipv4"/>'
            self._ips = re.findall(pattern, ip_data)

    def _init(self):
        # 执行获取ip的函数
        self._active_ip()
        # 将ip和端口组装起来，然后放入queue
        for ip in self._ips:
            # 遍历端口
            for port in ports:
                # 组装链接
                self._queue.put(f"http://{ip}:{port}")
                self._queue.put(f"https://{ip}:{port}")
        self._total_count = self._queue.qsize()

    def start(self):
        self._init()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Scan_Run(self._queue, self._total_count, self._result))
        for i in self._threads:
            i.start()
        for i in self._threads:
            i.join()
        # 拿到端口过后，把c段扫描出来的内容存在文件里面
        ips = self._ip_name.split("/")[0]
        ips = ips.replace(".", "-")
        save(data=self._result, module="c_ip", domain=f"{ips}")

    class Scan_Run(threading.Thread):
        def __init__(self, queue, total_count, result):
            super().__init__()
            self._queue = queue
            self._total_count = total_count
            self._result = result

        def run(self):
            while not self._queue.empty():
                scan_url = self._queue.get()
                # 调用进度函数
                self._msg()
                # 请求地址
                try:
                    response = do_get(scan_url)
                    if response.status_code != 404:
                        self._result.append(scan_url)
                except Exception as e:
                    pass

        def _msg(self):
            # 算百分比
            already_do = round((100 - (self._queue.qsize() / self._total_count) * 100), 2)
            progress(already_do)