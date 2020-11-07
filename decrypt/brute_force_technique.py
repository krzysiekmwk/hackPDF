from decrypt.decrypting_technique import DecryptingTechnique
from core.client_setup import ClientSetup
import exrex


class BruteForce(DecryptingTechnique):

    def __init__(self, pdf_file_path: str, client_setup: ClientSetup):
        super().__init__(pdf_file_path, client_setup)
        self.pass_generator = exrex

    def _get_start_and_end_line_number(self):
        count_of_str = self.pass_generator.count(r'[\d]{4}')
        chunks = count_of_str // self.client_setup.count_of_clients
        if count_of_str % self.client_setup.count_of_clients != 0:
            chunks += 1
        start = chunks * self.client_setup.current_client
        end = start + chunks

        return start, end

    def start_decode(self):
        start, end = self._get_start_and_end_line_number()
        for num, password in enumerate(self.pass_generator.generate(r'[\d]{4}')):
            if start <= num < end:
                yield self.try_decode(password)
        return False
