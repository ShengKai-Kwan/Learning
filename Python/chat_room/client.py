import socket
import threading
#from _thread import *
import sys

serverIP = input("Enter Server IP: ")
port = int(input("Enter Port Number: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = input ("Enter a name: ")
def getMsg():
    try:
        while True:
            message = server.recv (2048)
            print (message.decode('utf-8'))
    except KeyboardInterrupt:
        pass


def sendMsg():
    while True:
        try:
            message = sys.stdin.readline()
        except Exception as e:
            print(e)
            pass
        else:
            message = name + ": " + message
            server.send(message.encode('utf-8'))



try:
    server.connect ((serverIP, port))
except Exception as e:
    print (e)
else:
    while True:
        recvThread = threading.Thread(target=getMsg)
        sendThread = threading.Thread(target=sendMsg)
        try:
            recvThread.start()
            sendThread.start ()
        except Exception as e:
            print(e)
            break
        else:
            recvThread.join()
            sendThread.join()
        '''
        for _ in range(50):
            start_new_thread(getMsg, ())
            start_new_thread(sendMsg, ())
        '''

    server.close()


