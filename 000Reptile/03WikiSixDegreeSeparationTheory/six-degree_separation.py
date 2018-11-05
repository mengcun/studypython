from urllib.request import urlopen  # 用于请求网页
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
from bs4 import BeautifulSoup       # 用于分析网页
import datetime                     # 用于随机数生成器的种子
import random                       # 用于生成随机数生成器
import re                           # 用于正则表达式


random.seed(datetime.datetime.now())        # 使用系统当前时间生成一个随机数生成器
base_url = 'https://en.wikipedia.org'


def get_inside_links(article_url):
    full_url = base_url + article_url
    try:
        html = urlopen(full_url)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31mError occurred when request the url %s:' % full_url)
        print(e)
        return None
    try:
        # 程序继续运行
        bs_obj = BeautifulSoup(html, 'html.parser')
        inside_links = bs_obj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    except AttributeError as e:
        print('\033[1;31mError occurred when find the tag')     # 没有使用背景色
        print(e)
        return None
    return inside_links


def get_related_links(article):
    article_links = get_inside_links(article)
    if article_links is None:
        print('\033[1;31mThe inside_links could not be found!')
    else:
        while len(article_links) > 0:
            new_article = article_links[random.randint(0, len(article_links) - 1)].attrs['href']
            print(new_article)
            article_links = get_inside_links(new_article)


get_related_links('/wiki/Kevin_Bac')
