import re

class TextCleaner:
    @staticmethod
    def clean(text: str):
        text = re.sub(r"\s+"," ",text,)
        return text.strip()