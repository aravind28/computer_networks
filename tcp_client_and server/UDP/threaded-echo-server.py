# Python 2.7
import socket
import thread
import time

# Get host name, IP address, and port number
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

# Make a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number
s.bind((host_ip, host_port))

# Listen allow 5 pending connects
s.listen(5)

# Current time on the server
def now():
  return time.ctime(time.time())

bufsize = 1024
def handler(conn):
  while True:
    data = conn.recv(bufsize)
    if not data: break
    print 'Server received: ', repr(data)
    conn.sendall('Echo ==> ' + data)
    time.sleep(10)  # simulating long running program
  conn.close()


while True:
  conn, addr = s.accept()
  print 'Server connected by', addr,
  print 'at', now()
  thread.start_new(handler, (conn,))
