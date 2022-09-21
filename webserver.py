from socket import *

serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    # print("got connection")
    msg = connectionSocket.recv(2048).decode()
    # print(msg)
    try:
        # print(type(msg))
        msg = msg.split()[1]
        temp = '/favicon.ico'

        html = 'html'
        png = 'png'
        jpg = 'jpg'

        if msg != temp:
            fileType = msg.split('.')[1]
            if fileType == html:
                file = open(msg[1:])
                data = file.read()
                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                for i in range(0, len(data)):
                    connectionSocket.send(data[i].encode())
                    file.close()
            else:
                file = open(msg[1:], 'rb')
                connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
                imageData = file.read(2048)
                while imageData:
                    connectionSocket.send(imageData)
                    imageData = file.read(2048)
                file.close()

        connectionSocket.close()
    except :
        print('failed')
        connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
        connectionSocket.close()