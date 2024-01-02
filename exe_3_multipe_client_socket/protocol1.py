LENGTH_FIELD_SIZE = 2
PORT = 9999


def create_msg(data):
    """
    param data: the data that you about to send
    return: the data + the length of the data
    """
    length = str(len(data))
    zfill_length = length.zfill(LENGTH_FIELD_SIZE)
    message = zfill_length + data
    return str(message)


def get_msg(my_socket):
    """
    param my_socket: the socket that will receive the data
    return: the data that have been  sent
    """
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length.isdigit():
        return False, "Error"
    data = my_socket.recv(int(length)).decode()
    return True, str(data)
