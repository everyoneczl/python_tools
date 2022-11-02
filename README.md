# python_tools
put some tools about python
# 需要安装python依赖包
`import threading`
`import requests`
`from queue import Queue`
`from fake_useragent import UserAgent`
`import dns.resolver`
`import time`
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
