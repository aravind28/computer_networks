import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 8181))
s.settimeout(0.5)
print "Server listening on: ", 8181
t = {}
t[2] = (0, 0)
t[4] = (0, 8)
t[5] = (0, 10)

print t
# while True:
try:
    data, addr = s.recvfrom(1024)
    print "Received message is:", pickle.loads(data)
except socket.timeout:
    print "exception"
