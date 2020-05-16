import socket
from _thread import *

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = socket.gethostbyname(socket.gethostname())
port = 9000
serverSock.bind((host_ip, port))
serverSock.listen(10) #listens for 10 connections
print("Server IP: " + host_ip + " Port: " + str(port))

clients = []

def clientThread(clientSock, client_ip):
    try:
        clientSock.send("Welcome to the Chat Room!".encode('utf-8'))
    except ConnectionAbortedError:
        print(client_ip[0] + " Disconnected!")
    else:
        while True:
            try:
                message = clientSock.recv(2048)
                if message:
                    msg_to_send = "<" + client_ip[0] + "> " + message.decode('utf-8')
                    print(msg_to_send)  #print the message of the user who just sent to the server

                    for client in clients: #broadcast the message
                        if client != clientSock: #don't send the message to the sender
                            try:
                                client.send(msg_to_send.encode('utf-8'))
                            except: #if error occurs, probably connection between user and server broken. close the connection and remove user from the Clients list
                                client.close()
                                if client in clients:
                                    clients.remove(client)
            except:
                continue



while True:
    try:
        clientSock, client_ip = serverSock.accept()
    except Exception as e:
        print(e)
    else:
        clients.append(clientSock)
        print("received connection from " + str(client_ip))

        start_new_thread(clientThread,(clientSock, client_ip))
