from bs4 import BeautifulSoup
import requests
import time
import urllib.request

url_movies = 'https://movie.douban.com/chart'
headers_movies = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': 'bid=o5R_UMszexM; gr_user_id=1c7c52b4-fb38-4f2b-a0db-01e2246833eb; _vwo_uuid_v2=D977B7F9701C9756A9DEEB0D0DC9CA031|334402f021eaf5e873e1d898441ff714; viewed="1168618_1310376_1231162_26614049_10773324"; douban-fav-remind=1; ll="108288"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1540371723%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1589339816.1519868013.1539069620.1540371723.9; __utmb=30149280.0.10.1540371723; __utmz=30149280.1540371723.9.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1979596219.1540371723.1540371723.1540371723.1; __utmb=223695111.0.10.1540371723; __utmz=223695111.1540371723.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=Q1bqtJak2lfrw9z08pqANUmwUo3G2UP2; __utmc=30149280; __utmc=223695111; as="https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action="; ps=y; dbcl2="147782006:OFXc6p9b9y4"; ck=L6JE; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=c71b97126997c509.1540371723.1.1540374175.1540371723.'
}


def get_movies_top(url, data=None):
    wb_movies_data = requests.get(url, headers_movies)
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
# ----------------------------------------------------------------------------------------------------------------------


url_rent_details = 'http://bj.xiaozhu.com/fangzi/35337972403.html'
pages_link = []  # 批量获取链接 <- 每个详情页的链接都存在这里，解析详情的时候就遍历这个列表然后访问就好啦~
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


# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------


# 'http://weheartit.com/inspirations/beach?page=8' full url


base_url = 'http://weheartit.com/inspirations/beach?page='
path = 'E:\Picture\\'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}
# 此网站会有针对 ip 的反爬取，可以采用代理的方式
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


def get_images_url(number_of_pages):
    x = 0
    page = 8
    for page_number in range(9, number_of_pages+1):
        page += 1
        full_image_url = base_url + str(page_number)
        wb_images_data = requests.get(full_image_url, headers)
        soup = BeautifulSoup(wb_images_data.text, 'lxml')
        # names = soup.select('span.text-overflow > a > span.text-big')
        images = soup.select('img.entry-thumbnail')

        for image in images:
            data = {
                'ImageSrc': image.get('src')
            }
            print(data)
            file_name = path + str(page) + '_' + str(x) + '.jpg'    # 必须为绝对路径
            image_src = data.get('ImageSrc')
            urllib.request.urlretrieve(image_src, file_name, reporthook=None, data=None)
            print('Download %s Finished! wait for 10 seconds' % (str(page) + '_' + str(x)))
            x += 1
            time.sleep(10)

        print('The Page %d Download Finished' % page)
        time.sleep(60)


# get_movies_top(url_movies)
# get_number_of_pages_link(10)
# get_rent_details(url_rent_details)    # For test
# get_number_of_pages_things(1, 1)
# get_images_url(2) # For test
get_images_url(100)

"""
for each_page in pages_link:
    time.sleep(60)
    get_rent_details(each_page)
"""
