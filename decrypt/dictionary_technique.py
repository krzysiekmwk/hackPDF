import PyPDF2


class DictionaryTechnique:

    def __init__(self, dict_file, pdf_file):
        self.dict_file = dict_file
        self.pdf_file = pdf_file

    def start_decode(self):
        with open(self.dict_file) as file:
            line = file.readline()
            while line:
                password = self.try_decode(line.strip())
                if password:
                    return password
                line = file.readline()
        return False

    def try_decode(self, password):
        try:
            pdf_reader = PyPDF2.PdfFileReader(self.pdf_file)
            pdf_reader.decrypt(password)
            pdf_reader.getPage(0)
            return password
        except PyPDF2.utils.PdfReadError:
            return False
