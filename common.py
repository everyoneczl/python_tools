# coding=utf-8
"""
公共函数
"""
import sys
import requests
from fake_useragent import UserAgent
import re
import os
from config import *
import json
import time
import dns.resolver


def get_headers():
    """
    产生随机ua
    :return:
    """
    ua = UserAgent()
    headers = {
        "UserAgent": ua.random
    }
    return headers


def do_get(url):
    # 获取随机头
    headers = get_headers()
    # 请求
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return response
    except Exception as e:
        pass


def is_domain(domain):
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9])).'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    if pattern.match(domain):
        return True
    else:
        return False


def save(**dict):
    """
    base_path:./cache
    path = ./cache/模块/域名/域名.时间.json
    :param dict:传入动态字典，data:数据，modules:模块 domain:域名
    :return:
    """
    # 分别获取数据
    data = dict['data']
    module = dict['module']
    domain = dict['domain']
    if data is not None and module is not None and domain is not None:
        # 先把路径生成出来
        save_path = cache_base_path + module + "/" + domain
        make_dir(save_path)
        # 准备保存的完整路径
        save_path = save_path + "/" + domain + "." + str(time.time()) + ".json"
        # 保存数据
        with open(save_path, "a+") as f:
            json.dump(data, f, indent=4)


def make_dir(path):
    """
    用于生成路径
    :param path:
    :return:
    """
    # 先判断这个路径是否正确
    if not os.path.exists(path):
        os.makedirs(path)


# 书写进度条
def progress(num):
    """

    :param num: 已经完成了的数量
    :return:
    """
    count = int(num)
    sys.stdout.write("\r" + ("▓" * count) + f">[{num}%]")


# 书写我们所有模块查询子域名的一个总和
def domain_combination(domain):
    """
    1. 首先我们要取出两个模块查询出来的子域名文件，一定要取最新的文件
    2。 然后我们把两个文件进行去重操作
    :param domain:
    :return:
    """
    # 定义一个列表，装所有的域名
    all_domain = []
    for module in zi_domain_list:
        # 拼接模块的路劲
        path = cache_base_path + module + "/" + domain
        # 判断这个路径是否存在，如果存在我们就把他下面的文件取出来。
        if os.path.exists(path):
            files = os.listdir(path)
            # 默认列表最后一个就是最新的一个
            file = files[-1]
            filepath = path + "/" + file
            # 然后把文件的雷动取出来，放到列表里面
            with open(filepath, "r") as f:
                data = json.load(f)
                all_domain += data
    # 取重操作
    all_domain = list(set(all_domain))
    # 然后把他以json格式存入我们的文件里面
    # 路径拼接
    make_dir(combine_domain)
    path_combine = combine_domain + domain + "." + str(time.time()) + "json"
    with open(path_combine, "a+") as f:
        json.dump(all_domain, f, indent=4)


# 查询网站的真实ip
def found_ip(domain):
    A = dns.resolver.resolve(domain,"A")
    for a in A.response.answer:
        if len(a.items) == 1:
            for ip in a.items:
                return ip.address

