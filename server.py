# !/bin/python3
import socket
import sys
import threading

# Connection Data
host = 'ENTER YOUR IP'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Add this flags to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = {}

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients.keys():
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            # Removing And Closing Clients
            nickname = clients[client]
            clients.pop(client)
            client.close()
            if type(e) == ConnectionResetError:
                print(nickname, 'left the chat!')
                broadcast('{} left!'.format(nickname).encode('utf-8', errors='ignore'))
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8', errors='ignore'))
        nickname = client.recv(1024).decode('utf-8', errors='ignore')
        clients[client] = nickname

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8', errors='ignore'))
        client.send('Connected to server!'.encode('utf-8', errors='ignore'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

try:
    print("Server is listening...")
    receive()
except KeyboardInterrupt:
    print('\nServer stopped.')
    for client in clients.keys():
        client.send('EXIT'.encode('utf-8', errors='ignore'))
        client.close()
    print('\nServer stopped.')
    sys.exit()
