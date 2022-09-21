from socket import *

serverPort = 6790
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
print ('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    msg = connectionSocket.recv(2048)

    try:
        tempMsg = msg.split()[1]
        temp = b'/favicon.ico'
        if tempMsg != temp:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect(('127.0.0.1', 6789))
            clientSocket.send(msg)
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            while True:
                payload = clientSocket.recv(2048)
                if not payload:
                    break
                connectionSocket.send(payload)
            clientSocket.close()
        connectionSocket.close()
    except:
        print('failed')
        connectionSocket.send('HTTP/1.1 404 File not found\r\n'.encode())
        connectionSocket.close()