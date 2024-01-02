# Ex 4.4 - HTTP Server Shell
# Author: Barak Goner
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
import furl

# TO DO: set constants
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 100
SIZE_OF_PACKET = 1024
DEFAULT_URL = r'C:\Networks\work\webroot\index.html'
PATH_START = r'C:\Networks\work\webroot'
PATH_FAVICON = r'C:\Networks\work\webroot\imgs'
REDIRECTION_DICTIONARY = {r"/secure_index.html": r'C:\Networks\work\webroot\index.html',
                          r"/move_index.html": r'C:\Networks\work\webroot\index.html'}
FIXED_RESPONSE = ""


def get_file_data(filename):
    """ Get data from file """
    # windows use "\" but the internet uses "/"
    filename.replace(r'/', "\\")
    my_file = open(filename, "rb")
    response = my_file.read()
    my_file.close()
    return response


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response

    # prints URL
    print(resource)
    # checks if he wants the whole page
    if resource == '/':
        url = DEFAULT_URL
    elif resource == "/favicon.ico":
        url = PATH_FAVICON + resource
    elif resource.startswith("/calculate-area"):
        url = DEFAULT_URL
    else:
        url = PATH_START + resource

    if os.path.isfile(url):
        http_header = "HTTP/1.1 200 OK\r\n"

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    elif resource in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
        http_header = "HTTP/1.1 302 Moved Permanently\r\n"
        print("302 Moved Permanently\n")
        client_socket.send(http_header.encode())
        url = REDIRECTION_DICTIONARY[resource]
    else:
        http_header = "HTTP/1.1 404 Not Found\r\n".encode()
        print("404 Not Found\n")
        client_socket.send(http_header)
        return

    # TO DO: extract requested file type from URL (html, jpg etc)
    filetype = url.split('.')[-1]
    if filetype == 'html' or filetype == "txt":
        http_header += 'Content Type: text/html; charset=utf-8\r\n'
    elif filetype == 'jpg':
        http_header += 'Content Type: image/jpeg\r\n'
    elif filetype == "js":
        http_header += 'Content Type: text/javascript; charset=UTF-8\r\n'
    elif filetype == "css":
        http_header += 'Content Type: text/css\r\n'
    elif filetype == '.ico':
        http_header += 'Content Type: image/x-icon\r\n'
    elif filetype == '.gif':
        http_header += 'Content Type: image/gif\r\n'
    http_header += "\r\n"
    http_header = http_header.encode()

    # calculates the parameters he got for the area
    if resource.startswith("/calculate-area"):
        r = furl(resource)
        height = r.args['height']
        width = r.args['width']
        # checks if the parameters are positive numbers
        if height.isnumeric() and float(height) > 0 and width.isnumeric() and float(width) > 0:
            area = (float(width) * float(height)) / 2
        else:
            area = "ERROR"
        http_response = http_header + str(area).encode()
    else:
        # TO DO: read the data from the file
        data = get_file_data(url)
        http_response = http_header + data
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
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


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    client_socket.send(FIXED_RESPONSE.encode())

    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(SIZE_OF_PACKET).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
