# -*- coding: utf8 -*-
import numpy as np

from cfg import MAX_CAPTCHA, CHAR_SET_LEN


def char2pos(c):
    """
    字符验证码，字符串转成位置信息,即在cfg.py中的数字字母表中的位置
    :param c:
    :return:
    """
    if c == '_':
        k = 62
        return k
    k = ord(c) - 48 #判断是不是0-9
    """
    ord()函数是chr()函数（对于8位的ASCII字符串）或unichr()函数（对于Unicode对象）的配对函数，
    它以一个字符（长度为1的字符串）作为参数，返回对应的ASCII数值，或者Unicode数值，
    如果所给的Unicode字符超出了你的Python定义范围，则会引发一个TypeError的异常
    """
    if k > 9:
        k = ord(c) - 55 #K = 90 时， 是大写字母Z的ACSII
        if k > 35:
            k = ord(c) - 61 #K = 122时， 是小写字母z的ASCII
            if k > 61:
                raise ValueError('No Map')
    return k


def pos2char(char_idx):
    """
    根据位置信息转化为索引信息
    :param char_idx:
    :return:
    """
    #
    # if not isinstance(char_idx, int64):
    #     raise ValueError('error')

    if char_idx < 10:
        char_code = char_idx + ord('0')
    elif char_idx < 36:
        char_code = char_idx - 10 + ord('A')
    elif char_idx < 62:
        char_code = char_idx - 36 + ord('a')
    elif char_idx == 62:
        char_code = ord('_')
    else:
        raise ValueError('error')

    return chr(char_code)

#把彩色图像转换成灰度图
def convert2gray(img):
    """
    把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
    :param img:
    :return:
    """
    if len(img.shape) > 2:
        gray = np.mean(img, -1)
        # 上面的转法较快，正规转法如下
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


def text2vec(text):
    """
    返回的向量是一维数组，1代表匹配到的字符，其他区域为0表示
    向量(大小MAX_CAPTCHA * CHR_SET_LEN)用0，1编码，每63个编码一个字符
    """
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('验证码最长4个字符')

    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    #"返回来一个大小为MAX_CAPTCHA * CHAR_SET_LEN的一维数组"

    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + char2pos(c) #使用63个编码为一个字符，这里确定了字符在一维向量中的位
        vector[idx] = 1 #在该位置填1代表该字
    return vector


# 向量转回文本
def vec2text(vec):
    """
    nonzero函数是numpy中用于得到数组array中非零元素的位置（数组索引）的函数。它的返回值是一个长度为
    a.ndim(数组a的轴数)的元组，元组的每个元素都是一个整数数组，其值为非零元素的下标在对应轴上的值。

    （1）只有a中非零元素才会有索引值，那些零值元素没有索引值；
    （2）返回的索引值数组是一个2维tuple数组，该tuple数组中包含一维的array数组。其中，一维array向量的个数与a的维数是一致的。
    （3）索引值数组的每一个array均是从一个维度上来描述其索引值。比如，如果a是一个二维数组，则索引值数组有两个array，第一个array从行维度来描述索引值；第二个array从列维度来描述索引值。
    （4）transpose(np.nonzero(x))函数能够描述出每一个非零元素在不同维度的索引值。
    （5）通过a[nonzero(a)]得到所有a中的非零值
    这里以实例说明：
    一维数组：a = [0,2,3] --> [1,2]:因为a是一维，所以得到的结果也是一个一维数组，[1,2]，注意从0开始。表示：第2个和第3个.
    二维数组：a = [[0,0,3],[0,0,0],[0,0,9]]:因为是二维，所以得到的结果也是两个一维数组，array1=[0,2]， array2=[2,2], 
                                            表示：array1中的第一个元素0和array2中的第一个元素2共同表示二位数组中第一个[0,0,3]中的3
                                                  array1中的第二个元素2和array2中的第二个元素2共同表示二位数组中第三个[0,0,9]中的9
    三维数组：a = [ [[0,0],[1,0]],[[0,0],[1,0]],[[0,0],[1,0]] ]:因为是三维，所以得到的是三个一维数组，array1=[0,1,2], array2=[1,1,1], array3=[0,0,0]
                                                                表示：array1中的第一个元素0表示[[0,0],[1,0]]
                                                                      array2中的第一个元素1表示上面[[0,0],[1,0]]中的[1,0]
                                                                      array3中的第一个元素0表示上面[1,0]的1
    """
    char_pos = vec.nonzero()[0] #这里返回的是一维数组，即数组vec中不为0的索
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i  # c/63 这里确定了该字符是text中的第几个（0，1，2，3
        char_idx = c % CHAR_SET_LEN # c%63 这里确定是该字符在char_set中的索引，下面是对索引分情况处理

        char_code = pos2char(char_idx)

        text.append(chr(char_code))
    return "".join(text)

if __name__ == '__main__':
    text = 'XD8K' #用来测试
    print(text2vec(text)) #用来测试
