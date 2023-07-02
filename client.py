import socket
import sys
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Read file with IP-address
with open('address', 'r') as addr:
    address = eval(addr.read())

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8', errors='ignore')
            if message == 'NICK':
                client.send(nickname.encode('utf-8', errors='ignore'))
            elif message == 'EXIT':
                client.close()
                print('Server stopped.')
                sys.exit()
            else:
                print(message)
        except ConnectionAbortedError as e:
            # Close Connection When Error
            print('You left the chat.')
            client.close()
            sys.exit()

# Sending message to Server
def write():
    while True:
        try:
            message = f'{nickname}: {input()}'
            client.send(message.encode('utf-8', errors='ignore'))
        except (EOFError, OSError):
            client.close()
            break


# Starting Threads For Listening And Writing
write_thread = threading.Thread(target=write)
write_thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()
try:
    treads = [write_thread, receive_thread]
    for t in treads:
        t.join()
except KeyboardInterrupt:
    pass
