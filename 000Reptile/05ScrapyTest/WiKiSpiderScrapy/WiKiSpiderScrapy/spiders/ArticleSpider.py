from scrapy import Spider
from WiKiSpiderScrapy.items import WikiArticle

"""
收集每页的title字段
"""


class ArticleSpider(Spider):
    name = 'wiki_title_src'    # 该条目名称用来调用爬虫 #scrapy crawl wiki_title_src -s LOG_FILE=WiKiScrapy.log,
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page',
                  'https://en.wikipedia.org/wiki/Python_(programming_language)']

    def parse(self, response):
        item = WikiArticle()
        # //*[@id="firstHeading"]/text() 将 *[@id="firstHeading"] 换成了 h1
        # print(response.xpath('//h1/text()'))
        title = response.xpath('//h1/text()')[0].extract()
        print('Title is: ' + title)
        item['title'] = title
        return item
