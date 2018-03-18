# -*- coding: utf-8 -*-
from code_generate import gen_captcha_text_and_image
from code_generate import number
from code_generate import alphabet
from code_generate import ALPHABET

import numpy as np
import tensorflow as tf

text, image = gen_captcha_text_and_image()
print('验证码图像channel:', image.shape) #(60, 160, 3)

#图像大小
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
MAX_CAPTCHA = len(text)
print('验证码文本最长字符数', MAX_CAPTCHA)

#把彩色图像转换成灰度图
def convert2gray(img):
    if len(img.shape) > 2:
        gray = np.mean(img, -1)
        #上面的转法比较快，正规转法如下
        #r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        #gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img

"""
cnn在图像大小是2的倍数时性能最高，如果你用的图像大小不是2的倍数，可以在图像边缘补充无用像素
np.pad( image, ((2,3),(2,2)), 'constant', connstant_value=(255,) ) 这里是在图像上补两行
"""

#文本转向量
"""
返回的向量是一维数组，1代表匹配到的字符，其他区域为0表示
向量(大小MAX_CAPTCHA * CHR_SET_LEN)用0，1编码，每63个编码一个字符
"""
char_set = number + alphabet + ALPHABET + ['_'] #如果验证码长度小于4， 使用'_'来补齐
CHAR_SET_LEN = len(char_set)
def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('验证码最长4个字符')
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN) #"返回来一个大小为MAX_CAPTCHA * CHAR_SET_LEN的一维数组"
    def char2pos(c):
        if c == '_':
            k = 62
            return k
        k = ord(c) - 48 #判断是不是0-9
        """
        ord()函数是chr()函数（对于8位的ASCII字符串）或unichr()函数（对于Unicode对象）的配对函数，
        它以一个字符（长度为1的字符串）作为参数，返回对应的ASCII数值，或者Unicode数值，
        如果所给的Unicode字符超出了你的Python定义范围，则会引发一个TypeError的异常
        """
        if k > 9 :
            k = ord(c) - 55 #K = 90 时， 是大写字母Z的ACSII
            if k > 35: 
                k = ord(c) - 61 #K = 122时， 是小写字母z的ASCII
                if k > 61:
                    raise ValueError('No Map')
        return k
    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + char2pos(c) #使用63个编码为一个字符，这里确定了字符在一维向量中的位置
        vector[idx] = 1 #在该位置填1代表该字符
    return vector

#向量转回文本
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
    char_pos = vec.nonzero()[0] #这里返回的是一维数组，即数组vec中不为0的索引
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i # c/63 这里确定了该字符是text中的第几个（0，1，2，3）
        char_idx = c % CHAR_SET_LEN # c%63 这里确定是该字符在char_set中的索引，下面是对索引分情况处理
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
        text.append(chr(char_code))
    return "".join(text)

#生成一个训练batch
def get_next_batch(batch_size = 128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH]) #生成表示图片的二维向量，也就是输入图片的矩阵？？？？？？
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN]) #生成一个二维向量，这里是过滤器？？？？？？
    #有时生成的图像大小不是(60,160,3):
    def wrap_gen_captcha_text_and_image():
        while True:
            text, image = gen_captcha_text_and_image()
            if image.shape == (60, 160 ,3):
                return text, image

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)
        #x[:,i]表示取所有维中第i个数据，通常返回数组
        #x[:,m:n]，即取所有维中第m到n-1个数据，含左不含右
        #x[i,:]表示取第一维中下标为i的所有元素，通常返回数组
        #flatten() 是将多维数组降位到一维并返回拷贝，默认降维是横向的
        batch_x[i,:] = image.flatten() / 255 #(image.flatten()-128)/128  mean为0
        batch_y[i,:] = text2vec(text)
    return batch_x, batch_y
#####################################################################################################################
#这里开始tensorflow
X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA* CHAR_SET_LEN])

keep_prob = tf.placeholder(tf.float32) #dropout

#定义CNN
def crack_captcha_cnn(w_alpha = 0.01, b_alpha = 0.1):
    x = tf.reshape(X, shape = [-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    #w_c1_alpha = np.sqrt(2.0/(IMAGE_HEIGHT*IMAGE_WIDTH)) #
    #w_c2_alpha = np.sqrt(2.0/(3*3*32)) 
    #w_c3_alpha = np.sqrt(2.0/(3*3*64)) 
    #w_d1_alpha = np.sqrt(2.0/(8*32*64))
    #out_alpha = np.sqrt(2.0/1024)

    # 3 conv layer
    w_c1 = tf.Variable(w_alpha*tf.random_normal([3, 3, 1, 32]))
    b_c1 = tf.Variable(b_alpha*tf.random_normal([32]))
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv1 = tf.nn.dropout(conv1, keep_prob)

    w_c2 = tf.Variable(w_alpha*tf.random_normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha*tf.random_normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)

    w_c3 = tf.Variable(w_alpha*tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha*tf.random_normal([64]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    # Fully connected layer
    w_d = tf.Variable(w_alpha*tf.random_normal([8*20*64, 1024]))
    b_d = tf.Variable(b_alpha*tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, keep_prob)

    w_out = tf.Variable(w_alpha*tf.random_normal([1024, MAX_CAPTCHA*CHAR_SET_LEN]))
    b_out = tf.Variable(b_alpha*tf.random_normal([MAX_CAPTCHA*CHAR_SET_LEN]))
    out = tf.add(tf.matmul(dense, w_out), b_out)
    #out = tf.nn.softmax(out)
    return out

#开始训练
"""
CNN需要大量的样本进行训练，由于时间和资源有限，测试时可只使用数字做为验证码字符集。
如果使用数字+大小写字母CNN网络有4*62个输出，只使用数字CNN网络有4*10个输出
"""
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # loss
    #loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, Y))
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    # 最后一层用来分类的softmax和sigmoid有什么不同？
    # optimizer 为了加快训练 learning_rate应该开始大，然后慢慢衰
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        step = 0
        while True:
            batch_x, batch_y = get_next_batch(64)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            print(step, loss_)

            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc)
                # 如果准确率大于50%,保存模型,完成训练
                if acc > 0.5:
                    saver.save(sess, "crack_capcha.model", global_step=step)
                    break
            step += 1

train_crack_captcha_cnn()
