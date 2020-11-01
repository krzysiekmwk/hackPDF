import PyPDF2


class DecodeFile:
    def __init__(self, pdf_file_path: str, client_setup: ClientSetup):
        self.pdf_file_path = pdf_file_path
        self.client_setup = client_setup


