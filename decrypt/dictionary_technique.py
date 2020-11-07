from decrypt.decrypting_technique import DecryptingTechnique
from core.client_setup import ClientSetup


class DictionaryTechnique(DecryptingTechnique):

    def __init__(self, pdf_file_path: str, client_setup: ClientSetup, dict_file_path: str):
        super().__init__(pdf_file_path, client_setup)
        self.dict_file_path = dict_file_path

    def _get_start_and_end_line_number(self):
        num_lines = sum(1 for _ in open(self.dict_file_path))
        chunks = num_lines // self.client_setup.count_of_clients
        if num_lines % self.client_setup.count_of_clients != 0:
            chunks += 1
        start = chunks * self.client_setup.current_client
        end = start + chunks

        return start, end

    def start_decode(self):
        print(self.dict_file_path)

        with open(self.dict_file_path) as file:
            start, end = self._get_start_and_end_line_number()
            current_line = 0

            line = file.readline()
            while line:
                if start <= current_line < end:
                    password = self.try_decode(line.strip())
                    yield password
                line = file.readline()
                current_line += 1
        return False
