import numpy as np
from app.ai.embedding.embedding_service import EmbeddingService
from app.ai.vectorstore.faiss_store import FaissStore
from app.ai.vectorstore.metadata_store import MetadataStore

class RetrievalService:
    def __init__(self):
        self.embedding = EmbeddingService()
        self.store = FaissStore()
        self.metadata = MetadataStore()

    def search(self,query: str,top_k=5,):
        vector = self.embedding.embed_text(query)
        scores, ids = self.store.search(vector.reshape(1, -1),top_k,)
        metadata = self.metadata.load()
        results = []
        
        for idx in ids[0]:
            if idx == -1:
                continue

            results.append(metadata[idx])

        return results