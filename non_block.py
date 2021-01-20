"""
设置非阻塞的套接字
"""

from socket import *
from time import *

#创建tcp套接字
sock = socket()
sock.bind(("127.0.0.1",8888))
sock.listen(5)

file = open("my.log","a")

#设置为非阻塞
# sock.setblocking(False)
#设置超时事件
sock.settimeout(3)

#循环处理客户端连接
while True:
    try:
        connfd,addr = sock.accept()
        print("Connect from",addr)
    except timeout as e:
        #模拟一个与accept无关的事件
        msg = "%s:%s\n"%(ctime(),e)
        file.write(msg)
    except BlockingIOError as e:
        #模拟一个与accept无关的事件
        msg = "%s:%s\n"%(ctime(),e)
        file.write(msg)
        sleep(2)
    else:
        #accept正常执行
        data = connfd.recv(1024)
        print(data.decode())