# -*- coding: utf-8 -*-
"""
crawl.py:用来爬取租房网站上的房源信息
rent.csv:生成的房源数据，用来导入到index.html中
index.html:网页实现代码

代码没有难度，主要就是看看几个API如何使用，下面给出文档链接：

高德 JavaScript API 帮助文档:http://lbs.amap.com/api/javascript-api/summary/
高德 JavaScript API 示例中心:http://lbs.amap.com/api/javascript-api/example/map/map-show/
Requests: HTTP for Humans:http://www.python-requests.org/en/master/
Beautiful Soup 4.2.0 文档:https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
csv — CSV 文件的读写:http://python.usyiyi.cn/translate/python_278/library/csv.html

"""
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

#已经完成的页数序号，初始为0
page = 0
"""
python2中用wb的方式打工文件，python3中用w的方式即可，这里牵扯到bytes类型与string类型的转化
bytes解码会得到str str编码会变成bytes
>>> b'123'.decode('ascii')
'123'
>>> '123'.encode('ascii')
b'123
"""
csv_file = open("rent.csv", "wb")
csv_writer = csv.writer(csv_file, delimiter = ',')

while True:
    page += 1
    print "fetch: ", url.format(page=page)
    response = requests.get(url.format(page = page))
    #Beautiful Soup是一个用来解析html或者xml文件的库，支持元素选择器
    html = BeautifulSoup(response.text, "lxml")
    house_list = html.select(".list > li")

    #循环在读不到新的房源时候结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8")
        #由于读取到的链接路径是相对路径，所以需要urljoin得到完整的url地址
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()
        #如果第二列是公寓名则取消第一列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]
        house_money =house.select(".money")[0].select("b")[0].string.encode("utf8")
        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()
