import os
from decrypt.dictionary_technique import DictionaryTechnique
#from decrypt.brute_force import BruteForce
from decrypt.decrypting_technique import DecryptingTechnique
from core.commands import Commands
from core.client_setup import ClientSetup


class DecryptFactory:
    def __init__(self):
        self.client_setup = ClientSetup()
        # TODO - saved path can be None before start - change it
        self.saved_pdf_file_path = None
        self.last_command = None
        #self.client_setup.decode_type = Commands.get_value(command, Commands.DECODE_TYPE)"""

    def setup_client(self, command):
        self.client_setup.count_of_clients = int(Commands.get_value(command, Commands.COUNT_OF_CLIENTS))
        self.client_setup.current_client = int(Commands.get_value(command, Commands.CURRENT_CLIENT))
        self.last_command = command

    def create_decrypt_object(self):
        decrypt_type = None

        if Commands.get_value(self.last_command, Commands.DICTIONARY):
            print(os.getcwd())
            dict_path = "decrypt" + os.sep + "dictionaries" + os.sep + "very_small.txt"
            decrypt_type = DictionaryTechnique(self.saved_pdf_file_path, self.client_setup, dict_path)

        if Commands.get_value(self.last_command, Commands.BRUTE_FORCE):
            pass
            #decrypt_type =

        return decrypt_type