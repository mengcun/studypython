from smtplib import SMTP    # 用于发送邮件
from poplib import POP3     # 用于接收邮件
from time import sleep      # 用于休眠
from email.mime.text import MIMEText    # 邮件的正文部分

smtp_srv = 'smtp.sina.com.cn'      # smtp服务器地址
pop3_srv = 'pop3.sina.com'    # pop3服务器地址
message = MIMEText('This is the body of the email \n')  # 发件的主题内容
sender = 'mengcun111@sina.com'      # 发件人
password = '**********'             # 登录密码
receiver = 'mengcun111@sina.com'    # 收件人


# 发送邮件
def send_email(send_from, send_password, to_receive, content, server):
    content['Subject'] = 'An Email Send By SMTP'
    content['From'] = send_from
    content['To'] = to_receive

    send_srv = SMTP(server)       # 创建一个smtp用于发送对象
    send_srv.login(send_from, send_password)     # 登录操作
    errs = send_srv.send_message(content)
    send_srv.quit()         # 关闭smtp服务器
    assert len(errs) == 0, errs     # assert返回为假就会触发异常
    print('smtp send the email successfully')
    sleep(10)   # 睡眠10秒，等待邮件发送完成，服务器完成消息的发送和接收


# 接收邮件
def receive_email(to_receive, receiver_password, server):
    receive_srv = POP3(server)          # 创建一个pop3用于接收对象
    receive_srv.user(to_receive)         # 设置登录服务器的用户名
    receive_srv.pass_(receiver_password)  # 设置登录服务器的密码
    email_list = receive_srv.stat()     # 获取邮件列表
    response, msg, size = receive_srv.retr(email_list[0])   # 下载邮件列表中的第一个邮件
    receive_srv.quit()      # 关闭POP3服务器
    print(response, msg, size, sep='\n-------------------------\n')
    print('POP3 receive the email successfully')


send_email(sender, password, receiver, message, smtp_srv)
sleep(10)
receive_email(sender, password, pop3_srv)



