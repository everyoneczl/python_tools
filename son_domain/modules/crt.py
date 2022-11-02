# coding=utf-8
"""
解析站点返回子域名
"""
import os
import sys

# 这儿找不到这个配置文件，因为不是同级
sys.path.append("../")
from config import *
from common import do_get, save, is_domain
from bs4 import BeautifulSoup


class Crt_spider(object):
    def __init__(self, domain):
        self._base_url = "https://crt.sh/?q="
        self._domain = domain

    def start(self):
        scan_url = self._base_url + self._domain
        flag = True
        while flag:
            # 调用公共的模块
            response = do_get(scan_url)
            if response is not None:
                if response.status_code == 200:
                    flag = False
        # 开始解析
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            tds = soup.find_all(name="td", attrs={"style": None, "class": None})
            domain_list = []
            for i in tds:
                try:
                    if is_domain(i.string):
                        domain_list.append(i.string)
                except Exception as e:
                    pass

            # 去重了
            domain_list = list(set(domain_list))
            save(data=domain_list, module="son_domain/crt", domain=self._domain)
