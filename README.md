# python_tools
put some tools about python
# 介绍
该工具主要包含子域名扫描，目录扫描，C段扫描功能，可以同时进行三个功能，希望能够帮助大家！
# 需要安装python依赖包
`import threading`
`import requests`
`from queue import Queue`
`from fake_useragent import UserAgent`
`import dns.resolver`
`import time`
# 电脑上要准备nmap扫描工具
# 参数解释
| 参数名 | 解释 |
| --- | --- |
| -D | 需要输入我们的域名（www.51nav.com）|
| -n | 设置多线程的数量 |
| -i | 设置本网站ip地址(当你确定本网站ip时，建议加上该参数) |
# 配置文件参数解释以及如何修改
| 变量名 | 解释 |
| --- | --- |
| timeout | 网站请求的时延 |
| three1_w | 网站三级域名，确保我们目录扫描的时候，网址的正确性，根据域名修改此参数 |
| three2_w | 确保我们的C段扫描正常进行(例如扫描www.51nav,这个参数就不需要加上，根据网站实际情况使用) |
| xie_yi | 该网站是什么协议这人就写什么协议（http://  https://） |
# 操作演示
## 进入工具
### 1.进入cmd，在该目录下运行代码`python start.py -D www.51nav.com -n 100`
![图片](https://user-images.githubusercontent.com/82155432/199540970-4a22a033-3057-4a8f-821d-ae2ac017ddc0.png)
### 2.可以选着模式，选择3，进入C段扫描
![图片](https://user-images.githubusercontent.com/82155432/199545177-177da314-b116-4528-8e72-657138a6b3f4.png)
### 扫描完毕过后，我们在根文件下面会生成一个文件加cache，我们C段扫描结果就在里面。
![图片](https://user-images.githubusercontent.com/82155432/199543150-4e4a1f52-17eb-436d-a810-9b76ed73fbb5.png)
### 后续收集到的数据全部都会在这个文件夹下面，通过名字就可以找到对应的文件内容。要注意，当你完成子域名扫描的时候，生成的combine_domain才是收集子域名的最终文件
# 该工具会持续更新，后续还会有whois信息收集功能上线，快快尝试起来吧！！！


