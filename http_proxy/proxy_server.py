# Python 2.7
import socket
import signal
import sys
import threading

# Constants
host_name = "localhost"
bind_port = 6666
bufsize = 1024
connection_timeout = 5


# The server class
class Server:

    def __init__(self):
        signal.signal(signal.SIGINT, self.shutdown)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host_name, bind_port))
        self.serverSocket.listen(6)
        self.clients = {}

    def listenForClients(self):
        print "Listening for clients: "
        while True:
            (clientSocket, client_address) = self.serverSocket.accept()
            c = threading.Thread(name=self._getClientName(client_address), target=self.proxy, args=(clientSocket, client_address))
            c.setDaemon(True)
            c.start()
        self.shutdown()

    def _getClientName(self, cli_addr):
        return cli_addr

    def shutdown(self):
        self.serverSocket.close()
        sys.exit(0)

    def proxy(self, conn, client_addr):
        request = conn.recv(bufsize)
        first_line = request.split('\n')[0]
        url = first_line.split(' ')[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        print "Connect to :", webserver, port

        print "Request is ", first_line, " to URL: ", webserver

        #Search if file is present in cache
        file_to_use = "/" + webserver
        print file_to_use
        try:
            file = open(file_to_use[1:], "r")
            data = file.readlines()
            print "File present in Cache\n"

            for i in range(0, len(data)):
                #print (data[i])
                conn.send(data[i])
            print "Read file from cache\n"

        except IOError:
            print "File does not exist...Fetching from server and creating new file\n"

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(connection_timeout)
                s.connect((webserver, port))
                s.sendall(request)

                fileobj = s.makefile('r', 0)
                fileobj.write("GET " + "http://" + webserver + " HTTP/1.1\n\n")

                buffer = fileobj.readlines()

                tmp = open("./" + webserver, "wb")

                for i in range(0, len(buffer)):
                    tmp.write(buffer[i])
                    conn.send(buffer[i])

                s.close()
                conn.close()
            except socket.error as error_msg:
                print 'Error :', client_addr, error_msg
                if s:
                    s.close()
                if conn:
                    conn.close()

if __name__ == "__main__":
    server = Server()
    server.listenForClients()
