from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi


class BM25Store:

    def __init__(self):
        self.documents = []
        self.metadata = []
        self.index = None

    def build(self, metadata: list):

        self.metadata = metadata

        if not metadata:
            self.documents = []
            self.index = None
            return

        self.documents = [
            word_tokenize(item["content"].lower())
            for item in metadata
        ]

        self.index = BM25Okapi(self.documents)
        
    def search(
        self,
        query: str,
        top_k: int = 10,
    ):

        if self.index is None:
            return []

        tokens = word_tokenize(query.lower())

        scores = self.index.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            self.metadata[idx]
            for idx, _ in ranked[:top_k]
        ]