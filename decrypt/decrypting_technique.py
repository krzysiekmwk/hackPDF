import abc
from core.client_setup import ClientSetup
import PyPDF2


class DecryptingTechnique(abc.ABC):

    @abc.abstractmethod
    def __init__(self, pdf_file_path: str, client_setup: ClientSetup):
        self.pdf_file_path = pdf_file_path
        self.client_setup = client_setup

    @abc.abstractmethod
    def start_decode(self):
        pass

    def try_decode(self, password):
        try:
            pdf_reader = PyPDF2.PdfFileReader(self.pdf_file_path)
            pdf_reader.decrypt(password)
            pdf_reader.getPage(0)
            return password
        except PyPDF2.utils.PdfReadError:
            return False