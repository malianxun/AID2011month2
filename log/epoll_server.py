"""
基于epoll 方法的io 多路复用网络并发
重点代码！！
"""
from select import *
from socket import *

# 地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

def main():
    # tcp套接字 连接客户端
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d" % PORT)

    #防止IO处理过程中产生阻塞行为
    sock.setblocking(False)

    # 创建epoll对象
    ep = epoll()
    # 关注IO对象
    ep.register(sock, EPOLLIN)
    # 建立查找字典
    map = {
        sock.fileno(): sock,
    }
    # 循环接收客户端连接
    while True:
        print("开始监控IO")
        events = ep.poll()
        #逐个取值，分情况讨论
        for fd,event in events:
            if fd is sock.fileno():
                conffd,addr = map[fd].accept()
                conffd.setblocking(False)
                print("Connect from",addr)
                #将客户端套接字添加到监控列表
                ep.register(conffd, EPOLLIN)
                map[conffd.fileno()] = conffd
            else:
                #连接套接字就绪
                data = map[fd].recv(1024).decode()
                #客户端退出
                if not data:
                    # 不再关注
                    ep.unregister(map[fd])
                    map[fd].close()
                    del map[fd]
                    continue
                print(data)
                map[fd].send(b"ok")


if __name__ == '__main__':
    main()
