from app.ai.parser.docx_parser import DOCXParser
from app.ai.parser.image_parser import ImageParser
from app.ai.parser.pdf_parser import PDFParser
from app.ai.parser.txt_parser import TXTParser


class ParserFactory:
    parsers = {
        "pdf": PDFParser(),
        "docx": DOCXParser(),
        "txt": TXTParser(),
        "png": ImageParser(),
        "jpg": ImageParser(),
        "jpeg": ImageParser(),
    }

    @classmethod
    def get_parser(cls, extension: str):
        parser = cls.parsers.get(extension.lower())

        if parser is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return parser