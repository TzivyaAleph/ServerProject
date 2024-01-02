"""EX 2.6 client implementation
   Author:
   Date:
   Possible client commands defined in protocol.py
"""

import socket
PORT = 5555

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", PORT))

    while True:
        user_input = input("Enter command\n")
        # 2. Send it to the server
        my_socket.send(user_input.encode())
        # 3. Get server's response
        data = my_socket.recv(1024).decode()
        # 4. If server's response is valid, print it
        if data:
            print("The server response is: " + data)
        else:
            break

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
