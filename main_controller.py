from core.server import Server
from core.client import Client
import threading
from core import messages


class MainController:

    def __init__(self):
        self.server = Server()

    def start_server(self):
        self.server.start()

    def show_results(self):
        pass

    def start(self):
        pass

    def choose_decode_method(self):
        pass

    def upload_pdf_file(self):
        pass

    @staticmethod
    def run_as_client():
        my_client = Client(Server.IP, Server.PORT)
        my_client.connect_to_server()
        my_client.handle_commands()


def foo(server):
    threading.Timer(5, foo, args=(server,)).start()
    for sock_client, client_messages in server.client_list.items():
        print("Send SAY_HELLO to my: " + client_messages.address + " client")
        messages.send_message("SAY_HELLO", sock_client)


if __name__ == '__main__':
    controller = MainController()
    controller.start_server()
    # path_to_PDF_file = input("Give PDF path: ")
    path_to_PDF_file = "has1234.pdf"

    while True:
        print("Wait for clients...")
        controller.server.receive_messages_or_add_active_socket(1)
        while len(controller.server.client_list.keys()) < 1:
            controller.server.receive_messages_or_add_active_socket(1)

        print("Sending pdf")
        controller.server.upload_pdf_to_client(path_to_PDF_file)
        controller.server.start_decrypt()

        while True:
            controller.server.receive_messages_or_add_active_socket(1)
            for client in controller.server.client_list.values():
                if len(client.all_messages) > 0:
                    print(client.all_messages)
                    client.all_messages.clear()
            if len(controller.server.client_list.keys()) < 1:
                break


'''foo(controller.server)

while True:
    for client in controller.server.client_list.values():
        if client.last_message == "HELLO":
            print(client.all_messages)

    controller.server.receive_messages_or_add_active_socket()'''