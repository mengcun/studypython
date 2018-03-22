# -*- coding: utf8 -*-
"""
1.等待某个人连接我们的服务器并向我们发送一个HTTP请求
2.解析该请求
3.了解该请求希望请求的内容
4.服务器根据请求抓取需要的数据（从服务器本地文件中读或者程序动态生成）
5.将数据格式化为请求需要的格式
6.送回HTTP响应

1，2，6的操作对所有web应用都是一样的，这部分内容Python标准库中的 BaseHTTPServer 模块可以帮助我们处理。我们只需要关注步骤3～5
"""
import BaseHTTPServer
import sys
import os

#定义异常类
class ServerException(Exception):
    """服务器内部错误"""
    pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    模块的 BaseHTTPRequestHandler 类会帮我们处理对请求的解析，并通过确定请求的方法来调用其对应的函数
    """
    """处理请求并返回页面"""
    #页面模板:第一个/是用来转义？？？？？
    #这里显示客户端的请求信息，相关信息是从RequestHandler的实体变量中得到
    Page = """\
    <html>
        <body>
            <table>
                <tr>  <td>Header</td>         <td>Value</td>          </tr>
                <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
                <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
                <tr>  <td>Client port</td>    <td>{client_port}</td>  </tr>
                <tr>  <td>Command</td>        <td>{command}</td>      </tr>
                <tr>  <td>Path</td>           <td>{path}</td>         </tr>
            </table>
        </body>
    </html>
    """
    Error_Page = """\
    <html>
        <body>
            <h1>Error accessing {path}</h1>
            <p>{msg}</p>
        </body>
    </html>

    """

    #处理一个GET请求
    """
    RequestHandler 继承了 BaseHTTPRequestHandler 并重写了 do_GET 方法
    """
    def do_GET(self):
        try:
            #page = self.create_page()
            #self.send_content(page)
            #文件路径完整
            full_path = os.getcwd() + self.path #os.getcwd 为当前服务器工作路径，self.path为请求信息面里的相对路径
            #如果路径不存在
            if not os.path.exists(full_path):
                #抛出异常
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                #路径是一个文件
                self.handle_file(full_path)
            else:
                #该路径不是一个文件，抛出异常
                raise ServerException("Unknown object '{0}'".format(self.path))
        #处理异常
        except Exception as msg:
            self.handle_error(msg)

    #文件处理函数
    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                #以二进制模式打开文件的，这样读文件的时候就不会对读取的内容做多余的处理
                content = reader.read()
            self.send_content(content)

        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    #定义错误处理函数
    def handle_error(self, msg):
        content = self.Error_Page.format(path = self.path, msg = msg)
        self.send_content(content, 404)

    def send_content(self, source, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html") #告诉了客户端要以处理html文件的方式处理返回的内容
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers() #这里插入一个空白行，根据的是request的结构要求 
        self.wfile.write(source) #将所请求的数据写到客户端响应的输出流

    def create_page(self):
        values = {
            'date_time':self.date_time_string(),
            'client_host':self.client_address[0], #关联的客户端地址
            'client_port':self.client_address[1], #关联的客户端端口
            'command':self.command, #请求类型
            'path':self.path #请求路径
        }
        page = self.Page.format(**values) #format成功
        #若关键字参数使用列表形式，在列表前面加*
        #若关键字参数使用字典形式，在字典前面加**
        return page

#----------------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
