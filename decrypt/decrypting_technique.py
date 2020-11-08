import abc
from core.client_setup import ClientSetup
import pikepdf


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
            pikepdf.open(self.pdf_file_path, password=password)
            return password
        except:
            return False
