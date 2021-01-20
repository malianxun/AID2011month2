"""
epoll练习
"""
from select import *
from socket import *

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

def main():
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    sock.setblocking(False)

    ep = epoll()
    ep.register(sock,EPOLLIN)

    map = {
        sock.fileno():sock
    }

    while True:
        events = ep.poll()
        for fd,event in events:
            if fd is sock.fileno():
                connfd,addr = map[fd].accept()
                connfd.setblocking(False)
                ep.register(connfd,EPOLLIN)
                map[connfd.fileno()] = connfd
            else:
                data = map[fd].recv(1024)
                if not data:
                    ep.unregister(fd)
                    map[fd].close()
                    del map[fd]
                    continue
                print(data)
                map[fd].send(b"ok")


if __name__ == '__main__':
    main()
