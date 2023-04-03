import socket
import threading
import

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        print("Receive function is running to the server")
        client, address = server.accept()
        print(f"Connected to {address}")
        name ="Nick"
        client.send(name.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client {nickname}")
        broadcast(f"{nickname} has been joined the chat room".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("Server is listening....")
receive()