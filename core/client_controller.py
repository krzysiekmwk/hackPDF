import os
from core.client import Client
from datetime import datetime
from core.commands import Commands
from decrypt.decrypt_factory import DecryptFactory
from core.server import Server


class ClientController(Client):

    def __init__(self, server_ip, server_port):
        super().__init__(server_ip, server_port)
        self.decrypt_factory = DecryptFactory()

    def receive_pdf_file(self):
        pdf_file = self.receive_message_from_server(get_binary_data=True)
        while not pdf_file:
            pdf_file = self.receive_message_from_server(get_binary_data=True)
        pdf_file = pdf_file['data']

        self.decrypt_factory.saved_pdf_file_path = \
            datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + '-' + str(id(self)) + ".pdf"
        with open(self.decrypt_factory.saved_pdf_file_path, mode='wb') as file:
            file.write(pdf_file)

    def handle_commands(self):
        while True:
            command = self.receive_message_from_server(get_binary_data=False)
            if command:
                command = command['data']
                print(command)

            if Commands.get_value(command, Commands.SEND_PDF_FILE):
                self.receive_pdf_file()

            if Commands.get_value(command, Commands.SETUP_CLIENT):
                self.decrypt_factory.setup_client(command)

            if Commands.get_value(command, Commands.START_DECRYPT):
                self.start_decode()

    def start_decode(self):
        # TODO: metods should yield values. In that case there will be possibility to
        # TODO: check handle_command method and then if neccessary stop finding next solution
        # TODO: simple case - other client just found solution
        decrypt_type = self.decrypt_factory.create_decrypt_object()

        password = decrypt_type.start_decode()
        if password:
            print(f"send message -> CMD:FOUND_PASSWORD:{password}")
            self.messages.send_message(f"CMD:FOUND_PASSWORD:{password}", self.server_socket)
        else:
            print("send message -> CMD:NOT_FOUND_PASSWORD")
            self.messages.send_message("CMD:NOT_FOUND_PASSWORD", self.server_socket)

        # remove unnecessary pdf file
        os.remove(self.decrypt_factory.saved_pdf_file_path)

if __name__ == '__main__':
    client = ClientController(Server.IP, Server.PORT)
    client.connect_to_server()
    client.handle_commands()
