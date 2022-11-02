# coding=utf-8
import sys
import os
import threading
from optparse import OptionParser
from son_domain.modules.crt import Crt_spider
from son_domain.modules.brute import Brute
from dir_scan.dir_scan import Dir_scan
from config import *
from c_scan.c_scan import C_scan
from common import domain_combination, found_ip


def son_domain_scan(domain):
    crt = Crt_spider(options.Domain)
    brute = Brute(options.Domain, int(options.Threads_count))
    crt.start()
    brute.start()
    # 把这两个的数据结合起来
    domain_combination(domain)


def tip():
    functions = {
        "1": "子域名扫描",
        "2": "目录扫描",
        "3": "C段扫描"
    }
    print("您可以选择以下功能：")
    for key, value in functions.items():
        print(f"   [*]{key}. {value}")
    print("   [*]0. 综合扫描")


if __name__ == "__main__":
    jieshao = """
版本：hard_study v1.0     作者：ThanCat
"身体健康，努力学习，珍惜当下，怀揣梦想"
    _                   _         _             _       
| |__   __ _ _ __ __| |    ___| |_ _   _  __| |_   _ 
| '_ \ / _` | '__/ _` |   / __| __| | | |/ _` | | | |
| | | | (_| | | | (_| |   \__ \ |_| |_| | (_| | |_| |
|_| |_|\__,_|_|  \__,_|___|___/\__|\__,_|\__,_|\__, |
                     |_____|                   |___/ 

    """
    print(jieshao)
    tip()
    n = input("请选择以上数字：")
    parser = OptionParser()
    parser.add_option("-D", "--Domain", dest="Domain", help="Please you input target domain")
    parser.add_option("-n", "--number", dest="Threads_count", help="Threads_count")
    parser.add_option("-i", "--ip", dest="IP", help="Please you input IP(**.**.**.0/24)")
    (options, args) = parser.parse_args()
    if options.Domain is None or options.Threads_count is None:
        parser.print_help()
    else:
        # 目录扫描功能
        url = xie_yi + three1_w + options.Domain
        dir = Dir_scan(url, int(options.Threads_count))

        if int(n) == 1:
            print(f"正在对{options.Domain}进行子域名扫描")
            son_domain_scan(options.Domain)
        elif int(n) == 2:
            print(f"正在对{url}站点进行目录扫描")
            dir.start()
        elif int(n) == 3:
            if options.IP is not None:
                print(f"正在对{options.IP}进行子域名扫描")
                # 搜先使用nmap扫描出存活的主机
                os.system(f"nmap -sn -PE --min-hostgroup 1024 --min-parallelism 1024 -oX nmap.xml {options.IP}")
                # 然后再ba用我们的扫描端口的功能
                scan = C_scan(str(options.IP), 100)
            else:
                # 在调用c段扫描，我们先要调用函数，把网站的ip地址找出来
                domain = three2_w + options.Domain
                print(f"正在对{domain}进行子域名扫描")
                c_ip = found_ip(domain)
                ip_list = c_ip.split(".")
                c_ip = ".".join(ip_list[0:3]) + ".0/24"
                os.system(f"nmap -sn -PE --min-hostgroup 1024 --min-parallelism 1024 -oX nmap.xml {c_ip}")
                scan = C_scan(c_ip, 100)
            scan.start()
        elif int(n) == 0:
            print(f"正在对{options.Domain}进行综合扫描")
            if options.IP is not None:
                # 搜先使用nmap扫描出存活的主机
                os.system(f"nmap -sn -PE --min-hostgroup 1024 --min-parallelism 1024 -oX nmap.xml {options.IP}")
                # 然后再ba用我们的扫描端口的功能
                scan = C_scan(str(options.IP), 100)
            else:
                # 在调用c段扫描，我们先要调用函数，把网站的ip地址找出来
                domain = three2_w + options.Domain
                c_ip = found_ip(domain)
                ip_list = c_ip.split(".")
                c_ip = ".".join(ip_list[0:3]) + ".0/24"
                os.system(f"nmap -sn -PE --min-hostgroup 1024 --min-parallelism 1024 -oX nmap.xml {c_ip}")
                scan = C_scan(c_ip, 100)


            # 创建进程
            threads = [threading.Thread(target=scan.start),
                       threading.Thread(target=son_domain_scan(options.Domain)),
                       threading.Thread(target=dir.start)]
            # 启动进程
            for i in threads:
                i.start()
            # 等待子进程结束
            for i in threads:
                i.join()
