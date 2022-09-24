from socket import *

serverPort = 6790
serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print ('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    msg = connectionSocket.recv(2048)
    try:
        splitMsg = msg.decode().split('\r\n')
        # print(splitMsg)
        splitUrl = splitMsg[0].split('/')
        # print(splitUrl)
        hostName = splitUrl[1]
        fileName = splitUrl[len(splitUrl)-2].split(' ')[0]

        # first check if the file exists in the directory as a cached object
        try:
            html = 'html'
            png = 'png'
            jpg = 'jpg'
            fileType = fileName.split('.')[1]
            if fileType == html:
                file = open(fileName)
                data = file.read()
                # connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                # connectionSocket.send('Content-Type: text/html\r\n')
                for i in range(0, len(data)):
                    connectionSocket.send(data[i].encode())
                    file.close()
            # if the file requested is an image
            elif fileType == png or fileType == jpg:
                file = open(fileName, 'r+b')
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
        except:
            # if not then try to get it from the original server
            try:
                # tempMsg = splitMsg[1]
                temp = '/favicon.ico'
                if fileName != temp:
                    splitUrl.remove(splitUrl[1])
                    newReq = '/'.join(splitUrl)
                    splitMsg[0] = newReq
                    newMsg = ('\r\n'.join(splitMsg)).encode()
                    clientSocket = socket(AF_INET, SOCK_STREAM)
                    # tempMsg =
                    tempIP = gethostbyname(hostName)

                    clientSocket.connect((tempIP, 80))
                    clientSocket.send(newMsg)
                    connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                    file = open(fileName, 'w')
                    tempBool = False
                    while True:
                        payload = clientSocket.recv(2048)
                        if not payload:
                            break
                        tempPayload = payload.split()
                        if tempPayload[1] != b'404':
                            tempBool = True

                        if tempBool:
                            file.write(payload.decode())
                        connectionSocket.send(payload)
                    tempBool = False
                    clientSocket.close()
                    file.close()
                connectionSocket.close()
            except:
                print('failed')
                connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
                connectionSocket.close()
    except:
        connectionSocket.close()