# C:\Users\tzivy\Desktop\for_the_test\exe_3_multipe_client_socket\client_chat1.py
import socket
import select
import protocol1
import msvcrt

CLIENT_PORT = 3333
CLIENT_IP = "127.0.0.1"

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((CLIENT_IP, CLIENT_PORT))
msg = ""
print("pls enter commands \n")
server_sockets = []
input_ch = ""
while True:
    if msg != "":
        new_msg = protocol1.create_msg(msg)
        my_socket.send(new_msg.encode())
    #rlist- ready to read from them  wlist - ready to write on them
    rlist, wlist, xlist = select.select([my_socket], [my_socket], [])
    for current_socket in rlist:
        if current_socket is my_socket:
            is_valid, data = protocol1.get_msg(current_socket)
            if is_valid:
                if data == "":
                    break
                else:
                    print("\nServer sent: " + data + "\n")
            else:  # there was no digit in the start
                print("ERROR")

    # break when exit
    if msg == "EXIT\r":
        break
    msg = ""

    #for multiple clients that typing at the same time
    # if there is a keyboard hit.
    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8")
        input_ch += key
        print(key, flush=True, end="")
        if key == "\r":  # the key is Enter char.
            msg = input_ch
            input_ch = ""
            print(msg)

my_socket.close()
