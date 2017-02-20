# Python 2.7
import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host_ip, host_port))

print 'Server started. Waiting for connection...'
while True:
  data, addr = s.recvfrom(5)
  print addr, '==>', data
  s.sendto(data, addr)
