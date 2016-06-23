import socket


def isInteger(value):
    try:
        int(value)
        return True
    except:
        return False

Input = input('istemci <ServerIp> <ServerPort>: ')
#Input = 'istemci 10.2.37.23 9988'
indexes = [i for i, x in enumerate(Input) if x == ' ']

if len(indexes) == 2 and Input[:indexes[0]] == 'istemci' and isInteger(Input[indexes[1] + 1:]):
    serverIp = Input[indexes[0] + 1: indexes[1]]
    serverPort = Input[indexes[1] + 1:]
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverIp, int(serverPort)))
    except:
        print("Ip or Port is Wrong. Cannot Connect to Server")
    print('Connection is started')

    index = input('Lutfen index numarasi giriniz: ')
    serverSocket.send((index).encode('utf-8'))
    recv = (serverSocket.recv(1024)).decode("utf-8")
    print(recv)
    change = input('>>')
    serverSocket.send((change).encode('utf-8'))
    serverSocket.close
else:
    print('Wrong input!')
