import socket
import threading

HOST='127.0.0.1'
PORT=5555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients=[]

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        client,address=server.accept()
        print("Connected:",address)

        clients.append(client)

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server Running...")
receive()