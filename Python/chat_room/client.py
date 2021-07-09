import socket
import threading

serverIP = input("Enter Server IP: ")
port = int(input("Enter Port Number: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = input ("Enter a name: ")

run = True

def getMsg():
    try:
        while True:
            global run
            if run != True:
                break
            message = server.recv(2048)
            print (message.decode('utf-8'))
    except Exception as e:
        print('Host disconnected')
        run = False


def sendMsg():
    try:
        while True:
            try:
                message = input()
            except EOFError:
                print("Exiting...")
                global run
                run = False
                break
            else:
                message = name + ": " + message
                server.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print(2)



try:
    server.connect ((serverIP, port))
except Exception as e:
    print(e)
else:
    while run:
        try:
            recvThread = threading.Thread(target=getMsg)
            sendThread = threading.Thread(target=sendMsg)
        except:
            break
        else:
            recvThread.daemon = True
            sendThread.daemon = True
            try:
                sendThread.start()
                recvThread.start()
            except:
                pass
            else:
                try:
                    sendThread.join()
                except:
                    pass
                else:
                    recvThread.join()
