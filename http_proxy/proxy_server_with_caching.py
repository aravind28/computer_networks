import sys, thread, socket

#Constants
MAX_DATA = 99999

def main():
    host = ''

    if(len(sys.argv) < 2):
        port = 2846
        print "No port is entered so using port ", port
    else:
        port = int(sys.argv[1])

    print "Proxy server is running on host: ", "local host", " on port : ", str(port)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(10)

    except:
        if s:
            s.close()
            print "Proxy server socket is closed for further connections"
            sys.exit(1)

    while 1:
        socket_obj, conn_add = s.accept()
        print "Server is connected to : ", conn_add
        thread.start_new_thread(proxy, (socket_obj, conn_add))

    s.close()

def proxy(conn, client_addr):
    request_from_browser = conn.recv(MAX_DATA)

    first_line = request_from_browser.split('\n')[0]
    url = first_line.split(' ')[1]

    print "Request from web browser is for url: ", url

    http_pos = url.find("://")
    if (http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]

    port_pos = temp.find(":")

    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1
    if (port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = temp[:port_pos]

    file_to_use = "/" + webserver

    try:
        file = open(file_to_use[1:], "r")
        data = file.readlines()
        print "File present in Cache\n"
        print "File to use", temp
        for i in range(0, len(data)):
            # print (data[i])
            conn.send(data[i])
        print "Read file from cache\n"

    except IOError:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            print "File not present in Cache so connecting to web server from proxy"
            s.send(request_from_browser)

            while 1:
                data = s.recv(MAX_DATA)

                if (len(data) > 0):
                    fileobj = s.makefile('r', 0)
                    fileobj.write("GET " + "http://" + webserver + " HTTP/1.1\n\n")

                    buffer = fileobj.readlines()

                    tmp = open("./" + webserver, "wb")

                    for i in range(0, len(buffer)):
                        tmp.write(buffer[i])
                        #conn.send(buffer[i])
                    conn.send(data)
                    print "Data is received from web server, sent to browser and cached in proxy for future use"
                else:
                    break
            s.close()
            conn.close()
        except socket.error, (value, message):
            if s:
                s.close()
            if conn:
                conn.close()
            print "Peer Reset", first_line, client_addr
            sys.exit(1)

if __name__ == '__main__':
    main()

