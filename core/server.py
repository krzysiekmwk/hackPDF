import socket
import select
from core import messages


class ClientMessages:

    def __init__(self):
        self.last_message = ""
        self.all_messages = []
        self.address = ""


class Server:
    IP = "127.0.0.1"
    PORT = 1234

    def __init__(self):
        self.client_list = {}
        self.sockets_list = []
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((Server.IP, Server.PORT))
        self.server_socket.listen()

        # List of sockets for select.select()
        self.sockets_list = [self.server_socket]
        print(f'Start listening for connections on {Server.IP}:{Server.PORT}...')

    def receive_messages_or_add_active_socket(self, time_out):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, time_out)

        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == self.server_socket:
                client_socket, client_address = self.server_socket.accept()
                self.sockets_list.append(client_socket)
                self.client_list[client_socket] = ClientMessages()
                self.client_list[client_socket].address = '{}:{}'.format(*client_address)

                print('Accepted new connection from {}:{}'.format(*client_address))

            # Else existing socket is sending a message
            else:

                # Receive message
                message = messages.receive_message(notified_socket)

                # If False, client disconnected, cleanup
                if message is False:
                    print('Closed connection from: {}'.format(self.client_list[notified_socket].address))
                    # Remove from un active socket from lists
                    self.remove_socket(notified_socket)
                    continue

                self.client_list[notified_socket].last_message = message["data"]
                self.client_list[notified_socket].all_messages.append(message["data"])

                # Get user by notified socket, so we will know who sent the message
                client_address = self.client_list[notified_socket].address
                print(f'Received message from {client_address}: {message["data"]}')

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:
            self.remove_socket(notified_socket)

    def remove_socket(self, socket_to_remove):
        if socket_to_remove in self.sockets_list:
            self.sockets_list.remove(socket_to_remove)
        self.client_list.pop(socket_to_remove, None)

    def close(self):
        self.server_socket.close()

    def handle_messages(self):
        while True:
            self.receive_messages_or_add_active_socket(1)

    def upload_pdf_to_client(self, pdf_path):
        with open(pdf_path, mode='rb') as pdf:
            for client in self.client_list.keys():
                messages.send_message("CMD:SEND_PDF_FILE", client)
                messages.send_message(pdf.read(), client, send_binary_data=True)


if __name__ == '__main__':
    '''server = Server()
    server.start()

    while True:
        for client in server.client_list.values():
            if client.last_message == "HELLO":
                print(client.all_messages)

        server.receive_messages_or_add_active_socket()'''
