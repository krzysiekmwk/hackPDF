from core.server_controller import ServerController
from core.client_controller import ClientController
import threading
from core import messages
from core.commands import Commands


class MainController:

    def __init__(self):
        self.server = ServerController()

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
        my_client = ClientController(ServerController.IP, ServerController.PORT)
        my_client.connect_to_server()
        my_client.handle_commands()


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

        print("SETUP CLIENT")
        controller.server.setup_client(Commands.DICTIONARY)

        print("Sending pdf")
        controller.server.upload_pdf_to_client(path_to_PDF_file)
        print("Start decrypt pdf")
        controller.server.start_decrypt()

        import time
        start_time = time.time()
        while True:
            controller.server.receive_messages_or_add_active_socket(1)
            for client in controller.server.client_list.values():
                if len(client.all_messages) > 0:
                    end_time = time.time()
                    print(client.all_messages)
                    client.all_messages.clear()
                    print(end_time - start_time)
                    print("CLOSE YOUR CLIENT. TRY AGAIN...")
            if len(controller.server.client_list.keys()) < 1:
                break
