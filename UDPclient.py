import re
import socket


def isInteger(value):
    try:
        int(value)
        return True
    except:
        return False


Input = input('istemci <ServerIp> <ServerPort>: ')
indexes = [i for i, x in enumerate(Input) if x == ' ']

p = re.compile(
    '''^ID=<(1[0-9]{8}){0,1}>,Name=<([a-zA-ZçÇğĞıİöÖüÜşŞ]+){0,1}>,Surname=<([a-zA-ZçÇğĞıİöÖüÜşŞ]+){0,1}>,Mail=<(st1[0-9]{8}@etu.edu.tr){0,1}>$''')

if len(indexes) == 2 and Input[:indexes[0]] == 'istemci' and isInteger(Input[indexes[1] + 1:]):
    serverIp = Input[indexes[0] + 1: indexes[1]]
    serverPort = int(Input[indexes[1] + 1:])
    index = ''
    print('Connection is started')
    while True:
        index = input('Lutfen index numarasi giriniz: ')
        if not isInteger(index) or int(index) < 1 or int(index) > 45:
            print('Input has to lower than 45 bigger than 0!')
        else:
            break

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto((index).encode('utf-8'), (serverIp, serverPort))
        recvSlot, addr = sock.recvfrom(1024)
        recvSlot = recvSlot.decode('utf-8')
        print(recvSlot)
        change = ''
        while True:
            change = input('>>')
            if p.match(change):
                break
            else:
                print('wrong INPUT')
        sock.settimeout(30)
        while True:
            sock.sendto((change).encode('utf-8'), (serverIp, serverPort))
            recvSlot, addr = sock.recvfrom(1024)
            recvSlot = recvSlot.decode('utf-8')
            if recvSlot == '-1':
                print('İslem tamamlandi.')
                sock.close()
    except:
        exit(0)
else:
    print('Wrong input!')
