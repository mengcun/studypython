from urllib.request import urlopen  # 用于请求网页
from urllib.parse import urlparse   # 用于分析网页链接地址
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
from bs4 import BeautifulSoup       # 用于提取网页内容
import datetime                     # 用于随机数生成器的种子
import random                       # 用于生成随机数生成器
import re                           # 用于正则表达式


pages_external_links = set()   # 用于存储已经发现的一个随机外部网页链接链路
pages_all_internal_links = set()
pages_all_external_links = set()

random.seed(datetime.datetime.now())        # 使用系统当前时间生成一个随机数生成器
start_site = 'https://en.wikipedia.org/wiki/Main_Page'


# 获取一个网页内的所有内链的列表
"""
获取一个网页的所有内部链接：
1.提取出网页的基链接
2.分析网页的所有链接情况，找出需要的网址，一般有：/, http, www, //为开头的几种形式
3.注意排除干扰项，错误处理
"""


def get_page_internal_links(page_url_address):
    internal_links = []     # 用于存储网站的内部链接

    # urlparse 可将网页链接地址解析成六部分，以'https://en.wikipedia.org/wiki/Wikipedia'为例:
    # scheme='https', netloc='en.wikipedia.org', path='/wiki/Wikipedia', params='', query='', fragment=''
    url_parse = urlparse(page_url_address)
    # print(url_parse)
    page_url_base_address = url_parse.scheme + '://' + url_parse.netloc    # 得到网站基础域名
    # print(page_url_base_address)
    try:
        html = urlopen(page_url_address)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31m Error occurred when request the url %s:' % page_url_address)  # 使用红色字体表示Error发生
        print(e)
        return None
    # 找到所有以'/'为开头或者包含基地址的链接，这里大部分是内部链接，但是有的有些网页中的外部链接也以'/'开始，然后重定向到外部链接
    try:
        page_url_bs_obj = BeautifulSoup(html, 'html.parser')
        inside_links = page_url_bs_obj.findAll('a', href=re.compile('^(/|.*'+page_url_base_address+')'))
        # print(inside_links)
    except AttributeError as e:
        print('\033[1;31m Error occurred when find the tag')     # 使用红色字体表示Error发生
        print(e)
        return None
    for inside_link in inside_links:
        if inside_link.attrs['href'] is not None:
            if inside_link.attrs['href'] not in internal_links:
                if inside_link.attrs['href'].startswith('/'):
                    if inside_link.attrs['href'].startswith('//'):
                        # 这里是以双'//'开始的链接，其中大部分是外部链接，有个别的是内部链接
                        if inside_link.attrs['href'].startswith('//' + url_parse.netloc):
                            # 以双'//'开始，但是后面接的是页面基础链接，此时为内部链接
                            internal_links.append('https:' + inside_link.attrs['href'])
                            # print('\033[1;36m Internal Links: ' + inside_link.attrs['href'])    # 使用青蓝色字体表示内部链接
                        else:
                            # 以双'//'开始，但是后面接的不是页面基础链接，此时为外部链接，这里舍去
                            # print('\033[1;34m External Links: ' + inside_link.attrs['href'])    # 使用蓝色字体表示外部链接
                            pass
                    else:
                        # 这里是以单个'/'开始的内部链接,加上页面基础链接存档
                        internal_links.append(page_url_base_address + inside_link.attrs['href'])
                        # print('\033[1;36m Internal Links: ' + inside_link.attrs['href'])    # 使用青蓝色字体表示内部链接
                else:
                    # 不以双'/'开始，而且包含基地址的链接，此时一般为内部完整连接
                    # print('\033[1;36m Internal Links: ' + inside_link.attrs['href'])  # 使用青蓝色字体表示内部链接
                    pass
        else:
            print('\033[1;33m Warning! The <href> of the tag is empty: ' + inside_link)     # 使用黄色字体表示Warning发生
            return None
    # print('There are %d internal_links in ' % len(internal_links) + page_url_address)
    # print(internal_links)
    return internal_links


# 获取页面上的所有的外链接列表
"""
获取一个网页的所有外部链接：
1.根据所给的网址提取出网页的基链接
2.分析网页的所有链接情况，找出需要的网址，一般有：/, http, www, //为开头的几种形式
3.注意排除干扰项，错误处理
"""


