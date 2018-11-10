from urllib.request import urlopen  # 用于请求网页
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
from bs4 import BeautifulSoup       # 用于分析网页
import datetime                     # 用于随机数生成器的种子
import random                       # 用于生成随机数生成器
import re                           # 用于正则表达式
import pymysql                      # 用于MySQL数据库的存取


random.seed(datetime.datetime.now())        # 使用系统当前时间生成一个随机数生成器
base_url = 'https://en.wikipedia.org'
search_url = '/wiki/Kevin_Bacon'
page_links = set()      # 用于存储得到的网页
link_chain = []         # 用于存储找到的链接的链路
recursion_deep_max = 2  # 递归深度
id_from_page = 0        # 来自的链接的Id值
id_to_page = 0          # 指向的链接的Id值
"""
创建位于wiki_article数据库下的pages表用于存储得到的网页链接
create table wiki_article.pages (id INT NOT NULL AUTO_INCREMENT, url VARCHAR(255), time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));
创建位于wiki_article数据库下的links表用于存储链接的索引:包含from_links_id即来自于那个链接的id和to_links_id即可以链接到的地址的id
create table wiki_article.links (id INT NOT NULL AUTO_INCREMENT, from_page_id INT NULL, to_page_id INT NULL, time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));

新版mysql使用的caching_sha2_password认证方式，换成mysql_native_password才可以成功。
在cmd命令行连接mysql, 
然后输入ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'
"""
connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='Mvemajsunp-', db='wiki_article', charset='utf8')
cursor_1 = connection.cursor()
cursor_1.execute("use wiki_article")


# 将得到的不重复的url链接存入MySQL数据库中的pages表中
def insert_to_mysql_pages(url):
    cursor_1.execute("SELECT * FROM pages WHERE url = %s", url)
    if cursor_1.rowcount == 0:
        cursor_1.execute("INSERT INTO pages (url) VALUES (%s)", url)
        connection.commit()
        return cursor_1.lastrowid
    else:
        return cursor_1.fetchone()[0]


# 将得到的一组from_page_id 和to_page_id存入MySQL数据库中的links表中
def insert_to_mysql_links(from_id, to_id):
    cursor_1.execute("SELECT * FROM links WHERE from_page_id = %s AND to_page_id = %s", (int(from_id), int(to_id)))
    if cursor_1.rowcount == 0:
        cursor_1.execute("INSERT INTO links (from_page_id, to_page_id) VALUES (%s, %s)", (int(from_id), int(to_id)))
        connection.commit()


# 返回网页的内部链接
def get_inside_links(article_url):
    full_url = base_url + article_url
    try:
        html = urlopen(full_url)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31m Error occurred when request the url %s:' % full_url)
        print(e)
        return None
    try:
        # 程序继续运行
        bs_obj = BeautifulSoup(html, 'html.parser')
        inside_links = bs_obj.findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    except AttributeError as e:
        print('\033[1;31m Error occurred when find the tag')     # 没有使用背景色
        print(e)
        return None
    return inside_links


# 对得到的无重复的链接进行处理，递归的将得到from_page_id和to_page_id放入到links表中
def sort_links_to_sql(page_url, recursion_level):
    global page_links, id_from_page, id_to_page
    if recursion_level < 0:
        link_chain.append(id_to_page)
        print(
            '\033[1;33m The current recursion deep for the link:' + search_url + ' up to %d:' % recursion_deep_max)
        print(link_chain)
        del link_chain[:]  # 清空链路列表，为新的链路做准备
        print('\033[1;33m Start the new link chain.')
        return
    id_from_page = insert_to_mysql_pages(page_url)   # 如果链接在pages表中不存在，则将链接存入pages表中,并返回其在pages中的id值
    inside_links = get_inside_links(page_url)
    if inside_links is None:
        print('\033[1;32m Warning! There is no inside_links could be found!')
        return None
    else:
        for link_info in inside_links:
            link = link_info.attrs['href']
            id_to_page = insert_to_mysql_pages(link)
            # 对page_url中的内部链接进行分析，并把本网页所在pages中的id值和该网页内部链接所在pages中的id值放入links表中
            insert_to_mysql_links(id_from_page, id_to_page)
            # 对遇到新的链接页面分析，如果pages中没有，则加入pages并继续搜索里面的词条链接
            if link not in page_links:
                page_links.add(link)
                link_chain.append(id_from_page)
                # 递归的寻找该链接的下一层,直到recursion_level递减到0,停止对该链路的递归
                print('\033[1;34m The current recursion deep for the link:' + search_url + ' is %d:' % (recursion_deep_max - recursion_level))
                print(link_chain)
                sort_links_to_sql(link, recursion_level - 1)


sort_links_to_sql(search_url, recursion_deep_max)
cursor_1.close()
connection.close()
