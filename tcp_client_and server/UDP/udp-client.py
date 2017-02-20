# Python 2.7
import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('Hello world', (host_ip, host_port))
data, addr = s.recvfrom(1024)
print addr, '==>', data
