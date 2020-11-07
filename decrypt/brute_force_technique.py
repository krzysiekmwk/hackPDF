from decrypt.decrypting_technique import DecryptingTechnique
from core.client_setup import ClientSetup
import exrex


class BruteForce(DecryptingTechnique):

    def __init__(self, pdf_file_path: str, client_setup: ClientSetup, given_regex="", min_pass=None, max_pass=None):
        super().__init__(pdf_file_path, client_setup)
        self.pass_generator = exrex
        self.given_regex = given_regex
        self.min_pass = min_pass
        self.max_pass = max_pass

    def _get_start_and_end_line_number(self, rex):
        count_of_str = self.pass_generator.count(rex)
        # TODO remove?
        print("Regex: " + rex)
        print("Example: " + self.pass_generator.getone(rex))
        chunks = count_of_str // self.client_setup.count_of_clients
        if count_of_str % self.client_setup.count_of_clients != 0:
            chunks += 1
        start = chunks * self.client_setup.current_client
        end = start + chunks

        return start, end

    def start_decode(self):
        for val in range(int(self.min_pass), int(self.max_pass) + 1):
            new_regex = self.given_regex.replace('{XXX}', "{" + str(val) + "}")
            start, end = self._get_start_and_end_line_number(new_regex)
            for num, password in enumerate(self.pass_generator.generate(new_regex)):
                if start <= num < end:
                    yield self.try_decode(password)
        return False
