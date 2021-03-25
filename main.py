"""
 A simple application that allows people to add comments or write journal entries.
 It can allow comments or not and timestamps for all entries. Could also be made into a shout box.

"""
import socket
import threading
import mongodb


# Connection data
host = '127.0.0.1'
port= 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

# Lists for clients and nicknames
clients = []
nicknames = []

# Sending messages to clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling messages from clients
def handle(client):
    while True:
        try:
            # Broadcasting message
            message = client.recv(1024)
            broadcast(message)

            # Mongodb upload
            index = clients.index(client)
            nickname = nicknames[index]
            others = [nick for nick in nicknames if nick is not nickname]
            # print(others)
            mongodb.write_message(nickname, others if len(nicknames) > 1 else nicknames[0], message.decode('ascii'))

            # [nick for nick in nicknames]

        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving/ Listening function
def receive():
    while True:
        # Accept connection
        client, adress = server.accept()
        print("Connected with {}".format(str(adress)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# def db_entries():
#     while True:
#         client, adress = server.accept()
#
#
# db_entries()
receive()
