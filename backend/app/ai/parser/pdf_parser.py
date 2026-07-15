import fitz
from app.ai.parser.base_parser import BaseParser

class PDFParser(BaseParser):
    def parse(self, path: str):
        document = fitz.open(path)
        text = ""
        for page in document:
            text += page.get_text()

        return text