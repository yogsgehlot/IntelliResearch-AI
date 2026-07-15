import numpy as np

from app.ai.embedding.model import embedding_model

class EmbeddingService:
    def embed_text(self, text: str) -> np.ndarray:
        vector = embedding_model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vector

    def embed_batch(self,texts: list[str],) -> np.ndarray:
        vectors = embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vectors