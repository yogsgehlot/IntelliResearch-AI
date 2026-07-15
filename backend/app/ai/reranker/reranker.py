from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.model = CrossEncoder("BAAI/bge-reranker-base")

    def rerank(self,query: str,documents: list,top_k: int = 5,):
        pairs = [(query, doc["content"]) for doc in documents]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(scores, documents),reverse=True,key=lambda x: x[0],)
        return [doc for _, doc in ranked[:top_k]]