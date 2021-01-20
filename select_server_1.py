"""
基于select 方法的io 多路复用网络并发
重点代码 ！！
"""
from socket import *
from select import select

# 地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

# 定义监控IO列表
rlist = []
wlist = []
xlist = []


# 创建套接字
def create_socket():
    # tcp套接字 连接客户端
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d" % PORT)
    # 防止IO处理过程中产生阻塞行为
    sock.setblocking(False)
    return sock


# 处理写就绪
def write_manager(ws=[]):
    for w in ws:
        w.send(b"OK")
        wlist.remove(w)  # 否则一直让你发送


# 连接客户端
def connect_client(r):
    connfd, addr = r.accept()
    print("Connect from", addr)
    # 将客户端套接字添加到监控列表
    connfd.setblocking(False)
    rlist.append(connfd)


# 具体处理客户端请求，与客户端交互
def handle_client(r):
    # 连接套接字就绪
    data = r.recv(1024).decode()
    # 客户端退出
    if not data:
        rlist.remove(r)  # 不再监控
        r.close()
        return
    print(data)
    # r.send(b"OK")
    wlist.append(r)  # 加入写关注


# 处理读就绪
def read_manager(rs=[]):
    # 逐个取值，分情况讨论
    for r in rs:
        if r is rlist[0]:
            connect_client(r)
        else:
            handle_client(r)


# 入口函数
def main():
    sock = create_socket()
    rlist.append(sock)  # 初始监控
    # 循环接收客户端连接
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        read_manager(rs) # 处理读操作
        write_manager(ws) #　处理写操作


if __name__ == '__main__':
    main()
