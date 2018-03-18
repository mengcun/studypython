# -*- coding: utf8 -*-
#可以参考网络上这个：https://github.com/lepture/captcha.git
from captcha.image import ImageCaptcha # pip install captcha Python验证码库，能够生成音频和图片验证码
import numpy as np #是一个强大的计算库，numpy模块提供了python对N维数组对象的支持
import matplotlib.pyplot as plt
from PIL import Image
import random
 
# 验证码中的字符, 就不用汉字了
number = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):
	captcha_text = []
	for i in range(captcha_size):
		c = random.choice(char_set)
		captcha_text.append(c)
	return captcha_text
 
# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha()
 
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text) #以''(这里表示空)为间隔符，将captcha_text中所有的元素组成字符串
 
    captcha = image.generate(captcha_text)
    #image.write(captcha_text, captcha_text + '.jpg')  # 写到文件,可用来查看效果，在实际训练中不要写入，否则大量文件会被创建到本地
 
    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image) #将图片转成数组形式
    #print captcha_image #可用来查看效果，在实际训练中不要打印，影响效率
    return captcha_text, captcha_image

if __name__ == '__main__':
    #进行测试
    text, image = gen_captcha_text_and_image()

    f = plt.figure() #你可以多次使用figure命令来产生多个图，其中，图片号按顺序增加
    ax = f.add_subplot(111) #添加子图
    #text()可以在图中的任意位置添加文字，并支持LaTex语法
    ax.text(0.1, 0.9, text, ha = 'center', va = 'center', transform = ax.transAxes) 
    plt.imshow(image)

    plt.show()
