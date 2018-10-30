from bs4 import BeautifulSoup
path = "./Ref/index.html"  #这里使用了相对路径,只要你本地有这个文件就能打开
info = []
with open(path, 'r') as wb_data:    # 使用with open打开本地文件
    soup = BeautifulSoup(wb_data, 'lxml')   # 解析网页内容
    #print(soup)    #打印解析到的网页
    # 复制每个元素的css selector 路径即可得到，注意观察，去除一些不必要的子路径
    titles = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    images = soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    reviews = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    prices = soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    stars = soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
    # 为了从父节点开始取,此处保留:nth-of-type(2),观察网页,多取几个星星的selector,就发现规律了
    #print(titles,images,reviews,prices,stars,sep='\n--------\n')    # 打印每个元素,其中sep='\n--------\n'是为了在不同元素之间添加分割线

    for title, image, review, price, star in zip(titles, images, reviews, prices, stars):   # 使用for循环,把每个元素装到字典中
        data = {
            'title': title.get_text(),  # 使用get_text()方法取出文本
            'image': image.get('src'),  # 使用get 方法取出带有src的图片链接
            'review': review.get_text(),
            'price': price.get_text(),
            'star': len(star.find_all("span", class_="glyphicon glyphicon-star"))
        # 观察发现,每一个星星会有一次<span class="glyphicon glyphicon-star"></span>,所以我们统计有多少次,就知道有多少个星星了;
        # 使用find_all 统计有几处是★的样式,第一个参数定位标签名,第二个参数定位css 样式,具体可以参考BeautifulSoup 文档示例http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#find-all;
        # 由于find_all()返回的结果是列表,我们再使用len()方法去计算列表中的元素个数,也就是星星的数量
        }
        print(data)
        info.append(data)

    for i in info:
        if float(i['star']) > 3:
            print(i['title'], i['price'])