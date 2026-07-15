from app.ai.parser.base_parser import BaseParser

class TXTParser(BaseParser):
    def parse(self, path: str):
        with open(path,encoding="utf8") as f:
            return f.read()