import numpy as np
from app.ai.embedding.model import embedding_model
from app.core.config import settings

class EmbeddingService:
    def embed_text(self, text: str) -> np.ndarray:
        if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
            vector = embedding_model.embed_query(text)
            return np.array(vector, dtype=np.float32)
        else:
            vector = embedding_model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            return vector

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        if settings.USE_NVIDIA and settings.NVIDIA_API_KEY:
            vectors = embedding_model.embed_documents(texts)
            return np.array(vectors, dtype=np.float32)
        else:
            vectors = embedding_model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            return vectors