# coding=utf-8
"""
公用变量
"""
# 基本路径
cache_base_path = "./cache/"
timeout = 6
# 这是我们进行目录扫描的时候改写，每个网站不一样
three1_w = ""
# 这个是在我们使用c段扫描的时候要该，有的网站不需要加这个www前缀
three2_w = ""
"""
子域名配置
"""
# 爆破域名字典的路径
domain_dict_path = "./son_domain/dict/domain2.txt"
# 放我们查询子域名的所有模块
zi_domain_list = ['son_domain/crt', 'son_domain/brute']
# 结合子域名存放的路径
combine_domain = "./cache/son_domain/combine_domain/"

"""
目录扫描配置
"""
base_dir_path = "./dir_scan/dict/php.txt"
# 根据自己扫描的网站添加https://或者http://
xie_yi = "http://"
"""
C段扫描配置
"""
nmap_xml_path = "./nmap.xml"
ports = ["21", "22", "23", "25", "53", "110", "139", "143", "445", "1080", "1433", "1521",
         "2049", "2375", "3389", "5000", "6379", "80", "443", "7001", "7002", "8089", "8080",
         "9000", "27017", "27018", "3306"]