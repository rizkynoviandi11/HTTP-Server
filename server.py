import socket
import sys
import string
import random
import time
import hashlib
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
    req = client_connection.recv(1024)
    req_content = req.split('\n')
    request = HTTPRequest(req)
    command = request.command
    httpVersion = request.request_version
    response, contentType, contentLength, files, etag = '', '', '', '', ''

    if httpVersion != 'HTTP/1.1' and httpVersion != 'HTTP/1.0':
        response = httpVersion + ' 400 Bad Request \r\n'
        contentType = 'Content-Type: text/plain \r\n'
        contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'

    elif command != 'GET' and command != 'POST':
        response = httpVersion + ' 501 Not Implemented \r\n'
        contentType = 'Content-Type: text/plain \r\n'
        contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'

    else:
        if request.command == 'GET':
            if request.path == '/':
                response = httpVersion + ' 302 Found \r\nLocation: \hello-world\r\n'
                contentType = 'Content-Type: text/plain \r\n'
                contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
            elif request.path == '/style':
                fileRequest = 'style.css'
                f = open(fileRequest, 'rb')
                files = f.read()
                encryptedFile = hashlib.sha256(files).hexdigest()
                if 'if-none-match' in request.headers.keys() and encryptedFile == request.headers['If-None-Match']:
                    response = httpVersion + ' 304 Not Modified\r\n'
                    contentType = 'Content-Type: text/plain \r\n'
                    contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
                else:
                    response = httpVersion + ' 200 OK \r\n'
                    etag = 'ETag: ' + str(encryptedFile) + '\r\n'
                    contentType = 'Content-Type: text/css \r\n'
                    contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                f.close()
            elif request.path == '/background':
                response = httpVersion + ' 200 OK \r\n'
                fileRequest = 'background.jpg'
                f = open(fileRequest, 'rb')
                files = f.read()
                encryptedFile = hashlib.sha256(files).hexdigest()
                if 'if-none-match' in request.headers.keys() and encryptedFile == request.headers['If-None-Match']:
                    response = httpVersion + ' 304 Not Modified\r\n'
                    contentType = 'Content-Type: text/plain \r\n'
                    contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
                else:
                    response = httpVersion + ' 200 OK \r\n'
                    etag = 'ETag: ' + str(encryptedFile) + '\r\n'
                    contentType = 'Content-Type: image/jpg \r\n'
                    contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                f.close()
            elif request.path == '/hello-world':
                response = httpVersion + ' 200 OK \r\n'
                fileRequest = 'hello-world.html'
                f = open(fileRequest, 'rb')
                files_old = f.read()
                files = string.replace(files_old, '__HELLO__', 'World')
                contentType = 'Content-Type: text/html \r\n'
                contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                f.close()
            elif request.path.split('?')[0] == '/info':
                if request.path.split('?')[1].split('=')[1] == 'time':
                    response = httpVersion + ' 200 OK \r\n'
                    files = time.ctime()
                    contentType = 'Content-Type: text/html \r\n'
                    contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                elif request.path.split('?')[1].split('=')[1] == 'random':
                    response = httpVersion + ' 200 OK \r\n'
                    files = str(random.randint(0, 100000000000000000))
                    contentType = 'Content-Type: text/html \r\n'
                    contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                else:
                    files = 'No Data'
                    contentType = 'Content-Type: text/plain \r\n'
                    contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
            else:
                response = httpVersion + ' 404 Not Found  \r\n'
                contentType = 'Content-Type: text/plain \r\n'
                contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'

        elif request.command == 'POST':
            if request.path == '/':
                response = httpVersion + ' 302 Found \r\nLocation: \hello-world\r\n'
                contentType = 'Content-Type: text/plain \r\n'
                contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
            elif 'content-type' in request.headers.keys() and request.headers['content-type'] == 'application/x-www-form-urlencoded' and len(req_content) > 0:
                response = httpVersion + ' 200 OK \r\n'
                fileRequest = 'hello-world.html'
                f = open(fileRequest, 'rb')
                files_old = f.read()
                files = string.replace(files_old, '__HELLO__', (req_content[len(req_content) - 1].split('=')[1]).replace('+', ' '))
                contentType = 'Content-Type: text/html \r\n'
                contentLength = 'Content-Length: ' + str(len(files)) + '\r\n\r\n'
                f.close()
            else:
                response = httpVersion + ' 400 Bad Request \r\n'
                contentType = 'Content-Type: text/plain \r\n'
                contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
        else:
            response = httpVersion + ' 404 Not Found  \r\n'
            contentType = 'Content-Type: text/plain \r\n'
            contentLength = 'Content-Length: ' + str(len(response)) + '\r\n\r\n'
    http_response = response + "Connection: close\r\n" + etag + contentType + contentLength + files
    client_connection.send(http_response)
    client_connection.close()
