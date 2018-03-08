# -*- coding: utf-8 -*-

import re
import requests #用于请求12306网站网址
from pprint import pprint #使用pprint模块将信息打印到文件，更容易阅读:python3 parse_station.py > stations.py
#爬取车站信息，在12306查询界面查看，station_version 可能会升级
url ='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9048'

response = requests.get(url, verify = False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(stations), indent = 4)
