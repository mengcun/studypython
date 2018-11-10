from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import csv  # 用于存储数据到CSV文件中
from urllib.request import urlopen  # 用于打开网址
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
"""
os模块用于获取每个下载文件的目标文件夹，创建完整的路径。
是与操作系统进行交互的接口，可以操作文件路径，创建目录，获取运行进程和环境变量的信息，以及其他系统相关操作
"""
# ----------------------------------------------------------------------------------------------------------------------
# 爬取豆瓣电影排行榜
url_movies = 'https://movie.douban.com/chart'
# 使用手机端和登录Cookie模拟真实页面访问，降低被禁IP的风险
headers_movies = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': 'bid=o5R_UMszexM; gr_user_id=1c7c52b4-fb38-4f2b-a0db-01e2246833eb; _vwo_uuid_v2=D977B7F9701C9756A9DEEB0D0DC9CA031|334402f021eaf5e873e1d898441ff714; viewed="1168618_1310376_1231162_26614049_10773324"; douban-fav-remind=1; ll="108288"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1540371723%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1589339816.1519868013.1539069620.1540371723.9; __utmb=30149280.0.10.1540371723; __utmz=30149280.1540371723.9.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1979596219.1540371723.1540371723.1540371723.1; __utmb=223695111.0.10.1540371723; __utmz=223695111.1540371723.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=Q1bqtJak2lfrw9z08pqANUmwUo3G2UP2; __utmc=30149280; __utmc=223695111; as="https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action="; ps=y; dbcl2="147782006:OFXc6p9b9y4"; ck=L6JE; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=c71b97126997c509.1540371723.1.1540374175.1540371723.'
}


def get_movies_top(url_movie, data=None):
    wb_movies_data = requests.get(url_movie, headers_movies)
    time.sleep(4)
    soup = BeautifulSoup(wb_movies_data.text, 'lxml')
    titles = soup.select('tr > td > a')
    images = soup.select('img[width="75"]')
    rates = soup.select('tr > td > div > div > span.rating_nums')
    # print(titles, images, rates, sep='\n---------\n')

    if data is None:
        for title, img, rate in zip(titles, images, rates):
            data = {
                'title': img.get("alt"),
                'img': img.get('src'),
                'rate': rate.get_text()
            }
            print(data, sep='\n---------\n')


# get_movies_top(url_movies)
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# 小猪短租爬取租房信息
url_rent_details = 'http://bj.xiaozhu.com/fangzi/35337972403.html'
# 批量获取链接 <- 每个详情页的链接都存在这里，解析详情的时候就遍历这个列表然后访问就好啦~
pages_link = []
# 使用手机端和登录Cookie模拟真实页面访问，降低被禁IP的风险
headers_rents = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': 'abtest_ABTest4SearchDate=b; gr_user_id=ba7564e8-22d6-4c34-a9c6-e13e81cc1774; grwng_uid=d7323db5-ad54-4d33-9bb8-7c3219ae6735; xz_guid_4se=4c8def4c-6e5c-4b11-9eef-05cd066f14b9; xzuinfo=%7B%22user_id%22%3A43900226101%2C%22user_name%22%3A%2218510051034%22%2C%22user_key%22%3A%221014714923%22%7D; xzucode=312fd321b4a086d80761e8002a1835fb; xzucode4im=6f64e6a35ac8be67720e2122646120fb; xztoken=WyIxMzExMTAxOTI1cTJnVCIseyJ1c2VyaWQiOjQzOTAwMjI2MTAxLCJleHBpcmUiOjAsImMiOiJ3ZWIifSwiZWRiM2YyNWYwZTk1MzdkNjM0MzY5MDZlYzQ5Y2I4MWMiXQ%3D%3D; xzSessId4H5=c4fdd5b26fca3470f873340838c0d4eb; startDate=2018-10-25; endDate=2018-10-26; haveapp=1; xzuuid=98ddcf0c; rule_math=hom06b6owws; newcheckcode=1eddc3e0c0fc2090f2bbf9b9856092d4; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_sid_with_cs1=e57d5321-8d28-479a-a106-2c769192e3ad; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_cs1=43900226101; 59a81cc7d8c04307ba183d331c373ef6_gr_cs1=43900226101; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id=e57d5321-8d28-479a-a106-2c769192e3ad; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id_e57d5321-8d28-479a-a106-2c769192e3ad=true'
}


