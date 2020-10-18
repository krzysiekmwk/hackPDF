import socket
import errno
import sys
import messages
from server import Server
import time

class Client:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.decode_type = None

    def connect_to_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        self.server_socket.setblocking(False)

    def receive_message_from_server(self, get_binary_data=False) -> dict:
        try:
            msg = messages.receive_message(self.server_socket, get_binary_data)
            if not msg:
                msg = {}

            return msg

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            return {}

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()

    def handle_commands(self):
        while True:
            command = client.receive_message_from_server(get_binary_data=False)
            if command:
                command = command['data']

            if command == "SAY_HELLO":
                print("Sending Hello")
                messages.send_message("HELLO", self.server_socket)

    def start_decode(self):
        pass


if __name__ == '__main__':
    client = Client(Server.IP, Server.PORT)
    client.connect_to_server()
    client.handle_commands()
