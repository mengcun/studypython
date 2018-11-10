from urllib.request import urlopen
from urllib.error import URLError   # 用于URL链接本身的错误处理
from requests import HTTPError      # 用于HTTP请求的错误处理
from bs4 import BeautifulSoup
from io import StringIO             # 用于将在线csv文件转换成StringIO对象，使其具有文件属性
from io import BytesIO              # 用于将在线doc文件转换成二进制文件对象
from pdfminer.pdfinterp import PDFResourceManager, PDFResourceError, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import csv                          # 用于csv文件的读取
from zipfile import ZipFile

"""
从互联网中读取文本文档时，网站会在<head>部分显示网页使用的编码格式，注意查看
三种编码格式：
1.Unicode： 包括utf-8,utf-16,utf-32  可以编码全球不同的语言
2.ASCII： 大多数英文网站使用
3.ISO系列字符集：目前仍有9%的网站使用
"""
text_url = 'https://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt'


# 读取链接给出的文本文档，并将其转换成UTF-8格式
def open_text_url(page_url):
    try:
        text_page = urlopen(page_url)
    except (HTTPError, URLError) as e:
        print('\033[1;31m Error occurred when request the url %s' % page_url)
        print(e)
        return None
    # content = str(text_page.read(), 'UTF-8')    # 直接将字符装换成UTF-8编码格式
    # print(content)
    # content = bytes(content, 'UTF-8)')  # 将得到的文本转换成字节流，并按照utf-8格式进行编码

    content = text_page.read()
    content = content.decode('UTF-8')   # 将得到的编码的文件按照utf-8格式解码
    print(content)
    return content


"""
读取csv格式文件时，因为python的csv库主要是面对本地文件，
1.在读取在线csv格式文件时，可以将其读成字符串，然后封装成StringIO对象，使其具有文件属性。
2.在使用csv库读取时候，有两种形式：csv_reader返回的是列表形式的数据，csv_dic_reader返回的是字典形式的数据
"""
csv_url = 'https://www.pythonscraping.com/files/MontyPythonAlbums.csv'


def open_csv_url(page_url):
    try:
        csv_page = urlopen(page_url)
    except (HTTPError, URLError) as e:
        print('\033[1;31m Error occurred when request the url %s' % page_url)
        print(e)
        return None

    # 使用库在线读取，返回的csv_reader对象是列表，可迭代的
    print('\033[1;31m Using csv_reader to get the list_data.')
    csv_data = csv_page.read()  # 获取csv文件的内容
    csv_data = csv_data.decode('ascii', 'ignore')   # 将csv文件中的内容按ASCII解码
    csv_data = StringIO(csv_data)   # 将编码后的内容封装成StringIO对象，可以被Python的csv库处理
    csv_reader = csv.reader(csv_data)
    for row in csv_reader:
        print('\033[1;33m The album \'' + row[0] + '\'was released in ' + str(row[1]))
        print(row)

    # 使用库在线读取，返回的csv_dic_reader对象是字典，同时字段保存在csv_dic_reader.filenames里，字段同时作为字典的键
    print('\033[1;31m Using csv_dic_reader to get the dict_data.')
    csv_data = csv_page.read()  # 获取csv文件的内容
    csv_data = csv_data.decode('ascii', 'ignore')  # 将csv文件中的内容按ASCII解码
    csv_data = StringIO(csv_data)  # 将编码后的内容封装成StringIO对象，可以被Python的csv库处理
    csv_dic_reader = csv.DictReader(csv_data)
    print(csv_dic_reader.fieldnames)
    for row in csv_dic_reader:
        print('\033[1;33m The album \'' + row['Name'] + '\' was released in ' + row['Year'])
        print(row)


"""
PDF: portable document format 便携式文档格式
可以在不同系统上用同样的方式查看图片和文本文档，无论这些文件时在哪种系统上制作的
第三库中的PDFMiner3K可以方便的读取PDF文档
"""

pdf_url = 'https://www.pythonscraping.com/pages/warandpeace/chapter1.pdf'


def open_pdf_url(page_url):
    try:
        pdf_page = urlopen(page_url)
    except (HTTPError, URLError) as e:
        print('\033[1;31m Error occurred when request the url %s' % page_url)
        print(e)
        return None

    pdf_resource_manager = PDFResourceManager()
    pdf_resource = StringIO()
    pdf_param = LAParams()
    # 将pdf格式文档以字符串形式读出并转换成StringIO对象格式
    pdf_reader = TextConverter(pdf_resource_manager, pdf_resource, laparams=pdf_param)  # 创建pdf读取器
    process_pdf(pdf_resource_manager, pdf_reader, pdf_page)     # 使用pdf读取器读取文件
    pdf_reader.close()
    content = pdf_resource.getvalue()
    pdf_resource.close()
    print(content)
    return content


"""
对word文档的处理比较繁琐，主要是因为里面包含了大量的信息
1.先把文档读成一个二进制文件对象
2.再用Python标准库zipfile解压（所有的.docx文件为了节省空间都进行过压缩）
3.读取该解压文件，得到XML格式文件
"""

word_url = 'https://www.pythonscraping.com/pages/AWordDocument.docx'


def open_word_url(page_url):
    try:
        word_page = urlopen(page_url)
    except (HTTPError, URLError) as e:
        print('\033[1;31m Error occurred when request the url %s' % page_url)
        print(e)
        return None
    word_data = word_page.read()
    # print(word_data)
    word_data_bin = BytesIO(word_data)      # 将word文档页面转换成一个二进制文件
    # print(word_data_bin)
    word_data_zip = ZipFile(word_data_bin)      # 使用标准库zipfile解压（因为所有的.doc文件为了节省空间都进行过压缩）
    # print(word_data_zip)
    xml_content = word_data_zip.read(word_data_zip.namelist()[0])  # 读取解压后的文件，得到的是xml格式
    print(xml_content)
    word_bs_obj = BeautifulSoup(xml_content.decode('utf-8'), 'html.parser')    # 将得到的xml格式的数据解码成utf-8格式
    print(word_bs_obj)
    text_string = word_bs_obj.find_all('w:t')   # 提取需要的信息
    print(text_string)
    for text_item in text_string:
        print(text_item.text)


# open_text_url(text_url)
# open_csv_url(csv_url)
# open_pdf_url(pdf_url)
open_word_url(word_url)
