from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from manage import app  # Flask程序，把它导入进来
# 监听5000，相当于把5000转到5000，但有优化，部署时再用

http_server = HTTPServer(WSGIContainer(app))

# http_server.bind(5000, "0.0.0.0")  # 设置对外开启访问，端口设置为5000
# http_server.start(1)
http_server.listen(5000)  # 也可以设置值进行本地访问，也就是监听本地的端口
IOLoop.instance().start()
