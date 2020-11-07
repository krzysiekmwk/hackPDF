from core.server import Server
from core.commands import Commands


class ServerController(Server):
    def handle_messages(self):
        while True:
            self.receive_messages_or_add_active_socket(1)

    def upload_pdf_to_client(self, pdf_path):
        for client in self.client_list.keys():
            with open(pdf_path, mode='rb') as pdf:
                cmd = Commands.create_command(Commands.SEND_PDF_FILE)
                self.messages.send_message(cmd, client)
                self.messages.send_message(pdf.read(), client, send_binary_data=True)

    def start_decrypt(self):
        for client in self.client_list.keys():
            cmd = Commands.create_command(Commands.START_DECRYPT)
            self.messages.send_message(cmd, client)

    def stop_decrypt(self):
        for client in self.client_list.keys():
            cmd = Commands.create_command(Commands.STOP_DECRYPT)
            self.messages.send_message(cmd, client)

    def setup_clients(self, *args):
        for client_num, client in enumerate(self.client_list.keys()):
            cmd = Commands.create_command(Commands.SETUP_CLIENT,
                                          Commands.COUNT_OF_CLIENTS, len(self.client_list.keys()),
                                          Commands.CURRENT_CLIENT, client_num, args)
            self.messages.send_message(cmd, client)
