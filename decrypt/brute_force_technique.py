from decrypt.decode_file import DecodeFile
from decrypt.decrypting_technique import DecryptingTechnique


class BruteForce(DecryptingTechnique):

    def __init__(self, pdf_file_path: str):
        super().__init__(pdf_file_path)

    def start_decode(self):
        pass
