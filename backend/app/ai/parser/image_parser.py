from app.ai.ocr.paddle_ocr import ocr
from app.ai.parser.base_parser import BaseParser

class ImageParser(BaseParser):
    def parse(self, path: str):
        result = ocr.ocr(path)
        text = ""
        for page in result:
            for line in page:
                text += line[1][0]
                text += "\n"
        return text