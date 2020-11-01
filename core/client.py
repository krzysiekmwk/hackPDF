import socket
import errno
import sys
from core import messages


class Client:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.messages = messages

    def connect_to_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        self.server_socket.setblocking(False)
        print(f"Client connect to: {self.server_ip}:{self.server_port}")

    def receive_message_from_server(self, get_binary_data=False) -> dict:
        try:
            msg = self.messages.receive_message(self.server_socket, get_binary_data)
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
