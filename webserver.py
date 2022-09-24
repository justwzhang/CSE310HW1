from socket import *

serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    # print("got connection")
    msg = connectionSocket.recv(2048).decode()
    # print(msg)
    try:
        # print(type(msg))
        msg = msg.split()[1]
        temp = b'/favicon.ico'

        html = 'html'
        png = 'png'
        jpg = 'jpg'

        if msg != temp:
            fileType = msg.split('.')[1]
            # if the file requested is a html
            if fileType == html:
                file = open(msg[1:])
                data = file.read()
                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                # connectionSocket.send('Content-Type: text/html\r\n')
                for i in range(0, len(data)):
                    connectionSocket.send(data[i].encode())
                    file.close()
            # if the file requested is an image
            elif fileType == png or fileType == jpg:
                file = open(msg[1:], 'r+b')
                imageData = file.read()
                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                if fileType == png:
                    connectionSocket.send('Content-Type: image/png\r\n'.encode())
                else:
                    connectionSocket.send('Content-Type: image/jpg\r\n'.encode())
                tempString = bytes('Content-Length: %s\r\n' % len(imageData), 'utf8')
                connectionSocket.send(tempString)
                connectionSocket.send('\r\n'.encode())
                connectionSocket.send(imageData)
                file.close()
            else:
                connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
        connectionSocket.close()
    except:
        print('failed')
        connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
        connectionSocket.close()
