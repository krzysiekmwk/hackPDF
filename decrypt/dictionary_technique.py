from decrypt.decrypting_technique import DecryptingTechnique
from core.client_setup import ClientSetup


class DictionaryTechnique(DecryptingTechnique):

    def __init__(self, pdf_file_path: str, client_setup: ClientSetup, dict_file_path: str):
        super().__init__(pdf_file_path, client_setup)
        self.dict_file_path = dict_file_path

    def start_decode(self):
        with open(self.dict_file_path) as file:
            line = file.readline()
            while line:
                password = self.try_decode(line.strip())
                if password:
                    return password
                line = file.readline()
        return False
