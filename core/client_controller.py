import os
from core.client import Client
from datetime import datetime
from core.commands import Commands
from decrypt.decrypt_factory import DecryptFactory


class ClientController(Client):

    def __init__(self, server_ip, server_port):
        super().__init__(server_ip, server_port)
        self.decrypt_factory = DecryptFactory()

    def _receive_file(self):
        # TODO check bigger files
        # TODO check receiving data throgh network
        file = self.receive_message_from_server(get_binary_data=True)
        while not file:
            file = self.receive_message_from_server(get_binary_data=True)
        return file['data']

    def receive_pdf_file(self):
        pdf_file = self._receive_file()

        self.decrypt_factory.saved_pdf_file_path = 'downloaded_files' + os.sep + \
            datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + '-' + str(id(self)) + ".pdf"
        with open(self.decrypt_factory.saved_pdf_file_path, mode='wb') as file:
            file.write(pdf_file)

    def receive_file(self, file_name):
        received_file = self._receive_file()
        saved_file_path = 'downloaded_files' + os.sep + os.path.basename(file_name)

        with open(saved_file_path, mode='wb') as file:
            file.write(received_file)

    def _get_command(self):
        command = self.receive_message_from_server(get_binary_data=False)
        if command:
            command = command['data']
            print(command)

        return command

    def check_if_client_should_stop(self):
        command = self._get_command()

        if Commands.get_value(command, Commands.STOP_DECRYPT):
            return True
        return False

    def handle_commands(self):
        while True:
            command = self._get_command()

            if Commands.get_value(command, Commands.SEND_PDF_FILE):
                self.receive_pdf_file()

            if Commands.get_value(command, Commands.SEND_FILE):
                self.receive_file(Commands.get_value(command, Commands.SEND_FILE))

            if Commands.get_value(command, Commands.SETUP_CLIENT):
                self.decrypt_factory.setup_client(command)

            if Commands.get_value(command, Commands.START_DECRYPT):
                self.start_decode()
                # remove unnecessary pdf file
                os.remove(self.decrypt_factory.saved_pdf_file_path)
                # TODO - at this moment our client ends job after found password
                return

    def start_decode(self):
        decrypt_type = self.decrypt_factory.create_decrypt_object()

        for password in decrypt_type.start_decode():
            if self.check_if_client_should_stop():
                return False
            if password:
                cmd = Commands.create_command(Commands.FOUND_PASSWORD, password)
                print(f"send message ->{cmd}")
                self.messages.send_message(cmd, self.server_socket)
                return True

        cmd = Commands.create_command(Commands.NOT_FOUND_PASSWORD)
        print(f"send message ->{cmd}")
        self.messages.send_message(cmd, self.server_socket)
        return False


