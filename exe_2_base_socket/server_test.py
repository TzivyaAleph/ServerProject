"""EX 2.6 server implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""

import socket
import datetime
import random

NAME = "Tzivya's server"
PORT = 5555

def create_server_rsp(code):
    """Based on the command, create a proper response"""
    method = code.split('/')
    cmd = int(method[0])
    result = ""
    if cmd == 1:
        result = str(int(method[1])+int(method[2]))
    elif cmd == 2:
        result = str(int(method[1])-int(method[2]))
    elif cmd == 3:
        result = str(int(method[1])*int(method[2]))
    elif cmd == 4:
        result = str(int(method[1])/int(method[2]))
    return result

def check_code_number(code):
    method = code.split('/')
    if not len(method) == 3:
        return false,"ERROR"
    else:
        if  method[0] not in [1,2,3,4]:
            return false,"ERROR"
        elif not method[1].isdigit() or not method[2].isdigit() :
            return false, "ERROR"
        if method[0]== 4 and method[2] == 0:
            return false, "ERROR"
        else:
            return True, ""



def check_cmd(request):
    if request:
        request_list = request.split('\r\n')
        method = request_list[0]
        split_method = method.split(' ')
        if split_method[0] == "GET" and split_method[2] == "HTTP/1.1":
            request_url = split_method[1]
        else:
            return False, "ERROR"
    else:
        return False, "ERROR"
    return True, request_url


def main():
    # Create TCP/IP socket object
    my_server = socket.socket()
    # Bind server socket to IP and Port
    my_server.bind(("0.0.0.0", PORT))
    # Listen to incoming connections
    my_server.listen()
    print("Server is up and running")
    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)

def handle_client(client_socket):
        # Get message from socket and check if it is according to protocol
        cmd = my_server.recv(1024).decode()
        valid_msg,code_numbers = check_cmd(cmd)
        if valid_msg:
            # 1. Print received message
            print("The received message: " + code_numbers)
            # 2. Check if the command is valid, use "check_cmd" function
            valid_code, response= check_code_number(code_numbers)
            if valid_code:
                response = create_server_rsp(code_numbers)
                http_header = "HTTP/1.1 200 OK\r\n"
            else:
                http_header = "HTTP/1.1 404 Not Found\r\n"
            # Send response to the client
            http_header += "Content-Length: 1\r\n"
            http_header += "Content-Type: text/html; charset=utf-8\r\n"
            http_header += "\r\n"
            result = (http_header + response).encode()
            client_socket.send(result)
        else:
            print("Closing\n")
            # Close sockets
            client_socket.close()
            my_server.close()




if __name__ == "__main__":
    main()
