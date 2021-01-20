"""
select 复习
"""
from socket import *
from select import select

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

def main():
    #创建套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    sock.setblocking(False)

    #设置监控的IO
    rlist = [sock]
    wlist = []
    xlist = []

    #循环接收客户端连接
    while True:
        rs,ws,xs = select(rlist,wlist,xlist)

        for r in rs:
            if r is sock:
                conffd,addr = r.accept()
                conffd.setblocking(False)
                print("Connect from",addr)
                rlist.append(conffd)
            else:
                data = r.recv(1024).decode()
                if not data:
                    rlist.remove(r)
                    r.close()
                    continue
                print(data)
                # r.send(b"ok")
                wlist.append(r)
        for w in ws:
            w.send(b"ok")
            wlist.remove(w)


if __name__ == '__main__':
    main()
