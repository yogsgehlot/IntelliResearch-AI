import faiss
import numpy as np
from pathlib import Path
import threading

class FaissStore:
    INDEX_PATH = Path(__file__).resolve().parents[3] / "storage" / "faiss" / "index.bin"
    _lock = threading.Lock()

    def __init__(self):
        with self._lock:
            if self.INDEX_PATH.exists():
                self.index = faiss.read_index(str(self.INDEX_PATH))
                self.dimension = self.index.d
            else:
                from app.ai.embedding.embedding_service import EmbeddingService
                sample_vector = EmbeddingService().embed_text("test")
                self.dimension = len(sample_vector)
                self.index = faiss.IndexFlatIP(self.dimension)

    def add(self, vectors: np.ndarray):
        with self._lock:
            self.index.add(vectors)
            self.save_unlocked()

    def search(self, vector, top_k=5):
        with self._lock:
            if vector.shape[1] != self.index.d:
                raise ValueError(
                    f"Embedding dimension mismatch: query vector has {vector.shape[1]} dimensions, "
                    f"but the vector index has {self.index.d} dimensions. "
                    "Please rebuild the vector store by saving settings again or re-uploading documents."
                )
            scores, ids = self.index.search(vector, top_k)
            return scores, ids

    def save_unlocked(self):
        self.INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.INDEX_PATH))

    def save(self):
        with self._lock:
            self.save_unlocked()