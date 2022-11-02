# coding=utf-8
"""
1. 我们需要找到我们目录字典的位置。
2. 把字典拼接在地址的后面，然后取判断改路径是否存在。
3. 如果存在，就把我们的路径保存到一个文件里面。
"""
import os
import sys
import threading
from queue import Queue
from fake_useragent import UserAgent

sys.path.append("../")
from config import *
from common import do_get, progress, save


class Dir_scan(object):
    def __init__(self, url, threads_count):
        self._url = url
        self._queue = Queue()
        self._threads = []
        self._threads_count = threads_count
        self._total_count = 0
        self._result = []
        self._url_list = []

    def _check_dict(self, path):
        """
        去除字典开头的值
        :return:
        """
        path = path.strip("/")
        return path

    # 初始化，判断路径是否存在，而且放入一个列表里面
    def _init(self):
        # 判断字典是否存在
        dict_path = base_dir_path
        if not os.path.exists(dict_path):
            print("字典不存在！")
            sys.exit(-1)
        with open(dict_path, "r") as f:
            for d in f:
                # 去除字典里面内容前后的/
                ds = self._check_dict(d).rstrip()
                # 判断我们的传入的路劲里面是否是一个地址
                self._url_list = self._url.split("://")
                complete_dir = self._url + "/" + ds
                self._queue.put(complete_dir)
        self._total_count = self._queue.qsize()

    def start(self):
        # 先初始化我们的队列，拿到所有的路径
        self._init()
        # 然后开始我们的请求，如果请求不是
        # 创建队列
        for i in range(self._threads_count):
            self._threads.append(self.Dir_scan_run(self._queue, self._total_count, self._result))
        for i in self._threads:
            i.start()
        for i in self._threads:
            i.join()
        # 把他存入一个文件里面
        # 获取域名
        save(data=self._result, module="dir_scan", domain=self._url_list[1])

    class Dir_scan_run(threading.Thread):
        def __init__(self, queue, total_count, result):
            super().__init__()
            self._queue = queue
            self._ua = UserAgent()
            self._total_count = total_count
            self._result = result

        def run(self):
            while not self._queue.empty():
                scan_url = self._queue.get()
                # 加提示信息
                self._msg()
                response = do_get(scan_url)
                if response is not None:
                    if response.status_code == 200:
                        self._result.append(scan_url)

        def _msg(self):
            # 算百分比
            already_do = round((100 - (self._queue.qsize() / self._total_count) * 100), 2)
            progress(already_do)