def get_page_external_links(page_url_address):
    external_links = []     # 用于存储网站的内部链接

    # urlparse 可将网页链接地址解析成六部分，以'https://en.wikipedia.org/wiki/Wikipedia'为例:
    # scheme='https', netloc='en.wikipedia.org', path='/wiki/Wikipedia', params='', query='', fragment=''
    url_parse = urlparse(page_url_address)
    # print(url_parse)
    page_url_base_address = url_parse.scheme + '://' + url_parse.netloc    # 得到网站基础域名
    # print(page_url_base_address)
    try:
        html = urlopen(page_url_address)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31m Error occurred when request the url %s:' % page_url_address)  # 使用红色字体表示Error发生
        print(e)
        return None
    # 找到所有以'http'或'www'为开头,并且不包含当前URL的链接的netloc部分，这里的链接一般都是外部链接
    try:
        page_url_bs_obj = BeautifulSoup(html, 'html.parser')
        outside_links = page_url_bs_obj.findAll('a', href=re.compile('^(https://|http://|www.|//)((?!'+url_parse.netloc+').)*$'))
        # print(outside_links)
    except AttributeError as e:
        print('\033[1;31m Error occurred when find the tag')        # 使用红色字体表示Error发生
        print(e)
        return None
    for outside_link in outside_links:
        if outside_link.attrs['href'] is not None:
            if outside_link.attrs['href'] not in external_links:
                if outside_link.attrs['href'].startswith('//'):
                    # 以双'//'开始，但是后面接的不是页面基础链接，此时为外部链接,需要协助构成可用的链接
                    external_links.append('https:' + outside_link.attrs['href'])
                    # print('\033[1;34m External Links: ' + outside_link.attrs['href'])  # 使用蓝色字体表示外部链接
                else:
                    external_links.append(outside_link.attrs['href'])
                    # print('\033[1;34m External Links: ' + outside_link.attrs['href'])  # 使用蓝色字体表示外部链接
                    pass
        else:
            print('\033[1;33m Warning! The <href> of the tag is empty: ' + outside_link)     # 使用黄色字体表示Warning发生
            return None
    # print('There are %d external_links in ' % len(external_links) + page_url_address)
    # print(external_links)
    return external_links


# 分解地址
def split_address(url_address):
    if url_address.startswith('https'):
        address_parts = url_address.replace('https://', '').split('/')
    elif url_address.startswith('http'):
        address_parts = url_address.replace('http://', '').split('/')
    else:
        return None
    return address_parts


# 随机返回页面的一个外部链接，如果该页面没有外部链接，则随机获取内部链接然后继续迭代，直到内部外部链接都不存在，即最后的页面
def get_random_external_link(start_page_url):
    external_links = get_page_external_links(start_page_url)
    if external_links is None or len(external_links) == 0:
        # 使用黄色字体表示Warning发生
        print('\033[1;33m Warning! No external links in ' + start_page_url + '\033[1;33m Look around another site')
        internal_links = get_page_internal_links(start_page_url)
        if internal_links is None or len(internal_links) == 0:
            print('\033[1;33m Warning! No external or internal links in ' + start_page_url)     # 使用黄色字体表示Warning发生
            return None
        else:
            return get_random_external_link(internal_links[random.randint(0, len(internal_links) - 1)])
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


# 只跟随随机的一个外部链接链路并将其显示出来
def follow_external_link_only(start_site_url):
    external_link = get_random_external_link(start_site_url)
    if external_link is None:
        print('\033[1;34m Finished! The site: ' + start_site_url + '\033[1;33m is isolated.(The last web page)')
        return None
    else:
        print('\033[1;34m The Random External Links: ' + external_link)  # 使用蓝色字体表示外部链接
        if external_link not in pages_external_links:
            pages_external_links.add(external_link)
            follow_external_link_only(external_link)


# 获取网页的所有外部链接
def get_page_all_external_links(page_url):
    internal_links = get_page_internal_links(page_url)
    external_links = get_page_external_links(page_url)
    # print(internal_links)
    # print(external_links)
    print('\033[1;32m There are %d internal and %d external links in page: '
          % (len(internal_links), len(external_links)) + page_url)
    for link in external_links:
        if link not in pages_all_external_links:
            pages_all_external_links.add(link)
    for link in internal_links:
        if link not in pages_all_internal_links:
            pages_all_internal_links.add(link)
            get_page_all_external_links(link)       # 迭代获取所有外部链接，这里内存的耗费可能会很大


follow_external_link_only('https://oreilly.com/')
# get_page_all_external_links('https://oreilly.com/')
