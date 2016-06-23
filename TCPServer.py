import socket
from time import strftime


def isInteger(value):
    try:
        int(value)
        return True
    except:
        return False


with open('nameListSorted.txt', encoding='utf-8') as f:
    lines = f.readlines()
f.close()
nameList = []
idList = []
mailList = []
for line in lines:
    indexes = [i for i, x in enumerate(line) if x == ' ']
    idList.append(line[:indexes[0]])
    nameList.append(line[indexes[0] + 1:line.index('Bilgisayar')])
    mailList.append(line[indexes[len(indexes) - 1] + 1:])

serverPort = input('sunucu <ServerPort> : ')
# serverPort = 'sunucu 9988'
if serverPort.count(' ') == 1 and serverPort[:serverPort.index(' ')] == 'sunucu' and isInteger(
        serverPort[serverPort.index(' ') + 1:]):

    serverPort = serverPort[serverPort.index(' ') + 1:]

    serverIp = socket.getaddrinfo(socket.gethostname(), serverPort, 0, 0, socket.SOL_TCP)[1][4][0]
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind((serverIp, int(serverPort)))
        print("Socket Created -> IP:", serverIp, "  Port:", serverPort)
    except:
        print("Error In Connection..")
        exit(0)
    serverSocket.listen(10)

    while True:
        c, addr = serverSocket.accept()
        print('Connection Accepted -> Ip:', addr[0], '  Port:', addr[1], '  Time:', strftime("%Y-%m-%d %H:%M:%S"))
        try:
            recvSlot = (c.recv(1024)).decode("utf-8")
            if isInteger(recvSlot):
                recvSlot = int(recvSlot) - 1
                if recvSlot < 44 and recvSlot >= 0:
                    c.send(
                        ('StudenID: ' + idList[recvSlot] + '  StudentName: ' + nameList[recvSlot] + '  StudentMail: ' +
                         mailList[recvSlot] +
                         'Herhangi bir degisiklik icin lutfen "ID=<>,Name=<>,Mail=<>" formatinda giris yapiniz.').encode(
                            'utf-8'))
                    try:
                        c.settimeout(30)
                        recv = (c.recv(1024)).decode("utf-8")
                        if recv != None:
                            print(recv)
                            recvParser = [i for i, x in enumerate(recv) if x == ',']
                            id = recv[recv.index('ID=<') + 4:recvParser[0] - 1]
                            name = recv[recv.index('Name=<') + 6:recvParser[1] - 1]
                            mail = recv[recv.index('Mail=<') + 6:-1]
                            if id != '':
                                idList[recvSlot] = id
                            if name != '':
                                nameList[recvSlot] = name
                            if mail != '':
                                mailList[recvSlot] = mail
                            with open("output.txt", "wt", encoding='utf-8') as out_file:
                                for index in range(44):
                                    out_file.writelines(
                                        nameList[index] + '  ' + idList[index] + '  ' + mailList[index] + '\r\n')
                            print('File Printed.')
                    except:
                        print('Connection Timeout or Error in Input-> Socket Closed-> Ip:', addr[0], '  Port:',
                              addr[1], '  Time:',
                              strftime("%Y-%m-%d %H:%M:%S"))
                        continue

                else:
                    c.send(('Input has to lower than 45 bigger than 0!').encode('utf-8'))
                    c.close()
                    continue
            else:
                print('Wrong Input -> ', addr[0])
                c.send(('Wrong Input!').encode('utf-8'))
                c.close()
                continue
        except:
            continue
else:
    print('Wrong Input!')
