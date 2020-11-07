from core.server_controller import ServerController
from core.client_controller import ClientController
from core.commands import Commands
import argparse


class MainController:

    def __init__(self):
        self.server = ServerController()

    def start_server(self):
        self.server.start()

    def show_results(self):
        import time
        start_time = time.time()
        while True:
            self.server.receive_messages_or_add_active_socket(1)
            for client in self.server.client_list.values():
                for msg in client.all_messages:
                    if Commands.get_value(msg, Commands.FOUND_PASSWORD):
                        end_time = time.time()
                        print("Found password !")
                        print(client.all_messages)
                        client.all_messages.clear()
                        print(end_time - start_time)
                        self.server.stop_decrypt()
                        print("CLOSE YOUR CLIENT. TRY AGAIN...")
            if len(self.server.client_list.keys()) < 1:
                break

    def start(self):
        print("Start decrypt pdf")
        self.server.start_decrypt()

    def upload_pdf_file(self, path_to_pdf_file):
        print("Sending pdf")
        self.server.upload_pdf_to_client(path_to_pdf_file)

    def choose_decode_method(self, decrypt_option):
        print("Setup clients")
        self.server.setup_clients(decrypt_option)

    def wait_for_clients(self, num_of_clients):
        print(f"Wait for {num_of_clients} clients...")

        self.server.receive_messages_or_add_active_socket(1)
        current_num_of_clients = len(self.server.client_list.keys())
        last_num_of_clients = 0

        while current_num_of_clients < int(num_of_clients):
            self.server.receive_messages_or_add_active_socket(1)
            current_num_of_clients = len(self.server.client_list.keys())

            if last_num_of_clients > current_num_of_clients:
                print("One client left :(")
                last_num_of_clients = current_num_of_clients
            if last_num_of_clients < current_num_of_clients:
                print("One client more!")
                last_num_of_clients = current_num_of_clients

        print("Start...")


def run_as_client():
    my_client = ClientController(ServerController.IP, ServerController.PORT)
    my_client.connect_to_server()
    my_client.handle_commands()


# TODO remove it to get user input
# PDF path, client counts, Technique
input_return = ["has1234.pdf", "1", r"BRUTE_FORCE:BRUTE_FORCE_REGEX:[\d]{XXX}:BRUTE_FORCE_MIN:3:BRUTE_FORCE_MAX:4"]
#input_return = ["has1234.pdf", "1", r"DICTIONARY:DICTIONARY_PATH:decrypt\\dictionaries\\very_small.txt"]
ret = 0
def input(*args):
    global ret
    if ret >= len(input_return):
        ret = 0
    val = input_return[ret]
    ret += 1
    return val


def main():
    controller = MainController()
    controller.start_server()

    while True:
        path_to_pdf_file = input("Give PDF path: ")
        controller.wait_for_clients(input())
        controller.choose_decode_method(input())
        controller.upload_pdf_file(path_to_pdf_file)

        controller.start()
        controller.show_results()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lets hack some PDFs')
    parser.add_argument('-c', help='Start as Client.', action='store_true')
    args = parser.parse_args()

    if args.c:
        run_as_client()
    else:
        main()