def get_rent_details(url, data=None):
    wb_rent_details_data = requests.get(url, headers_rents)
    # 因为是单页面，使用 select 方法获得的元素又是一个列表，那么列表中的第一个元素且也是唯一一个元素即是我们要找的信息 用 “[0]” 索引将其取出
    # 后在对其使用处理的方法，因为 BeautifulSoup 的一些筛选方法并不能针对列表类型的元素使用
    soup = BeautifulSoup(wb_rent_details_data.text, 'lxml')
    title = soup.select('div.pho_info > h4')[0].text
    address = soup.select('div.pho_info > p')[0].get('title')  # 和 get('href') 同理，他们都是标签的一个属性而已，我们只需要的到这个属性的内容即可
    price = soup.select('div.day_l > span')[0].text
    image = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')[0].get('src')
    # “#”代表 id 这个找元素其实就是找他在页面的唯一
    host_name = soup.select('#floatRightBox > div.js_box.clearfix > div > h6 > a.lorder_name')[0].get('title')
    host_gender = soup.select('#floatRightBox > div.js_box.clearfix > div > h6 > span')[0].get('class')[0]
    # print(title, address, price, image, host_name, host_gender, sep='\n---------\n')

    if host_gender == 'member_girl_ico':
        host_sex = 'Girl'
    if host_gender == 'member_boy_ico':
        host_sex = 'Boy'

    data = {
        'HouseName': title,
        'HouseAddress': address,
        'DayPrice': price,
        'HostPicture': image,
        'HostName': host_name,
        'HostGender': host_sex
    }
    print(data)


def get_number_of_pages_link(number_of_pages):
    """
    full_url = 'http://bj.xiaozhu.com/search-duanzufang-0//'    # 注意观察发现第一页的地址跟后面的地址不一样， 但是不需要处理
    wb_data = requests.get(full_url, headers_rents)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('a.resule_img_a'):  # 找到这个 class 样为resule_img_a 的 a 标签即可
        print(link)
        page_link.append(link.get('href'))
    """
    for each_number in range(1, number_of_pages):   # 每页24个链接,这里输入的是页码
        full_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(each_number)
        time.sleep(300)
        wb_rent_pages_data = requests.get(full_url, headers_rents)
        soup = BeautifulSoup(wb_rent_pages_data.text, 'lxml')
        for link in soup.select('a.resule_img_a'):  # 找到这个 class 样为resule_img_a 的 a 标签即可
            print(link)
            pages_link.append(link.get('href'))
    print(pages_link)
    print(pages_link.__len__())


# get_number_of_pages_link(10)
# get_rent_details(url_rent_details)    # For Test
"""
for each_page in pages_link:
    time.sleep(60)
    get_rent_details(each_page)
"""
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# 爬取商品信息
url_KnewOne = 'https://knewone.com/discover?page='


def get_things_page(url_things, data=None):
    wb_things_page = requests.get(url_things)
    soup = BeautifulSoup(wb_things_page.text, 'lxml')
    images = soup.select('a.cover-inner > img')
    titles = soup.select('section.content > h4 > a')
    links = soup.select('div.interactions > span.fancy_button > a')
    fanciers = soup.select('div.interactions > span > a > span')
    # print(images, titles, links, fanciers, sep='\n----------\n')

    if data is None:
        for fanciers, title, image, link in zip(fanciers, titles, images, links):
            data = {
                'Likes': fanciers.get_text(),
                'Title': title.get('title'),
                'Image': image.get('src'),
                'DetailLink': link.get('data-link')
            }
            print(data)


def get_number_of_pages_things(start, end):
    for page_number in range(start, end):
        get_things_page(url_KnewOne + str(page_number))
        time.sleep(5)


# get_number_of_pages_things(1, 1)
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# 爬取图片
# 'http://weheartit.com/inspirations/beach?page=8' full url


base_url = 'http://weheartit.com/inspirations/beach?page='      # 多网页爬取时的基地址
path = 'E:\Picture\\'       # 本地存储目录，必须为绝对路径
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}
# 此网站会有针对 ip 的反爬取，可以采用代理的方式，但是一般的代理不稳定，稳定的代理需要花钱。。。
proxies = {
        "http": "31.145.138.134:55463"
    }


def loading(block_number, block_size, total_size):
    """
    回调函数: 数据传输时自动调用
    block_number:已经传输的数据块数目
    block_size:每个数据块字节
    total_size:总字节
    """
    percent = int(100 * block_number * block_size / total_size)
    if percent > 100:
        percent = 100
    print("Downloading:{}%".format(percent))


def get_images_url(start_page, number_of_pages):
    for page_number in range(start_page, start_page + number_of_pages):
        x = 0
        full_image_url = base_url + str(page_number)
        wb_images_data = requests.get(full_image_url, headers)
        soup = BeautifulSoup(wb_images_data.text, 'lxml')
        # names = soup.select('span.text-overflow > a > span.text-big')     # 实际爬取中发现有的图片中没有名字
        images = soup.select('img.entry-thumbnail')

        for image in images:
            data = {
                'ImageSrc': image.get('src')
            }
            print(data)
            file_name = path + str(page_number) + '_' + str(x) + '.jpg'    # 必须为绝对路径
            image_src = data.get('ImageSrc')
            urllib.request.urlretrieve(image_src, file_name, reporthook=loading, data=None)
            print('Download %s Finished! wait for 10 seconds' % (str(page_number) + '_' + str(x)))
            x += 1
            time.sleep(10)

        print('The Page %d Download Finished! wait for 60 seconds' % page_number)
        time.sleep(60)


