from bs4 import BeautifulSoup
from urllib.request import urlretrieve  # 用于网页上的数据下载
from urllib.request import urlopen  # 用于打开网址
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
import os


# 获取网页上所有'src'属性中的链接文件
"""
注意！！！在从网络上下载链接文件时候，因为不知道该链接下是什么文件类型，很可能下载到恶意程序或代码
因此，在操作网络链接下载时候，注意检查文件类型和属性，防止电脑中毒
"""
download_directory = 'download_from_net'
start_base_url = 'https://pythonscraping.com'


# 获取页面中的所有内部链接，即包含基链接的src属性中的链接
def get_absolute_url(url, source):
    if source.startswith('http://www.'):
        absolute_url = 'http://' + source[11:]
    elif source.startswith('https://www.'):
        absolute_url = 'https://' + source[12:]
    elif source.startswith('http://'):
        absolute_url = source
    elif source.startswith('https://'):
        absolute_url = source
    elif source.startswith('www.'):
        absolute_url = 'https://' + source[4:]
    else:
        absolute_url = url + '/' + source
    if start_base_url not in absolute_url:    # 如果在得到的链接中没有包含基链接，那么不是该网页内部链接，舍去
        return None
    return absolute_url


# 获取下载
def get_download_path(b_url, a_url, d_directory):
    d_path = a_url.replace('www.', '')
    d_path = d_path.replace(b_url, '')
    d_path = d_directory + d_path
    directory = os.path.dirname(d_path)   # 返回d_path所在的绝对目录
    if not os.path.exists(directory):
        os.makedirs(directory)
    d_path = d_path.split('?')[0]    # 得到文件名的绝对路径
    return d_path


def get_all_src(page_url):
    try:
        html = urlopen(page_url)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31m Error occurred when request the url %s:' % page_url)  # 使用红色字体表示Error发生
        print(e)
        return None
    # 找到所有的src属性
    try:
        page_url_bs_obj = BeautifulSoup(html, 'html.parser')
        page_url_src = page_url_bs_obj.findAll(src=True)
        # print(page_url_src)
    except AttributeError as e:
        print('\033[1;31m Error occurred when find the tag of src')  # 使用红色字体表示Error发生
        print(e)
        return None

    for src in page_url_src:
        file_url = get_absolute_url(start_base_url, src['src'])
        if file_url is not None:
            print(file_url)
            urlretrieve(file_url, get_download_path(start_base_url, file_url, download_directory))


get_all_src('https://pythonscraping.com/')
