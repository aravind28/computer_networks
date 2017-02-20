# Python 2.7
import socket

# Get host name, IP address, and port number
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

# Make a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number
s.bind((host_ip, host_port))

# Allow 5 pending connects
s.listen(5)

print 'Server started. Waiting for connection...'

# Listen until process is killed
bufsize = 1024
while True:
  # Wait for next client connect
  conn, addr = s.accept()
  print 'Server connected by ', addr

  # Read next line on client socket. Send a reply line to the client
  while True:
    data = conn.recv(bufsize)
    if not data: break
    print 'Server received: ', repr(data)
    conn.sendall('Echo => ' + data)

  # Close TCP connection
  conn.close()
