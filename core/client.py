import socket
import errno
import sys
import os
from core import messages
from core.server import Server
from datetime import datetime
from decrypt.dictionary_technique import DictionaryTechnique
# from decrypt.brute_force import BruteForce


class Client:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.decode_type = None
        self.saved_pdf_file_path = ""

    def connect_to_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        self.server_socket.setblocking(False)
        print(f"Client connect to: {self.server_ip}:{self.server_port}")

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

    def receive_pdf_file(self):
        pdf_file = self.receive_message_from_server(get_binary_data=True)
        while not pdf_file:
            pdf_file = self.receive_message_from_server(get_binary_data=True)
        pdf_file = pdf_file['data']

        self.saved_pdf_file_path = datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + '-' + str(id(self)) + ".pdf"
        with open(self.saved_pdf_file_path, mode='wb') as file:
            file.write(pdf_file)

    def handle_commands(self):
        while True:
            command = self.receive_message_from_server(get_binary_data=False)
            if command:
                command = command['data']
                print(command)

            if command == "CMD:SEND_PDF_FILE":
                self.receive_pdf_file()

            if command == "CMD:START_DECRYPT":
                self.start_decode()

            if command == "SAY_HELLO":
                print("Sending Hello")
                messages.send_message("HELLO", self.server_socket)

    def start_decode(self):
        print(os.getcwd())
        dictionary = DictionaryTechnique("decrypt" + os.sep + "dictionaries" + os.sep + "very_small.txt",
                                         self.saved_pdf_file_path)
        password = dictionary.start_decode()
        if password:
            messages.send_message(f"CMD:FOUND_PASSWORD:{password}", self.server_socket)
        else:
            messages.send_message("CMD:NOT_FOUND_PASSWORD", self.server_socket)


if __name__ == '__main__':
    client = Client(Server.IP, Server.PORT)
    client.connect_to_server()
    client.handle_commands()
