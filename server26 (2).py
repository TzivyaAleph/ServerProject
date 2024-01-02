"""EX 2.6 server implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""

import socket
import protocol
import datetime
import random

NAME = "Tzivya's server"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    result = ""
    if cmd == "TIME":
        result = str(datetime.datetime.now().time())
    elif cmd == "HELLO":
        result = NAME
    elif cmd == "NUMBER":
        result = str(random.randint(0, 99))
    elif cmd == "EXIT":
        result = "BYE BYE!!"
    return result


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g NUMBER, HELLO, TIME, EXIT)"""
    if data in ["TIME", "HELLO", "NUMBER", "EXIT"]:
        return True
    return False


def main():
    # Create TCP/IP socket object
    my_server = socket.socket()
    # Bind server socket to IP and Port
    my_server.bind(("0.0.0.0", protocol.PORT))
    # Listen to incoming connections
    my_server.listen()
    print("Server is up and running")
    # Create client socket for incoming connection
    (client_socket, client_address) = my_server.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print("The received message: " + cmd)
            # 2. Check if the command is valid, use "check_cmd" function
            if check_cmd(cmd):
                response = create_server_rsp(cmd)
            # 3. If valid command - create response
            else:
                response = "Command was not found"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        result = protocol.create_msg(response)
        client_socket.send(str(result).encode())

        # If EXIT command, break from loop
        if create_server_rsp(cmd) == "BYE BYE!!":
            break

    print("Closing\n")
    # Close sockets
    client_socket.close()
    my_server.close()


if __name__ == "__main__":
    main()