# get_images_url(80, 20)
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# 爬取58二手商品信息

# 'https://bj.58.com/pbdn/?/'


headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}


def get_page_links_from(who_sells):      # 选择是个人出售还是商家
    goods_links = []
    page_link = 'https://bj.58.com/pbdn/{}/'.format(str(who_sells))
    wb_page_data = requests.get(page_link)
    soup = BeautifulSoup(wb_page_data.text, 'lxml')
    for link in soup.select('div > table.tbimg >  tr > td.t > a'):
        # 选取被问号分割后的的第一部分，即前半部分。通过分析多个页面发现问号后面的字符没有用，关注前面的字符
        # print(link)
        goods_links.append(link.get('href').split('?')[0])
    print(goods_links)
    return goods_links


def get_views_times_from(goods_link):       # 得到浏览量，该值时由JS控制，需要找到请求ID，一般在source中可看到,没有成功！
    # 观察网址地址和JS的请求ID，为网址链接中的一串数字，通过分割，去除操作得到数字
    view_id = goods_link.split('/')[-1].strip('x.shtml')
    print(view_id)
    js_api = 'http://jst1.58.com/counter?infoid={}'.format(view_id)     # 查询接口
    print(js_api)
    js_data = requests.get(js_api)      # 请求JS脚本的数据
    views_times = js_data.text.split('=')[-1]   # [-1] 表示倒数第一个
    print(views_times)
    return views_times


def get_goods_details_from(who_sells=0):        # 默认情况为0，即在调用函数时候如果不指定who_sells参数值，则取0
    for good_link in get_page_links_from(who_sells):
        wb_good_data = requests.get(good_link, headers)
        soup = BeautifulSoup(wb_good_data.text, 'lxml')
        data = {
            'Title': soup.title.text,
            'Price': (soup.select('span.infocard__container__item__main__text--price')[0].text.split('元')[0].split('\t\t\t\t\t\t'))[4],
            'Area': list(soup.select('div.infocard__container__item__main')[2].stripped_strings),
            'Date': soup.select('div.detail-title__info > div')[0].text,
            'Cate': '个人' if who_sells == 0 else '商家',
            'Views': get_views_times_from(good_link)
        }
        print(data)
        time.sleep(30)


# get_goods_details_from(0)
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# 使用CSV库，将数据存储到CSV文件中
def get_data_to_csv(url_link, csv_path):
    url_link_bs_obj = get_link_page_bs_obj(url_link, 'html.parser')
    if url_link_bs_obj is not None:
        page_url_data = get_bs_obj_data(url_link_bs_obj)
        # 将得到的数据写入CSV文件中，python的文件机制处理很到位，如果文件不存在，那么新建，如果存在，那么覆盖其内容。
        csv_file = open(csv_path, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csv_file)   # 创建文件读写器
        try:
            for row in page_url_data:
                csv_row = []
                for cell in row.findAll(['th', 'td']):
                    csv_row.append(cell.get_text())
                writer.writerow(csv_row)    # 将提取到一行写入
        finally:
            csv_file.close()
            print('\033[1;33m Success to get the data to ' + path_csv)
    else:
        return None


# 使用BS进行网二分析并返回bs_obj
def get_link_page_bs_obj(url_link, url_parser):
    try:
        html = urlopen(url_link)
    except (HTTPError, URLError) as e:
        # 网页在服务器上不存在(404 Page Not Found)或者获取页面时出现错误(500 Internal Server Error)
        # 打印的信息显示颜色: print('\033[显示方式;字体色;背景色m + 打印的内容')
        print('\033[1;31m Error occurred when request the url %s:' % url_link)  # 使用红色字体表示Error发生
        print(e)
        return None
    page_url_bs_obj = BeautifulSoup(html, url_parser)
    return page_url_bs_obj


# 从bs_obj格式的数据中提取有用的属性或其他信息
def get_bs_obj_data(bs_obj):
    try:
        # 这里选取了所有class 中第一词组为wikitable的table所组成的列表的第一个
        page_url_data_table = bs_obj.findAll('table', {'class': 'wikitable'})[0]
        page_url_data = page_url_data_table.findAll('tr')
    except AttributeError as e:
        print('\033[1;31m Error occurred when find the tag of src')  # 使用红色字体表示Error发生
        print(e)
        return None
    return page_url_data


path_csv = 'editors.csv'
page_url = 'https://en.wikipedia.org/wiki/Comparison_of_text_editors'
get_data_to_csv(page_url, path_csv)
