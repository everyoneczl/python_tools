import sys
import requests
sys.path.append("../")
from common import found_ip


def scan_whois(ip):
    # 中文查询网站
    url1 = "http://freeapi.ipip.net/"
    # 国外网站
    url2 = "http://ip-api.com/json/"
    # 拼接链接
    url1 = url1 + str(ip)
    url2 = url2 + str(ip)
    # 对着两个地址发起请求
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    print(response1.status_code)
    print(response2.status_code)
    if response1.status_code == 200 and response2.status_code == 200:
        print(response1.text)
        print("=============")
        print(response2.text)


ips = found_ip("www.51nav.com")
print(ips)
scan_whois(ips)

# import sys
# import requests
#
# def main(argv):
#
#   url = 'http://freeapi.ipip.net/'  #中文免费
#   url2 = 'http://ip-api.com/json/'  #外国网站
#   args = sys.argv[1]
#   url=url+format(args)
#   url2 = url2 + format(args)
#   response = requests.get(url)
#   response2 = requests.get(url2)
#
#   str=response.text.replace('\"','') #去掉双引号
#   str=str.replace('[','')      #去掉方括号
#   str=str.replace(']','')
#   str=str.replace(' ','')
#
#   str=str.split(",")  #已逗号为分割符号，分割字符串为数组
#   print("****************************************")
#   print("您查询的IP地址 %s 来源地是："%args)
#   print("国家：%s"%(str[0])) #访问数组里面的值
#   print("省份：%s"%(str[1]))
#   print("城市：%s"%(str[2]))
#   print("区域：%s"%(str[3]))
#   str[4] = str[4].replace('\n', '') #去掉回车符号
#   print("运营商：%s"%(str[4]))
#   print("数据来源<www.ipip.net免费查询接口>")
#   print("****************************************")
#   strpp={}         #定义一个字典strpp
#   strpp=response2.json()  #把英文网站json接口返回值传给字典strpp
#   print("\n")        #下面就是直接从字典取值，显示。
#   print("您查询的IP地址 %s 来源地是："%(strpp.get('query')))
#   print("国家：%s"%(strpp.get('country')))
#   print("城市：%s"%(strpp.get('city')))
#   print("经纬度坐标：%s,%s"%(strpp.get('lat'),strpp.get('lon')))
#   print("运营商编号：%s"%(strpp.get('as')))
#   print("ISP服务商：%s"%(strpp.get('isp')))
#   print("数据来源<www.ip-api.com免费查询接口>")
#   print("****************************************")
# if __name__ == "__main__":
#   main(sys.argv)