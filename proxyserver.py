from socket import *

serverPort = 6790
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print('The proxy server is ready to receive')
while True:
    # await a connection request
    connectionSocket, addr = serverSocket.accept()
    msg = connectionSocket.recv(2048)
    try:
        # first process the msg to get the host name and requested file and file location
        splitMsg = msg.decode().split('\r\n')
        splitUrl = splitMsg[0].split('/')
        hostName = splitUrl[1]
        fileName = splitUrl[len(splitUrl) - 2].split(' ')[0]

        # first check if the file exists in the directory as a cached object
        try:
            html = 'html'
            png = 'png'
            jpg = 'jpg'
            fileType = fileName.split('.')[1]
            if fileType == html:  # if it is requesting a html
                file = open(fileName)
                data = file.read()
                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                for i in range(0, len(data)):
                    connectionSocket.send(data[i].encode())
                    file.close()
            # if the file requested is an image
            elif fileType == png or fileType == jpg:  # if it is requesting a picture
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
                temp = '/favicon.ico'
                if fileName != temp:  # ignore all favicons
                    splitUrl.remove(splitUrl[1])
                    # splitUrl.remove(splitUrl[0])
                    newReq = '/'.join(splitUrl)
                    splitMsg[0] = newReq
                    print(splitMsg)
                    # create the new request
                    newMsg = ('\r\n'.join(splitMsg)).encode()
                    clientSocket = socket(AF_INET, SOCK_STREAM)
                    # get the ip of the host name
                    tempIP = gethostbyname(hostName)
                    # connect to the server
                    clientSocket.connect((tempIP, 80))
                    clientSocket.send(newMsg)
                    # connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                    file = open(fileName, 'w')
                    tempBool = False
                    while True:  # write to file and send the data recieved
                        payload = clientSocket.recv(2048)
                        if not payload:
                            break
                        tempPayload = payload.split()
                        if tempPayload[1] != b'404':
                            tempBool = True
                        if tempBool:
                            writePayload = payload.decode().split('\r\n')
                            writePayload = writePayload[len(writePayload) - 1]
                            file.write(writePayload)
                        connectionSocket.send(payload)
                    tempBool = False
                    clientSocket.close()
                    file.close()
                connectionSocket.close()
            except: # file not found
                print('failed')
                connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
                connectionSocket.close()
    except:
        connectionSocket.close()
