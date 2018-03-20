# -*- coding: utf8 -*-
#可以参考网络上这个：https://github.com/lepture/captcha.git
from captcha.image import ImageCaptcha # pip install captcha Python验证码库，能够生成音频和图片验证码
import numpy as np #是一个强大的计算库，numpy模块提供了python对N维数组对象的支持
import matplotlib.pyplot as plt
from PIL import Image
import random
from os import path
from os.path import join
from cfg import number, alphabet, ALPHABET
from cfg import workspace
import uuid 

# 验证码一般都无视大小写；验证码长度4个字符,char_set 在cfg.py中
def random_captcha_text(char_set = number + alphabet + ALPHABET, captcha_size=4):
    """
    生成随机字符串，4位
    :param char_set:
    :param captcha_size:
    :return:
    """   
    captcha_text = []
    for i in range(captcha_size):
	    c = random.choice(char_set)
	    captcha_text.append(c)
    return captcha_text
    #print("The code is:", captcha_text) #用于调试，训练时候不要打开

# 生成字符对应的验证码
def gen_captcha_text_and_image():
    """
    生成字符对应的验证码
    :return:
    """
    image = ImageCaptcha()
 
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text) #以''(这里表示空)为间隔符，将captcha_text中所有的元素组成字符串
 
    captcha = image.generate(captcha_text)
    #image.write(captcha_text, captcha_text + '.jpg')  # 写到文件,可用来查看效果，在实际训练中不要写入，否则大量文件会被创建到本地
 
    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image) #将图片转成数组形式

    #print captcha_image #可用来查看效果，在实际训练中不要打印，影响效率
    return captcha_text, captcha_image

def wrap_gen_captcha_text_and_image():
    """
    有时生成图像大小不是(60, 160, 3)
    :return:
    """
    while True:
        text, image = gen_captcha_text_and_image()
        if image.shape == (60, 160 ,3):
            return text, image

def __gen_and_save_image():
    """
    可以批量生成验证图片集，并保存到本地，方便做本地的实验
    :return:
    """

    for i in range(2):
        text, image = wrap_gen_captcha_text_and_image()

        im = Image.fromarray(image)

        uuid_test = uuid.uuid1().hex
        #基于MAC地址，时间戳，随机数来生成唯一的uuid，可以保证全球范围内的唯一性
        image_name = '__%s__%s.png' % (text, uuid_test)

        img_root = join(workspace, 'train')
        image_file = path.join(img_root, image_name)
        im.save(image_file)

        print("图片%s保存到%s"%(image_name,img_root))  # (60, 160, 3) 用于调试，训练时不要打开


def __demo_show_img():
    """
    使用matplotlib来显示生成的图片
    :return:
    """
    text, image = wrap_gen_captcha_text_and_image()

    print("The iamge channel:", image.shape)  # (60, 160, 3)

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
    plt.imshow(image)

    plt.show()

if __name__ == '__main__':

    #__gen_and_save_image() #在进行训练时候不要保存图片
    #__demo_show_img()
    pass
