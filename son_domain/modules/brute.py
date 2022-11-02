# coding=utf-8
import threading
import os
import sys
sys.path.append("../")
from config import *
from common import do_get, progress, save
from queue import Queue


class Brute(object):
    def __init__(self, domain, thread_count):
        self._domain = domain
        self._queue = Queue()
        self._threads = []
        self._thread_count = thread_count
        self._total_count = 0
        self._result = []

    def _init(self):
        # 读取字典的内容
        with open(domain_dict_path, "r") as f:
            for d in f:
                # 拼接域名
                scan_domain = d.rstrip()+"."+self._domain
                self._queue.put("http://"+scan_domain)
        self._total_count = self._queue.qsize()

    def start(self):
        # 初始化
        self._init()
        # 创建队列
        for i in range(self._thread_count):
            self._threads.append(self.Brute_run(self._queue,self._total_count, self._result))
        # 启动线程
        for i in self._threads:
            i.start()
        # 等待子线程结束
        for i in self._threads:
            i.join()
        save(data=self._result, module="son_domain/brute", domain=self._domain)

    class Brute_run(threading.Thread):
        def __init__(self, queue, total_count, result):
            super().__init__()
            self._queue = queue
            self._total_count = total_count
            self._result = result

        def run(self):
            while not self._queue.empty():
                scan_url = self._queue.get()
                threading.Thread(target=self._msg).start()
                try:
                    response = do_get(scan_url)
                    if response.status_code != 404:
                        # 存放在一个result
                        self._result.append(scan_url.lstrip("http://"))
                except Exception as e:
                    pass

        # 显示进度条
        def _msg(self):
            # 算百分比
            already_do = round((100 - (self._queue.qsize() / self._total_count) * 100), 2)
            progress(already_do)