from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict

"""
create time: 2018-11-09
自然语言处理过程中需要根据项目要求对数据源进行处理：（可以直接使用OpenRefine第三方工具）
1.数据清理
    将数据统一大小写
    剔除回车符号,替换成空格
    剔除单字符的单词，替换成空格，除非这个字符是‘i’或者‘a’
    剔除引用标记（方括号包裹的数字，如[1]），替换成空格
    剔除标点符号，替换成空格（注意，这个规则有点矫枉过正，剔除连字符号，替换成空格，但是引来的问题是真正的连字符怎么处理）
2.数据格式化
    通常可以将数据按空格分开

3.对得到的数据进行去重操作，这里用到了python的collections 库里的OrderedDict
"""


def clean_input_data(input_data):
    cleaned_input_data = []
    input_data = re.sub('\n', ' ', input_data)
    input_data = re.sub("\[[0-9]*\]", ' ', input_data)
    input_data = re.sub(' +', ' ', input_data)
    input_data = bytes(input_data, 'UTF-8')
    input_data = input_data.decode('ascii', 'ignore')
    input_data = input_data.upper()
    input_data = input_data.split(' ')
    for item in input_data:
        item = item.strip(string.punctuation)   # 剔除标点符号 string.punctuation获取所有的标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleaned_input_data.append(item)
    return cleaned_input_data


# 对数据进行分解,按照参数n分解成['data1', 'data2'],并去重
def n_grams(input_data, n):
    output_data = []
    cleaned_data = clean_input_data(input_data)
    # print(cleaned_data)   # 数据太大，谨慎打印
    print('The len of the cleaned_data:' + str(len(cleaned_data)))
    for i in range(len(cleaned_data) - n + 1):
        output_data.append(cleaned_data[i: (i+n)])
    return output_data


html = urlopen('https://en.wikipedia.org/wiki/Python_(programming_language)')
bs_obj = BeautifulSoup(html, 'html.parser')
content = bs_obj.find('div', {'id': 'mw-content-text'}).get_text()
# print(content)
data = n_grams(content, 2)
print(data)
