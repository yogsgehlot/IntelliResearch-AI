from langdetect import detect

class LanguageDetector:

    @staticmethod
    def detect(text: str):
        try:
            return detect(text)

        except:
            return "unknown"