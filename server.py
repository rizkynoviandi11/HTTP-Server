import socket
import sys
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

if len(sys.argv) > 1:
    HOST, PORT = 'localhost', int(sys.argv[1])
else:
    sys.exit("Please specify the port")

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print 'Serving HTTP on port %s ...' % PORT

while True:
    client_connection, client_address = listen_socket.accept()
    request = HTTPRequest(client_connection.recv(1024))
    ver = request.request_version
    response, fileRequest, contentType, contentLength = ''

    if ver != 'HTTP/1.1' or ver != 'HTTP/1.0':
        response = ver + '400 Bad Request \n\r'

    elif request.command != 'GET' or request.command != 'POST':
        response = ver + '501 Not Implemented \n\r'

    if request.command == 'GET':
        if request.path == '/':
            response = ver + '302 Found \n\r'

        elif request.path == '/style':
            fileRequest = 'style.css'
            f = open(fileRequest, 'r')
            files = f.read()
            contentType = 'Content-Type: style/css \n\r'

        elif request.path == '/background':
            fileRequest = 'background.jpg'
            contentType =

        elif request.path == '/hello-world':

        else:

    else:



    #http_response = """\
#HTTP/1.1 200 OK

#Hello, World!
#"""
    #client_connection.sendall(http_response)
    client_connection.close()
