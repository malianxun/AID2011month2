"""
基于select 方法的io 多路复用网络并发
重点代码！！
"""
from select import select
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

    # 设置要监控的IO
    rlist = [sock]
    wlist = []
    xlist = []
    # 循环接收客户端连接
    while True:
        rs,ws,xs = select(rlist,wlist,xlist)
        #逐个取值，分情况讨论
        for r in rs:
            if r is sock:
                conffd,addr = r.accept()
                conffd.setblocking(False)
                print("Connect from",addr)
                #将客户端套接字添加到监控列表
                rlist.append(conffd)
            else:
                #连接套接字就绪
                data = r.recv(1024).decode()
                #客户端退出
                if not data:
                    rlist.remove(r) #不再监控
                    r.close()
                    continue
                print(data)
                # r.send(b"ok")
                wlist.append(r) #加入写列表
        for w in ws:
            w.send(b"ok")
            wlist.remove(w)


if __name__ == '__main__':
    main()
