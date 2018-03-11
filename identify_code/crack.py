# -*- coding: utf8 -*-

from PIL import Image
import hashlib
import time
import os
import math

#加载要识别的验证码图片
im = Image.open("captcha.gif")
#将图片转换为8位像素模式
im2 = Image.new("P", im.size, 255)
im.convert("P")
#可以打印颜色直方图方便理解
print im.histogram()

#颜色直方图的每一位数字都代表了在图片中含有对应位的颜色的像素的数量。
#每个像素点可表现256种颜色，发现白点是最多（白色序号255的位置，也就是最后一位，可以看到，有625个白色像素）
#红像素在序号200左右，我们可以通过排序，得到有用的颜色。
his = im.histogram()
#存储每个像素的数量的字典
values = {}
for i in range(256):
    values[i] = his[i]

#通过排序我们可以找到出现次数最多的前10种像素
"""
sorted(iterable, cmp=None, key=None, reverse=False)
     把iterable中的items进行排序之后，返回一个新的列表，原来的iterable没有任何改变
     1）iterable：iteralbe指的是能够一次返回它的一个成员的对象。iterable主要包括3类：
             1.第一类是所有的序列类型，比如list(列表)、str(字符串)、tuple(元组)。 
             2.第二类是一些非序列类型，比如dict(字典)、file(文件)。
             3.第三类是你定义的任何包含__iter__()或__getitem__()方法的类的对象。
     2) cmp：指定一个定制的比较函数，这个函数接收两个参数（iterable的元素），
             如果第一个参数小于第二个参数，返回一个负数；
             如果第一个参数等于第二个参数，返回零；
             如果第一个参数大于第二个参数，返回一个正数。默认值为None。
     3）key：指定一个接收一个参数的函数，这个函数用于从每个元素中提取一个用于比较的关键字。默认值为None。
             在这里使用的是出现次数：key = lambda x:x:[1]
     4）reverse：是一个布尔值。如果设置为True，列表元素将被降序排列，默认为升序排列。
通常来说，key和reverse比一个等价的cmp函数处理速度要快。这是因为对于每个列表元素，
cmp都会被调用多次，而key和reverse只被调用一次
"""
for j,k in sorted(values.items(), key = lambda x:x[1], reverse = True)[:10]:
    print j, k

#我们得到了图片中最多的10种颜色，其中 220 与 227
#才是我们需要的红色和灰色，可以通过这一讯息构造一种黑白二值图片
temp = {}
for x in range(im.size[1]): #这里的x取的是图片的宽
    for y in range(im.size[0]):#y取得是图片的长
        pix = im.getpixel((y,x))#最后的（y，x）其实就是图片的像素的坐标
        if pix == 220 or pix == 227:#得到所要的像素点
            #然后将目标像素点填充为黑色
            im2.putpixel((y,x) , 0)
#可以将得到的黑白二值图片展示
im2.show()

#得到黑白二值图后需要提取出单个字符图片，采用纵向切割，己沿着x轴进行分析
inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):#仍然y值对应图片长度，这里沿着图片的长也就是x轴进行切割
    for x in range(im2.size[1]):#x值对应图片的宽度 ，对图片的宽也就是Y轴上每个点扫描
        pix = im2.getpixel((y,x))#获取该点的像素值
        if pix != 255:#如果不是白色，则为字母值
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y #确定字母左上角起始的像素的x值位置
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))#这里每一个（）里是一个字母的沿x轴的起点和终点
    inletter = False
#将找到的字母的X轴的起始点终止点打印出来:(x1, x2)(x3, x4)(x5, x6)...
print letters

"""
在这里我们使用向量空间搜索引擎来做字符识别，它具有很多优点：

1.不需要大量的训练迭代
2.不会训练过度
3.你可以随时加入／移除错误的数据查看效果
4.很容易理解和编写成代码
5.提供分级结果，你可以查看最接近的多个匹配
6.对于无法识别的东西只要加入到搜索引擎中，马上就能识别了。

当然它也有缺点，例如分类的速度比神经网络慢很多，它不能找到自己的方法解决问题等等。

简单原理：两向量的点积 = 两向量的的模的乘机 * cos(a,b) 其中cos(a,b) 的值就是相似度:

关于向量空间搜索引擎的原理可以参考这篇文章：http://ondoc.logand.com/d/2697/pdf
"""

#python类实现向量空间，比较两个python字典类型并输出他们的相似度（用0～1的数字表示）
class VectorCompare:
    #计算矢量大小,即向量的模
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems(): #在python2.7版本中，.iteritems 返回字典的迭代器
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        relevace = 0
        topvalue = 0
        #遍历concordance1中的键值对，返回的是迭代器
        for word, count in concordance1.iteritems():
            #当concordance2中也有对应的值时
            if concordance2.has_key(word):
                #那么计算所有对应值的乘积和（也就是向量的点积）
                topvalue += count * concordance2[word]
        #最后计算他们的相似度
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

#将图片转换为矢量{(0,a),(1,b),(2,c) ...}
def buildvector(im):
    d1 = {}
    count = 0
    #getdata : 返回一个图像内容的像素值序列。
    #不过，这个返回值是PIL内部的数据类型，只支持确切的序列操作符，包括迭代器和基本序列方法
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

#训练集合的文件夹名称，用于加载训练集
iconset =  ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#加载当前目录下的训练集
imageset = []#也是字典列表，最终这里存放的是每个字母的矢量图：[{0:temp}, {1:temp}, ...]

for letter in iconset:
    for img in os.listdir('./iconset/%s'%(letter)):
        temp = []#这里的temp[]最终是个字典列表：[{(0,a),(1,b),...}, ...]
                 #注意，因为有的字母文件夹下不止一张图片，所以一个temp列表中可能存在多个字典
        #注意不要加载以下两个文件
        if img != "Thumbs.db" and img != ".DS_Store":
            #打开本地目录下文件夹内的img文件并将其转为矢量后添加到temp[]
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter, img))))
        #最后生成一个键值对的字典列表
        imageset.append({letter:temp})

#对图片进行切割，得到每个字符所在的那部分图片然后进行分析
v = VectorCompare() #实例一个向量空间类

count =0 #用于摘要算法
for letter in letters:
    #摘要算法，详见：https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328251266d86585fc9514536a638f06b41908d44000
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    m.update("%s%s"%(time.time(), count))
    im3.save("./%s.gif"%(m.hexdigest()))

    #进行机器识别
    guess = []
    #调用训练集来匹配
    for image in imageset:  #这里的image是{0:temp},所有的训练集合都要与之匹配一次，找出相似度最大的并打印
        for x,y in image.iteritems():
            if len(y) != 0: #当训练集的矢量不为空时候,这里的y是 temp, 也就是图片的矢量图 [{(0,a),(1,b),(3,c) ...}, ...]
                            #注意，因为有的字母文件夹下不止一张图片，所以一个temp列表中可能存在多个字典
                #计算训练集中的样本字母和当前得到的字符的相似度
                #这里的 guess[]最终是相似度的一个列表[(cos值，'letter'),(cos值, 'letter'),(cos值, 'letter'),...]
                guess.append((v.relation(y[0], buildvector(im3)), x))  
                #y[0]在这里表示只对temp矢量集合中的第一个字典集合与所要验证的图片的矢量集合进行操作，
                #也可更改y[0]为其他值，但要保证所有的训练集中有对应的样本
                #并将每次的匹配都加入guess[]列表。
        guess.sort(reverse = True)  #将所有相似度按照从大到小排序
    print "", guess[0]  #将最大相似度的值打印出来，就是该letter的值，然后进行下一个值的匹配

count += 1 #用于更新摘要
