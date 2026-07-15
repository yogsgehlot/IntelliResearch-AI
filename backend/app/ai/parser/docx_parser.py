from docx import Document
from app.ai.parser.base_parser import BaseParser

class DOCXParser(BaseParser):
    def parse(self, path: str):
        document = Document(path)
        text = "\n".join(p.text for p in document.paragraphs)
        return text