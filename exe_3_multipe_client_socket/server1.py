import socket
import select
import protocol1
import re

MAX_MSG_LENGTH = 1024
SERVER_PORT = 3333
SERVER_IP = "0.0.0.0"


def sending_options(data1, clients, my_socket):
    """
    param data1: the message from the client
    param clients: the dictionary with names and sockets of the clients
    param my_socket: the socket that send me the message
    return: the response message and the socket of the client I will send the message.
    """
    if data1[0] == "NAME":
        if not data1[1].isalpha():
            return "the name should include only letters", my_socket
        if my_socket in clients.values():
            return "this client already has a name", my_socket
        if data1[1] in clients.keys():
            return "this name is already exist", my_socket
        else:
            clients[data1[1]] = my_socket
            return "Hello " + data1[1], my_socket
    if data1[0] == "GET_NAMES":
        return " ".join(list(clients.keys())), my_socket
    if data1[0] == "MSG":
        if data1[1] in clients.keys():
            # finds the name of the client that send the message
            val = [i for i in clients if clients[i] == my_socket]
            if val:
                return "".join(val) + " sends " + " ".join(data1[2:]), clients[data1[1]]
            else:
                return "peak a name before sending a message", my_socket
        else:
            return "cant find this client", my_socket
    if data1[0] == "EXIT":
        return "", my_socket


def check_data(data2):
    """
    param data2: the message from the client
    return: TRUE if the client message is a valid one
    """
    if data2[0] in ["NAME", "MSG", "GET_NAMES", "EXIT","NSLOOKUP"]:
        if data2[0] == "NAME" and len(data2) != 2:
            return False
        elif data2[0] == "MSG" and len(data2) < 3:
            return False
        elif data2[0] == "NSLOOKUP" and len(data2) != 2:
            return False
        else:
            return True
    return False


def print_client_sockets(clients_sockets):
    """
    param clients_sockets: the list of clients sockets
    prints the clients that connected to the server
    """
    for c in clients_sockets:
        print("\t", c.getpeername())


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
messages_to_send = []

my_clients = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            is_valid, data = protocol1.get_msg(current_socket)
            if is_valid:
                if data == "EXIT\r":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    # finds the client of the corresponding socket
                    value = "".join([i for i in my_clients if my_clients[i] == current_socket])
                    if value != "":
                        my_clients.pop(value)
                else:
                    list_data = data.split()
                    if check_data(list_data):
                        data, socket = sending_options(list_data, my_clients, current_socket)
                    else:
                        data = "invalid message"
                        socket = current_socket

                    messages_to_send.append((socket, data))
            else:
                response = "Wrong protocol"
                messages_to_send.append((current_socket, response))

    # send the messages to the correct sockets
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in wlist:
            response = protocol1.create_msg(data)
            current_socket.send(response.encode())
            messages_to_send.remove(message)

