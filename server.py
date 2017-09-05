import socket
import sys
import string
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

if len(sys.argv) > 1:
    HOST, PORT = '', int(sys.argv[1])
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
    command = request.command
    var = request.request_version
    response, contentType, contentLength, files = '', '', '', ''

    if var != 'HTTP/1.1' and var != 'HTTP/1.0':
        response = var + ' 400 Bad Request \r\n'

    elif command != 'GET' and command != 'POST':
        response = var + ' 501 Not Implemented \r\n'

    else:

        if request.command == 'GET':
            if request.path == '/':
                response = var + ' 302 Found \r\nLocation: \hello-world'
            elif request.path == '/style':
                response = var + ' 200 OK \r\n'
                fileRequest = 'style.css'
                f = open(fileRequest, 'rb')
                files = f.read()
                contentType = 'Content-Type: text/css \r\n\r\n'
                f.close()
            elif request.path == '/background':
                response = var + ' 200 OK \r\n'
                fileRequest = 'background.jpg'
                f = open(fileRequest, 'rb')
                files = f.read()
                contentType = 'Content-Type: image/jpg \r\n\r\n'
                f.close()
            elif request.path == '/hello-world':
                response = var + ' 200 OK \r\n'
                fileRequest = 'hello-world.html'
                f = open(fileRequest, 'rb')
                files_old = f.read()
                files = string.replace(files_old, '__HELLO__', 'World')
                contentType = 'Content-Type: text/html \r\n\r\n'
                f.close()

        elif request.command == 'POST':
            if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
                fileRequest = 'hello-world.html'
                f = open(fileRequest, 'rb')
                files_old = f.read()
                files.replace(files_old, '__HELLO__', )
                contentType = 'Content-Type: text/html \r\n'
                f.close()
            else:
                response = var + ' 400 Bad Request \r\n'

        else:
            response = var + ' 404 Not Found  \r\n'

    http_response = response + contentType + files
    client_connection.send(http_response)
    print 'Connection: close'
    client_connection.close()