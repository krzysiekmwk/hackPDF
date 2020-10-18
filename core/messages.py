import socket

HEADER_LENGTH = 10


def send_message(message, client, send_binary_data=False):
    try:
        if message:
            if not send_binary_data:
                message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client.send(message_header + message)
            return True
    except (ConnectionResetError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError):
        return False


# Handles message receiving
def receive_message(client_socket, get_binary_data=False):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        if get_binary_data:
            received_data = client_socket.recv(message_length)
        else:
            received_data = client_socket.recv(message_length).decode('utf-8').strip()

        return {'header': message_header, 'data': received_data}

    except socket.error:
        # client closed connection violently, or just lost his connection
        return False
