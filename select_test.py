
from select import select
from socket import *

#创建几个IO对象
tcp_sock = socket()
tcp_sock.bind(("0.0.0.0",8888))
tcp_sock.listen(5)

file = open("my.log","r+")

udp_sock = socket(AF_INET,SOCK_DGRAM)

print("开始监控IO")
# rs, ws, xs=select([tcp_sock],[],[])
rs, ws, xs=select([file,udp_sock],[file,udp_sock],[])
print("rlist:",rs)
print("wlist:",ws)
print("xlist:",xs)


