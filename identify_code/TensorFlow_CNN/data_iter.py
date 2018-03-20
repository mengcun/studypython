# -*- coding: utf8 -*-
"""
数据生成器
"""

import numpy as np

from cfg import IMAGE_HEIGHT, IMAGE_WIDTH, CHAR_SET_LEN, MAX_CAPTCHA
from code_generate import wrap_gen_captcha_text_and_image
from utils import convert2gray, text2vec


def get_next_batch(batch_size=128):
    """
    # 生成一个训练batch
    :param batch_size:
    :return:
    """
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    #生成表示图片的二维向量，也就是输入图片的矩阵？？？？？？
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])
    #生成一个二维向量，这里是过滤器？？？？？？

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)
        #x[:,i]表示取所有维中第i个数据，通常返回数组
        #x[:,m:n]，即取所有维中第m到n-1个数据，含左不含右
        #x[i,:]表示取第一维中下标为i的所有元素，通常返回数组
        #flatten() 是将多维数组降位到一维并返回拷贝，默认降维是横向的

        batch_x[i, :] = image.flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y
